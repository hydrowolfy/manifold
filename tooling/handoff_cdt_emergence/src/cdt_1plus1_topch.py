#!/usr/bin/env python3
"""FAITHFUL 1+1D generalized/CDT with SPATIAL TOPOLOGY CHANGE (baby universes).

Base substrate (validated, d_H->2): T periodic time slices; slice t is a spatial CIRCLE of
L[t] vertices; strip t->t+1 is a triangulated annulus = cyclic U/D word. Volume moves flip /
relocate keep N2 fixed (Ambjorn-Loll NPB536 (1998) 407).

GENERALIZATION: a slice may hold a MULTISET of spatial circles. A genuine baby universe is a
spatial-topology-change EVENT: an S^1 SPLITS into two circles; a baby circle evolves forward and
CAPS OFF (shrinks to nothing) a few slices later. Foliation preserved (time-ordered stack); only
per-slice spatial topology changes. Penalty mu per topology-change event (ALWZ g_s~e^{-mu};
arXiv:0709.2784; d_H=4/d_s=2 Liouville: Ambjorn-Watabiki NPB445).

REPRESENTATION (index-based, tuned so reverse-move combinatorics are explicit -> exact DB).
For each t: circles[t] = list of circles. Each circle = dict:
    v    : list of global vertex ids (spatial cycle, cyclic)
    to   : list of indices into circles[t+1] this circle glues UP to
           (len 1 => annulus; len 2 => split/pants); [] and kind='cap' => caps off
    kind : 'ann' | 'split' | 'cap'
    word : U/D word of the strip above this circle (over concatenated child boundary for split)
Topology-change events = splits + caps. build_graph assembles full multi-circle adjacency so
baby-universe volume is genuine geodesic volume behind a neck (no shortcut).
"""
import math, random, sys
from collections import deque, defaultdict, Counter

_NEXT = [0]
def newv():
    _NEXT[0] += 1
    return _NEXT[0]

# ------------------------------------------------------------------ state ----
def make_circle(L, kind='ann'):
    return {'v': [newv() for _ in range(L)], 'to': [], 'kind': kind, 'word': None}

def init_state(T, L0):
    _NEXT[0] = 0
    circles = [[make_circle(L0)] for _ in range(T)]
    for t in range(T):
        c = circles[t][0]
        c['to'] = [0]; c['kind'] = 'ann'; c['word'] = ['U','D']*L0
    return circles

def n_circles(circles): return sum(len(s) for s in circles)
def total_len(circles): return sum(len(c['v']) for s in circles for c in s)
def n_topch(circles):
    return sum(1 for s in circles for c in s if c['kind'] in ('split','cap'))
def N2(circles):
    # number of triangles = number of U + number of D over all strips = sum of word lengths
    return sum(len(c['word']) for s in circles for c in s if c['word'] is not None)

# ------------------------------------------------------------ build_graph ----
def build_graph(circles, T):
    adj = defaultdict(set)
    def add(a,b):
        if a!=b: adj[a].add(b); adj[b].add(a)
    for t in range(T):
        for c in circles[t]:
            v=c['v']; L=len(v)
            for i in range(L): add(v[i], v[(i+1)%L])
    for t in range(T):
        tn=(t+1)%T
        for c in circles[t]:
            bottom=c['v']
            if c['kind']=='ann':
                top=circles[tn][c['to'][0]]['v']
                _glue(add, bottom, top, c['word'])
            elif c['kind']=='split':
                cA=circles[tn][c['to'][0]]['v']; cB=circles[tn][c['to'][1]]['v']
                top=cA+cB
                _glue(add, bottom, top, c['word'])
                # seam vertices shared so pants is one connected neck (baby volume behind neck)
                add(cA[0], cB[0]); add(cA[-1], cB[-1])
            elif c['kind']=='cap':
                apex=('cap', bottom[0])
                for i in range(len(bottom)): add(bottom[i], apex)  # cone: L up-spokes to 1 apex
    return {k:set(v) for k,v in adj.items()}

