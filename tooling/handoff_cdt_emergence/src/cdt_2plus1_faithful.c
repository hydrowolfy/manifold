/* cdt_2plus1.c -- fast C port of the 2+1D CDT bulk (v2) TetComplex Monte Carlo.
 *
 * Reproduces the physics of cdt_2plus1.py (TetComplex + bulk ergodic moves):
 *   moves (2,3)/(3,2), (2,6)/(6,2), (4,4) on a closed foliated causal 3-manifold
 *   with S^2 (chi=2) spatial slices; action S = -k0*N0 + k3*N3 + eps*(N3-Nbar)^2.
 *
 * Vertices are (time,index) encoded as one 32-bit int: v = t*VBASE + i.
 * A tetrahedron is 4 sorted vertex codes.
 *
 * Adjacency maps (face->tets, edge->tets, vertex->tets) and per-slice spatial
 * (V,E,F) counts are maintained INCREMENTALLY -> each proposal is O(local).
 *
 * Compile: gcc -O3 -march=native -o cdt2p1 cdt_2plus1.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

#define VBASE  1000000
#define VT(v)  ((int)((v) / VBASE))
#define VI(v)  ((int)((v) % VBASE))

/* ---- xoshiro256** ------------------------------------------------------- */
static uint64_t rng_s[4];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static uint64_t rng_next(void){
    uint64_t r=rotl(rng_s[1]*5,7)*9, t=rng_s[1]<<17;
    rng_s[2]^=rng_s[0]; rng_s[3]^=rng_s[1]; rng_s[1]^=rng_s[2]; rng_s[0]^=rng_s[3];
    rng_s[2]^=t; rng_s[3]=rotl(rng_s[3],45); return r;
}
static void rng_seed(uint64_t seed){
    for(int i=0;i<4;i++){ seed+=0x9E3779B97F4A7C15ULL; uint64_t z=seed;
        z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL;
        rng_s[i]=z^(z>>31);} }
static inline double rng_double(void){return (rng_next()>>11)*(1.0/9007199254740992.0);}
static inline uint64_t rng_below(uint64_t n){return n?rng_next()%n:0;}

typedef int32_t i32;

/* ---- tet table ---------------------------------------------------------- */
static i32 *TV=NULL;
static int ntet_cap=0, ntet_used=0;
static int *freelist=NULL, nfree=0, freelist_cap=0;
static int N3=0, T=0, next_idx_max=0; static int gN0=0;

static void ensure_tet_cap(int need){ if(need<=ntet_cap)return;
    int nc=ntet_cap?ntet_cap*2:8192; while(nc<need)nc*=2;
    TV=realloc(TV,(size_t)nc*4*sizeof(i32)); ntet_cap=nc; }
static void freelist_push(int k){ if(nfree>=freelist_cap){freelist_cap=freelist_cap?freelist_cap*2:2048;
    freelist=realloc(freelist,freelist_cap*sizeof(int));} freelist[nfree++]=k; }
static int freelist_pop(void){return nfree>0?freelist[--nfree]:-1;}

/* ---- hash map ----------------------------------------------------------- */
typedef struct { i32 v[3]; int cnt; int cap; int *t; uint8_t used; } Slot;
typedef struct { Slot*slot; int cap; int mask; int size; } HMap;
static uint64_t hash3(i32 a,i32 b,i32 c){ uint64_t h=1469598103934665603ULL; i32 k[3]={a,b,c};
    for(int i=0;i<3;i++){h^=(uint32_t)k[i]; h*=1099511628211ULL;} return h; }
static void hmap_init(HMap*m,int cap){m->cap=cap;m->mask=cap-1;m->size=0;m->slot=calloc(cap,sizeof(Slot));}
static Slot* hmap_get(HMap*m,i32 a,i32 b,i32 c,int create);
static void hmap_grow(HMap*m){ int oc=m->cap; Slot*old=m->slot; m->cap*=2; m->mask=m->cap-1; m->size=0;
    m->slot=calloc(m->cap,sizeof(Slot));
    for(int i=0;i<oc;i++) if(old[i].used){ Slot*d=hmap_get(m,old[i].v[0],old[i].v[1],old[i].v[2],1);
        d->cnt=old[i].cnt; d->cap=old[i].cap; d->t=old[i].t; } free(old); }
static Slot* hmap_get(HMap*m,i32 a,i32 b,i32 c,int create){
    if(create && (m->size+1)*10>=m->cap*7) hmap_grow(m);
    uint64_t h=hash3(a,b,c); int idx=h&m->mask;
    while(1){ Slot*s=&m->slot[idx];
        if(!s->used){ if(!create)return NULL; s->used=1; s->v[0]=a;s->v[1]=b;s->v[2]=c; s->cnt=0; s->cap=0; s->t=NULL; m->size++; return s; }
        if(s->v[0]==a&&s->v[1]==b&&s->v[2]==c) return s;
        idx=(idx+1)&m->mask; }
}
static inline void slot_add(Slot*s,int k){
    if(s->cnt>=s->cap){ s->cap=s->cap?s->cap*2:4; s->t=realloc(s->t,s->cap*sizeof(int)); }
    s->t[s->cnt++]=k; }
static inline void slot_del(Slot*s,int k){
    for(int i=0;i<s->cnt;i++) if(s->t[i]==k){ s->t[i]=s->t[s->cnt-1]; s->cnt--; return; } }
static HMap FACE,EDGE,VERT;
static int *sliceV=NULL,*sliceE=NULL,*sliceF=NULL;

static inline void sort4(i32*a){ for(int i=1;i<4;i++){i32 x=a[i];int j=i-1;while(j>=0&&a[j]>x){a[j+1]=a[j];j--;}a[j+1]=x;} }
static inline void tet_faces(const i32*v,i32 f[4][3]){
    f[0][0]=v[1];f[0][1]=v[2];f[0][2]=v[3];
    f[1][0]=v[0];f[1][1]=v[2];f[1][2]=v[3];
    f[2][0]=v[0];f[2][1]=v[1];f[2][2]=v[3];
    f[3][0]=v[0];f[3][1]=v[1];f[3][2]=v[2]; }

static inline void slice_face_delta(const i32*fv,int dir){ if(VT(fv[0])==VT(fv[1])&&VT(fv[1])==VT(fv[2])) sliceF[VT(fv[0])]+=dir; }
static inline void slice_edge_delta(i32 a,i32 b,int dir){ if(VT(a)==VT(b)) sliceE[VT(a)]+=dir; }
static inline void slice_vert_delta(i32 a,int dir){ sliceV[VT(a)]+=dir; gN0+=dir; }

static void register_tet(int k){
    i32 v[4]={TV[4*k],TV[4*k+1],TV[4*k+2],TV[4*k+3]}; i32 f[4][3]; tet_faces(v,f);
    for(int i=0;i<4;i++){ Slot*s=hmap_get(&FACE,f[i][0],f[i][1],f[i][2],1); if(s->cnt==0)slice_face_delta(f[i],+1); slot_add(s,k);}
    for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){ Slot*s=hmap_get(&EDGE,v[a],v[b],-1,1); if(s->cnt==0)slice_edge_delta(v[a],v[b],+1); slot_add(s,k);}
    for(int a=0;a<4;a++){ Slot*s=hmap_get(&VERT,v[a],-1,-1,1); if(s->cnt==0)slice_vert_delta(v[a],+1); slot_add(s,k);}
}
static void unregister_tet(int k){
    i32 v[4]={TV[4*k],TV[4*k+1],TV[4*k+2],TV[4*k+3]}; i32 f[4][3]; tet_faces(v,f);
    for(int i=0;i<4;i++){ Slot*s=hmap_get(&FACE,f[i][0],f[i][1],f[i][2],0); if(s){slot_del(s,k); if(s->cnt==0)slice_face_delta(f[i],-1);} }
    for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){ Slot*s=hmap_get(&EDGE,v[a],v[b],-1,0); if(s){slot_del(s,k); if(s->cnt==0)slice_edge_delta(v[a],v[b],-1);} }
    for(int a=0;a<4;a++){ Slot*s=hmap_get(&VERT,v[a],-1,-1,0); if(s){slot_del(s,k); if(s->cnt==0)slice_vert_delta(v[a],-1);} }
}
static int add_tet(i32 a,i32 b,i32 c,i32 d){
    i32 v[4]={a,b,c,d}; sort4(v);
    int k=freelist_pop(); if(k<0){ensure_tet_cap(ntet_used+1); k=ntet_used++;}
    TV[4*k]=v[0];TV[4*k+1]=v[1];TV[4*k+2]=v[2];TV[4*k+3]=v[3];
    register_tet(k); N3++; return k;
}
static void del_tet(int k){ unregister_tet(k); TV[4*k]=-1; freelist_push(k); N3--; }

static inline i32 other_vertex(int k,i32 a,i32 b,i32 c){
    for(int i=0;i<4;i++){i32 v=TV[4*k+i]; if(v!=a&&v!=b&&v!=c) return v;} return -1; }

