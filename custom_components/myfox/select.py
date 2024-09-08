import logging

from homeassistant.components.select import (SelectEntity)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (DOMAIN_MYFOX, HEATER_OPTIONS)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi import (MyFoxApiClient)
from .entities import DictStateBaseSelectEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = client_item

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.selects(coordinator))

class HeaterSelectEntity(DictStateBaseSelectEntity):
    _attr_device_class = SelectEntity
    _attr_entity_category = EntityCategory.CONFIG
    _options_dict: dict[str, str] = HEATER_OPTIONS

    @property
    def icon(self) -> str | None:
        if self.state() == "on": 
            return "mdi:radiator"
        elif self.state() == "eco": 
            return "mdi:radiator"
        elif self.state() == "off": 
            return "mdi:radiator-off"
        elif self.state() == "frost": 
            return "mdi:radiator-disabled"
        else:
            return "mdi:radiator-disabled"