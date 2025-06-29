import logging
import urllib.parse
import aiohttp
import asyncio
import selectors
import time
import urllib

from abc import abstractmethod
from typing import Any
from aiohttp import ClientResponse, hdrs
from .const import (
    DEFAULT_MYFOX_URL_API, MYFOX_TOKEN_PATH, MYFOX_INFO_SITE_PATH, MYFOX_HISTORY_GET,
    KEY_GRANT_TYPE, KEY_CLIENT_ID, KEY_CLIENT_SECRET, KEY_MYFOX_USER, KEY_MYFOX_PSWD, KEY_REFRESH_TOKEN,
    KEY_EXPIRE_IN, KEY_EXPIRE_AT, KEY_ACCESS_TOKEN, GRANT_TYPE_PASSWORD, GRANT_REFRESH_TOKEN, SEUIL_EXPIRE_MIN,
    CONTENT_TYPE_JSON, CONTENT_TYPE_HTML
)
from ..scenes import (BaseScene, DiagnosticScene, MyFoxSceneInfo)
from ..devices import (BaseDevice, DiagnosticDevice, MyFoxDeviceInfo)
from ..devices.site import MyFoxSite
from .myfoxapi_exception import (MyFoxException, InvalidTokenMyFoxException, RetryMyFoxException)
from . import MyFoxEntryDataApi

_LOGGER = logging.getLogger(__name__)


class MyFoxPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        selector = selectors.SelectSelector()
        return asyncio.SelectorEventLoop(selector)


