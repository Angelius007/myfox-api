import logging
from typing import Any

from homeassistant.helpers.entity import Entity, EntityCategory, DeviceInfo
from homeassistant.components.button import ButtonEntity
from homeassistant.components.light  import LightEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.core import callback

from ..api.myfoxapi import MyFoxApiClient
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)


from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)

class MyFoxAbstractEntity(CoordinatorEntity, Entity):

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, context=str(device.device_info.deviceId)+"|"+key)
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._client: MyFoxApiClient = coordinator.myfoxApiClient
        self._device: BaseDevice = device
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._device.device_info.deviceId}-{self._device.device_info.modelLabel}")},
            manufacturer="MyFox",
            name=self._device.device_info.label,
            model=self._device.device_info.modelLabel,
            model_id=self._device.device_info.modelId,
            serial_number=str(self._device.device_info.deviceId),
        )

class BaseWithValueEntity(MyFoxAbstractEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            statutok=self._update_value(coordinator.data[self.idx])
            _LOGGER.debug("init value : %s, %s : %s", self.idx, self.coordinator.data[self.idx], str(statutok))
            
    def _update_value(self, val: Any) -> bool:
        self._attr_native_value = self.coordinator.data[self.idx]
        return True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            _LOGGER.debug("_handle_coordinator_update : %s, %s", self.idx, self.coordinator.data[self.idx])
            if self._update_value(self.coordinator.data[self.idx]) :
                self.async_write_ha_state()

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

class BaseNumberEntity(NumberEntity, BaseWithValueEntity):
    pass

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractEntity):
    pass

class BaseSelectEntity(SelectEntity, BaseWithValueEntity):
    pass

class DictStateBaseSelectEntity(BaseSelectEntity):
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
                self._attr_current_option = lval[0]
                return True
            else:
                return False
        else :
            return False

    async def async_select_option(self, option: str):
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.selectOption(self.idx, self.getOptionValue(option))
    
class BaseButtonEntity(ButtonEntity, MyFoxAbstractEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    def press(self) -> None:
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        coordinator.deferredPressButton(self.idx)

    async def async_press(self) -> None:
        """Handle the button press."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.pressButton(self.idx)

class BaseLightEntity(LightEntity, MyFoxAbstractEntity):
    pass
