---
title: "ADR 005: Event Bus and Telemetry"
tags: ["architecture", "adr", "telemetry", "events"]
created_at: "2026-08-10"
last_updated_at: "2026-08-10"
---

# ADR 005: Event Bus and Telemetry

## Status
Accepted

## Context
As the game scales, various systems need to communicate without being tightly coupled. For example, when a Pokemon takes damage, the Audio System needs to play a sound, the UI needs to flash the health bar, and the Analytics system needs to record the combat statistics. If the `BattleState` directly calls all three systems, it violates the Single Responsibility Principle and creates a tangled dependency web. 

Additionally, we require a mechanism to track player behavior and game balance metrics over time in a structured, machine-readable format (Telemetry), strictly distinct from the human-readable diagnostic Logger defined in ADR 004.

## Decision
We will implement a central **Event Bus** utilizing the Publish/Subscribe (Pub/Sub) pattern.

### 1. Conceptual Distinction
*   **Logger (ADR 004):** Unstructured text. Used for system health (e.g., "Engine Booted", "File Not Found"). Output to terminal.
*   **Event Bus (ADR 005):** Structured data. Used for domain occurrences (e.g., "DamageDealt(amount=50, target='Pikachu')"). Output to internal subscribers and structured `.jsonl` files.

### 2. The Implementation Pipeline
1.  **Domain Events (The Payload):**
    All events must be defined as pure Python `@dataclass` objects that inherit from the `IDomainEvent` protocol. They contain no logic, only immutable state.
2.  **The Port (`IEventBus`):**
    The interface mandates a `publish(event: IDomainEvent)` method. (A `subscribe` method may be added later for internal system wiring, but `publish` is the primary domain interaction).
3.  **The Adapter (`SyncEventBus`):**
    A synchronous implementation located in `src/infrastructure/events/sync_bus.py`. 
    *   **Tooling:** Pure Python standard library (no external dependencies required).
    *   **Telemetry Sink:** The adapter will be hardcoded (or configured via AppConfig) to serialize every published event into a JSON string and append it to `data/telemetry.jsonl`.
4.  **Bootstrapper Injection (`main.py`):**
    Instantiated alongside the Logger and injected into the `GameEngine`.

### 3. Example Usage
```python
from dataclasses import dataclass
from src.engine.core.interfaces import IDomainEvent, IContext
from src.engine.states.base import State

@dataclass
class PlayerMovedEvent(IDomainEvent):
    x: int
    y: int
    map_name: str

class ExplorationState(State):
    def handle(self, context: IContext) -> None:
        # Move logic...
        
        # Fire and forget. The State doesn't care who is listening.
        context.events.publish(PlayerMovedEvent(x=10, y=15, map_name="Route 1"))
```

### 4. Telemetry Output Format (JSONL)
The resulting output in `data/telemetry.jsonl` will look like this, making it perfectly parsable by data analytics tools:
```json
{"event_type": "PlayerMovedEvent", "timestamp": "2026-08-10T00:48:00Z", "data": {"x": 10, "y": 15, "map_name": "Route 1"}}
{"event_type": "DamageDealtEvent", "timestamp": "2026-08-10T00:48:05Z", "data": {"amount": 50, "target": "Pikachu"}}
```

## Consequences
*   **Positive:** Complete decoupling. The game logic simply broadcasts that something happened and moves on.
*   **Positive:** Data is inherently structured and ready for analytical ingestion.
*   **Negative:** Developers must remember to define a formal dataclass for every new event type, rather than just passing strings.
