import json
import time
import dataclasses
from pathlib import Path
from src.engine.core.interfaces import IEventBus, IDomainEvent

class SyncEventBus(IEventBus):
    """
    A synchronous implementation of the Event Bus that routes
    all domain events directly to a JSONL telemetry file.
    """
    def __init__(self, file_path: str = "data/telemetry.jsonl") -> None:
        self._file_path = Path(file_path)
        # Ensure the target directory exists
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def publish(self, event: IDomainEvent) -> None:
        """Serializes the event payload and appends it to the telemetry log."""
        if not dataclasses.is_dataclass(event) or isinstance(event, type):
            raise ValueError(
                f"Event {event} must be an instantiated dataclass "
                "inheriting from IDomainEvent"
            )
            
        # Convert the pure Python dataclass to a dictionary
        payload = dataclasses.asdict(event)
        
        # Structure the telemetry envelope
        envelope = {
            "event_type": event.__class__.__name__,
            "timestamp": time.time(),
            "data": payload
        }
        
        # Append the JSON string to the log file immediately
        with open(self._file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(envelope) + "\n")
