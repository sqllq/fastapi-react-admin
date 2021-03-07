from http import HTTPStatus
from fastapi import Depends
from pydantic import BaseModel
from typing import Coroutine, Callable

from ..entities import BaseRouter
from ..dependencies import user_is_superuser


class ReactUpdateRouter(BaseRouter):
    """
    React Update Router
    """

    def get_route(self) -> Callable:
        route: Callable = self.router.put(
            f"/{self.model.__name__.lower()}" + "/{id}",
            status_code=HTTPStatus.OK,
            response_model=self.pydantic_single
        )
        return route

    def get_view(self) -> Coroutine:
        model: BaseModel = self.pydantic_single

        async def view(id: int, payload: model, user=Depends(user_is_superuser)):
            instance = await self.model.get_or_none(id=id)
            if instance:
                for field, value in payload.dict().items():
                    setattr(instance, field, value)
                await instance.save()
            return instance

        return view