class MyFoxApiClient:

    def __init__(self, myfox_info: MyFoxEntryDataApi) -> None:
        self.client_key = "generic"
        self.client = None
        self.devices: dict[str, BaseDevice] = {}
        self.scenes: dict[str, BaseScene] = {}
        self.infoSites_times = 0
        self.history = list()
        self.history_time = 0
        self.saveMyFoxInfo(myfox_info)

    def saveMyFoxInfo(self, myfox_info: MyFoxEntryDataApi) :
        self.myfox_info: MyFoxEntryDataApi = myfox_info
        self.cache_expire_in = myfox_info.options.cache_time
        self.nb_retry = myfox_info.options.nb_retry_default
        self.delay_between_retry = myfox_info.options.delay_between_retry

    def configure_device(self, deviceId: int, label: str, modelId: int, modelLabel: str):
        """ Configuration device """
        info = self.__create_device_info(deviceId, label, modelId, modelLabel)
        from ..devices.registry import device_by_product, device_by_model_label, device_by_client_key
        device = None
        # Type indique dans l'implementation de l'api
        if self.client_key in device_by_client_key:
            device = device_by_client_key[str(self.client_key)](info)
        # Sinon, recherche par modele
        elif modelLabel in device_by_model_label:
            device = device_by_model_label[str(modelLabel)](info)
        # Si non renseigne, recherche via le deviceId
        elif str(deviceId) in device_by_product:
            device = device_by_product[str(deviceId)](info)
        # Sinon, on positionne en Diagnostic
        else:
            device = DiagnosticDevice(info)
        _LOGGER.debug("New device : %s", str(device))
        self.add_device(device)

    def add_device(self, device: BaseDevice):
        if device :
            self.devices[str(device.device_info.deviceId)] = device

    def __create_device_info(self, deviceId: int, label: str, modelId: int, modelLabel: str) -> MyFoxDeviceInfo:
        return MyFoxDeviceInfo(deviceId,
                               label,
                               modelId,
                               modelLabel)

    def configure_scene(self, scenarioId: int, label: str, typeLabel: str, enabled: str):
        """ Configuration device """
        info = self.__create_scene_info(scenarioId, label, typeLabel, enabled)
        from ..scenes.registry import scene_by_typeLabel_key
        scene = None
        # Type indique dans l'implementation de l'api
        if info.typeLabel in scene_by_typeLabel_key:
            scene = scene_by_typeLabel_key[str(info.typeLabel)](info)
        # Sinon, on positionne en Diagnostic
        else:
            scene = DiagnosticScene(info)
        _LOGGER.debug("New scene : %s", str(scene))
        self.add_scene(scene)

    def add_scene(self, scene: BaseScene):
        if scene :
            self.scenes[str(scene.scene_info.scenarioId)] = scene

    def __create_scene_info(self, scenarioId: int, label: str, typeLabel: str, enabled: str) -> MyFoxSceneInfo:
        return MyFoxSceneInfo(scenarioId,
                              label,
                              typeLabel,
                              enabled)

    def getUrlMyFoxApi(self, path: str) :
        """ Formattage URL """
        url = f"{DEFAULT_MYFOX_URL_API}{path}"
        return url

    async def updateDevices(self) :
        """ Mise a jour de chaque device """
        for device in self.devices :
            await self.updateDevices(device)

    @abstractmethod
    async def updateDevice(self, device: BaseDevice) :
        """ Miser a jour d'un device """
        pass

    @abstractmethod
    async def getList(self) -> list[Any]:
        """ Liste """
        pass

    async def callMyFoxApiGet(self, path: str, data=None, retry: int = 0):
        """ Appel API en GET """
        return await self.callMyFoxApiWithSession_(path, data, "GET", "json", retry=retry)

    async def callMyFoxApiBinaryGet(self, path: str, data=None, retry: int = 0):
        """ Appel API en GET """
        return await self.callMyFoxApiWithSession_(path, data, "GET", "binary", retry)

    async def callMyFoxApiPost(self, path: str, data=None, retry: int = 0):
        """ Appel API en POST """
        return await self.callMyFoxApiWithSession_(path, data, "POST", "json", retry=retry)

    async def callMyFoxApiBinaryPost(self, path: str, data=None, retry: int = 0):
        """ Appel API en POST """
        return await self.callMyFoxApiWithSession_(path, data, "POST", "binary", retry)

    async def callMyFoxApiWithSession_(self, path: str, data=None, method: str = "POST",
                                       responseClass: str = "json", retry: int = 0):
        """ Appel API """
        try:
            async with aiohttp.ClientSession() as session:
                return await self.callMyFoxApi_(session, path, data, method, responseClass, retry)
        except MyFoxException as exception:
            """ Retry """
            if retry < self.nb_retry :
                await asyncio.sleep(self.delay_between_retry)  # tempo de qqes secondes pour relancer la requete
                return await self.callMyFoxApiWithSession_(path, data, method, responseClass, retry=(retry + 1))
            else :
                _LOGGER.warning(exception)
                raise exception
        except Exception as exception:
            """ Retry """
            if retry < self.nb_retry :
                await asyncio.sleep(self.delay_between_retry)  # tempo de qqes secondes pour relancer la requete
                return await self.callMyFoxApiWithSession_(path, data, method, responseClass, retry=(retry + 1))
            else :
                _LOGGER.error(exception)
                raise MyFoxException(args=exception)

    async def callMyFoxApi_(self, session: aiohttp.ClientSession, path: str, data=None, method: str = "POST",
                            responseClass: str = "json", retry: int = 0):
        """ Appel API """
        _LOGGER.debug(f"Appel : {path}/{method}/{responseClass} - Essai : {retry}/{self.nb_retry}")
        try:
            headers = {
                hdrs.CONTENT_TYPE: CONTENT_TYPE_JSON
            }
            urlApi = self.getUrlMyFoxApi(path)
            if not data or KEY_GRANT_TYPE not in data :
                urlApi = urlApi + "?access_token=" + await self.getToken()
                if data is not None :
                    params = urllib.parse.urlencode(data)
                    urlApi = urlApi + "&" + str(params)
            _LOGGER.debug(f"Appel : {urlApi} - Essai : {retry}/{self.nb_retry}")
            if method == "POST":
                async with session.post(urlApi, headers=headers, json=data) as resp :
                    retour = await self._get_response(resp, responseClass)
            else :
                async with session.get(urlApi, headers=headers, json=data) as resp :
                    retour = await self._get_response(resp, responseClass)
            if retry > 0 :
                _LOGGER.info(f"Relance de la requete {path} : OK (Tentative : {(retry)}/{self.nb_retry})")
            return retour
        except InvalidTokenMyFoxException as exception:
            _LOGGER.error(f"InvalidTokenMyFoxException : {exception.status} - {exception.message}")
            raise exception
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error(f"Erreur {str(exception)}. Echec des relances {path} (Tentative : {retry}/{self.nb_retry})")
            raise MyFoxException(args=exception)

    async def _get_response(self, resp: ClientResponse, responseClass: str = "json"):
        if responseClass == "json" :
            return await self._get_json_response(resp)
        elif responseClass == "binary" :
            return await self._get_binary_response(resp)
        else :
            raise MyFoxException(f"Erreur de format pour la reponse : {responseClass}. (Choix possibles : json/binary)")

    async def _get_binary_response(self, resp: ClientResponse):
        """ Traitement de la reponse """
        ctype = resp.headers.get(hdrs.CONTENT_TYPE, "").lower()
        if resp.status == 401:
            try:
                if CONTENT_TYPE_JSON not in ctype :
                    json_resp = await resp.json()
                    raise InvalidTokenMyFoxException(resp.status, f"Error : {json_resp["error"]}")
                else :
                    html_resp = await resp.text()
                    raise InvalidTokenMyFoxException(resp.status, f"Error : {html_resp}")
            except MyFoxException as exception:
                raise exception
            except Exception as error:
                _LOGGER.error(error)
                raise MyFoxException(resp.status, f"Failed to parse response: {resp.text} Error: {error}")

        if resp.status != 200:
            raise MyFoxException(resp.status, f"Got HTTP status code {resp.status}: {resp.reason}")

        try:
            response = {
                "filename": str,
                "binary": bytes
            }
            response["binary"] = await resp.read()
            response["filename"] = "undefined"
            if resp and resp.content_disposition and resp.content_disposition.filename :
                filename = resp.content_disposition.filename
                _LOGGER.info(filename)
                response["filename"] = filename

            return response

        except Exception as error:
            _LOGGER.error(error)
            raise MyFoxException(f"Failed to parse response: {resp.text} Error: {error}")

    async def _get_json_response(self, resp: ClientResponse):
        """ Traitement de la reponse """
        ctype = resp.headers.get(hdrs.CONTENT_TYPE, "").lower()
        json_resp = None
        if CONTENT_TYPE_HTML in ctype :
            html_resp = await resp.text()
            _LOGGER.debug(f"Erreur : {resp.status} / {html_resp}")
            raise RetryMyFoxException(resp.status, f"Failed json call: {html_resp} - Error: unexpected mimetype")
        if resp.status == 401:
            try:
                if CONTENT_TYPE_JSON in ctype :
                    json_resp = await resp.json()
                    if "error" in json_resp :
                        raise InvalidTokenMyFoxException(resp.status, f"Error : {json_resp["error"]}")
                    else :
                        raise InvalidTokenMyFoxException(resp.status, f"Error no detail : {resp.status}")
                else :
                    raise MyFoxException(resp.status, f"Failed to parse response: Format {ctype} - Error: unexpected mimetype")
            except MyFoxException as exception:
                raise exception
            except Exception as error:
                _LOGGER.error(error)
                raise MyFoxException(resp.status, f"Failed to parse response: {resp.text} Error: {error}")

        if resp.status != 200:
            raise MyFoxException(resp.status, f"Got HTTP status code {resp.status}: {resp.reason}")

        try:
            if CONTENT_TYPE_JSON in ctype :
                json_resp = await resp.json()
                if "status" in json_resp and json_resp["status"] == "KO":
                    statut = 999
                    description = ""
                    error = ""
                    if "error_description" in json_resp:
                        description = json_resp["error_description"]
                    if "error" in json_resp:
                        error = json_resp["error"]
                        if "(632)" in error :
                            """ Erreur temporaire. Tentative de relance """
                            raise RetryMyFoxException(632, f"Error : {error} - Description: {description}")
                    raise MyFoxException(statut, f"Error : {error} - Description: {description}")
            else :
                raise MyFoxException(resp.status, f"Failed to parse response: Format {ctype} - Error: unexpected mimetype")

        except MyFoxException as exception:
            raise exception
        except Exception as error:
            _LOGGER.error(error)
            raise MyFoxException(resp.status, f"Failed to parse response: {resp.text} Error: {error}")

        return json_resp

    def stop(self) -> bool:
        return True

    async def login(self) -> bool :
        """ Recuperation des tokens """
        try:
            data = {
                KEY_GRANT_TYPE: GRANT_TYPE_PASSWORD,
                KEY_CLIENT_ID: self.myfox_info.client_id,
                KEY_CLIENT_SECRET: self.myfox_info.client_secret,
                KEY_MYFOX_USER: self.myfox_info.username,
                KEY_MYFOX_PSWD: self.myfox_info.password
            }

            response = await self.callMyFoxApiPost(MYFOX_TOKEN_PATH, str(data))
            # save des tokens
            self.saveToken(response)
            # en cas d'absence, recuperation du site
            await self.getInfoSites()

            return True
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + str(exception))
            return False

    async def refreshToken(self) -> bool:
        """ Rafraichissement des tokens """
        try:
            data = {
                KEY_GRANT_TYPE: GRANT_REFRESH_TOKEN,
                KEY_CLIENT_ID: self.myfox_info.client_id,
                KEY_CLIENT_SECRET: self.myfox_info.client_secret,
                KEY_REFRESH_TOKEN: self.myfox_info.refresh_token
            }
            _LOGGER.debug("Refresh token utilise : %s", str(self.myfox_info.refresh_token))

            response = await self.callMyFoxApiPost(MYFOX_TOKEN_PATH, str(data))
            # save des tokens
            self.saveToken(response)
            # en cas d'absence, recuperation du site
            await self.getInfoSites()

            return True
        except InvalidTokenMyFoxException as exception:
            raise exception
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + str(exception))
            return False

    # Sauvegarde du token
    def saveToken(self, response) :
        """ Sauvegarde des tokens """
        try:
            _LOGGER.debug("Response for token : %s", str(response))
            if KEY_ACCESS_TOKEN in response :
                self.myfox_info.access_token = response[KEY_ACCESS_TOKEN]
            if KEY_REFRESH_TOKEN in response :
                self.myfox_info.refresh_token = response[KEY_REFRESH_TOKEN]
            if KEY_EXPIRE_IN in response :
                self.myfox_info.expires_in = response[KEY_EXPIRE_IN]
            if KEY_EXPIRE_AT in response :
                self.myfox_info.expires_time = response[KEY_EXPIRE_AT]
            else :
                self.myfox_info.expires_time = (time.time() + self.myfox_info.expires_in)

        except KeyError as key:
            _LOGGER.error("Error : " + str(key))
            raise MyFoxException(f"Failed to extract key {key} from response: {response}")

    async def getToken(self) -> str:
        """ Recuperation des derniers tokens ou renouvellement si expire """
        try:
            expireDelay = self.getExpireDelay()
            if expireDelay == 0:  # jeton expire
                _LOGGER.debug("Jeton expire -> demande de renouvellement")
                await self.refreshToken()
                expireDelay = self.getExpireDelay()
            elif expireDelay < (SEUIL_EXPIRE_MIN):  # si jeton valide - de 5 min, on renouvelle
                # Token expire, on renouvelle
                _LOGGER.debug("Jeton bientot expire -> demande de renouvellement")
                await self.refreshToken()
                expireDelay = self.getExpireDelay()
            return self.myfox_info.access_token
        except InvalidTokenMyFoxException as exception:
            raise exception
        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + exception)
            raise MyFoxException(args=exception)

    def getExpireDelay(self) -> float :
        """ Calcul du temps restant """
        current_time = time.time()
        expires_time = self.myfox_info.expires_time
        expiration = expires_time - current_time
        if expiration < 0:
            expiration = 0
            _LOGGER.debug("Token expire")
        else:
            _LOGGER.debug("Expiration du token dans " + str(expiration) + " secondes a " + str(time.ctime(expires_time)))
        return expiration

    def isCacheExpire(self, start_time) -> float :
        return self.isCacheExpireWithParam(start_time, self.cache_expire_in)

    def isCacheExpireWithParam(self, start_time, param_expire) -> float :
        current_time = time.time()
        expiration = (current_time - start_time)
        _LOGGER.debug("Expiration cache - %s [%s / %s]", self.client_key, expiration, param_expire)
        return expiration >= param_expire

    async def getInfoSite(self, siteId: int, forceCall: bool = False) -> MyFoxSite:
        """ Recuperation info site """
        try:
            if self.myfox_info.site is None or self.myfox_info.site.siteId == 0 :
                sites = await self.getInfoSites(forceCall)

                for site in sites :
                    if int(site.siteId) == int(siteId) :
                        _LOGGER.debug("Site selectionne : %s", str(site))
                        self.myfox_info.site = site
                        return site
            else:
                _LOGGER.debug("Site deja connu : %s", str(self.myfox_info.site))
                return self.myfox_info.site

            _LOGGER.debug("Aucun site trouve avec l'id : %s", str(siteId))
            return None

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def getInfoSites(self, forceCall: bool = False) -> list[MyFoxSite]:
        """ Recuperation info site """
        try:
            if self.isCacheExpire(self.infoSites_times) or forceCall:
                _LOGGER.debug("Recherches de sites : (Forcage : %s)", str(forceCall))
                response = await self.callMyFoxApiGet(MYFOX_INFO_SITE_PATH)
                items = response["payload"]["items"]

                for item in items :
                    site = MyFoxSite(int(item["siteId"]),
                                     item["label"],
                                     str(item["siteId"]) + " - " + str(item["label"]),
                                     item["brand"],
                                     item["timezone"],
                                     item["AXA"],
                                     int(item["cameraCount"]),
                                     int(item["gateCount"]),
                                     int(item["shutterCount"]),
                                     int(item["socketCount"]),
                                     int(item["moduleCount"]),
                                     int(item["heaterCount"]),
                                     int(item["scenarioCount"]),
                                     int(item["deviceTemperatureCount"]),
                                     int(item["deviceStateCount"]),
                                     int(item["deviceLightCount"]),
                                     int(item["deviceDetectorCount"]))
                    self.myfox_info.sites.append(site)
                    _LOGGER.debug("site_id:" + str(site.siteId))
                    _LOGGER.debug("Nouveau site : %s", str(site))
                    # break
                self.infoSites_times = time.time()
            else :
                _LOGGER.debug("Sites en cache : %s", str(self.myfox_info.sites))

            return self.myfox_info.sites

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)

    async def getHistory(self, type: str = "security") -> list[Any]:
        """ Recuperation info site """
        try:
            if self.isCacheExpire(self.history_time) :
                # "dateFrom"  : "xxx",
                # "dateTo"    : "yyy",
                data = {
                    "dateOrder" : -1
                }
                if type is not None:
                    data["type"] = type
                response = await self.callMyFoxApiGet(MYFOX_HISTORY_GET % self.myfox_info.site.siteId, data)
                items = response["payload"]["items"]
                _LOGGER.debug("MyFoxApiClient.getHistory -> items %s", str(items))

                self.history = items
                self.history_time = time.time()
                for item in items :
                    # SiteEvent {
                    # logId (integer): The event identifier,
                    # label (string): The event label,
                    # type (string) = ['scenario' or 'homeAuto' or 'security' or 'config' or 'alarm' or 'access' or 'account' or 'diagnosis']: The event type,
                    # createdAt (string): The event date
                    # }
                    _LOGGER.debug(str(item))
                    break
            else :
                _LOGGER.debug("MyFoxApiClient.getHistory -> Cache ")

            return self.history

        except MyFoxException as exception:
            raise exception
        except Exception as exception:
            _LOGGER.error(exception)
            _LOGGER.error("Error : " + str(exception))
            raise MyFoxException(args=exception)
