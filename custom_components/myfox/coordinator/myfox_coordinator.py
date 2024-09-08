import logging
import async_timeout
import asyncio

from datetime import timedelta
from typing import Any, List, TypeVar

import threading
import queue

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..api.myfoxapi import (
    MyFoxApiClient
)
from ..api.myfoxapi_exception import (MyFoxException)
from ..api.myfoxapi_shutter import (MyFoxApiShutterClient)
from ..api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from ..api.myfoxapi_socket import (MyFoxApiSocketClient)
from ..api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from ..api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from ..api.myfoxapi_light import (MyFoxApiLightClient)
from ..api.myfoxapi_sensor_alerte import (MyFoxApiAlerteSensorClient)
from ..api.myfoxapi_heater import (MyFoxApiHeaterClient)
from ..api.myfoxapi_scenario import MyFoxApiSecenarioClient

_LOGGER = logging.getLogger(__name__)


_T = TypeVar("_T")
class BoundFifoList(List):

    def __init__(self, maxlen=30) -> None:
        super().__init__()
        self.maxlen = maxlen

    def append(self, __object: _T) -> None:
        super().insert(0, __object)
        while len(self) >= self.maxlen:
            self.pop()

async def worker(coordinator, queued_action:queue.Queue):
    continue_processing = True
    
    while continue_processing:
        item = queued_action.get()
        print(f'Working on {item}')
        # arret du process
        if "stop" in item :
            continue_processing = False
        elif "pressButton" in item :
            await coordinator.pressButton(item["pressButton"])

        print(f'Finished {item}')
        queued_action.task_done()

