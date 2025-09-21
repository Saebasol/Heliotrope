from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from heliotrope.application.tasks.manager import TaskManager


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.add_task = MagicMock()
    app.purge_tasks = MagicMock()
    return app


@pytest.fixture
def task_manager(mock_app):
    return TaskManager(mock_app)


def test_task_manager_init(mock_app):
    manager = TaskManager(mock_app)
    assert manager.app == mock_app
    assert manager.registered_tasks == {}
    assert manager.task_errors == {}
    assert manager.max_retry_attempts == 5
    assert manager.base_retry_delay == 30


@patch("heliotrope.application.tasks.manager.logger")
def test_register_task(mock_logger, task_manager):
    mock_task_instance = MagicMock()
    mock_task_instance.get_name.return_value = "test_task"
    task_manager.app.add_task.return_value = mock_task_instance

    async def dummy_task():
        pass

    result = task_manager.register_task(dummy_task, "test_task")

    assert result == mock_task_instance
    assert "test_task" in task_manager.registered_tasks
    assert "test_task" in task_manager.task_errors
    mock_logger.debug.assert_called_with("Registering task: test_task")


def test_get_task_status_not_exists(task_manager):
    status = task_manager.get_task_status("nonexistent")
    assert status == {"exists": False}


def test_get_task_status_exists(task_manager):
    mock_task = MagicMock()
    mock_task.done.return_value = False
    mock_task.cancelled.return_value = False

    task_manager.registered_tasks["test_task"] = mock_task
    task_manager.task_errors["test_task"] = {
        "count": 2,
        "last_error": "Some error",
        "retry_delay": 60,
    }

    status = task_manager.get_task_status("test_task")

    assert status["exists"] is True
    assert status["done"] is False
    assert status["cancelled"] is False
    assert status["error_count"] == 2
    assert status["last_error"] == "Some error"
    assert status["next_retry_delay"] == 60


