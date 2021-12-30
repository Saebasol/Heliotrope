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
        super().__init__(
            defaults=defaults,
            env_prefix=env_prefix,
            keep_alive=keep_alive,
            converters=converters,
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
                "FORWARDED_SECRET": "",
                "FALLBACK_ERROR_FORMAT": "json",
                # Sanic ext config
                "OAS_UI_DEFAULT": "swagger",
                "OAS_URI_REDOC": False,
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

    def update_with_args(self, args: Namespace) -> None:
        if args.config:
            with open(args.config, "r") as f:
                config = loads(f.read())
                self.update_config(config)
        else:
            self.update_config(
                {
                    "TESTING": args.test,
                    "FORWARDED_SECRET": args.forwarded_secret,
                    "SENTRY_DSN": args.sentry_dsn,
                    "GALLERYINFO_DB_URL": args.galleryinfo_db_url,
                    "INFO_DB_URL": args.info_db_url,
                    "INDEX_FILE": args.index_file,
                    "MIRRORING_DELAY": args.mirroring_delay,
                    "REFRESH_COMMON_JS_DELAY": args.refresh_delay,
                }
            )
        return None
