from tortoise import Model
from fastapi import Depends
from http import HTTPStatus
from typing import Coroutine, Callable
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..entities import BaseRouter
from ..dependencies import user_is_superuser


class ReactListRouter(BaseRouter):
    """
    React List Router
    """

    def get_route(self) -> Callable:
        route: Callable = self.router.get(
            f"/{self.model.__name__.lower()}",
            status_code=HTTPStatus.OK,
            response_model=self.pydantic_queryset
        )
        return route

    def get_view(self) -> Coroutine:

        async def view(user=Depends(user_is_superuser)):
            data: list[Model] = await self.model.all()
            response: JSONResponse = JSONResponse(content=jsonable_encoder(data))
            response.headers["Content-Range"]: str = f"{self.model.__name__.lower()} {self.list_size}/{len(data)}"
            return response

        return view
