#!/usr/bin/env python3
"""Urban Mobility Digital Twin v2 exporter: fixed, local adaptive, coordinated adaptive."""
import argparse, json, time, random
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
    p.add_argument('--controller',choices=['fixed','local-adaptive','coordinated-adaptive','ai-adaptive'],default='coordinated-adaptive')
    p.add_argument('--scenario',choices=list(ROUTES),default='rush-hour')
    p.add_argument('--steps',type=int,default=600)
    p.add_argument('--sample-every',type=int,default=3)
    p.add_argument('--output',default='viewer_data_v2.json')
    p.add_argument('--driver-policy',choices=['sumo-default','safe-ai'],default='sumo-default')
    a=p.parse_args()
    traci.start(['sumo','-n',str(NET),'-r',str(ROUTES[a.scenario]),'--end',str(a.steps),'--seed','42','--no-step-log','true','--no-warnings','true'])
    tls_ids=sorted(traci.trafficlight.getIDList()); groups=lane_groups(); neigh=neighbors(tls_ids)
    frames=[]; decisions=0; maxq=0; phases=0; last={t:-1 for t in tls_ids}
    ai_q={t:{} for t in tls_ids}; ai_prev={t:None for t in tls_ids}; ai_last_change={t:0.0 for t in tls_ids}; ai_rng=random.Random(42)
    min_green=12.0; max_green=60.0; alpha=.22; gamma=.86; epsilon=.08
    def ai_state(t, queues):
        local=queues[t]; ns=[queues[n] for n in neigh[t]]
        pressure=local-(sum(ns)/max(1,len(ns))) if ns else local
        return (min(8, local//2), min(8, max(-8, int(pressure))), min(3, traci.trafficlight.getPhase(t)//2))
    def ai_choose(t, state, remaining, now):
        # Actions: hold, extend green, or safely shorten only after minimum green.
        actions=[0,1] if remaining < max_green-1 else [0,2]
        if now-ai_last_change[t] < min_green: actions=[0]
        q=ai_q[t].setdefault(state,{a:0.0 for a in (0,1,2)})
        if ai_rng.random()<epsilon: return ai_rng.choice(actions)
        return max(actions,key=lambda a:q.get(a,0.0))
    while traci.simulation.getMinExpectedNumber()>0:
        traci.simulationStep()
        now=traci.simulation.getTime()
        queues={t:sum(traci.lane.getLastStepHaltingNumber(l) for l in ls) for t,ls in groups.items()}
        total=sum(queues.values()); maxq=max(maxq,total)
        if a.controller!='fixed':
            for t in tls_ids:
                ph=traci.trafficlight.getPhase(t)
                if ph!=last[t]:
                    phases+=1; last[t]=ph
                    if ph%2==0:
                        logic=traci.trafficlight.getAllProgramLogics(t)[0]; base=logic.phases[ph].duration
                        local=queues[t]; ns=[queues[n] for n in neigh[t]]
                        if a.controller=='local-adaptive': pressure=local-(sum(queues.values())/max(1,len(queues)))
                        elif a.controller=='coordinated-adaptive': pressure=local-(sum(ns)/max(1,len(ns))) if ns else local
                        else:
                            state=ai_state(t,queues); remaining=max(0.0,traci.trafficlight.getNextSwitch(t)-now)
                            reward=-float(total)-0.15*phases
                            previous=ai_prev[t]
                            if previous is not None:
                                ps,pa=previous; q=ai_q[t].setdefault(ps,{x:0.0 for x in (0,1,2)})
                                nq=ai_q[t].setdefault(state,{x:0.0 for x in (0,1,2)})
                                q[pa]+=alpha*(reward+gamma*max(nq.values())-q[pa])
                            action=ai_choose(t,state,remaining,now); ai_prev[t]=(state,action)
                            if action==1: pressure=max(1,local-(sum(ns)/max(1,len(ns))) if ns else local)
                            elif action==2: pressure=min(-1,local-(sum(ns)/max(1,len(ns))) if ns else local)
                            else: pressure=0
                        if a.controller!='ai-adaptive': extra=min(18,max(0,int(pressure*1.7)))
                        else: extra=max(-12,min(18,int(pressure*1.5)))
                        remaining=max(0.5,traci.trafficlight.getNextSwitch(t)-now)
                        target=max(0.5,min(max_green,remaining+extra))
                        if a.controller=='ai-adaptive' and extra<0 and now-ai_last_change[t]>=min_green: target=.2
                        traci.trafficlight.setPhaseDuration(t,target)
                        ai_last_change[t]=now if a.controller=='ai-adaptive' and extra!=0 else ai_last_change[t]
                        decisions += int(extra!=0)
        if int(traci.simulation.getTime())%a.sample_every==0:
            vehicles=[]
            for vid in traci.vehicle.getIDList():
                if a.driver_policy=='safe-ai':
                    # SUMO safety checks: right-of-way, braking and signal compliance;
                    # lane changes remain collision-safe and are not forced by the viewer.
                    traci.vehicle.setSpeedMode(vid,31)
                    traci.vehicle.setLaneChangeMode(vid,1621)
                x,y=traci.vehicle.getPosition(vid); speed=traci.vehicle.getSpeed(vid)
                vehicles.append({'id':vid,'x':round(x,2),'y':round(y,2),'a':round(traci.vehicle.getAngle(vid),1),'s':round(speed,2),'type':'vehicle','policy':a.driver_policy})
            frames.append({'t':round(traci.simulation.getTime(),1),'vehicles':vehicles,'signals':{t:traci.trafficlight.getPhase(t) for t in tls_ids},'queues':queues,'queue':total})
    traci.close()
    data={'meta':{'controller':a.controller,'controllerType':'online-constrained-q-learning' if a.controller=='ai-adaptive' else 'rule-based-adaptive','minGreen':min_green,'maxGreen':max_green,'vehicleSafety':'SUMO car-following + signal compliance','driverPolicy':a.driver_policy,'scenario':a.scenario,'steps':a.steps,'sampleEvery':a.sample_every,'intersections':len(tls_ids),'maxQueue':maxq,'adaptiveDecisions':decisions,'phaseChanges':phases,'network':'5x5 / 25 signalised intersections'},'frames':frames}
    Path(a.output).write_text(json.dumps(data,separators=(',',':')))
    print(json.dumps(data['meta'],indent=2)); print('frames',len(frames),'output',a.output)
if __name__=='__main__': main()
