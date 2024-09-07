import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_HEATER_THERMO_LIST,
    MYFOX_DEVICE_HEATER_THERMO_SET_AUTO,
    MYFOX_DEVICE_HEATER_THERMO_SET_AWAY,
    MYFOX_DEVICE_HEATER_THERMO_SET_BOOST,
    MYFOX_DEVICE_HEATER_THERMO_SET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApThermoClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "thermo"
        self.temperature = list()
        self.temperatureRecord = list()

    def stop(self) -> bool:
        super().stop()
        self.temperature.clear()
        self.temperatureRecord.clear()
        return True

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_HEATER_THERMO_LIST % (self.myfox_info.site.siteId))
            print(str(response))
            items = response["payload"]["items"]
            _LOGGER.debug("getList : %s",str(items))
            self.temperature = items
            #for item in items :
            #    if "lastTemperature" in item :
            #        self.temperature.append(MyFoxHeater(item["deviceId"],
            #                                            item["label"],
            #                                            item["modelId"],
            #                                            item["modelLabel"],
            #                                            item["modeLabel"],
            #                                            item["stateLabel"],
            #                                            item["lastTemperature"])
            #                            )

            return self.temperature

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setAuto(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_AUTO % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setAuto : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setAway(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_AWAY % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setAway : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setBoost(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_BOOST % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setBoost : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def setOff(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_DEVICE_HEATER_THERMO_SET_OFF % (self.myfox_info.site.siteId, deviceId))
            _LOGGER.debug("setOff : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
