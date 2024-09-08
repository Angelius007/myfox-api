from typing import Type, OrderedDict
from ..devices import (BaseDevice, DiagnosticDevice, 
                       camera, gate, group, heater,
                       librairie, light, module, scenario,
                       sensor, shutter, socket, temperature)

device_by_product: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "5" : camera.MyFoxCameraDevice,
    "44" : heater.MyFoxHeaterDevice,
    "Diagnostic": DiagnosticDevice
})

device_by_client_key: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "camera" : camera.MyFoxCameraDevice,
    "thermo" : heater.MyFoxHeaterDevice,
    "shutter" : shutter.MyFoxShuttereDevice,
    "group_shutter" : shutter.MyFoxShuttereDevice,
    "temperature" : temperature.MyFoxTemperatureDevice,
    "light" : light.MyFoxLightDevice,
    "socket" : socket.MyFoxSocketDevice,
    "group_electric" : socket.MyFoxSocketDevice,
    "generic": DiagnosticDevice
})

device_by_model_label: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "Panasonic BL-C131"                 : camera.MyFoxCameraDevice,
    "Module chauffage"                  : heater.MyFoxHeaterDevice,
    "Capteur température & luminosité"  : sensor.MyFoxSensorDevice,
    "Capteur température"               : temperature.MyFoxTemperatureDevice,
    "Capteur luminosité"                : light.MyFoxLightDevice,
    "Module DIO pour volet"             : shutter.MyFoxShuttereDevice,
    "Shutters"                          : shutter.MyFoxShuttereDevice,
    "Prise électrique commandée"        : socket.MyFoxSocketDevice,
    "Electrical devices"                : socket.MyFoxSocketDevice,
    "Diagnostic"                        : DiagnosticDevice
})