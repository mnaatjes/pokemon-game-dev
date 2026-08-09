# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - Architecture Foundation

### Added
- **Core Engine**: Implemented `GameEngine` and the `IContext` protocol to manage the central heartbeat loop and prevent circular dependencies.
- **State Species**: Created specialized abstract base classes for the four identified State species to strictly enforce architectural behaviors:
  - `TransientState`: Enforces instantaneous logic and immediate transitions via the Template Method Pattern.
  - `WaitState`: Enforces non-blocking input polling and idling at Input Boundaries.
  - `CompositeState`: Enforces Hierarchical State Machine (HSM) macroscopic behavior and sub-state delegation.
  - `TerminalState`: Enforces system cleanup and safely halts the engine loop.
- **Architectural Testing (AST Linter)**: Built a custom static analysis linter (`tests/architecture/test_no_while_loops.py`) that strictly bans `while` loops, `input()`, and `time.sleep()` calls inside any game state, ensuring the "Single Heartbeat Rule".
- **Heartbeat Timer**: Implemented a 1.5-second execution threshold in the test suite to catch computationally blocked states.
- **CI/CD Enforcement Regime**: Established a full pipeline configuration (`scripts/run_checks.py` and `.github/workflows/ci.yml`) integrating `mypy`, `ruff`, and `pytest`.
- **Complexity Enforcement**: Configured `ruff` (McCabe complexity limit = 5) to strictly enforce the "Simple Orchestrator Role", guaranteeing states delegate complex logic to Services and Models.
- **Project Documentation**: Initialized `README.md` defining the unified Hexagonal/Domain-Driven Design directory structure and overarching paradigms.
- **Dependencies**: Added `requirements.txt` and `pyproject.toml` configurations for `pytest`, `mypy`, and `ruff`.