def _glue(add, bottom, top, word):
    Lb,Lt=len(bottom),len(top); pi=pj=0
    for s in word:
        if s=='U':
            add(bottom[pi%Lb], top[pj%Lt]); add(bottom[(pi+1)%Lb], top[pj%Lt]); pi+=1
        else:
            add(bottom[pi%Lb], top[pj%Lt]); add(bottom[pi%Lb], top[(pj+1)%Lt]); pj+=1

# ------------------------------------------------------------------ check ----
def check(circles, T):
    for t in range(T):
        tn=(t+1)%T
        used=[False]*len(circles[tn])
        for c in circles[t]:
            L=len(c['v']); assert L>=3, "circle <3"
            if c['kind']=='ann':
                assert len(c['to'])==1
                top=circles[tn][c['to'][0]]['v']
                assert c['word'].count('U')==L, (c['word'].count('U'),L)
                assert c['word'].count('D')==len(top)
                used[c['to'][0]]=True
            elif c['kind']=='split':
                assert len(c['to'])==2 and c['to'][0]!=c['to'][1]
                lt=sum(len(circles[tn][j]['v']) for j in c['to'])
                assert c['word'].count('U')==L
                assert c['word'].count('D')==lt
                for j in c['to']: used[j]=True
            elif c['kind']=='cap':
                assert L>=3 and c['to']==[]
                assert c['word'] is not None and c['word'].count('U')==L and c['word'].count('D')==0
        assert all(used), "orphan circle in slice %d"%tn


# ============================================================================
# VOLUME MOVES (per-circle) -- flip (2,2) and relocate (2,4)/(4,2) volume xfer.
# These act within a single circle's strip word, exactly as the validated substrate,
# but generalized to select any circle in any slice.
# ============================================================================
def _all_circles(circles, T):
    return [(t,ci) for t in range(T) for ci in range(len(circles[t]))]

def move_flip(circles, T, rng):
    lst=[(t,ci) for (t,ci) in _all_circles(circles,T) if circles[t][ci]['word'] is not None]
    if not lst: return
    t,ci=rng.choice(lst); c=circles[t][ci]; w=c['word']; n=len(w)
    if n<2: return
    p=rng.randrange(n); a,b=w[p],w[(p+1)%n]
    if a!=b:
        w[p],w[(p+1)%n]=b,a

def move_relocate(circles, T, rng, Lmin=3, Lmax=400):
    """Move one vertex of spatial length from circle (td,cd) to circle (ti,ci):
    delete a U from cd's word + matching D from its parent's word; insert into ci.
    Keeps N2 fixed. Faithful generalization of substrate relocate; only touches ANNULUS
    circles (single parent/child) so words stay well-formed."""
    lst=[(t,ci) for (t,ci) in _all_circles(circles,T) if circles[t][ci]['kind']=='ann']
    if len(lst)<2: return False
    (td,cd)=rng.choice(lst); (ti,ci)=rng.choice(lst)
    cdel=circles[td][cd]; cins=circles[ti][ci]
    if (td,cd)==(ti,ci): return False
    if len(cdel['v'])<=Lmin or len(cins['v'])>=Lmax: return False
    # parent of cdel: the circle in slice td-1 whose child (annulus) is cd
    par=_annulus_parent(circles,T,td,cd)
    if par is None: return False
    us=[i for i,s in enumerate(cdel['word']) if s=='U']
    ds=[i for i,s in enumerate(par['word']) if s=='D']
    if not us or not ds: return False
    del cdel['word'][rng.choice(us)]; del par['word'][rng.choice(ds)]; cdel['v'].pop()
    # insert into cins
    pari=_annulus_parent(circles,T,ti,ci)
    if pari is None:
        # undo
        cdel['v'].append(newv()); cdel['word'].append('U'); par['word'].append('D'); return False
    cins['word'].insert(rng.randrange(len(cins['word'])+1),'U')
    pari['word'].insert(rng.randrange(len(pari['word'])+1),'D')
    cins['v'].append(newv())
    return True

