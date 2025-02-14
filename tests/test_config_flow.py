"""Tests config_flow"""
from typing import Final
from unittest.mock import AsyncMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import (
    SOURCE_USER
)
from homeassistant.const import (
    CONF_HOST
)
from homeassistant.data_entry_flow import FlowResultType

DOMAIN_MYFOX: Final = "myfox"

async def test_full_flow(
    hass: HomeAssistant,
    mock_myfoxApiClient: AsyncMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test full flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN_MYFOX,
        context={"source": SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "10.0.0.131"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My integration"
    assert result["data"] == {
        CONF_HOST: "10.0.0.131",
    }