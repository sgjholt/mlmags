"""utils for data cleansing.
"""

import numpy as np
import pandas as pd
from typing import Tuple 


def load_vel_mod(path) -> np.ndarray:
    """[summary]

    Args:
        path ([type]): [description]

    Returns:
        np.ndarray: [description]
    """
    return np.loadtxt(path, skiprows=1)


def get_source_params(
    vel_model: np.ndarray, depth: np.ndarray, phase: str
    ) -> Tuple[np.ndarray, np.ndarray]:
    """[summary]

    Args:
        vel_model (np.ndarray): [description]
        depth (np.ndarray): [description]
        phase (str): [description]

    Raises:
        ValueError: [description]

    Returns:
        Tuple[np.ndarray, np.ndarray]: [description]
    """
    vels = None
    if phase.upper() == "P":
        vels = np.interp(depth, vel_model[:, 0], vel_model[:, 1])
    if phase.upper() == "S":
        vels = np.interp(depth, vel_model[:, 0], vel_model[:, 2])
    if vels is None:    
        raise ValueError("Invalid phase given, choose P or S")
    dens = np.interp(depth, vel_model[:, 0], vel_model[:, 3])
    return vels, dens