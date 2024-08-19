from dataclasses import dataclass

#LightSensor  {
    # deviceId (integer): The device identifier,
    # label (string): The device label,
    # light (integer, null): Current light level,
    # modelId (string): The device model identifier,
    # modelLabel (string): The device model label
#}
@dataclass
class MyFoxLightSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    light: int
