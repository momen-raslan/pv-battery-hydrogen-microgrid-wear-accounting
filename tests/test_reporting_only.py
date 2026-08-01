from __future__ import annotations

import importlib
import ast
import csv
from pathlib import Path

import pytest

from src import reporting_only
from src import reproduce_manuscript_artifacts


def test_pemel_reporting_denominator_is_0p19_volt_per_cell() -> None:
    assert reporting_only.PEMEL_EOL_VOLTAGE_RISE_PER_CELL_V == pytest.approx(0.19)
    assert reporting_only.reporting_pemel_soh(0.0) == pytest.approx(1.0)
    assert reporting_only.reporting_pemel_soh(1.9) == pytest.approx(0.9)
    assert reporting_only.reporting_pemel_soh(19.0) == pytest.approx(0.0)


def test_reporting_module_has_no_solver_or_simulator_import() -> None:
    tree = ast.parse(
        reproduce_manuscript_artifacts.Path(
            reproduce_manuscript_artifacts.__file__
        ).read_text(encoding="utf-8")
    )
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    forbidden = {"gurobipy", "pyomo", "optimizer_mpc", "main_simulation"}
    assert forbidden.isdisjoint(imported)


def test_corrected_figure_4_source_has_all_rows_and_pemel_endpoints() -> None:
    source = Path(__file__).resolve().parents[1] / "reference" / "FIGURE_4_HOURLY_SOH.csv"
    with source.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 26280
    for policy, expected in reproduce_manuscript_artifacts.EXPECTED_PEMEL_ENDPOINTS.items():
        subset = [row for row in rows if row["policy"] == policy]
        assert [int(row["hour"]) for row in subset] == list(range(8760))
        assert float(subset[-1]["pemel_soh"]) == pytest.approx(expected, abs=5e-11)


@pytest.mark.parametrize("module", ["matplotlib", "pypdf"])
def test_base_dependency_is_importable(module: str) -> None:
    assert importlib.import_module(module) is not None
