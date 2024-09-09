import logging

from dataclasses import dataclass

from homeassistant.components.scene import Scene
from homeassistant.components.switch import SwitchEntity

from . import BaseScene, MyFoxSceneInfo
from ..entities.entities_scene import ActivabledSceneEntity,OnDemandSceneEntity

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

    def switches(self, coordinator) -> list[SwitchEntity]:
        if self.scene_info.typeLabel == "scheduled" or self.scene_info.enabled == "onEvent" or self.scene_info.enabled == "simulation" :
            return [ActivabledSceneEntity(coordinator, self, f"Scenario {self.scene_info.label}", self.scene_info.typeLabel)]
    
    def scenes(self, coordinator) -> list[Scene]:
        _LOGGER.debug("Ajout ScenarioScene sur scene %s", str(self.scene_info.scenarioId))
        if self.scene_info.typeLabel == "onDemand" :
            return [OnDemandSceneEntity(coordinator, self, f"Scenario {self.scene_info.label}", self.scene_info.typeLabel)]    
