from sys import argv
from json import loads
from heliotrope.config import HeliotropeConfig
from heliotrope.server import create_app
from heliotrope.argparser import parse_args

heliotrope_config = HeliotropeConfig()

args = parse_args(argv[1:])

if args.config:
    with open(args.config, "r") as f:
        config = loads(f.read())
        heliotrope_config.update(config)
else:
    heliotrope_config.update_config(
        {
            "TESTING": args.test,
            "SENTRY_DSN": args.sentry_dsn,
            "GALLERYINFO_DB_URL": args.galleryinfo_db_url,
            "INFO_DB_URL": args.info_db_url,
            "INDEX_FILE": args.index_file,
            "MIRRORING_DELAY": args.mirroring_delay,
            "REFRESH_COMMON_JS_DELAY": args.refresh_delay,
        }
    )


create_app(heliotrope_config).run(args.host, args.port, workers=args.workers)
