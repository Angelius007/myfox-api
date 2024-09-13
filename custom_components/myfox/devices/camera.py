from dataclasses import dataclass

from homeassistant.components.camera import Camera
from homeassistant.components.button import ButtonEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_camera import MyFoxCameraEntity
from ..entities.entities_button import CameraButtonEntity
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
    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def cameras(self, coordinator) -> list[Camera]:
        return [MyFoxCameraEntity(coordinator, self, f'{self.device_info.label}', "camera")]
    
    def buttons(self, coordinator) -> list[ButtonEntity]:
        return [CameraButtonEntity(coordinator, self, f'{self.device_info.label} Snapshot', "snapshot"),
                CameraButtonEntity(coordinator, self, f'{self.device_info.label} Rec Start', "recording_start"),
                CameraButtonEntity(coordinator, self, f'{self.device_info.label} Rec Stop', "recording_stop"),
                CameraButtonEntity(coordinator, self, f'{self.device_info.label} Live Start', "live_start"),
                CameraButtonEntity(coordinator, self, f'{self.device_info.label} Live Extend', "live_extend"),
                CameraButtonEntity(coordinator, self, f'{self.device_info.label} Live Stop', "live_stop")]
