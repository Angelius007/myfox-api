from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from myfox.devices.sensor import MyFoxGenerictSensor, MyFoxDeviceWithState, MyFoxDeviceWithStateState

from .const import (
    MYFOX_DEVICE_OTHER_LIST,
    MYFOX_DEVICE_STATE_LIST,
    MYFOX_DEVICE_STATE_GET
)

class MyFoxApiSensorClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.sensor = list()
        self.sensorState = list()

    async def getSensorList(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_OTHER_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.sensor.append(MyFoxGenerictSensor(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"],
                                                       item["state"]))

            return self.sensor

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def getDeviceWithStateList(self):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_STATE_LIST % (self.myfox_info.site.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.sensor.append(MyFoxDeviceWithState(item["deviceId"],
                                                       item["label"],
                                                       item["modelId"],
                                                       item["modelLabel"],
                                                       item["stateLabel"]))

            return self.sensor

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def getDeviceWithState(self, device:MyFoxDeviceWithState):
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_DEVICE_STATE_GET % (self.myfox_info.site.siteId, device.deviceId))
            items = response["payload"]["items"]

            for item in items :
                self.sensorState.append(MyFoxDeviceWithStateState(item["deviceId"],
                                                       item["stateLabel"]))

            return self.sensorState

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
