from .env import *

try:
    from .settings_local import *
except ImportError:
    pass
