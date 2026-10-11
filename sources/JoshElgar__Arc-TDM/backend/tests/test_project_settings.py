from __future__ import annotations

from app.core import project_settings


def test_default_agent_prompt_uses_workbook_vocabulary() -> None:
    prompt = project_settings.DEFAULT_AGENT_SYSTEM_PROMPT

    assert "Asset -> Run -> Workbook -> Steps -> Execution -> Outputs" in prompt
    assert "Do not use \"run\" to\n  mean Arc executing code" in prompt
    assert "Workbook Data" in prompt
    assert "workbook steps" in prompt
    assert "workflow" not in prompt.lower()


def test_default_agent_prompt_hides_underlying_infrastructure_from_users() -> None:
    prompt = project_settings.DEFAULT_AGENT_SYSTEM_PROMPT

    assert "Users should not need to know Arc's underlying infrastructure" in prompt
    assert "even if the user asks" in prompt
    assert "Arc handles that behind the scenes" in prompt
    assert "model providers" in prompt
    assert "environment variable names" in prompt


def test_default_agent_prompt_treats_analytics_as_charts() -> None:
    prompt = project_settings.DEFAULT_AGENT_SYSTEM_PROMPT

    assert "analytics" in prompt
    assert "visualisations" in prompt
    assert "visualizations" in prompt
    assert "possibly meaning charts" in prompt


def test_workbook_step_instruction_requires_decomposition_and_independence() -> None:
    prompt = project_settings.WORKBOOK_STEP_INSTRUCTION

    assert "one clear responsibility" in prompt
    assert "multiple ordered steps" in prompt
    assert "independently useful" in prompt
    assert "read the Workbook Data it needs directly" in prompt
    assert "Prefer a little repeated, obvious loading code" in prompt
    assert "It should not become one large step" in prompt
