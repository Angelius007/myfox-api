import logging

from homeassistant.components.camera import Camera

from . import MyFoxAbstractDeviceEntity
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseCameraEntity(Camera, MyFoxAbstractDeviceEntity):
    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)


    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        coordinator:MyFoxCoordinator = self.coordinator
        await coordinator.cameraPreviewTake(self.idx)