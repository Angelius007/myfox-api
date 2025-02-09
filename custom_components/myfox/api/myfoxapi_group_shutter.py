import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi )
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_GROUP_SHUTTER_LIST,
    MYFOX_GROUP_SHUTTER_SET_CLOSE,
    MYFOX_GROUP_SHUTTER_SET_OPEN
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiGroupShutterClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "group_shutter"
        self.module = list()
        self.module_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.module_time) :
                response = await self.callMyFoxApiGet(MYFOX_GROUP_SHUTTER_LIST % (self.myfox_info.site.siteId))
                _LOGGER.debug(str(response))
                items = response["payload"]["items"]
                self.module = items
                self.module_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiGroupShutterClient.getList -> Cache ")

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setOpen(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_OPEN % (self.myfox_info.site.siteId, groupId))
            _LOGGER.debug("Response : %s", str(response))
            
            statut_ok =  ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(exception)
    
    async def setClose(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_SHUTTER_SET_CLOSE % (self.myfox_info.site.siteId, groupId))
            _LOGGER.debug("Response : %s", str(response))
            
            statut_ok =  ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(exception)
