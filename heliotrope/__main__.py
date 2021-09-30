import argparse
from json import load

from heliotrope.server import heliotrope

parser = argparse.ArgumentParser("heliotrope")

parser.add_argument(
    "--host",
    "-H",
    type=str,
    default="0.0.0.0",
    help="The hostname to listen on (default: 0.0.0.0)",
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


config = parser.add_argument_group("Config")

config.add_argument(
    "--test",
    "-T",
    type=bool,
    default=False,
    help="Run the server in test mode (default: False)",
)

config.add_argument(
    "--index-file",
    "-I",
    type=str,
    default="index-korean.nozomi",
    help="The index to use (default: index-korean.nozomi)",
)

config.add_argument(
    "--delay",
    "-D",
    type=int,
    default=3600,
    help="The delay between mirroring task (default: 3600)",
)

config.add_argument(
    "--nosql",
    "-N",
    type=str,
    default=None,
    help="The mongodb connection string (default: mongodb://localhost:27017)",
)

config.add_argument(
    "--sql",
    "-S",
    type=str,
    default=None,
    help="The sql connection string (default: sqlite:///heliotrope.db)",
)

config.add_argument(
    "--config",
    "-C",
    type=str,
    default=None,
    help="The config file to use (default: None)",
)

args = parser.parse_args()

options = {
    "INDEX_FILE": args.index_file,
    "DELAY": args.delay,
    "MONGO_DB_URL": args.nosql,
    "DB_URL": args.sql,
    "TESTING": args.test,
}

if args.config:
    with open(args.config) as f:
        options.update(load(f))

heliotrope.update_config(options)

# NOTE: Will fixed
heliotrope.run(args.host, args.port, workers=args.workers)
