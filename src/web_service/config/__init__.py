import os

from .config_base import ConfigBase
from .config_local import ConfigLocal

# Get the stack definition
stack: str = os.getenv("ENVIRONMENT", "local")

# Select correct configuration
CONFIG: type[ConfigBase] = ConfigLocal

if stack == "local":
    CONFIG: type[ConfigBase] = ConfigLocal
# other options here (typically 'production')
else:
    raise RuntimeError("Wrong stack name")
