from dataclasses import dataclass

#TemperatureSensor {
#deviceId (integer): The device identifier,
#label (string): The device label,
#lastTemperature (float, null): Last temperature,
#lastTemperatureAt (string): Last temperature date,
#modelId (string): The device model identifier,
#modelLabel (string): The device model label
#}

@dataclass
class MyFoxTemperatureSensor :
    deviceId: int
    label: str
    modelId: int
    modelLabel: str
    lastTemperature: float = 0.0
    lastTemperatureAt: str = None

#TemperatureRecord {
#deviceId (integer): The temperature sensor device identifier,
#celsius (float): The temperature value is celsius degrees,
#recordedAt (string): The temperature value creation date
#}

@dataclass
class MyFoxTemperatureRecord :
    deviceId: int
    celsius: float
    recordedAt: str