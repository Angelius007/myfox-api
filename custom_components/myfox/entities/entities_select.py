import logging
from typing import Any

from homeassistant.components.select import SelectEntity

from . import BaseWithValueEntity
from ..const import (HEATER_OPTIONS, SECURITY_OPTIONS)
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseSelectEntity(SelectEntity, BaseWithValueEntity):
    pass

class DictStateBaseSelectEntity(BaseSelectEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key)
        if options :
            self._options_dict = options
        if self._options_dict :
            self._attr_options = list(self._options_dict.keys())
        self._attr_current_option = None

    def setOptions(self, options: dict[str, str]) :
        self._options_dict = options
        self._attr_options = list(self._options_dict.keys())

    def options_dict(self) -> dict[str, str]:
        return self._options_dict
    
    def getOptionValue(self, option:str) -> str:
        options = self.options_dict()
        if option in options :
            return options[option]
        else :
            return None
    
    def _update_value(self, val: Any) -> bool:
        if self._options_dict :
            sval = str(val)
            lval = [k for k, v in self._options_dict.items() if v == sval]
            if len(lval) == 1:
                self.current_option = lval[0]
                return True
            else:
                return False
        else :
            return False

    async def async_select_option(self, option: str):
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.selectOption(self.idx, self.getOptionValue(option))

class HeaterSelectEntity(DictStateBaseSelectEntity):
    _options_dict: dict[str, str] = HEATER_OPTIONS

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key, options)
    
    @property
    def icon(self) -> str | None:
        if self.current_option in HEATER_OPTIONS:
            if self.current_option == "ON": 
                return "mdi:radiator"
            elif self.current_option == "OFF": 
                return "mdi:radiator-off"
            elif self.current_option == "Mode ECO": 
                return "mdi:radiator"
            elif self.current_option == "Hors GEL": 
                return "mdi:radiator-disabled"
            else:
                return "mdi:radiator-disabled"
        else :
            return "mdi:radiator-disabled"

class SecuritySelectEntity(DictStateBaseSelectEntity):
    _options_dict: dict[str, str] = SECURITY_OPTIONS

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str, options: dict[str, str]=None):
        super().__init__(coordinator, device, title, key, options)
    
    @property
    def icon(self) -> str | None:
        if self.current_option in SECURITY_OPTIONS:
            if self.current_option == "Disarmed": 
                return "mdi:shield-outline"
            elif self.current_option == "Partial": 
                return "mdi:shield-half-full"
            elif self.current_option == "Armed": 
                return "mdi:shield-check"
            else:
                return "mdi:security"
        else :
            return "mdi:security"
