from http import HTTPStatus
from fastapi import Depends
from typing import Coroutine, Callable

from .. entities import BaseRouter
from .. dependencies import user_is_superuser


class ReactCreateRouter(BaseRouter):
    """
    React Create Router
    """

    def get_route(self) -> Callable:
        route: Callable = self.router.post(
            f"/{self.model.__name__.lower()}",
            status_code=HTTPStatus.CREATED,
            response_model=self.pydantic_single
        )
        return route

    def get_view(self) -> Coroutine:
        model = self.pydantic_single

        async def view(payload: model, user=Depends(user_is_superuser)):
            return await self.model.create(**payload.dict())

        return view


