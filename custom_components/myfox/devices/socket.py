from dataclasses import dataclass

#Socket {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxSocket :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str