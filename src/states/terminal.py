from abc import abstractmethod
from typing import TYPE_CHECKING
from src.states.base import State

if TYPE_CHECKING:
    from src.core.interfaces import IContext

class TerminalState(State):
    """
    A state representing the end of a lifecycle.
    Enforces that context.stop() is called.
    """
    def handle(self, context: 'IContext') -> None:
        self._execute_cleanup()
        context.stop()

    @abstractmethod
    def _execute_cleanup(self) -> None:
        """Execute final save data, network disconnects, or teardown logic."""
        pass
