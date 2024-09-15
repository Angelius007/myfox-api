import logging
import time

from .myfoxapi_exception import (MyFoxException)
from .myfoxapi import (MyFoxApiClient, MyFoxEntryDataApi )

from .const import (
    MYFOX_LIBRARY_IMAGE_LIST,
    MYFOX_LIBRARY_VIDEO_LIST,
    MYFOX_LIBRARY_VIDEO_PLAY
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiLibraryClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "librarie"
        self.video = list()
        self.video_time = 0
        self.image = list()
        self.image_time = 0

    async def getList(self) -> list:
        """ Liste """
        pass

    async def getImageList(self) -> list:
        """ Get image list """
        try:
            if self.isCacheExpire(self.image_time) :
                response = await self.callMyFoxApiGet(MYFOX_LIBRARY_IMAGE_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                _LOGGER.debug("getImageList : %s",str(items))
                self.image = items

                #for item in items :
                #    self.module.append(MyFoxImage(item["imageId"],
                #                                item["cameraId"],
                #                                item["cameraLabel"],
                #                                item["height"],
                #                                item["width"],
                #                                item["createdAt"],
                #                                item["fileURL"]))
            else :
                _LOGGER.debug("MyFoxApiLibraryClient.getImageList -> Cache ")

            return self.image

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def getVideoList(self) -> list:
        """ Get vdieo list """
        try:
            if self.isCacheExpire(self.video_time) :
                response = await self.callMyFoxApiGet(MYFOX_LIBRARY_VIDEO_LIST % (self.myfox_info.site.siteId))
                items = response["payload"]["items"]
                _LOGGER.debug("getVideoList : %s",str(items))
                self.video = items
                #for item in items :
                #    self.module.append(MyFoxVideo(item["videoId"],
                #                                item["cameraId"],
                #                                item["modelId"],
                #                                item["cameraLabel"],
                #                                item["duration"],
                #                                item["height"],
                #                                item["width"],
                #                                item["isRecording"],
                #                                item["createdAt"],
                #                                item["fileURL"],
                #                                item["playURL"],
                #                                item["previewURL"]))

            else :
                _LOGGER.debug("MyFoxApiLibraryClient.getVideoList -> Cache ")

            return self.video

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def playVideo(self, videoId:int) -> str:
        """ Get video """
        try:
            response = await self.callMyFoxApiGet(MYFOX_LIBRARY_VIDEO_PLAY % (self.myfox_info.site.siteId, videoId))
            _LOGGER.debug("playVideo : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)

    async def getImage(self, image_url:int) -> bytes:
        """ Get image """
        try:
            response = await self.callMyFoxApiBinaryGet(image_url)
            _LOGGER.debug("playVideo : %s",str(response))

            return response

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            print("Error : " + str(exception))
            raise MyFoxException(exception)
