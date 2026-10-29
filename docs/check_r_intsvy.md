# Verification — Python estimates against R's intsvy (29 Oct 2026)

The standard errors in finding_03 come from an implementation written for
this project. A plausible-looking BRR routine with a wrong divisor produces
plausible-looking wrong intervals, so the method was checked against an
independent implementation: the `intsvy` package in R, written by other
people, in another language, against the same data.

## Specification

One country, Great Britain, no fixed effects, so that both sides estimate
exactly the same model:

    PVxMATH ~ ST438Q04DA + ST438Q03DA + ESCS

Weighted by W_FSTUWT; ten plausible values; BRR over the 80 replicate
weights with a Fay factor of 0.5. The R side received the same 15,546
rows and 95 columns exported to `data/processed/gbr_for_r.csv`.

## Result

| Term       | Python estimate | intsvy | Python SE | intsvy SE |
|------------|-----------------|--------|-----------|-----------|
| Intercept  | 509.860         | 509.86 | 3.261     | 3.26      |
| ST438Q04DA |   1.147         |   1.15 | 1.223     | 1.22      |
| ST438Q03DA |  -8.081         |  -8.08 | 1.349     | 1.35      |
| ESCS       |  31.428         |  31.43 | 1.979     | 1.98      |

Agreement to two decimal places on every coefficient and every standard
error — the precision intsvy prints. intsvy additionally reports
R-squared = 0.11 (SE 0.01).

## What this does and does not establish

It establishes that the estimation machinery is correct: Rubin's rule over
ten plausible values, BRR over 80 replicate weights, the Fay factor, and
the combination of the two variance components. That machinery is shared
by every specification in this project, so the check carries over to the
pooled and categorical models, which call the same functions.

It does not establish that the specification is the right one. Both sides
computed the same model correctly; whether that model answers the research
question is a separate argument, made in decision_outcome_variable.md and
decision_index_vs_items.md.

## Practical notes for repeating this

intsvy was written for earlier PISA cycles and its defaults do not match
the 2025 file:

- The wrapper `pisa.reg.pv` takes `pvlabel` but no `config`, so it cannot
  be told about the 2025 naming. The general function `intsvy.reg.pv`
  takes `pvnames` — the explicit vector of column names — and `config`.
  Passing the ten names directly removes all guesswork about how many
  plausible values are used.
- `pisa_conf$variables$weightBRR` is `"W_"`, so the package looks for
  `W_1`...`W_80`, whereas PISA 2025 names them `W_FSTURWT1`...`W_FSTURWT80`.
  The replicate weights were renamed in R's copy of the data; the file
  itself is unchanged.
- `pisa_conf$variables$pvlabelsuff` defaults to `READ`.

The failure mode worth noting: these mismatches produced an error rather
than silently wrong numbers, which is lucky. A package that had found
columns under the names it expected would have returned a plausible
result computed on the wrong inputs.

## Consequence for the write-up

The word "provisional" can be dropped from statements about how the
standard errors are computed. It still applies to the categorical
specification, which has no standard errors yet, and to the pooled model,
which must be re-run with the full ten-PV procedure.