def wrap_async_worker(coordinator, queued_action:queue.Queue):
    asyncio.run(worker(coordinator, queued_action))

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
        self.deferredPressButtonAction = BoundFifoList[dict[str, Any]]()
        self.queued_action = queue.Queue()

        # Turn-on the worker thread.
        threading.Thread(target=wrap_async_worker,  args=(self, self.queued_action), daemon=True).start()
        _LOGGER.debug("Init " + str(self.name))


    def stop(self) :
        """ Arret des process """
        msg = dict[str, Any]
        action="stop"
        msg[action] = action
        self.queued_action.put(msg)
        self.queued_action.join()

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
            try:
                await myfoxApiClient.getList()
            except MyFoxException as exception:
                _LOGGER.error(exception)

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            _LOGGER.debug("Load data from : %s", str(self.name))
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
                        try:
                            _LOGGER.debug("Client[%s].getList:%s",str(client_key),str(myfoxApiClient.__class__))
                            await myfoxApiClient.getList()
                        except MyFoxException as exception:
                            _LOGGER.error(exception)
                    # cas d'un client temperature
                    if myfoxApiClient.__class__ == MyFoxApiTemperatureClient :
                        
                        client:MyFoxApiTemperatureClient = myfoxApiClient
                        for temp in client.temperature :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client light
                    if myfoxApiClient.__class__ == MyFoxApiLightClient :
                        
                        client:MyFoxApiLightClient = myfoxApiClient
                        for temp in client.ligth :
                            self.addToParams(params, listening_idx, temp)
                    
                    # cas d'un client sensor alert
                    if myfoxApiClient.__class__ == MyFoxApiAlerteSensorClient :
                        
                        client:MyFoxApiAlerteSensorClient = myfoxApiClient
                        for temp in client.sensor :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client heater
                    if myfoxApiClient.__class__ == MyFoxApiHeaterClient :
                        
                        client:MyFoxApiHeaterClient = myfoxApiClient
                        for temp in client.heater :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client heater
                    if myfoxApiClient.__class__ == MyFoxApiSecenarioClient :
                        
                        client:MyFoxApiSecenarioClient = myfoxApiClient
                        for temp in client.scenarii :
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
        if "deviceId" in temp :
            device_id = temp["deviceId"]
            for key,val in temp.items() :
                control_key = str(device_id) + "|" + str(key)
                if control_key in listening_idx or len(listening_idx) == 0 :
                    params[control_key] = val
                    _LOGGER.debug("addToParams -> deviceId(%s) : %s [%s]", str(device_id), control_key, str(val))
        elif "scenarioId" in temp :
            scene_id = temp["scenarioId"]
            for key,val in temp.items() :
                control_key = str(scene_id) + "|" + str(key)
                if control_key in listening_idx or len(listening_idx) == 0 :
                    params[control_key] = val
                    _LOGGER.debug("addToParams -> scenarioId(%s) : %s [%s]", str(scene_id), control_key, str(val))

    def deferredPressButton(self, idx:str) :
        """ deferred press """
        try:
            _LOGGER.debug("Deferred Press button : %s from %s", idx, str(self.name))
            msg = dict[str, Any]
            action="pressButton"
            msg[action] = idx
            self.queued_action.put(msg)
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")
        
    async def pressButton(self, idx:str) -> bool :
        """ Appuis sur un bouton et transmission au bon client """
        action_ok = False
        try:
            _LOGGER.debug("Press button : %s from %s", idx, str(self.name))
            valeurs = idx.split("|", 2)
            device_id = valeurs[0]
            device_action = valeurs[1]
            # recherche du client et du device
            for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                if myfoxApiClient.__class__ == MyFoxApiShutterClient :
                    client:MyFoxApiShutterClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "open" :
                            """ open """
                            action_ok = await client.setOpen(int(device_id))
                            break
                        elif device_action == "close" :
                            """ close """
                            action_ok = await client.setClose(int(device_id))
                            break
                        elif device_action == "my" :
                            """ favorite """
                            action_ok = await client.setFavorite(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
                    _LOGGER.debug("pressButton %s pour le volet %s : %s", str(device_action), str(device_id), str(action_ok) )
                elif myfoxApiClient.__class__ == MyFoxApiGroupShutterClient :
                    client:MyFoxApiGroupShutterClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "open" :
                            """ open """
                            action_ok = await client.setOpen(int(device_id))
                            break
                        elif device_action == "close" :
                            """ close """
                            action_ok = await client.setClose(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
                    _LOGGER.debug("pressButton %s pour le volet %s : %s", str(device_action), str(device_id), str(action_ok) )
                elif myfoxApiClient.__class__ == MyFoxApiSocketClient :
                    client:MyFoxApiSocketClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "on" :
                            """ on """
                            action_ok = await client.setOn(int(device_id))
                            break
                        elif device_action == "off" :
                            """ off """
                            action_ok = await client.setOff(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
                    _LOGGER.debug("pressButton %s pour le volet %s : %s", str(device_action), str(device_id), str(action_ok) )
                elif myfoxApiClient.__class__ == MyFoxApiGroupElectricClient :
                    client:MyFoxApiGroupElectricClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "on" :
                            """ on """
                            action_ok = await client.setOn(int(device_id))
                            break
                        elif device_action == "off" :
                            """ off """
                            action_ok = await client.setOff(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
            _LOGGER.debug("pressButton %s pour le volet %s : %s", str(device_action), str(device_id), str(action_ok) )

            return action_ok
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return action_ok
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")

    async def selectOption(self, idx:str, option:str) -> bool :
        """ Selection option et transmission au bon client """
        action_ok = False
        try:
            _LOGGER.debug("Select Option : %s/%s from %s", idx, option, str(self.name))
            valeurs = idx.split("|", 2)
            device_id = valeurs[0]
            device_option = valeurs[1]
            device_action = option
            # recherche du client et du device
            for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                if myfoxApiClient.__class__ == MyFoxApiHeaterClient :
                    client:MyFoxApiHeaterClient = myfoxApiClient
                    # verification device
                    _LOGGER.debug("selectOption '%s' for '%s'", str(device_action), str(device_option) )
                    if device_id in client.devices :
                        """ """
                        if device_action == "on" :
                            """ on """
                            action_ok = await client.setOn(int(device_id))
                            break
                        elif device_action == "off" :
                            """ off """
                            action_ok = await client.setOff(int(device_id))
                            break
                        elif device_action == "eco" :
                            """ eco """
                            action_ok = await client.setEco(int(device_id))
                            break
                        elif device_action == "frost" :
                            """ frost """
                            action_ok = await client.setFrost(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("selectOption '%s' non reconnue pour le device %s", str(device_action), str(device_id))
            _LOGGER.debug("selectOption %s pour le radiateur %s : %s", str(device_action), str(idx), str(action_ok) )

            if action_ok :
                params = dict[str, Any]()
                listening_idx = set()
                listening_idx.add(idx)
                valeurs = list()
                valeur = dict[str, Any]()
                valeur["deviceId"] = device_id
                valeur[device_option] = device_action
                valeurs.append(valeur)
                self.addToParams(params, listening_idx,valeur)
                self.async_set_updated_data(params)
                
            return action_ok
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return action_ok
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")
