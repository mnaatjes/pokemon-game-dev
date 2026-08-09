# Project Architecture

This project strictly adheres to a combination of **Hexagonal Architecture** and **Domain-Driven Design (DDD)**, utilizing the **State Pattern** to manage execution flow.

## Unified Directory Structure

```text
src/
├── core/                   # (HEXAGONAL: Pure logic only, zero outside dependencies)
│   ├── engine.py           # The heartbeat loop (Context)
│   ├── interfaces.py       # IContext, IInputProvider, ISaveManager (Ports)
│   ├── architecture/       # State ABCs (Transient, Wait, Composite, Terminal)
│   │
│   ├── battle/             # (DDD: Organized by Feature)
│   │   ├── models.py
│   │   ├── services.py
│   │   └── states.py       # Concrete Battle states
│   │
│   └── exploration/        # (DDD: Organized by Feature)
│       ├── models.py
│       └── states.py       # Concrete Exploration states
│
└── infrastructure/         # (HEXAGONAL: Adapters for the outside world)
    ├── terminal_input.py   # Implements IInputProvider (keyboard reading)
    ├── pygame_renderer.py  # Implements IRenderer
    └── json_save_repo.py   # Implements ISaveManager
```

## Architectural Paradigms

1. **Rich Domain Models:** Models strictly encapsulate their own localized mutation logic.
2. **State Dependency Injection:** A `ConcreteState` must explicitly request only the specific Models or Services it requires.
3. **Service Centralization:** `Services` act as the centralized, stateless authority for operations spanning multiple models.
4. **Context Encapsulation:** The `Engine` never performs game logic. It only maintains the heartbeat loop.
5. **The Input Boundary Rule:** A state represents a continuous block of execution that is only broken when the system must wait for external input. (Enforced via `WaitState`).
6. **The Single Heartbeat Rule:** There is strictly one infinite loop in the architecture. States must never implement their own blocking `while` loops or sleep calls.
7. **The Orchestrator Role:** `ConcreteStates` act purely as localized orchestrators, delegating math to Services and mutation to Models. (Enforced via McCabe Complexity checks).
