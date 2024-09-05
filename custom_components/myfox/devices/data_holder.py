import logging
from datetime import datetime
from typing import Any, List, TypeVar

import jsonpath_ng.ext as jp
from homeassistant.util import utcnow
from reactivex import Subject, Observable

_LOGGER = logging.getLogger(__name__)

_T = TypeVar("_T")
class BoundFifoList(List):

    def __init__(self, maxlen=20) -> None:
        super().__init__()
        self.maxlen = maxlen

    def append(self, __object: _T) -> None:
        super().insert(0, __object)
        while len(self) >= self.maxlen:
            self.pop()



class MyFoxDataHolder:

    def __init__(self, update_period_sec: int, collect_raw: bool = False):
        self.update_period_sec = update_period_sec
        self.__collect_raw = collect_raw

        self.params = dict[str, Any]()

        self.raw_data = BoundFifoList[dict[str, Any]]()

        self.__params_time = utcnow().replace(year=2000, month=1, day=1, hour=0, minute=0, second=0)
        self.__params_broadcast_time = utcnow().replace(year=2000, month=1, day=1, hour=0, minute=0, second=0)
        self.__params_observable = Subject[dict[str, Any]]()

        self.__set_reply_observable = Subject[list[dict[str, Any]]]()
        self.__get_reply_observable = Subject[list[dict[str, Any]]]()

    def params_observable(self) -> Observable[dict[str, Any]]:
        return self.__params_observable

    def get_reply_observable(self) -> Observable[list[dict[str, Any]]]:
        return self.__get_reply_observable

    def set_reply_observable(self) -> Observable[list[dict[str, Any]]]:
        return self.__set_reply_observable


    def update_to_target_state(self, target_state: dict[str, Any]):
        # key can be xpath!
        for key, value in target_state.items():
            expr = jp.parse("'"+key+"'")
            expr.update(self.params, value)

        self.__broadcast()

    def update_data(self, raw: dict[str, Any]):
        self.__add_raw_data(raw)
        self.__params_time = utcnow()

        try:
            if "timestamp" in raw:
                self.params['timestamp'] = raw['timestamp']
            elif "time" in raw:
                self.params['timestamp'] = raw['time']

            self.params.update(raw['params'])

            if (utcnow() - self.__params_broadcast_time).total_seconds() > self.update_period_sec:
                self.__broadcast()

        except Exception as error:
            _LOGGER.error("Error updating data", error)

    def __broadcast(self):
        self.__params_broadcast_time = utcnow()
        self.__params_observable.on_next(self.params)

    def __add_raw_data(self, raw: dict[str, Any]):
        if self.__collect_raw:
            self.raw_data.append(raw)

    def params_time(self) -> datetime:
        return self.__params_time
