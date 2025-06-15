import logging
import time

from .myfoxapi_exception import (MyFoxException)
from . import (MyFoxEntryDataApi )
from .myfoxapi import (MyFoxApiClient)

from .const import (
    MYFOX_GROUP_ELECTRIC_LIST,
    MYFOX_GROUP_ELECTRIC_SET_ON,
    MYFOX_GROUP_ELECTRIC_SET_OFF
)
_LOGGER = logging.getLogger(__name__)

class MyFoxApiGroupElectricClient(MyFoxApiClient) :

    def __init__(self, myfox_info:MyFoxEntryDataApi) -> None:
        super().__init__(myfox_info)
        self.client_key = "group_electric"
        self.module = list()
        self.module_time = 0

    async def getList(self) -> list:
        """ Get security site """
        try:
            if self.isCacheExpire(self.module_time) :
                response = await self.callMyFoxApiGet(MYFOX_GROUP_ELECTRIC_LIST % (self.myfox_info.site.siteId))
                _LOGGER.debug(str(response))
                items = response["payload"]["items"]
                self.module = items
                self.module_time = time.time()

            else :
                _LOGGER.debug("MyFoxApiGroupElectricClient.getList -> Cache ")

            return self.module

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
    
    async def setOn(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_ON % (self.myfox_info.site.siteId, groupId))
            _LOGGER.debug("Response : %s", str(response))
            
            statut_ok =  ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
    
    async def setOff(self, groupId:int) -> list:
        """ Get security site """
        try:
            response = await self.callMyFoxApiPost(MYFOX_GROUP_ELECTRIC_SET_OFF % (self.myfox_info.site.siteId, groupId))
            _LOGGER.debug("Response : %s", str(response))
            
            statut_ok =  ("status" in response and response["status"] == "OK")
            if statut_ok :
                self.module_time = 0
            return statut_ok

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
