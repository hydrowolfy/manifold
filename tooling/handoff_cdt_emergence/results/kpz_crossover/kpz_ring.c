/* kpz_ring.c -- biased-ASEP bond-current sampler for the weak-drive KPZ crossover test.
 *
 * Port of run_bond_current() from cdt_nonequilib.py (same proposal, same Metropolis-with-bias
 * acceptance): n_rings independent periodic rings of length L, density 1/2.
 *   pick site p uniform in [0,L), q=(p+1)%L
 *   'UD' (particle,hole) -> forward hop,  accept min(1, e^{+E})
 *   'DU'                 -> backward hop, accept min(1, e^{-E})
 * Observable: time-integrated current Q across bond (0,1) per ring, sampled every
 * sample_every sweeps (1 sweep = L attempts per ring).
 * Init: exact-N/2 shuffle = the exact stationary measure of ring ASEP (no thermalization).
 *
 * Checkpoint/resume: state file holds rng + rings + counters; program runs until
 * done or wall-time budget, then checkpoints. Exit 0 = complete, 3 = checkpointed.
 *
 * Usage: kpz_ring L E n_rings meas_sweeps sample_every seconds_budget statefile outfile [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

/* xoshiro256** */
static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x, int k){ return (x<<k)|(x>>(64-k)); }
static inline uint64_t nxt(void){
    const uint64_t r = rotl(s[1]*5,7)*9;
    const uint64_t t = s[1]<<17;
    s[2]^=s[0]; s[3]^=s[1]; s[1]^=s[2]; s[0]^=s[3]; s[2]^=t; s[3]=rotl(s[3],45);
    return r;
}
static inline double u01(void){ return (nxt()>>11)*0x1.0p-53; }
static inline uint32_t randint(uint32_t n){ /* unbiased enough for n<<2^32 */
    return (uint32_t)(((__uint128_t)nxt()*(__uint128_t)n)>>64);
}
static void seed_rng(uint64_t seed){
    uint64_t z=seed;
    for(int i=0;i<4;i++){ z+=0x9e3779b97f4a7c15ULL; uint64_t x=z;
        x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL; x=(x^(x>>27))*0x94d049bb133111ebULL;
        s[i]=x^(x>>31); }
}

typedef struct {
    int64_t L, n_rings, meas_sweeps, sample_every, done_sweeps;
    double E;
    uint64_t rng[4];
} Hdr;

int main(int argc, char**argv){
    if(argc<9){ fprintf(stderr,"usage: %s L E n_rings meas_sweeps sample_every seconds statefile outfile [seed]\n",argv[0]); return 1; }
    int64_t L=atoll(argv[1]); double E=atof(argv[2]); int64_t NR=atoll(argv[3]);
    int64_t MEAS=atoll(argv[4]); int64_t SE=atoll(argv[5]); double BUDGET=atof(argv[6]);
    const char*statef=argv[7]; const char*outf=argv[8];
    uint64_t seed = (argc>9)? strtoull(argv[9],0,10) : 12345;

    unsigned char *ring = malloc((size_t)NR*L);
    int64_t *Q = malloc(NR*sizeof(int64_t));
    int64_t *W = malloc(NR*sizeof(int64_t));
    int64_t done=0;
    Hdr h;

    FILE*sf=fopen(statef,"rb");
    if(sf){ /* resume */
        if(fread(&h,sizeof h,1,sf)!=1){fprintf(stderr,"bad state\n");return 1;}
        if(h.L!=L||h.n_rings!=NR||h.E!=E||h.meas_sweeps!=MEAS||h.sample_every!=SE){
            fprintf(stderr,"state mismatch\n"); return 1; }
        memcpy(s,h.rng,sizeof s);
        fread(ring,1,(size_t)NR*L,sf); fread(Q,sizeof(int64_t),NR,sf); fread(W,sizeof(int64_t),NR,sf);
        fclose(sf); done=h.done_sweeps;
        fprintf(stderr,"resumed at sweep %lld/%lld\n",(long long)done,(long long)MEAS);
    } else { /* fresh init: exact stationary measure (uniform over fixed-N configs) */
        seed_rng(seed);
        for(int64_t r=0;r<NR;r++){
            unsigned char*w=ring+r*L;
            for(int64_t i=0;i<L;i++) w[i]=(i<L/2)?1:0;
            for(int64_t i=L-1;i>0;i--){ int64_t j=randint(i+1); unsigned char t=w[i];w[i]=w[j];w[j]=t; }
            Q[r]=0; W[r]=0;
        }
        /* write header line to outfile */
        FILE*of=fopen(outf,"w");
        fprintf(of,"# L=%lld E=%g n_rings=%lld meas_sweeps=%lld sample_every=%lld seed=%llu\n",
            (long long)L,E,(long long)NR,(long long)MEAS,(long long)SE,(unsigned long long)seed);
        fclose(of);
    }

    double acc_bwd = exp(-E);   /* E>=0 assumed; forward always accepted */
    if(E<0){ fprintf(stderr,"E<0 unsupported\n"); return 1; }
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    FILE*of=fopen(outf,"a");

    while(done<MEAS){
        /* advance every ring by SE sweeps (SE*L attempts) */
        for(int64_t r=0;r<NR;r++){
            unsigned char*w=ring+r*L;
            int64_t q=Q[r], wd=W[r];
            int64_t attempts=SE*L;
            for(int64_t a=0;a<attempts;a++){
                int64_t p=randint((uint32_t)L);
                int64_t pq=p+1; if(pq==L) pq=0;
                unsigned char x=w[p], y=w[pq];
                if(x==y) continue;
                if(x){ /* UD forward: accept 1 */
                    w[p]=0; w[pq]=1; wd++;
                    if(p==0) q++;
                } else { /* DU backward: accept e^{-E} */
                    if(E==0.0 || u01()<acc_bwd){ w[p]=1; w[pq]=0; wd--; if(p==0) q--; }
                }
            }
            Q[r]=q; W[r]=wd;
        }
        done+=SE;
        /* sample line: sweep then Q per ring */
        fprintf(of,"%lld",(long long)done);
        for(int64_t r=0;r<NR;r++) fprintf(of," %lld",(long long)Q[r]);
        fputc('\n',of);
        clock_gettime(CLOCK_MONOTONIC,&t1);
        double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
        if(el>BUDGET && done<MEAS){
            fclose(of);
            h.L=L;h.n_rings=NR;h.E=E;h.meas_sweeps=MEAS;h.sample_every=SE;h.done_sweeps=done;
            memcpy(h.rng,s,sizeof s);
            FILE*sf2=fopen(statef,"wb");
            fwrite(&h,sizeof h,1,sf2); fwrite(ring,1,(size_t)NR*L,sf2);
            fwrite(Q,sizeof(int64_t),NR,sf2); fwrite(W,sizeof(int64_t),NR,sf2);
            fclose(sf2);
            fprintf(stderr,"checkpoint at sweep %lld/%lld (%.1fs)\n",(long long)done,(long long)MEAS,el);
            return 3;
        }
    }
    fclose(of);
    remove(statef);
    fprintf(stderr,"complete: %lld sweeps\n",(long long)done);
    return 0;
}
