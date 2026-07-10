#!/usr/bin/env python3
"""
cdt4_phasescan.py -- STAGE 3 PART D: coarse (kappa0, Delta) phase-diagram scan for 3+1D
causal CDT. Reuses the VALIDATED cdt4_prod.py move set + cdt4_scan.py Metropolis engine
VERBATIM (imported, not reimplemented). Adds ONLY the preregistered order parameters of
PREREG_PHASE_SCAN_CDT_4D.md:
  OP1 profile shape : cv, r_max, r_min, n_empty, top_frac, cos3_r2, cos3_amp_frac, peaks
  OP2 hubs          : f_hub(deg>40), f_hub30, deg_mean/sd/max
  OP3 d_H(2-6) ratio r_H to matched-N0 flat-T^4 benchmark (linear interp m6<->m8)
  OP4 d_s flow      : ds_uv=d_s(4-12), ds_ir=d_s(8-24), delta_ds=uv-ir, delta_ds_rel vs
                      the measured flat-T^4 reference (+0.995 at N0=1296; UV-bias baseline)
  OP5               : f_tl=N32/N4, rho0=N0/N4
Thermalizes each (k0,D) to a plateau (drift test on N0,f_tl,cv over the last `win` sweeps,
after `min_sweeps`), checkpoints per point (resumable), and streams PROVISIONAL measures at
milestones for early signal. Writes results.jsonl + progress.txt + heartbeat.txt + START.log.
Stdlib only (no networkx). One uncontended run on the uncapped box; re-run to resume/extend.
"""
import sys, os, math, json, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdt4_prod as C
import cdt4_scan as SC

# ---- FROZEN measurement order (PREREG Sec 6); grid = kappa0{1,2.2,3.5,5} x Delta{0,.2,.4,.6}
FROZEN_ORDER = [(2.2,0.6),(2.2,0.0),(5.0,0.0),(1.0,0.6),(3.5,0.6),(5.0,0.6),
                (2.2,0.4),(2.2,0.2),(1.0,0.0),(3.5,0.0),(1.0,0.2),(3.5,0.2),
                (5.0,0.2),(1.0,0.4),(3.5,0.4),(5.0,0.4)]
# frozen flat-T^4 benchmark: N0 -> (d_s(8-24), d_H(2-6)); UV ref d_s(4-12)@m6 = 4.916 measured
BENCH = {1296:(4.117,2.656), 4096:(4.491,2.840)}
BENCH_DELTA_DS = 0.995   # measured flat-T^4 m6 d_s(4-12)-d_s(8-24): the estimator UV-bias baseline

def bench_interp(N0):
    lo,hi=1296,4096
    if N0<=lo: return BENCH[lo][0],BENCH[lo][1],True
    if N0>=hi: return BENCH[hi][0],BENCH[hi][1],False
    f=(N0-lo)/(hi-lo)
    return (BENCH[lo][0]+f*(BENCH[hi][0]-BENCH[lo][0]),
            BENCH[lo][1]+f*(BENCH[hi][1]-BENCH[lo][1]), False)

def cos3_fit(prof):
    """Fit N(t) ~ A*cos^3((t-t0)*pi/W)+c (A>0) over periodic t by t0,W grid search.
    Returns (R2, params=(A,c,t0,W))."""
    T=len(prof); mean=sum(prof)/T if T else 0.0
    sstot=sum((x-mean)**2 for x in prof) or 1e-9
    best=(-1e9,None)
    for t0i in range(T*4):
        t0=t0i/4.0
        for Wi in range(2,T*3):
            W=Wi/2.0; b=[]
            for t in range(T):
                d=(t-t0); d=(d+T/2.0)%T - T/2.0; ang=d*math.pi/W
                b.append(math.cos(ang)**3 if abs(ang)<math.pi/2 else 0.0)
            n=T; sb=sum(b); sbb=sum(x*x for x in b); sy=sum(prof); sby=sum(b[t]*prof[t] for t in range(T))
            det=n*sbb-sb*sb
            if abs(det)<1e-9: continue
            A=(n*sby-sb*sy)/det; c=(sy-A*sb)/n
            if A<=0: continue
            ssres=sum((prof[t]-(A*b[t]+c))**2 for t in range(T))
            r2=1-ssres/sstot
            if r2>best[0]: best=(r2,(round(A,1),round(c,1),round(t0,2),round(W,2)))
    return round(best[0],3), best[1]

