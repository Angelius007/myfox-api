import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi)
from .myfoxapi import (MyFoxApiClient)
from .const import (
    MYFOX_CAMERA_LIST, MYFOX_CAMERA_LIVE_START, MYFOX_CAMERA_LIVE_STOP, MYFOX_CAMERA_LIVE_EXTEND,
    MYFOX_CAMERA_PREV_TAKE, MYFOX_CAMERA_REC_START, MYFOX_CAMERA_REC_STOP,
    MYFOX_CAMERA_SHUTTER_OPEN, MYFOX_CAMERA_SHUTTER_CLOSE, MYFOX_CAMERA_SNAP_TAKE
)
_LOGGER = logging.getLogger(__name__)


class MyFoxApiCameraClient(MyFoxApiClient) :

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "camera"
        self.camera = list()
        self.camera_time = 0
        self.lastPreview: bytes = None
        self.lastPreviewFilename: str = None
        self.lastPreview_time = 0

    def saveMyFoxInfo(self, myfox_info: MyFoxEntryDataApi) :
        super().saveMyFoxInfo(myfox_info)
        self.camera_cache_expire_in = myfox_info.options.cache_camera_time
        self.nb_retry = myfox_info.options.nb_retry_camera

    async def getList(self):
        """ Recuperation scenarios """
        try:
            if self.isCacheExpire(self.camera_time) :
                response = await self.callMyFoxApiGet(MYFOX_CAMERA_LIST % self.myfox_info.site.siteId)
                items = response["payload"]["items"]
                self.camera = items
                self.camera_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiCameraClient.getList -> Cache ")

            return self.camera

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraLiveStart(self, deviceId: int, protocol: str):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_START % (self.myfox_info.site.siteId, deviceId, protocol))
            data = response["payload"]
            _LOGGER.info("Live stream : %s", str(data))
            return data

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraLiveExtend(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_EXTEND % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraLiveStop(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_STOP % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraPreviewTake(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            if self.isCacheExpireWithParam(self.lastPreview_time, self.camera_cache_expire_in) :
                response = await self.callMyFoxApiBinaryPost(MYFOX_CAMERA_PREV_TAKE % (self.myfox_info.site.siteId, deviceId))
                if ("binary" in response and "filename" in response) :
                    self.lastPreview = response["binary"]
                    self.lastPreviewFilename = response["filename"]
                    if response["filename"] == "default.jpg" :
                        # Pas de cache si on a l'umage par defaut
                        self.lastPreview_time = 0
                    else :
                        self.lastPreview_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiCameraClient.cameraPreviewTake -> Cache %s", str(self.lastPreviewFilename))

            return self.lastPreview

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraSnapshotTake(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SNAP_TAKE % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraRecordingStart(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_START % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraRecordingStop(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_STOP % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraShutterOpen(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_OPEN % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def cameraShutterClose(self, deviceId: int):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_CLOSE % (self.myfox_info.site.siteId, deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