/* ---- validity ----------------------------------------------------------- */
static int faces_all_closed(int*new_k,int nnew){
    for(int n=0;n<nnew;n++){ int k=new_k[n]; i32 v[4]={TV[4*k],TV[4*k+1],TV[4*k+2],TV[4*k+3]}; i32 f[4][3]; tet_faces(v,f);
        for(int i=0;i<4;i++){ Slot*s=hmap_get(&FACE,f[i][0],f[i][1],f[i][2],0); if(!s||s->cnt!=2) return 0; } }
    return 1;
}
static int foliation_ok_tets(int*new_k,int nnew){
    for(int n=0;n<nnew;n++){ int k=new_k[n]; int tset[4],ns=0;
        for(int i=0;i<4;i++){ int t=VT(TV[4*k+i]),seen=0; for(int j=0;j<ns;j++) if(tset[j]==t)seen=1; if(!seen)tset[ns++]=t; }
        if(ns>2) return 0;
        if(ns==2){ int a=tset[0],b=tset[1]; int dt=((b-a)%T+T)%T; if(dt!=1&&dt!=T-1) return 0; } }
    return 1;
}
/* ---- FIX (C): full simplicial-manifold gate ----------------------------- */
/* A slice-Euler chi==2 is necessary but NOT sufficient: a pinched pseudo-
 * sphere (two cones joined at a vertex) also has chi=2. We add the genuine
 * manifold test: (i) chi==2 per touched slice, and (ii) every touched vertex
 * has a link that is a SINGLE cycle (in-slice, spacelike edges) with no pinch,
 * i.e. the vertex is not a cut-vertex of its own link and the link edges form
 * one closed loop. We test this by walking the spatial-triangle fan around the
 * vertex within its slice: the opposite spacelike edges of the incident
 * spatial triangles must form exactly one cycle covering all of them. */

/* collect the distinct vertices touched by a set of new tets */
static int gather_verts(int*ks,int nk,i32*out,int cap){
    int n=0;
    for(int a=0;a<nk;a++){int k=ks[a];
        for(int i=0;i<4;i++){ i32 v=TV[4*k+i]; int seen=0; for(int j=0;j<n;j++) if(out[j]==v)seen=1;
            if(!seen && n<cap) out[n++]=v; } }
    return n;
}
/* vertex-link-in-slice single-cycle test. For vertex v in slice t, gather all
 * spatial triangles (all 3 verts in slice t) containing v. Each contributes the
 * opposite spacelike edge (the two other verts). The link is the graph on those
 * edges; v is a good (manifold, unpinched) spatial vertex iff that edge set is a
 * single closed cycle: every endpoint has degree exactly 2 and the whole thing
 * is one connected loop. Returns 1 if OK. */
static int vertex_link_ok(i32 v){
    int t=VT(v);
    Slot*sv=hmap_get(&VERT,v,-1,-1,0); if(!sv||sv->cnt==0) return 0;
    /* collect distinct in-slice link edges (a,b) from spatial triangles at v */
    i32 ea[256],eb[256]; int ne=0;
    for(int q=0;q<sv->cnt;q++){ int k=sv->t[q];
        /* the 4 faces; pick the spatial triangle(s) containing v */
        i32 vv[4]={TV[4*k],TV[4*k+1],TV[4*k+2],TV[4*k+3]}; i32 f[4][3]; tet_faces(vv,f);
        for(int fi=0;fi<4;fi++){ i32 x=f[fi][0],y=f[fi][1],z=f[fi][2];
            if(VT(x)!=t||VT(y)!=t||VT(z)!=t) continue;         /* spatial tri only */
            if(x!=v&&y!=v&&z!=v) continue;                     /* must contain v */
            i32 p=-1,r=-1; if(x==v){p=y;r=z;} else if(y==v){p=x;r=z;} else {p=x;r=y;}
            if(p>r){i32 tt=p;p=r;r=tt;}
            int seen=0; for(int e=0;e<ne;e++) if(ea[e]==p&&eb[e]==r){seen=1;break;}
            if(!seen && ne<256){ ea[ne]=p; eb[ne]=r; ne++; }
        }
    }
    if(ne<3) return 0;               /* a manifold vertex link has >=3 edges */
    /* degree of each endpoint must be exactly 2 (no pinch, no boundary) */
    i32 nodes[512]; int deg[512]; int nn=0;
    for(int e=0;e<ne;e++){ i32 en[2]={ea[e],eb[e]};
        for(int s=0;s<2;s++){ int idx=-1; for(int m=0;m<nn;m++) if(nodes[m]==en[s]){idx=m;break;}
            if(idx<0){ if(nn>=512)return 0; nodes[nn]=en[s]; deg[nn]=0; idx=nn; nn++; }
            deg[idx]++; } }
    for(int m=0;m<nn;m++) if(deg[m]!=2) return 0;   /* pinched/branched link */
    /* single connected cycle: walk from edge 0, must return after visiting all ne */
    int used[256]={0}; used[0]=1; i32 start=ea[0], cur=eb[0]; int count=1;
    while(cur!=start && count<=ne){
        int found=-1;
        for(int e=0;e<ne;e++){ if(used[e])continue;
            if(ea[e]==cur){ used[e]=1; cur=eb[e]; found=e; break; }
            if(eb[e]==cur){ used[e]=1; cur=ea[e]; found=e; break; } }
        if(found<0) break; count++;
    }
    if(cur!=start) return 0;          /* did not close */
    if(count!=ne) return 0;           /* multiple components (pinch) */
    return 1;
}
static int slices_chi_ok(int*ts,int nt){
    for(int i=0;i<nt;i++){ int s=ts[i]; if(sliceF[s]==0) return 0;
        if(sliceV[s]-sliceE[s]+sliceF[s]!=2) return 0; }
    return 1;
}
/* full gate: chi + every touched vertex's link a single cycle. new_k = new tets */
static int manifold_gate(int*ts,int nt,int*new_k,int nnew){
    if(!slices_chi_ok(ts,nt)) return 0;
    i32 vv[64]; int nvv=gather_verts(new_k,nnew,vv,64);
    for(int i=0;i<nvv;i++) if(!vertex_link_ok(vv[i])) return 0;
    return 1;
}
static inline void add_touch(int*ts,int*nt,int s){ for(int i=0;i<*nt;i++) if(ts[i]==s) return; ts[(*nt)++]=s; }

/* replace old tets (slot idxs) by new tets (vertex quads). On success returns 1
 * and fills created[] with new slot idxs and removed_verts[] with the removed
 * tets' verts so the caller can UNDO a valid-but-Metropolis-rejected move. */
#define MAXOLD 8
#define MAXNEW 8
static int last_created[MAXNEW], last_ncreated;
static i32 last_removed[MAXOLD][4]; static int last_nremoved;
static int last_nextidx_before;

static int apply_replace(int*old_idx,int nold,i32 newv[][4],int nnew){
    int touch[16],nt=0; i32 old_verts[MAXOLD][4];
    for(int i=0;i<nold;i++){int k=old_idx[i]; for(int j=0;j<4;j++){old_verts[i][j]=TV[4*k+j]; add_touch(touch,&nt,VT(TV[4*k+j]));}}
    for(int i=0;i<nnew;i++) for(int j=0;j<4;j++) add_touch(touch,&nt,VT(newv[i][j]));
    for(int i=0;i<nold;i++) del_tet(old_idx[i]);
    int new_k[MAXNEW];
    for(int i=0;i<nnew;i++){
        i32 a=newv[i][0],b=newv[i][1],c=newv[i][2],d=newv[i][3];
        if(a==b||a==c||a==d||b==c||b==d||c==d){
            for(int q=0;q<i;q++) del_tet(new_k[q]);
            for(int q=0;q<nold;q++) add_tet(old_verts[q][0],old_verts[q][1],old_verts[q][2],old_verts[q][3]);
            return 0; }
        new_k[i]=add_tet(a,b,c,d);
    }
    if(faces_all_closed(new_k,nnew)&&foliation_ok_tets(new_k,nnew)&&manifold_gate(touch,nt,new_k,nnew)){
        last_ncreated=nnew; for(int i=0;i<nnew;i++) last_created[i]=new_k[i];
        last_nremoved=nold; for(int i=0;i<nold;i++) for(int j=0;j<4;j++) last_removed[i][j]=old_verts[i][j];
        return 1;
    }
    for(int i=0;i<nnew;i++) del_tet(new_k[i]);
    for(int i=0;i<nold;i++) add_tet(old_verts[i][0],old_verts[i][1],old_verts[i][2],old_verts[i][3]);
    return 0;
}
/* undo the last successful apply_replace (used when Metropolis rejects) */
static void undo_last(void){
    for(int i=0;i<last_ncreated;i++) del_tet(last_created[i]);
    for(int i=0;i<last_nremoved;i++) add_tet(last_removed[i][0],last_removed[i][1],last_removed[i][2],last_removed[i][3]);
}

/* ---- FIX (A)+(D): tet classification + redex (proposal) counters --------- */
/* classify a live tet by (#verts on lower slice, #verts on upper slice):
 *   returns 31 for (3,1), 13 for (1,3), 22 for (2,2), 0 otherwise. */
static int tet_class(int k){
    if(TV[4*k]<0) return 0;
    int ts[2]={-1,-1}, cnt[2]={0,0}, ns=0;
    for(int i=0;i<4;i++){ int t=VT(TV[4*k+i]); int f=-1;
        for(int j=0;j<ns;j++) if(ts[j]==t){f=j;break;}
        if(f<0){ if(ns>=2) return 0; ts[ns]=t; cnt[ns]=1; ns++; } else cnt[f]++; }
    if(ns!=2) return 0;
    int lo = (((ts[1]-ts[0])%T+T)%T==1)?0:1;   /* which of ts is the lower slice */
    int hi = 1-lo;
    if(cnt[lo]==3&&cnt[hi]==1) return 31;
    if(cnt[lo]==1&&cnt[hi]==3) return 13;
    if(cnt[lo]==2&&cnt[hi]==2) return 22;
    return 0;
}
/* is triangle (a,b,c) purely spatial (all in one slice)? */
static inline int tri_spatial(i32 a,i32 b,i32 c){ return VT(a)==VT(b)&&VT(b)==VT(c); }

