from __future__ import annotations

import importlib
import ast

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


@pytest.mark.parametrize("module", ["matplotlib", "pypdf"])
def test_base_dependency_is_importable(module: str) -> None:
    assert importlib.import_module(module) is not None
