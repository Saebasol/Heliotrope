from asyncio import Task
from typing import Any, Callable, Coroutine, NoReturn

from sanic.log import logger

from heliotrope.infrastructure.sanic.app import Heliotrope


def callback(
    callback_task: Task[NoReturn],
    retry_task: Callable[..., Coroutine[Any, Any, None]],
    app: Heliotrope,
) -> None:
    logger.debug(f"Callback for {callback_task.get_name()}")

    if callback_task.cancelled():
        logger.warning(f"{callback_task.get_name()} Task was cancelled")
    elif callback_task.exception():
        try:
            callback_task.result()
        except:
            logger.exception(f"{callback_task.get_name()} Task raised an exception")

    logger.debug(f"{callback_task.get_name()} Task finished")
    app.purge_tasks()
    logger.debug(f"Purging {callback_task.get_name()} Task")
    logger.info(f"Retrying {callback_task.get_name()} Task")
    task = app.add_task(
        retry_task(),
        name=f"{callback_task.get_name()}",
    )
    assert task
    task.add_done_callback(lambda t: callback(t, retry_task, app))
