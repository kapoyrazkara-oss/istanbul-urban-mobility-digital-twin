# From Research to Simulation: Building an Adaptive Traffic Signal System for Istanbul

## Introduction

In my previous article, [How Can AI and Adaptive Traffic Signal Systems Improve Urban Transportation?](https://medium.com/@ka.poyrazkara/how-can-ai-and-adaptive-traffic-signal-systems-improve-urban-transportation-d3025ebf36c6), I explored how traffic-responsive signal systems could help reduce urban congestion. I focused on Istanbul and argued that these systems should be tested in small, measurable pilots rather than adopted based only on assumptions.

For the Build stage, I turned that idea into a working traffic simulation.

## The project question

I wanted to test the following question:

> Can a traffic-responsive signal controller reduce average waiting time compared with a fixed-time controller under uneven traffic conditions?

My hypothesis was that an adaptive controller would reduce waiting time by giving more green time to the direction with the larger queue, while still respecting safe phase transitions.

## Why simulation?

I cannot change the traffic lights at a real Istanbul intersection for a student project. A simulation makes it possible to test the idea safely and repeatably. I used Eclipse SUMO, an open-source traffic simulator, together with Python and TraCI. TraCI allows an external Python controller to read the simulation state and change traffic-light behavior during the run.

The first model contains one four-way intersection with north, south, east, and west approaches. Vehicles follow reproducible routes so that the fixed-time and adaptive controllers can be compared under the same conditions.

## Two controllers

The first controller is fixed-time. It uses the same signal cycle regardless of the traffic conditions.

The second controller is traffic-responsive. It checks the number of stopped vehicles on the north-south and east-west approaches. When a green phase begins, it can extend that phase within a safe range when the active direction has more pressure than the other direction.

This first version is a rule-based adaptive controller, not a machine-learning model. I made this distinction deliberately. Before using reinforcement learning or computer vision, I wanted to establish whether a simple adaptive idea could produce a measurable improvement.

## Experimental scenarios

I ran both controllers in two scenarios:

1. **Balanced traffic:** north-south and east-west traffic have similar demand.
2. **North-south-heavy traffic:** the north-south approaches receive vehicles more frequently than the east-west approaches.

For each experiment, I recorded completed vehicles, average waiting time, average travel time, and average time loss.

## Results

| Scenario | Controller | Completed vehicles | Average waiting time | Average travel time |
|---|---:|---:|---:|---:|
| Balanced | Fixed-time | 236 | 12.97 s | 67.52 s |
| Balanced | Adaptive | 236 | 9.76 s | 64.14 s |
| North-south heavy | Fixed-time | 300 | 15.62 s | 73.66 s |
| North-south heavy | Adaptive | 300 | 10.05 s | 66.70 s |

In the balanced scenario, the adaptive controller reduced average waiting time by approximately 24.7% compared with the fixed-time controller. In the north-south-heavy scenario, the reduction was approximately 35.7%.

These results support the hypothesis for these simulated conditions. They do not prove that the same percentage would be achieved at every real intersection in Istanbul.

![Average waiting time comparison](../charts/waiting-time-comparison.png)

## What I learned

The most important lesson was that a strong idea needs a measurable experiment. My first article discussed real-world examples and possible benefits. The Build stage forced me to define a baseline, create repeatable traffic conditions, choose metrics, and compare two controllers fairly.

I also learned that calling every adaptive traffic-light system “AI” can be misleading. My first controller uses traffic measurements and explicit rules. It is adaptive, but it is not yet a machine-learning controller. This distinction made the project more technically honest.

## Limitations

This is a small simulation, not a complete model of Istanbul. It contains one intersection and simplified routes. It does not yet model pedestrians, buses, emergency vehicles, weather, camera errors, or coordination between multiple intersections. The results are therefore a proof of concept rather than a city-wide prediction.

The controller is also rule-based. A future version could compare it with reinforcement learning, but that would require careful reward design and additional safety constraints.

## Next steps

The next step is to add a 3D visualization so that vehicles, queues, and traffic-light phases can be observed more clearly. After that, I want to add pedestrian and public-transport priorities, test multiple connected intersections, and investigate whether real traffic data could improve the model.

## Conclusion

I started with a research question about whether AI and adaptive traffic signals could help Istanbul. I then built a SUMO and Python prototype that compares fixed-time and traffic-responsive control.

In the experiments, the adaptive controller reduced average waiting time in both tested scenarios. The result is limited to this simulation, but it gives the idea a measurable starting point.

The project also showed me the value of moving from learning to building: research helped me define the problem, while the prototype helped me test what actually happened.

## Technical resources

- [Eclipse SUMO](https://eclipse.dev/sumo/)
- [SUMO Traffic Lights documentation](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html)
- [TraCI traffic-light tutorial](https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html)
