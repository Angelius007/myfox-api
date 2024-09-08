import logging

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_button import ShutterButtonEntity

_LOGGER = logging.getLogger(__name__)
#Shutter {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxShutter :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str

@dataclass
class MyFoxShuttereDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def buttons(self, coordinator) -> list[ButtonEntity]:
        _LOGGER.debug("Ajout buttons sur device %s", str(self.device_info.deviceId))
        return [ShutterButtonEntity(coordinator, self,f"Ouverture {self.device_info.label}", "open"),
                ShutterButtonEntity(coordinator, self, f"Fermeture {self.device_info.label}", "close")]
