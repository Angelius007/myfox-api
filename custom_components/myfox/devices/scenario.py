from dataclasses import dataclass

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