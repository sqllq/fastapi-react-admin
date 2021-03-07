"""
  ______        _              _   _____           _                 _           _
 |  ____|      | |            (_) |  __ \         | |       /\      | |         (_)
 | |__ __ _ ___| |_ __ _ _ __  _  | |__) |___  ___| |_     /  \   __| |_ __ ___  _ _ __
 |  __/ _` / __| __/ _` | '_ \| | |  _  // _ \/ __| __|   / /\ \ / _` | '_ ` _ \| | '_ \
 | | | (_| \__ \ || (_| | |_) | | | | \ \  __/ (__| |_   / ____ \ (_| | | | | | | | | | |
 |_|  \__,_|___/\__\__,_| .__/|_| |_|  \_\___|\___|\__| /_/    \_\__,_|_| |_| |_|_|_| |_|
                        | |
                        |_|
"""

from .config import router
from .auth import admin_login_view
from .core import ReactAppAdmin, ReactTortoiseModelAdmin
from .commands import create_super_user, compile_app_admin, compile_model_admin

__version__ = "0.0.1"
