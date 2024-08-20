from .myfoxapi import (MyFoxApiClient, MyFoxException, MyFoxEntryDataApi )
from .devices.librairie import MyFoxImage, MyFoxVideo

from .const import (
    MYFOX_LIBRARY_IMAGE_LIST,
    MYFOX_LIBRARY_VIDEO_LIST,
    MYFOX_LIBRARY_VIDEO_PLAY
)

class MyFoxApiLibraryClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.module = list()

    async def getImageList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIBRARY_IMAGE_LIST % (self.myfox_info.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.module.append(MyFoxImage(item["imageId"],
                                            item["cameraId"],
                                            item["cameraLabel"],
                                            item["height"],
                                            item["width"],
                                            item["createdAt"],
                                            item["fileURL"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def getVideoList(self) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIBRARY_VIDEO_LIST % (self.myfox_info.siteId))
            items = response["payload"]["items"]

            for item in items :
                self.module.append(MyFoxVideo(item["videoId"],
                                            item["cameraId"],
                                            item["modelId"],
                                            item["cameraLabel"],
                                            item["duration"],
                                            item["height"],
                                            item["width"],
                                            item["isRecording"],
                                            item["createdAt"],
                                            item["fileURL"],
                                            item["playURL"],
                                            item["previewURL"]))

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def playVideo(self, device:MyFoxVideo) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiBinaryPost(MYFOX_LIBRARY_VIDEO_PLAY % (self.myfox_info.siteId, device.videoId))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
