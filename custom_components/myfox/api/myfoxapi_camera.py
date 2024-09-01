from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from ..devices.camera import MyFoxCamera, MyFoxCameraDevice
from .const import (
    MYFOX_CAMERA_LIST, MYFOX_CAMERA_LIVE_START, MYFOX_CAMERA_LIVE_STOP, MYFOX_CAMERA_LIVE_EXTEND,
    MYFOX_CAMERA_PREV_TAKE, MYFOX_CAMERA_REC_START, MYFOX_CAMERA_REC_STOP,
    MYFOX_CAMERA_SHUTTER_OPEN, MYFOX_CAMERA_SHUTTER_CLOSE, MYFOX_CAMERA_SNAP_TAKE
)

class MyFoxApiCameraClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.camera = list()
        self.type = MyFoxCameraDevice

    async def getCamera(self):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiGet(MYFOX_CAMERA_LIST % self.myfox_info.site.siteId)
            items = response["payload"]["items"]

            for item in items :
                self.camera.append(MyFoxCamera(item["deviceId"],
                                item["label"],
                                item["modelId"],
                                item["modelLabel"],
                                item["hideTimeLine"],
                                item["resolutionHeight"],
                                item["resolutionWidth"]))

            return self.camera

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraLiveStart(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_START % (self.myfox_info.site.siteId, camera.deviceId, camera.protocol))
            data = response["payload"]

            camera.guid = data["GUID"]
            camera.protocol = data["protocol"]
            camera.location = data["location"]

            return camera

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraLiveExtend(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_EXTEND % (self.myfox_info.site.siteId, camera.deviceId))
            # data = response["payload"]

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraLiveStop(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_LIVE_STOP % (self.myfox_info.site.siteId, camera.deviceId))
            # data = response["payload"]

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraPreviewTake(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiBinaryPost(MYFOX_CAMERA_PREV_TAKE % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraSnapshotTake(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SNAP_TAKE % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraRecordingStart(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_START % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraRecordingStop(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_REC_STOP % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def cameraShutterOpen(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_OPEN % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
        
    async def cameraShutterClose(self, camera: MyFoxCamera):
        """ Recuperation scenarios """
        try:
            response = await self.callMyFoxApiPost(MYFOX_CAMERA_SHUTTER_CLOSE % (self.myfox_info.site.siteId, camera.deviceId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)