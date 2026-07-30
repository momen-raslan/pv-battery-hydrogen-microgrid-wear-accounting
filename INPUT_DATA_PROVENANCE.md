# Input-data provenance

- Weather: `data/alexandria_tmy.csv`, the fixed PVGIS TMY input used by the
  study. It is a byte-identical response from the documented official API;
  see `WEATHER_RETRIEVAL.md`.
- Load: deterministic synthetic medium-office profile scaled to
  1,000,000 kWh/year with weekday/weekend and seasonal structure.
- Tariffs: modeled study assumptions (0.0519 USD/kWh off peak, 1.5 peak
  multiplier from 12:00 through 19:59, and 0.0415 USD/kWh export).
- Hydrogen value: modeled gross 6 USD/kg sale value, not net delivered profit.
- Carbon case: 50 USD/tCO2 and 0.49 tCO2/MWh operational grid-import factor.

The annual results in `evidence/` are curated derivatives from the protected
scientific audit. The unavailable original 27-file campaign is not included
and is not reconstructed here.