def profile_scalars(prof):
    T=len(prof); mean=sum(prof)/T if T else 0.0
    if mean<=0:
        return dict(cv=0,r_max=0,r_min=0,n_empty=T,top_frac=0,cos3_r2=0,cos3=None,cos3_amp_frac=0,peaks=0)
    sd=math.sqrt(sum((x-mean)**2 for x in prof)/T); mx=max(prof); tot=sum(prof)
    n_empty=sum(1 for x in prof if x<0.15*mean)
    r2,params=cos3_fit(prof); peaks=0
    for t in range(T):
        if prof[t]>=0.5*mx and prof[t]>=prof[(t-1)%T] and prof[t]>=prof[(t+1)%T]: peaks+=1
    return dict(cv=round(sd/mean,4), r_max=round(mx/mean,3), r_min=round(min(prof)/mean,3),
                n_empty=n_empty, top_frac=round(mx/tot,3), cos3_r2=r2, cos3=params,
                cos3_amp_frac=(round(params[0]/mx,3) if params else 0.0), peaks=peaks)

def measure_ext(st, seeds=8, seedbase=1):
    """SC.measure (verbatim estimators) + preregistered extra order parameters."""
    m = SC.measure(st, seeds=seeds, dHw=((2,6),(3,8)), dSw=((4,12),(8,24),(10,30)),
                   tmax=40, nz=6, nsrc=16, seedbase=seedbase)
    adj=C.skeleton_adj(st); degs=[len(v) for v in adj.values()]
    dm=sum(degs)/len(degs); dsd=math.sqrt(sum((d-dm)**2 for d in degs)/len(degs))
    f_hub=sum(1 for d in degs if d>40)/len(degs); f_hub30=sum(1 for d in degs if d>30)/len(degs)
    ps=profile_scalars(m['profile']); ds=m['dS']
    ds_uv=(ds.get('4-12') or [None])[0]; ds_ir=(ds.get('8-24') or [None])[0]
    delta_ds=round(ds_uv-ds_ir,3) if (ds_uv is not None and ds_ir is not None) else None
    dsb,dhb,sat=bench_interp(st.N0); dH26=(m['dH'].get('2-6') or [None])[0]
    m.update(dict(deg_sd=round(dsd,2), f_hub=round(f_hub,3), f_hub30=round(f_hub30,3),
                  prof_scalars=ps, ds_uv=ds_uv, ds_ir=ds_ir, delta_ds=delta_ds,
                  delta_ds_bench=BENCH_DELTA_DS,
                  delta_ds_rel=(round(delta_ds-BENCH_DELTA_DS,3) if delta_ds is not None else None),
                  bench_ds=round(dsb,3), bench_dH=round(dhb,3),
                  r_H=(round(dH26/dhb,3) if dH26 else None),
                  ds_offset=(round(ds_ir-dsb,3) if ds_ir is not None else None),
                  saturated=(sat or st.N0<1300), rho0=round(st.N0/max(st.N4,1),4)))
    return m

def drift(ys):
    n=len(ys)
    if n<3: return 1.0
    xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((x-mx)**2 for x in xs) or 1e-9
    slope=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den
    return abs(slope*n/(my if abs(my)>1e-9 else 1e-9))

