from typing import Type, OrderedDict

from . import state

from ..devices import (BaseDevice, DiagnosticDevice, 
                       camera, gate, heater, alarme,
                       media, light, module, shutter, socket, temperature)

device_by_product: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "Diagnostic"    : DiagnosticDevice
})

device_by_client_key: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "alerte_state_sensor"   : state.MyFoxAlerteStateDevice,
    "camera"                : camera.MyFoxCameraDevice,
    "gate"                  : gate.MyFoxGateDevice,
    "group_electric"        : socket.MyFoxSocketDevice,
    "group_shutter"         : shutter.MyFoxShuttereDevice,
    "heater"                : heater.MyFoxHeaterDevice,
    "librairie"             : media.MyFoxMediaDevice,
    "light"                 : light.MyFoxLightDevice,
    "module"                : module.MyFoxModuleDevice,
    "security"              : alarme.MyFoxAlarmeDevice,
    "shutter"               : shutter.MyFoxShuttereDevice,
    "socket"                : socket.MyFoxSocketDevice,
    "state"                 : state.MyFoxStateDevice,
    "temperature"           : temperature.MyFoxTemperatureDevice,
    "thermo"                : heater.MyFoxHeaterWithStateDevice,
    "generic"               : DiagnosticDevice
})

device_by_model_label: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "Alarme MyFox"                          : alarme.MyFoxAlarmeDevice,
    "Capteur luminosité"                    : light.MyFoxLightDevice,
    "Capteur température"                   : temperature.MyFoxTemperatureDevice,
    "Electrical devices"                    : socket.MyFoxSocketDevice,
    "Module chauffage"                      : heater.MyFoxHeaterDevice,
    "Module DIO pour volet"                 : shutter.MyFoxShuttereDevice,
    "Panasonic BL-C131"                     : camera.MyFoxCameraDevice,
    "Prise électrique commandée"            : socket.MyFoxSocketDevice,
    "Prise électrique commandée DIO First"  : socket.MyFoxSocketDevice,
    "Shutters"                              : shutter.MyFoxShuttereDevice,
    "Diagnostic"                            : DiagnosticDevice
})