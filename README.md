# PV-battery-hydrogen microgrid wear-accounting reporting package

This archived submission release reproduces the curated reporting layer for
one fixed, intentionally PV-rich PV--battery--PEMEL--tank--PEMFC case. It does
not rerun the annual optimization campaign or claim broader sizing, weather,
tariff, price, or technology robustness.

The three reported policies are:

- **C1:** direct operating economics;
- **C2:** degradation-aware operation with zero carbon price;
- **C3:** the C2 formulation with a 50 USD/tCO2 grid-import carbon price.

Common wear is an ex-post, non-cash physical proxy based on a common
CAPEX-fraction valuation of battery, PEMEL, and PEMFC state consumption. Direct
balance plus common wear is a comparative diagnostic, not an audited lifecycle
cashflow. The annual trajectories were accepted by the disclosed candidate
architecture; local and global optimality are not established.

The package regenerates Main Tables 3--4 and source data for Main Figures
2--4 from released derivative evidence. Figure 4 uses the corrected 0.19
V/cell PEMEL end-of-life basis and validates all three terminal values. The
unavailable historical raw 27-file annual campaign is neither included nor
claimed to be available.

## Quick start

```text
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m src.reproduce_manuscript_artifacts --output reproduced
```

On POSIX systems, replace `.venv\Scripts\python` with `.venv/bin/python`.
The final command produces the two tables, Figure 2--4 source CSVs, reporting
PDFs, and `REPRODUCTION_CHECK.json`. It calls no solver, optimizer, plant
simulation, sensitivity, holdout, or annual campaign.

## Data and licensing

The included Alexandria PVGIS TMY response is third-party material governed
by the European Commission PVGIS usage conditions. See
`THIRD_PARTY_NOTICES.md`, `WEATHER_RETRIEVAL.md`, and
`INPUT_DATA_PROVENANCE.md`.

Original code is licensed under MIT. Original author-created documentation,
curated evidence, and manuscript-derivative assets are licensed under CC BY
4.0, subject to the exclusions in `LICENSE_SCOPE.md`.

Release record:
`https://github.com/momen-raslan/pv-battery-hydrogen-microgrid-wear-accounting/releases/tag/v1.0.0-submission`
