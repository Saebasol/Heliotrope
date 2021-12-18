from heliotrope.argparser import parse_args


def test_parse_args():
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
        ]
    )
    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.workers == 1
    assert args.test == True
    assert args.sentry_dsn == ""
    assert args.galleryinfo_db_url == ""
    assert args.info_db_url == ""
    assert args.index_file == "index-korean.nozomi"
    assert args.mirroring_delay == 0
    assert args.refresh_delay == 0


def test_parse_args_with_config():
    args = parse_args(
        [
            "--config",
            "tests/test_arg.json",
        ]
    )

    assert args.config == "tests/test_arg.json"
