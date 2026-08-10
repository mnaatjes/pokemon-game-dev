from src.engine.core.interfaces import IContext
from src.engine.states import State, TransientState, WaitState, CompositeState, TerminalState

class MockContext(IContext):
    def __init__(self):
        self.next_state = None
        self.is_stopped = False
    @property
    def logger(self): return None
    @property
    def events(self): return None
        
    def transition_to(self, new_state: State) -> None:
        self.next_state = new_state
        
    def stop(self) -> None:
        self.is_stopped = True

class DummyTargetState(State):
    def handle(self, context: IContext) -> None: pass

# --- Transient Test ---
class MathState(TransientState):
    def _execute_logic(self) -> State:
        return DummyTargetState()

def test_transient_state_forces_transition():
    context = MockContext()
    state = MathState()
    state.handle(context)
    assert isinstance(context.next_state, DummyTargetState)

# --- Wait Test ---
class PollingState(WaitState):
    def __init__(self, key_pressed: bool):
        self.key_pressed = key_pressed
        
    def _poll_events(self):
        if self.key_pressed:
            return DummyTargetState()
        return None

def test_wait_state_idles():
    context = MockContext()
    state = PollingState(key_pressed=False)
    state.handle(context)
    assert context.next_state is None # Engine ticks again

def test_wait_state_transitions():
    context = MockContext()
    state = PollingState(key_pressed=True)
    state.handle(context)
    assert isinstance(context.next_state, DummyTargetState)

# --- Composite Test ---
class InnerState(State):
    def __init__(self):
        self.was_handled = False
    def handle(self, context: IContext) -> None:
        self.was_handled = True

class BattleMacroState(CompositeState):
    def __init__(self, inner: State, battle_over: bool):
        super().__init__(inner)
        self.battle_over = battle_over
        
    def _evaluate_macro_transition(self):
        if self.battle_over:
            return DummyTargetState()
        return None

def test_composite_state_delegates_downward():
    inner = InnerState()
    macro = BattleMacroState(inner, battle_over=False)
    main_engine = MockContext()
    
    macro.handle(main_engine)
    
    assert inner.was_handled is True
    assert main_engine.next_state is None # Macro state is still active

def test_composite_state_transitions_upward():
    inner = InnerState()
    macro = BattleMacroState(inner, battle_over=True)
    main_engine = MockContext()
    
    macro.handle(main_engine)
    assert isinstance(main_engine.next_state, DummyTargetState)

# --- Terminal Test ---
class EndGameState(TerminalState):
    def _execute_cleanup(self) -> None:
        pass

def test_terminal_state_forces_stop():
    context = MockContext()
    state = EndGameState()
    state.handle(context)
    assert context.is_stopped is True
