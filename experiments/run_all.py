#!/usr/bin/env python3
import argparse, csv, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'multiseed_results.csv'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seeds', nargs='+', type=int, default=[11,22,33,44,55])
    p.add_argument('--steps', type=int, default=650)
    args=p.parse_args()
    OUT.parent.mkdir(exist_ok=True)
    if OUT.exists(): OUT.unlink()
    legacy=ROOT/'results'/'experiment_results.csv'
    if legacy.exists(): legacy.unlink()
    for seed in args.seeds:
        for scenario in ('balanced','ns-heavy'):
            for controller in ('fixed','adaptive'):
                print(f'Running seed={seed} scenario={scenario} controller={controller}', flush=True)
                cmd=[sys.executable,str(ROOT/'simulator.py'),'--controller',controller,'--scenario',scenario,'--steps',str(args.steps),'--seed',str(seed)]
                subprocess.run(cmd, cwd=ROOT, check=True)
                row=ROOT/'results'/'experiment_results.csv'
                rows=list(csv.DictReader(row.open()))
                last=rows[-1]
                last['seed']=str(seed)
                fields=['seed','controller','scenario','completed_vehicles','average_waiting_time_s','average_travel_time_s','average_time_loss_s']
                new=not OUT.exists()
                with OUT.open('a',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=fields)
                    if new:w.writeheader()
                    w.writerow({k:last[k] for k in fields})
    print(f'Wrote {OUT}')
if __name__=='__main__': main()
