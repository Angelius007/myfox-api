from dataclasses import dataclass
from ..devices import  BaseDevice

#Heater {
#deviceId (integer): The device identifier,
#label (string): The device label,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label,
#modeLabel (string) = ['boiler' or 'wired']: The heater heating mode,
#stateLabel (string) = ['on' or 'off' or 'eco' or 'frost' or 'boost' or 'away' or 'auto']: The heater state,
#lastTemperature (float, null, optional): Last temperature
#}

@dataclass
class MyFoxHeater :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    modeLabel: str
    stateLabel: str
    lastTemperature: float | None = None

@dataclass
class MyFoxHeaterDevice(BaseDevice) :
    """ """
    heater:MyFoxHeater = None