# eFuse Cable Protection: Thermal Model vs Fixed I²t

Simulation study of thermal cable protection in 12 V automotive wiring
systems, comparing conventional fixed I²t protection against a
software thermal model (digital twin) running inside an electronic fuse.

## Result

| Method | Conditions failed |
|---|---|
| Fixed I²t | **14 / 20** |
| Thermal model | **0 / 20** |

Across 5 ambient temperatures (−20 to 100 °C) and 4 fault currents
(20 to 50 A) on a 0.5 mm² PVC-insulated cable.

## Key findings

**1. Fixed I²t fails catastrophically at automotive ambient temperatures.**
At 85 °C ambient the cable is damaged in 0.45 to 3.0 s, while the I²t
fuse trips after 2.25 to 14.1 s. Safety margin: **−390%**. Engine bay
temperatures of 85 °C and above are normal, so this is an operating
condition, not a corner case.

**2. Fixed I²t also fails at room temperature for high currents.**
At 25 °C, 40 A and 50 A both trip late (−6%, −9%) despite the threshold
being tuned at 30 A. A constant-I²t characteristic is a straight line on
a log-log plot; the real cable limit is curved. Two independent failure
mechanisms.

**3. A software thermal model tracks every ambient correctly.**
Running the cable's thermal RC model live inside the eFuse, using
measured current and ambient temperature, gives positive margin at all
20 conditions.

**4. Above 100 °C ambient the model correctly refuses to close.**
With the insulation limit at 105 °C and trip threshold at 95 °C, the
cable is beyond limit at zero current. Trip time is 0 s by design.

## Trade-off

Accurate protection reduces nuisance headroom. At −20 °C the thermal
model trips with 7 to 13% margin where fixed I²t has 38 to 66%. Tighter
protection means less tolerance for model error, so model parameter
accuracy and sensor tolerance become the limiting factors rather than
the algorithm.

## Model

Single-node lumped thermal model of a 1 m, 0.5 mm² copper cable:

    dT/dt = (I²·R(T) − (T − T_amb)/R_th) / C_th
    R(T)  = R₂₀·(1 + α·(T − 20))

| Parameter | Value |
|---|---|
| R₂₀ | 34.4 mΩ/m |
| α (copper) | 0.00393 /K |
| C_th | 2.5 J/K |
| R_th | 9.0 K/W |
| Insulation limit (PVC) | 105 °C |
| Trip threshold | 95 °C |

Self-heating feedback is included: copper resistance rises ~51% from
20 °C to 150 °C, so a hot cable heats faster at the same current.

**Validation:** the model predicts 13.5 A continuous rating at 25 °C
ambient, consistent with the typical 11 to 13 A rating for 0.5 mm²
automotive cable.

## Files

| File | Purpose |
|---|---|
| `step1_resistance.py` | Copper resistance vs temperature |
| `step2_heating.py` | Transient heating at 10 / 15 / 25 A |
| `step3_tripcurve.py` | Current vs time-to-damage curve |
| `step4_i2t.py` | Fixed I²t protection and where it fails |
| `step5_thermal_model.py` | Thermal-model protection |
| `step6_report.py` | Full sweep, CSV export, comparison plots |
| `results.csv` | All 20 conditions |

## Limitations

- Single-node thermal model; no separate conductor and insulation nodes,
  so short-duration behaviour below ~100 ms is optimistic
- R_th assumes free air; bundled harnesses and conduits are worse
- No hardware validation; simulation only
- Ambient assumed perfectly measured; sensor error not modelled

## Run

    python3 step6_report.py