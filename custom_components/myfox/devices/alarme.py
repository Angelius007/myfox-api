import logging

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity

from ..devices import BaseDevice, MyFoxDeviceInfo
from ..entities.entities_select import SecuritySelectEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class MyFoxAlarmeDevice(BaseDevice) :
    """ """

    def __init__(self, device_info:MyFoxDeviceInfo):
        super().__init__(device_info)

    def selects(self, coordinator) -> list[SelectEntity]:
        _LOGGER.debug("Ajout SecuritySelectEntity sur device %s", str(self.device_info.deviceId))
        return [SecuritySelectEntity(coordinator, self, f"{self.device_info.label}", "status")]
