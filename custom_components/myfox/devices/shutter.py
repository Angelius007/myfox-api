from dataclasses import dataclass

#Shutter {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxShutter :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str