@patch("heliotrope.application.tasks.manager.logger")
def test_cancel_task_success(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.done.return_value = False
    task_manager.registered_tasks["test_task"] = mock_task

    result = task_manager.cancel_task("test_task")

    assert result is True
    mock_task.cancel.assert_called_once()
    mock_logger.info.assert_called_with("Task test_task cancelled")


def test_cancel_task_not_exists(task_manager):
    result = task_manager.cancel_task("nonexistent")
    assert result is False


def test_reset_task_error(task_manager):
    task_manager.task_errors["test_task"] = {
        "count": 3,
        "last_error": "Some error",
        "last_error_type": ValueError,
        "retry_delay": 90,
    }

    task_manager._reset_task_error("test_task")

    assert task_manager.task_errors["test_task"]["count"] == 0
    assert task_manager.task_errors["test_task"]["last_error"] is None
    assert task_manager.task_errors["test_task"]["last_error_type"] is None
    assert task_manager.task_errors["test_task"]["retry_delay"] == 0


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_completion_cancelled(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"
    mock_task.cancelled.return_value = True

    task_manager._handle_task_completion(mock_task, AsyncMock())

    mock_logger.warning.assert_called_with("test_task - Task was cancelled")


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_completion_calls_purge_tasks(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"
    mock_task.cancelled.return_value = False
    mock_task.exception.return_value = None

    task_manager.task_errors["test_task"] = {"count": 0}

    task_manager._handle_task_completion(mock_task, AsyncMock())

    task_manager.app.purge_tasks.assert_called_once()


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_completion_success(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"
    mock_task.cancelled.return_value = False
    mock_task.exception.return_value = None

    task_manager.task_errors["test_task"] = {"count": 1}

    task_manager._handle_task_completion(mock_task, AsyncMock())

    mock_logger.info.assert_called_with("test_task - Task completed successfully")
    assert task_manager.task_errors["test_task"]["count"] == 0


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_error_first_time(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"

    error = ValueError("Test error")
    task_manager.task_errors["test_task"] = {
        "count": 0,
        "last_error": None,
        "last_error_type": None,
        "retry_delay": 0,
    }

    with patch.object(task_manager, "_schedule_retry") as mock_schedule:
        task_manager._handle_task_error(mock_task, AsyncMock(), error)

    assert task_manager.task_errors["test_task"]["count"] == 1
    assert task_manager.task_errors["test_task"]["last_error"] == "Test error"
    assert task_manager.task_errors["test_task"]["last_error_type"] == ValueError
    mock_schedule.assert_called_once()


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_error_max_retries(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"

    error = ValueError("Test error")
    task_manager.registered_tasks["test_task"] = mock_task
    task_manager.task_errors["test_task"] = {
        "count": 4,
        "last_error": "Previous error",
        "last_error_type": ValueError,
        "retry_delay": 30,
    }

    task_manager._handle_task_error(mock_task, AsyncMock(), error)

    assert "test_task" not in task_manager.registered_tasks
    assert "test_task" not in task_manager.task_errors
    mock_logger.critical.assert_called_once()


def test_cancel_task_already_done(task_manager):
    mock_task = MagicMock()
    mock_task.done.return_value = True
    task_manager.registered_tasks["test_task"] = mock_task

    result = task_manager.cancel_task("test_task")
    assert result is False
    mock_task.cancel.assert_not_called()


@patch("heliotrope.application.tasks.manager.logger")
def test_handle_task_completion_with_error(mock_logger, task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"
    mock_task.cancelled.return_value = False
    mock_task.exception.return_value = ValueError("Some error")

    with patch.object(task_manager, "_handle_task_error") as mock_handle_error:
        task_manager._handle_task_completion(mock_task, AsyncMock())

    mock_handle_error.assert_called_once()


def test_handle_task_error_different_error_type(task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"

    task_manager.task_errors["test_task"] = {
        "count": 2,
        "last_error": "Previous error",
        "last_error_type": ValueError,
        "retry_delay": 60,
    }

    # 다른 타입의 에러 발생
    error = RuntimeError("Different error")

    with patch.object(task_manager, "_schedule_retry"):
        task_manager._handle_task_error(mock_task, AsyncMock(), error)

    # 카운트가 1로 리셋되고 retry_delay가 base_retry_delay로 변경되어야 함
    assert task_manager.task_errors["test_task"]["count"] == 1
    assert task_manager.task_errors["test_task"]["retry_delay"] == 30


def test_handle_task_error_same_error_type(task_manager):
    mock_task = MagicMock()
    mock_task.get_name.return_value = "test_task"

    task_manager.task_errors["test_task"] = {
        "count": 1,
        "last_error": "Previous error",
        "last_error_type": ValueError,
        "retry_delay": 30,
    }

    error = ValueError("Same type error")

    with patch.object(task_manager, "_schedule_retry"):
        task_manager._handle_task_error(mock_task, AsyncMock(), error)

    # 카운트 증가, retry_delay 증가
    assert task_manager.task_errors["test_task"]["count"] == 2
    assert task_manager.task_errors["test_task"]["retry_delay"] == 60


@pytest.mark.asyncio
@patch("heliotrope.application.tasks.manager.asyncio.sleep")
@patch("heliotrope.application.tasks.manager.logger")
async def test_schedule_retry(mock_logger, mock_sleep, task_manager):
    mock_task_func = AsyncMock()
    mock_new_task = MagicMock()
    task_manager.app.add_task.return_value = mock_new_task

    task_manager._schedule_retry("test_task", 30, mock_task_func)

    assert task_manager.app.add_task.call_count == 1
    call_args = task_manager.app.add_task.call_args
    assert call_args[1]["name"] == "test_task_retry_scheduler"

    delayed_retry_coro = call_args[0][0]
    await delayed_retry_coro

    mock_sleep.assert_called_once_with(30)
    mock_logger.info.assert_called_with("test_task - Retrying task now after 30s delay")
    assert task_manager.app.add_task.call_count == 2  # retry scheduler + actual retry


def test_reset_task_error_nonexistent_task(task_manager):
    task_manager._reset_task_error("nonexistent")
    assert "nonexistent" not in task_manager.task_errors
