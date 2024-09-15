import logging
import async_timeout

from datetime import timedelta
from typing import Any, List, TypeVar

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..api.myfoxapi import (
    MyFoxApiClient
)
from ..api.myfoxapi_exception import MyFoxException
from ..api.myfoxapi_shutter import MyFoxApiShutterClient
from ..api.myfoxapi_group_shutter import MyFoxApiGroupShutterClient
from ..api.myfoxapi_socket import MyFoxApiSocketClient
from ..api.myfoxapi_group_electric import MyFoxApiGroupElectricClient
from ..api.myfoxapi_temperature import MyFoxApiTemperatureClient
from ..api.myfoxapi_light import MyFoxApiLightClient
from ..api.myfoxapi_state_alerte import MyFoxApiAlerteStateClient
from ..api.myfoxapi_state import MyFoxApiStateClient
from ..api.myfoxapi_heater import MyFoxApiHeaterClient
from ..api.myfoxapi_thermo import MyFoxApThermoClient
from ..api.myfoxapi_scenario import MyFoxApiSecenarioClient
from ..api.myfoxapi_security import MyFoxApiSecurityClient
from ..api.myfoxapi_camera import MyFoxApiCameraClient
from ..api.myfoxapi_gate import MyFoxApiGateClient
from ..api.myfoxapi_module import MyFoxApiModuleClient

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