/* ------- redex counters: number of applicable sub-complexes for each move --- */
/* (2,3) forward: a triangle shared by exactly two tets, one of type (3,1) OR
 * (1,3) and the other of type (2,2). (AJL: (3,1)+(2,2) sharing triangle 345;
 * (1,3) is the time-reverse and equally valid.) The shared triangle must be a
 * TIMELIKE triangle (2 verts one slice, 1 the other) -- that is exactly the
 * face type common to a (3,1)/(1,3) and a (2,2). */
static int count_23(void){
    int c=0;
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i];
        if(!s->used||s->cnt!=2) continue;
        if(tri_spatial(s->v[0],s->v[1],s->v[2])) continue;      /* need timelike face */
        int c0=tet_class(s->t[0]), c1=tet_class(s->t[1]);
        int a3=(c0==31||c0==13), b3=(c1==31||c1==13);
        int a2=(c0==22), b2=(c1==22);
        if((a3&&b2)||(a2&&b3)) c++;
    }
    return c;
}
/* (3,2) forward (== inverse of (2,3)): a TIMELIKE edge 12 shared by exactly 3
 * tets which are one (3,1)/(1,3) and two (2,2). Reversing it removes edge 12 and
 * merges to (3,1)+(2,2). */
static int count_32(void){
    int c=0;
    for(int i=0;i<EDGE.cap;i++){ Slot*s=&EDGE.slot[i];
        if(!s->used||s->cnt!=3) continue;
        if(VT(s->v[0])==VT(s->v[1])) continue;                 /* need timelike edge */
        int n31=0,n22=0,ok=1;
        for(int q=0;q<3;q++){ int cl=tet_class(s->t[q]);
            if(cl==31||cl==13) n31++; else if(cl==22) n22++; else {ok=0;break;} }
        if(ok&&n31==1&&n22==2) c++;
    }
    return c;
}
/* (2,6) forward: a spatial triangle 345 shared by exactly two tets, one (3,1)
 * (up-apex above) and one (1,3) (down-apex below). Count such spatial faces. */
static int count_26(void){
    int c=0;
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i];
        if(!s->used||s->cnt!=2) continue;
        if(!tri_spatial(s->v[0],s->v[1],s->v[2])) continue;
        int c0=tet_class(s->t[0]), c1=tet_class(s->t[1]);
        if((c0==31&&c1==13)||(c0==13&&c1==31)) c++;
    }
    return c;
}
/* (6,2) forward (== inverse of (2,6)): a spatial vertex X of order 6 whose 6
 * incident tets are 3 (3,1)+3 (1,3) forming the removable bipyramid: exactly two
 * apices (one up, one down) and three base verts. Count such vertices. */
static int count_62(void){
    int c=0;
    for(int i=0;i<VERT.cap;i++){ Slot*s=&VERT.slot[i];
        if(!s->used||s->cnt!=6) continue;
        i32 X=s->v[0]; int sT=VT(X);
        i32 apex[8]; int na=0; i32 base[8]; int nb=0; int ok=1; int n31=0,n13=0;
        for(int q=0;q<6;q++){ int k=s->t[q]; int cl=tet_class(k);
            if(cl==31)n31++; else if(cl==13)n13++; else {ok=0;break;}
            i32 ap=-1; int nbase=0; i32 bs[4];
            for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==X)continue;
                if(VT(v)!=sT){ if(ap>=0)ok=0; ap=v; } else { if(nbase<4)bs[nbase]=v; nbase++; } }
            if(ap<0||nbase!=2){ok=0;break;}
            int seen=0; for(int u=0;u<na;u++) if(apex[u]==ap)seen=1; if(!seen&&na<8)apex[na++]=ap; else if(!seen)na++;
            for(int u=0;u<2;u++){ int sn=0; for(int w=0;w<nb;w++) if(base[w]==bs[u])sn=1; if(!sn&&nb<8)base[nb++]=bs[u]; else if(!sn)nb++; } }
        if(ok&&na==2&&nb==3&&n31==3&&n13==3) c++;
    }
    return c;
}
/* (4,4) self-inverse: a spacelike edge shared by exactly 4 tets = the diamond
 * (2 up to a common apex, 2 down to a common apex, 2 spatial nbrs). Count such
 * edges. (The redex count is the same shape for forward and reverse, since the
 * move is its own inverse.) */
static int count_44(void){
    int c=0;
    for(int i=0;i<EDGE.cap;i++){ Slot*s=&EDGE.slot[i];
        if(!s->used||s->cnt!=4) continue;
        i32 a=s->v[0],b=s->v[1]; if(VT(a)!=VT(b)) continue; int sT=VT(a);
        i32 sp_nbr[8]; int nsp=0; i32 upp=-1,downq=-1; int nup=0,ndown=0,good=1; int tp=(sT+1)%T;
        for(int q=0;q<4;q++){ int k=s->t[q]; i32 ap=-1,spn=-1;
            for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==a||v==b)continue;
                if(VT(v)!=sT){ if(ap>=0)good=0; ap=v; } else { if(spn>=0)good=0; spn=v; } }
            if(ap<0||spn<0){good=0;break;}
            int seen=0; for(int u=0;u<nsp;u++) if(sp_nbr[u]==spn)seen=1; if(!seen&&nsp<8)sp_nbr[nsp++]=spn; else if(!seen)nsp++;
            if(VT(ap)==tp){ if(nup==0)upp=ap; else if(upp!=ap)good=0; nup++; }
            else { if(ndown==0)downq=ap; else if(downq!=ap)good=0; ndown++; } }
        if(good&&nsp==2&&nup==2&&ndown==2) c++;
    }
    return c;
}

/* ---- the five moves (FIX D: uniform redex selection; forward count set) --- */
/* Each move enumerates ALL valid redexes of its type, picks ONE uniformly,
 * applies it, and records the forward-redex count in last_Nforward so the
 * Metropolis-Hastings acceptance in bulk_sweep can multiply by
 * N_forward/N_reverse.  On any failure returns 0.                            */
static long last_Nforward=0;

