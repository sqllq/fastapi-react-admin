from http import HTTPStatus
from fastapi import Depends
from typing import Callable, Coroutine

from .. dependencies import user_is_superuser
from .. entities import BaseRouter


class ReactReferenceRouter(BaseRouter):
    """
    React Reference Router
    """

    pass