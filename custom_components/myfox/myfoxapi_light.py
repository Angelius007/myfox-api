from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from .devices.light import MyFoxLightSensor

from .const import (
    MYFOX_LIGHT_LIST, MYFOX_LIGHT_HISTORY
)

class MyFoxApiLightClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.ligth = list()

    async def getLightList(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIGHT_LIST % (self.myfox_info.siteId))
            items = response["payload"]["items"]
            for item in items :
                self.ligth.append(MyFoxLightSensor(item["deviceId"],
                                item["label"],
                                item["modelId"],
                                item["modelLabel"],
                                item["light"]))
            return self.ligth

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def getLightHistory(self, light: MyFoxLightSensor):
        """ Mise a jour security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIGHT_HISTORY % (self.myfox_info.siteId , light.deviceId))
            # {'status': 'OK', 'timestamp': 1723759985, 'payload': {'request': 'OK'}}
            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)