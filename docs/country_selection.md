# Country selection — PISA 2025

Final sample: ARE, ESP, AUS, BRA, KAZ, GBR

| Country | n | ST438 coverage | IC170 coverage | ESCS coverage |
|---|---|---|---|---|
| ARE | 34,639 | 0.90 | 0.81 | 0.91 |
| BRA | 30,140 | 0.80 | 0.00 | 0.91 |
| ESP | 29,966 | 0.88 | 0.79 | 0.95 |
| KAZ | 22,680 | 0.92 | 0.00 | 0.93 |
| GBR | 15,546 | 0.87 | 0.17 | 0.90 |
| AUS | 14,658 | 0.93 | 0.89 | 0.95 |

Rationale: six world regions (Gulf, Southern Europe, Oceania,
Latin America, Central Asia, North-Western Europe); all six have
ST438 coverage above 0.80 and ESCS above 0.90.

Main specification uses ST438 (how AI is used) and ESCS.
IC170 (school vs home use) is available only in ARE, ESP and AUS,
so it is used for robustness on a sub-sample, never in the main model.

Excluded: USA (ST438 0.51, ESCS 0.55 — coverage too low to include).
Canada dropped in favour of Australia (ST438 0.77 vs 0.93, no ICT block).