def _annulus_parent(circles,T,tn,ci):
    """Return the parent circle of circles[tn][ci] ONLY if that parent is a plain annulus
    (1->1). Split parents are excluded so relocate never touches topology-change words."""
    tp=(tn-1)%T
    for c in circles[tp]:
        if c['kind']=='ann' and c['to'] and c['to'][0]==ci:
            return c
    return None

# ============================================================================
# TOPOLOGY-CHANGE MOVE:  SPROUT <-> ABSORB  (a minimal baby universe)
# ----------------------------------------------------------------------------
# A minimal baby universe = SPLIT at slice t (parent -> parent' + baby[3] in t+1) followed by
# CAP of that baby at slice t+2 (baby[3] caps to a cone apex). It shares the two seam vertices
# with the parent (couples to the volume/Pachner sector). This is TWO topology-change events
# (one split + one cap) -> penalty weight e^{-2 mu} for a minimal baby.
#
# SPROUT proposal: pick an ANNULUS circle c at slice t that stays annulus for >=2 steps
#   (child at t+1 is annulus, grandchild path exists), pick a U-position in c['word'] to
#   attach the seam. Turn c into a SPLIT producing (child_copy, baby3). The baby3 in slice t+1
#   is a fresh 3-circle whose strip above is a CAP. The child at t+1 must itself be able to
#   host the extra child index -> we append baby to circles[t+1].
# ABSORB proposal: pick an existing minimal-baby (a split whose second child is a len-3 circle
#   that caps at t+1). Remove it, restoring the plain annulus.
#
# DETAILED BALANCE (canonical, N2 held ~fixed by matching triangle count; here SPROUT changes
# N2 by a fixed +dN2, absorbed into the mu/lambda weight). Proposal combinatorics:
#   P(sprout at a specific slot) = 0.5 * 1/Nsprout_slots
#   P(absorb that baby)          = 0.5 * 1/Nbabies_after
# Acceptance: A_sprout = min(1, e^{-2 mu} e^{-lam*dN2} * Nsprout_slots / Nbabies_after )
#             A_absorb = min(1, e^{+2 mu} e^{+lam*dN2} * Nbabies_before / Nsprout_slots_after)
# where Nsprout_slots counts (annulus circle, U-position) candidates.
# ============================================================================

def _sprout_slots(circles, T):
    """List of (t, ci, up) candidate attachment slots: c=circles[t][ci] is annulus, its child
    is annulus (so grandchild path is clean), up is index of a 'U' in c['word']."""
    slots=[]
    for t in range(T):
        tn=(t+1)%T
        for ci,c in enumerate(circles[t]):
            if c['kind']!='ann': continue
            child=circles[tn][c['to'][0]]
            if child['kind']!='ann': continue
            for k,s in enumerate(c['word']):
                if s=='U':
                    slots.append((t,ci,k))
    return slots

def _babies(circles, T):
    """List of (t,ci) where circles[t][ci] is a SPLIT whose 2nd child (at t+1) is a len-3 CAP:
    a minimal baby, removable by ABSORB."""
    out=[]
    for t in range(T):
        tn=(t+1)%T
        for ci,c in enumerate(circles[t]):
            if c['kind']!='split': continue
            bj=c['to'][1]
            baby=circles[tn][bj]
            if len(baby['v'])==3 and baby['kind']=='cap':
                out.append((t,ci))
    return out

