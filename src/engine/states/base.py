from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.core.interfaces import IContext

class State(ABC):
    """
    The root abstract base class for all states.
    Satisfies the contract required by the GameEngine loop.
    """
    @abstractmethod
    def handle(self, context: 'IContext') -> None:
        pass