/* generic: collect matching hash slots into idx[] up to cap, return count */
/* move (2,3): pick a timelike face shared by (3,1)/(1,3)+(2,2) uniformly */
static int move_23(void){
    /* reservoir of matching FACE slot indices */
    static int *buf=NULL; static int bufcap=0;
    int n=0;
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i];
        if(!s->used||s->cnt!=2) continue;
        if(tri_spatial(s->v[0],s->v[1],s->v[2])) continue;
        int c0=tet_class(s->t[0]), c1=tet_class(s->t[1]);
        int a3=(c0==31||c0==13), b3=(c1==31||c1==13), a2=(c0==22), b2=(c1==22);
        if(!((a3&&b2)||(a2&&b3))) continue;
        if(n>=bufcap){ bufcap=bufcap?bufcap*2:256; buf=realloc(buf,bufcap*sizeof(int)); }
        buf[n++]=i;
    }
    last_Nforward=n; if(n==0) return 0;
    int pick=buf[rng_below(n)]; Slot*s=&FACE.slot[pick];
    int i=s->t[0],j=s->t[1];
    i32 a=s->v[0],b=s->v[1],c=s->v[2]; i32 d=other_vertex(i,a,b,c),e=other_vertex(j,a,b,c);
    if(d<0||e<0||d==e) return 0;
    int old[2]={i,j}; i32 nv[3][4]={{a,b,d,e},{b,c,d,e},{a,c,d,e}};
    return apply_replace(old,2,nv,3);
}
/* move (3,2): pick a timelike edge shared by (3,1)/(1,3)+two (2,2) uniformly */
static int move_32(void){
    static int *buf=NULL; static int bufcap=0; int n=0;
    for(int i=0;i<EDGE.cap;i++){ Slot*s=&EDGE.slot[i];
        if(!s->used||s->cnt!=3) continue;
        if(VT(s->v[0])==VT(s->v[1])) continue;
        int n31=0,n22=0,ok=1;
        for(int q=0;q<3;q++){ int cl=tet_class(s->t[q]);
            if(cl==31||cl==13)n31++; else if(cl==22)n22++; else {ok=0;break;} }
        if(!(ok&&n31==1&&n22==2)) continue;
        if(n>=bufcap){ bufcap=bufcap?bufcap*2:256; buf=realloc(buf,bufcap*sizeof(int)); }
        buf[n++]=i;
    }
    last_Nforward=n; if(n==0) return 0;
    Slot*s=&EDGE.slot[buf[rng_below(n)]];
    i32 d=s->v[0],e=s->v[1]; i32 oth[8]; int no=0;
    for(int q=0;q<3;q++){ int k=s->t[q]; for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v!=d&&v!=e){
        int seen=0; for(int u=0;u<no;u++) if(oth[u]==v)seen=1; if(!seen&&no<8)oth[no++]=v; else if(!seen)no++; } } }
    if(no!=3) return 0; i32 a=oth[0],b=oth[1],c=oth[2]; int old[3]={s->t[0],s->t[1],s->t[2]};
    i32 nv[2][4]={{a,b,c,d},{a,b,c,e}}; return apply_replace(old,3,nv,2);
}
/* move (2,6): pick a spatial (3,1)+(1,3) triangle uniformly */
static int move_26(void){
    static int *buf=NULL; static int bufcap=0; int n=0;
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i];
        if(!s->used||s->cnt!=2) continue;
        if(!tri_spatial(s->v[0],s->v[1],s->v[2])) continue;
        int c0=tet_class(s->t[0]), c1=tet_class(s->t[1]);
        if(!((c0==31&&c1==13)||(c0==13&&c1==31))) continue;
        if(n>=bufcap){ bufcap=bufcap?bufcap*2:256; buf=realloc(buf,bufcap*sizeof(int)); }
        buf[n++]=i;
    }
    last_Nforward=n; if(n==0) return 0;
    Slot*s=&FACE.slot[buf[rng_below(n)]];
    i32 a=s->v[0],b=s->v[1],c=s->v[2]; int sT=VT(a);
    int i=s->t[0],j=s->t[1];
    i32 p=other_vertex(i,a,b,c),q=other_vertex(j,a,b,c);
    int tp=(sT+1)%T,tm=((sT-1)%T+T)%T,pT=VT(p),qT=VT(q);
    if(!((pT==tp&&qT==tm)||(pT==tm&&qT==tp))) return 0;
    i32 X=(i32)sT*VBASE+next_idx_max; int old[2]={i,j};
    i32 nv[6][4]={{a,b,X,p},{b,c,X,p},{a,c,X,p},{a,b,X,q},{b,c,X,q},{a,c,X,q}};
    next_idx_max++; if(apply_replace(old,2,nv,6)) return 1; next_idx_max--; return 0;
}
/* move (6,2): pick an order-6 removable spatial vertex uniformly */
static int move_62(void){
    static int *buf=NULL; static int bufcap=0; int n=0;
    for(int i=0;i<VERT.cap;i++){ Slot*s=&VERT.slot[i];
        if(!s->used||s->cnt!=6) continue;
        i32 X=s->v[0]; int sT=VT(X);
        i32 apex[8]; int na=0; i32 base[8]; int nb=0; int ok=1; int n31=0,n13=0;
        for(int q=0;q<6;q++){ int k=s->t[q]; int cl=tet_class(k);
            if(cl==31)n31++; else if(cl==13)n13++; else {ok=0;break;}
            i32 ap=-1; int nbase=0; i32 bs[4];
            for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==X)continue;
                if(VT(v)!=sT){ if(ap>=0)ok=0; ap=v; } else { if(nbase<4)bs[nbase]=v; nbase++; } }
            if(ap<0||nbase!=2){ok=0;break;}
            int seen=0; for(int u=0;u<na;u++) if(apex[u]==ap)seen=1; if(!seen&&na<8)apex[na++]=ap; else if(!seen)na++;
            for(int u=0;u<2;u++){ int sn=0; for(int w=0;w<nb;w++) if(base[w]==bs[u])sn=1; if(!sn&&nb<8)base[nb++]=bs[u]; else if(!sn)nb++; } }
        if(!(ok&&na==2&&nb==3&&n31==3&&n13==3)) continue;
        if(n>=bufcap){ bufcap=bufcap?bufcap*2:256; buf=realloc(buf,bufcap*sizeof(int)); }
        buf[n++]=i;
    }
    last_Nforward=n; if(n==0) return 0;
    Slot*s=&VERT.slot[buf[rng_below(n)]];
    i32 X=s->v[0]; int sT=VT(X);
    i32 apex[8]; int na=0; i32 base[8]; int nb=0;
    for(int q=0;q<6;q++){ int k=s->t[q]; i32 ap=-1; int nbase=0; i32 bs[4];
        for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==X)continue;
            if(VT(v)!=sT){ ap=v; } else { if(nbase<4)bs[nbase]=v; nbase++; } }
        int seen=0; for(int u=0;u<na;u++) if(apex[u]==ap)seen=1; if(!seen&&na<8)apex[na++]=ap;
        for(int u=0;u<2;u++){ int sn=0; for(int w=0;w<nb;w++) if(base[w]==bs[u])sn=1; if(!sn&&nb<8)base[nb++]=bs[u]; } }
    i32 a=base[0],b=base[1],c=base[2],p=apex[0],qq=apex[1];
    int old[6]; for(int q=0;q<6;q++)old[q]=s->t[q]; i32 nv[2][4]={{a,b,c,p},{a,b,c,qq}};
    return apply_replace(old,6,nv,2);
}
/* move (4,4): pick a spacelike edge in the 4-tet diamond uniformly */
static int move_44(void){
    static int *buf=NULL; static int bufcap=0; int n=0;
    for(int i=0;i<EDGE.cap;i++){ Slot*s=&EDGE.slot[i];
        if(!s->used||s->cnt!=4) continue;
        i32 a=s->v[0],b=s->v[1]; if(VT(a)!=VT(b)) continue; int sT=VT(a);
        i32 sp_nbr[8]; int nsp=0; i32 upp=-1,downq=-1; int nup=0,ndown=0,good=1; int tp=(sT+1)%T;
        for(int q=0;q<4;q++){ int k=s->t[q]; i32 ap=-1,spn=-1;
            for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==a||v==b)continue;
                if(VT(v)!=sT){ if(ap>=0)good=0; ap=v; } else { if(spn>=0)good=0; spn=v; } }
            if(ap<0||spn<0){good=0;break;}
            int seen=0; for(int u=0;u<nsp;u++) if(sp_nbr[u]==spn)seen=1; if(!seen&&nsp<8)sp_nbr[nsp++]=spn; else if(!seen)nsp++;
            if(VT(ap)==tp){ if(nup==0)upp=ap; else if(upp!=ap)good=0; nup++; }
            else { if(ndown==0)downq=ap; else if(downq!=ap)good=0; ndown++; } }
        if(!(good&&nsp==2&&nup==2&&ndown==2)) continue;
        if(n>=bufcap){ bufcap=bufcap?bufcap*2:256; buf=realloc(buf,bufcap*sizeof(int)); }
        buf[n++]=i;
    }
    last_Nforward=n; if(n==0) return 0;
    Slot*s=&EDGE.slot[buf[rng_below(n)]];
    i32 a=s->v[0],b=s->v[1]; int sT=VT(a);
    i32 sp_nbr[8]; int nsp=0; i32 upp=-1,downq=-1; int tp=(sT+1)%T;
    for(int q=0;q<4;q++){ int k=s->t[q]; i32 ap=-1,spn=-1;
        for(int r=0;r<4;r++){ i32 v=TV[4*k+r]; if(v==a||v==b)continue;
            if(VT(v)!=sT){ ap=v; } else { spn=v; } }
        int seen=0; for(int u=0;u<nsp;u++) if(sp_nbr[u]==spn)seen=1; if(!seen&&nsp<8)sp_nbr[nsp++]=spn;
        if(VT(ap)==tp)upp=ap; else downq=ap; }
    i32 c=sp_nbr[0],d=sp_nbr[1],p=upp,qq=downq; int old[4]; for(int q=0;q<4;q++)old[q]=s->t[q];
    i32 nv[4][4]={{a,c,d,p},{b,c,d,p},{a,c,d,qq},{b,c,d,qq}}; return apply_replace(old,4,nv,4);
}

/* inverse-move index for each move: after applying move mv, the reverse redex
 * count is count of the inverse move in the NEW configuration.
 *   (2,3)<->(3,2) ; (2,6)<->(6,2) ; (4,4) self-inverse.                        */
static int (*COUNT_FN[5])(void)={count_23,count_32,count_26,count_62,count_44};
static const int INV_MOVE[5]={1,0,3,2,4};   /* 0:23 1:32 2:26 3:62 4:44 */

static int (*MOVES[5])(void)={move_23,move_32,move_26,move_62,move_44};

/* ---- N0 ----------------------------------------------------------------- */
static int count_N0_scan(void){ int n=0; for(int i=0;i<VERT.cap;i++) if(VERT.slot[i].used&&VERT.slot[i].cnt>0)n++; return n; }
static inline int count_N0(void){ return gN0; }

/* ---- Metropolis --------------------------------------------------------- */
static double gk0,gk3,geps; static long gNbar;
static inline double Svol(int n3){ return geps>0? geps*(double)(n3-gNbar)*(double)(n3-gNbar):0.0; }

/* FIX (D): proper Metropolis-Hastings with the combinatorial proposal ratio.
 * Move mv is chosen with prob 1/5; a redex is chosen UNIFORMLY among the
 * N_forward valid redexes of that type in the current config (done inside the
 * move; count returned in last_Nforward). After applying, N_reverse = number of
 * redexes of the INVERSE move in the NEW config. The proposal density for
 *   T -> T' is  g(T->T') = (1/5)*(1/N_forward)
 *   T'-> T  is  g(T'->T) = (1/5)*(1/N_reverse)
 * so the Hastings factor is g(T'->T)/g(T->T') = N_forward/N_reverse and
 *   A = min(1, (N_forward/N_reverse) * exp(-dS)).                              */
static void bulk_sweep(int nsteps,long*acc,long*att){
    for(int step=0;step<nsteps;step++){
        int mv=rng_below(5); att[mv]++;
        int N0o = (gk0!=0.0)? count_N0():0;
        double S_old = -gk0*N0o + gk3*N3 + Svol(N3);
        if(!MOVES[mv]()){ continue; }        /* no valid redex, or apply failed */
        long Nf = last_Nforward;             /* forward redexes in OLD config   */
        long Nr = COUNT_FN[INV_MOVE[mv]]();  /* reverse redexes in NEW config   */
        int N0n = (gk0!=0.0)? count_N0():0;
        double S_new = -gk0*N0n + gk3*N3 + Svol(N3);
        double dS = S_new - S_old;
        /* A = min(1, (Nf/Nr) exp(-dS)). Nr>=1 (the just-applied redex reverses). */
        double ratio = (Nr>0)? ((double)Nf/(double)Nr) : 0.0;
        double a = ratio*exp(-dS);
        if(a>=1.0 || rng_double() < a) acc[mv]++;
        else undo_last();
    }
}

/* ================= build initial product complex ======================== */
/* Octahedron on each slice (8 tris, 6 verts idx 0..5), sandwiches cut into
 * 3 tets per spatial triangle, matching build_tetra_complex() ordering.      */
