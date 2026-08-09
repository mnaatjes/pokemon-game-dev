# Project Architecture

This project strictly adheres to a combination of **Hexagonal Architecture** and **Domain-Driven Design (DDD)**, utilizing the **State Pattern** to manage execution flow.

## Unified Directory Structure

```text
src/
├── engine/                 # (HEXAGONAL: Highly reusable, zero game logic)
│   ├── core/               # GameEngine, IContext, Ports
│   └── states/             # State ABCs (Transient, Wait, Composite, Terminal)
│
├── game/                   # (DDD: Strictly Pokemon Business Logic)
│   ├── battle/             # Organized by Feature
│   └── exploration/        # Organized by Feature
│
└── infrastructure/         # (HEXAGONAL: Adapters for the outside world)
    ├── terminal_input.py   # Implements IInputProvider (keyboard reading)
    └── main.py             # Entry point hooking Game to Engine via Adapters
```

## Architectural Paradigms

1. **Rich Domain Models:** Models strictly encapsulate their own localized mutation logic.
2. **State Dependency Injection:** A `ConcreteState` must explicitly request only the specific Models or Services it requires.
3. **Service Centralization:** `Services` act as the centralized, stateless authority for operations spanning multiple models.
4. **Context Encapsulation:** The `Engine` never performs game logic. It only maintains the heartbeat loop.
5. **The Input Boundary Rule:** A state represents a continuous block of execution that is only broken when the system must wait for external input. (Enforced via `WaitState`).
6. **The Single Heartbeat Rule:** There is strictly one infinite loop in the architecture. States must never implement their own blocking `while` loops or sleep calls.
7. **The Orchestrator Role:** `ConcreteStates` act purely as localized orchestrators, delegating math to Services and mutation to Models. (Enforced via McCabe Complexity checks).
