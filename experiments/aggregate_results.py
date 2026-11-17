#!/usr/bin/env python3
import csv, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/'results'/'multiseed_results.csv'
OUT=ROOT/'results'/'multiseed_summary.csv'
rows=list(csv.DictReader(IN.open()))
groups={}
for r in rows:
    groups.setdefault((r['scenario'],r['controller']),[]).append(r)
metrics=['average_waiting_time_s','average_travel_time_s','average_time_loss_s']
out=[]
for (scenario,controller),rs in sorted(groups.items()):
    item={'scenario':scenario,'controller':controller,'n':len(rs)}
    for m in metrics:
        vals=[float(r[m]) for r in rs]
        item[m+'_mean']=round(statistics.mean(vals),2)
        item[m+'_stdev']=round(statistics.stdev(vals),2) if len(vals)>1 else 0
    out.append(item)
for scenario in sorted({r['scenario'] for r in out}):
    fixed=next(r for r in out if r['scenario']==scenario and r['controller']=='fixed')
    adaptive=next(r for r in out if r['scenario']==scenario and r['controller']=='adaptive')
    base=fixed['average_waiting_time_s_mean']; new=adaptive['average_waiting_time_s_mean']
    adaptive['waiting_improvement_pct']=round((base-new)/base*100,2)
fields=list(out[0].keys())
with OUT.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
print(OUT)
for r in out: print(r)
