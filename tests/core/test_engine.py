from src.core.engine import GameEngine
from src.core.interfaces import IContext
from src.states.base import State

class DummyEndState(State):
    """A state that immediately stops the engine when reached."""
    def handle(self, context: IContext) -> None:
        context.stop()

class DummyTransitionState(State):
    """A state that transitions to another state."""
    def handle(self, context: IContext) -> None:
        context.transition_to(DummyEndState())

def test_engine_initialization():
    initial_state = DummyEndState()
    engine = GameEngine(initial_state)
    assert engine._current_state is initial_state
    assert engine._is_running is True

def test_engine_transition():
    engine = GameEngine(DummyTransitionState())
    engine.transition_to(DummyEndState())
    assert isinstance(engine._current_state, DummyEndState)

def test_engine_stop():
    engine = GameEngine(DummyEndState())
    engine.stop()
    assert engine._is_running is False

def test_engine_run_loop():
    # Engine starts in TransitionState, which transitions to EndState, which stops the loop.
    # This verifies the loop runs states in sequence and correctly halts without mocking.
    initial_state = DummyTransitionState()
    engine = GameEngine(initial_state)
    
    engine.run()
    
    assert engine._is_running is False
    assert isinstance(engine._current_state, DummyEndState)
