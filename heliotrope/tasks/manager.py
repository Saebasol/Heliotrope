from asyncio import sleep
from asyncio.tasks import Task
from dataclasses import dataclass
from typing import Any, Callable, NoReturn, Optional

from sanic.log import logger

from heliotrope.sanic import Heliotrope
from heliotrope.types import SetupTask


@dataclass
class RegisteredTask:
    setup_func: Callable[[Heliotrope, float], SetupTask]
    delay: float
    name: Optional[str] = None


class SuperVisor:
    def __init__(self, app: Heliotrope) -> None:
        self.app = app
        self.tasks: dict[Task[Any], RegisteredTask] = {}

    def add_task(
        self,
        setup_func: Callable[[Heliotrope, float], SetupTask],
        delay: float,
        name: Optional[str] = None,
    ) -> None:
        task: Optional[Task[Any]] = self.app.add_task(
            setup_func(self.app, delay), name=name or setup_func.__qualname__
        )
        assert task
        self.tasks[task] = RegisteredTask(setup_func, delay, name)

    async def start(self, delay: float) -> NoReturn:
        logger.info(f"Supervisor started")
        while True:
            for task in self.app.tasks:
                if task.done():
                    if task.cancelled():
                        logger.warning(f"{task.get_name()} cancled")
                    elif task.exception():
                        try:
                            task.result()
                        except:
                            logger.exception(f"{task.get_name()} is raise exception")

                    logger.warning("Purge task")
                    self.app.purge_tasks()  # type: ignore
                    registered_task = self.tasks[task]
                    del self.tasks[task]
                    logger.warning(f"Try restart {registered_task.name}")
                    self.add_task(
                        registered_task.setup_func,
                        registered_task.delay,
                        registered_task.name,
                    )

            await sleep(delay)
