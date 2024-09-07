import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_HEATER_LIST,
    MYFOX_DEVICE_HEATER_SET_ECO,
    MYFOX_DEVICE_HEATER_SET_FROST,
    MYFOX_DEVICE_HEATER_SET_ON,
    MYFOX_DEVICE_HEATER_SET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApHeaterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "heater"
        self.heater = list()
        self.heater_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.heater_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_HEATER_LIST % (self.myfox_info.site.siteId))
                print(str(response))
                items = response["payload"]["items"]
                self.heater = items
                #for item in items :
                #    self.temperature.append(MyFoxHeater(item["deviceId"],
                #                                        item["label"],
                #                                        item["modelId"],
                #                                        item["modelLabel"],
                #                                        item["modeLabel"],
                #                                        item["stateLabel"])
                #                            )
            else :
                _LOGGER.debug("MyFoxApHeaterClient.getList -> Cache ")

            return self.heater

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setEco(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_ECO % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setFrost(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_FROST % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setOn(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_ON % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setOff(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_SET_OFF % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
