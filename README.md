# PV-battery-hydrogen microgrid wear-accounting reporting package

This private, submission-staging repository reproduces the curated reporting
layer and manuscript derivatives for one fixed PV-rich
PV--battery--PEMEL--tank--PEMFC case. It regenerates Main Tables 3--4 and Main
Figures 2--4 from released derivative evidence with one reporting-only
command.

It does **not** contain or regenerate the unavailable original 27-file annual
campaign. It does not run an optimizer, solver, plant simulation, sensitivity,
holdout, or annual campaign. The results are physically replayed trajectories
accepted by the disclosed architecture, not certificates of local or global
optimality.

The package includes the exact Alexandria PVGIS TMY response used in the
study. Redistribution is permitted by the source usage conditions, but the
file remains third-party material and is excluded from the author licenses.
See `THIRD_PARTY_NOTICES.md` and `WEATHER_RETRIEVAL.md`.

## Quick start

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m src.reproduce_manuscript_artifacts --output reproduced
```

On POSIX systems, replace `.venv\Scripts\python` with `.venv/bin/python`.

Original code is licensed under MIT. Original author-created documentation
and evidence are licensed under CC BY 4.0. The detailed boundaries and
third-party exclusions are in `LICENSE_SCOPE.md`.
