import os
import importlib

current_dir = os.path.dirname(__file__)

for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename not in ("__init__.py", "nodeRegistry.py"):
        module_name = filename[:-3]  # Strip the .py extension
        print(f"Loading module: {module_name}")
        importlib.import_module(f".{module_name}", package=__package__)