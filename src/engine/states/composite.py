from abc import abstractmethod
from typing import Optional
from src.engine.states.base import State
from src.engine.core.interfaces import IContext, ILogger, IEventBus

class CompositeState(State, IContext):
    """
    A Hierarchical State Machine (HSM) node.
    Acts as a State to its parent engine, and a Context to its sub-states.
    """
    def __init__(self, initial_sub_state: State):
        self._current_sub_state: Optional[State] = initial_sub_state
        self._parent_context: Optional[IContext] = None

    @property
    def logger(self) -> ILogger:
        if not self._parent_context:
            raise RuntimeError("CompositeState accessed logger before parent context was bound.")
        return self._parent_context.logger

    @property
    def events(self) -> IEventBus:
        if not self._parent_context:
            raise RuntimeError("CompositeState accessed events before parent context was bound.")
        return self._parent_context.events

    def transition_to(self, new_sub_state: State) -> None:
        """Fulfills IContext for children."""
        self._current_sub_state = new_sub_state
        
    def stop(self) -> None:
        """Fulfills IContext for children. Halts the sub-ecosystem."""
        self._current_sub_state = None

    def handle(self, context: 'IContext') -> None:
        """Fulfills State for parent. Delegates downward."""
        self._parent_context = context
        if self._current_sub_state:
            self._current_sub_state.handle(self)
        
        # Evaluate if the macroscopic state is finished
        next_macro_state = self._evaluate_macro_transition()
        if next_macro_state:
            context.transition_to(next_macro_state)

    @abstractmethod
    def _evaluate_macro_transition(self) -> Optional[State]:
        """
        Determine if the entire sub-ecosystem is finished and return the 
        next macroscopic state, or None to continue sub-state execution.
        """
        pass
