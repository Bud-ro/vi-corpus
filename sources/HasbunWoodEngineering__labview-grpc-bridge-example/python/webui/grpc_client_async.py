"""Async gRPC bridge for the thermal chamber UI.

Provides command methods (unary RPCs) and stream listeners to keep a shared
UI state updated in the background.
"""

import asyncio
from dataclasses import dataclass
import grpc

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "python" / "gen"

for p in (GEN,):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import thermal_chamber_controller_dqmh_pb2 as pb2  # type: ignore
import thermal_chamber_controller_dqmh_pb2_grpc as pb2_grpc  # type: ignore


@dataclass
class ChamberUiState:
    """In-memory snapshot used by the UI layer."""

    actual_temperature: float = float("nan")
    temperature_set_point: float = 22.0
    temperature_ramp_rate: float = 1.0
    heater_state: int = pb2.HEATER_DISABLED
    stream_ok: bool = False


class GrpcBridgeAsync:
    """gRPC client wrapper with background listeners and a shared state."""

    def __init__(self, target: str):
        self.target = target
        self.channel: grpc.aio.Channel | None = None
        self.stub: pb2_grpc.ThermalChamberControllerStub | None = None

        self.state = ChamberUiState()
        self._lock = asyncio.Lock()
        self._reconnect_lock = asyncio.Lock()
        self._tasks: list[asyncio.Task] = []
        self._connected = False

    async def connect(self, timeout_s: float = 5.0) -> None:
        """One-shot connect helper (not used by the UI loop)."""
        self.channel = grpc.aio.insecure_channel(self.target)
        self.stub = pb2_grpc.ThermalChamberControllerStub(self.channel)
        await asyncio.wait_for(self.channel.channel_ready(), timeout=timeout_s)

    async def close(self) -> None:
        """Cancel listeners and close the channel."""
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        if self.channel:
            await self.channel.close()

    @property
    def is_connected(self) -> bool:
        """True when channel is currently healthy."""
        return self._connected

    async def connect_loop(self, retry_s: float = 2.0, timeout_s: float = 5.0) -> None:
        """Maintain a persistent connection and auto-reconnect on failures."""
        while True:
            try:
                if self.channel is None:
                    self.channel = grpc.aio.insecure_channel(self.target)
                    self.stub = pb2_grpc.ThermalChamberControllerStub(self.channel)

                async with self._lock:
                    self.state.stream_ok = False

                await asyncio.wait_for(self.channel.channel_ready(), timeout=timeout_s)
                self._connected = True

                while self._connected:
                    state_fn = (
                        getattr(self.channel, "get_state", None)
                        if self.channel
                        else None
                    )
                    if state_fn:
                        state = state_fn(False)
                        if state != grpc.ChannelConnectivity.READY:
                            self._connected = False
                            async with self._lock:
                                self.state.stream_ok = False
                            break
                    await asyncio.sleep(1)

            except Exception:
                await self._trigger_reconnect()
                await asyncio.sleep(retry_s)

    def _require(self):
        """Ensure the stub is available before making RPC calls."""
        if not self.stub:
            raise RuntimeError("Not connected")
        
    async def _trigger_reconnect(self):
        """Tear down the current connection and stop all listeners safely."""
        # Lock order rule:
        # Always acquire _reconnect_lock before _lock
        async with self._reconnect_lock:
            if not self._connected and self.channel is None:
                return

            self._connected = False
            async with self._lock:
                self.state.stream_ok = False

            current = asyncio.current_task()

            for t in self._tasks:
                if t is not current:
                    t.cancel()

            await asyncio.gather(
                *[t for t in self._tasks if t is not current],
                return_exceptions=True,
            )
            self._tasks.clear()

            if self.channel:
                try:
                    await self.channel.close()
                except Exception:
                    pass
            self.channel = None
            self.stub = None

    # ---- commands (Unary) ----
    async def start_module(self) -> None:
        """Start the simulated device and start stream listeners."""
        self._require()
        await self.stub.StartModule(pb2.Empty(), timeout=5)
        if not self._tasks:
            self.start_listeners()

    async def stop_module(self) -> None:
        """Stop the simulated device and stop stream listeners."""
        self._require()
        await self.stub.StopModule(pb2.Empty(), timeout=5)
        async with self._lock:
            self.state.stream_ok = False
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def show_panel(self) -> None:
        """Ask the server to show the LabVIEW panel (if supported)."""
        self._require()
        await self.stub.ShowModulePanel(pb2.Empty(), timeout=5)

    async def hide_panel(self) -> None:
        """Ask the server to hide the LabVIEW panel (if supported)."""
        self._require()
        await self.stub.HideModulePanel(pb2.Empty(), timeout=5)

    async def update_setpoint(self, value: float) -> None:
        """Send a new temperature setpoint to the server."""
        self._require()
        req = pb2.UpdateSetPointRequest(temperature_set_point=value)
        await self.stub.UpdateSetPoint(req, timeout=5)
        async with self._lock:
            self.state.temperature_set_point = value

    async def update_ramprate(self, value: float) -> None:
        """Send a new temperature ramp rate to the server."""
        self._require()
        req = pb2.UpdateRampRateRequest(temperature_ramp_rate=value)
        await self.stub.UpdateRampRate(req, timeout=5)
        async with self._lock:
            self.state.temperature_ramp_rate = value

    async def set_heater(self, enabled: bool) -> None:
        """Enable or disable the heater."""
        self._require()
        hs = pb2.HEATER_ENABLED if enabled else pb2.HEATER_DISABLED
        req = pb2.UpdateHeaterStateRequest(heater_state=hs)
        await self.stub.UpdateHeaterState(req, timeout=5)
        async with self._lock:
            self.state.heater_state = hs

    # ---- streams ----
    def start_listeners(self) -> None:
        """Start background stream listeners."""
        self._require()
        self._tasks = [
            asyncio.create_task(self._listen_status()),
            asyncio.create_task(self._listen_setpoint()),
            asyncio.create_task(self._listen_ramprate()),
            asyncio.create_task(self._listen_heater()),
        ]

    async def _listen_status(self) -> None:
        """Stream combined status updates."""
        self._require()
        try:
            async for msg in self.stub.SubscribeChamberStatusUpdated(pb2.Empty()):
                async with self._lock:
                    self.state.actual_temperature = msg.actual_temperature
                    self.state.temperature_set_point = msg.temperature_set_point
                    self.state.temperature_ramp_rate = msg.temperature_ramp_rate
                    self.state.heater_state = msg.heater_state
                    self.state.stream_ok = True
        except grpc.aio.AioRpcError:
            await self._trigger_reconnect()

    async def _listen_setpoint(self) -> None:
        """Stream setpoint-only updates."""
        self._require()
        try:
            async for msg in self.stub.SubscribeSetPointUpdated(pb2.Empty()):
                async with self._lock:
                    self.state.temperature_set_point = msg.temperature_set_point
        except grpc.aio.AioRpcError:
            await self._trigger_reconnect()

    async def _listen_ramprate(self) -> None:
        """Stream ramp-rate-only updates."""
        self._require()
        try:
            async for msg in self.stub.SubscribeRampRateUpdated(pb2.Empty()):
                async with self._lock:
                    self.state.temperature_ramp_rate = msg.temperature_ramp_rate
        except grpc.aio.AioRpcError:
            await self._trigger_reconnect()

    async def _listen_heater(self) -> None:
        """Stream heater-state-only updates."""
        self._require()
        try:
            async for msg in self.stub.SubscribeHeaterStateUpdated(pb2.Empty()):
                async with self._lock:
                    self.state.heater_state = msg.heater_state
        except grpc.aio.AioRpcError:
            await self._trigger_reconnect()

    async def snapshot(self) -> ChamberUiState:
        """Return a safe copy of the current UI state."""
        async with self._lock:
            return ChamberUiState(**self.state.__dict__)
