---
title: "ADR 001: Automated Architectural Enforcement"
tags: ["architecture", "adr", "ci-cd", "state-pattern"]
created_at: "2026-08-09"
last_updated_at: "2026-08-09"
---

# ADR 001: Automated Architectural Enforcement

## Status
Accepted

## Context
Our system utilizes a strict Hexagonal Architecture combined with Domain-Driven Design (DDD) and the State Pattern. 
Without rigid, automated enforcement, these boundaries naturally erode as developers take shortcuts under deadline pressure. Specifically:
1. **Dependency Inversion:** The generic `engine` layer might accidentally import from the specific `game` layer, creating a circular dependency and destroying the Engine's reusability.
2. **State Bloat:** Concrete `State` classes might assume mathematical or heavy algorithmic duties, violating the "Simple Orchestrator Role" of the State Pattern.
3. **Heartbeat Blocking:** States might implement `while` loops or synchronous blocking calls, destroying the Engine's continuous Single Heartbeat loop.

## Decision
We have elected to automate architectural enforcement using a rigid CI/CD pipeline (`scripts/run_checks.py`), guaranteeing that no code can be merged into `main` if it violates the system's design. We rely on three specific automated mechanisms:

### 1. Clean Architecture Dependencies (`import-linter`)
We enforce the Dependency Inversion Principle via `import-linter`. The contract defined in `pyproject.toml` physically prevents the inner `src.engine` package from importing any code from the `src.game` or `src.infrastructure` packages, and prevents `src.game` from importing `src.infrastructure`.

### 2. The Simple Orchestrator Role (`ruff`)
We cap McCabe cyclomatic complexity at `5` globally via `ruff`. If a State contains complex mathematical branching or heavy `if/else` logic, the build fails. This physically forces the developer to offload complex logic into dedicated injected Services or Models.

### 3. The Single Heartbeat Rule (AST Linter)
A custom Python Abstract Syntax Tree (AST) parser (`tests/architecture/test_no_while_loops.py`) statically analyzes all production code. It will instantly fail the build if it detects `while`, `time.sleep()`, or `input()` calls inside any State, ensuring the game loop never hangs.

## Consequences
*   **Positive:** The Engine is permanently protected from domain logic leakage and remains highly portable. Developers are physically forced to write clean, Service-oriented, non-blocking code.
*   **Negative:** There is a steeper learning curve for new developers who may feel constrained by the strict build failures.
*   **Exemptions:** The `tests/` directory is explicitly exempt from the `ruff` complexity check, as testing utilities (like the AST parser itself) naturally require higher cyclomatic complexity.
