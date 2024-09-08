import dataclasses
import logging
from abc import ABC

from homeassistant.components.scene import Scene

#from .data_holder import MyFoxDataHolder

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

    def scenes(self, coordinator) -> list[Scene]:
        return []
    
class DiagnosticScene(BaseScene):

    def scenes(self, coordinator) -> list[Scene]:
        return []