import logging

from .entity import MyFoxAbstractCameraEntity
from ..devices import BaseDevice
from ..api.myfoxapi_exception import (MyFoxException)
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)
 
class BaseCameraEntity(MyFoxAbstractCameraEntity):

    _attr_should_poll = False
    _unavailable_state: bool = False

    def __init__(self, coordinator:MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)


class MyFoxCameraEntity(BaseCameraEntity) :

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        if self.stream:
            """ verification si un stream est en cours ou en ano """
            if self.stream._available:
                _LOGGER.debug("Stream actif sur %s", self.stream.source)
            else :
                _LOGGER.debug("Stream non accessible. On coupe")
                self._attr_is_streaming = False
                await self.stream.stop()
                self.stream = None
            
        coordinator:MyFoxCoordinator = self.coordinator
        try:
            retour = await coordinator.cameraPreviewTake(self.idx)
            self._attr_available = True
            if self._unavailable_state:
                _LOGGER.info("The MyFoxCameraEntity-async_camera_image is back online")
                self._unavailable_state = False
            return retour
        except MyFoxException as ex:
            self._attr_available = False
            if not self._unavailable_state:
                _LOGGER.info("The MyFoxCameraEntity-async_camera_image is unavailable: %s", ex)
                self._unavailable_state = True

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        _LOGGER.debug("Recuperation source du Stream pour %s", str(self.idx))
        coordinator:MyFoxCoordinator = self.coordinator
        
        try:
            info_stream = await coordinator.cameraLiveStart(self.idx, "hls")
            self._attr_available = True
            # repasse le statut a ok
            if self._unavailable_state:
                _LOGGER.info("The MyFoxCameraEntity-stream_source is back online")
                self._unavailable_state = False
            # recupere le flux de stream
            if info_stream :
                self._attr_is_streaming = True
                return info_stream["location"]
            else :
                return None

        except MyFoxException as ex:
            # passe le statut a KO
            self._attr_available = False
            if not self._unavailable_state:
                _LOGGER.info("The MyFoxCameraEntity-stream_source is unavailable: %s", ex)
                self._unavailable_state = True