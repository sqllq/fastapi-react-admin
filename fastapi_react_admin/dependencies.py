from typing import Union
from http import HTTPStatus
from fastapi import Depends, HTTPException

from . config import (
    user_model,
    token_decoder,
    oauth2_scheme,
    permission_field,
)


async def user_is_superuser(token: str = Depends(oauth2_scheme)) -> user_model:
    """
    Superuser permission
    """
    id: Union[int, None] = token_decoder(token)
    if not id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Not authenticated.",
        )
    user = await user_model.get_or_none(id=id)
    has_permission_field: bool = hasattr(user, permission_field)
    if not has_permission_field:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Permission field does not exist.",
        )
    suits_permission = getattr(user, permission_field, False)
    if not suits_permission:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Permission denied.",
        )
    return user
