from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.states.base import State

class IContext(Protocol):
    """The interface representing the State Machine orchestrator."""
    
    def transition_to(self, new_state: 'State') -> None:
        """Transitions the context to a new ConcreteState."""
        ...
        
    def stop(self) -> None:
        """Signals the context to halt execution."""
        ...
