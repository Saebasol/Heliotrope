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
                "MIRRORING_DELAY": 3600,
                "REFRESH_COMMON_JS_DELAY": 86400,
                # Sanic config
                "FALLBACK_ERROR_FORMAT": "json",
                # Sanic ext config
                "OAS_UI_DEFAULT": "swagger",
                "OAS_URI_TO_REDOC": False,
                # Open API config
                "API_TITLE": "Heliotrope",
                "API_VERSION": __version__,
                "API_DESCRIPTION": "Hitomi.la mirror api",
                "API_LICENSE_NAME": "MIT",
                "API_LICENSE_URL": "https://github.com/Saebasol/Heliotrope/blob/main/LICENSE",
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
