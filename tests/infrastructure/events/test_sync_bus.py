import json
from dataclasses import dataclass
from pathlib import Path
import pytest
from src.engine.core.interfaces import IDomainEvent
from src.infrastructure.events.sync_bus import SyncEventBus

@dataclass
class DummyCombatEvent(IDomainEvent):
    damage: int
    target: str

def test_sync_bus_serializes_and_appends_correctly(tmp_path: Path) -> None:
    """Verifies that the SyncEventBus correctly formats and saves JSONL telemetry."""
    # Use an isolated temporary file provided natively by Pytest
    test_file = tmp_path / "test_telemetry.jsonl"
    
    bus = SyncEventBus(file_path=str(test_file))
    
    # Fire an event
    event1 = DummyCombatEvent(damage=50, target="Pikachu")
    bus.publish(event1)
    
    # Fire a second event
    event2 = DummyCombatEvent(damage=10, target="Bulbasaur")
    bus.publish(event2)
    
    # Read the file back from disk and verify contents
    assert test_file.exists()
    
    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    assert len(lines) == 2
    
    # Parse the first line mathematically
    parsed_1 = json.loads(lines[0])
    assert parsed_1["event_type"] == "DummyCombatEvent"
    assert parsed_1["data"]["damage"] == 50
    assert parsed_1["data"]["target"] == "Pikachu"
    assert "timestamp" in parsed_1
    
    # Parse the second line
    parsed_2 = json.loads(lines[1])
    assert parsed_2["data"]["target"] == "Bulbasaur"

def test_sync_bus_rejects_non_dataclass(tmp_path: Path) -> None:
    """Verifies that the bus strictly enforces the dataclass payload requirement."""
    test_file = tmp_path / "test_telemetry.jsonl"
    bus = SyncEventBus(file_path=str(test_file))
    
    class BadEvent: # Missing @dataclass decorator
        pass
        
    with pytest.raises(ValueError, match="must be an instantiated dataclass"):
        bus.publish(BadEvent())
