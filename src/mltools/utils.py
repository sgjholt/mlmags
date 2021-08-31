"""[summary]
"""

import numpy as np
from typing import Tuple

def event_train_test_split(
    evs: np.ndarray, n_evs: int, train_split: float, random_seed: int=1
    ) -> Tuple[np.ndarray, np.ndarray]:
    """[summary]

    Args:
        n_evs (int): [description]
        train_split (float): [description]
        random_seed (int, optional): [description]. Defaults to 1.

    Returns:
        Tuple[np.ndarray, np.ndarray]: [description]
    """
    # some basic checks
    assert 0 < train_split < 1, "Variable train_split (ts) must be 0<ts<1."
    assert n_evs > 1, "Need more than 1 event to split."
    # set the random state locally
    r = np.random.RandomState(random_seed)
    # compute the number of test and train samples
    train_samples = int(np.round(train_split * n_evs, 0))
    test_samples = int(n_evs - train_samples)
    # split the events
    train_events = r.choice(evs, train_samples, replace=False)
    test_events = evs[~np.isin(evs, train_events)]
    # make sure they add up to the total number!
    assert len(train_events) + len(test_events) == n_evs

    return train_events, test_events