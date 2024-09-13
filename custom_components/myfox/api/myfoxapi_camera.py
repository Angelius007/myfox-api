import logging
import time

from .myfoxapi_exception import (MyFoxException)
from .myfoxapi import (MyFoxApiClient,  MyFoxEntryDataApi )
from .const import (
    MYFOX_CAMERA_LIST, MYFOX_CAMERA_LIVE_START, MYFOX_CAMERA_LIVE_STOP, MYFOX_CAMERA_LIVE_EXTEND,
    MYFOX_CAMERA_PREV_TAKE, MYFOX_CAMERA_REC_START, MYFOX_CAMERA_REC_STOP,
    MYFOX_CAMERA_SHUTTER_OPEN, MYFOX_CAMERA_SHUTTER_CLOSE, MYFOX_CAMERA_SNAP_TAKE
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiCameraClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "camera"
        self.camera = list()
        self.camera_time = 0
        self.lastPreview:bytes = None
        self.lastPreview_time = 0
        self.cache_expire_in = myfox_info.options.cache_camera_time

    async def getList(self):
        """ Recuperation scenarios """
        try:
            if self.isCacheExpire(self.camera_time) :
                response = await self.callMyFoxApiGet(MYFOX_CAMERA_LIST % self.myfox_info.site.siteId)
                items = response["payload"]["items"]
                self.camera = items
                self.camera_time = time.time()
                #for item in items :
                #    self.camera.append(MyFoxCamera(item["deviceId"],
                #                    item["label"],
                #                    item["modelId"],
                #                    item["modelLabel"],
                #                    item["hideTimeLine"],
                #                    item["resolutionHeight"],
                #                    item["resolutionWidth"]))
            else :
                _LOGGER.debug("MyFoxApiCameraClient.getList -> Cache ")

            return self.camera

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraLiveStart(self, deviceId:int, protocol:str):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_START % (self.myfox_info.site.siteId, deviceId, protocol))
            data = response["payload"]

            #camera.guid = data["GUID"]
            #camera.protocol = data["protocol"]
            #camera.location = data["location"]

            return data

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraLiveExtend(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_EXTEND % (self.myfox_info.site.siteId, deviceId))
            # data = response["payload"]

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraLiveStop(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_STOP % (self.myfox_info.site.siteId, deviceId))
            # data = response["payload"]

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraPreviewTake(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            if self.isCacheExpire(self.lastPreview_time) :
                self.lastPreview = await self.callMyFoxApiBinaryPost(MYFOX_CAMERA_PREV_TAKE % (self.myfox_info.site.siteId, deviceId))
                self.lastPreview_time = time.time()
            else :
                _LOGGER.debug("MyFoxApiCameraClient.cameraPreviewTake -> Cache ")

            return self.lastPreview

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraSnapshotTake(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SNAP_TAKE % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraRecordingStart(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_START % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraRecordingStop(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_STOP % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraShutterOpen(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_OPEN % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraShutterClose(self, deviceId:int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_CLOSE % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)