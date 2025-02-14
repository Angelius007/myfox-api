from typing import Type, OrderedDict

from ..scenes import (BaseScene, DiagnosticScene, scenario)


scene_by_typeLabel_key: OrderedDict[str, Type[BaseScene]] = OrderedDict[str, Type[BaseScene]]({
    "scheduled"             : scenario.MyFoxScheduledScenarioScene,
    "onEvent"               : scenario.MyFoxOnEventScenarioScene,
    "simulation"            : scenario.MyFoxSimulationScenarioScene,
    "onDemand"              : scenario.MyFoxOnDemandScenarioScene,
    "generic"               : DiagnosticScene
})
