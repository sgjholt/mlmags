"""mw_corrections contains functions to correct raw data to moment magnitude.
"""
import numpy as np
import pandas as pd
from typing import Tuple 
from copy import deepcopy
from ..data.utils import get_source_params


def get_mo(
    slpsps: np.ndarray, 
    vel: float = 3736.9, 
    rad_coef: float = 0.55, 
    FS: float = 2, 
    eta: float = 1, 
    rho: float = 2800, 
    ro: float = 1000
) -> np.ndarray:
    """Computes the seismic moment for a long period spectral level corrected 
    for geometric spreading (and anelastic attenuation if necessary).

    Args:
        slpsps (np.ndarray): Station long period spectral level (m / Hz)
        vel (float, optional): [description]. Defaults to 3736.9.
        rad_coef (float, optional): [description]. Defaults to 0.55.
        FS (float, optional): [description]. Defaults to 2.
        eta (float, optional): [description]. Defaults to 1.
        rho (float, optional): [description]. Defaults to 2800.
        ro (float, optional): [description]. Defaults to 1000.

    Returns:
        np.ndarray: Array of seismic moment estimates for each station.
    """
    return (slpsps * np.pi * 4 * rho * (vel**3) * ro) / (rad_coef * FS * eta)


def get_mw(mo: np.ndarray) -> np.ndarray:
    """Computes the Hanks & Kanamori (198X) definition of Mw which 
    is corrected to accept sesimic moment (mo) in SI units of Nm.  

    Args:
        mo (np.ndarray): [description]

    Returns:
        np.ndarray: [description]
    """
    return (2/3) * np.log10(mo) - 6.0333


def get_geo_four(
    coeffs: np.ndarray, 
    d: np.ndarray, 
    R: np.ndarray
) -> np.ndarray:
    """[summary]

    Args:
        coeffs (np.ndarray): [description]
        d (np.ndarray): [description]
        R (np.ndarray): [description]

    Returns:
        np.ndarray: [description]
    """
    R0 = np.where(R <= d[0])
    R1 = np.where((R > d[0])&(R <= d[1]))
    R2 = np.where((R > d[1])&(R <= d[2]))
    R3 = np.where((R > d[2]))
    
    amp = np.zeros(len(R))
    
    amp[R0] += coeffs[0] * np.log10(R[R0])
    
    amp[R1] += (coeffs[0] * np.log10(d[0]) + coeffs[1] * np.log10(R[R1] / d[0]))
    
    amp[R2] += (coeffs[0] * np.log10(d[0]) + coeffs[1] * np.log10(d[1] / d[0])) + \
               (coeffs[2] * np.log10(R[R2] / d[1]))
    
    amp[R3] += (coeffs[0] * np.log10(d[0]) + coeffs[1] * np.log10(d[1] / d[0])) + \
               (coeffs[2] * np.log10(d[2] / d[1])) + (coeffs[3] * np.log10(R[R3] / d[2]))

    return amp


def compute_holt19_mo_and_mw(
    df: pd.DataFrame, phase: str, coeffs: dict, velocity_model: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
    """[summary]

    Args:
        df (pd.DataFrame): [description]
        phase (str): [description]
        coeffs (dict): [description]
        velocity_model (np.ndarray): [description]

    Returns:
        Tuple[np.ndarray, np.ndarray]: [description]
    """
    df = df.copy(deep=True)
    coeffs = deepcopy(coeffs[phase])
    # get the approproate distance corrections from Holt (2019) model
    df["holt-19-dist-corr"] = get_geo_four(
        (0.9, 2.57, 0.44, 1.54), # coefficients 
        (43, 76, 136), # break points
        df['rhyp'].values # actual hypocentral distances
    )
    # correct log-long period spectral levels for app. geo. spreading
    df["holt-19-source-llpsp"] = (
        df["llpsp"] + df["holt-19-dist-corr"]
        ).values
    # assign the correct source properties to coeffs dict
    vel, rho = get_source_params(velocity_model, df["dep"], phase)
    
    coeffs['vel'] = vel * 1000
    coeffs['rho'] = rho * 1000
    # save back to DataFrame for validation
    df[f"source-vel-{phase}g"] = coeffs['vel']  
    df[f"source-density"] = coeffs['rho']
    # compute seismic moment (mo) using Brune's (1970) model
    df[f"holt-19-station-{phase}g-M0"] = get_mo(10**df["holt-19-source-llpsp"], **coeffs)
    df[f"holt-19-station-{phase}g-Mw"] = get_mw(df[f"holt-19-station-{phase}g-M0"].values)
    
    return df
