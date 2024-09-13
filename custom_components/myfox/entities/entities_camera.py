import logging

from homeassistant.components.camera import Camera

from . import MyFoxAbstractCameraEntity
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseCameraEntity(MyFoxAbstractCameraEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)


class ImageCameraEntity(BaseCameraEntity) :

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        coordinator:MyFoxCoordinator = self.coordinator
        return await coordinator.cameraPreviewTake(self.idx)
    

class StreamCameraEntity(BaseCameraEntity) :

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        coordinator:MyFoxCoordinator = self.coordinator
        return await coordinator.cameraLiveStart(self.idx)["location"]