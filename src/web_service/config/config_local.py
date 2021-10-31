from .config_base import ConfigBase


class ConfigLocal(ConfigBase):
    """Local stack configuration"""
    PGSQL_HOST: str = "database"
    PGSQL_USER: str = "letstalk"
    PGSQL_PASS: str = "KdfjiED8"
    PGSQL_PORT: int = 5432
    PGSQL_DATABASE: str = "letstalk"

    CORS_ORIGINS: list[str] = ["*"]
