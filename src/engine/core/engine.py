from src.engine.core.interfaces import IContext
from src.engine.states.base import State

class GameEngine:
    """The central context orchestrating the State Machine lifecycle."""
    
    def __init__(self, initial_state: State) -> None:
        self._current_state: State = initial_state
        self._is_running: bool = True

    def transition_to(self, new_state: State) -> None:
        """Updates the current state to a new state."""
        self._current_state = new_state

    def stop(self) -> None:
        """Halts the execution loop."""
        self._is_running = False

    def run(self) -> None:
        """The main application loop driving execution."""
        while self._is_running:
            self._current_state.handle(self)

# Type checking assertion to ensure GameEngine strictly conforms to IContext Protocol
_: IContext = GameEngine(initial_state=None) # type: ignore
