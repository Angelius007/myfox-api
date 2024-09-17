## MyFox
### Author : Angelius007

API : https://api.myfox.me/

Implémentation Custom pour interfaçage avec les API MyFox (racheté par Somfy).

Récupère l'ensemble des items dispo via les API MyFox et crée les "appareils" et "entités" associées

Endpoints implémentés / non implémentés :
- /client/site/items : listing des sites de l'utilisateur. Choix du site paramétrable dans HA
- /site/{siteId}/device/camera/items : listing des caméras
    - /site/{siteId}/device/{cameraId}/camera/live/start/{protocol} : démarrage d'un live (protocol "hls" implémenté)
    - /site/{siteId}/device/{cameraId}/camera/live/extend : pour ajouter 30 sec de live
    - /site/{siteId}/device/{cameraId}/camera/live/stop : pour arrêter le live
    - /site/{siteId}/device/{cameraId}/camera/preview/take: photo instantané (sert pour la vignette de la caméra)
    - /site/{siteId}/device/{cameraId}/camera/recording/start : enregistre une vidéo de 2 min dans le cloud MyFox (nécessite abonnement. Encore dispo ?)
    - /site/{siteId}/device/{cameraId}/camera/recording/stop : stop l'enregistrement de la vidéo dans le cloud
    - /site/{siteId}/device/{cameraId}/camera/snapshot/take : photo instantané sauvegardé dans le cloud MyFox
    - (not implemented) /site/{siteId}/device/{cameraId}/camera/shutter/open : ouverture obturateur caméra (si dispo)
    - (not implemented) /site/{siteId}/device/{cameraId}/camera/shutter/close : fermeture obturateur caméra (si dispo)
- /site/{siteId}/device/data/light/items : listing des capteurs de lumières
    - (not implemented) /site/{siteId}/device/{deviceId}/data/light : historique des capteurs
- /site/{siteId}/device/data/other/items : lising des autres capteurs (incendie / capteur panne congélateur / etc.)
- /site/{siteId}/device/data/state/items : listing des appareils à état
    - (not implemented) /site/{siteId}/device/{deviceId}/data/state : récupère l'état d'un appareil
- /site/{siteId}/device/data/temperature/items : listing des capteurs de température
    - (not implemented) /site/{siteId}/device/{deviceId}/data/temperature : historique des capteurs
- /site/{siteId}/device/gate/items : listing des appareils
    - /site/{siteId}/device/{deviceId}/gate/perform/one : action 1 de l'appareil
    - /site/{siteId}/device/{deviceId}/gate/perform/two : action 2 de l'appareil
- /site/{siteId}/device/heater/items/withthermostat : listing des modules de chauffage avec thermostat
- /site/{siteId}/device/heater/items : listing des modules de chauffage
    - (not implemented) /site/{siteId}/device/{deviceId}/heater/auto : positionnement en mode auto du module de chauffage
    - (not implemented) /site/{siteId}/device/{deviceId}/heater/away : positionnement en mode absent du module de chauffage
    - (not implemented) /site/{siteId}/device/{deviceId}/heater/boost : positionnement en mode boost du module de chauffage
    - /site/{siteId}/device/{deviceId}/heater/eco : positionnement en mode eco du module de chauffage
    - /site/{siteId}/device/{deviceId}/heater/frost : positionnement en mode frost du module de chauffage
    - /site/{siteId}/device/{deviceId}/heater/off : positionnement en mode off du module de chauffage
    - /site/{siteId}/device/{deviceId}/heater/on : positionnement en mode confort du module de chauffage
    - (not implemented) /site/{siteId}/device/{deviceId}/heater/thermostatoff : positionnement en mode off du module de chauffage
- /site/{siteId}/device/module/items : listing des modules
    - /site/{siteId}/device/{deviceId}/module/perform/one : action 1 de l'appareil
    - /site/{siteId}/device/{deviceId}/module/perform/two : action 2 de l'appareil
- /site/{siteId}/device/shutter/items : listing des modules volets
    - /site/{siteId}/device/{deviceId}/shutter/open : volet en position ouverte
    - /site/{siteId}/device/{deviceId}/shutter/close : volet en position fermée
    - (not implemented) /site/{siteId}/device/{deviceId}/shutter/my : volet en position "favoris"
- /site/{siteId}/device/socket/items : listing des prises connectées
    - /site/{siteId}/device/{deviceId}/socket/on : position on
    - /site/{siteId}/device/{deviceId}/socket/off : position off
- /site/{siteId}/group/electric/items : listing des groupements d'appreils électriques
    - /site/{siteId}/group/{groupId}/electric/on : position on
    - /site/{siteId}/group/{groupId}/electric/off : positionoff
- /site/{siteId}/group/shutter/items : listing des groupes de volets
    - /site/{siteId}/group/{groupId}/shutter/open : volets en position ouverte
    - /site/{siteId}/group/{groupId}/shutter/close : volets en position fermée
- (not implemented) /site/{siteId}/history : historique de la centrale
- (not implemented) /site/{siteId}/library/image/items : listing des photos dans le cloud MyFox
- (not implemented) /site/{siteId}/library/video/items : listing des vidéos dans le cloud MyFox
    - (not implemented) /site/{siteId}/library/video/{videoId}/play : lecture d'une viédo du cloud MyFox
- /site/{siteId}/scenario/items : listing des scénarios
    - /site/{siteId}/scenario/{scenarioId}/play : déclenchement d'un scénario
    - /site/{siteId}/scenario/{scenarioId}/enable : activation d'un scénario
    - /site/{siteId}/scenario/{scenarioId}/disable : désactivation d'un scénario
- /site/{siteId}/security : récupération de l'état de l'alarme
    - /site/{siteId}/security/set/{securityLevel} : changement du niveau de sécurité de l'alarme


Préconisations :
- Installer le plugin "custom-ui" via HACS pour changer la couleur des icônes

Après installation :
- Pour pouvoir mettre des couleurs sur les icônes
    - installer Custom-ui : https://github.com/Mariusthvdb/custom-ui
    - ajouter dans le configuration.yaml la ligne : 
        homeassistant: !include custom_components/myfox/customize.yaml



Pour les Tests :

- Commencer par remplir le fichier "init_cache.txt"
    - "CLIENT_ID": "xxx" -> A recuperer sur api.myfox.me
    - "CLIENT_SECRET": "xxx" -> A recuperer sur api.myfox.me
    - "MYFOX_USER": "xxx" -> Email compte MyFox
    - "MYFOX_PSWD": "xxx"  -> Pswd MyFox
