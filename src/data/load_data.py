"""
Module with functions to load data. 
"""
# import installed dependencies
# -----------------------------------------------------------------------------
import os 
import pandas as pd
from dataclasses import dataclass

ROOT_DIR = os.path.abspath("../data")

@dataclass()
class Data():
    root: str 
    state: str
    kind: str
    path: str
    name: str
    data: pd.DataFrame
    
    @staticmethod
    def build_path(
        state: str, 
        kind: str, 
        name: str
        ) -> str:
        """builds a path to a file from the arguments.

        Args:
            state (str): e.g., "raw", "processed", or otherwise
            kind (str): what subdirectory? e.g., "catalogs" 
            name (str): name of the file plus extension e.g., "data.csv"

        Returns:
            str: the path to the file
        """
        return os.path.join(ROOT_DIR, state, kind, name)

    @classmethod
    def load_file(
        cls, 
        state: str, 
        kind: str, 
        name: str,
        func: callable = pd.read_csv,
        **kwargs: dict
        ):
        """Loads file and builds dataclass from single function call.

        Args:
            state (str): e.g., "raw", "processed", or otherwise
            kind (str): what subdirectory? e.g., "catalogs" 
            name (str): name of the file plus extension e.g., "data.csv"
            func (callable): the function to read the file, default is 
                pandas.read_csv
            **kwargs (dict): keyword arguments to pass to func.

        Returns:
            Instance of the Data class with loaded data file.
        """
        path = Data.build_path(state, kind, name)
        return cls(
            root = ROOT_DIR, 
            state = state, 
            kind = kind, 
            name = name,
            path = path, 
            data = func(path, **kwargs)
            )