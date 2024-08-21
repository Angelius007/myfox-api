from dataclasses import dataclass

from myfox.myfoxapi_socket import MyFoxSocket
from myfox.myfoxapi_shutter import MyFoxShutter

#GroupElectric {
#groupId (integer): The group identifier,
#label (string): The group label,
#type (string): The group type,
#devices (array[Device]): The group devices list
#}
@dataclass
class MyFoxGroupElectric :
    groupId: int
    label: str
    type: str
    devices: list[MyFoxSocket]

#GroupElectric {
#groupId (integer): The group identifier,
#label (string): The group label,
#type (string): The group type,
#devices (array[Device]): The group devices list
#}
@dataclass
class MyFoxGroupShutter :
    groupId: int
    label: str
    type: str
    devices: list[MyFoxShutter]