static const int OCTA[8][3]={{0,1,2},{0,2,3},{0,3,4},{0,4,1},{1,2,5},{2,3,5},{3,4,5},{1,4,5}};
static void build_product(int Tin){
    T=Tin;
    /* sort octa tris ascending like python sorted(tuple(sorted(t))) */
    int tri[8][3]; for(int i=0;i<8;i++){int a=OCTA[i][0],b=OCTA[i][1],c=OCTA[i][2];
        int x[3]={a,b,c}; for(int p=0;p<2;p++)for(int q=0;q<2-p;q++) if(x[q]>x[q+1]){int t=x[q];x[q]=x[q+1];x[q+1]=t;}
        tri[i][0]=x[0];tri[i][1]=x[1];tri[i][2]=x[2]; }
    /* bubble-sort the 8 triangles lexicographically */
    for(int i=0;i<8;i++)for(int j=0;j<7-i;j++){
        int gt = (tri[j][0]>tri[j+1][0])||(tri[j][0]==tri[j+1][0]&&(tri[j][1]>tri[j+1][1]||(tri[j][1]==tri[j+1][1]&&tri[j][2]>tri[j+1][2])));
        if(gt){int tmp[3];memcpy(tmp,tri[j],12);memcpy(tri[j],tri[j+1],12);memcpy(tri[j+1],tmp,12);} }
    for(int t=0;t<T;t++){ int tp=(t+1)%T;
        for(int q=0;q<8;q++){ int a=tri[q][0],b=tri[q][1],c=tri[q][2];
            i32 A=(i32)t*VBASE+a, B=(i32)t*VBASE+b, C=(i32)t*VBASE+c;
            i32 Au=(i32)tp*VBASE+a, Bu=(i32)tp*VBASE+b, Cu=(i32)tp*VBASE+c;
            add_tet(A,B,C,Cu);   /* (3,1) */
            add_tet(A,B,Cu,Bu);  /* (2,2) */
            add_tet(A,Bu,Cu,Au); /* (1,3) */
        } }
    next_idx_max=6; /* octahedron used indices 0..5 */
}

/* ================= measurement: slice volumes =========================== */
static void slice_volumes(int*vol){
    for(int t=0;t<T;t++) vol[t]=0;
    for(int t=0;t<T;t++) vol[t]=sliceF[t]; /* spatial triangles per slice */
}

/* ================= tet type census: (3,1)+(1,3) vs (2,2) ================= */
/* Classify each live tet by how its 4 vertices split across two adjacent
 * slices. (3,1)/(1,3): three verts on one slice, one on neighbor (timelike
 * "spatial-base" tets). (2,2): two verts on each of two slices (the timelike
 * tets that carry inter-slice coupling in AJL). Purely-spatial tets (4,0)
 * should not exist in a valid foliation but are counted as "other". */
static void tet_type_census(long*n31, long*n22, long*nother){
    long a=0,b=0,c=0;
    for(int k=0;k<ntet_used;k++){ if(TV[4*k]<0)continue;
        int ts[4], cnt[4], ns=0;
        for(int i=0;i<4;i++){ int t=VT(TV[4*k+i]); int seen=-1;
            for(int j=0;j<ns;j++) if(ts[j]==t){seen=j;break;}
            if(seen<0){ ts[ns]=t; cnt[ns]=1; ns++; } else cnt[seen]++; }
        if(ns==2){ if(cnt[0]==2&&cnt[1]==2) b++;            /* (2,2) */
                   else if((cnt[0]==3&&cnt[1]==1)||(cnt[0]==1&&cnt[1]==3)) a++; /* (3,1)/(1,3) */
                   else c++; }
        else c++;
    }
    *n31=a; *n22=b; *nother=c;
}

/* ================= dual graph (tet adjacency) =========================== */
/* build compact tet id remap (live tets -> 0..M-1) and adjacency lists via FACE map */
static int *live_id=NULL, *live_list=NULL, live_M=0, live_cap=0;
static void build_live_ids(void){
    if(ntet_used>live_cap){ live_cap=ntet_used; live_id=realloc(live_id,live_cap*sizeof(int)); live_list=realloc(live_list,live_cap*sizeof(int)); }
    live_M=0;
    for(int k=0;k<ntet_used;k++){ if(TV[4*k]>=0){ live_id[k]=live_M; live_list[live_M]=k; live_M++; } else live_id[k]=-1; }
}
/* adjacency as CSR from FACE map (each internal face joins 2 tets) */
static int *adj_off=NULL,*adj_nbr=NULL; static int adj_cap=0;
static void build_dual(void){
    build_live_ids();
    int *deg=calloc(live_M,sizeof(int));
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i]; if(s->used&&s->cnt==2){
        int a=live_id[s->t[0]],b=live_id[s->t[1]]; if(a>=0&&b>=0){deg[a]++;deg[b]++;} } }
    if(!adj_off||live_M+1>adj_cap){ adj_cap=live_M+1; adj_off=realloc(adj_off,adj_cap*sizeof(int)); }
    adj_off[0]=0; for(int i=0;i<live_M;i++) adj_off[i+1]=adj_off[i]+deg[i];
    int total=adj_off[live_M];
    adj_nbr=realloc(adj_nbr,(total>0?total:1)*sizeof(int));
    int *cur=malloc(live_M*sizeof(int)); for(int i=0;i<live_M;i++)cur[i]=adj_off[i];
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i]; if(s->used&&s->cnt==2){
        int a=live_id[s->t[0]],b=live_id[s->t[1]]; if(a>=0&&b>=0){ adj_nbr[cur[a]++]=b; adj_nbr[cur[b]++]=a; } } }
    free(deg); free(cur);
}

/* BFS ball growth: cumulative N(r) averaged over sources */
static double *Nr_accum=NULL; static int Nr_rmax=0;
static int *bfs_dist=NULL, *bfs_queue=NULL;
static int bfs_cap=0;
static void ball_growth(int nsrc,int rmax,double*out){
    if(live_M>bfs_cap){ bfs_cap=live_M; bfs_dist=realloc(bfs_dist,bfs_cap*sizeof(int)); bfs_queue=realloc(bfs_queue,bfs_cap*sizeof(int)); }
    for(int r=0;r<=rmax;r++) out[r]=0;
    for(int sidx=0;sidx<nsrc;sidx++){
        int s=rng_below(live_M);
        for(int i=0;i<live_M;i++)bfs_dist[i]=-1;
        int head=0,tail=0; bfs_dist[s]=0; bfs_queue[tail++]=s;
        int *shell=calloc(rmax+2,sizeof(int)); shell[0]=1;
        while(head<tail){ int u=bfs_queue[head++]; int du=bfs_dist[u]; if(du>=rmax)continue;
            for(int e=adj_off[u];e<adj_off[u+1];e++){ int w=adj_nbr[e]; if(bfs_dist[w]<0){ bfs_dist[w]=du+1; if(du+1<=rmax)shell[du+1]++; bfs_queue[tail++]=w; } } }
        int cum=0; for(int r=0;r<=rmax;r++){ cum+=shell[r]; out[r]+=cum; }
        free(shell);
    }
    for(int r=0;r<=rmax;r++) out[r]/=nsrc;
}

/* spectral dimension: lazy random walk return prob P(sigma) */
static void spectral(int nsrc,int sigma_max,double*P){
    double *prob=malloc(live_M*sizeof(double)), *nxt=malloc(live_M*sizeof(double));
    int *touched=malloc(live_M*sizeof(int)); int *touched2=malloc(live_M*sizeof(int));
    for(int s=0;s<=sigma_max;s++)P[s]=0;
    for(int sidx=0;sidx<nsrc;sidx++){
        int src=rng_below(live_M);
        for(int i=0;i<live_M;i++)prob[i]=0; prob[src]=1.0; int nt=1; touched[0]=src;
        P[0]+=1.0;
        for(int sigma=1;sigma<=sigma_max;sigma++){
            int nt2=0;
            for(int a=0;a<nt;a++){ int u=touched[a]; double pu=prob[u]; if(pu==0)continue;
                int deg=adj_off[u+1]-adj_off[u];
                if(deg==0){ if(nxt[u]==0)touched2[nt2++]=u; nxt[u]+=pu; continue; }
                if(nxt[u]==0){touched2[nt2++]=u;} nxt[u]+=0.5*pu;
                double share=0.5*pu/deg;
                for(int e=adj_off[u];e<adj_off[u+1];e++){ int w=adj_nbr[e]; if(nxt[w]==0)touched2[nt2++]=w; nxt[w]+=share; } }
            for(int a=0;a<nt;a++) prob[touched[a]]=0;
            for(int a=0;a<nt2;a++){ prob[touched2[a]]=nxt[touched2[a]]; nxt[touched2[a]]=0; }
            memcpy(touched,touched2,nt2*sizeof(int)); nt=nt2;
            P[sigma]+=prob[src];
        }
    }
    for(int s=0;s<=sigma_max;s++)P[s]/=nsrc;
    free(prob);free(nxt);free(touched);free(touched2);
}

