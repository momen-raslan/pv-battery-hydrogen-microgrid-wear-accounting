"""Reproduce Main Tables 3-4 and Main Figures 2-4 from derivative evidence.

This module deliberately has no optimizer, solver, plant, campaign, or
simulation import. The command consumes only the curated derivative evidence
shipped in this repository and verifies the regenerated numerical sources
against the sealed reference sources.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pypdf import PdfReader


POLICIES = ("C1", "C2", "C3")
COLORS = {"C1": "#1f4e79", "C2": "#2e8b57", "C3": "#b35c00"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_inputs(root: Path) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]]]:
    metric = json.loads(
        (root / "evidence" / "AUTHORITATIVE_METRIC_DICTIONARY.json").read_text(
            encoding="utf-8"
        )
    )
    ledger = read_csv(root / "evidence" / "DIRECT_LEDGER_RECONCILIATION.csv")
    soh = read_csv(root / "evidence" / "PEMEL_SOH_REPORTING_CORRECTION.csv")
    return metric, ledger, soh


def table_3(metric: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for policy in POLICIES:
        p = metric["policies"][policy]
        pemfc_mwh = p["pemfc_electricity_kWh"] / 1000.0
        rows.append(
            {
                "Case": policy,
                "Import_MWh": f"{p['grid_import_kWh'] / 1000.0:.1f}",
                "Export_MWh": f"{p['grid_export_kWh'] / 1000.0:.1f}",
                "Battery_throughput_MWh": f"{p['battery_throughput_kWh'] / 1000.0:.1f}",
                "PEMEL_MWh": f"{p['pemel_electricity_kWh'] / 1000.0:.1f}",
                "PEMFC_MWh": (
                    f"{pemfc_mwh:.1f}" if policy == "C1" else f"{pemfc_mwh:.2e}"
                ),
                "H2_produced_kg": f"{p['h2_produced_kg']:.1f}",
                "H2_sold_kg": f"{p['h2_sold_kg']:.1f}",
                "Grid_import_CO2_t": f"{p['total_emissions_tonnes']:.4f}",
                "Battery_SoH_final": f"{p['final_battery_soh']:.4f}",
                "PEMEL_SoH_final": f"{p['final_pemel_soh_corrected_0p19']:.4f}",
                "PEMFC_SoH_final": f"{p['final_pemfc_soh']:.4f}",
            }
        )
    return rows


def table_4(metric: dict[str, Any], ledger: list[dict[str, str]]) -> list[dict[str, str]]:
    ledger_by_policy = {row["policy"]: row for row in ledger}
    rows: list[dict[str, str]] = []
    for policy in POLICIES:
        p = metric["policies"][policy]
        l = ledger_by_policy[policy]
        rows.append(
            {
                "Case": policy,
                "Off_peak_import_USD": f"{float(l['offpeak_import_cost_USD']):.0f}",
                "Peak_import_USD": f"{float(l['peak_import_cost_USD']):.0f}",
                "Peak_surcharge_USD": f"{float(l['peak_surcharge_USD']):.0f}",
                "Total_import_USD": f"{float(l['total_import_cost_USD']):.0f}",
                "Export_revenue_USD": f"{float(l['export_revenue_USD']):.0f}",
                "H2_revenue_USD": f"{float(l['hydrogen_revenue_USD']):.0f}",
                "Carbon_USD": f"{float(l['carbon_transfer_USD']):.0f}",
                "Direct_balance_USD": f"{p['direct_realized_operating_economics_USD']:.0f}",
                "Battery_wear_USD": f"{p['common_wear_battery_USD']:.0f}",
                "PEMEL_wear_USD": f"{p['common_wear_pemel_USD']:.0f}",
                "PEMFC_wear_USD": f"{p['common_wear_pemfc_USD']:.0f}",
                "Total_common_wear_USD": f"{p['common_wear_total_USD']:.0f}",
                "Direct_plus_common_wear_USD": f"{p['direct_plus_common_wear_proxy_USD']:.0f}",
                "Memo_reconciliation_USD": f"{float(l['reconciliation_cost_USD_memo_only']):.2f}",
            }
        )
    return rows


def figure_2_source(metric: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for policy in POLICIES:
        p = metric["policies"][policy]
        rows.append(
            {
                "policy": policy,
                "grid_import_MWh": p["grid_import_kWh"] / 1000.0,
                "grid_export_MWh": p["grid_export_kWh"] / 1000.0,
                "battery_throughput_MWh": p["battery_throughput_kWh"] / 1000.0,
                "PEMEL_MWh": p["pemel_electricity_kWh"] / 1000.0,
                "PEMFC_MWh": p["pemfc_electricity_kWh"] / 1000.0,
                "H2_produced_kg": p["h2_produced_kg"],
                "emissions_tCO2": p["total_emissions_tonnes"],
            }
        )
    return rows


def figure_3_source(metric: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    components = (
        ("Direct", "direct_realized_operating_economics_USD"),
        ("Battery wear", "common_wear_battery_USD"),
        ("PEMEL wear", "common_wear_pemel_USD"),
        ("PEMFC wear", "common_wear_pemfc_USD"),
    )
    for policy in POLICIES:
        p = metric["policies"][policy]
        running = 0.0
        for label, field in components:
            change = float(p[field])
            start = running
            running += change
            rows.append(
                {
                    "policy": policy,
                    "component": label,
                    "start_USD": start,
                    "change_USD": change,
                    "end_USD": running,
                }
            )
        rows.append(
            {
                "policy": policy,
                "component": "Diagnostic total",
                "start_USD": 0.0,
                "change_USD": running,
                "end_USD": running,
            }
        )
    return rows


def figure_4_source(soh: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "policy": row["policy"],
            "hour": int(row["hour"]),
            "battery_soh": row["battery_soh_unchanged"],
            "pemel_soh": row["pemel_soh_corrected_0p19"],
            "pemfc_soh": row["pemfc_soh_unchanged"],
        }
        for row in soh
    ]


def compare_exact(generated: list[dict[str, Any]], expected: list[dict[str, str]]) -> dict[str, Any]:
    fields = list(expected[0]) if expected else []
    normalized = [{field: str(row[field]) for field in fields} for row in generated]
    return {
        "mode": "exact formatted-string equality",
        "rows": len(generated),
        "status": "PASS" if normalized == expected else "FAIL",
    }


def compare_numeric(
    generated: list[dict[str, Any]],
    expected: list[dict[str, str]],
    key_fields: tuple[str, ...],
    absolute_tolerance: float,
) -> dict[str, Any]:
    if len(generated) != len(expected):
        return {"status": "FAIL", "reason": "row-count mismatch"}
    max_error = 0.0
    failures = 0
    for got, want in zip(generated, expected):
        if any(str(got[key]) != str(want[key]) for key in key_fields):
            failures += 1
            continue
        for field in want:
            if field in key_fields:
                continue
            error = abs(float(got[field]) - float(want[field]))
            max_error = max(max_error, error)
            failures += int(error > absolute_tolerance)
    return {
        "mode": "absolute numerical comparison",
        "absolute_tolerance": absolute_tolerance,
        "maximum_absolute_error": max_error,
        "rows": len(generated),
        "failures": failures,
        "status": "PASS" if failures == 0 else "FAIL",
    }


def plot_figure_2(rows: list[dict[str, Any]], path: Path) -> None:
    fields = [
        ("grid_import_MWh", "Grid import (MWh)"),
        ("grid_export_MWh", "Grid export (MWh)"),
        ("battery_throughput_MWh", "Battery throughput (MWh)"),
        ("PEMEL_MWh", "PEMEL electricity (MWh)"),
        ("H2_produced_kg", "Hydrogen produced (kg)"),
        ("emissions_tCO2", "Grid-import emissions (tCO2)"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.0), constrained_layout=True)
    for axis, (field, title) in zip(axes.flat, fields):
        axis.bar(POLICIES, [float(row[field]) for row in rows], color=[COLORS[p] for p in POLICIES])
        axis.set_title(title, fontsize=9)
        axis.grid(axis="y", alpha=0.25)
    fig.savefig(path)
    plt.close(fig)


def plot_figure_3(rows: list[dict[str, Any]], path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.8), constrained_layout=True)
    for axis, policy in zip(axes, POLICIES):
        subset = [row for row in rows if row["policy"] == policy]
        labels = [row["component"] for row in subset]
        values = [float(row["end_USD"]) for row in subset]
        axis.bar(range(len(values)), values, color=COLORS[policy])
        axis.axhline(0, color="#333333", linewidth=0.8)
        axis.set_xticks(range(len(values)), labels, rotation=45, ha="right", fontsize=7)
        axis.set_title(policy)
        axis.set_ylabel("Cumulative USD")
        axis.grid(axis="y", alpha=0.25)
    fig.savefig(path)
    plt.close(fig)


def plot_figure_4(rows: list[dict[str, Any]], path: Path) -> None:
    fields = (
        ("battery_soh", "Battery SoH"),
        ("pemel_soh", "PEMEL SoH (0.19 V/cell basis)"),
        ("pemfc_soh", "PEMFC SoH"),
    )
    fig, axes = plt.subplots(3, 1, figsize=(10.5, 7.5), sharex=True, constrained_layout=True)
    for axis, (field, label) in zip(axes, fields):
        for policy in POLICIES:
            subset = [row for row in rows if row["policy"] == policy]
            axis.plot(
                [int(row["hour"]) for row in subset],
                [float(row[field]) for row in subset],
                label=policy,
                color=COLORS[policy],
                linewidth=0.8,
            )
        axis.set_ylabel(label)
        axis.grid(alpha=0.25)
    axes[0].legend(ncol=3)
    axes[-1].set_xlabel("Annual hour")
    fig.savefig(path)
    plt.close(fig)


def artifact(path: Path) -> dict[str, Any]:
    payload = {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
    if path.suffix.lower() == ".pdf":
        payload["pdf_pages"] = len(PdfReader(str(path)).pages)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("reproduced"))
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    metric, ledger, soh = load_inputs(root)

    t3 = table_3(metric)
    t4 = table_4(metric, ledger)
    f2 = figure_2_source(metric)
    f3 = figure_3_source(metric)
    f4 = figure_4_source(soh)

    table_3_path = output / "MAIN_TABLE_3.csv"
    table_4_path = output / "MAIN_TABLE_4.csv"
    figure_2_source_path = output / "MAIN_FIGURE_2_SOURCE.csv"
    figure_3_source_path = output / "MAIN_FIGURE_3_SOURCE.csv"
    figure_4_source_path = output / "MAIN_FIGURE_4_SOURCE.csv"
    figure_2_pdf = output / "MAIN_FIGURE_2.pdf"
    figure_3_pdf = output / "MAIN_FIGURE_3.pdf"
    figure_4_pdf = output / "MAIN_FIGURE_4.pdf"

    write_csv(table_3_path, t3, list(t3[0]))
    write_csv(table_4_path, t4, list(t4[0]))
    write_csv(figure_2_source_path, f2, list(f2[0]))
    write_csv(figure_3_source_path, f3, list(f3[0]))
    write_csv(figure_4_source_path, f4, list(f4[0]))
    plot_figure_2(f2, figure_2_pdf)
    plot_figure_3(f3, figure_3_pdf)
    plot_figure_4(f4, figure_4_pdf)

    comparisons = {
        "Main Table 3": compare_exact(t3, read_csv(root / "reference" / "MAIN_TABLE_3.csv")),
        "Main Table 4": compare_exact(t4, read_csv(root / "reference" / "MAIN_TABLE_4.csv")),
        "Main Figure 2 source": compare_numeric(
            f2,
            read_csv(root / "reference" / "FIGURE_2_ANNUAL_REGIMES.csv"),
            ("policy",),
            5e-9,
        ),
        "Main Figure 3 source": compare_numeric(
            f3,
            read_csv(root / "reference" / "FIGURE_3_RANKING_REVERSAL.csv"),
            ("policy", "component"),
            5e-6,
        ),
        "Main Figure 4 source": {
            "mode": "exact projection from sealed 26,280-row reporting-correction evidence",
            "rows": len(f4),
            "expected_rows": 26280,
            "status": "PASS" if len(f4) == 26280 else "FAIL",
        },
    }
    status = "PASS" if all(item["status"] == "PASS" for item in comparisons.values()) else "FAIL"
    report_path = output / "REPRODUCTION_CHECK.json"
    report = {
        "schema_version": "1.0",
        "status": status,
        "scope": "curated reporting layer and manuscript derivatives only",
        "original_annual_campaign_regenerated": False,
        "solver_calls": 0,
        "simulation_calls": 0,
        "optimization_calls": 0,
        "comparisons": comparisons,
        "input_sha256": {
            name: sha256(root / "evidence" / name)
            for name in (
                "AUTHORITATIVE_METRIC_DICTIONARY.json",
                "DIRECT_LEDGER_RECONCILIATION.csv",
                "PEMEL_SOH_REPORTING_CORRECTION.csv",
            )
        },
        "outputs": [
            artifact(path)
            for path in (
                table_3_path,
                table_4_path,
                figure_2_source_path,
                figure_3_source_path,
                figure_4_source_path,
                figure_2_pdf,
                figure_3_pdf,
                figure_4_pdf,
            )
        ],
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "report": str(report_path)}, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

