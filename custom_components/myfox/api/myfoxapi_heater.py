from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.heater import MyFoxHeater

from .const import (
    MYFOX_DEVICE_HEATER_LIST,
    MYFOX_DEVICE_HEATER_SET_ECO,
    MYFOX_DEVICE_HEATER_SET_FROST,
    MYFOX_DEVICE_HEATER_SET_ON,
    MYFOX_DEVICE_HEATER_SET_OFF
)

class MyFoxApHeaterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.temperature = list()
        self.temperatureRecord = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_HEATER_LIST % (self.myfox_info.site.siteId))
            print(str(response))
            items = response["payload"]["items"]

            for item in items :
                self.temperature.append(MyFoxHeater(item["deviceId"],
                                                    item["label"],
                                                    item["modelId"],
                                                    item["modelLabel"],
                                                    item["modeLabel"],
                                                    item["stateLabel"])
                                        )

            return self.temperature

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setEco(self, device:MyFoxHeater) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_ECO % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setFrost(self, device:MyFoxHeater) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_FROST % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setOn(self, device:MyFoxHeater) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_ON % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setOff(self, device:MyFoxHeater) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_OFF % (self.myfox_info.site.siteId, device.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
