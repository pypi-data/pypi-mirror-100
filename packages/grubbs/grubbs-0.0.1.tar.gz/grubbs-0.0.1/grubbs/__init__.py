"""Grubbs test for outliers. See https://en.wikipedia.org/wiki/Grubbs%27s_test
"""

from __future__ import annotations

import warnings
from typing import TypedDict, Union

import numpy as np
from numpy.typing import ArrayLike  # pylint: disable=no-name-in-module,import-error
from scipy.stats import t as t_distribution

MIN_OBS = 6  # Grubbs test not recomended for 6 observations or fewer


class GrubbsResults(TypedDict): # pylint: disable=too-few-public-methods
    """Results of the Grubbs tests."""

    index: int
    statistic: float
    pvalue: float


def grubbs(arr: Union[list, np.ndarray], alternative="two-sided") -> GrubbsResults:
    """Run Grubbs test

    Args:
        arr (ArrayLike): Sample to test for outliers
        alternative (str, optional): Specify "two-sided" alternative, "min" to
            test if the minimum observation is an outlier, "max" to test if
            the maximum observation is an outlier. Defaults to "two-sided".

    Raises:
        ValueError: `alternative` must be "two-sided", "min", or "max".

    Returns:
        GrubbsResults: Dictionary containing the index of the outlier, Grubbs
        statistic, and p-value.

    Notes:
        The p-value is corrected for multiple hypothesis tests, which may lead
        to p-values > 1.
    """
    if alternative not in ("two-sided", "min", "max"):
        raise ValueError("alternative must be one of 'two-sided', 'min', 'max'")
    n_obs = len(arr)  # type: ignore
    if n_obs <= MIN_OBS:
        warnings.warn(
            f"Grubbs test is not recommended for fewer than {MIN_OBS} observations",
            RuntimeWarning,
        )
    min_idx = np.argmin(arr)
    max_idx = np.argmax(arr)
    y_min, y_max, y_mean = arr[min_idx], arr[max_idx], np.mean(arr)  # type: ignore
    y_min = np.min(arr)
    y_max = np.max(arr)
    y_std = np.std(arr, ddof=1)
    if alternative == "two-sided":
        idx = max_idx if y_max - y_mean > y_mean - y_min else min_idx
        grubbs_stat = max(y_max - y_mean, y_mean - y_min) / y_std
        omega = 2 * n_obs
    elif alternative == "min":
        idx = min_idx
        grubbs_stat = (y_mean - y_min) / y_std
        omega = n_obs
    else:
        idx = max_idx
        grubbs_stat = (y_max - y_mean) / y_std
        omega = n_obs
    t_stat = grubbs_stat * np.sqrt(
        (n_obs * (n_obs - 2)) / ((n_obs - 1) ** 2 - n_obs * grubbs_stat ** 2)
    )
    p_value = omega * (1 - t_distribution(n_obs - 2).cdf(t_stat))
    return {"index": int(idx), "statistic": grubbs_stat, "pvalue": p_value}


def detect_outliers(
    arr: Union[list, np.ndarray], alternative="two-sided", alpha=0.05
) -> list[GrubbsResults]:  # pylint: disable=unsubscriptable-object
    """Recursively detect outliers using Grubbs test.

    Args:
        arr (ArrayLike): Sample to test for outliers.
        alternative (str, optional): See `grubbs`. Defaults to "two-sided".
        alpha (float, optional): Significance threshold. Defaults to 0.05.

    Returns:
        list[GrubbsResults]: Grubbs results for all outliers detected.
    """
    outliers = []
    grubbs_results = grubbs(arr, alternative=alternative)
    while grubbs_results["pvalue"] < alpha and len(arr) > MIN_OBS:  # type: ignore
        outliers.append(grubbs_results)
        arr = np.delete(arr, grubbs_results["index"])
        grubbs_results = grubbs(arr, alternative=alternative)
    return outliers
