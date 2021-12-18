# pragma: no cover
# I've done all of my testing on this.
from sys import argv

from heliotrope.argparser import parse_args
from heliotrope.config import HeliotropeConfig
from heliotrope.server import create_app


def main() -> None:
    heliotrope_config = HeliotropeConfig()

    args = parse_args(argv[1:])

    heliotrope_config.update_with_args(args)

    create_app(heliotrope_config).run(args.host, args.port, workers=args.workers)


if __name__ == "__main__":
    main()
