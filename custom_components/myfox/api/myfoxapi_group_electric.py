from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from myfox.devices.group import (MyFoxGroupElectric)
from myfox.devices.socket import (MyFoxSocket)


from .const import (
    MYFOX_GROUP_ELECTRIC_LIST,
    MYFOX_GROUP_ELECTRIC_SET_ON,
    MYFOX_GROUP_ELECTRIC_SET_OFF
)

class MyFoxApiGroupElectricClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_GROUP_ELECTRIC_LIST % (self.myfox_info.site.siteId))
            print(str(response))
            items = response["payload"]["items"]
            for item in items :
                group = MyFoxGroupElectric(item["groupId"],
                                            item["label"],
                                            item["type"],
                                            [])
                for device in item["devices"] :
                    group.devices.append(MyFoxSocket(device["deviceId"],
                                                        device["label"],
                                                        device["modelId"],
                                                        device["modelLabel"]))
                self.module.append(group)

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOn(self, device:MyFoxGroupElectric) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_ON % (self.myfox_info.site.siteId, device.groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOff(self, device:MyFoxGroupElectric) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_OFF % (self.myfox_info.site.siteId, device.groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
