---
title: "ADR 002: Composition Root and Bootstrapping Pipeline"
tags: ["architecture", "adr", "bootstrapping", "dependency-injection"]
created_at: "2026-08-09"
last_updated_at: "2026-08-09"
---

# ADR 002: Composition Root and Bootstrapping Pipeline

## Status
Pending

## Context
To adhere strictly to Hexagonal Architecture, our `src/engine/` and `src/game/` layers must remain entirely ignorant of the outside world. However, the system must eventually be assembled and provided with concrete infrastructure (like loggers, save managers, and renderers) to function. If bootstrapping is not strictly controlled, developers may inject domain logic into infrastructure or vice versa, creating tightly coupled spaghetti code that is impossible to test.

## Decision
We have established a single, strictly controlled **Composition Root** located exclusively within `src/infrastructure/` (e.g., `main.py`). This is the only domain permitted to wire together the application's distinct layers.

### The Ordered Bootstrapping Steps
The Composition Root must assemble the application in the following strict sequence:
1. **Environment Loading:** Parse configuration files and command-line arguments to construct a strictly-typed `AppConfig` object via `pydantic-settings`. This parsing logic must be completely isolated inside `src/infrastructure/config.py` to keep the main bootstrapper clean.
   *   **`config.json` (Production Baseline):** Tracked in Git. Must define `initial_state` (e.g., `"MainMenuState"`), `target_fps` (e.g., `60`), and `log_level` (e.g., `"INFO"`). Since JSON cannot execute code, it does NOT contain the version number. Instead, the bootstrapper dynamically reads the version from `pyproject.toml` (the SSoT) at runtime and merges it into the configuration object.
   *   **`.env` (Developer Overrides):** Ignored by Git. Developers use this to locally hijack the boot sequence. Must support `DEBUG_MODE=True`, `OVERRIDE_LOG_LEVEL=DEBUG`, and `OVERRIDE_INITIAL_STATE=BattleState` (to bypass the main menu during testing).
2. **Infrastructure Initialization:** Instantiate raw OS/Hardware adapters (e.g., `TerminalLogger`, `JsonTelemetrySink`).
3. **Domain Service Assembly:** Instantiate global services that require adapters.
4. **Context Construction:** Assemble the `GameEngine` (which fulfills the `IContext` protocol), injecting the concrete infrastructure adapters into the Engine's defined Ports.
5. **State Booting:** Inject the initial `State` (dynamically selected via the environment loader to ensure decoupling) into the Engine and execute `engine.run()`.

### Injection Rules & Directory Boundaries
*   **Permitted:** The Composition Root MUST inject concrete implementations from `src/infrastructure/` into the abstract Ports defined within `src/engine/core/interfaces.py`.
*   **Forbidden:** The Composition Root MUST NOT manage highly specific, internal Domain object wiring (e.g., injecting a specific `Pikachu` entity into a `BattleState`). Object generation within the game's business logic is the responsibility of Domain Factories located strictly within `src/game/`.

## Enforcement Mechanism
These rules are automated and guaranteed by our CI/CD pipeline (`scripts/run_checks.py`):
1. **Boundary Enforcement (`import-linter`):** The `import-linter` contract explicitly defines `src.infrastructure` as the top-most layer. It physically prevents any code within `src.engine` or `src.game` from attempting to bootstrap or import adapters, forcing all assembly to occur in the Composition Root.
2. **Type Safety (`mypy`):** Statically ensures that the concrete infrastructure adapters instantiated in the Composition Root perfectly fulfill the Protocol requirements of `src/engine/core/interfaces.py`.

### Configuration Hierarchy of Truth
When `AppConfig` is constructed, property conflicts are resolved via a strict priority system. If multiple sources declare a value for the same property, the highest priority wins:
1.  **CLI Arguments:** (Highest) Command-line flags explicitly passed by the user (e.g., `--state=BattleState`).
2.  **`.env` File:** Developer local overrides (`DEBUG=True`).
3.  **`config.json`:** The global production baseline.
4.  **`pyproject.toml`:** (Lowest) Used exclusively as the immutable Single Source of Truth for the version number.

### CLI Implementation Rules
The CLI parser (`argparse`) must remain a thin translation layer. It is restricted to parsing the following specific parameters before passing them to the Pydantic configuration model:

| Command | Flag | Type | Description |
| :--- | :--- | :--- | :--- |
| `python src/infrastructure/main.py` | `--debug` | `bool` | Enables development logging, telemetry streaming, and visual cheat markers. |
| `python src/infrastructure/main.py` | `--state` | `string` | Bypasses the default `config.json` initial state, instantly booting the engine into the specified state. |
| `python src/infrastructure/main.py` | `--log-level` | `string` | Overrides the default logging verbosity (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`). |

## Consequences
*   **Positive:** Absolute decoupling. The Engine and Game layers can be tested completely in isolation using mock adapters.
*   **Negative:** Added boilerplate. Even simple services must be deliberately wired through the formal pipeline before they can be used by the game.
