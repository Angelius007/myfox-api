from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.temperature import MyFoxTemperatureSensor, MyFoxTemperatureRecord

from .const import (
    MYFOX_DEVICE_TEMPERATURE_LIST,
    MYFOX_DEVICE_TEMPERATURE_GET
)

class MyFoxApiTemperatureClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.temperature = list()
        self.temperatureRecord = list()
        self.type = MyFoxTemperatureSensor

    async def getList(self) -> list[MyFoxTemperatureSensor]:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.temperature.append(MyFoxTemperatureSensor(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"],
                                                       item["lastTemperature"],
                                                       item["lastTemperatureAt"]))

            return self.temperature

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def getTemperature(self, device:MyFoxTemperatureSensor) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_TEMPERATURE_GET % (self.myfox_info.site.siteId, device.deviceId))
            items = response["payload"]["items"]

            for item in items :
                self.temperatureRecord.append(MyFoxTemperatureRecord(item["recordId"],
                                                                    item["celsius"],
                                                                    item["recordedAt"]))

            return self.temperatureRecord

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
