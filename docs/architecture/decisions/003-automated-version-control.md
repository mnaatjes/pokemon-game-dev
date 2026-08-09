---
title: "ADR 003: Automated Version Control and Release Management"
tags: ["architecture", "adr", "ci-cd", "versioning", "release"]
created_at: "2026-08-09"
last_updated_at: "2026-08-09"
---

# ADR 003: Automated Version Control and Release Management

## Status
Accepted

## Context
As the project grows, manually tracking version numbers, managing Git tags, and updating the changelog becomes error-prone. A missed tag or a desynced version number between the configuration and the codebase can break save files, corrupt telemetry analytics, and confuse developers. We require a system that eliminates human error by completely automating the release process via our CI/CD pipeline.

## Decision
We will adopt **Semantic Release** using `python-semantic-release` to fully automate versioning, Git tagging, and CHANGELOG generation based entirely on strict commit message formatting.

### 1. Single Source of Truth (SSoT)
*   **The Location:** `pyproject.toml` will serve as the absolute SSoT for the version number. 
*   **Initial State:** The project will begin at `version = "0.1.0"`.
*   **Access:** The game's bootstrapper and telemetry systems will read this version dynamically at runtime using `importlib.metadata`, ensuring they never desync from the codebase.

### 2. Affected and Created Files
*   `pyproject.toml`: Will be modified to include the `[tool.semantic_release]` configuration and the `version = "0.1.0"` property.
*   `.github/workflows/ci.yml`: Will be modified to include the PR Linting Phase and the Post-Merge Release Phase.
*   `CHANGELOG.md`: Will be automatically overwritten/appended to by the release bot during every merge.

### 3. Tooling Required
*   `python-semantic-release`: The Python bot that analyzes commits, bumps the version, and pushes the Git tags.
*   `amannn/action-semantic-pull-request`: A GitHub Action that lints Pull Request titles to ensure they match the Conventional Commits standard (e.g., `feat:`, `fix:`).

### 4. CI/CD Execution Order and Pipeline Integration
The automation relies on separating the pipeline into two strict phases defined in our GitHub Actions YAML configuration:

#### Phase A: The PR Phase (Linting & Testing)
When a developer opens a Pull Request targeting `main`:
1.  **Semantic PR Linter:** GitHub Actions inspects the PR Title. If it does not begin with a valid semantic prefix (like `feat:` or `fix:`), the pipeline instantly fails, physically blocking the merge.
2.  **Standard Checks:** `scripts/run_checks.py` executes (Mypy, Ruff, AST Linter, Pytest).

#### Phase B: The Post-Merge Phase (Release Execution)
When the PR is Squashed and Merged into `main`, the CI/CD pipeline triggers the release sequence:
1.  **Verification:** `scripts/run_checks.py` runs one final time to guarantee the `main` branch is stable.
2.  **Version Bump:** `python-semantic-release` analyzes the Squashed commit message. If it sees `feat:`, it bumps the minor version (e.g., `0.1.0` -> `0.2.0`). If it sees `fix:`, it bumps the patch version (e.g., `0.1.0` -> `0.1.1`).
3.  **File Modification:** The bot updates `pyproject.toml` with the new version number.
4.  **Changelog Generation:** The bot automatically parses the commit body and updates `CHANGELOG.md`.
5.  **Git Tagging & Push:** The bot commits these two file changes, generates a Git tag for the new version (e.g., `git tag v0.2.0`), and pushes everything back to the repository automatically. 

## Consequences
*   **Positive:** Developers never have to manually edit version numbers, write changelogs, or remember to push Git tags. The version history is mathematically guaranteed to be accurate.
*   **Negative:** Developers are forced to adhere strictly to Conventional Commit formatting. A malformed PR title will fail the build.