def _do_sprout(circles, T, t, ci, up):
    tn=(t+1)%T
    c=circles[t][ci]
    # baby: a fresh len-3 circle in slice t+1 that caps
    baby=make_circle(3, kind='cap'); baby['to']=[]; baby['word']=['U','U','U']
    circles[tn].append(baby); bj=len(circles[tn])-1
    # parent's original single child index
    ch0=c['to'][0]
    # turn c into split: children = [ch0, bj]; word gets 3 D's appended for baby's 3 top verts
    # Insert the baby's 3 D's right after the chosen U so the seam is local.
    # New word: same U's, plus 3 extra D's routed to baby (which sits at top-index >= len(child)).
    c['kind']='split'; c['to']=[ch0, bj]
    w=c['word'][:]
    # place 3 D's for the baby immediately after position 'up'
    for _ in range(3):
        w.insert(up+1, 'D')
    c['word']=w
    return bj

def _undo_sprout(circles, T, t, ci, bj):
    tn=(t+1)%T
    c=circles[t][ci]
    ch0=c['to'][0]
    c['kind']='ann'; c['to']=[ch0]
    # remove the 3 baby D's: remove the last-added 3 D's is ambiguous; recompute word to the
    # plain annulus word for child ch0. Its U-count must equal len(c['v']); D-count len(child).
    Lp=len(c['v']); Lc=len(circles[tn][ch0]['v'])
    # keep the U structure but strip baby D's: rebuild alternating-ish valid word.
    # Simplest exact inverse: remove exactly 3 D's that were inserted. We stored them contiguous.
    # Reconstruct by removing 3 consecutive D's.
    w=c['word']
    # find 3 consecutive D's and drop them
    for k in range(len(w)-2):
        if w[k]=='D' and w[k+1]=='D' and w[k+2]=='D':
            del w[k:k+3]; break
    c['word']=w
    # remove baby circle from slice tn
    del circles[tn][bj]
    # fix any 'to' indices in slice t pointing past bj
    for cc in circles[t]:
        cc['to']=[(j-1 if j>bj else j) for j in cc['to']]


# --- exact, record-based sprout/undo so reject restores the identical microstate ----------
def _do_sprout_rec(circles, T, t, ci, up):
    """Perform sprout; return a record sufficient for exact undo."""
    tn=(t+1)%T
    c=circles[t][ci]
    ch0=c['to'][0]
    baby=make_circle(3, kind='cap'); baby['to']=[]; baby['word']=['U','U','U']
    circles[tn].append(baby); bj=len(circles[tn])-1
    old_kind=c['kind']; old_to=c['to'][:]; old_word=c['word'][:]
    c['kind']='split'; c['to']=[ch0, bj]
    w=c['word'][:]
    for _ in range(3):
        w.insert(up+1,'D')
    c['word']=w
    return {'t':t,'ci':ci,'tn':tn,'bj':bj,'old_kind':old_kind,'old_to':old_to,'old_word':old_word}

def _undo_sprout_rec(circles, rec):
    t=rec['t']; ci=rec['ci']; tn=rec['tn']; bj=rec['bj']
    c=circles[t][ci]
    c['kind']=rec['old_kind']; c['to']=rec['old_to'][:]; c['word']=rec['old_word'][:]
    del circles[tn][bj]  # bj is always the LAST appended, so no index shift for others

def _split_parent_of(circles,T,tn,ci):
    """Return (parent_split_circle, slot) if circles[tn][ci] is the BABY child (2nd child)
    of a split in slice tn-1, else (None,None)."""
    tp=(tn-1)%T
    for c in circles[tp]:
        if c['kind']=='split' and len(c['to'])==2 and c['to'][1]==ci:
            return c
    return None