/* ================= checkpoint I/O (binary) ============================== */
/* scalar measurement accumulators, persisted across checkpoint resume */
typedef struct { double n3sum,n3sq,t31sum,t22sum; long n3cnt,tccnt; } ScalarAcc;
static void save_ckpt(const char*path,int done_therm,int meas_n,
                      double*prof_acc,int prof_n,double*ntvar,int nv,
                      double*Nr_acc,int Nr_rmax_,int Nr_n,
                      double*ds_acc,int*ds_n,double*P_acc,int P_n,int sigma_max,ScalarAcc*sa){
    char tmp[512]; snprintf(tmp,sizeof(tmp),"%s.tmp",path);
    FILE*f=fopen(tmp,"wb"); if(!f)return;
    fwrite("CDTC0003",1,8,f);
    fwrite(&T,sizeof(int),1,f); fwrite(&N3,sizeof(int),1,f);
    fwrite(&next_idx_max,sizeof(int),1,f);
    fwrite(&gk0,sizeof(double),1,f);fwrite(&gk3,sizeof(double),1,f);
    fwrite(&geps,sizeof(double),1,f);fwrite(&gNbar,sizeof(long),1,f);
    fwrite(rng_s,sizeof(uint64_t),4,f);
    fwrite(&done_therm,sizeof(int),1,f); fwrite(&meas_n,sizeof(int),1,f);
    /* tets */
    int live=0; for(int k=0;k<ntet_used;k++) if(TV[4*k]>=0)live++;
    fwrite(&live,sizeof(int),1,f);
    for(int k=0;k<ntet_used;k++) if(TV[4*k]>=0) fwrite(&TV[4*k],sizeof(i32),4,f);
    /* accumulators */
    fwrite(&prof_n,sizeof(int),1,f); fwrite(prof_acc,sizeof(double),T,f);
    fwrite(&nv,sizeof(int),1,f); fwrite(ntvar,sizeof(double),nv,f);
    fwrite(&Nr_rmax_,sizeof(int),1,f); fwrite(&Nr_n,sizeof(int),1,f); fwrite(Nr_acc,sizeof(double),Nr_rmax_+1,f);
    fwrite(&sigma_max,sizeof(int),1,f); fwrite(&P_n,sizeof(int),1,f);
    fwrite(P_acc,sizeof(double),sigma_max+1,f);
    fwrite(ds_acc,sizeof(double),sigma_max+1,f); fwrite(ds_n,sizeof(int),sigma_max+1,f);
    fwrite(sa,sizeof(ScalarAcc),1,f);
    fclose(f); rename(tmp,path);
}

static int load_ckpt(const char*path,int*done_therm,int*meas_n,
                     double*prof_acc,int*prof_n,double*ntvar,int*nv,int ntvar_cap,
                     double*Nr_acc,int*Nr_rmax_,int*Nr_n,
                     double*ds_acc,int*ds_n,double*P_acc,int*P_n,int*sigma_max,ScalarAcc*sa){
    FILE*f=fopen(path,"rb"); if(!f)return 0;
    char magic[8]; if(fread(magic,1,8,f)!=8||memcmp(magic,"CDTC0003",8)){fclose(f);return 0;}
    int t_,n3_; fread(&t_,sizeof(int),1,f); fread(&n3_,sizeof(int),1,f);
    fread(&next_idx_max,sizeof(int),1,f);
    fread(&gk0,sizeof(double),1,f);fread(&gk3,sizeof(double),1,f);
    fread(&geps,sizeof(double),1,f);fread(&gNbar,sizeof(long),1,f);
    fread(rng_s,sizeof(uint64_t),4,f);
    fread(done_therm,sizeof(int),1,f); fread(meas_n,sizeof(int),1,f);
    T=t_;
    /* reset structures */
    sliceV=realloc(sliceV,T*sizeof(int)); sliceE=realloc(sliceE,T*sizeof(int)); sliceF=realloc(sliceF,T*sizeof(int));
    for(int i=0;i<T;i++){sliceV[i]=sliceE[i]=sliceF[i]=0;}
    N3=0; gN0=0; ntet_used=0; nfree=0;
    int live; fread(&live,sizeof(int),1,f);
    for(int k=0;k<live;k++){ i32 v[4]; fread(v,sizeof(i32),4,f); add_tet(v[0],v[1],v[2],v[3]); }
    fread(prof_n,sizeof(int),1,f); fread(prof_acc,sizeof(double),T,f);
    fread(nv,sizeof(int),1,f); if(*nv>ntvar_cap)*nv=ntvar_cap; fread(ntvar,sizeof(double),*nv,f);
    fread(Nr_rmax_,sizeof(int),1,f); fread(Nr_n,sizeof(int),1,f); fread(Nr_acc,sizeof(double),*Nr_rmax_+1,f);
    fread(sigma_max,sizeof(int),1,f); fread(P_n,sizeof(int),1,f);
    fread(P_acc,sizeof(double),*sigma_max+1,f);
    fread(ds_acc,sizeof(double),*sigma_max+1,f); fread(ds_n,sizeof(int),*sigma_max+1,f);
    if(fread(sa,sizeof(ScalarAcc),1,f)!=1){ sa->n3sum=sa->n3sq=sa->t31sum=sa->t22sum=0; sa->n3cnt=sa->tccnt=0; }
    fclose(f); return 1;
}

/* ================= self tests =========================================== */
static int global_checks(int verbose){
    /* closed: every face in exactly 2 tets */
    int bad_faces=0,boundary=0;
    for(int i=0;i<FACE.cap;i++){ Slot*s=&FACE.slot[i]; if(s->used){ if(s->cnt==1)boundary++; else if(s->cnt>2)bad_faces++; } }
    /* foliation */
    int folbad=0;
    for(int k=0;k<ntet_used;k++){ if(TV[4*k]<0)continue; int ts[4],ns=0;
        for(int i=0;i<4;i++){int t=VT(TV[4*k+i]),seen=0;for(int j=0;j<ns;j++)if(ts[j]==t)seen=1;if(!seen)ts[ns++]=t;}
        if(ns>2)folbad++; else if(ns==2){int dt=((ts[1]-ts[0])%T+T)%T; if(dt!=1&&dt!=T-1)folbad++;} }
    /* chi per slice */
    int chibad=0; for(int t=0;t<T;t++){ if(sliceF[t]==0){chibad++;continue;} if(sliceV[t]-sliceE[t]+sliceF[t]!=2)chibad++; }
    if(verbose) printf("  closed: boundary_faces=%d bad_faces=%d | foliation_bad=%d | chi_bad_slices=%d\n",boundary,bad_faces,folbad,chibad);
    return (boundary==0&&bad_faces==0&&folbad==0&&chibad==0);
}
static void free_all(void){
    memset(&FACE,0,0); }

static void init_maps(void){
    hmap_init(&FACE,1<<16); hmap_init(&EDGE,1<<16); hmap_init(&VERT,1<<14);
}
static void reset_all(void){
    /* free maps and re-init (used between tests) */
    free(FACE.slot); free(EDGE.slot); free(VERT.slot);
    init_maps();
    N3=0; gN0=0; ntet_used=0; nfree=0;
}

