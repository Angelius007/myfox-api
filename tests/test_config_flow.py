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
    hass: HomeAssistant
) -> None:
    """Test full flow."""
    assert True