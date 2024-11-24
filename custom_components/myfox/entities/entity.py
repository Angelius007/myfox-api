import logging
from typing import Any

from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.components.camera.const import StreamType

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.core import callback

from ..devices import BaseDevice
from ..scenes import BaseScene
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)


from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)

## ////////////////////////////////////////////////////////////////////////////
## DEVICES
## ////////////////////////////////////////////////////////////////////////////

class MyFoxAbstractDeviceEntity(CoordinatorEntity[MyFoxCoordinator], Entity):
    
    _attr_has_entity_name = True

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, context=str(device.device_info.deviceId)+"|"+key)
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._device: BaseDevice = device
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+title+"-"+self.idx

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

class BaseWithValueEntity(MyFoxAbstractDeviceEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        if self.idx in self.coordinator.data:
            self._update_value(coordinator.data[self.idx])
            
    def _update_value(self, val: Any) -> bool:
        self._attr_native_value = self.coordinator.data[self.idx]
        return True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            if self._update_value(self.coordinator.data[self.idx]) :
                self.async_write_ha_state()

## ////////////////////////////////////////////////////////////////////////////
## SCENES
## ////////////////////////////////////////////////////////////////////////////

class MyFoxAbstractSceneEntity(CoordinatorEntity[MyFoxCoordinator], Entity):

    _attr_has_entity_name = True

    def __init__(self, coordinator:MyFoxCoordinator, scene: BaseScene, title: str, key: str):
        super().__init__(coordinator, context=str(scene.scene_info.scenarioId)+"|"+key)
        self.idx = str(scene.scene_info.scenarioId)+"|"+key 
        self._scene: BaseScene = scene
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+title+"-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._scene.scene_info.scenarioId}-{self._scene.scene_info.typeLabel}")},
            manufacturer="MyFox",
            name=self._scene.scene_info.label,
            model=self._scene.scene_info.typeLabel,
            serial_number=str(self._scene.scene_info.scenarioId),
        )
    
class BaseSceneWithValueEntity(MyFoxAbstractSceneEntity):
    def __init__(self, coordinator:MyFoxCoordinator, scene: BaseScene, title: str, key: str):
        super().__init__(coordinator, scene, title, key)
        if self.idx in self.coordinator.data:
            self._update_value(coordinator.data[self.idx])
            
    def _update_value(self, val: Any) -> bool:
        self._attr_native_value = self.coordinator.data[self.idx]
        return True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.idx in self.coordinator.data:
            if self._update_value(self.coordinator.data[self.idx]) :
                self.async_write_ha_state()

## ////////////////////////////////////////////////////////////////////////////
## CAMERA
## ////////////////////////////////////////////////////////////////////////////

class MyFoxAbstractCameraEntity(Camera):

    _attr_has_entity_name = True
    
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__()
        self.idx = str(device.device_info.deviceId)+"|"+key 
        self._device: BaseDevice = device
        self.coordinator = coordinator
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+title+"-"+self.idx
        self._attr_frame_interval = 30 # 30 sec d'interval minimum entre deux mises a jour
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._attr_frontend_stream_type = StreamType.HLS

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