int main(int argc,char**argv){
    if(argc<2){ printf("usage: %s [selftest|xval|measure] ...\n",argv[0]); return 1; }

    if(!strcmp(argv[1],"dbtest")){
        /* VALIDATION A: detailed balance to machine precision.
         * For every valid redex of every move type in a thermalized small config
         * A, apply the forward move to reach B, measure Nr (inverse redexes in B),
         * dS, then confirm the reversibility identity
         *    exp(-S_A) * P(A->B)  ==  exp(-S_B) * P(B->A)
         * with P(A->B)=(1/5)(1/Nf) min(1,(Nf/Nr) e^{-dS}),
         *      P(B->A)=(1/5)(1/Nr) min(1,(Nr/Nf) e^{+dS}).
         * We also verify the inverse move applied to B returns to N3(A) and that
         * B counts the forward redex (Nr>=1). Report max |imbalance|/scale.       */
        rng_seed(777);
        int Tin=argc>2?atoi(argv[2]):4;
        double k0=argc>3?atof(argv[3]):0.8, k3=argc>4?atof(argv[4]):1.0;
        gk0=k0;gk3=k3;geps=0.0;gNbar=0;   /* eps=0: pure -k0N0+k3N3 for clean dS */
        sliceV=calloc(Tin,sizeof(int));sliceE=calloc(Tin,sizeof(int));sliceF=calloc(Tin,sizeof(int));
        init_maps(); build_product(Tin);
        long acc[5]={0},att[5]={0};
        for(int s=0;s<40;s++) bulk_sweep(30,acc,att);   /* thermalize */
        printf("=== DETAILED-BALANCE TEST (T=%d k0=%g k3=%g) N3=%d ===\n",Tin,k0,k3,N3);
        double worst=0.0; long checked=0, badrev=0;
        /* count-fn table and forward-move table indexed 0..4 */
        int (*CNT[5])(void)={count_23,count_32,count_26,count_62,count_44};
        for(int mv=0;mv<5;mv++){
            long Nf = CNT[mv]();            /* forward redexes in A */
            if(Nf==0){ printf("  move %d: no redex\n",mv); continue; }
            /* enumerate: to test each redex we re-run the move but it picks
             * randomly; instead we sample many applications and, for each, form
             * the exact reversibility residual. Statistical over redexes. */
            int trials = (int)(Nf<200?Nf:200);
            double mvworst=0.0; long mvbad=0;
            for(int tr=0;tr<trials;tr++){
                int N0A=count_N0(); int N3A=N3;
                double SA=-gk0*N0A+gk3*N3A;
                long NfA=CNT[mv]();          /* forward count in A (recomputed live) */
                if(!MOVES[mv]()){ continue; }
                long NfUsed=last_Nforward;   /* == NfA */
                int N0B=count_N0(); int N3B=N3;
                double SB=-gk0*N0B+gk3*N3B;
                double dS=SB-SA;
                long Nr=CNT[INV_MOVE[mv]]();  /* reverse redexes in B */
                /* reversibility residual */
                double PAB=(1.0/5.0)*(1.0/(double)NfUsed)*fmin(1.0,((double)NfUsed/(double)Nr)*exp(-dS));
                double PBA=(1.0/5.0)*(1.0/(double)Nr)*fmin(1.0,((double)Nr/(double)NfUsed)*exp(+dS));
                double lhs=exp(-SA)*PAB, rhs=exp(-SB)*PBA;
                double scale=fabs(lhs)+fabs(rhs)+1e-300;
                double resid=fabs(lhs-rhs)/scale;
                if(resid>mvworst)mvworst=resid;
                if(Nr<1){ badrev++; mvbad++; }
                checked++;
                undo_last();                 /* restore A for next trial */
                /* sanity: back to N3A */
                if(N3!=N3A){ mvbad++; }
            }
            if(mvworst>worst)worst=mvworst;
            printf("  move %d (%s): NfA=%ld trials=%d  max_rel_imbalance=%.3e  badrev=%ld\n",
                   mv, (const char*[]){"2,3","3,2","2,6","6,2","4,4"}[mv], Nf, trials, mvworst, mvbad);
        }
        printf("=== worst relative flux imbalance over all moves = %.3e ; checks=%ld badrev=%ld ===\n",worst,checked,badrev);
        printf("=== %s ===\n", (worst<1e-12 && badrev==0)?"DETAILED BALANCE EXACT (machine precision)":"DETAILED BALANCE VIOLATION");
        return (worst<1e-12&&badrev==0)?0:1;
    }
    if(!strcmp(argv[1],"selftest")){
        rng_seed(2024);
        int Tin = argc>2?atoi(argv[2]):4;
        sliceV=calloc(Tin,sizeof(int)); sliceE=calloc(Tin,sizeof(int)); sliceF=calloc(Tin,sizeof(int));
        init_maps();
        build_product(Tin);
        printf("=== C BULK SELF-TEST (T=%d) ===\n",Tin);
        int vol[64]; slice_volumes(vol);
        printf("[B1] init product: N3=%d N0=%d closed/fol/chi=%d N(t)=[",N3,count_N0(),global_checks(0));
        for(int t=0;t<T;t++)printf("%d%s",vol[t],t<T-1?",":""); printf("]\n");
        gk0=1.4; gk3=1.0; geps=0.02; gNbar=20*T;
        long acc[5]={0},att[5]={0};
        for(int s=0;s<30;s++) bulk_sweep(30,acc,att);
        printf("[B2] 30x30 sweeps accepted per move (23,32,26,62,44): %ld %ld %ld %ld %ld\n",acc[0],acc[1],acc[2],acc[3],acc[4]);
        int okg=global_checks(1);
        printf("[B3] after bulk: closed+foliated+chi=2 all slices: %d ; N3=%d\n",okg,N3);
        slice_volumes(vol);
        int vmax=0,vmin=1<<30; double vm=0; for(int t=0;t<T;t++){vm+=vol[t]; if(vol[t]>vmax)vmax=vol[t]; if(vol[t]<vmin)vmin=vol[t];} vm/=T;
        double vv=0; for(int t=0;t<T;t++)vv+=(vol[t]-vm)*(vol[t]-vm); vv/=T;
        printf("[B6] slice volumes N(t)=["); for(int t=0;t<T;t++)printf("%d%s",vol[t],t<T-1?",":""); printf("] mean=%.1f var=%.2f\n",vm,vv);
        /* independent fluctuation: run more, check slices differ over time */
        int series0[128],series1[128],ns=0;
        for(int s=0;s<20 && ns<128;s++){ bulk_sweep(20,acc,att); slice_volumes(vol); series0[ns]=vol[0]; series1[ns]=vol[1%T]; ns++; }
        int differ=0; for(int i=0;i<ns;i++) if(series0[i]!=series1[i])differ=1;
        printf("[B7] independent fluctuation (slice0 != slice1 timeseries): %d\n",differ);
        int n0chk=(count_N0()==count_N0_scan());
        printf("[B8] incremental N0 == scan N0: %d (gN0=%d scan=%d)\n",n0chk,count_N0(),count_N0_scan());
        printf("=== %s ===\n",(okg&&vv>0.0&&differ&&n0chk)?"ALL C SELF-TESTS PASSED":"SELF-TEST FAILURE");
        return okg?0:1;
    }


    if(!strcmp(argv[1],"bench")){
        double k0=argc>2?atof(argv[2]):1.6,k3=argc>3?atof(argv[3]):1.0;
        int Tin=argc>4?atoi(argv[4]):8; long Nbar=argc>5?atol(argv[5]):(long)(30*Tin);
        double eps=argc>6?atof(argv[6]):0.02; double budget=argc>7?atof(argv[7]):10.0;
        gk0=k0;gk3=k3;geps=eps;gNbar=Nbar; rng_seed(12345);
        sliceV=calloc(Tin,sizeof(int));sliceE=calloc(Tin,sizeof(int));sliceF=calloc(Tin,sizeof(int));
        init_maps(); build_product(Tin);
        long acc[5]={0},att[5]={0};
        /* thermalize toward Nbar first */
        clock_t tw=clock();
        while((double)(clock()-tw)/CLOCKS_PER_SEC < budget*0.4) bulk_sweep(200,acc,att);
        int n3=N3;
        long a2[5]={0},t2[5]={0};
        clock_t t0=clock(); long moves=0;
        while((double)(clock()-t0)/CLOCKS_PER_SEC < budget*0.6){ bulk_sweep(500,a2,t2); moves+=500; }
        double el=(double)(clock()-t0)/CLOCKS_PER_SEC;
        printf("BENCH k0=%g k3=%g T=%d Nbar=%ld N3=%d moves=%ld time=%.3f moves/sec=%.0f\n",
               k0,k3,Tin,Nbar,n3,moves,el,moves/el);
        return 0;
    }

    if(!strcmp(argv[1],"measure")){
        /* args: measure k0 k3 T Nbar eps seed sigma_max budget_s meas_target ckpt out */
        double k0=argc>2?atof(argv[2]):1.6, k3=argc>3?atof(argv[3]):1.0;
        int Tin=argc>4?atoi(argv[4]):12;
        long Nbar=argc>5?atol(argv[5]):(long)(20*Tin);
        double eps=argc>6?atof(argv[6]):0.02;
        uint64_t seed=argc>7?strtoull(argv[7],0,10):1;
        int sigma_max=argc>8?atoi(argv[8]):40;
        double budget=argc>9?atof(argv[9]):34.0;
        int meas_target=argc>10?atoi(argv[10]):200;
        int therm_target=argc>11?atoi(argv[11]):60;
        const char*ckpt=argc>12?argv[12]:NULL;
        const char*outp=argc>13?argv[13]:NULL;

        clock_t t0=clock();
        FILE*tracef=getenv("CDTTRACE")?fopen(getenv("CDTTRACE"),"a"):NULL;
        /* CDTSNAP: append each raw per-snapshot slice-volume vector N(t)
         * (length T, comma-separated) to a file, one line per measured
         * sample, appending across checkpointed chunks. MEASUREMENT-ONLY
         * side output: does not touch moves/measure accumulators/action --
         * it just records the same vol[] already sampled, for offline
         * iterative template registration. */
        FILE*snapf=getenv("CDTSNAP")?fopen(getenv("CDTSNAP"),"a"):NULL;
        gk0=k0;gk3=k3;geps=eps;gNbar=Nbar;
        rng_seed(seed);
        sliceV=calloc(Tin,sizeof(int)); sliceE=calloc(Tin,sizeof(int)); sliceF=calloc(Tin,sizeof(int));
        init_maps();

        int Nr_rmax_ = 2*Tin<24?2*Tin:24;
        double *prof_acc=calloc(Tin,sizeof(double));
        double *Nr_acc=calloc(Nr_rmax_+2,sizeof(double));
        double *P_acc=calloc(sigma_max+2,sizeof(double));
        double *ds_acc=calloc(sigma_max+2,sizeof(double));
        int *ds_n=calloc(sigma_max+2,sizeof(int));
        int NTVAR_CAP=1000000; double*ntvar=calloc(NTVAR_CAP,sizeof(double)); int nv=0;
        ScalarAcc SA={0,0,0,0,0,0};
        double pk_sum=0; long pk_cnt=0;   /* per-snapshot max/mean slice-vol concentration */
        #define n3sum SA.n3sum
        #define n3sq  SA.n3sq
        #define n3cnt SA.n3cnt
        #define t31sum SA.t31sum
        #define t22sum SA.t22sum
        #define tccnt SA.tccnt
        int done_therm=0, meas_n=0, prof_n=0, Nr_n=0, P_n=0;
        int sm_load=sigma_max, nrrm_load=Nr_rmax_;

        int loaded=0;
        if(ckpt && ckpt[0]) loaded=load_ckpt(ckpt,&done_therm,&meas_n,prof_acc,&prof_n,ntvar,&nv,NTVAR_CAP,
                             Nr_acc,&nrrm_load,&Nr_n,ds_acc,ds_n,P_acc,&P_n,&sm_load,&SA);
        if(loaded){ k0=gk0;k3=gk3;eps=geps;Nbar=gNbar; Tin=T;
            /* CDTMEASRESET=1: keep thermalized complex, discard measurement
             * accumulators so a fresh measurement pass runs on a hot state. */
            if(getenv("CDTMEASRESET")){ meas_n=0; prof_n=0; Nr_n=0; P_n=0; nv=0;
                for(int t=0;t<T;t++)prof_acc[t]=0;
                for(int r=0;r<Nr_rmax_+2;r++)Nr_acc[r]=0;
                for(int s2=0;s2<sigma_max+2;s2++){P_acc[s2]=0;ds_acc[s2]=0;ds_n[s2]=0;}
                n3sum=n3sq=t31sum=t22sum=0; n3cnt=tccnt=0; }
        }
        else { build_product(Tin); }

        double elapsed(){ return (double)(clock()-t0)/CLOCKS_PER_SEC; }
        long acc[5]={0},att[5]={0};
        /* thermalize */
        while(done_therm<therm_target && elapsed()<budget*0.45){
            bulk_sweep(25,acc,att); done_therm++;
        }
        int vol[512];
        /* measure */
        while(meas_n<meas_target && elapsed()<budget){
            bulk_sweep(20,acc,att);
            if(!global_checks(0)) continue;
            slice_volumes(vol);
            /* nt var */
            double vm=0; for(int t=0;t<T;t++)vm+=vol[t]; vm/=T;
            double vv=0; for(int t=0;t<T;t++)vv+=(vol[t]-vm)*(vol[t]-vm); vv/=T;
            if(nv<NTVAR_CAP)ntvar[nv++]=vv;
            { int vmax=0; for(int t=0;t<T;t++) if(vol[t]>vmax)vmax=vol[t];
              if(vm>0){ pk_sum += (double)vmax/vm; pk_cnt++; } }
            n3sum+=N3; n3sq+=(double)N3*N3; n3cnt++;
            { long n31,n22,noth; tet_type_census(&n31,&n22,&noth);
              t31sum+=(double)n31; t22sum+=(double)n22; tccnt++; }
            if(tracef){ fprintf(tracef,"%d %d %.4f\n",meas_n,N3,vv); }
            if(snapf){ for(int t=0;t<T;t++) fprintf(snapf,"%d%s",vol[t],t<T-1?",":"\n"); }
            /* COV-align profile. Default: circular center of mass on 3-pt
             * smoothed N(t). CDTALIGN=peak: anchor on the argmax of a WIDE
             * (window ~T/8) circular moving average -- locks a broad droplet
             * against a competing stalk far better than the COM, which the
             * stalk mass biases. (measurement-only; ensemble unchanged.)      */
            static int align_peak=-1;
            if(align_peak<0){ const char*a=getenv("CDTALIGN"); align_peak=(a&&!strcmp(a,"peak"))?1:0; }
            double sm[512]; for(int t=0;t<T;t++) sm[t]=(vol[(t-1+T)%T]+2.0*vol[t]+vol[(t+1)%T])/4.0;
            int com;
            if(align_peak){
                int w=T/8; if(w<1)w=1;
                double best=-1; int bi=0;
                for(int t=0;t<T;t++){ double acc2=0; for(int dd=-w;dd<=w;dd++){int u=((t+dd)%T+T)%T; acc2+=vol[u];}
                    if(acc2>best){best=acc2;bi=t;} }
                com=bi;
            } else {
                double sx=0,sy=0; for(int t=0;t<T;t++){sx+=sm[t]*cos(2*M_PI*t/T); sy+=sm[t]*sin(2*M_PI*t/T);}
                if(sx==0&&sy==0){com=0;double mx=-1;for(int t=0;t<T;t++)if(sm[t]>mx){mx=sm[t];com=t;}}
                else { double ang=atan2(sy,sx); com=((int)lround(ang/(2*M_PI)*T))%T; if(com<0)com+=T; }
            }
            int center=T/2;
            for(int t=0;t<T;t++){ int src=(com+(t-center))%T; if(src<0)src+=T; prof_acc[t]+=vol[src]; }
            prof_n++;
            /* dual graph + observables */
            build_dual();
            int rmax=Nr_rmax_;
            double tmpNr[64]; ball_growth(30,rmax,tmpNr);
            for(int r=0;r<=rmax;r++) Nr_acc[r]+=tmpNr[r];
            Nr_n++;
            double *Ptmp=malloc((sigma_max+2)*sizeof(double));
            spectral(6,sigma_max,Ptmp);
            for(int s=0;s<=sigma_max;s++)P_acc[s]+=Ptmp[s];
            P_n++;
            /* running ds from this sample's P */
            for(int sig=2;sig<sigma_max;sig++){ double p1=Ptmp[sig-1],p2=Ptmp[sig+1];
                if(p1>0&&p2>0){ double v=-2.0*(log(p2)-log(p1))/(log((double)sig+1)-log((double)sig-1)); ds_acc[sig]+=v; ds_n[sig]++; } }
            free(Ptmp);
            meas_n++;
        }
        if(ckpt&&ckpt[0]) save_ckpt(ckpt,done_therm,meas_n,prof_acc,prof_n,ntvar,nv,Nr_acc,Nr_rmax_,Nr_n,ds_acc,ds_n,P_acc,P_n,sigma_max,&SA);

        /* emit JSON */
        FILE*out = outp?fopen(outp,"w"):stdout;
        double el=elapsed();
        long tot_att=att[0]+att[1]+att[2]+att[3]+att[4];
        fprintf(out,"{\n");
        fprintf(out,"  \"k0\": %g, \"k3\": %g, \"T\": %d, \"Nbar\": %ld, \"eps\": %g,\n",gk0,gk3,T,gNbar,geps);
        fprintf(out,"  \"done_therm\": %d, \"target_therm\": %d, \"meas_samples\": %d, \"target_meas\": %d,\n",done_therm,therm_target,meas_n,meas_target);
        fprintf(out,"  \"N3_final\": %d, \"N0_final\": %d, \"elapsed_s\": %.2f,\n",N3,count_N0(),el);
        fprintf(out,"  \"moves_proposed\": %ld, \"moves_per_sec\": %.0f,\n",tot_att, tot_att/(el>0?el:1));
        /* nt var mean */
        double ntv=0; for(int i=0;i<nv;i++)ntv+=ntvar[i]; if(nv)ntv/=nv;
        fprintf(out,"  \"Nt_var_mean\": %.3f,\n",ntv);
        fprintf(out,"  \"snap_peakmean\": %.4f,\n", pk_cnt? pk_sum/pk_cnt:0.0);
        double n3m = n3cnt? n3sum/n3cnt:0; double n3v = n3cnt? n3sq/n3cnt-n3m*n3m:0;
        fprintf(out,"  \"N3_mean\": %.3f, \"N3_sd\": %.3f,\n",n3m, n3v>0?sqrt(n3v):0);
        { double t31m = tccnt? t31sum/tccnt:0; double t22m = tccnt? t22sum/tccnt:0;
          double tot = t31m+t22m; double frac22 = tot>0? t22m/tot:0;
          fprintf(out,"  \"tet31_mean\": %.1f, \"tet22_mean\": %.1f, \"frac22\": %.4f,\n",t31m,t22m,frac22); }
        /* profile */
        if(prof_n>0){
            fprintf(out,"  \"Nt_profile\": [");
            double prof[512]; for(int t=0;t<T;t++){prof[t]=prof_acc[t]/prof_n; fprintf(out,"%.3f%s",prof[t],t<T-1?", ":"");}
            fprintf(out,"],\n");
        }
        /* Nr avg */
        if(Nr_n>0){
            fprintf(out,"  \"Nr_avg\": {");
            for(int r=0;r<=Nr_rmax_;r++) fprintf(out,"\"%d\": %.3f%s",r,Nr_acc[r]/Nr_n,r<Nr_rmax_?", ":"");
            fprintf(out,"},\n");
        }
        /* P_return + ds */
        if(P_n>0){
            fprintf(out,"  \"P_return\": {");
            for(int s=0;s<=sigma_max;s++) fprintf(out,"\"%d\": %.8f%s",s,P_acc[s]/P_n,s<sigma_max?", ":"");
            fprintf(out,"},\n");
            fprintf(out,"  \"ds_running\": {");
            int first=1; for(int s=2;s<sigma_max;s++){ double p1=P_acc[s-1]/P_n,p2=P_acc[s+1]/P_n;
                if(p1>0&&p2>0){ double v=-2.0*(log(p2)-log(p1))/(log((double)s+1)-log((double)s-1));
                    fprintf(out,"%s\"%d\": %.4f",first?"":", ",s,v); first=0; } }
            fprintf(out,"},\n");
            /* dH from ensemble-avg Nr (oracle scaling window) */
            if(Nr_n>0){ double Nmax=0; for(int r=0;r<=Nr_rmax_;r++){double v=Nr_acc[r]/Nr_n; if(v>Nmax)Nmax=v;}
                int rlo=3,rhi=8; for(int r=Nr_rmax_;r>=3;r--){ if(Nr_acc[r]/Nr_n<0.6*Nmax){rhi=r;break;} }
                int n=0; double sx=0,sy=0,sxx=0,sxy=0;
                for(int r=rlo;r<=rhi;r++){ double y=Nr_acc[r]/Nr_n; if(y>0){ double lx=log((double)r),ly=log(y); sx+=lx;sy+=ly;sxx+=lx*lx;sxy+=lx*ly;n++; } }
                double dH=0; if(n>=2){ double mx=sx/n,my=sy/n; double denom=sxx-n*mx*mx; if(denom!=0) dH=(sxy-n*mx*my)/denom; }
                fprintf(out,"  \"dH_fit\": %.4f, \"dH_window\": [%d,%d]\n",dH,rlo,rhi);
            } else fprintf(out,"  \"dH_fit\": null\n");
        } else fprintf(out,"  \"P_return\": {}\n");
        fprintf(out,"}\n");
        if(tracef)fclose(tracef);
        if(snapf)fclose(snapf);
        if(outp)fclose(out);
        #undef n3sum
        #undef n3sq
        #undef n3cnt
        #undef t31sum
        #undef t22sum
        #undef tccnt
        return 0;
    }
    printf("unknown command %s\n",argv[1]); return 1;
}
