from copy import copy
from tortoise import Tortoise
from typing import Callable, Any
from tortoise.exceptions import IntegrityError


async def create_super_user() -> None:
    """
    Superuser creation
    """
    from .config import (
        hasher,
        user_model,
        orm_config,
        hasher_hash_method
    )

    config: dict[str, Any] = copy(orm_config)
    config.pop("generate_schemas", None)
    await Tortoise.init(**config)
    username: str = input("Username: ")
    email: str = input("Email: ")
    password: str = input("Password: ")
    repeat_password: str = input("Repeat password: ")
    if not password == repeat_password:
        raise ValueError("Passwords did not match.")
    if len(password) < 6:
        raise ValueError("Password's length less then 6 symbols.")
    is_active: bool = True
    is_superuser: bool = True
    hash: Callable = getattr(hasher(), hasher_hash_method)
    password: str = hash(password)
    try:
        await user_model.create(
            username=username,
            password=password,
            is_superuser=is_superuser,
            email=email,
            is_active=is_active
        )
        print("Superuser created successfully.")
    except IntegrityError:
        print("User with such data already exists.")


def compile_model_admin() -> None:
    """
    Models directory regeneration
    """
    from .config import admins

    print("WARNING: This will override existing models directory.")
    print("Are you sure you wish to continue? [Yes/No/Fingerprint].")

    result: str = input("Decision: ")

    if result.lower() not in ("yes", "y"):
        exit()

    if isinstance(admins, Callable):
        admins: list[object] = admins()

    for admin in admins:
        initialized: object = admin()
        initialized.compile()

    print("Models directory regenerated successfully.")


def compile_app_admin() -> None:
    """
    App.js regeneration
    """
    from .core import ReactAppAdmin
    from .config import admins

    print("WARNING: This will override existing App.js.")
    print("Are you sure you wish to continue? [Yes/No/Fingerprint].")

    result: str = input("Decision: ")

    if result.lower() not in ("yes", "y"):
        exit()

    initialized: list = list()

    if isinstance(admins, Callable):
        admins: list[object] = admins()

    for admin in admins:
        initialized.append(admin())

    app: ReactAppAdmin = ReactAppAdmin(initialized)
    app.compile()

    print("App.js regenerated successfully.")