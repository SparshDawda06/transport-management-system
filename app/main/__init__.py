from flask import Blueprint

bp = Blueprint("main", __name__)

from . import routes  # noqa: E402,F401

# register CLI commands
from ..cli import create_db as create_db_command  # noqa: E402

__all__ = ["bp", "create_db_command"]
