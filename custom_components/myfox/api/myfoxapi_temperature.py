import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_TEMPERATURE_LIST,
    MYFOX_DEVICE_TEMPERATURE_GET
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiTemperatureClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.temperature = list()
        self.temperatureRecord = list()

    async def getList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_LIST % (self.myfox_info.site.siteId))
            _LOGGER.debug("getList.response : %s",str(response))
            items = response["payload"]["items"]
            _LOGGER.debug("getList : %s",str(items))

            # for item in items :
            self.temperature = items
            #     self.temperature.append(MyFoxTemperatureDevice(MyFoxTemperatureSensor(item["deviceId"],
            #                                            item["label"],
            #                                            item["modelId"],
            #                                            item["modelLabel"],
            #                                            item["lastTemperature"],
            #                                            item["lastTemperatureAt"])))

            return self.temperature

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def updateDevice(self, deviceId:int) :
        """ """
        #self.getTemperature(device.sensor)

    async def getTemperature(self, deviceId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_GET % (self.myfox_info.site.siteId, deviceId))
            items = response["payload"]["items"]
            _LOGGER.debug("getTemperature : %s",str(items))
            self.temperatureRecord = items
            #for item in items :
            #    self.temperatureRecord.append(MyFoxTemperatureRecord(item["recordId"],
            #                                                        item["celsius"],
            #                                                        item["recordedAt"]))

            return self.temperatureRecord

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
