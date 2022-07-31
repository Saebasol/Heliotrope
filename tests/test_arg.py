from heliotrope.argparser import parse_args
from heliotrope.config import HeliotropeConfig


def test_parse_args():
    config = HeliotropeConfig()
    args = parse_args(
        [
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--workers",
            "1",
        ]
    )
    config.update_with_args(args)
    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.workers == 1


def test_parse_args_with_config():
    config = HeliotropeConfig()
    args = parse_args(
        [
            "--config",
            "tests/config.json",
        ]
    )
    config.update_with_args(args)

    assert (
        config.GALLERYINFO_DB_URL
        == "postgresql+asyncpg://postgres:test@localhost/test_heliotrope"
    )
    assert config.INFO_DB_URL == "mongodb://root:test@127.0.0.1"
    assert config.INDEX_FILE == "index-english.nozomi"
    assert config.MIRRORING_DELAY == 3600
    assert config.REFRESH_COMMON_JS_DELAY == 86400
