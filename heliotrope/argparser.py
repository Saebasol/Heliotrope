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

    config = parser.add_argument_group("config")

    config.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Run the server in test mode (default: False)",
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
        type=str,
        default=86400,
        help="The delay between refresh commonjs (default: 86400)",
    )

    config.add_argument(
        "--config",
        type=str,
        default="",
        help="The path to the config file (default: '')",
    )

    return parser.parse_args(argv)