class MyFoxCoordinator(DataUpdateCoordinator) :
    """ Corrd inator pour synchro avec les appels API MyFox """

    def __init__(self, hass: HomeAssistant,  pooling_frequency: int):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="MyFox coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=pooling_frequency),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.myfoxApiClient =  dict[str, MyFoxApiClient]()

        _LOGGER.info("Init " + str(self.name) + " avec un pooling de " + str(pooling_frequency) + " minutes")


    def stop(self) :
        """ Arret des process """

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
            _LOGGER.info("Load data from : %s", str(self.name))
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

                    # cas d'un client security
                    if myfoxApiClient.__class__ == MyFoxApiSecurityClient :
                        
                        client:MyFoxApiSecurityClient = myfoxApiClient
                        for temp in client.security :
                            self.addToParams(params, listening_idx, temp)

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
                    if myfoxApiClient.__class__ == MyFoxApiAlerteStateClient :
                        
                        client:MyFoxApiAlerteStateClient = myfoxApiClient
                        for temp in client.sensor :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client sensor alert
                    if myfoxApiClient.__class__ == MyFoxApiStateClient :
                        
                        client:MyFoxApiStateClient = myfoxApiClient
                        for temp in client.sensor :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client heater
                    if myfoxApiClient.__class__ == MyFoxApiHeaterClient :
                        
                        client:MyFoxApiHeaterClient = myfoxApiClient
                        for temp in client.heater :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client thermo
                    if myfoxApiClient.__class__ == MyFoxApThermoClient :
                        
                        client:MyFoxApThermoClient = myfoxApiClient
                        for temp in client.heater :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client scenario
                    if myfoxApiClient.__class__ == MyFoxApiSecenarioClient :
                        
                        client:MyFoxApiSecenarioClient = myfoxApiClient
                        for temp in client.scenarii :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client gate
                    if myfoxApiClient.__class__ == MyFoxApiGateClient :
                        
                        client:MyFoxApiGateClient = myfoxApiClient
                        for temp in client.gate :
                            self.addToParams(params, listening_idx, temp)

                    # cas d'un client module
                    if myfoxApiClient.__class__ == MyFoxApiModuleClient :
                        
                        client:MyFoxApiModuleClient = myfoxApiClient
                        for temp in client.gate :
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
        if "scenarioId" in temp :
            scene_id = temp["scenarioId"]
            for key,val in temp.items() :
                control_key = str(scene_id) + "|" + str(key)
                if control_key in listening_idx or len(listening_idx) == 0 :
                    params[control_key] = val
                    _LOGGER.debug("addToParams -> scenarioId(%s) : %s [%s]", str(scene_id), control_key, str(val))
        
    async def pressButton(self, idx:str) -> bool :
        """ Appuis sur un bouton et transmission au bon client """
        action_ok = False
        try:
            _LOGGER.info("Press button : %s from %s", idx, str(self.name))
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
                elif myfoxApiClient.__class__ == MyFoxApiCameraClient :
                    client:MyFoxApiCameraClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "snapshot" :
                            """ snapshot """
                            action_ok = await client.cameraSnapshotTake(int(device_id))
                            break
                        elif device_action == "recording_start" :
                            """ recording_start """
                            action_ok = await client.cameraRecordingStart(int(device_id))
                            break
                        elif device_action == "recording_stop" :
                            """ cameraRecordingStop """
                            action_ok = await client.cameraRecordingStop(int(device_id))
                            break
                        elif device_action == "shutter_open" :
                            """ shutter_open """
                            action_ok = await client.cameraShutterOpen(int(device_id))
                            break
                        elif device_action == "shutter_close" :
                            """ shutter_close """
                            action_ok = await client.cameraShutterClose(int(device_id))
                            break
                        elif device_action == "live_start" :
                            """ live_start """
                            action_ok = await client.cameraLiveStart(int(device_id), "hls")
                            break
                        elif device_action == "live_extend" :
                            """ live_extend """
                            action_ok = await client.cameraLiveExtend(int(device_id))
                            break
                        elif device_action == "live_stop" :
                            """ live_stop """
                            action_ok = await client.cameraLiveStop(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
                elif myfoxApiClient.__class__ == MyFoxApiGateClient :
                    client:MyFoxApiGateClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "performeOne" :
                            """ performeOne """
                            action_ok = await client.performeOne(int(device_id))
                            break
                        elif device_action == "performeTwo" :
                            """ performeTwo """
                            action_ok = await client.performeTwo(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
                elif myfoxApiClient.__class__ == MyFoxApiModuleClient :
                    client:MyFoxApiModuleClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        if device_action == "performeOne" :
                            """ performeOne """
                            action_ok = await client.performeOne(int(device_id))
                            break
                        elif device_action == "performeTwo" :
                            """ performeTwo """
                            action_ok = await client.performeTwo(int(device_id))
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("pressButton %s  non reconnue pour le device %s", str(device_action), str(device_id))
            _LOGGER.debug("pressButton %s pour le volet %s : %s", str(device_action), str(device_id), str(action_ok) )

            if action_ok :
                params = dict[str, Any]()
                listening_idx = set()
                listening_idx.add(idx)
                valeur = dict[str, Any]()
                valeur["deviceId"] = device_id
                valeur["device_action"] = device_action
                self.addToParams(params, listening_idx, valeur)
                self.async_set_updated_data(params)
            return action_ok
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return action_ok
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")

    async def playScenario(self, idx:str) -> bool :
        _LOGGER.info("playScenario : %s from %s", idx, str(self.name))
        valeurs = idx.split("|", 2)
        scenario_id = valeurs[0]
        scenario_type = valeurs[1]
        action_ok = False
        for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
            if myfoxApiClient.__class__ == MyFoxApiSecenarioClient :
                client:MyFoxApiSecenarioClient = myfoxApiClient
                if scenario_id in client.scenes :
                    action_ok = await client.playScenario(int(scenario_id))
                    break
        _LOGGER.debug("playScenario %s : %s", str(idx), str(action_ok) )

        if action_ok :
            params = dict[str, Any]()
            listening_idx = set()
            listening_idx.add(idx)
            valeur = dict[str, Any]()
            valeur["scenarioId"] = scenario_id
            valeur["typeLabel "] = scenario_type
            valeur["enabled"] = "None"
            self.addToParams(params, listening_idx, valeur)
            self.async_set_updated_data(params)

    async def enableScenario(self, idx:str) -> bool :
        _LOGGER.info("enableScenario : %s from %s", idx, str(self.name))
        valeurs = idx.split("|", 2)
        scenario_id = valeurs[0]
        scenario_type = valeurs[1]
        action_ok = False
        for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
            if myfoxApiClient.__class__ == MyFoxApiSecenarioClient :
                client:MyFoxApiSecenarioClient = myfoxApiClient
                if scenario_id in client.scenes :
                    action_ok = await client.enableScenario(int(scenario_id))
                    break
        _LOGGER.debug("enableScenario %s : %s", str(idx), str(action_ok) )

        if action_ok :
            params = dict[str, Any]()
            listening_idx = set()
            listening_idx.add(idx)
            valeur = dict[str, Any]()
            valeur["scenarioId"] = scenario_id
            valeur["typeLabel "] = scenario_type
            valeur["enabled"] = True
            self.addToParams(params, listening_idx, valeur)
            self.async_set_updated_data(params)

    async def disableScenario(self, idx:str) -> bool :
        _LOGGER.info("disableScenario : %s from %s", idx, str(self.name))
        valeurs = idx.split("|", 2)
        scenario_id = valeurs[0]
        scenario_type = valeurs[1]
        action_ok = False
        for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
            if myfoxApiClient.__class__ == MyFoxApiSecenarioClient :
                client:MyFoxApiSecenarioClient = myfoxApiClient
                if scenario_id in client.scenes :
                    action_ok = await client.disableScenario(int(scenario_id))
                    break
        _LOGGER.debug("disableScenario %s : %s", str(idx), str(action_ok) )

        if action_ok :
            params = dict[str, Any]()
            listening_idx = set()
            listening_idx.add(idx)
            valeur = dict[str, Any]()
            valeur["scenarioId"] = scenario_id
            valeur["typeLabel "] = scenario_type
            valeur["enabled"] = False
            self.addToParams(params, listening_idx, valeur)
            self.async_set_updated_data(params)

    async def selectOption(self, idx:str, option:str) -> bool :
        """ Selection option et transmission au bon client """
        action_ok = False
        try:
            _LOGGER.info("Select Option : %s/%s from %s", idx, option, str(self.name))
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
                elif myfoxApiClient.__class__ == MyFoxApiSecurityClient :
                    client:MyFoxApiSecurityClient = myfoxApiClient
                    # verification device
                    _LOGGER.debug("selectOption '%s' for '%s'", str(device_action), str(device_option) )
                    if device_id in client.devices :
                        """ """
                        if int(device_action) == 1 :
                            """ Disarmed """
                            action_ok = await client.setSecurity("disarmed")
                            break
                        elif int(device_action) == 2 :
                            """ Partial """
                            action_ok = await client.setSecurity("partial")
                            break
                        elif int(device_action) == 4 :
                            """ Armed """
                            action_ok = await client.setSecurity("armed")
                            break
                        else :
                            """ inconnu """
                            _LOGGER.error("selectOption '%s' non reconnue pour le device %s", str(device_action), str(device_id))
            _LOGGER.debug("selectOption %s pour %s : %s", str(device_action), str(idx), str(action_ok) )

            if action_ok :
                params = dict[str, Any]()
                listening_idx = set()
                listening_idx.add(idx)
                valeur = dict[str, Any]()
                valeur["deviceId"] = device_id
                valeur[device_option] = device_action
                self.addToParams(params, listening_idx, valeur)
                self.async_set_updated_data(params)
                
            return action_ok
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return action_ok
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")

    async def cameraLiveStart(self, idx:str, protocol:str) -> str :
        """ Selection option et transmission au bon client """
        retour_url:str = None
        try:
            _LOGGER.debug("cameraLiveStart : %s from %s with protocol %s", idx, str(self.name), protocol)
            valeurs = idx.split("|", 2)
            device_id = valeurs[0]
            # recherche du client et du device
            for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                if myfoxApiClient.__class__ == MyFoxApiCameraClient :
                    client:MyFoxApiCameraClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ live """
                        retour_url = await client.cameraLiveStart(int(device_id), protocol)
                        break

            return retour_url
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return retour_url
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")
        
    async def cameraLiveStop(self, idx:str) -> bytes :
        """ Selection option et transmission au bon client """
        retour_url = None
        try:
            _LOGGER.info("cameraLiveStop : %s from %s", idx, str(self.name))
            valeurs = idx.split("|", 2)
            device_id = valeurs[0]
            device_option = valeurs[1]
            # recherche du client et du device
            for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                if myfoxApiClient.__class__ == MyFoxApiCameraClient :
                    client:MyFoxApiCameraClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        retour_url = await client.cameraLiveStop(int(device_id))
                        break
               
            return retour_url
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return retour_url
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")


    async def cameraPreviewTake(self, idx:str) -> bytes :
        """ Selection option et transmission au bon client """
        retour_byte:bytes = None
        try:
            _LOGGER.debug("cameraPreviewTake : %s from %s", idx, str(self.name))
            valeurs = idx.split("|", 2)
            device_id = valeurs[0]
            # recherche du client et du device
            for (client_key,myfoxApiClient) in self.myfoxApiClient.items() :
                if myfoxApiClient.__class__ == MyFoxApiCameraClient :
                    client:MyFoxApiCameraClient = myfoxApiClient
                    # verification device
                    if device_id in client.devices :
                        """ """
                        """ on """
                        retour_byte = await client.cameraPreviewTake(int(device_id))
                        break

            return retour_byte
        except MyFoxException as exception:
            _LOGGER.error(exception)
            return retour_byte
        except Exception as err:
            raise UpdateFailed(f"Error with API: {err}")