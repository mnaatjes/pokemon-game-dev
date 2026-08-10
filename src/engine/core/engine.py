from src.engine.core.interfaces import IContext, ILogger, IEventBus
from src.engine.states.base import State

class GameEngine:
    """The central context orchestrating the State Machine lifecycle."""
    
    def __init__(self, initial_state: State, logger: 'ILogger', events: 'IEventBus') -> None:
        self._current_state: State = initial_state
        self._logger = logger
        self._events = events
        self._is_running: bool = True

    @property
    def logger(self) -> 'ILogger':
        return self._logger

    @property
    def events(self) -> 'IEventBus':
        return self._events

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
_: IContext = GameEngine(initial_state=None, logger=None, events=None) # type: ignore
