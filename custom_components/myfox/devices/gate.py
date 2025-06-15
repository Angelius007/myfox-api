import logging
from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_button import PerformButtonEntity

_LOGGER = logging.getLogger(__name__)

# Gate {
# deviceId (integer): The device identifier,
# label (string): The device label,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }


@dataclass
class MyFoxGateDevice(BaseDevice):
    """ """
    def __init__(self, device_info: MyFoxDeviceInfo):
        super().__init__(device_info)

    def buttons(self, coordinator) -> list[ButtonEntity]:
        _LOGGER.debug("Ajout PerformButtonEntity sur device %s", str(self.device_info.deviceId))
        return [PerformButtonEntity(coordinator, self, f"One - {self.device_info.label}", "performeOne"),
                PerformButtonEntity(coordinator, self, f"Two - {self.device_info.label}", "performeTwo")]
