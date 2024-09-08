import logging

from dataclasses import dataclass

from homeassistant.components.scene import Scene

from ..scenes import BaseScene, MyFoxSceneInfo
from ..entities.entities_scene import BaseSceneEntity

_LOGGER = logging.getLogger(__name__)

#"scenarioId": 318925,
#"label": "Volets Nuit ON",
#"typeLabel": "onDemand",
#"enabled": null
@dataclass
class MyFoxScenario :
    scenarioId: int
    label: str
    typeLabel: str
    enabled: bool | None


@dataclass
class MyFoxScenarioDevice(BaseScene) :
    """ """

    def __init__(self, scene_info:MyFoxSceneInfo):
        super().__init__(scene_info)

    def scenes(self, coordinator) -> list[Scene]:
        _LOGGER.debug("Ajout ScenarioScene sur scene %s", str(self.scene_info.scenarioId))
        return [BaseSceneEntity(coordinator, self, f"Temperature {self.scene_info.label}", "scene")]
    
