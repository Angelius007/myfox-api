import logging

from homeassistant.components.sensor import (SensorDeviceClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api.myfoxapi import (MyFoxApiClient)
from .const import (DOMAIN_MYFOX, HEATER_OPTIONS)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .devices import BaseDevice
from .entities import DictStateBaseSelectEntity,DictStateStrBaseSensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des switchs """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = client_item

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.selects(coordinator))

class HeaterSensorEntity(DictStateStrBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, str] = HEATER_OPTIONS

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key, options)
    
    #@property
    #def icon(self) -> str | None:
    #    if self._attr_native_value in HEATER_OPTIONS:
    #        if self._attr_native_value == "ON": 
    #            return "mdi:radiator"
    #        elif self._attr_native_value == "OFF": 
    #            return "mdi:radiator-off"
    #        elif self._attr_native_value == "Mode ECO": 
    #            return "mdi:radiator"
    #        elif self._attr_native_value == "Hors GEL": 
    #            return "mdi:radiator-disabled"
    #        else:
    #            return "mdi:radiator-disabled"
    #    else :
    #        return "mdi:radiator-disabled"
        
class HeaterSelectEntity(DictStateBaseSelectEntity):
    _options_dict: dict[str, str] = HEATER_OPTIONS

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key, options)
        self._attr_current_option = None
        
    def current_option(self) -> str | None:
        return self._attr_current_option
    
    #@property
    #def icon(self) -> str | None:
    #    current_option = self.current_option()
    #    if current_option in HEATER_OPTIONS:
    #        if current_option == "ON": 
    #            return "mdi:radiator"
    #        elif current_option == "OFF": 
    #            return "mdi:radiator-off"
    #        elif current_option == "Mode ECO": 
    #            return "mdi:radiator"
    #        elif current_option == "Hors GEL": 
    #            return "mdi:radiator-disabled"
    #        else:
    #            return "mdi:radiator-disabled"
    #    else :
    #        return "mdi:radiator-disabled"