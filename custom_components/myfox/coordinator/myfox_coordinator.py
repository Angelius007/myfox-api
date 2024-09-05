import logging
import async_timeout
from datetime import timedelta
from typing import  Any

from homeassistant.core import HomeAssistant
from homeassistant.components.light import LightEntity
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..devices import (BaseDevice)
from ..api.myfoxapi import (
    MyFoxEntryDataApi,
    MyFoxApiClient
)
from ..api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
#from ..devices.temperature import  MyFoxTemperatureDevice

_LOGGER = logging.getLogger(__name__)

class MyFoxCoordinator(DataUpdateCoordinator) :
    """ Corrd inator pour synchro avec les appels API MyFox """
    
    def __init__(self, hass: HomeAssistant, myfoxApiClient:MyFoxApiClient):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="My coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=5),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.myfoxApiClient = myfoxApiClient
        #self._device: BaseDevice | None = None
        _LOGGER.debug("Init " + str(self.name) + " - Client : " + str(self.myfoxApiClient.__class__))

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        _LOGGER.debug("Client.getList:"+str(self.myfoxApiClient.__class__))
        await self.myfoxApiClient.getList()

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                # Grab active context variables to limit data required to be fetched from API
                # Note: using context is not required if there is no need or ability to limit
                # data retrieved from API.
                await self.myfoxApiClient.getList()
                
                listening_idx = set(self.async_contexts())
                _LOGGER.debug("listening_idx : %s", str(listening_idx))
                params = dict[str, Any]()
                if len(listening_idx) > 0:
                    if self.myfoxApiClient.__class__ == MyFoxApiTemperatureClient :
                        
                        client_temperature:MyFoxApiTemperatureClient = self.myfoxApiClient
                        for temp in client_temperature.temperature :
                            
                            self.addToParams(params, listening_idx, temp)

                            #params[str(temp["deviceId"] )+"|lastTemperature"] = temp["lastTemperature"] 
                            #params[str(temp["deviceId"] )+"|lastTemperatureAt"] = temp["lastTemperatureAt"] 
                            #params[str(temp["deviceId"] )+"|deviceId"] = int(temp["deviceId"])
                            #_LOGGER.debug("_async_update_data -> deviceId : %s", str(temp["deviceId"]))

                    #for (deviceid,device) in  self.myfoxApiClient.devices.items() :
                    #    if str(params[str(deviceid)+"|deviceId"]) == str(deviceid) :
                    #        _LOGGER.debug("device.update : %s", str(deviceid))
                    #        device.data.update_data(params)

                _LOGGER.debug("params : %s", str(params))

                return params
        # except ApiAuthError as err:   
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        #     raise ConfigEntryAuthFailed from err
        # except ApiError as err:
        #     raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")
        
    def addToParams(self, params:dict[str, Any], listening_idx:set,temp:Any):
        """ Ajout des parames de la liste si correspond aux attentes """
        device_id = temp["deviceId"]
        for key,val in temp :
            control_key = str(device_id) + "|" + str(key)
            if control_key in listening_idx:
                params[control_key] = val
                _LOGGER.debug("addToParams -> deviceId(%s) : %s [%s]", str(device_id), control_key, str(val))

        