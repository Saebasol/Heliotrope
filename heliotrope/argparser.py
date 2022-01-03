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
from argparse import ArgumentParser, Namespace


def parse_args(argv: list[str]) -> Namespace:
    parser = ArgumentParser("heliotrope")

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The hostname to listen on (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The port of the webserver (default: 8000)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="The number of worker processes to spawn (default: 1)",
    )

    parser.add_argument(
        "--access-log",
        action="store_false",
        default=True,
        help="Disable the access log (default: False)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="The debug mode to use (default: False)",
    )

    config = parser.add_argument_group("config")

    config.add_argument(
        "--production",
        action="store_true",
        default=False,
        help="Run the server in production mode (default: False)",
    )

    config.add_argument(
        "--sentry-dsn",
        type=str,
        default="",
        help="The Sentry DSN to use (default: '')",
    )

    config.add_argument(
        "--galleryinfo-db-url",
        type=str,
        default="",
        help="The url of the sql database (default: '')",
    )

    config.add_argument(
        "--info-db-url",
        type=str,
        default="",
        help="The url of the Meilisearch (default: '')",
    )

    config.add_argument(
        "--index-file",
        type=str,
        default="index-korean.nozomi",
        help="The index to use (default: index-korean.nozomi)",
    )

    config.add_argument(
        "--mirroring-delay",
        type=int,
        default=3600,
        help="The delay between mirroring task (default: 3600)",
    )

    config.add_argument(
        "--refresh-delay",
        type=int,
        default=86400,
        help="The delay between refresh commonjs (default: 86400)",
    )

    config.add_argument(
        "--supervisor-delay",
        type=int,
        default=30,
        help="The delay between supervisor task (default: 30)",
    )

    config.add_argument(
        "--forwarded-secret",
        type=str,
        default="",
        help="The secret to use for forwarded headers (default: '')",
    )

    config.add_argument(
        "--config",
        type=str,
        default="",
        help="The path to the config file (default: '')",
    )

    return parser.parse_args(argv)
