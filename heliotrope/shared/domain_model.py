from abc import ABCMeta, abstractmethod
from typing import Any


class DomainModel(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_dict(cls, d: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Any:
        raise NotImplementedError
