"""NiceGUI front-end for the thermal chamber demo.

This module wires UI controls to the async gRPC bridge and renders live status,
stream indicators, and a rolling temperature chart.
"""

import asyncio
import atexit
import time
from collections import deque
from nicegui import ui, app

from grpc_client_async import GrpcBridgeAsync

TARGET = "127.0.0.1:50051"  # gRPC server address
grpcb = GrpcBridgeAsync(TARGET)  # shared gRPC bridge instance

grpc_task_started = False  # ensure connect loop is started only once


def _cleanup():
    """Best-effort cleanup to close gRPC resources on exit."""
    try:
        asyncio.run(grpcb.close())
    except RuntimeError:
        pass


atexit.register(_cleanup)


@ui.page("/")
def index():
    """Main page layout and UI logic."""
    global grpc_task_started
    if not grpc_task_started:
        grpc_task_started = True
        # Background task that keeps the client connected.
        asyncio.create_task(grpcb.connect_loop())

    ui.label("Thermal Chamber WebUI").classes("text-2xl font-semibold")

    # --- connection indicators (visual) ---
    with ui.row().classes("items-center gap-3"):
        conn_badge = ui.badge("DISCONNECTED").props("color=red-6 text-color=white")
        stream_badge = ui.badge("NO STREAM").props("color=red-6 text-color=white")
        ui.label(TARGET).classes("text-sm text-gray-500")

    # --- controls ---
    with ui.row().classes("gap-2"):
        btn_start = ui.button(
            "Start", on_click=lambda: asyncio.create_task(grpcb.start_module())
        )
        btn_stop = ui.button(
            "Stop", on_click=lambda: asyncio.create_task(grpcb.stop_module())
        )
        btn_show = ui.button(
            "Show Panel", on_click=lambda: asyncio.create_task(grpcb.show_panel())
        )
        btn_hide = ui.button(
            "Hide Panel", on_click=lambda: asyncio.create_task(grpcb.hide_panel())
        )

    with ui.row().classes("gap-6 items-end"):
        ui.label("Temperature Set Point (°C)").classes("text-sm text-gray-600")
        sp = ui.slider(min=0.0, max=100.0, step=0.1, value=22.0).props(
            "label label-always"
        )
        with ui.column().classes("items-start"):
            ui.label("Ramp Rate (°C/s)").classes("text-sm text-gray-600")
            rr = ui.radio(
                {
                    1: "1 °C/s",
                    5: "5 °C/s",
                    10: "10 °C/s",
                },
                value=1,
            ).props("inline")

    with ui.row().classes("gap-2"):
        heater_switch = ui.switch("Heater", value=False)

    # --- live values ---
    with ui.row().classes("gap-6 items-center"):
        actual_lbl = ui.label("Actual Temperature: -- °C").classes("text-xl")
        info_lbl = ui.label("").classes("text-sm text-gray-500")

    # --- live plot (last 60 seconds) ---
    ui.label("Actual Temperature (last 60s)").classes("text-sm text-gray-600 mt-2")
    temp_history = deque()
    plot = ui.echart(
        {
            "grid": {"left": "10%", "right": "5%", "bottom": "12%", "top": "18%"},
            "xAxis": {"type": "time", "axisLabel": {"rotate": 90}},
            "yAxis": {"type": "value", "name": "°C"},
            "series": [
                {
                    "type": "line",
                    "name": "Actual Temperature",
                    "showSymbol": False,
                    "data": [],
                }
            ],
            "tooltip": {"trigger": "axis"},
        }
    ).classes("w-[500px] ml-0")

    def set_controls_enabled(enabled: bool):
        """Enable/disable all interactive controls based on connectivity."""
        for w in (btn_start, btn_stop, btn_show, btn_hide, sp, rr, heater_switch):
            w.enabled = enabled

    def set_badge_colors(badge, bg: str, text: str):
        """Apply Quasar badge colors (NiceGUI uses Quasar under the hood)."""
        badge.props(f"color={bg} text-color={text}")

    set_controls_enabled(False)

    # apply inputs (only when connected)
    async def apply_setpoint():
        """Send setpoint to server."""
        await grpcb.update_setpoint(float(sp.value))

    async def apply_ramprate():
        """Send ramp rate to server."""
        await grpcb.update_ramprate(float(rr.value))

    sp.on(
        "change",
        lambda _: asyncio.create_task(apply_setpoint()) if grpcb.is_connected else None,
    )
    rr.on_value_change(
        lambda _: asyncio.create_task(apply_ramprate()) if grpcb.is_connected else None
    )

    def on_heater_toggle(e):
        """Toggle heater state on the server."""
        value = e.value
        if grpcb.is_connected:
            asyncio.create_task(grpcb.set_heater(bool(value)))

    heater_switch.on_value_change(on_heater_toggle)

    # --- refresh UI every 100ms ---
    async def refresh():
        """Pull latest snapshot and update UI widgets."""
        s = await grpcb.snapshot()

        # connection badge
        if grpcb.is_connected:
            conn_badge.text = "CONNECTED"
            set_badge_colors(conn_badge, "green-6", "black")
            set_controls_enabled(True)
        else:
            conn_badge.text = "DISCONNECTED"
            set_badge_colors(conn_badge, "red-6", "white")
            set_controls_enabled(False)

        # stream badge
        if s.stream_ok:
            stream_badge.text = "STREAM OK"
            set_badge_colors(stream_badge, "green-6", "black")
        else:
            stream_badge.text = "NO STREAM"
            set_badge_colors(stream_badge, "red-6", "white")

        # values
        if s.stream_ok:
            actual_lbl.text = f"Actual Temperature: {s.actual_temperature:.1f} °C"
            info_lbl.text = (
                f"SP={s.temperature_set_point:.2f} °C | "
                f"Rate={s.temperature_ramp_rate:.2f} °C/s | "
                f"Heater={s.heater_state}"
            )
        else:
            actual_lbl.text = "Actual Temperature: -- °C"
            info_lbl.text = f"SP= -- °C | " f"Rate= -- °C/s | " f"Heater= --"

        # update plot data (keep last 60 seconds)
        if s.stream_ok:
            now_ms = int(time.time() * 1000)
            temp_history.append((now_ms, float(s.actual_temperature)))
            cutoff = now_ms - 60_000
            while temp_history and temp_history[0][0] < cutoff:
                temp_history.popleft()
            plot.options["series"][0]["data"] = list(temp_history)
            plot.update()

    # Periodic UI refresh loop.
    ui.timer(0.1, lambda: asyncio.create_task(refresh()))


# Start the NiceGUI server.
ui.run(host="127.0.0.1", port=8081, title="Thermal Chamber WebUI", reload=False)
