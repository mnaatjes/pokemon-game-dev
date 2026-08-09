from abc import abstractmethod
from typing import TYPE_CHECKING
from src.states.base import State

if TYPE_CHECKING:
    from src.core.interfaces import IContext

class TransientState(State):
    """
    A state that executes instantaneous logic and immediately transitions.
    Enforces the Template Method Pattern to guarantee a transition occurs.
    """
    def handle(self, context: 'IContext') -> None:
        next_state = self._execute_logic()
        context.transition_to(next_state)

    @abstractmethod
    def _execute_logic(self) -> State:
        """
        Execute business logic and return the next state to transition to.
        Must not contain blocking loops.
        """
        pass
