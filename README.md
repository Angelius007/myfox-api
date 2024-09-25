# MyFox Integration pour Home Assistant
[![GitHub release](https://img.shields.io/github/release/Angelius007/myfox-api?include_prereleases=&sort=semver&color=blue)](https://github.com/Angelius007/myfox-api/releases/)
[![GH-code-size](https://img.shields.io/github/languages/code-size/Angelius007/myfox-api?color=red)](https://github.com/Angelius007/myfox-api)
[![issues - myfox-api](https://img.shields.io/github/issues/Angelius007/myfox-api)](https://github.com/Angelius007/myfox-api/issues)
[![GH-last-commit](https://img.shields.io/github/last-commit/Angelius007/myfox-api?style=flat-square)](https://github.com/Angelius007/myfox-api/commits/main)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![HACS validation](https://github.com/Angelius007/myfox-api/workflows/HACS%20validation/badge.svg)](https://github.com/Angelius007/myfox-api/actions?query=workflow:"HACS+validation")
[![Validate with hassfest](https://github.com/Angelius007/myfox-api/workflows/Validate%20with%20hassfest/badge.svg)](https://github.com/Angelius007/myfox-api/actions?query=workflow:"Validate+with+hassfest")

Implémentation Custom pour interfaçage avec les API MyFox (racheté par Somfy).

Récupère l'ensemble des items dispo via les API MyFox et ajoute les "appareils" et "entités" associées

## Installation
3 méthodes disponibles pour l'installation :
- Installation via HACS _(prochainement)_
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Angelius007&repository=myfox-api)
- Installation avec "Dépôts personnalisés / custom repository" via HACS :
   - Dépôt : https://github.com/Angelius007/myfox-api
   - Type : Integration
- Installation manuelle en téléchargeant la dernière archive :
   - [Télécharger la dernière archive](https://github.com/Angelius007/myfox-api/releases/latest)
   - Désarchivez le fichier
   - Copier le dossier "**myfox**" dans le répertoire "**custom_components**"

Une fois installé, ajouter via les intégrations -> MyFox.

Ou bien cliquez sur le lien [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=myfox)

## Endpoints implémentés / non implémentés :
<details><summary> Recherche des sites <i>(1 service sur 1, 1 entry)</i> </summary>
<p>

*Services*
- /client/site/items : listing des sites de l'utilisateur. Choix du site paramétrable dans HA

*Entry*
- Choix du site ID

</p></details>
<details><summary> Gestion des caméras <i>(8 services sur 10, camera:1, buttons:6)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/camera/items : listing des caméras
- /site/{siteId}/device/{cameraId}/camera/live/start/{protocol} : démarrage d'un live (protocol "hls" implémenté)
- /site/{siteId}/device/{cameraId}/camera/live/extend : pour ajouter 30 sec de live
- /site/{siteId}/device/{cameraId}/camera/live/stop : pour arrêter le live
- /site/{siteId}/device/{cameraId}/camera/preview/take: photo instantané (sert pour la vignette de la caméra)
- /site/{siteId}/device/{cameraId}/camera/recording/start : enregistre une vidéo de 2 min dans le cloud MyFox (nécessite abonnement. Encore dispo ?)
- /site/{siteId}/device/{cameraId}/camera/recording/stop : stop l'enregistrement de la vidéo dans le cloud
- /site/{siteId}/device/{cameraId}/camera/snapshot/take : photo instantané sauvegardé dans le cloud MyFox
- _(not implemented)_ /site/{siteId}/device/{cameraId}/camera/shutter/open : ouverture obturateur caméra (si dispo)
- _(not implemented)_ /site/{siteId}/device/{cameraId}/camera/shutter/close : fermeture obturateur caméra (si dispo)

*Camera*
- Image/Aperçu Caméra
- Stream (protocol *hls*)

*Buttons*
- Snapshot
- Rec Start
- Rec Stop
- Live Start
- Live Extend
- Live Stop

</p></details>
<details><summary> Gestion des capteurs de lumière <i>(1 service sur 2, sensors:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/data/light/items : listing des capteurs de lumières
- _(not implemented)_ /site/{siteId}/device/{deviceId}/data/light : historique des capteurs

*Sensors*
- Luminosité/light

</p></details>
<details><summary> Gestion des autres capteurs (incendie / panne congélateur / etc.) <i>(1 service sur 1, sensors:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/data/other/items : lising des autres capteurs (incendie / capteur panne congélateur / etc.)

*Sensors*
- Etat capteur

</p></details>
<details><summary> Gestion des appareils à état <i>(1 service sur 2, sensors:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/data/state/items : listing des appareils à état
- _(not implemented)_ /site/{siteId}/device/{deviceId}/data/state : récupère l'état d'un appareil

*Sensors*
- Etat capteur

</p></details>
<details><summary> Gestion des capteurs de température <i>(1 service sur 2, sensors:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/data/temperature/items : listing des capteurs de température
- _(not implemented)_ /site/{siteId}/device/{deviceId}/data/temperature : historique des capteurs

*Sensors*
- Temperature

</p></details>
<details><summary> Gestion des portails <i>(3 services sur 3, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/gate/items : listing des appareils
- /site/{siteId}/device/{deviceId}/gate/perform/one : action 1 de l'appareil
- /site/{siteId}/device/{deviceId}/gate/perform/two : action 2 de l'appareil

*Buttons*
- Bouton action 1
- Bouton action 2

</p></details>
<details><summary> Gestion des modules de chauffage <i>(6 services sur 10, sensors:1, selects:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/heater/items/withthermostat : listing des modules de chauffage avec thermostat
- /site/{siteId}/device/heater/items : listing des modules de chauffage
- _(not implemented)_ /site/{siteId}/device/{deviceId}/heater/auto : positionnement en mode auto du module de chauffage
- _(not implemented)_ /site/{siteId}/device/{deviceId}/heater/away : positionnement en mode absent du module de chauffage
- _(not implemented)_ /site/{siteId}/device/{deviceId}/heater/boost : positionnement en mode boost du module de chauffage
- /site/{siteId}/device/{deviceId}/heater/eco : positionnement en mode eco du module de chauffage
- /site/{siteId}/device/{deviceId}/heater/frost : positionnement en mode frost du module de chauffage
- /site/{siteId}/device/{deviceId}/heater/off : positionnement en mode off du module de chauffage
- /site/{siteId}/device/{deviceId}/heater/on : positionnement en mode confort du module de chauffage
- _(not implemented)_ /site/{siteId}/device/{deviceId}/heater/thermostatoff : positionnement en mode off du module de chauffage

*Sensors*
- Temperature (pour module radiateur avec thermostat)

*Selects*
- Selection programme (ON/OFF/Mode ECO/Mode Hors-Gel)
- Selection programme (ON/OFF/Mode ECO/Mode Hors-Gel) _(inactif:Mode Absent/Mode Auto/Mode Boost/Thermostat OFF)_

</p></details>
<details><summary> Gestion des autres modules <i>(3 services sur 3, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/module/items : listing des modules
- /site/{siteId}/device/{deviceId}/module/perform/one : action 1 de l'appareil
- /site/{siteId}/device/{deviceId}/module/perform/two : action 2 de l'appareil

*Buttons*
- Bouton action 1
- Bouton action 2

</p></details>
<details><summary> Gestion des volets <i>(3 services sur 4, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/shutter/items : listing des modules volets
- /site/{siteId}/device/{deviceId}/shutter/open : volet en position ouverte
- /site/{siteId}/device/{deviceId}/shutter/close : volet en position fermée
- _(not implemented)_ /site/{siteId}/device/{deviceId}/shutter/my : volet en position "favoris"

*Buttons*
- Ouverture volet
- Fermeture volet

</p></details>
<details><summary> Gestion des groupes de volets <i>(3 services sur 3, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/group/shutter/items : listing des groupes de volets
- /site/{siteId}/group/{groupId}/shutter/open : volets en position ouverte
- /site/{siteId}/group/{groupId}/shutter/close : volets en position fermée

*Buttons*
- Ouverture volet
- Fermeture volet

</p></details>
<details><summary> Gestion des prises <i>(3 services sur 3, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/device/socket/items : listing des prises connectées
- /site/{siteId}/device/{deviceId}/socket/on : position on
- /site/{siteId}/device/{deviceId}/socket/off : position off

*Buttons*
- Bouton ON
- Bouton OFF

</p></details>
<details><summary> Gestion des groupes de prises <i>(3 services sur 3, buttons:2)</i> </summary>
<p>

*Services*
- /site/{siteId}/group/electric/items : listing des groupements d'appreils électriques
- /site/{siteId}/group/{groupId}/electric/on : position on
- /site/{siteId}/group/{groupId}/electric/off : positionoff

*Buttons*
- Bouton ON
- Bouton OFF

</p></details>
<details><summary> Gestion des scénarios <i>(4 services sur 4, scenes:1, switches:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/scenario/items : listing des scénarios
- /site/{siteId}/scenario/{scenarioId}/play : déclenchement d'un scénario
- /site/{siteId}/scenario/{scenarioId}/enable : activation d'un scénario
- /site/{siteId}/scenario/{scenarioId}/disable : désactivation d'un scénario

*Scenes*
- Déclenchement scénario à la demande

*Switches*
- Activation/Désactivation scénario

</p></details>
<details><summary> Gestion de l'alarme <i>(2 services sur 2, selects:1)</i> </summary>
<p>

*Services*
- /site/{siteId}/security : récupération de l'état de l'alarme
- /site/{siteId}/security/set/{securityLevel} : changement du niveau de sécurité de l'alarme

*Selects*
- Changement niveau alarme (Disarmed/Partial/Armed)

</p></details>
<details><summary> Gestion de l'historique <i>(0 services sur 1)</i> </summary>
<p>

*Services*
- _(not implemented)_ /site/{siteId}/history : historique de la centrale

</p></details>
<details><summary> Gestion des médias <i>(0 services sur 3)</i> </summary>
<p>

*Services*
- _(not implemented)_ /site/{siteId}/library/image/items : listing des photos dans le cloud MyFox
- _(not implemented)_ /site/{siteId}/library/video/items : listing des vidéos dans le cloud MyFox
- _(not implemented)_ /site/{siteId}/library/video/{videoId}/play : lecture d'une viédo du cloud MyFox

</p></details>

## Configurations :

<details><summary>Fréquence de pooling (en minutes) / Pooling frequency (in minutes) </summary>
<p>
Fréquence d'appel des API via le coordinateur. Tous les services de récupération des appareils et de certains capteurs sont mis à jour via ce pooling.
</p></details>

<details><summary>Durée du cache (en secondees) / Cache duration (in seconds) </summary>
<p>
Durée du cache pour les listes d'appareils et capteurs. Si le pooling tente de récupérer des informations avant la fin de durée du cache, l'appel à l'API ne sera pas réalisé et la donnée en cache sera utilisée. (permet de limiter le nombre d'appels aux API MyFox)
</p></details>

<details><summary>Durée du cache de l'alarme (en secondes) / Security Cache duration (in seconds) </summary>
<p>
Durée du cache spécifique à l'alarme (pour récupérer l'état de l'armement)
</p></details>

<details><summary>Durée du cache de la camera (en secondes) / Camera Cache duration (in seconds) </summary>
<p>
Durée du cache spécifique à la caméra (pour récupérer un aperçu des caméras).
</p></details>

## Préconisations :
- Pour intégrer des couleurs dans les icônes, installer le plugin "custom-ui" via HACS pour changer la couleur des icônes

Après installation :
- Pour pouvoir mettre des couleurs sur les icônes
- installer Custom-ui : https://github.com/Mariusthvdb/custom-ui
- ajouter dans le configuration.yaml la ligne : 
        homeassistant: !include custom_components/myfox/customize.yaml

## Pour les développeurs

Pour les Tests :

Commencer par dupliquer le fichier "init_cache.txt" en le renommant en "cache.txt"
Puis remplissez les zones prévues :  
- "CLIENT_ID": "xxx" -> A recuperer sur api.myfox.me
- "CLIENT_SECRET": "xxx" -> A recuperer sur api.myfox.me
- "MYFOX_USER": "xxx" -> Email compte MyFox
- "MYFOX_PSWD": "xxx"  -> Pswd MyFox

## Autres informations

### Author 
Angelius007

### Sources
https://github.com/Angelius007/myfox-api

### API MyFox
API : https://api.myfox.me/

_Attention, MyFox a été racheté par Somfy depuis plusieurs années. Il n'y a plus de support ou de mise à jour des API MyFox_