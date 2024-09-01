from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.group import (MyFoxGroupShutter)
from ..devices.shutter import (MyFoxShutter)

from .const import (
    MYFOX_GROUP_SHUTTER_LIST,
    MYFOX_GROUP_SHUTTER_SET_CLOSE,
    MYFOX_GROUP_SHUTTER_SET_OPEN
)

class MyFoxApiGroupShutterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_GROUP_SHUTTER_LIST % (self.myfox_info.site.siteId))
            print(str(response))
            items = response["payload"]["items"]
            for item in items :
                group = MyFoxGroupShutter(item["groupId"],
                                            item["label"],
                                            item["type"],
                                            [])
                for device in item["devices"] :
                    group.devices.append(MyFoxShutter(device["deviceId"],
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
    
    async def setOpen(self, device:MyFoxGroupShutter) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_OPEN % (self.myfox_info.site.siteId, device.groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setClose(self, device:MyFoxGroupShutter) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_CLOSE % (self.myfox_info.site.siteId, device.groupId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
