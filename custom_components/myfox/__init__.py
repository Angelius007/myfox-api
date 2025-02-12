import logging
import time

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.util.hass_dict import HassEntryKey


from homeassistant.components.application_credentials import (
    ClientCredential, ApplicationCredentialsStorageCollection, DOMAIN as DOMAIN_CREDENTIAL
)
from .api.myfoxapi_exception import (MyFoxException)

from .api.const import (
    KEY_CLIENT_ID,
    KEY_CLIENT_SECRET,
    KEY_MYFOX_USER,
    KEY_MYFOX_PSWD,
    KEY_TOKEN,
    KEY_ACCESS_TOKEN,
    KEY_REFRESH_TOKEN,
    KEY_EXPIRE_IN,
    KEY_EXPIRE_AT,
    KEY_EXPIRE_TIME,
    KEY_SITE_ID,
    KEY_CACHE_EXPIRE_IN,
    KEY_AUTH_IMPLEMENTATION,
    CACHE_EXPIRE_IN,
    POOLING_INTERVAL_DEF,
    KEY_POOLING_INTERVAL,
    KEY_CACHE_CAMERA,
    CACHE_CAMERA,
    KEY_CACHE_SECURITY,
    CACHE_SECURITY,
    KEY_USE_CODE_ALARM,
    KEY_AUTHORIZED_CODE_ALARM
)
from .api import (
    MyFoxEntryDataApi,
    MyFoxOptionsDataApi
)
from .api.myfoxapi import (
    MyFoxApiClient
)

from .api.myfoxapi_camera import (MyFoxApiCameraClient)
from .api.myfoxapi_light import (MyFoxApiLightClient)
from .api.myfoxapi_security import (MyFoxApiSecurityClient)
from .api.myfoxapi_scenario import (MyFoxApiSecenarioClient)
from .api.myfoxapi_state import (MyFoxApiStateClient)
from .api.myfoxapi_state_alerte import (MyFoxApiAlerteStateClient)
from .api.myfoxapi_temperature import (MyFoxApiTemperatureClient)
from .api.myfoxapi_gate import (MyFoxApiGateClient)
from .api.myfoxapi_module import (MyFoxApiModuleClient)
from .api.myfoxapi_shutter import (MyFoxApiShutterClient)
from .api.myfoxapi_socket import (MyFoxApiSocketClient)
from .api.myfoxapi_group_electric import (MyFoxApiGroupElectricClient)
from .api.myfoxapi_group_shutter import (MyFoxApiGroupShutterClient)
from .api.myfoxapi_heater import (MyFoxApiHeaterClient)
from .api.myfoxapi_thermo import (MyFoxApThermoClient)
from .coordinator.myfox_coordinator import (MyFoxCoordinator)
from .api.myfoxapi_exception import (InvalidTokenMyFoxException)

from .const import (DOMAIN_MYFOX, CONFIG_VERSION)

_LOGGER = logging.getLogger(__name__)
MYFOX_KEY: HassEntryKey["MyFoxCoordinator"] = HassEntryKey(DOMAIN_MYFOX)

_PLATFORMS = {
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.SCENE,
    Platform.CAMERA,
    Platform.ALARM_CONTROL_PANEL
}

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""
    old_version = config_entry.version
    if old_version < CONFIG_VERSION :
        """ Action en cas d'ancienne version detectee """
        new_data = {**config_entry.data}
        new_options = {**config_entry.options}
        if old_version < 2 :
            """ Migration token dans le bloc token """
            if KEY_TOKEN not in new_data :
                new_data[KEY_TOKEN] = {
                    KEY_ACCESS_TOKEN  : new_data.pop(KEY_ACCESS_TOKEN, ""),
                    KEY_REFRESH_TOKEN : new_data.pop(KEY_REFRESH_TOKEN, ""),
                    KEY_EXPIRE_IN     : new_data.pop(KEY_EXPIRE_IN, ""),
                    KEY_EXPIRE_AT     : new_data.pop(KEY_EXPIRE_TIME, ""),
                    "token_type"      : "Bearer",
                }
            # suppression anciennes clefs
            new_data.pop(KEY_ACCESS_TOKEN, "")
            new_data.pop(KEY_REFRESH_TOKEN, "")
            new_data.pop(KEY_EXPIRE_IN, "")
            new_data.pop(KEY_EXPIRE_TIME, "")
            new_data.pop(KEY_CLIENT_ID, "")
            new_data.pop(KEY_CLIENT_SECRET, "")
            new_data.pop(KEY_MYFOX_USER, "")
            new_data.pop(KEY_MYFOX_PSWD, "")

        hass.config_entries.async_update_entry(config_entry, data=new_data, options=new_options, version=CONFIG_VERSION)
        _LOGGER.info("Migration from version %s to version %s successful", old_version, CONFIG_VERSION)
    return True

