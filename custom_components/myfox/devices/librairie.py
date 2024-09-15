from dataclasses import dataclass

from ..devices import BaseDevice, MyFoxDeviceInfo

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
class MyFoxLibrairieDevice(BaseDevice) :
    """" """
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)