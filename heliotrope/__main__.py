def main() -> None:  # pragma: no cover
    # I've done all of my testing on this.
    from functools import partial
    from sys import argv

    from sanic import Sanic
    from sanic.worker.loader import AppLoader

    from heliotrope.application.server import create_app
    from heliotrope.application.config import HeliotropeConfig
    from heliotrope.application.argparser import parse_args

    heliotrope_config = HeliotropeConfig()

    args = parse_args(argv[1:])
    heliotrope_config.update_with_args(args)

    loader = AppLoader(factory=partial(create_app, heliotrope_config))
    app = loader.load()

    app.prepare(
        heliotrope_config.HOST,
        heliotrope_config.PORT,
        debug=heliotrope_config.DEBUG,
        workers=heliotrope_config.WORKERS,
    )
    Sanic.serve(app, app_loader=loader)


if __name__ == "__main__":  # pragma: no cover
    main()
