import logging

from homeassistant.components.camera import Camera

from . import MyFoxAbstractCameraEntity
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseCameraEntity(MyFoxAbstractCameraEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)


class MyFoxCameraEntity(BaseCameraEntity) :

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        coordinator:MyFoxCoordinator = self.coordinator
        return await coordinator.cameraPreviewTake(self.idx)
    
    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        coordinator:MyFoxCoordinator = self.coordinator
        info_stream = await coordinator.cameraLiveStart(self.idx, "hls")
        if info_stream :
            return info_stream["location"]
        else :
            return None
    
    async def async_turn_off(self) -> None:
        self._attr_is_streaming = False
        self._attr_is_on = True
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.cameraLiveStop(self.idx)
        info_stream = await coordinator.cameraLiveStart(self.idx)
        self.stream.update_source(info_stream)
        
    async def async_turn_on(self) -> None:
        self._attr_is_streaming = False
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.cameraLiveStop(self.idx)
        info_stream = await coordinator.cameraLiveStart(self.idx)
        self.stream.update_source(info_stream)