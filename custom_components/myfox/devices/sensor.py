from dataclasses import dataclass

# GenericSensor {
# deviceId (integer): The device identifier,
# label (string): The device label,
# state (integer, null): Current device state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }

@dataclass
class MyFoxGenerictSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    state: int

# DeviceWithState {
# deviceId (integer): The device identifier,
# label (string): The device label,
# stateLabel (string, null) = ['opened' or 'closed']: Current state,
# modelId (string): The device model identifier,
# modelLabel (string): The device model label
# }
@dataclass
class MyFoxDeviceWithState :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    stateLabel : str

@dataclass
class MyFoxDeviceWithStateState :
    deviceId: int
    stateLabel : str