from typing import Final

DEFAULT_MYFOX_URL_API: Final = "https://api.myfox.me/"

CONTENT_TYPE_JSON: Final = "application/json"
CONTENT_TYPE_HTML: Final = "text/html"

KEY_CLIENT_ID    : Final = "client_id"
KEY_CLIENT_SECRET: Final = "client_secret"
KEY_MYFOX_USER   : Final = "username"
KEY_MYFOX_PSWD   : Final = "password"
KEY_SITE_ID      : Final = "site_id"
KEY_TOKEN        : Final = "token"
KEY_ACCESS_TOKEN : Final = "access_token"
KEY_REFRESH_TOKEN: Final = "refresh_token"
KEY_EXPIRE_IN    : Final = "expires_in"
KEY_EXPIRE_AT    : Final = "expires_at"
KEY_EXPIRE_TIME  : Final = "expires_time"
KEY_GRANT_TYPE   : Final = "grant_type"
KEY_AUTH_IMPLEMENTATION   : Final = "auth_implementation"

KEY_POOLING_INTERVAL       : Final = "pool_interval_minutes"
KEY_CACHE_EXPIRE_IN        : Final = "cache_expires_in"
KEY_CACHE_CAMERA           : Final = "cache_camera"
KEY_CACHE_SECURITY         : Final = "cache_security"
KEY_USE_CODE_ALARM         : Final = "utilisation_code"
KEY_AUTHORIZED_CODE_ALARM  : Final = "autorisation_codes"
KEY_NB_RETRY_DEFAULT       : Final = "nb_retry_default"
KEY_NB_RETRY_CAMERA        : Final = "nb_retry_camera"
KEY_DELAY_BETWEEN_RETRY    : Final = "delay_between_retry"

GRANT_TYPE_PASSWORD           : Final = "password"
GRANT_TYPE_AUTHORIZATION_CODE : Final = "authorization_code"
GRANT_REFRESH_TOKEN           : Final = "refresh_token"

# SEUILS
POOLING_INTERVAL_DEF:int = 2 # 2 min
SEUIL_EXPIRE_MIN:int     = (5*60) # 5 min
CACHE_EXPIRE_IN:int      = (10*60) # 10 min
CACHE_CAMERA:int         = (5*60) # 5 min
CACHE_SECURITY:int       = (5*60) # 5 min

