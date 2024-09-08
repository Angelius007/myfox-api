from typing import Type, OrderedDict

from ..scenes import (BaseScene, DiagnosticScene, scenario)


scene_by_client_key: OrderedDict[str, Type[BaseScene]] = OrderedDict[str, Type[BaseScene]]({
    "scenario"              : scenario.MyFoxScenarioDevice,
    "generic"               : DiagnosticScene
})

