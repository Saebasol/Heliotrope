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
        help="The url of the mongodb (default: '')",
    )

    config.add_argument(
        "--index-files",
        nargs="+",
        default=["index-english.nozomi"],
        help="The index to use (default: ['index-english.nozomi'])",
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
        help="The delay between refresh ggjs (default: 86400)",
    )

    config.add_argument(
        "--integrity-partial-check-delay",
        type=int,
        default=86400,
        help="The delay between integrity check partial task (default: 86400)",
    )

    config.add_argument(
        "--integrity-check-all-delay",
        type=int,
        default=86400,
        help="The delay between integrity check all task (default: 86400)",
    )

    config.add_argument(
        "--forwarded-secret",
        type=str,
        default="",
        help="The secret to use for forwarded headers (default: '')",
    )
    config.add_argument(
        "--use-atlas-search",
        action="store_true",
        default=False,
        help="Use mongodb Atlas search (default: False)",
    )

    config.add_argument(
        "--mirroring-remote-concurrent-size",
        type=int,
        default=50,
        help="The number of concurrent requests to the remote server (default: 50)",
    )

    config.add_argument(
        "--mirroring-local-concurrent-size",
        type=int,
        default=25,
        help="The number of concurrent requests to the local database (default: 5)",
    )

    config.add_argument(
        "--integrity-check-range-size",
        type=int,
        default=100,
        help="The range size for integrity checks (default: 100)",
    )

    config.add_argument(
        "--config",
        type=str,
        default="",
        help="The path to the config file (default: '')",
    )

    return parser.parse_args(argv)
