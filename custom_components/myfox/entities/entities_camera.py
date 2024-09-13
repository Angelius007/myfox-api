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
        if self.stream:
            """ verification si un stream est en cours ou en ano """
            _LOGGER.debug("Source : %s", self.stream.source)
            if self.stream._available:
                _LOGGER.debug("Stream actif")
            else :
                _LOGGER.debug("Stream non accessible. On coupe")
                await self.stream.stop()
                self._attr_is_streaming = False
                self.stream = None
            
        coordinator:MyFoxCoordinator = self.coordinator
        return await coordinator.cameraPreviewTake(self.idx)
    
    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        coordinator:MyFoxCoordinator = self.coordinator
        info_stream = await coordinator.cameraLiveStart(self.idx, "hls")
        if info_stream :
            self._attr_is_streaming = True
            _LOGGER.debug("Démarrage du stream sur : %s", str(info_stream))
            return info_stream["location"]
        else :
            return None
