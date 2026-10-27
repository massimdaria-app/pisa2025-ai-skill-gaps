"""Shared helpers for the PISA 2025 AI-use project.

Use from a notebook in notebooks/:

    import sys; sys.path.append("../src")
    from pisa_tools import load_sample, wmean, fit_pv, SIX, ST438

Everything here is weighted by default. Unweighted figures are a
diagnostic only and never go into docs/ (see finding_02, finding_03).
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "data" / "processed" / "pisa2025_six.pkl"

SIX = ["ARE", "ESP", "AUS", "BRA", "KAZ", "GBR"]

ST438 = ["ST438Q01DA", "ST438Q02DA", "ST438Q03DA", "ST438Q04DA"]
ST438_LABELS = {
    "ST438Q01DA": "Summarise a text",
    "ST438Q02DA": "Preliminary research",
    "ST438Q03DA": "Draft my writing",
    "ST438Q04DA": "Help me learn",
}

# 1 never or almost never / 2 once or twice a year / 3 once or twice a
# month / 4 once or twice a week / 5 every day or almost every day.
# Codes 95-99 are missing and must already be cleared in the sample.
FREQ_LABELS = {
    1: "Never or almost never",
    2: "About once or twice a year",
    3: "About once or twice a month",
    4: "About once or twice a week",
    5: "Every day or almost every day",
}

WEIGHT = "W_FSTUWT"
REPLICATE_WEIGHTS = [f"W_FSTURWT{i}" for i in range(1, 81)]
FAY = 0.5


def load_sample(path=SAMPLE):
    """Load the six-country working sample (147,629 x 141)."""
    return pd.read_pickle(path)


def wmean(g, var, w=WEIGHT):
    """Weighted mean of `var`, dropping rows missing the value or the weight."""
    d = g[[var, w]].dropna()
    return np.average(d[var], weights=d[w])


def pv_names(domain="MATH"):
    """The ten plausible-value column names for a domain."""
    return [f"PV{i}{domain}" for i in range(1, 11)]


def _formula_columns(formula, df):
    """Column names of `df` that appear in `formula`."""
    tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", formula))
    return [c for c in df.columns if c in tokens]


def fit_one(df, formula, weight=WEIGHT):
    """One weighted least-squares fit, listwise deletion on the terms used."""
    need = _formula_columns(formula, df) + [weight]
    d = df.dropna(subset=need)
    return smf.wls(formula, data=d, weights=d[weight]).fit(), len(d)


def fit_pv(df, rhs, domain="MATH", weight=WEIGHT):
    """Fit `PVxDOMAIN ~ rhs` on each of the ten plausible values.

    Returns (table, point) where `table` has one row per plausible value
    and `point` is the mean across them: Rubin's point estimate. The
    standard errors reported by statsmodels are NOT valid here - the
    sampling design is clustered by school, and uncertainty must come
    from the 80 replicate weights with a Fay factor of 0.5.
    """
    rows = []
    for v in pv_names(domain):
        formula = f"{v} ~ {rhs}"
        m, n = fit_one(df, formula, weight=weight)
        row = {"pv": v, "n": n}
        row.update(m.params.to_dict())
        rows.append(row)

    table = pd.DataFrame(rows)
    point = table.drop(columns=["pv", "n"]).mean()
    return table, point


def brr_se(df, formula, weight=WEIGHT, replicates=REPLICATE_WEIGHTS, fay=FAY):
    """Sampling standard errors from the 80 replicate weights.

    Refits `formula` once with the full-sample weight and once per
    replicate weight, then applies the Fay correction:

        Var = sum((theta_r - theta)^2) / (G * (1 - fay)^2)

    Returns (theta, se, n). The design matrix is built once and reused,
    which is what makes 81 fits take seconds rather than minutes.
    """
    need = _formula_columns(formula, df) + [weight] + list(replicates)
    d = df.dropna(subset=need)

    m0 = smf.wls(formula, data=d, weights=d[weight]).fit()
    y, X, names = m0.model.endog, m0.model.exog, m0.model.exog_names
    theta = pd.Series(m0.params, index=names)

    reps = pd.DataFrame(
        [sm.WLS(y, X, weights=d[w].to_numpy()).fit().params for w in replicates],
        columns=names,
    )
    var = ((reps - theta) ** 2).sum() / (len(replicates) * (1 - fay) ** 2)
    return theta, np.sqrt(var), len(d)


def imputation_se(table, m=10):
    """Rubin's second term from a fit_pv() table: sqrt((1 + 1/m) * Var_between)."""
    between = table.drop(columns=["pv", "n"]).var(ddof=1)
    return np.sqrt((1 + 1 / m) * between)


def total_se(sampling_se, imputation_se):
    """Variances add, standard errors do not."""
    return np.sqrt(sampling_se ** 2 + imputation_se ** 2)
