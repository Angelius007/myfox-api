import dataclasses
import logging
from abc import ABC

from homeassistant.components.scene import Scene
from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class MyFoxSceneInfo:
    scenarioId: int
    label: str
    typeLabel: str
    enabled: str


class BaseScene(ABC):

    scene_info: MyFoxSceneInfo = None

    def __init__(self, scene_info: MyFoxSceneInfo):
        super().__init__()
        self.scene_info = scene_info

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def scenes(self, coordinator) -> list[Scene]:
        return []

class DiagnosticScene(BaseScene):

    def switches(self, coordinator) -> list[SwitchEntity]:
        return []

    def scenes(self, coordinator) -> list[Scene]:
        return []
