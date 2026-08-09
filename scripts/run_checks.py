import subprocess
import sys

def run_check(command: list[str], step_name: str) -> None:
    print(f"--- Running: {step_name} ---")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"FAILED: {step_name}. Halting pipeline.")
        sys.exit(1)
    print("PASSED\n")

if __name__ == "__main__":
    # 1. Type Checking
    run_check(["mypy", "."], "Type Checking (mypy)")
    
    # 2. Architectural Complexity & Linting
    run_check(["ruff", "check", "."], "Architecture & Complexity (ruff)")
    
    # 3. Dependency Boundary Enforcement
    run_check(["lint-imports"], "Dependency Boundaries (import-linter)")
    
    # 3. Unit & Architectural Tests
    run_check(["pytest", "-v"], "Unit & Architecture Tests (pytest)")
    
    print("All checks passed successfully! Code is architecturally sound.")