def emit(results, prog, a, st, meta, k0, D, plateaued, status):
    m=measure_ext(st,seeds=a.meas_seeds,seedbase=1)
    rem=None
    if status=='measured':
        m2=measure_ext(st,seeds=a.meas_seeds,seedbase=501)
        rem=dict(ds_uv=m2['ds_uv'],ds_ir=m2['ds_ir'],delta_ds=m2['delta_ds'],
                 dH=m2['dH'].get('2-6'),f_hub=m2['f_hub'])
    rec=dict(status=status,k0=k0,D=D,T=a.T,N4t=a.N4t,eps=a.eps,sweeps=meta['sweeps_done'],
             plateaued=plateaued,census_bad=st.census()[0])
    for kk,vv in m.items(): rec[kk]=vv
    rec['remeasure']=rem
    with open(results,"a") as f: f.write(json.dumps(rec)+"\n")
    with open(prog,"a") as f:
        f.write("[%s] %s k0=%s D=%s sw=%d plat=%s N0=%d N4=%d f_tl=%s cv=%s f_hub=%s r_H=%s "
                "dS{4-12=%s,8-24=%s} Dds=%s Ddsrel=%s rho0=%s sat=%s cos3R2=%s amp=%s top=%s\n"%(
                time.strftime('%H:%M:%S'),status,k0,D,meta['sweeps_done'],plateaued,m['N0'],m['N4'],
                m['f_tl'],m['prof_cv'],m['f_hub'],m['r_H'],m['ds_uv'],m['ds_ir'],m['delta_ds'],
                m['delta_ds_rel'],m['rho0'],m['saturated'],m['prof_scalars']['cos3_r2'],
                m['prof_scalars']['cos3_amp_frac'],m['prof_scalars']['top_frac']))
    return m

def run_scan(a):
    scr=a.scratch; os.makedirs(scr,exist_ok=True)
    results=os.path.join(scr,"results.jsonl"); prog=os.path.join(scr,"progress.txt")
    hb=os.path.join(scr,"heartbeat.txt"); startlog=os.path.join(scr,"START.log")
    milestones=set(int(x) for x in a.provisional_at.split(",") if x.strip())
    with open(os.path.join(scr,"RUNNER.pid"),"w") as f: f.write(str(os.getpid()))
    with open(startlog,"a") as f:
        f.write("START %s pid=%d T=%d N4t=%d eps=%s min=%d win=%d cap=%d order=%s\n"%(
            time.strftime('%Y-%m-%d %H:%M:%S'),os.getpid(),a.T,a.N4t,a.eps,
            a.min_sweeps,a.win,a.cap_sweeps,FROZEN_ORDER))
    base=os.path.join(scr,"base_T%d_N%d.pkl"%(a.T,a.N4t))
    if not os.path.exists(base):
        rng=random.Random(a.seed); st0=C.seed_flat(a.T)
        SC.grow_to(st0,int(a.N4t*a.overgrow),rng)   # grow ABOVE target -> irregularize + approach from above
        SC.save_ckpt(st0,rng,dict(kind="base",sweeps_done=0),base)
        with open(startlog,"a") as f:
            f.write("BASE grown N4=%d N0=%d census=%s\n"%(st0.N4,st0.N0,st0.census()))
    done=set()
    if os.path.exists(results):
        for line in open(results):
            try: r=json.loads(line)
            except Exception: continue
            if r.get('status')=='measured': done.add((r['k0'],r['D']))
    order=FROZEN_ORDER[:a.maxpoints] if a.maxpoints else FROZEN_ORDER
    for (k0,D) in order:
        if (k0,D) in done: continue
        tag="pt_T%d_N%d_k%s_D%s"%(a.T,a.N4t,k0,D)
        ckpt=os.path.join(scr,tag+".pkl"); plog=os.path.join(scr,tag+".jsonl")
        if os.path.exists(ckpt):
            try:
                st,rng,meta=SC.load_ckpt(ckpt); _=st.N4; hist=meta.get('hist',[])
            except Exception as e:
                with open(startlog,"a") as f: f.write("WARN point ckpt %s unreadable (%s) -> restart this point from base\n"%(tag,type(e).__name__))
                st,rng,meta=SC.load_ckpt(base); meta=dict(sweeps_done=0,k0=k0,D=D,prov_done=[]); hist=[]
        else:
            st,rng,meta=SC.load_ckpt(base); meta=dict(sweeps_done=0,k0=k0,D=D,prov_done=[]); hist=[]
        p=dict(k0=k0,D=D,k4=a.k4,eps=a.eps,N4t=a.N4t); sl=a.sweep_len or a.N4t
        prov_done=set(meta.get('prov_done',[])); plateaued=False
        while meta['sweeps_done']<a.cap_sweeps:
            SC.sweep(st,p,rng,sl); meta['sweeps_done']+=1
            b,u=st.census()
            prof=C.slice_profile(st); mean=sum(prof)/len(prof) if prof else 0.0
            cv=math.sqrt(sum((x-mean)**2 for x in prof)/len(prof))/mean if mean>0 else 0.0
            f_tl=st.n32/max(st.N4,1); hist.append((st.N0,round(f_tl,4),round(cv,4))); meta['hist']=hist
            with open(hb,"w") as f:
                f.write("ALIVE %s | pt k0=%s D=%s | sweep %d/%d | N0=%d N4=%d f_tl=%.3f cv=%.3f | census_bad=%d\n"%(
                    time.strftime('%H:%M:%S'),k0,D,meta['sweeps_done'],a.cap_sweeps,st.N0,st.N4,f_tl,cv,b))
            with open(plog,"a") as f:
                f.write(json.dumps(dict(sweep=meta['sweeps_done'],N0=st.N0,N4=st.N4,
                        f_tl=round(f_tl,4),cv=round(cv,4),census_bad=b))+"\n")
            if meta['sweeps_done']%a.ckpt_every==0: SC.save_ckpt(st,rng,meta,ckpt)
            if meta['sweeps_done'] in milestones and meta['sweeps_done'] not in prov_done:
                emit(results,prog,a,st,meta,k0,D,False,'provisional')
                prov_done.add(meta['sweeps_done']); meta['prov_done']=sorted(prov_done)
                SC.save_ckpt(st,rng,meta,ckpt)
            if meta['sweeps_done']>=a.min_sweeps and len(hist)>=a.win:
                w=hist[-a.win:]
                if (drift([h[0] for h in w])<0.05 and drift([h[1] for h in w])<0.05
                        and (drift([h[2] for h in w])<0.05 or sum(x[2] for x in w)/len(w)<0.05)):  # cv-drift gate exempt for uniform (cv<0.05) states (PREREG Sec6 deviation, logged)
                    plateaued=True; break
        SC.save_ckpt(st,rng,meta,ckpt)
        emit(results,prog,a,st,meta,k0,D,plateaued,'measured')
        with open(hb,"w") as f: f.write("DONE pt k0=%s D=%s sweep %d plateau=%s\n"%(k0,D,meta['sweeps_done'],plateaued))
    with open(startlog,"a") as f: f.write("SCAN COMPLETE %s\n"%time.strftime('%Y-%m-%d %H:%M:%S'))
    print("scan complete")

