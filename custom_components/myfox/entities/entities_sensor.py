import logging
from typing import Any

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.const import (UnitOfTemperature)
from homeassistant.helpers.entity import EntityCategory

from . import BaseWithValueEntity
from ..const import (ALERTE_OPTIONS, ONLINE_OPTIONS, LIGHT_OPTIONS, HEATER_OPTIONS)
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseSensorEntity(SensorEntity, BaseWithValueEntity):
    pass

class DictStateBaseSensorEntity(BaseSensorEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, int]=None):
        super().__init__(coordinator, device, title, key)
        if options :
            self._options_dict = options
        if self._options_dict :
            self._attr_options = list(self._options_dict.keys())

    def setOptions(self, options: dict[str, int]) :
        self._options_dict = options
        self._attr_options = list(self._options_dict.keys())

    def options_dict(self) -> dict[str, int]:
        return self._options_dict
    
    def _update_value(self, val: Any) -> bool:
        if self._options_dict :
            ival = int(val)
            lval = [k for k, v in self._options_dict.items() if v == ival]
            if len(lval) == 1:
                self._attr_native_value = lval[0]
                return True
            else:
                return False
        else :
            return False

class DictStateStrBaseSensorEntity(BaseSensorEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key)
        if options :
            self._options_dict = options
        if self._options_dict :
            self._attr_options = list(self._options_dict.keys())

    def setOptions(self, options: dict[str, str]) :
        self._options_dict = options
        self._attr_options = list(self._options_dict.keys())

    def options_dict(self) -> dict[str, str]:
        return self._options_dict
    
    def _update_value(self, val: Any) -> bool:
        if self._options_dict :
            ival = str(val)
            lval = [k for k, v in self._options_dict.items() if v == ival]
            if len(lval) == 1:
                self._attr_native_value = lval[0]
                return True
            else:
                return False
        else :
            return False
        
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
            return "mdi:weather-sunny-off"

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
            return "mdi:toggle-switch-off-outline"

class HeaterSensorEntity(DictStateStrBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, str] = HEATER_OPTIONS

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key, options)
    
    @property
    def icon(self) -> str | None:
        if self._attr_native_value in HEATER_OPTIONS:
            if self._attr_native_value == "ON": 
                return "mdi:radiator"
            elif self._attr_native_value == "OFF": 
                return "mdi:radiator-off"
            elif self._attr_native_value == "Mode ECO": 
                return "mdi:radiator"
            elif self._attr_native_value == "Hors GEL": 
                return "mdi:radiator-disabled"
            else:
                return "mdi:radiator-disabled"
        else :
            return "mdi:radiator-disabled"
        
class AlerteSateSensorEntity(DictStateBaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _options_dict: dict[str, int] = ALERTE_OPTIONS

    @property
    def icon(self) -> str | None:
        if self._attr_native_value in ALERTE_OPTIONS:
            if self._attr_native_value == "OK": 
                return "mdi:check-circle"
            elif self._attr_native_value == "ALERTE": 
                return "mdi:alert"
            else:
                return "mdi:bell-outline"
        else :
            return "mdi:bell-outline"
