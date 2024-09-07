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
from ..api.myfoxapi_light import (MyFoxApiLightClient)
#from ..devices.temperature import  MyFoxTemperatureDevice

_LOGGER = logging.getLogger(__name__)

class MyFoxCoordinator(DataUpdateCoordinator) :
    """ Corrd inator pour synchro avec les appels API MyFox """
    
    def __init__(self, hass: HomeAssistant):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="MyFox coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=2),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.myfoxApiClient =  dict[str, MyFoxApiClient]()

        _LOGGER.debug("Init " + str(self.name))

    def add_client(self, myfoxApiClient:MyFoxApiClient):
        """ Ajout d'un nouveau client """
        # Si le client existe deja, on ajoute les devices au client existant
        if myfoxApiClient.client_key in self.myfoxApiClient :
            for deviceId,device in myfoxApiClient.devices.items() :
                self.myfoxApiClient[myfoxApiClient.client_key].devices[deviceId] = device
        # Sinon, on ajoute le client directement
        else :
            self.myfoxApiClient[myfoxApiClient.client_key] = myfoxApiClient

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
            _LOGGER.debug("Client[%s].getList:%s",str(client_key),str(myfoxApiClient.__class__))
            await myfoxApiClient.getList()

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
                params = dict[str, Any]()
                listening_idx = set(self.async_contexts())
                _LOGGER.debug("listening_idx : %s", str(listening_idx))

                # Si vide, alors init donc deja charge via _async_setup
                for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                    if len(listening_idx) > 0:
                        _LOGGER.debug("Client[%s].getList:%s",str(client_key),str(myfoxApiClient.__class__))
                        await myfoxApiClient.getList()
                    # cas d'un client temperature
                    if myfoxApiClient.__class__ == MyFoxApiTemperatureClient :
                        
                        client_temperature:MyFoxApiTemperatureClient = myfoxApiClient
                        for temp in client_temperature.temperature :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client light
                    if myfoxApiClient.__class__ == MyFoxApiLightClient :
                        
                        client_light:MyFoxApiLightClient = myfoxApiClient
                        for temp in client_light.ligth :
                            self.addToParams(params, listening_idx, temp)

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
        for key,val in temp.items() :
            control_key = str(device_id) + "|" + str(key)
            if control_key in listening_idx or len(listening_idx) == 0 :
                params[control_key] = val
                _LOGGER.debug("addToParams -> deviceId(%s) : %s [%s]", str(device_id), control_key, str(val))

        