def bench_mode(a):
    st=C.seed_flat(a.bench_m); m=measure_ext(st,seeds=a.meas_seeds,seedbase=1)
    print("BENCH m=%d N0=%d: dH=%s dS=%s f_hub=%s cos3R2=%s amp=%s"%(
        a.bench_m,st.N0,m['dH'],m['dS'],m['f_hub'],m['prof_scalars']['cos3_r2'],m['prof_scalars']['cos3_amp_frac']))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scan",action="store_true"); ap.add_argument("--bench",action="store_true")
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--T",type=int,default=6); ap.add_argument("--N4t",type=int,default=42000)
    ap.add_argument("--eps",type=float,default=0.002); ap.add_argument("--k4",type=float,default=0.0)
    ap.add_argument("--overgrow",type=float,default=1.15); ap.add_argument("--sweep-len",type=int,default=0)
    ap.add_argument("--min-sweeps",type=int,default=600)   # PREREG Sec 6: >=600 sweeps past grow
    ap.add_argument("--win",type=int,default=300)          # PREREG Sec 6: drift over last 300 sweeps
    ap.add_argument("--cap-sweeps",type=int,default=1500)
    ap.add_argument("--provisional-at",type=str,default="150,300,600")
    ap.add_argument("--ckpt-every",type=int,default=5); ap.add_argument("--meas-seeds",type=int,default=8)
    ap.add_argument("--maxpoints",type=int,default=0); ap.add_argument("--seed",type=int,default=0)
    ap.add_argument("--scratch",type=str,default="out"); ap.add_argument("--bench-m",type=int,default=6)
    a=ap.parse_args()
    if a.bench: return bench_mode(a)
    if a.selftest:
        print("DB", SC.db_check()); return
    if a.scan: return run_scan(a)
    ap.print_help()

if __name__=="__main__":
    main()
