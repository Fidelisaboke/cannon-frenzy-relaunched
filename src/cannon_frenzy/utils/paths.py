import os
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # In development, use the project root (one level up from src/cannon_frenzy/utils)
        # Actually, let's make it relative to the PROJECT_ROOT
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # current_dir is src/cannon_frenzy/utils
        # project_root is three levels up
        base_path = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

    return os.path.join(base_path, relative_path)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

def get_asset_path(path_under_assets):
    return os.path.join(ASSETS_DIR, path_under_assets)
