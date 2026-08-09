from src.engine.core.interfaces import IContext
from src.engine.states.base import State

class BadAstState(State):
    """A state designed to fail the AST architectural test."""
    def handle(self, context: 'IContext') -> None:
        while True:
            # This loop will be caught by the AST sniffer
            pass
