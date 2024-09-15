from typing import Final

DOMAIN_MYFOX: Final = "myfox"
CONFIG_VERSION: int = 1

ONLINE_OPTIONS = {
    "Online": 0,
    "Offline": 1,
}

ALERTE_OPTIONS = {
    "OK": 0,
    "ALERTE": 1,
}

LIGHT_OPTIONS = {
    "Inconnu (0)": 0,
    "Pleine lumière": 1,
    "Lumière du jour": 2,
    "Inconnu (3)": 3,
    "Lumière basse": 4,
    "Pénombre": 5,
    "Obscurité": 6,
}

HEATER_OPTIONS = {
    "ON": "on",
    "OFF": "off",
    "Mode ECO": "eco",
    "Hors GEL": "frost",
}

SECURITY_OPTIONS = {
    "Disarmed": 1,
    "Partial": 2,
    "Armed": 4
}