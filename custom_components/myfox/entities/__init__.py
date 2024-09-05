
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
            identifiers={(DOMAIN_MYFOX, f"{self._device.device_info.modelId}")},
            manufacturer="MyFox",
            name=self._device.device_info.label,
            model=self._device.device_info.modelLabel,
            serial_number=str(self._device.device_info.deviceId),
        )

class BaseSensorEntity(SensorEntity, MyFoxAbstractEntity):
    pass

class BaseNumberEntity(NumberEntity, MyFoxAbstractEntity):
    pass

class BaseSwitchEntity(SwitchEntity, MyFoxAbstractEntity):
    pass

class BaseSelectEntity(SelectEntity, MyFoxAbstractEntity):
    pass

class BaseButtonEntity(ButtonEntity, MyFoxAbstractEntity):
    pass