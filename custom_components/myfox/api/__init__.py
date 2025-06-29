""" Gestion API """

from dataclasses import dataclass, field
from ..devices.site import MyFoxSite
from homeassistant.const import (
    Platform,
)


@dataclass
class MyFoxEntryData:
    platforms: list[Platform]


@dataclass
class MyFoxOptionsDataApi:
    cache_time: int = 600
    pooling_frequency: int = 2
    cache_camera_time: int = 300
    cache_security_time: int = 300
    nb_retry_default: int = 5
    nb_retry_camera: int = 2
    delay_between_retry: int = 30
    use_code_alarm: bool = False
    secure_codes: str = False


@dataclass
class MyFoxEntryDataApi:
    client_id: str = None
    client_secret: str = None
    username: str = None
    password: str = None
    access_token: str = None
    refresh_token: str = None
    expires_in: int = 0
    expires_time: float = 0.0
    site: MyFoxSite = None
    sites: list[MyFoxSite] = field(default_factory=list[MyFoxSite(0)])
    options: MyFoxOptionsDataApi = None
