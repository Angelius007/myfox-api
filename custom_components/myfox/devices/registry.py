from typing import Type, OrderedDict
from ..devices import (BaseDevice, DiagnosticDevice, 
                       camera, gate, group, heater,
                       librairie, light, module, scenario,
                       sensor, shutter, socket, temperature)

device_by_product: OrderedDict[str, Type[BaseDevice]] = OrderedDict[str, Type[BaseDevice]]({
    "5" : camera,
    #"" : gate,
    #"" : group,
    "44" : heater,
    #"" : librairie,
    #"29" : light,
    #"" : module,
    #"" : scenario,
    #"" : sensor,
    #"" : shutter,
    #"" : socket,
    "29" : temperature,
    "Diagnostic": DiagnosticDevice
})