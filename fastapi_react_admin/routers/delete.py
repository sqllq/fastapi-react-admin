from http import HTTPStatus
from fastapi import Depends
from typing import Coroutine, Callable

from .. entities import BaseRouter
from .. dependencies import user_is_superuser


class ReactDeleteRouter(BaseRouter):
    """
    React Delete Router
    """
    def get_route(self) -> Callable:
        route: Callable = self.router.delete(
            f"/{self.model.__name__.lower()}" + "/{id}",
            status_code=HTTPStatus.NO_CONTENT,
        )
        return route

    def get_view(self) -> Coroutine:

        async def view(id: int, user=Depends(user_is_superuser)):
            instance = await self.model.get_or_none(id=id)
            if instance:
                await instance.delete()

        return view
