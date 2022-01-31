"""
MIT License

Copyright (c) 2021 SaidBySolo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from argparse import Namespace
from json import loads
from typing import Any, Callable, Optional, Sequence, Union

from sanic.config import SANIC_PREFIX, Config

from heliotrope import __version__


class HeliotropeConfig(Config):
    def __init__(
        self,
        defaults: dict[str, Union[str, bool, int, float, None]] = {},
        env_prefix: Optional[str] = SANIC_PREFIX,
        keep_alive: Optional[bool] = None,
        *,
        converters: Optional[Sequence[Callable[[str], Any]]] = None
    ):
        # Defualt
        self.update(
            {
                # heliotrope
                "CONFIG": "",
                "PRODUCTION": False,
                "USE_ENV": False,
                "SENTRY_DSN": "",
                "GALLERYINFO_DB_URL": "",
                "INFO_DB_URL": "",
                "INDEX_FILE": "index-korean.nozomi",
                "MIRRORING_DELAY": 3600,
                "REFRESH_COMMON_JS_DELAY": 86400,
                "SUPERVISOR_DELAY": 30,
                "USE_ATLAS_SEARCH": False,
                # Sanic config
                "HOST": "127.0.0.1",
                "PORT": 8000,
                "WORKERS": 1,
                "DEBUG": False,
                "ACCESS_LOG": False,
                "FORWARDED_SECRET": "",
                "FALLBACK_ERROR_FORMAT": "json",
                # Sanic ext config
                "OAS_UI_DEFAULT": "swagger",
                "OAS_URI_REDOC": False,
                # Open API config
                "SWAGGER_UI_CONFIGURATION": {
                    "apisSorter": "alpha",
                    "operationsSorter": "alpha",
                },
                "API_TITLE": "Heliotrope",
                "API_VERSION": __version__,
                "API_DESCRIPTION": "Hitomi.la mirror api",
                "API_LICENSE_NAME": "MIT",
                "API_LICENSE_URL": "https://github.com/Saebasol/Heliotrope/blob/main/LICENSE",
            }
        )

        super().__init__(
            defaults=defaults,
            env_prefix=env_prefix,
            keep_alive=keep_alive,
            converters=converters,
        )

    # Heliotrope
    USE_ENV: bool
    CONFIG: str
    PRODUCTION: bool
    SENTRY_DSN: str
    GALLERYINFO_DB_URL: str
    INFO_DB_URL: str
    MIRRORING_DELAY: float
    REFRESH_COMMON_JS_DELAY: float
    SUPERVISOR_DELAY: float
    INDEX_FILE: str
    USE_ATLAS_SEARCH: bool
    # Sanic config
    DEBUG: bool
    HOST: str
    PORT: int
    WORKERS: int

    def load_config_with_config_json(self, path: str) -> None:
        with open(path, "r") as f:
            config = loads(f.read())
            self.update_config(config)
        return None

    def update_with_args(self, args: Namespace) -> None:
        if not self.USE_ENV:
            self.update_config({k.upper(): v for k, v in vars(args).items()})
        if self.CONFIG:
            self.load_config_with_config_json(self.CONFIG)
        return None