def getClientCredential(hass: HomeAssistant, entry: ConfigEntry) -> ClientCredential :
    if KEY_AUTH_IMPLEMENTATION in entry.data :
        auth_implementation = entry.data[KEY_AUTH_IMPLEMENTATION]
        if DOMAIN_CREDENTIAL in hass.data :
            application_credential:ApplicationCredentialsStorageCollection = hass.data[DOMAIN_CREDENTIAL]
            credentials = application_credential.async_client_credentials(DOMAIN_MYFOX)
            if auth_implementation in credentials :
                credential:ClientCredential = credentials[auth_implementation]
                client_name   = credential.name
                _LOGGER.debug("Credential selectionne %s", str(client_name))
                return credential
    return None

def updateMyFoxOptions(entry: ConfigEntry) -> MyFoxOptionsDataApi :
    options = MyFoxOptionsDataApi()
    # frequence de pooling du coordinator
    if KEY_POOLING_INTERVAL in entry.options :
        options.pooling_frequency = entry.options[KEY_POOLING_INTERVAL]
    else :
        options.pooling_frequency = POOLING_INTERVAL_DEF
    # cache global par defaut
    if KEY_CACHE_EXPIRE_IN in entry.options :
        options.cache_time = entry.options[KEY_CACHE_EXPIRE_IN]
    else :
        options.cache_time = CACHE_EXPIRE_IN
    # cache specifique de la camera
    if KEY_CACHE_CAMERA in entry.options :
        options.cache_camera_time = entry.options[KEY_CACHE_CAMERA]
    else :
        options.cache_camera_time = CACHE_CAMERA
    # cache specifique de la securite
    if KEY_CACHE_SECURITY in entry.options :
        options.cache_security_time = entry.options[KEY_CACHE_SECURITY]
    else :
        options.cache_security_time = CACHE_SECURITY
    # utilisation ou non d'un code de securite pour l'alarme
    if KEY_USE_CODE_ALARM in entry.options :
        options.use_code_alarm = entry.options[KEY_USE_CODE_ALARM]
    else :
        options.use_code_alarm = False
    # liste des codes possibles pour l'alarme
    if KEY_AUTHORIZED_CODE_ALARM in entry.options :
        options.secure_codes = entry.options[KEY_AUTHORIZED_CODE_ALARM]
    else :
        options.secure_codes = ""

    return options

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if DOMAIN_MYFOX not in hass.data:
        hass.data.setdefault(MYFOX_KEY, {})
    
    client_id = None
    if KEY_CLIENT_ID in entry.data :
        client_id = entry.data[KEY_CLIENT_ID]
    client_secret = None
    if KEY_CLIENT_SECRET in entry.data :
        client_secret = entry.data[KEY_CLIENT_SECRET]

    credential:ClientCredential = getClientCredential(hass, entry)
    if credential :
        client_id     = credential.client_id
        client_secret = credential.client_secret

    myfox_info = MyFoxEntryDataApi(client_id=client_id,
                                   client_secret=client_secret,
                                   access_token=entry.data[KEY_TOKEN][KEY_ACCESS_TOKEN],
                                   refresh_token=entry.data[KEY_TOKEN][KEY_REFRESH_TOKEN],
                                   expires_in=entry.data[KEY_TOKEN][KEY_EXPIRE_IN],
                                   expires_time=entry.data[KEY_TOKEN][KEY_EXPIRE_AT])
    if myfox_info.expires_time > 0 :
        _LOGGER.info("-> Tokens à jour jusqu'a %s", str(time.ctime(myfox_info.expires_time)))

    myfox_info.options = updateMyFoxOptions(entry)

    info_site = None
    coordinator = MyFoxCoordinator(hass, myfox_info.options, entry)
    hass.data.setdefault(MYFOX_KEY, {})[entry.entry_id] = coordinator
    try:
        myfox_client = MyFoxApiClient(myfox_info)
        coordinator.add_client(myfox_client)
        
        info_site = await myfox_client.getInfoSite(entry.data[KEY_SITE_ID])
        _LOGGER.debug("Chargement du site %s", str(info_site))
    except InvalidTokenMyFoxException as err:   
        # Raising ConfigEntryAuthFailed will cancel future updates
        # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        raise ConfigEntryAuthFailed from err
    except MyFoxException as exception:
        _LOGGER.error(exception)
        raise ConfigEntryNotReady("Service temporairement indisponible")

    retour = True
        
    if info_site :
        """Recherche des devices."""
        # add Alarme
        retour &= await addSecurity(hass, entry, myfox_info)
        # cameraCount: int = 0
        if myfox_client.myfox_info.site.cameraCount > 0 :
            retour &= await addCamera(hass, entry, myfox_info)
        # gateCount: int = 0
        if myfox_client.myfox_info.site.gateCount > 0 :
            retour &= await addGate(hass, entry, myfox_info)
        # shutterCount: int = 0
        if myfox_client.myfox_info.site.shutterCount > 0 :
            retour &= await addShutter(hass, entry, myfox_info)
        # socketCount: int = 0
        if myfox_client.myfox_info.site.socketCount > 0 :
            retour &= await addSocket(hass, entry, myfox_info)
        # moduleCount: int = 0
        if myfox_client.myfox_info.site.moduleCount > 0 :
            retour &= await addModule(hass, entry, myfox_info)
        # heaterCount: int = 0
        if myfox_client.myfox_info.site.heaterCount > 0 :
            retour &= await addHeater(hass, entry, myfox_info)
        # scenarioCount: int = 0
        if myfox_client.myfox_info.site.scenarioCount > 0 :
            retour &= await addScenario(hass, entry, myfox_info)
        # deviceStateCount: int = 0
        if myfox_client.myfox_info.site.deviceStateCount > 0 :
            retour &= await addDeviceState(hass, entry, myfox_info)
        # deviceLightCount: int = 0
        if myfox_client.myfox_info.site.deviceLightCount > 0 :
            retour &= await addDeviceLight(hass, entry, myfox_info)
        # deviceDetectorCount: int = 0
        if myfox_client.myfox_info.site.deviceDetectorCount > 0 :
            retour &= await addDetectorDevice(hass, entry, myfox_info)
        # Sondes de temperature
        if myfox_client.myfox_info.site.deviceTemperatureCount > 0 :
            retour &= await addTemperatureDevice(hass, entry, myfox_info)

        if not retour:
            raise ConfigEntryNotReady("Service partiellement chargé")

        # prepa coordinator
        await coordinator.async_config_entry_first_refresh()

        new_data = {**entry.data}
        
        hass.config_entries.async_update_entry(entry, data=new_data, options=entry.options)
        await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
        entry.async_on_unload(entry.add_update_listener(update_listener))


        return retour
    else :
        _LOGGER.warning("Pas de site trouve pour l'identifiant %s",entry.data[KEY_SITE_ID])
        raise ConfigEntryNotReady("Service temporairement indisponible")

