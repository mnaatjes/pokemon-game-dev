import sys
from typing import Dict, Type

from src.infrastructure.config import load_environment
from src.infrastructure.logging import RichConsoleLogger
from src.infrastructure.events.sync_bus import SyncEventBus
from src.engine.core.engine import GameEngine
from src.engine.states.base import State
from src.engine.core.interfaces import IContext


# --- Temporary Domain Stubs ---
# These will be moved to src/game/ once we begin Domain-Driven Design
class MainMenuState(State):
    def handle(self, context: IContext) -> None:
        context.logger.info("Main Menu Booted successfully.")
        context.logger.warning("No domain states exist yet. Halting engine.")
        context.stop()

class BattleState(State):
    def handle(self, context: IContext) -> None:
        context.logger.error("Battle State Booted! (Developer Override Activated)")
        context.stop()

# The Dictionary Factory resolving string names to classes
STATE_REGISTRY: Dict[str, Type[State]] = {
    "MainMenuState": MainMenuState,
    "BattleState": BattleState
}


def bootstrap() -> None:
    """The Composition Root of the application."""
    
    # Step 1: Environment Loading
    config = load_environment()
    
    # Step 2 & 3: Infrastructure & Service Assembly
    # We use the config to determine logging verbosity
    log_level = config.override_log_level or config.log_level
    logger = RichConsoleLogger(level=log_level)
    
    events = SyncEventBus()
    
    logger.info(f"Bootstrapping Pokemon Engine v{config.version}...")
    
    if config.debug_mode:
        logger.warning("DEVELOPER CHEATS ENABLED (Debug Mode: True)")
    
    # Resolve the initial state from config
    target_state_name = config.override_initial_state or config.initial_state
    
    if target_state_name not in STATE_REGISTRY:
        logger.error(f"Configuration requested unknown state: '{target_state_name}'")
        sys.exit(1)
        
    initial_state_class = STATE_REGISTRY[target_state_name]
    initial_state = initial_state_class()
    
    logger.info(f"Context Construction complete. Injecting into {target_state_name}.")
    
    # Step 4: Context Construction (Injecting infrastructure)
    engine = GameEngine(
        initial_state=initial_state,
        logger=logger,
        events=events
    )
    
    # Step 5: State Booting
    try:
        engine.run()
    except Exception as e:
        logger.error(f"Engine Crash: {e}")
        sys.exit(1)
    
    logger.info("Engine halted gracefully.")


if __name__ == "__main__":
    bootstrap()
