# Finding 03 — modes of AI use and mathematics performance (27 Oct 2026)

## Specification

Weighted least squares on the pooled six-country sample, country fixed
effects, ESCS as a control, both modes of use entered jointly:

    PVxMATH ~ ST438Q04DA + ST438Q03DA + ESCS + C(CNT)

weighted by W_FSTUWT. Estimation sample: 123,554 of 147,629 students
(listwise deletion on the variables above).

ST438Q04DA is "To help me learn"; ST438Q03DA is "To draft texts for
writing assignments". Both are five-point frequency scales:
1 never or almost never, 2 about once or twice a year, 3 about once or
twice a month, 4 about once or twice a week, 5 every day or almost
every day.

## Result 1 — linear specification, averaged over ten plausible values

| Variable                    | Coefficient (points) |
|-----------------------------|----------------------|
| Help me learn (per step)    |  +8.02               |
| Draft my writing (per step) | -10.04               |
| ESCS (per SD)               | +28.89               |

Estimates are stable across the ten plausible values: the learning
coefficient ranges 7.81 to 8.21, drafting -10.26 to -9.88, ESCS 28.82
to 29.00. Imputation variance is therefore negligible relative to the
sampling variance still to be estimated.

The ESCS coefficient is consistent with the established PISA literature
(roughly 30-40 points per standard deviation), which is a sanity check
on the weighting and the specification rather than a result.

Source: outputs/pv_coefficients_math.csv

## Result 2 — categorical specification (PV1 only)

Each level relative to "never or almost never", holding country, ESCS
and the other mode of use constant:

| Level                  | Help me learn | Draft my writing |
|------------------------|---------------|------------------|
| 2 once or twice a year |  -8.0         | -17.6            |
| 3 once or twice a month| +14.0         | -24.9            |
| 4 once or twice a week | +24.5         | -31.2            |
| 5 (almost) every day   | +24.4         | -38.1            |

Two shapes, and neither is a straight line.

Learning use is J-shaped with saturation. Students who use AI to learn
once or twice a year score *below* those who never use it. The
association turns positive at monthly use and increases to weekly, after
which it is flat: levels 4 and 5 are indistinguishable at +24.5 and
+24.4.

Drafting declines monotonically, but the first step is the largest by
far: -17.6 points between never and once-or-twice-a-year, then roughly
-7 per further step. The distinction that matters is between never and
ever, not between occasional and frequent.

Source: outputs/coefs_levels_math_pv1.csv

## Decision — the categorical specification becomes the main one

Not because it fits better, but because the instrument does not support
a linear reading. In events per year the five levels are approximately
0, 1.5, 18, 78 and 300. The step from level 1 to level 2 and the step
from level 4 to level 5 are quantitatively incomparable, so a model that
constrains them to the same coefficient is misspecified by construction.
The linear specification is retained as a robustness check.

## What this is NOT

- **Not causal.** The reverse reading is equally consistent with the
  data: weaker students outsource written work *because* they are
  struggling, stronger students ask for explanations *because* they are
  coping. A single cross-section cannot separate the two. The text must
  say association, never effect.
- **Not statistically tested.** No standard errors have been computed.
  The standard errors reported by statsmodels are wrong here: it treats
  W_FSTUWT as a precision weight rather than a sampling design weight,
  and the design is clustered by school. BRR with the 80 replicate
  weights and a Fay factor of 0.5 is still to be done. Until then the
  word "significant" does not appear anywhere, and the -8.0 dip at level
  2 cannot be claimed to differ from zero.
- **Result 2 uses PV1 only.** Final figures require the ten-PV wrapper
  used in Result 1.
- **Self-reported frequency.** Willingness to admit outsourcing written
  work may itself vary by country and by socio-economic status, which
  would bias the drafting coefficient in an unknown direction.
- **Six countries, not the world.** ARE, ESP, AUS, BRA, KAZ, GBR, chosen
  on coverage. See country_selection.md.
- **School effects not separated.** Country fixed effects absorb system-
  level differences but not school-level ones. Whether the gradient is
  about families or about schools requires CNTSCHID fixed effects, and
  the two cases imply different policy recommendations.

## Next

1. Ten-PV wrapper for the categorical specification.
2. BRR standard errors; then a coefficient plot with intervals.
3. Cross-check one country against R's intsvy.
4. School fixed effects as robustness.

## Appendix — one plausible value versus ten

| Coefficient | PV1    | Ten PV  | Difference | SD across PV | Imputation SE |
|-------------|--------|---------|------------|--------------|---------------|
| Learn       |   8.14 |   8.022 | +0.118     | 0.126        | 0.132         |
| Draft       | -10.05 | -10.043 | -0.007     | 0.113        | 0.118         |
| ESCS        |  28.84 |  28.892 | -0.052     | 0.068        | 0.072         |

The last column is the imputation component of the standard error,
sqrt((1 + 1/10) * Var_between), i.e. the second term of Rubin's rule.

Point estimates from a single plausible value are off by at most 0.12
points, which is negligible against a coefficient of 8. A single PV is
therefore acceptable for exploratory work.

The reason ten are required is the second term. One plausible value
yields no estimate of imputation variance at all, so an interval built
on it omits a component of uncertainty entirely and is narrower than it
should be. The sampling component, which BRR estimates from the 80
replicate weights, is still to be added; the two are then summed.

## Standard errors — BRR on PV1 (27 Oct 2026)

Sampling variance from the 80 replicate weights with a Fay factor of
0.5, combined with the imputation term from the appendix above.
Estimation sample 123,554.

| Coefficient | Estimate | SE sampling | SE imputation | SE total | t     | 95% CI           |
|-------------|----------|-------------|---------------|----------|-------|------------------|
| Learn       |   8.023  | 0.406       | 0.132         | 0.427    |  18.8 | [ 7.19,  8.86]   |
| Draft       | -10.043  | 0.449       | 0.119         | 0.464    | -21.6 | [-10.95, -9.13]  |
| ESCS        |  28.894  | 0.723       | 0.073         | 0.727    |  39.7 | [27.47, 30.32]   |

Variances add; standard errors do not.

## Design effects

| Coefficient | Naive SE | BRR SE | Design effect |
|-------------|----------|--------|---------------|
| Learn       | 0.196    | 0.406  |  4.30         |
| Draft       | 0.198    | 0.449  |  5.12         |
| ESCS        | 0.213    | 0.723  | 11.53         |

The naive standard errors understate variance by a factor of four to
eleven, i.e. intervals by two to three and a half. The design effect is
largest for ESCS because socio-economic status varies mainly *between*
schools - schools are socially segregated - while the frequency of AI
use also varies within them.

With n = 123,554 statistical significance is cheap and is not itself a
result. What carries content is the magnitude and the shape of the
association, and the fact that the two modes of use point in opposite
directions.

## Outstanding on the standard errors

- The figures above use BRR on PV1 only. The complete procedure, which
  averages the BRR variance across all ten plausible values, is now
  implemented as `brr_pv` in `src/pisa_tools.py`; the pooled model still
  has to be re-run with it.
- The categorical specification has no standard errors yet.
- The estimation machinery is verified. R's intsvy reproduces every
  coefficient and every standard error to two decimal places on GBR
  (29 Oct 2026, `docs/check_r_intsvy.md`). This verifies how the numbers
  are computed, not that the specification is the right one.

Source: outputs/brr_se_math_pv1.csv