async def addCamera(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Camera")
    return await addClientToCoordinator(hass, entry, MyFoxApiCameraClient(myfox_info))

async def addGate(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Gate")
    return await addClientToCoordinator(hass, entry, MyFoxApiGateClient(myfox_info))

async def addSecurity(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Security")
    return await addClientToCoordinator(hass, entry, MyFoxApiSecurityClient(myfox_info))
    
async def addShutter(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Shutter")
    retour  = await addClientToCoordinator(hass, entry, MyFoxApiShutterClient(myfox_info))
    _LOGGER.debug("Add Group Shutter")
    retour &= await addClientToCoordinator(hass, entry, MyFoxApiGroupShutterClient(myfox_info))
    return retour
    
async def addSocket(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Socket")
    retour  = await addClientToCoordinator(hass, entry, MyFoxApiSocketClient(myfox_info))
    _LOGGER.debug("Add Group Socket")
    retour &= await addClientToCoordinator(hass, entry, MyFoxApiGroupElectricClient(myfox_info))
    return retour

async def addModule(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Module")
    return await addClientToCoordinator(hass, entry, MyFoxApiModuleClient(myfox_info))

async def addHeater(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Heater")

    retour  = await addClientToCoordinator(hass, entry, MyFoxApiHeaterClient(myfox_info))
    retour &= await addClientToCoordinator(hass, entry, MyFoxApThermoClient(myfox_info))
    return retour

async def addScenario(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Scenario")
    return await addClientToCoordinator(hass, entry, MyFoxApiSecenarioClient(myfox_info))

async def addDeviceState(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add State Device")
    return await addClientToCoordinator(hass, entry, MyFoxApiStateClient(myfox_info))

async def addDeviceLight(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Light Device")
    return await addClientToCoordinator(hass, entry, MyFoxApiLightClient(myfox_info))

async def addDetectorDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    """ """
    _LOGGER.debug("Add Detector Device")
    return await addClientToCoordinator(hass, entry, MyFoxApiAlerteStateClient(myfox_info))

async def addTemperatureDevice(hass: HomeAssistant, entry: ConfigEntry, myfox_info:MyFoxEntryDataApi):
    _LOGGER.debug("Add Temperature Device")
    return await addClientToCoordinator(hass, entry, MyFoxApiTemperatureClient(myfox_info))

async def addClientToCoordinator(hass: HomeAssistant, entry: ConfigEntry, client:MyFoxApiClient) :
    """" """
    _LOGGER.debug("-> Get devices")
    try :
        liste_capteurs = await client.getList()
        for capteur in liste_capteurs :
            _LOGGER.debug("Configuration device " + str(capteur))
            deviceId = 0
            scenarioId = 0
            label = ""
            modelId = 0
            modelLabel = ""
            typeLabel = ""
            enabled = ""
            if "deviceId" in capteur :
                deviceId = capteur["deviceId"]
            elif "groupId" in capteur :
                deviceId = capteur["groupId"]
            if "scenarioId" in capteur :
                scenarioId = capteur["scenarioId"]
            if "label" in capteur :
                label = capteur["label"]
            if "modelId" in capteur :
                modelId = capteur["modelId"]
            if "modelLabel" in capteur :
                modelLabel = capteur["modelLabel"]
            elif "type" in capteur :
                modelLabel = capteur["type"]
            if "typeLabel" in capteur :
                typeLabel = capteur["typeLabel"]
            if "enabled" in capteur :
                enabled = capteur["enabled"]

            if deviceId > 0 :
                client.configure_device(deviceId, label, modelId, modelLabel)
            if scenarioId > 0 :
                client.configure_scene(scenarioId, label, typeLabel, enabled)

        if liste_capteurs.__len__() > 0 :
            coordinator:MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {})[entry.entry_id]
            coordinator.add_client(client)
        
        return True

    except MyFoxException as exception:
        _LOGGER.error("%s : Imposslble de charger le client %s", str(exception), client.__class__)
        return False
    except Exception as exception:
        _LOGGER.error("%s : Imposslble de charger le client %s", str(exception), client.__class__)
        return False
    
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if not await hass.config_entries.async_unload_platforms(entry, _PLATFORMS):
        return False

    coordinator:MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {}).pop(entry.entry_id)
    for (type,hassclient) in coordinator.myfoxApiClients.items() :
        client: MyFoxApiClient = hassclient
        client.stop()
    coordinator.stop()
    return True

async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    _LOGGER.debug("-> Mise à jour Entite")
    coordinator:MyFoxCoordinator = hass.data.setdefault(MYFOX_KEY, {})[config_entry.entry_id]
    new_data = {**config_entry.data}

    credential:ClientCredential = getClientCredential(hass, config_entry)
    if credential and coordinator :
        myfox_info:MyFoxEntryDataApi = coordinator.getMyFoxInfo()
        myfox_info.client_id         = credential.client_id
        myfox_info.client_secret     = credential.client_secret

        # mise a jour des options
        myfox_info.options = updateMyFoxOptions(config_entry)

        # Si le token de conf est plus lointain, on ecrase le token client,sinon, on reprend le token client dans la conf
        expires_time:float = config_entry.data[KEY_TOKEN][KEY_EXPIRE_AT]
        if(expires_time > myfox_info.expires_time ) :
            myfox_info.access_token  = config_entry.data[KEY_TOKEN][KEY_ACCESS_TOKEN]
            myfox_info.refresh_token = config_entry.data[KEY_TOKEN][KEY_REFRESH_TOKEN]
            myfox_info.expires_in    = config_entry.data[KEY_TOKEN][KEY_EXPIRE_IN]
            myfox_info.expires_time  = config_entry.data[KEY_TOKEN][KEY_EXPIRE_AT]
        else :
            # Mise a jour des confs
            new_data[KEY_TOKEN][KEY_ACCESS_TOKEN]  =  myfox_info.access_token
            new_data[KEY_TOKEN][KEY_REFRESH_TOKEN] =  myfox_info.refresh_token
            new_data[KEY_TOKEN][KEY_EXPIRE_IN]     =  myfox_info.expires_in
            new_data[KEY_TOKEN][KEY_EXPIRE_AT]     =  myfox_info.expires_time
        
        coordinator.updateMyfoxinfo(myfox_info)
        coordinator.updateTokens(new_data[KEY_TOKEN])
        _LOGGER.debug("-> Tokens à jour jusqu'a %s", str(time.ctime(myfox_info.expires_time)))
        
        hass.config_entries.async_update_entry(config_entry, data=new_data, options=config_entry.options)

        # si mise a jour du coordinator, on relance le chargement
        if (coordinator.options.pooling_frequency != myfox_info.options.pooling_frequency 
            or coordinator.options.use_code_alarm != myfox_info.options.use_code_alarm):
            _LOGGER.info("-> Rechargement Entite suite à modification de parametrage")
            hass.config_entries.async_schedule_reload(config_entry.entry_id)

    else :
        _LOGGER.info("-> Rechargement Entite")
        hass.config_entries.async_schedule_reload(config_entry.entry_id)
