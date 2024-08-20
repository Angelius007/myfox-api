from dataclasses import dataclass

#Image {
#imageId (integer): The image identifier,
#cameraId (integer): This value can be null if the camera has been uninstalled.,
#cameraLabel (integer): The label of the camera that has captured the image,
#height (integer): The image height in pixels,
#width (integer): The image width in pixels,
#createdAt (integer): The image creation date,
#fileURL (string): The download URL
#}
@dataclass
class MyFoxImage :
    imageId: int
    cameraId: int
    cameraLabel: str
    height: int
    width: int  
    createdAt: str
    fileURL: str

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
class MyFoxVideo :
    videoId: int
    cameraId: int
    cameraLabel: str
    duration: int
    height: int
    width: int  
    isRecording: bool
    createdAt: str
    fileURL: str
    playURL: str
    previewURL: str
