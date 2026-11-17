# From Research to Simulation: Building an Adaptive Traffic Signal System for Istanbul

*How I turned my research about smart traffic lights into a working SUMO and Python prototype.*

## From learning to building

In my previous article, [How Can AI and Adaptive Traffic Signal Systems Improve Urban Transportation?](https://medium.com/@ka.poyrazkara/how-can-ai-and-adaptive-traffic-signal-systems-improve-urban-transportation-d3025ebf36c6), I explored how traffic-responsive signal systems could help reduce urban congestion. I focused on Istanbul and argued that these systems should be tested through small, measurable pilots instead of being evaluated only through assumptions.

For the Build stage, I wanted to turn that idea into something I could actually run and test.

## The question I wanted to answer

My project asks:

> Can a traffic-responsive signal controller reduce average waiting time compared with a fixed-time controller under uneven traffic conditions?

My hypothesis was that an adaptive controller could reduce waiting time by giving more green time to the direction with greater traffic pressure, while still respecting safe phase transitions.

## Why I used simulation

As a student, I cannot change the traffic lights at a real intersection in Istanbul. A simulation gives me a safe and repeatable environment in which I can compare different strategies under the same conditions.

I used [Eclipse SUMO](https://eclipse.dev/sumo/), an open-source traffic simulator, with Python and [TraCI](https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html). TraCI allows an external Python program to read the state of a running simulation and control traffic lights.

My first model contains one four-way intersection with north, south, east, and west approaches. Vehicles follow reproducible routes so that the two controllers can be compared fairly.

## What I built

I created two traffic signal controllers.

The first is a fixed-time controller. It follows the same signal cycle regardless of the current traffic conditions.

The second is a traffic-responsive adaptive controller. It checks the number of stopped vehicles approaching the intersection from the north-south and east-west directions. When a green phase begins, the controller can extend that phase within a defined range if the active direction has greater traffic pressure.

This first version is rule-based. It is adaptive, but it is not yet a machine-learning system. I made this distinction deliberately because I wanted to establish a reliable baseline before trying reinforcement learning or computer vision.

## Experiment design

I tested both controllers in two scenarios:

- **Balanced traffic:** The north-south and east-west directions receive similar traffic demand.
- **North-south-heavy traffic:** The north-south directions receive vehicles more frequently than the east-west directions.

For each run, I recorded the number of completed vehicles, average waiting time, average travel time, and average time loss.

## Results

| Scenario | Controller | Completed vehicles | Average waiting time | Average travel time |
|---|---:|---:|---:|---:|
| Balanced | Fixed-time | 236 | 12.97 s | 67.52 s |
| Balanced | Adaptive | 236 | 9.76 s | 64.14 s |
| North-south heavy | Fixed-time | 300 | 15.62 s | 73.66 s |
| North-south heavy | Adaptive | 300 | 10.05 s | 66.70 s |

In the balanced scenario, the adaptive controller reduced average waiting time by approximately **24.7%** compared with the fixed-time controller.

In the north-south-heavy scenario, the reduction was approximately **35.7%**.

These results support my hypothesis under the tested simulation conditions. They do not mean that the same percentages would automatically be achieved at every real intersection in Istanbul.

![Average waiting time comparison](../charts/waiting-time-comparison.png)

## What I learned

The biggest lesson was that a promising idea needs a measurable experiment. My first article helped me understand the problem and investigate existing approaches. The Build stage forced me to define a baseline, create repeatable traffic conditions, choose evaluation metrics, and compare two controllers fairly.

I also learned that not every adaptive traffic-light system should automatically be called “AI.” My current controller uses traffic measurements and explicit rules. Calling it a rule-based adaptive controller is more technically accurate than describing it as a machine-learning model.

## Limitations

This is a small proof-of-concept simulation, not a complete model of Istanbul. It contains one intersection and simplified vehicle routes. It does not yet include pedestrians, buses, emergency vehicles, weather conditions, camera errors, or coordination between multiple intersections.

The controller is also rule-based. A future version could compare it with reinforcement learning, but that would require careful reward design, more scenarios, and additional safety constraints.

## What I will build next

My next step is to add a 3D visualization so that vehicles, queues, and traffic-light phases can be observed more clearly. I also want to explore public-transport and emergency-vehicle priority, pedestrian phases, and multiple connected intersections.

In the longer term, real traffic data could make the scenarios more realistic. However, I wanted to start with a small and understandable prototype before adding more complexity.

## Conclusion

I started with a research question about whether adaptive traffic signals could help reduce congestion in Istanbul. I then built a SUMO and Python prototype that compares fixed-time and traffic-responsive control at a four-way intersection.

In both tested scenarios, the adaptive controller produced a lower average waiting time. The result is limited to this simulation, but it gives the idea a measurable starting point.

This project showed me the value of moving from learning to building: research helped me define the problem, while the prototype helped me test what actually happened.

## Technical resources

- [Eclipse SUMO](https://eclipse.dev/sumo/)
- [SUMO Traffic Lights documentation](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html)
- [TraCI traffic-light tutorial](https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html)
