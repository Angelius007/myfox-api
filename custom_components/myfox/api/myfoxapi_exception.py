
from typing import Optional

class MyFoxException(Exception):
    def __init__(
        self,
        status: Optional[int] = None,
        message: str = "") -> None:

        if status is not None:
            self.status = status
        else:
            self.status = 0
        self.message = message

class InvalidTokenMyFoxException(MyFoxException) :
    """Client token expire or invalid """