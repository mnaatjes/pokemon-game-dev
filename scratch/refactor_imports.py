import os

files_to_update = [
    "src/engine/core/engine.py",
    "src/engine/core/interfaces.py",
    "src/engine/states/base.py",
    "src/engine/states/composite.py",
    "src/engine/states/terminal.py",
    "src/engine/states/transient.py",
    "src/engine/states/wait.py",
    "tests/architecture/bad_ast_state.py",
    "tests/architecture/test_no_while_loops.py",
    "tests/engine/core/test_engine.py",
    "tests/engine/states/test_state_species.py"
]

for filepath in files_to_update:
    path = f"/home/hp_prodesk/src/pokemon/{filepath}"
    if not os.path.exists(path):
        print(f"Skipping {path}")
        continue
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace("from src.core", "from src.engine.core")
    content = content.replace("from src.states", "from src.engine.states")
    with open(path, 'w') as f:
        f.write(content)
    print(f"Updated {path}")
