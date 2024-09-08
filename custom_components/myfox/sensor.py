import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (UnitOfTemperature)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (STATE_OK, STATE_PROBLEM, STATE_UNAVAILABLE)

from .const import (DOMAIN_MYFOX, ALERTE_OPTIONS, ONLINE_OPTIONS, LIGHT_OPTIONS)
from .api.myfoxapi import (MyFoxApiClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .entities import BaseSensorEntity,DictStateBaseSensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Chargement des sensors """
    coordinator:MyFoxCoordinator = hass.data[DOMAIN_MYFOX][entry.entry_id]
    for (client_key,client_item) in coordinator.myfoxApiClient.items() :
        client: MyFoxApiClient = client_item

        for (deviceId, device) in client.devices.items():
            async_add_entities(device.sensors(coordinator))


class TempSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1


class LightSensorEntity(DictStateBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, int] = LIGHT_OPTIONS

    @property
    def icon(self) -> str | None:
        if self._attr_native_value in LIGHT_OPTIONS:
            if self._attr_native_value == "Pleine lumière": 
                return "mdi:weather-sunny"
            elif self._attr_native_value == "Lumière du jour": 
                return "mdi:weather-sunny"
            elif self._attr_native_value == "Lumière basse": 
                return "mdi:weather-partly-cloudy"
            elif self._attr_native_value == "Pénombre": 
                return "mdi:weather-cloudy"
            elif self._attr_native_value == "Obscurité": 
                return "mdi:weather-night"
            else:
                return "mdi:weather-sunny-off"
        else :
            return "mdi:eye"

class OnlineSateSensorEntity(DictStateBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, int] = ONLINE_OPTIONS

    @property
    def icon(self) -> str | None:
        if self._attr_native_value in ONLINE_OPTIONS:
            if self._attr_native_value == "Online": 
                return "mdi:toggle-switch"
            elif self._attr_native_value == "Offline": 
                return "mdi:toggle-switch-off"
            else:
                return "mdi:toggle-switch-off-outline"
        else :
            return "mdi:eye"


class AlerteSateSensorEntity(DictStateBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, int] = ALERTE_OPTIONS

    @property
    def icon(self) -> str | None:
        if self._attr_native_value in ALERTE_OPTIONS:
            if self._attr_native_value == "OK": 
                self.state = STATE_OK
                return "mdi:check-circle"
            elif self._attr_native_value == "ALERTE": 
                self.state = STATE_PROBLEM
                return "mdi:alert"
            else:
                self.state = STATE_UNAVAILABLE
                return "mdi:bell-outline"
        else :
            self.state = STATE_UNAVAILABLE
            return "mdi:eye"