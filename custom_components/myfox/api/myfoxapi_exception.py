
from typing import Optional


class MyFoxException(Exception):
    def __init__(self,
                 status: Optional[int] = None,
                 message: Optional[str] = "",
                 *args, **kwargs) -> None:
        if status is not None:
            self.status = status
        else:
            self.status = 999
        self.message = message
        super().__init__(args, kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.status} - {self.message}"

class InvalidTokenMyFoxException(MyFoxException) :
    """Client token expire or invalid """


class RetryMyFoxException(MyFoxException) :
    """ Exception to retry call """
    def __init__(
            self,
            status: Optional[int] = 632,
            message: str = "",
            *args, **kwargs) -> None:

        super().__init__(status, message, args, kwargs)
