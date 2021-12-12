from argparse import ArgumentParser

from heliotrope.config import HeliotropeConfig
from heliotrope.server import create_app

config = HeliotropeConfig()

parser = ArgumentParser("heliotrope")

parser.add_argument(
    "--host",
    "-H",
    type=str,
    default="127.0.0.1",
    help="The hostname to listen on (default: 127.0.0.1)",
)
parser.add_argument(
    "--port",
    "-P",
    type=int,
    default=8000,
    help="The port of the webserver (default: 8000)",
)

parser.add_argument(
    "--workers",
    "-W",
    type=int,
    default=1,
    help="The number of worker processes to spawn (default: 1)",
)


args = parser.parse_args()

create_app(config).run(args.host, args.port, workers=args.workers)
