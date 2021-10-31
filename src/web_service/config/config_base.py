from classutilities import ConfigClassMixin


class ConfigBase(ConfigClassMixin):
    """Base configuration options for all stacks"""
    PGSQL_HOST: str
    PGSQL_USER: str
    PGSQL_PASS: str
    PGSQL_PORT: int
    PGSQL_DATABASE: str

    CORS_ORIGINS: list[str]
