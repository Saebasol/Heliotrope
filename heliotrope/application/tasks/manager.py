import asyncio
import traceback
from asyncio import Task
from typing import Any, Callable, Coroutine, NoReturn

from sanic.log import logger

from heliotrope.infrastructure.sanic.app import Heliotrope


class TaskManager:
    def __init__(self, app: Heliotrope) -> None:
        self.app = app
        self.registered_tasks: dict[str, Task[NoReturn]] = {}
        self.task_errors: dict[str, dict[str, Any]] = {}
        self.max_retry_attempts = 5
        self.base_retry_delay = 30

    def register_task(
        self,
        task: Callable[..., Coroutine[Any, Any, None]],
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> Task[NoReturn]:
        logger.debug(f"Registering task: {name}")

        self.task_errors[name] = {
            "count": 0,
            "last_error": None,
            "last_error_type": None,
            "retry_delay": 0,
        }

        task_instance = self.app.add_task(
            task(*args, **kwargs),
            name=name,
        )
        assert task_instance
        self.registered_tasks[name] = task_instance

        task_instance.add_done_callback(
            lambda t: self._handle_task_completion(t, task, *args, **kwargs)
        )

        return task_instance

    def _handle_task_completion(
        self,
        completed_task: Task[NoReturn],
        task_func: Callable[..., Coroutine[Any, Any, None]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        task_name = completed_task.get_name()
        logger.debug(f"Task completed: {task_name}")

        if completed_task.cancelled():
            logger.warning(f"{task_name} - Task was cancelled")
            self._reset_task_error(task_name)
            return

        error = completed_task.exception()
        if error:
            self._handle_task_error(completed_task, task_func, error, *args, **kwargs)
        else:
            logger.info(f"{task_name} - Task completed successfully")
            self._reset_task_error(task_name)

        self.app.purge_tasks()

    def _handle_task_error(
        self,
        failed_task: Task[NoReturn],
        task_func: Callable[..., Coroutine[Any, Any, None]],
        error: BaseException,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        task_name = failed_task.get_name()
        error_info = self.task_errors.get(
            task_name,
            {"count": 0, "last_error": None, "last_error_type": None, "retry_delay": 0},
        )
        current_error_type = type(error)

        if error_info["last_error_type"] == current_error_type:
            error_info["count"] += 1
        else:
            error_info["count"] = 1
            error_info["retry_delay"] = self.base_retry_delay

        error_info["last_error"] = str(error)
        error_info["last_error_type"] = current_error_type

        logger.error(f"{task_name} - Error #{error_info['count']}: {str(error)}")
        logger.error(f"{task_name} - Traceback: {traceback.format_exc()}")

        if error_info["count"] >= self.max_retry_attempts:
            logger.critical(
                f"{task_name} - Task failed {error_info['count']} times with same error type. "
                f"Disabling task permanently. Last error: {error_info['last_error']}"
            )
            self.registered_tasks.pop(task_name, None)
            self.task_errors.pop(task_name, None)
            return

        retry_delay = error_info["retry_delay"] or self.base_retry_delay
        error_info["retry_delay"] = retry_delay + self.base_retry_delay

        self.task_errors[task_name] = error_info

        logger.info(
            f"{task_name} - Will retry after {retry_delay} seconds (attempt #{error_info['count']})"
        )
        self._schedule_retry(task_name, retry_delay, task_func, *args, **kwargs)

    def _schedule_retry(
        self,
        task_name: str,
        delay: int,
        task_func: Callable[..., Coroutine[Any, Any, None]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        async def delayed_retry() -> None:
            await asyncio.sleep(delay)
            logger.info(f"{task_name} - Retrying task now after {delay}s delay")

            new_task = self.app.add_task(
                task_func(*args, **kwargs),
                name=task_name,
            )
            assert new_task
            self.registered_tasks[task_name] = new_task

            new_task.add_done_callback(
                lambda t: self._handle_task_completion(t, task_func, *args, **kwargs)
            )

        self.app.add_task(delayed_retry(), name=f"{task_name}_retry_scheduler")

    def _reset_task_error(self, task_name: str) -> None:
        if task_name in self.task_errors:
            self.task_errors[task_name] = {
                "count": 0,
                "last_error": None,
                "last_error_type": None,
                "retry_delay": 0,
            }

    def cancel_task(self, name: str) -> bool:
        if name in self.registered_tasks:
            task = self.registered_tasks[name]
            if not task.done():
                task.cancel()
                logger.info(f"Task {name} cancelled")
                return True
        return False

    def get_task_status(self, name: str) -> dict[str, Any]:
        if name not in self.registered_tasks:
            return {"exists": False}

        task = self.registered_tasks[name]
        error_info = self.task_errors.get(name, {})

        return {
            "exists": True,
            "done": task.done(),
            "cancelled": task.cancelled(),
            "error_count": error_info.get("count", 0),
            "last_error": error_info.get("last_error"),
            "next_retry_delay": error_info.get("retry_delay", 0),
        }
