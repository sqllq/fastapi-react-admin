from http import HTTPStatus
from fastapi import Depends
from typing import Coroutine, Callable

from ..entities import BaseRouter
from ..dependencies import user_is_superuser


class ReactRetrieveRouter(BaseRouter):
    """
    React Retrieve Router
    """

    def get_route(self) -> Callable:
        route: Callable = self.router.get(
            f"/{self.model.__name__.lower()}" + "/{id}",
            status_code=HTTPStatus.OK,
            response_model=self.pydantic_single
        )
        return route

    def get_view(self) -> Coroutine:

        async def view(id: int, user=Depends(user_is_superuser)):
            return await self.model.get_or_none(id=id)

        return view
