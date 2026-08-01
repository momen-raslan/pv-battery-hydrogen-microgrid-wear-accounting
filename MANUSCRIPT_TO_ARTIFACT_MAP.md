# Manuscript-to-artifact map

- Main Tables 3--4: `evidence/AUTHORITATIVE_METRIC_DICTIONARY.json` and
  `evidence/DIRECT_LEDGER_RECONCILIATION.csv`.
- Main Figure 2: the same metric dictionary, checked against
  `reference/FIGURE_2_ANNUAL_REGIMES.csv`.
- Main Figure 3: the direct and common-wear components in the same metric
  dictionary, checked against `reference/FIGURE_3_RANKING_REVERSAL.csv`.
- Main Figure 4: `evidence/PEMEL_SOH_REPORTING_CORRECTION.csv`, checked exactly
  against `reference/FIGURE_4_HOURLY_SOH.csv`, including all three corrected
  PEMEL endpoints.
- Hydrogen-shortage statements: `evidence/HYDROGEN_SHORTAGE_RECONCILIATION.csv`.
- Common-wear crossover: `evidence/COMMON_WEAR_CROSSOVER_CHECK.csv`.
- Residual threshold table:
  `evidence/SUPPLEMENTARY_RESIDUAL_THRESHOLD_TABLE.csv`.
- Literature and model disclosure:
  `evidence/LITERATURE_VERIFICATION_MATRIX.csv` and
  `evidence/MODEL_AND_PARAMETER_DISCLOSURE_CHECK.csv`.

Run `python -m src.reproduce_manuscript_artifacts --output reproduced` to
regenerate the two main tables and three main figures and produce the
machine-readable numerical comparison report.
