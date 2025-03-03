# app/db/models/__init__.py

import importlib

from sqlmodel import SQLModel

MODELS_LIST = [
    "app.features.users.model"
]

__all__ = []

# Dynamically import all models from the list
for module_path in MODELS_LIST:
    module = importlib.import_module(module_path)
    for attr in dir(module):
        if not attr.startswith("_"):  # Skip private attributes
            globals()[attr] = getattr(module, attr)
            __all__.append(attr)


target_metadata = SQLModel.metadata
