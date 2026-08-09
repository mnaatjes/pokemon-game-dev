from abc import abstractmethod
from typing import TYPE_CHECKING, Optional
from src.states.base import State

if TYPE_CHECKING:
    from src.core.interfaces import IContext

class WaitState(State):
    """
    A state that polls for events and idles until a condition is met.
    """
    def handle(self, context: 'IContext') -> None:
        next_state = self._poll_events()
        if next_state is not None:
            context.transition_to(next_state)

    @abstractmethod
    def _poll_events(self) -> Optional[State]:
        """
        Poll hardware or event queues. 
        Return a State to transition, or None to idle for the next heartbeat.
        """
        pass
