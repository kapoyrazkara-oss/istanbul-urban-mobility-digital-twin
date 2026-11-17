#!/usr/bin/env python3
"""Interactive SUMO experiment runner for the Istanbul traffic project."""
import argparse
import csv
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import traci

ROOT = Path(__file__).resolve().parent
CFG = ROOT / "simulation/fixed_time/cross.sumocfg"
RESULTS = ROOT / "results"
INCOMING = {
    "north_to_center": "NS",
    "south_to_center": "NS",
    "east_to_center": "EW",
    "west_to_center": "EW",
}


def parse_args():
    p = argparse.ArgumentParser(description="Istanbul Adaptive Traffic Signal Simulator")
    p.add_argument("--controller", choices=["fixed", "adaptive"], help="Signal controller")
    p.add_argument("--scenario", choices=["balanced", "ns-heavy"], default="balanced", help="Traffic scenario")
    p.add_argument("--gui", action="store_true", help="Open the SUMO visual simulator")
    p.add_argument("--steps", type=int, default=650, help="Simulation duration in seconds")
    p.add_argument("--delay", type=int, default=0, help="Milliseconds to wait between GUI simulation steps")
    p.add_argument("--seed", type=int, default=42, help="Random seed for reproducible demand")
    return p.parse_args()


def choose(args):
    controller = args.controller or input("Controller (fixed/adaptive) [adaptive]: ").strip().lower() or "adaptive"
    scenario = args.scenario
    if not args.controller:
        scenario = input("Scenario (balanced/ns-heavy) [balanced]: ").strip().lower() or "balanced"
    gui = args.gui
    if not args.controller and not gui:
        gui = input("SUMO penceresi açılsın mı? (e/h) [e]: ").strip().lower() != "h"
    if controller not in ("fixed", "adaptive"):
        raise SystemExit("Controller fixed veya adaptive olmalı.")
    if scenario not in ("balanced", "ns-heavy"):
        raise SystemExit("Scenario balanced veya ns-heavy olmalı.")
    return controller, scenario, gui


def pressure():
    values = {"NS": 0, "EW": 0}
    for edge, direction in INCOMING.items():
        try:
            values[direction] += sum(1 for v in traci.edge.getLastStepVehicleIDs(edge)
                                     if traci.vehicle.getSpeed(v) < 0.1)
        except traci.TraCIException:
            pass
    return values


def run(controller, scenario, gui, steps, delay_ms, seed=42):
    RESULTS.mkdir(exist_ok=True)
    name = f"{controller}_{scenario}"
    trip_path = RESULTS / f"{name}_tripinfo.xml"
    summary_path = RESULTS / f"{name}_summary.xml"
    binary = "sumo-gui" if gui else "sumo"
    route_file = ROOT / "simulation/routes/cross.rou.xml"
    if scenario == "ns-heavy":
        route_file = ROOT / "simulation/routes/cross_ns_heavy.rou.xml"
    cmd = [binary, "-c", str(CFG), "--route-files", str(route_file),
           "--tripinfo-output", str(trip_path),
           "--summary-output", str(summary_path), "--end", str(steps),
           "--no-step-log", "true", "--no-warnings", "true"]
    cmd += ["--seed", str(seed)]
    traci.start(cmd)
    tls = traci.trafficlight.getIDList()[0]
    last_phase = -1
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if gui and delay_ms > 0:
            time.sleep(delay_ms / 1000)
        if controller == "adaptive":
            phase = traci.trafficlight.getPhase(tls)
            if phase != last_phase:
                if phase in (0, 2):
                    q = pressure()
                    active = "NS" if phase == 0 else "EW"
                    other = "EW" if active == "NS" else "NS"
                    # Keep the phase between 20 and 60 seconds, based on pressure.
                    extra = min(18, max(0, (q[active] - q[other]) * 2))
                    traci.trafficlight.setPhaseDuration(tls, 24 + extra)
                last_phase = phase
    traci.close()
    trips = ET.parse(trip_path).getroot().findall("tripinfo")
    def avg(key):
        vals = [float(x.attrib[key]) for x in trips if key in x.attrib]
        return sum(vals) / len(vals) if vals else 0
    metrics = {
        "seed": seed,
        "controller": controller,
        "scenario": scenario,
        "completed_vehicles": len(trips),
        "average_waiting_time_s": round(avg("waitingTime"), 2),
        "average_travel_time_s": round(avg("duration"), 2),
        "average_time_loss_s": round(avg("timeLoss"), 2),
    }
    csv_path = RESULTS / "experiment_results.csv"
    exists = csv_path.exists()
    with csv_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(metrics)
    return metrics


def main():
    args = parse_args()
    controller, scenario, gui = choose(args)
    print(f"\nÇalışıyor: controller={controller}, scenario={scenario}, gui={gui}")
    metrics = run(controller, scenario, gui, args.steps, args.delay, args.seed)
    print("\nDeney tamamlandı")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print(f"Sonuçlar: {RESULTS / 'experiment_results.csv'}")


if __name__ == "__main__":
    main()
