from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from ..devices import  BaseDevice

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


    def sensors(self, coordinator) -> list[SensorEntity]:
        return []

    def numbers(self, coordinator) -> list[NumberEntity]:
        return []

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def buttons(self, coordinator) -> list[ButtonEntity]:
        return []

    def selects(self, coordinator) -> list[SelectEntity]:
        return []

    def texts(self, coordinator) -> list[ButtonEntity]:
        return []