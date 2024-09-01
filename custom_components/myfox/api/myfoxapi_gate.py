from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from myfox.devices.gate import MyFoxGate

from .const import (
    MYFOX_DEVICE_GATE_LIST,
    MYFOX_DEVICE_GATE_PERFORM_ONE,
    MYFOX_DEVICE_GATE_PERFORM_TWO
)

class MyFoxApiGateClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.temperature = list()
        self.temperatureRecord = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_GATE_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.temperature.append(MyFoxGate(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"]))

            return self.temperature

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeOne(self, device:MyFoxGate) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_GATE_PERFORM_ONE % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def performeTwo(self, device:MyFoxGate) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_GATE_PERFORM_TWO % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
