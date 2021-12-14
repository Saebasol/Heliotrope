from typing import Optional, Union

from sanic.config import SANIC_PREFIX, Config


class HeliotropeConfig(Config):
    def __init__(
        self,
        defaults: dict[str, Union[str, bool, int, float, None]] = None,  # type: ignore
        load_env: Optional[Union[bool, str]] = True,
        env_prefix: Optional[str] = SANIC_PREFIX,
        keep_alive: Optional[bool] = None,
    ):
        super().__init__(
            defaults=defaults,
            load_env=load_env,
            env_prefix=env_prefix,
            keep_alive=keep_alive,
        )
        # Defualt
        self.update(
            {
                "TESTING": False,
                "SENTRY_DSN": "",
                "GALLERYINFO_DB_URL": "",
                "INFO_DB_URL": "",
                "INFO_DB_API_KEY": "",
                "INDEX_FILE": "index-korean.nozomi",
                "FALLBACK_ERROR_FORMAT": "json",
                "MIRRORING_DELAY": 3600,
                "REFRESH_COMMON_JS_DELAY": 86400,
            }
        )

    TESTING: bool
    SENTRY_DSN: str
    GALLERYINFO_DB_URL: str
    INFO_DB_URL: str
    INFO_DB_API_KEY: str
    MIRRORING_DELAY: float
    REFRESH_COMMON_JS_DELAY: float
    INDEX_FILE: str
