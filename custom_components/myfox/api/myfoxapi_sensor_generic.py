import logging

from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )

from .const import (
    MYFOX_DEVICE_OTHER_LIST
)

_LOGGER = logging.getLogger(__name__)

class MyFoxApiGenericSensorClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "generic_sensor"
        self.sensor = list()

    def stop(self) -> bool:
        super().stop()
        self.sensor.clear()
        return True

    async def getList(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_OTHER_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]
            _LOGGER.debug("getSensorList : %s",str(items))
            self.sensor = items

            #for item in items :
            #    self.sensor.append(MyFoxGenerictSensor(item["deviceId"],
            #                                           item["label"],
            #                                           item["modelId"],
            #                                           item["modelLabel"],
            #                                           item["state"]))

            return self.sensor

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    