# Experimental methodology

## Paired multi-seed design

Each scenario uses five random seeds: 11, 22, 33, 44, and 55. For each seed, Fixed-Time and Adaptive receive the same route demand. This paired design reduces the risk that one controller wins only because it happened to receive an easier traffic sample.

## Metrics

The SUMO tripinfo output is used to calculate completed vehicles, average waiting time, average travel time, and average time loss. The aggregation script reports the mean and sample standard deviation across the five seeds.

## Results

| Scenario | Fixed-Time waiting | Adaptive waiting | Reduction |
|---|---:|---:|---:|
| Balanced | 12.93 ± 0.31 s | 10.52 ± 0.24 s | 18.64% |
| North-south-heavy | 14.74 ± 0.30 s | 10.04 ± 0.47 s | 31.89% |

The original single-run reductions were 24.7% and 35.7%. The difference demonstrates why repeated runs are necessary.

## Additional AI controller prototype

The project also contains a separate `ai-adaptive` replay controller. It is an online, tabular Q-learning policy with a fixed random seed, not a large language model. The state is `(local halted-vehicle bin, neighbour-pressure bin, current phase group)` and the actions are `hold`, `extend`, or `safely shorten` the current green. A hard safety layer enforces a 12-second minimum green, a 60-second maximum green, and leaves yellow/all-red transitions to the SUMO signal program. The reward is negative network queue plus a phase-change penalty.

For this prototype's vehicle layer, `safe-ai` applies SUMO `speedMode=31` and collision-safe `laneChangeMode=1621`. This should be described as a safety-constrained driver policy, not as a trained autonomous-driving model. The viewer is a trajectory replay and must not be used as evidence of an AI controller's performance until the AI policy has undergone the same paired five-seed evaluation as the validated baselines.
