# Project Backlog

## Architectural Enforcement Remaining
- [ ] **Dependency Boundary Contracts (`import-linter`)**: Implement and configure `import-linter` to strictly prevent Domain/Feature layers (e.g., `src.battle.states`) from importing back into the Core Engine layer, and to enforce Hexagonal boundary rules (the Core cannot import from Infrastructure).
- [ ] **AST Mathematical Restrictions (Optional)**: Expand `test_no_while_loops.py` to optionally ban `ast.Add`, `ast.Sub`, `ast.Mult`, and `ast.Div` inside state files, physically forcing 100% of arithmetic calculations into injected Services or Models.

## Hexagonal Infrastructure Construction
- [ ] **Define Port Interfaces**: Expand `src/core/interfaces.py` to define the architectural contracts required to interact with the outside world (e.g., `IInputProvider`, `IRenderer`, `ISaveManager`).
- [ ] **Build Adapters**: Create the `src/infrastructure/` directory and implement the terminal/Pygame adapters that fulfill the defined Ports.

## Concrete Game Implementation (Domain-Driven Design)
- [ ] **Domain Separation**: Create the first feature domain directory (e.g., `src/main_menu/` or `src/overworld/`).
- [ ] **First Concrete States**: Implement a working game state (like `MainMenuState`) inheriting from the appropriate architectural species (e.g., `WaitState`).
- [ ] **Dependency Injection Assembly**: Write the `main.py` root entry point that instantiates the Infrastructure Adapters, injects them into the Engine, and boots the initial state.
