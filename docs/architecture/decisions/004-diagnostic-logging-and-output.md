---
title: "ADR 004: Diagnostic Logging and Output"
tags: ["architecture", "adr", "logging", "observability"]
created_at: "2026-08-10"
last_updated_at: "2026-08-10"
---

# ADR 004: Diagnostic Logging and Output

## Status
Accepted

## Context
During development and production, the engine requires a mechanism to report system health, milestones, and errors (e.g., "Engine started," "Save file missing"). This output must be human-readable, visually distinct for developers, and strictly separated from structured game telemetry (which is handled by the EventBus). We require a logging solution that integrates seamlessly into our Hexagonal Architecture without tightly coupling the core engine to specific third-party libraries.

## Decision
We will utilize Python's built-in `logging` module, wrapped by the `rich.logging.RichHandler` for enhanced terminal output, behind a strict abstract interface.

### 1. Conceptual Distinction
*   **The Logger:** Dedicated exclusively to System Health and Diagnostics (human-readable text for developers).
*   **The Sinks:** The logger can be configured to multiplex outputs (e.g., simultaneously rendering color-coded text to the terminal while appending raw strings to a persistent `app.log` file).

### 2. Implementation Pipeline
To preserve Dependency Inversion, the Logger must be implemented in the following sequence:

1.  **Define the Port (`src/engine/core/interfaces.py`):**
    Establish the `ILogger` Protocol mandating four standard severity methods: `.debug()`, `.info()`, `.warning()`, and `.error()`. Update the `IContext` Protocol to expose the logger as a property.
2.  **Build the Adapter (`src/infrastructure/logging/rich_logger.py`):**
    Create a `RichConsoleLogger` class that fulfills the `ILogger` interface. This class will internally import Python's built-in `logging` and the `RichHandler` plugin, hiding their complexity from the engine.
3.  **Bootstrapper Injection (`src/infrastructure/main.py`):**
    The bootstrapper will read the desired `log_level` from the `AppConfig` (built in Step 1), instantiate the `RichConsoleLogger` with that threshold, and inject it into the `GameEngine`.

### 3. Example Usage
Because the logger is attached to the `IContext`, any Game State can access it natively during its execution phase without importing external libraries.

```python
class LoadingState(State):
    def handle(self, context: IContext) -> None:
        context.logger.info("Initializing game assets...")
        try:
            self._load_textures()
        except FileNotFoundError as e:
            # Prints to terminal in bold red via the Rich adapter
            context.logger.error(f"Failed to load texture: {e}")
            context.stop()
```

## Consequences
*   **Positive:** Complete decoupling. The Game Engine has no knowledge of Python's `logging` module or the `rich` library. The visual output format can be completely replaced by writing a new adapter without touching a single line of game logic.
*   **Positive:** Real-time, highly readable visual feedback in the terminal accelerates debugging.
*   **Negative:** Requires initial boilerplate to wrap the standard library tools behind the interface.
