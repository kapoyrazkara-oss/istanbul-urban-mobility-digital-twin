# Istanbul Urban Mobility Digital Twin

SUMO-based adaptive traffic signal simulation and 3D urban mobility digital twin for Istanbul.

## Research question

Can a simple, interpretable adaptive traffic-signal controller reduce waiting time compared with a fixed-time baseline under different traffic-demand patterns?

## Validated result

Five matched random seeds were run for each controller and scenario. The same seed gives Fixed-Time and Adaptive the same demand.

| Scenario | Fixed-Time | Adaptive | Reduction |
|---|---:|---:|---:|
| Balanced | 12.93 ± 0.31 s | 10.52 ± 0.24 s | 18.64% |
| North-south-heavy | 14.74 ± 0.30 s | 10.04 ± 0.47 s | 31.89% |

The earlier single-run article numbers were 24.7% and 35.7%. They are preserved as preliminary results; this repository reports the multi-seed validation separately.

## Run the experiments

Install SUMO and Python first, then:

```bash
pip install -r requirements.txt
python experiments/run_all.py --seeds 11 22 33 44 55
python experiments/aggregate_results.py
```

The raw matched results are saved to `results/multiseed_results.csv`; the summary is saved to `results/multiseed_summary.csv`; the chart is in `results/figures/`.

Run one experiment manually:

```bash
python simulator.py --controller adaptive --scenario balanced --seed 11 --steps 650
```

## Digital twin replay

The recommended presentation viewer is `advanced/final3d/START_FINAL_3D.bat`. Extract the repository or the final ZIP, double-click that launcher on Windows, and keep its command window open while Chrome runs at the local HTTP address. Do not open `viewer.html` directly with `file://`; the launcher avoids browser JSON/CORS problems and keeps Three.js local inside the package.

The final viewer compares Fixed-Time, Local Adaptive, and Coordinated Adaptive on a 5×5 / 25-intersection SUMO network. It includes a procedural Istanbul-inspired 3D environment, traffic-light state replay, live queue telemetry, queue trajectory, and a 5×5 intersection-pressure heatmap. The map is a presentation context rather than a geospatially exact city map; traffic data, signal states, and metrics come from SUMO.

## Repository map

- `simulator.py`: original four-way experiment runner with reproducible seeds.
- `experiments/run_all.py`: five-seed paired experiment runner.
- `experiments/aggregate_results.py`: mean, standard deviation, and improvement calculation.
- `simulation/`: original SUMO network and routes.
- `advanced/`: 25-intersection digital-twin replay and export tools.
- `article/`: revised Build Article, methodology, and reviewer response.
- `results/`: raw CSV results, summary table, and chart.

## Limitations

This is a rule-based prototype with synthetic demand on a small research network. It is not a city-wide prediction and is not ready for deployment without real detector data, safety validation, pedestrian/public-transport constraints, calibration, and field testing.

## Show-it

A 3+ minute demonstration video will be linked here after recording. It will show the SUMO network, Fixed-Time baseline, Adaptive controller, metrics, and limitations.
