#!/usr/bin/env bash
# de Sitter gate runner for the verified 2+1D CDT sampler.
# Runs parallel replicas across volumes on your cores, with checkpoint/resume.
# Usage:  bash run_desitter_gate.sh [PARALLEL]   (default PARALLEL=16)
# Re-run any time; it resumes from checkpoints. Safe to Ctrl-C and restart.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src/cdt_2plus1_faithful.c"
[ -f "$SRC" ] || SRC="$HERE/cdt_2plus1_faithful.c"
BIN="$HERE/cdt2p1"
PAR="${1:-16}"
OUT="$HERE/gate_out"; mkdir -p "$OUT"

echo "[build] compiling $SRC"
gcc -O3 -march=native -funroll-loops -o "$BIN" "$SRC" -lm || { echo "build failed"; exit 1; }
echo "[build] ok -> $BIN"
"$BIN" selftest >/dev/null 2>&1 && echo "[check] selftest passed" || echo "[check] WARNING selftest issue"

# k0=-2 (coupled/extended phase), k3=1.2, eps=0.04 soft volume fix.
# T scales ~3.2*N3^(1/3) so the blob (width ~N3^(1/3)) sits on a stalk.
VOLS="2000 4000 8000"
SEEDS="1 2 3 4 5 6"
THERM=300000     # thermalization sweeps target (checkpointed; grows the run)
MEAS=30000       # measurement samples target
BUDGET=45        # seconds per measure invocation before it checkpoints+exits

run_one(){
  local NB="$1" SD="$2"
  local T; T=$(python3 - "$NB" <<PY
import sys;NB=int(sys.argv[1]);print(max(6,round(3.2*NB**(1/3))))
PY
)
  local ck="$OUT/v${NB}_s${SD}.ck" out="$OUT/v${NB}_s${SD}.json" snap="$OUT/v${NB}_s${SD}.snap" log="$OUT/v${NB}_s${SD}.log"
  while :; do
    CDTSNAP="$snap" "$BIN" measure -2 1.2 "$T" "$NB" 0.04 "$SD" 40 "$BUDGET" "$MEAS" "$THERM" "$ck" "$out" >>"$log" 2>&1
    python3 - "$out" "$THERM" "$MEAS" <<PY && break
import json,sys
d=json.load(open(sys.argv[1]))
sys.exit(0 if d["done_therm"]>=int(sys.argv[2]) and d["meas_samples"]>=int(sys.argv[3]) else 1)
PY
  done
  echo "[done] N3~$NB seed $SD"
}
export -f run_one; export OUT BIN

echo "[run] launching replicas across volumes $VOLS x seeds, $PAR at a time"
for NB in $VOLS; do for SD in $SEEDS; do echo "$NB $SD"; done; done \
  | xargs -P "$PAR" -n 2 bash -c 'run_one "$0" "$1"'
echo "[all done] results in $OUT ; analyze with gate_register.py per snap file"
