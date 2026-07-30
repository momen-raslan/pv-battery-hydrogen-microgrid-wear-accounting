"""Small reporting transformations isolated from the production controller."""

from __future__ import annotations


PEMEL_CELLS = 100
PEMEL_EOL_VOLTAGE_RISE_PER_CELL_V = 0.19


def reporting_pemel_soh(stack_voltage_rise_v: float) -> float:
    """Return the display SoH for the retained PEMEL voltage-rise state.

    This is a reporting transformation only. It does not update a device
    state, dispatch value, degradation accumulator, or objective.
    """

    denominator = PEMEL_CELLS * PEMEL_EOL_VOLTAGE_RISE_PER_CELL_V
    return max(1.0 - float(stack_voltage_rise_v) / denominator, 0.0)

