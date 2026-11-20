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
