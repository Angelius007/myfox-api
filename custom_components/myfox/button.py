import logging

from homeassistant.components.button import (ButtonDeviceClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (DOMAIN_MYFOX)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi import (MyFoxApiClient)
from .entities import BaseButtonEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = client_item

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.buttons(coordinator))

class ShutterButtonEntity(BaseButtonEntity):
    """ """
    _attr_device_class = ButtonDeviceClass.IDENTIFY
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def icon(self) -> str | None:
        if self.idx.endswith("open"):
            return "mdi:window-shutter-open"
        elif self.idx.endswith("close"):
            return "mdi:window-shutter"
        elif self.idx.endswith("my"):
            return "mdi:window-shutter-auto"
        else :
            return "mdi:eye"


class SocketButtonEntity(BaseButtonEntity):
    """ """
    _attr_device_class = ButtonDeviceClass.IDENTIFY
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def icon(self) -> str | None:
        if self.idx.endswith("on"):
            return "mdi:toggle-switch-variant"
        elif self.idx.endswith("off"):
            return "mdi:toggle-switch-variant-off"
        else :
            return "mdi:eye"
    