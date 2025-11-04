from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from yggdrasil.application.tasks.refresh import RefreshggJS


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.ctx.pythonmonkey_resolved_image_repository.javascript_interpreter.refresh_gg_js = AsyncMock()
    return app


@pytest.fixture
def refresh_task(mock_app: MagicMock):
    return RefreshggJS(mock_app)


def test_refresh_gg_js_init(mock_app: MagicMock):
    refresh = RefreshggJS(mock_app)
    assert refresh.app == mock_app


@pytest.mark.asyncio
@patch("yggdrasil.application.tasks.refresh.sleep")
@patch("yggdrasil.application.tasks.refresh.logger")
async def test_start_task(
    mock_logger: MagicMock, mock_sleep: MagicMock, refresh_task: RefreshggJS
):
    call_count = 0

    async def side_effect(delay):
        nonlocal call_count
        call_count += 1
        if call_count >= 3:
            raise KeyboardInterrupt()

    mock_sleep.side_effect = side_effect

    delay = 5.0
    try:
        await refresh_task.start(delay)
    except KeyboardInterrupt:
        pass

    mock_logger.info.assert_called_once_with(
        f"Starting RefreshggJS task with delay: {delay}"
    )
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(delay)
    assert (
        refresh_task.app.ctx.pythonmonkey_resolved_image_repository.javascript_interpreter.refresh_gg_js.call_count
        == 2
    )
