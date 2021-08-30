"""utils for data cleansing.
"""

import pandas as pd

def col_to_dt(df: pd.DataFrame, name: str):
    """[summary]

    Args:
        df (pd.DataFrame): [description]
        name (str): [description]
    """
    df[name] = pd.to_datetime(df[name].values, unit='ns', utc=True)


def clean_mag_table(df: pd.DataFrame, min_nsta: int, max_std_err: float) -> pd.DataFrame:
    """[summary]

    Args:
        df (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
    """
    conds = (df["Mw-Nobs"] >= min_nsta) & (df["Mw-std-err"] <= max_std_err)
    mag_table = df[conds].copy(deep=True).rename(columns={"UTC": "otime"})
    col_to_dt(mag_table, 'otime')
    return mag_table

def clean_fit_table(df: pd.DataFrame, min_dep: float, max_fc: float) -> pd.DataFrame:
    """[summary]

    Args:
        df (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
    """
    conds = (df["dep"] >= min_dep & df["fc"] <= max_fc)
    fit_table = df[conds].copy(deep=True)
    col_to_dt(fit_table, 'otime')
    return fit_table
