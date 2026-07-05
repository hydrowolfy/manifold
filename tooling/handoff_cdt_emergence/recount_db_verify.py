import sys
VBASE=1000000
def VT(v): return v//VBASE
def parse(fn):
    states=[]; cur=None; tets=None
    for ln in open(fn):
        p=ln.split()
        if not p: continue
        if p[0]=='S':
            cur=dict(N0=int(p[1]),N3=int(p[2]),c23=int(p[3]),c32=int(p[4]),c26=int(p[5]),c62=int(p[6]),c44=int(p[7])); tets=[]
        elif p[0]=='T':
            tets.append(tuple(int(x) for x in p[1:5]))
        elif p[0]=='E':
            cur['tets']=tets; states.append(cur); cur=None
    return states
def tet_class(tv,T):
    slices={}
    for v in tv: slices.setdefault(VT(v),0); slices[VT(v)]+=1
    if len(slices)!=2: return 0
    ss=sorted(slices)  # two slice-times
    a,b=ss[0],ss[1]
    # which is lower: the one s.t. (upper-lower) mod T ==1
    if (b-a)%T==1: lo,hi=a,b
    elif (a-b)%T==1: lo,hi=b,a
    else: return 0   # not adjacent (shouldn't happen in foliation)
    cl,ch=slices[lo],slices[hi]
    if cl==3 and ch==1: return 31
    if cl==1 and ch==3: return 13
    if cl==2 and ch==2: return 22
    return 0
def recount(st,T):
    tets=st['tets']
    face={}; edge={}; vert={}
    cls={}
    for k,tv in enumerate(tets):
        cls[k]=tet_class(tv,T)
        vs=sorted(tv)
        # 4 faces
        for i in range(4):
            f=tuple(sorted(tv[j] for j in range(4) if j!=i)); face.setdefault(f,[]).append(k)
        # 6 edges
        for i in range(4):
            for j in range(i+1,4):
                e=tuple(sorted((tv[i],tv[j]))); edge.setdefault(e,[]).append(k)
        for v in tv: vert.setdefault(v,[]).append(k)
    N0=len(vert)
    # 23: timelike face shared by 2 tets, one (31|13) other 22
    c23=0
    for f,ks in face.items():
        if len(ks)!=2: continue
        if VT(f[0])==VT(f[1])==VT(f[2]): continue  # skip spatial
        a,b=cls[ks[0]],cls[ks[1]]
        a3=a in(31,13); b3=b in(31,13); a2=a==22; b2=b==22
        if (a3 and b2) or (a2 and b3): c23+=1
    # 26: spatial face shared by 2 tets, one 31 one 13
    c26=0
    for f,ks in face.items():
        if len(ks)!=2: continue
        if not(VT(f[0])==VT(f[1])==VT(f[2])): continue
        a,b=cls[ks[0]],cls[ks[1]]
        if (a==31 and b==13) or (a==13 and b==31): c26+=1
    # 32: timelike edge shared by 3 tets = one (31|13) + two 22
    c32=0
    for e,ks in edge.items():
        if len(ks)!=3: continue
        if VT(e[0])==VT(e[1]): continue
        n31=sum(1 for k in ks if cls[k] in(31,13)); n22=sum(1 for k in ks if cls[k]==22)
        if n31==1 and n22==2 and n31+n22==3: c32+=1
    # 62: spatial vertex order 6, 3x31+3x13 bipyramid (2 apices,3 base)
    c62=0
    for v,ks in vert.items():
        if len(ks)!=6: continue
        sT=VT(v); ok=True; n31=n13=0; apex=set(); base=set()
        for k in ks:
            cl=cls[k]
            if cl==31:n31+=1
            elif cl==13:n13+=1
            else: ok=False;break
            ap=None; bs=[]
            for w in tets[k]:
                if w==v: continue
                if VT(w)!=sT:
                    if ap is not None: ok=False
                    ap=w
                else: bs.append(w)
            if ap is None or len(bs)!=2: ok=False;break
            apex.add(ap); base.update(bs)
        if ok and len(apex)==2 and len(base)==3 and n31==3 and n13==3: c62+=1
    # 44: spacelike edge shared by 4 tets = diamond (2 spatial nbrs,2 up common apex,2 down common apex)
    c44=0
    for e,ks in edge.items():
        if len(ks)!=4: continue
        a,b=e
        if VT(a)!=VT(b): continue
        sT=VT(a); tp=(sT+1)%T; good=True; sp=set(); ups=[]; downs=[]
        for k in ks:
            ap=None; spn=None
            for w in tets[k]:
                if w==a or w==b: continue
                if VT(w)!=sT:
                    if ap is not None: good=False
                    ap=w
                else:
                    if spn is not None: good=False
                    spn=w
            if ap is None or spn is None: good=False;break
            sp.add(spn)
            if VT(ap)==tp: ups.append(ap)
            else: downs.append(ap)
        if good and len(sp)==2 and len(ups)==2 and len(set(ups))==1 and len(downs)==2 and len(set(downs))==1:
            c44+=1
    return dict(N0=N0,c23=c23,c32=c32,c26=c26,c62=c62,c44=c44)
if __name__=="__main__":
    fn=sys.argv[1]; T=int(sys.argv[2])
    sts=parse(fn); mism=0; keys=['N0','c23','c32','c26','c62','c44']
    for i,st in enumerate(sts):
        r=recount(st,T)
        for k in keys:
            if r[k]!=st[k]:
                mism+=1
                if mism<=8: print("MISMATCH state%d %s: sampler=%d indep=%d (N3=%d)"%(i,k,st[k],r[k],st['N3']))
    print("states=%d  total-field-mismatches=%d  (fields checked=%d)"%(len(sts),mism,len(sts)*len(keys)))
