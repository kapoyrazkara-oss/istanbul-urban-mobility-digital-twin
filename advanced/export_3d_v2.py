#!/usr/bin/env python3
"""Urban Mobility Digital Twin v2 exporter: fixed, local adaptive, coordinated adaptive."""
import argparse, json, time
from pathlib import Path
import traci

ROOT=Path(__file__).resolve().parent
NET=ROOT/'network/city5x5.net.xml'
ROUTES={'rush-hour':ROOT/'routes/rush5.rou.xml','balanced':ROOT/'routes/balanced5.rou.xml'}

def lane_groups():
    return {tls:sorted(set(l for l in traci.trafficlight.getControlledLanes(tls) if l and not l.startswith(':'))) for tls in traci.trafficlight.getIDList()}

def neighbors(tls_ids):
    pos={t:traci.junction.getPosition(t) for t in tls_ids}
    out={t:[] for t in tls_ids}
    for t in tls_ids:
        candidates=[]
        for u in tls_ids:
            if u==t: continue
            d=((pos[t][0]-pos[u][0])**2+(pos[t][1]-pos[u][1])**2)**.5
            if d<270: candidates.append(u)
        out[t]=candidates
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--controller',choices=['fixed','local-adaptive','coordinated-adaptive'],default='coordinated-adaptive')
    p.add_argument('--scenario',choices=list(ROUTES),default='rush-hour')
    p.add_argument('--steps',type=int,default=600)
    p.add_argument('--sample-every',type=int,default=3)
    p.add_argument('--output',default='viewer_data_v2.json')
    a=p.parse_args()
    traci.start(['sumo','-n',str(NET),'-r',str(ROUTES[a.scenario]),'--end',str(a.steps),'--seed','42','--no-step-log','true','--no-warnings','true'])
    tls_ids=sorted(traci.trafficlight.getIDList()); groups=lane_groups(); neigh=neighbors(tls_ids)
    frames=[]; decisions=0; maxq=0; phases=0; last={t:-1 for t in tls_ids}
    while traci.simulation.getMinExpectedNumber()>0:
        traci.simulationStep()
        queues={t:sum(traci.lane.getLastStepHaltingNumber(l) for l in ls) for t,ls in groups.items()}
        total=sum(queues.values()); maxq=max(maxq,total)
        if a.controller!='fixed':
            for t in tls_ids:
                ph=traci.trafficlight.getPhase(t)
                if ph!=last[t]:
                    phases+=1
                    if ph%2==0:
                        logic=traci.trafficlight.getAllProgramLogics(t)[0]; base=logic.phases[ph].duration
                        local=queues[t]; ns=[queues[n] for n in neigh[t]]
                        if a.controller=='local-adaptive': pressure=local-(sum(queues.values())/max(1,len(queues)))
                        else: pressure=local-(sum(ns)/max(1,len(ns))) if ns else local
                        extra=min(18,max(0,int(pressure*1.7)))
                        traci.trafficlight.setPhaseDuration(t,min(70,base+extra)); decisions += int(extra>0)
                    last[t]=ph
        if int(traci.simulation.getTime())%a.sample_every==0:
            vehicles=[]
            for vid in traci.vehicle.getIDList():
                x,y=traci.vehicle.getPosition(vid); speed=traci.vehicle.getSpeed(vid)
                vehicles.append({'id':vid,'x':round(x,2),'y':round(y,2),'a':round(traci.vehicle.getAngle(vid),1),'s':round(speed,2),'type':'vehicle'})
            frames.append({'t':round(traci.simulation.getTime(),1),'vehicles':vehicles,'signals':{t:traci.trafficlight.getPhase(t) for t in tls_ids},'queues':queues,'queue':total})
    traci.close()
    data={'meta':{'controller':a.controller,'scenario':a.scenario,'steps':a.steps,'sampleEvery':a.sample_every,'intersections':len(tls_ids),'maxQueue':maxq,'adaptiveDecisions':decisions,'phaseChanges':phases,'network':'5x5 / 25 signalised intersections'},'frames':frames}
    Path(a.output).write_text(json.dumps(data,separators=(',',':')))
    print(json.dumps(data['meta'],indent=2)); print('frames',len(frames),'output',a.output)
if __name__=='__main__': main()