def move_baby_vol(circles, T, rng, Lmin=3, Lmax=200):
    """Volume-transfer between the baby (cap) sector and the mother (annulus) sector, N2-neutral.
    GROW-baby: remove one vertex from a random annulus circle (as relocate does: del U from its
      word + D from its annulus parent), and add one vertex to a random cap circle (add U to cap
      word + D to the cap's split-parent word).
    SHRINK-baby: exact reverse.
    Detailed balance: pick GROW/SHRINK w.p. 1/2. Candidate counts enter symmetrically because
    grow and shrink are exact inverses selecting from (annulus set) x (cap set). We use a
    Metropolis accept with the proposal-count ratio.
    """
    caps=[(t,ci) for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='cap']
    anns=[(t,ci) for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='ann']
    if not caps or len(anns)<1: return ('babyvol',False)
    grow=rng.random()<0.5
    if grow:
        # source annulus loses 1, cap gains 1
        cand_ann=[(t,ci) for (t,ci) in anns if len(circles[t][ci]['v'])>Lmin
                  and _annulus_parent(circles,T,t,ci) is not None]
        cand_cap=[(t,ci) for (t,ci) in caps if len(circles[t][ci]['v'])<Lmax
                  and _split_parent_of(circles,T,t,ci) is not None]
        if not cand_ann or not cand_cap: return ('babyvol',False)
        (ta,ca)=rng.choice(cand_ann); (tc,cc)=rng.choice(cand_cap)
        annc=circles[ta][ca]; capc=circles[tc][cc]
        parA=_annulus_parent(circles,T,ta,ca); parC=_split_parent_of(circles,T,tc,cc)
        us=[i for i,s in enumerate(annc['word']) if s=='U']
        ds=[i for i,s in enumerate(parA['word']) if s=='D']
        if not us or not ds: return ('babyvol',False)
        # forward candidate counts
        n_ann_f=len(cand_ann); n_cap_f=len(cand_cap)
        # perform
        del annc['word'][rng.choice(us)]; del parA['word'][rng.choice(ds)]; annc['v'].pop()
        capc['word'].append('U'); parC['word'].insert(rng.randrange(len(parC['word'])+1),'D')
        capc['v'].append(newv())
        # reverse candidate counts (for shrink): caps that can shrink, anns that can grow
        n_cap_r=len([1 for (t,ci) in [(t,ci) for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='cap']
                     if len(circles[t][ci]['v'])>Lmin and _split_parent_of(circles,T,t,ci) is not None])
        n_ann_r=len([1 for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='ann'
                     and len(circles[t][ci]['v'])<Lmax and _annulus_parent(circles,T,t,ci) is not None])
        A=(n_ann_f*n_cap_f)/max(1,(n_cap_r*n_ann_r))
        if rng.random()<min(1.0,A): return ('babyvol',True)
        # undo
        capc['v'].pop(); capc['word'].pop()
        di=[i for i,s in enumerate(parC['word']) if s=='D'][0]; del parC['word'][di]
        annc['v'].append(newv()); annc['word'].append('U'); parA['word'].append('D')
        return ('babyvol',False)
    else:
        # shrink: cap loses 1, annulus gains 1
        cand_cap=[(t,ci) for (t,ci) in caps if len(circles[t][ci]['v'])>Lmin
                  and _split_parent_of(circles,T,t,ci) is not None]
        cand_ann=[(t,ci) for (t,ci) in anns if len(circles[t][ci]['v'])<Lmax
                  and _annulus_parent(circles,T,t,ci) is not None]
        if not cand_cap or not cand_ann: return ('babyvol',False)
        n_cap_f=len(cand_cap); n_ann_f=len(cand_ann)
        (tc,cc)=rng.choice(cand_cap); (ta,ca)=rng.choice(cand_ann)
        capc=circles[tc][cc]; annc=circles[ta][ca]
        parC=_split_parent_of(circles,T,tc,cc); parA=_annulus_parent(circles,T,ta,ca)
        capc['v'].pop(); capc['word'].pop()
        di=[i for i,s in enumerate(parC['word']) if s=='D'][0]; del parC['word'][di]
        annc['word'].insert(rng.randrange(len(annc['word'])+1),'U')
        parA['word'].insert(rng.randrange(len(parA['word'])+1),'D'); annc['v'].append(newv())
        n_ann_r=len([1 for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='ann'
                     and len(circles[t][ci]['v'])>Lmin and _annulus_parent(circles,T,t,ci) is not None])
        n_cap_r=len([1 for t in range(T) for ci,c in enumerate(circles[t]) if c['kind']=='cap'
                     and len(circles[t][ci]['v'])<Lmax and _split_parent_of(circles,T,t,ci) is not None])
        A=(n_cap_f*n_ann_f)/max(1,(n_ann_r*n_cap_r))
        if rng.random()<min(1.0,A): return ('babyvol',True)
        annc['v'].pop()
        ui=[i for i,s in enumerate(annc['word']) if s=='U'][0]; del annc['word'][ui]
        di2=[i for i,s in enumerate(parA['word']) if s=='D'][0]; del parA['word'][di2]
        capc['word'].append('U'); parC['word'].insert(0,'D'); capc['v'].append(newv())
        return ('babyvol',False)

