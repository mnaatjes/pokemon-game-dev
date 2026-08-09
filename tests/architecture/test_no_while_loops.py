import ast
import time
import pytest
from pathlib import Path
from src.core.interfaces import IContext
from src.states.base import State

class ArchitectureViolation(Exception):
    """Custom exception raised when architectural rules are broken."""
    pass

def validate_state_ast(filepath: str, file_content: str) -> None:  # noqa: C901
    """Parses AST and raises ArchitectureViolation if illegal nodes are found."""
    try:
        tree = ast.parse(file_content, filename=filepath)
    except SyntaxError:
        raise ArchitectureViolation(f"Syntax error while parsing {filepath}")
    
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            raise ArchitectureViolation(
                f"Found illegal 'while' loop in {filepath} on line {node.lineno}."
            )
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "input":
                raise ArchitectureViolation(
                    f"Found illegal 'input()' call in {filepath} on line {node.lineno}."
                )
            elif isinstance(node.func, ast.Attribute) and node.func.attr == "sleep":
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "time":
                    raise ArchitectureViolation(
                        f"Found illegal 'time.sleep()' call in {filepath} on line {node.lineno}."
                    )

def test_production_states_abide_by_architecture():
    """Recursively loops through production state files and ensures they pass the AST check."""
    src_dir = Path("src")
    if not src_dir.exists():
        return
        
    for path in src_dir.rglob("*.py"):
        if path.name == "__init__.py" or path.name == "bad_ast_state.py":
            continue
            
        # Target files inside any 'states' directory, or files named '*state*.py'
        if "states" in path.parts or "state" in path.name:
            with open(path, "r") as file:
                validate_state_ast(str(path), file.read())

def test_ast_linter_catches_violations():
    """Verifies that our custom linter correctly identifies bad syntax."""
    bad_filepath = "tests/architecture/bad_ast_state.py"
    with open(bad_filepath, "r") as file:
        bad_code_1 = file.read()
        
    with pytest.raises(ArchitectureViolation, match="Found illegal 'while' loop"):
        validate_state_ast(bad_filepath, bad_code_1)

# ---------------------------------------------------------
# Execution Time Tests
# ---------------------------------------------------------
class MockContext(IContext):
    def transition_to(self, new_state: State) -> None: pass
    def stop(self) -> None: pass

class MockState(State):
    def handle(self, context: IContext) -> None: pass 

class SlowMockState(State):
    def handle(self, context: IContext) -> None:
        time.sleep(1.6) # Over the 1.5s limit

def enforce_heartbeat(state: State, context: IContext) -> None:
    """Helper to run the state and enforce the timer."""
    start_time = time.perf_counter()
    state.handle(context)
    end_time = time.perf_counter()
    duration = end_time - start_time
    if duration >= 1.5:
        raise ArchitectureViolation(f"State blocked heartbeat for {duration}s")

def test_heartbeat_execution_time_success():
    """Ensures a valid state executes within the heartbeat limit."""
    enforce_heartbeat(MockState(), MockContext())

def test_heartbeat_execution_time_failure_is_caught():
    """Ensures the timer correctly catches a blocked state."""
    with pytest.raises(ArchitectureViolation, match="State blocked heartbeat"):
        enforce_heartbeat(SlowMockState(), MockContext())
