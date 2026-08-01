# Reproduction instructions

Use Python 3.11 or newer from the repository root:

```text
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m src.reproduce_manuscript_artifacts --output reproduced
```

The final command writes:

- `MAIN_TABLE_3.csv`;
- `MAIN_TABLE_4.csv`;
- numerical source CSVs for Main Figures 2--4;
- vector PDFs for Main Figures 2--4;
- `REPRODUCTION_CHECK.json`.

Tables are compared by exact formatted-string equality. Figure 2 source
values use an absolute tolerance of `5e-9`; Figure 3 source values use
`5e-6 USD`, reflecting serialization precision in the sealed source CSV.
Figure 4 is compared exactly with the released 26,280-row reference CSV. The
same check reads that CSV and verifies the corrected PEMEL endpoints C1 =
0.8475178671, C2 = 0.9771844256, and C3 = 0.9771773221 on the 0.19 V/cell
basis. The command exits nonzero on any failed check.

The original 27-file raw annual campaign is not included and was unavailable
when this reporting package was prepared. This command reproduces only the
curated reporting layer and manuscript derivatives. It calls no solver,
optimizer, simulation, sensitivity, holdout, or annual campaign.