# token
MYFOX_TOKEN_PATH: Final = "oauth2/token"
MYFOX_AUTORIZE_PATH: Final = "oauth2/authorize"
# sites
MYFOX_INFO_SITE_PATH: Final = "v2/client/site/items" #List available sites for the current user
MYFOX_HISTORY_GET   : Final = "v2/site/%i/history" #Get site history
# scenarios
MYFOX_SCENARIO_ITEMS  : Final = "v2/site/%i/scenario/items"
MYFOX_SCENARIO_PLAY   : Final = "v2/site/%i/scenario/%i/play"
MYFOX_SCENARIO_ENABLE : Final = "v2/site/%i/scenario/%i/enable"
MYFOX_SCENARIO_DISABLE: Final = "v2/site/%i/scenario/%i/disable"
# security
MYFOX_SECURITY_GET: Final = "v2/site/%i/security"
MYFOX_SECURITY_SET: Final = "v2/site/%i/security/set/%s"
# camera
MYFOX_CAMERA_LIST         : Final = "v2/site/%i/device/camera/items" #List camera devices
MYFOX_CAMERA_LIVE_EXTEND  : Final = "v2/site/%i/device/%i/camera/live/extend" #Add 30 seconds to live streaming
MYFOX_CAMERA_LIVE_START   : Final = "v2/site/%i/device/%i/camera/live/start/%s" #Start live streaming from a camera (hls / rtmp  )
MYFOX_CAMERA_LIVE_STOP    : Final = "v2/site/%i/device/%i/camera/live/stop" #Stop live streaming from a camera
MYFOX_CAMERA_PREV_TAKE    : Final = "v2/site/%i/device/%i/camera/preview/take" #Get a volatile preview from a camera
MYFOX_CAMERA_REC_START    : Final = "v2/site/%i/device/%i/camera/recording/start" #Start recording from a camera
MYFOX_CAMERA_REC_STOP     : Final = "v2/site/%i/device/%i/camera/recording/stop" #Stop recording from a camera
MYFOX_CAMERA_SHUTTER_CLOSE: Final = "v2/site/%i/device/%i/camera/shutter/close" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SHUTTER_OPEN : Final = "v2/site/%i/device/%i/camera/shutter/open" #Open shutter for Myfox Security Camera
MYFOX_CAMERA_SNAP_TAKE    : Final = "v2/site/%i/device/%i/camera/snapshot/take" #Take a snapshot from a camera and save it in the library
# device data light
MYFOX_LIGHT_LIST   : Final = "v2/site/%i/device/data/light/items" #List all light sensor featured devices
MYFOX_LIGHT_HISTORY: Final = "v2/site/%i/device/%i/data/light" #Get light measures
# device data other
MYFOX_DEVICE_OTHER_LIST: Final = "v2/site/%i/device/data/other/items" # List all generic sensor featured devices
# device data state
MYFOX_DEVICE_STATE_LIST: Final = "v2/site/%i/device/data/state/items" #List devices with state data
MYFOX_DEVICE_STATE_GET : Final = "v2/site/%i/device/%i/data/state" #Get device state
# device data temperature
MYFOX_DEVICE_TEMPERATURE_LIST: Final = "v2/site/%i/device/data/temperature/items" #List all temperature sensor featured devices
MYFOX_DEVICE_TEMPERATURE_GET : Final = "v2/site/%i/device/%i/data/temperature" #Get temperature measures
# device gate 
MYFOX_DEVICE_GATE_LIST       : Final = "v2/site/%i/device/gate/items" #List gate devices
MYFOX_DEVICE_GATE_PERFORM_ONE: Final = "v2/site/%i/device/%i/gate/perform/one" #Perform action #1 post
MYFOX_DEVICE_GATE_PERFORM_TWO: Final = "v2/site/%i/device/%i/gate/perform/two" #Perform action #2 post
# device heater
MYFOX_DEVICE_HEATER_LIST            : Final = "v2/site/%i/device/heater/items" #List heater devices
MYFOX_DEVICE_HEATER_SET_ECO         : Final = "v2/site/%i/device/%i/heater/eco" #Set a heater to 'eco' mode post
MYFOX_DEVICE_HEATER_SET_FROST       : Final = "v2/site/%i/device/%i/heater/frost" #Set a heater to 'frost' mode post
MYFOX_DEVICE_HEATER_SET_ON          : Final = "v2/site/%i/device/%i/heater/on" #Set a heater to 'on' mode post
MYFOX_DEVICE_HEATER_SET_OFF         : Final = "v2/site/%i/device/%i/heater/off" #Set a heater to 'off' mode post
# device heater
MYFOX_DEVICE_HEATER_THERMO_LIST: Final = "v2/site/%i/device/heater/items/withthermostat" #List heater devices with virtuals thermostats
MYFOX_DEVICE_HEATER_THERMO_SET_AUTO : Final = "v2/site/%i/device/%i/heater/auto" #Set a thermostat to 'auto' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_AWAY : Final = "v2/site/%i/device/%i/heater/away" #Set a thermostat to 'away' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_BOOST: Final = "v2/site/%i/device/%i/heater/boost" #Set a thermostat to 'boost' mode post
MYFOX_DEVICE_HEATER_THERMO_SET_OFF  : Final = "v2/site/%i/device/%i/heater/thermostatoff" #Set a thermostat to 'off' mode post
# device module
MYFOX_DEVICE_MODULE_LIST       : Final = "v2/site/%i/device/module/items" #List module devices
MYFOX_DEVICE_MODULE_PERFORM_ONE: Final = "v2/site/%i/device/%i/module/perform/one" #Perform action #1 post
MYFOX_DEVICE_MODULE_PERFORM_TWO: Final = "v2/site/%i/device/%i/module/perform/two" #Perform action #2 post
# device shutter
MYFOX_DEVICE_SHUTTER_LIST : Final = "v2/site/%i/device/shutter/items" #List shutter devices
MYFOX_DEVICE_SHUTTER_MY   : Final = "v2/site/%i/device/%i/shutter/my" #Set shutter to favorite position post
MYFOX_DEVICE_SHUTTER_OPEN : Final = "v2/site/%i/device/%i/shutter/open" #Open shutter post
MYFOX_DEVICE_SHUTTER_CLOSE: Final = "v2/site/%i/device/%i/shutter/close" #Close shutter post
# device socket
MYFOX_DEVICE_SOCKET_LIST: Final = "v2/site/%i/device/socket/items" #List socket devices
MYFOX_DEVICE_SOCKET_ON  : Final = "v2/site/%i/device/%i/socket/on" #Turn on a device post
MYFOX_DEVICE_SOCKET_OFF : Final = "v2/site/%i/device/%i/socket/off" #Turn off a device post
# group electic
MYFOX_GROUP_ELECTRIC_LIST   : Final = "v2/site/%i/group/electric/items" #List groups of type electric
MYFOX_GROUP_ELECTRIC_SET_ON : Final = "v2/site/%i/group/%i/electric/on" #Turn on all electric devices from a group post
MYFOX_GROUP_ELECTRIC_SET_OFF: Final = "v2/site/%i/group/%i/electric/off" #Turn off all electric devices from a group post
# group shutter
MYFOX_GROUP_SHUTTER_LIST     : Final = "v2/site/%i/group/shutter/items" #List groups of type shutter
MYFOX_GROUP_SHUTTER_SET_CLOSE: Final = "v2/site/%i/group/%i/shutter/close" #Close all shutters from a group post
MYFOX_GROUP_SHUTTER_SET_OPEN : Final = "v2/site/%i/group/%i/shutter/open" #Open all shutters from a group post
# site library
MYFOX_LIBRARY_IMAGE_LIST: Final = "v2/site/%i/library/image/items" #Get all images taken from a site's cameras
MYFOX_LIBRARY_VIDEO_LIST: Final = "v2/site/%i/library/video/items" #Get all videos taken from a site's cameras
MYFOX_LIBRARY_VIDEO_PLAY: Final = "v2/site/%i/library/video/%i/play" #Get video informations for HLS playing
