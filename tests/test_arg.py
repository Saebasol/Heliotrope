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
            "--test",
            "--sentry-dsn",
            "",
            "--galleryinfo-db-url",
            "",
            "--info-db-url",
            "",
            "--index-file",
            "index-korean.nozomi",
            "--mirroring-delay",
            "0",
            "--refresh-delay",
            "0",
            "--forwarded-secret",
            "",
        ]
    )
    config.update_with_args(args)
    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.workers == 1
    assert args.test == config.TESTING
    assert args.sentry_dsn == config.SENTRY_DSN
    assert args.galleryinfo_db_url == config.GALLERYINFO_DB_URL
    assert args.info_db_url == config.INFO_DB_URL
    assert args.index_file == config.INDEX_FILE
    assert args.mirroring_delay == config.MIRRORING_DELAY
    assert args.refresh_delay == config.REFRESH_COMMON_JS_DELAY
    assert args.forwarded_secret == config.FORWARDED_SECRET


def test_parse_args_with_config():
    config = HeliotropeConfig()
    args = parse_args(
        [
            "--config",
            "tests/config.json",
        ]
    )
    config.update_with_args(args)

    assert config.TESTING == True
    assert (
        config.GALLERYINFO_DB_URL
        == "postgresql+asyncpg://postgres:test@localhost/test_heliotrope"
    )
    assert config.INFO_DB_URL == "http://127.0.0.1:7700"
    assert config.INDEX_FILE == "index-korean.nozomi"
    assert config.MIRRORING_DELAY == 3600
    assert config.REFRESH_COMMON_JS_DELAY == 86400
