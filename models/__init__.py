import importlib
import pkgutil

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Import all modules in the models package
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    importlib.import_module('.' + module_name, __name__)
