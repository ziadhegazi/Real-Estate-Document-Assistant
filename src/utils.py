"""
Common Functions that you will use throughout the project.
"""
import os
import sys
import pickle
import dill
from src.exception import CustomException


def save_object(filepath: str, obj: object):
    """
    Saves a Python object to a file.

    Args:
        filepath (str): The path where the object should be saved.
        obj (object): The object to save.
    """
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e

def load_object(filepath: str) -> object:
    """
    Loads a Python object from a file.

    Args:
        filepath (str): The path to the object file.

    Returns:
        object: The loaded Python object.
    """
    try:
        with open(filepath, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e