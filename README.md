# AI use and skill gaps — PISA 2025

Does AI in education narrow or widen skill gaps between students? Evidence from
cross-country data on how fifteen-year-olds use AI chatbots for schoolwork, and
what that use is associated with.

**Status: work in progress.** Results are descriptive and associational. No
causal claim is made. Standard errors for the main specification are not yet
complete and have not been verified against an independent implementation.

## Data

PISA 2025 student questionnaire, public use file (OECD). Six education systems
selected on the actual coverage of the AI-use block (ST438) and the
socio-economic index: ARE, AUS, BRA, ESP, GBR, KAZ. Working sample 147,629
students.

Raw data is not in this repository — it is public and large. Download the
student questionnaire PUF from the OECD PISA 2025 database into `data/raw/`
and run the preparation cells in `notebooks/01_explore.ipynb`.

## Layout

    data/raw/        PISA source files (not tracked)
    data/processed/  working sample as pickle (not tracked)
    notebooks/       working notebook, in session order
    docs/            decisions and findings, each dated
    outputs/         figures and result tables
    src/             shared functions: weights, plausible values, BRR

`docs/` is the part worth reading first. Each file records a decision or a
finding with its justification, its date, and — for findings — an explicit
section on what the finding is *not*.

## Method

Estimation follows the OECD conventions: final student weights (`W_FSTUWT`),
ten plausible values combined by Rubin's rule, and sampling variance from the
eighty replicate weights under balanced repeated replication with a Fay factor
of 0.5. Socio-economic quintiles are computed within country. Design effects in
this sample range from 4.3 to 11.5, so conventional standard errors are not
usable here.

## AI assistance

Claude (Anthropic) was used to write and review code and to draft text. The
research question, sample, specification and interpretation are the author's,
and every reported figure is reproducible from the notebook cell recorded in
`docs/`.

## Author

Daria Storozhkova
