def main() -> None:  # pragma: no cover
    # I've done all of my testing on this.
    from functools import partial
    from sys import argv

    from sanic import Sanic
    from sanic.worker.loader import AppLoader

    from heliotrope.infrastructure.argparser import parse_args
    from heliotrope.infrastructure.sanic.bootstrap import create_app
    from heliotrope.infrastructure.sanic.config import HeliotropeConfig

    heliotrope_config = HeliotropeConfig()

    args = parse_args(argv[1:])
    heliotrope_config.update_with_args(args)

    loader = AppLoader(factory=partial(create_app, heliotrope_config))
    app = (  # pyright: ignore[reportUnknownVariableType]
        loader.load()  # pyright: ignore[reportUnknownMemberType]
    )

    app.prepare(  # pyright: ignore[reportUnknownMemberType]
        heliotrope_config.HOST,
        heliotrope_config.PORT,
        debug=heliotrope_config.DEBUG,
        workers=heliotrope_config.WORKERS,
    )

    Sanic.serve(app, app_loader=loader)  # pyright: ignore[reportUnknownMemberType]


if __name__ == "__main__":  # pragma: no cover
    main()
