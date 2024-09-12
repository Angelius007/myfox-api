from dataclasses import dataclass

from homeassistant.components.camera import Camera

from ..devices import  BaseDevice
from ..entities.entities_camera import BaseCameraEntity

#Camera {
#"deviceId": 1027535,
#"label": "Séjour",
##"resolutionHeight": null,
#"resolutionWidth": null,
#"modelId": 5,
#"modelLabel": "Panasonic BL-C131",
#"hideTimeLine": true
#}
@dataclass
class MyFoxCamera :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    hideTimeLine: bool
    resolutionHeight: int | None = None
    resolutionWidth: int | None = None
    guid: str | None = None
    protocol: str | None = None
    location: str | None = None
    #"GUID": "0080f0bdd5585db987a1075d04a0ce03",
    #"protocol": "hls",
    #"location": "https://myfox.me/live/0080f0bdd5585db987a1075d04a0ce03/index.m3u8"
    # OU
    #"GUID": "0080f0bdd5589177c12f436a39a94c1c",
    #"protocol": "rtmp",
    #"location": "rtmp://tag-shcprtmp-02.ig-1.net/myfox/0080f0bdd5589177c12f436a39a94c1c"


@dataclass
class MyFoxCameraDevice(BaseDevice):
    """ """
    camera:MyFoxCamera = None

    def cameras(self, coordinator) -> list[Camera]:
        return [BaseCameraEntity(coordinator, self, self.device_info.label, "camera")]