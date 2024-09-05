import logging

from homeassistant.helpers.entity import Entity, EntityCategory, DeviceInfo
from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from ..api.myfoxapi import MyFoxApiClient
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)


from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)

class MyFoxAbstractEntity(CoordinatorEntity, Entity):

    def __init__(self, client: MyFoxApiClient, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, context=str(device.device_info.deviceId)+"|"+key)
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._client: MyFoxApiClient = client
        self._device: BaseDevice = device
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._device.device_info.deviceId}")},
            manufacturer="MyFox",
            name=self._device.device_info.label,
            model=self._device.device_info.modelLabel,
            model_id=self._device.device_info.modelId,
            serial_number=str(self._device.device_info.deviceId),
        )

class BaseSensorEntity(SensorEntity, MyFoxAbstractEntity):

    def __init__(self, client: MyFoxApiClient, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(client, coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            _LOGGER.debug("init value : %s, %s", self.idx, self.coordinator.data[self.idx])
            self._attr_native_value = self.coordinator.data[self.idx]

class BaseNumberEntity(NumberEntity, MyFoxAbstractEntity):
    pass

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractEntity):
    pass

class BaseSelectEntity(SelectEntity, MyFoxAbstractEntity):
    pass

class BaseButtonEntity(ButtonEntity, MyFoxAbstractEntity):
    pass