from http import HTTPStatus
from typing import Callable
from fastapi import HTTPException
from pydantic import BaseModel

from . config import (
    router,
    hasher,
    user_model,
    token_creator,
    permission_field,
    hasher_verify_method,
)


class AuthModel(BaseModel):
    """
    Auth model
    """
    username: str
    password: str


@router.post("/login", status_code=HTTPStatus.OK)
async def admin_login_view(payload: AuthModel):
    """
    Admin login endpoint
    """
    verify: Callable = getattr(hasher(), hasher_verify_method)
    user = await user_model.get_or_none(username=payload.username)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify(payload.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not getattr(user, permission_field, False):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = token_creator(user.id)
    return token