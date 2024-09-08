import logging

from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.components.scene import Scene
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from ..scenes import BaseScene
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

from ..const import (DOMAIN_MYFOX)

_LOGGER = logging.getLogger(__name__)
 
## ////////////////////////////////////////////////////////////////////////////
## SCENES
## ////////////////////////////////////////////////////////////////////////////

class MyFoxAbstractSceneEntity(CoordinatorEntity, Entity):

    def __init__(self, coordinator:MyFoxCoordinator, scene: BaseScene, title: str, key: str):
        super().__init__(coordinator, context=str(scene.scene_info.scenarioId)+"|"+key)
        self.idx = str(scene.scene_info.scenarioId)+"|"+key 
        self._scene: BaseScene = scene
        self._attr_name = title
        self._attr_unique_id = "MyFox-"+self.idx

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers={(DOMAIN_MYFOX, f"{self._scene.scene_info.scenarioId}-{self._scene.scene_info.typeLabel}")},
            manufacturer="MyFox",
            name=self._scene.scene_info.label,
            model=self._scene.scene_info.typeLabel,
            serial_number=str(self._scene.scene_info.scenarioId),
        )
    
class BaseSceneEntity(Scene, MyFoxAbstractSceneEntity):
    pass