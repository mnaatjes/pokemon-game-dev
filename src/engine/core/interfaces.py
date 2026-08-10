from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.states.base import State


class ILogger(Protocol):
    """Protocol for diagnostic system health logging."""
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...


class IDomainEvent(Protocol):
    """Base Protocol for all game events passed through the EventBus."""
    pass


class IEventBus(Protocol):
    """Protocol for the core pub/sub telemetry and event router."""
    def publish(self, event: IDomainEvent) -> None: ...


class IContext(Protocol):
    """The interface representing the State Machine orchestrator."""
    
    @property
    def logger(self) -> ILogger:
        """Grants all states access to diagnostic logging."""
        ...
        
    @property
    def events(self) -> IEventBus:
        """Grants all states access to event publishing."""
        ...
    
    def transition_to(self, new_state: 'State') -> None:
        """Transitions the context to a new ConcreteState."""
        ...
        
    def stop(self) -> None:
        """Signals the context to halt execution."""
        ...