def move_topch(circles, T, mu, lam, rng):
    """One SPROUT or ABSORB attempt with EXACT detailed balance. Returns (label, accepted).
    dN2 = +3 for sprout (3 D-triangles of the capping baby; its 3 spatial edges + 3 up-edges
    are shared/seam). Two topology-change events (split+cap) => weight e^{-2 mu}."""
    dN2=3
    if rng.random()<0.5:  # SPROUT
        slots=_sprout_slots(circles,T)
        ns=len(slots)
        if ns==0: return ('sprout',False)
        t,ci,up=rng.choice(slots)
        rec=_do_sprout_rec(circles,T,t,ci,up)
        nb_after=len(_babies(circles,T))          # babies after sprout (>=1)
        A=math.exp(-2*mu)*math.exp(-lam*dN2)*ns/nb_after
        if rng.random()<min(1.0,A):
            return ('sprout',True)
        _undo_sprout_rec(circles,rec)
        return ('sprout',False)
    else:                 # ABSORB (reverse of sprout)
        babies=_babies(circles,T)
        nb=len(babies)
        if nb==0: return ('absorb',False)
        # pick a baby; to undo we need its up not required (undo uses stored old_word). But we
        # did not store rec. Reconstruct exact inverse: absorb = remove baby + strip 3 D's.
        t,ci=rng.choice(babies)
        tn=(t+1)%T
        c=circles[t][ci]; bj=c['to'][1]
        # ensure bj is last in slice tn (invariant: babies appended last & absorbed anytime).
        # If not last, swap it to last first (adjust references) to keep deletion index-safe.
        _ensure_last(circles,T,tn,bj); bj=len(circles[tn])-1
        c=circles[t][ci]
        ch0=c['to'][0]
        save_kind=c['kind']; save_to=c['to'][:]; save_word=c['word'][:]
        save_baby=circles[tn][bj]
        # perform absorb
        c['kind']='ann'; c['to']=[ch0]
        w=c['word'][:]
        # drop any 3 D's (words are equivalent up to U/D ordering; flips may have separated them)
        dpos=[k for k,s in enumerate(w) if s=='D']
        for k in sorted(dpos[:3], reverse=True):
            del w[k]
        c['word']=w
        removed_baby=circles[tn].pop(bj)
        ns_after=len(_sprout_slots(circles,T))
        A=(math.exp(+2*mu)*math.exp(+lam*dN2)*nb/ns_after) if ns_after>0 else 0.0
        if rng.random()<min(1.0,A):
            return ('absorb',True)
        # reject: restore identical microstate
        circles[tn].append(save_baby)
        c=circles[t][ci]; c['kind']=save_kind; c['to']=save_to[:]; c['word']=save_word[:]
        return ('absorb',False)

def _ensure_last(circles,T,tn,bj):
    """Swap circle bj to the last position of slice tn, updating all parent 'to' indices."""
    last=len(circles[tn])-1
    if bj==last: return
    circles[tn][bj],circles[tn][last]=circles[tn][last],circles[tn][bj]
    tp=(tn-1)%T
    for c in circles[tp]:
        c['to']=[last if j==bj else (bj if j==last else j) for j in c['to']]

