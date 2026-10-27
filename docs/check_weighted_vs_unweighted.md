# Methods check — weights, levels and slopes (27 Oct 2026)

Single-country check on GBR (n = 15,546 before listwise deletion),
comparing W_FSTUWT-weighted estimates with unweighted ones.

## Levels

| Quantity                    | Weighted | Unweighted | Difference |
|-----------------------------|----------|------------|------------|
| Draft my writing (1-5)      |   2.07   |   2.09     | -0.02      |
| Help me learn (1-5)         |   2.57   |   2.64     | -0.07      |
| Mathematics (mean of 10 PV) | 487.57   | 478.07     | +9.51      |

## Slopes

Model: PV1MATH ~ ST438Q04DA + ST438Q03DA + ESCS, GBR only.

| Term             | Weighted | Unweighted | Difference |
|------------------|----------|------------|------------|
| Intercept        | 510.20   | 501.13     | +9.07      |
| Help me learn    |   1.72   |   1.12     | +0.60      |
| Draft my writing |  -8.97   |  -9.49     | +0.52      |
| ESCS             |  30.94   |  31.08     | -0.14      |

## Reading

Weighting moves the *level* of achievement by 9.5 points - about a third
of an ESCS standard deviation - because the sample over-represents
students in smaller and rarer schools, which score lower. It barely
moves the frequency means, which sit on a 1-5 scale.

Slopes are almost unaffected. The selection distortion acts on the whole
relationship roughly uniformly, so its angle survives.

Two consequences:

1. The descriptive findings (finding_01, finding_02) genuinely required
   weights; unweighted versions of them were wrong and were rewritten.
2. Regression coefficients change little, but must still be weighted.
   The estimand is a population quantity; an unweighted coefficient
   estimates a different quantity, it is not an approximation to ours.

## What this check does NOT address

Standard errors. Weights barely moved the point estimates, but the
uncertainty around them is driven by the sampling design - students were
drawn as whole schools, not independently. In PISA this typically
inflates intervals by a factor of two to three. BRR with the 80
replicate weights is what estimates it, and nothing here substitutes
for it.

## Incidental

In GBR alone the learning-use coefficient is +1.72, against +8.02 pooled
across the six countries. Country heterogeneity is substantial, so
country-by-country estimates belong in the specification rather than in
an appendix.
