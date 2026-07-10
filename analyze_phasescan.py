#!/usr/bin/env python3
"""analyze_phasescan.py -- apply the FROZEN PREREG_PHASE_SCAN_CDT_4D.md decision tree to a
results.jsonl and print the (kappa0,Delta) phase map. Frozen thresholds only; no post-hoc tuning."""
import sys, json, argparse
from collections import OrderedDict

def shape_class(ps, T):
    top=ps['top_frac']; r_max=ps['r_max']; n_empty=ps['n_empty']; cv=ps['cv']
    r2=ps['cos3_r2']; amp=ps.get('cos3_amp_frac',0); peaks=ps['peaks']
    if top>0.50 or (r_max>3 and n_empty>=T-2): return 'SPIKE'
    if cv<0.10 and r_max<1.5 and amp<0.30: return 'UNIFORM-TUBE'
    if r2>=0.80 and peaks==1 and amp>=0.40 and n_empty<=2: return 'COS3-BLOB'
    if peaks>=2 or r2<0.5: return 'MULTIMODAL'
    return 'EXTENDED-OTHER'

def classify(r):
    T=r['T']; ps=r['prof_scalars']; f_hub=r['f_hub']; r_H=r.get('r_H')
    ds_ir=r.get('ds_ir'); dds_rel=r.get('delta_ds_rel'); sat=r.get('saturated')
    plat=r.get('plateaued'); bad=r.get('census_bad',0)
    shape=shape_class(ps,T)
    if bad and bad>0: return 'DISCARD(census)', shape
    hub_dom=f_hub>=0.20; low_hub=f_hub<=0.08
    extended=shape in ('UNIFORM-TUBE','COS3-BLOB','EXTENDED-OTHER')
    if hub_dom and shape=='SPIKE': return 'B (crumpled)', shape
    if hub_dom and extended:      return 'C_b (bifurcation/hub)', shape
    if low_hub and shape=='MULTIMODAL' and (ds_ir is not None and ds_ir<3.5):
        return 'A (branched-polymer)', shape
    if (low_hub and shape=='COS3-BLOB' and not sat and r_H is not None and r_H>=0.90
            and ds_ir is not None and abs(ds_ir-r['bench_ds'])<=0.30 and ds_ir>3.13
            and dds_rel is not None and dds_rel<0 and plat):
        return 'C (de Sitter)', shape
    if low_hub and extended and (ds_ir is not None and ds_ir>3.5):
        return ('C-CANDIDATE (N0<1300, push vol)' if sat else 'C?-partial (low-hub extended)'), shape
    return 'AMBIGUOUS', shape

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("results"); ap.add_argument("--all",action="store_true")
    a=ap.parse_args()
    latest=OrderedDict()  # (k0,D)->record ; keep latest measured, else latest provisional
    for line in open(a.results):
        line=line.strip()
        if not line: continue
        r=json.loads(line); key=(r['k0'],r['D'])
        cur=latest.get(key)
        if cur is None or r['status']=='measured' or (cur['status']!='measured'):
            latest[key]=r
    rows=sorted(latest.values(), key=lambda r:(r['D'],r['k0']))
    print("%-5s %-5s %-11s %-7s %5s %6s %6s %5s %6s %6s %6s %6s %-22s %-13s"%(
        "k0","D","status","sw","N0","f_tl","f_hub","cv","r_H","ds_ir","Ddsrel","cos3","PHASE","shape"))
    for r in rows:
        ph,shape=classify(r); ps=r['prof_scalars']
        print("%-5s %-5s %-11s %-7s %5d %6.3f %6.3f %5.3f %6s %6s %6s %6s %-22s %-13s"%(
            r['k0'],r['D'],r['status'],r['sweeps'],r['N0'],r['f_tl'],r['f_hub'],r['prof_cv'],
            str(r.get('r_H')),str(r.get('ds_ir')),str(r.get('delta_ds_rel')),str(ps['cos3_r2']),ph,shape))
    k0s=sorted({r['k0'] for r in rows}); Ds=sorted({r['D'] for r in rows},reverse=True)
    print("\n(kappa0 ->) x (Delta v) phase grid:")
    print("       "+"".join("k0=%-6s"%k for k in k0s))
    for D in Ds:
        cells=[]
        for k in k0s:
            r=latest.get((k,D)); cells.append((classify(r)[0].split()[0] if r else '-'))
        print("D=%-4s "%D+"".join("%-8s"%c for c in cells))

if __name__=="__main__": main()
