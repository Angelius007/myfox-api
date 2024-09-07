import logging
import time
from typing import Type

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices import (BaseDevice)
from ..devices.temperature import (MyFoxTemperatureDevice)


from .const import (
    MYFOX_DEVICE_TEMPERATURE_LIST,
    MYFOX_DEVICE_TEMPERATURE_GET,
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiTemperatureClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.type :  Type[BaseDevice] | None = MyFoxTemperatureDevice
        self.temperature = list()
        self.temperatureRecord = list()
        self.temperature_time = 0
        self.temperatureRecord_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.temperature_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_LIST % (self.myfox_info.site.siteId))
                _LOGGER.debug("getList.response : %s",str(response))
                items = response["payload"]["items"]

                # for item in items :
                self.temperature = items
                self.temperature_time = time.time()
                #     self.temperature.append(MyFoxTemperatureDevice(MyFoxTemperatureSensor(item["deviceId"],
                #                                            item["label"],
                #                                            item["modelId"],
                #                                            item["modelLabel"],
                #                                            item["lastTemperature"],
                #                                            item["lastTemperatureAt"])))
            else :
                _LOGGER.debug("MyFoxApiTemperatureClient.getList -> Cache ")
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
            if self.isCacheExpire(self.temperatureRecord_time) :
                response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_GET % (self.myfox_info.site.siteId, deviceId))
                items = response["payload"]["items"]
                _LOGGER.debug("getTemperature : %s",str(items))
                self.temperatureRecord = items
                self.temperatureRecord_time = time.time()
                #for item in items :
                #    self.temperatureRecord.append(MyFoxTemperatureRecord(item["recordId"],
                #                                                        item["celsius"],
                #                                                        item["recordedAt"]))
            else :
                _LOGGER.debug("MyFoxApiTemperatureClient.getTemperature -> Cache ")

            return self.temperatureRecord

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
