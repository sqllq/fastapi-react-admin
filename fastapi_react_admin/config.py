from typing import Callable
from fastapi import APIRouter
from importlib import import_module
from configparser import ConfigParser
from fastapi.security import OAuth2PasswordBearer


config = ConfigParser()
config.read("admin.ini")


ORM = config["admin"]["orm"]
USER_MODEL = config["admin"]["user_model"]
USER_MODULE = config["admin"]["user_module"]
LOGIN_ROUTE = config["admin"]["login_route"]
ADMIN_PREFIX = config["admin"]["admin_prefix"]
TOKEN_DECODE_MODULE = config["admin"]["token_decode_module"]
TOKEN_DECODE_OBJECT = config["admin"]["token_decode_object"]
PERMISSION_FIELD = config["admin"]["permission_field"]
BASE_DIR_MODULE = config["admin"]["base_dir_module"]
BASE_DIR_OBJECT = config["admin"]["base_dir_object"]
ORM_CONFIG_MODULE = config["admin"]["orm_config_module"]
ORM_CONFIG_OBJECT = config["admin"]["orm_config_object"]
CREATE_TOKEN_MODULE = config["admin"]["create_token_module"]
CREATE_TOKEN_OBJECT = config["admin"]["create_token_object"]
HASHER_MODULE = config["admin"]["hasher_module"]
HASHER_OBJECT = config["admin"]["hasher_object"]
HASHER_VERIFY_METHOD = config["admin"]["hasher_verify_method"]
HASHER_HASH_METHOD = config["admin"]["hasher_hash_method"]
DATA_PROVIDER = config["admin"]["data_provider"]
ADMINS_MODULE = config["admin"]["admins_module"]
ADMINS_OBJECT = config["admin"]["admins_object"]
SRC_OUTPUT_DIR = config["admin"]["src_output_dir"]
MODELS_OUTPUT_DIR = config["admin"]["models_output_dir"]
FRONTEND_ADMIN_PREFIX = config["admin"]["frontend_admin_prefix"]


try:
    user_model = getattr(import_module(USER_MODULE), USER_MODEL)
except ImportError:
    raise ValueError(
        "Wrong user's configuration in admin.ini file."
    )
if not user_model:
    raise ValueError(
        "Wrong user's configuration in admin.ini file."
    )


try:
    token_decoder = getattr(import_module(TOKEN_DECODE_MODULE), TOKEN_DECODE_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong decoder's configuration in admin.ini file."
    )
if not token_decoder:
    raise ValueError(
        "Wrong decoder's configuration in admin.ini file."
    )


try:
    base_dir = getattr(import_module(BASE_DIR_MODULE), BASE_DIR_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong base_dir's configuration in admin.ini file."
    )
if not base_dir:
    raise ValueError(
        "Wrong base_dir's configuration in admin.ini file."
    )


try:
    orm_config = getattr(import_module(ORM_CONFIG_MODULE), ORM_CONFIG_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong orm_config's configuration in admin.ini file."
    )
if not orm_config:
    raise ValueError(
        "Wrong orm_config's configuration in admin.ini file."
    )


try:
    token_creator = getattr(import_module(CREATE_TOKEN_MODULE), CREATE_TOKEN_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong create_token's configuration in admin.ini file."
    )
if not token_creator:
    raise ValueError(
        "Wrong create_token's configuration in admin.ini file."
    )


try:
    hasher = getattr(import_module(HASHER_MODULE), HASHER_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong hasher's configuration in admin.ini file."
    )
if not hasher:
    raise ValueError(
        "Wrong hasher's configuration in admin.ini file."
    )
if isinstance(hasher, Callable):
    if not hasattr(hasher(), HASHER_VERIFY_METHOD) or not hasattr(hasher(), HASHER_HASH_METHOD):
        raise ValueError(
            "Wrong hasher's configuration in admin.ini file."
        )
else:
    if not hasattr(hasher, HASHER_VERIFY_METHOD) or not hasattr(hasher, HASHER_HASH_METHOD):
        raise ValueError(
            "Wrong hasher's configuration in admin.ini file."
        )


try:
    admins = getattr(import_module(ADMINS_MODULE), ADMINS_OBJECT)
except ImportError:
    raise ValueError(
        "Wrong admin's configuration in admin.ini file."
    )
if not admins:
    raise ValueError(
        "Wrong admin's configuration in admin.ini file."
    )


prefix = ADMIN_PREFIX
data_provider = DATA_PROVIDER
src_output_dir = SRC_OUTPUT_DIR
permission_field = PERMISSION_FIELD
models_output_dir = MODELS_OUTPUT_DIR
hasher_hash_method = HASHER_HASH_METHOD
auth_route = ADMIN_PREFIX + LOGIN_ROUTE
hasher_verify_method = HASHER_VERIFY_METHOD
frontend_admin_prefix = FRONTEND_ADMIN_PREFIX
router = APIRouter(prefix=ADMIN_PREFIX, tags=["Admin"])
oauth2_scheme = OAuth2PasswordBearer(ADMIN_PREFIX + LOGIN_ROUTE)


__all__ = [
    router,
    hasher,
    prefix,
    base_dir,
    user_model,
    auth_route,
    orm_config,
    oauth2_scheme,
    data_provider,
    token_creator,
    token_decoder,
    src_output_dir,
    permission_field,
    models_output_dir,
    hasher_hash_method,
    hasher_verify_method,
    frontend_admin_prefix,
]
