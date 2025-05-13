import sys
from pathlib import Path


def resource_path(relative_path):
    """
    Get the absolute path to a resource, compatible with PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    base_path = getattr(sys, '_MEIPASS', Path(__file__).parent.parent)  # Handle PyInstaller's temporary folder
    return str(Path(base_path) / relative_path)