# ============================================================================
# OBSERVABLES: d_H (ball growth) and d_s (spectral dimension, return probability)
# ============================================================================
def ball_growth_dH(adj, nsrc=24, seed=3, rlo=2, rhi=9):
    rng=random.Random(seed); nodes=list(adj)
    acc=defaultdict(float); cnt=defaultdict(int)
    for _ in range(nsrc):
        s=rng.choice(nodes); dist={s:0}; q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in dist: dist[v]=dist[u]+1; q.append(v)
        sh=Counter(dist.values()); rmax=max(dist.values()); cum=0
        for r in range(rmax+1):
            cum+=sh.get(r,0); acc[r]+=cum; cnt[r]+=1
    xs,ys=[],[]
    for r in range(rlo,rhi):
        if cnt.get(r): xs.append(math.log(r)); ys.append(math.log(acc[r]/cnt[r]))
    if len(xs)<2: return float('nan')
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((xs[i]-mx)**2 for i in range(n))
    if den==0: return float('nan')
    return sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den

def spectral_dim(adj, nsrc=12, tmax=40, seed=5, tlo=6, thi=30):
    """d_s from return probability of a lazy random walk: P(t) ~ t^{-d_s/2}.
    d_s = -2 d ln P / d ln t (linear fit on log-log in [tlo,thi])."""
    rng=random.Random(seed); nodes=list(adj)
    idx={u:k for k,u in enumerate(nodes)}
    Pacc=[0.0]*(tmax+1); ncnt=0
    for _ in range(nsrc):
        s=rng.choice(nodes)
        # probability vector via sparse dict
        p={s:1.0}
        deg={u:len(adj[u]) for u in adj}
        Pacc[0]+=1.0
        for tstep in range(1,tmax+1):
            np_={}
            for u,pu in p.items():
                stay=0.5*pu
                np_[u]=np_.get(u,0.0)+stay
                share=0.5*pu/deg[u]
                for v in adj[u]:
                    np_[v]=np_.get(v,0.0)+share
            p=np_
            Pacc[tstep]+=p.get(s,0.0)
        ncnt+=1
    P=[Pacc[k]/ncnt for k in range(tmax+1)]
    xs=[]; ys=[]
    for tstep in range(tlo,thi+1):
        if P[tstep]>0:
            xs.append(math.log(tstep)); ys.append(math.log(P[tstep]))
    if len(xs)<2: return float('nan'), P
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=sum((xs[i]-mx)**2 for i in range(n))
    slope=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den
    return -2*slope, P

# ============================================================================
# DRIVER
# ============================================================================
def run(T, L0, mu, lam, sweeps, seed=0, moves_per_sweep=None,
        p_flip=0.4, p_reloc=0.35, p_topch=0.25, record=False):
    rng=random.Random(seed)
    circles=init_state(T,L0)
    mps = moves_per_sweep or max(20, n_circles(circles)*3)
    hist=[]
    for sw in range(sweeps):
        for _ in range(mps):
            r=rng.random()
            if r<p_flip: move_flip(circles,T,rng)
            elif r<p_flip+p_reloc: move_relocate(circles,T,rng)
            elif r<p_flip+p_reloc+0.5*p_topch: move_topch(circles,T,mu,lam,rng)
            else: move_baby_vol(circles,T,rng)
        if record:
            hist.append((n_topch(circles), n_circles(circles), total_len(circles)))
    return circles, hist

if __name__=="__main__":
    print("FAITHFUL 1+1D CDT w/ spatial topology change. Quick smoke test.")
    circles,hist=run(20,12,mu=1.0,lam=0.0,sweeps=200,seed=1,record=True)
    check(circles,20)
    adj=build_graph(circles,20)
    print("  n_circles=%d  n_topch=%d  total_len=%d  |V|=%d"
          %(n_circles(circles),n_topch(circles),total_len(circles),len(adj)))
    print("  d_H=%.2f"%ball_growth_dH(adj))
