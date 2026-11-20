# Istanbul Adaptive Traffic Signal Simulator

A SUMO- and Python-based prototype for comparing fixed-time and traffic-responsive traffic signal control at a four-way intersection.

## Research question

Can a traffic-responsive signal controller reduce average waiting time compared with a fixed-time controller under uneven traffic conditions?

## Hypothesis

A traffic-responsive signal controller can reduce average waiting time compared with a fixed-time controller under uneven traffic conditions, while respecting minimum green times and safe phase transitions.

## Project scope

This project uses a simulated 5×5 network with 25 signalised intersections. It does not control real traffic lights and does not claim to represent all of Istanbul's traffic. The validated paper results remain the fixed-time versus rule-based adaptive comparison; the AI controller below is an additional prototype and is not mixed into those reported results.

## Planned metrics

- Average waiting time
- Maximum queue length
- Average travel time
- Number of completed vehicles
- Number of stops

## Planned comparison

1. Fixed-time controller
2. Traffic-responsive adaptive controller
3. Balanced, uneven, and changing traffic scenarios

## Technology

- Eclipse SUMO
- Python
- TraCI
- Matplotlib / Streamlit for analysis and visualization

## First milestone

Create and run a four-way intersection with fixed-time traffic lights and reproducible vehicle routes.

## Current results

The first reproducible experiments are complete. In the balanced scenario, average waiting time was 12.97 seconds with fixed-time control and 9.76 seconds with adaptive control. In the north-south-heavy scenario, the values were 15.62 seconds and 10.05 seconds respectively. These are simulation results, not a prediction for all of Istanbul.

## AI adaptive and safe-driving prototype

`advanced/export_3d_v2.py --controller ai-adaptive` runs a deterministic, seed-controlled online Q-learning prototype. Its state contains local queue, neighbour pressure, and current phase; its actions are hold, extend green, or safely shorten green. Minimum green (12 s), maximum green (60 s), and the SUMO yellow/all-red transition program remain hard constraints. This is intentionally a constrained policy rather than an LLM making live signal decisions.

For the AI replay, `--driver-policy safe-ai` activates SUMO's full speed-safety checks (`speedMode=31`) and collision-safe lane-change mode (`laneChangeMode=1621`). SUMO's car-following and right-of-way logic therefore handle stopping and signal compliance. The 3D viewer only replays the resulting trajectories; it does not invent vehicle decisions. AI replay files are available for rush-hour and balanced demand in `advanced/final3d/data/ai_rush.json` and `advanced/final3d/data/ai_balanced.json`.

## Run the simulator

```bash
python simulator.py --controller adaptive --scenario balanced --gui --delay 200
```

Use `fixed` or `adaptive` for the controller and `balanced` or `ns-heavy` for the traffic scenario. Results are written to `results/experiment_results.csv`.

## Build Article

The current article draft is in `article/build-article-draft.md`. The SUMO phase is targeted for completion on 5 November 2026; 3D visualization work begins afterward.
