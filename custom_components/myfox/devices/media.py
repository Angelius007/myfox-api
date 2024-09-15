import logging
from dataclasses import dataclass

from homeassistant.components.media_player import MediaPlayerEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_media import ImageMediaEntity, VideoMediaEntity

_LOGGER = logging.getLogger(__name__)

#Image {
#imageId (integer): The image identifier,
#cameraId (integer): This value can be null if the camera has been uninstalled.,
#cameraLabel (integer): The label of the camera that has captured the image,
#height (integer): The image height in pixels,
#width (integer): The image width in pixels,
#createdAt (integer): The image creation date,
#fileURL (string): The download URL
#}

#Video {
#videoId (integer): The video identifier,
#cameraId (integer): The camera identifier,
#cameraLabel (string): The camera label,
#duration (integer): The video duration, in seconds,
#height (integer): The video height, in pixels,
#width (integer): The video width, in pixels,
#isRecording (boolean): Flag indicating if the video is currently recording,
#createdAt (integer): The video creation date,
#fileURL (string): The video file URL,
#playURL (string): URL to get informations for HLS playing,
#previewURL (string): The video preview file URL
#}

@dataclass
class MyFoxMediaDevice(BaseDevice):
    """ """
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def medias(self, coordinator) -> list[MediaPlayerEntity]:
        _LOGGER.debug("(inactif) Ajout ImageMediaEntity & VideoMediaEntity sur device %s", str(self.device_info.deviceId))
        #return [ImageMediaEntity(coordinator, self,f"Images - {self.device_info.label}", "images"),
        #        VideoMediaEntity(coordinator, self, f"Videos - {self.device_info.label}", "videos")]
        return []
