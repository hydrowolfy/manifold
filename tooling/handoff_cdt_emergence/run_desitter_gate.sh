#!/usr/bin/env bash
# de Sitter gate runner for the verified 2+1D CDT sampler.
# Parallel replicas across volumes, with checkpoint/resume.
# Usage:  bash run_desitter_gate.sh [PARALLEL]   (default 16)
# Safe to Ctrl-C / reboot and re-run: it resumes from gate_out/ checkpoints.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src/cdt_2plus1_faithful.c"; [ -f "$SRC" ] || SRC="$HERE/cdt_2plus1_faithful.c"
BIN="$HERE/cdt2p1"
PAR="${1:-16}"
OUT="$HERE/gate_out"; mkdir -p "$OUT"

echo "[build] compiling $SRC"
gcc -O3 -march=native -funroll-loops -o "$BIN" "$SRC" -lm || { echo "[build] FAILED"; exit 1; }
echo "[build] ok"
"$BIN" selftest >/dev/null 2>&1 && echo "[check] selftest passed" || echo "[check] WARNING selftest issue"

# coupled/extended phase; T ~ 3.2*N3^(1/3) (hardcoded per volume, no python needed)
THERM=300000     # thermalization-sweep target (checkpointed)
MEAS=30000       # measurement-sample target
BUDGET=45        # seconds per measure call before it checkpoints+exits
export BIN OUT THERM MEAS BUDGET

run_one(){
  local NB="$1" SD="$2" T
  case "$NB" in
    2000) T=40;; 3000) T=46;; 4000) T=51;; 6000) T=58;;
    8000) T=64;; 16000) T=81;; 32000) T=102;; *) T=48;;
  esac
  local ck="$OUT/v${NB}_s${SD}.ck" out="$OUT/v${NB}_s${SD}.json"
  local snap="$OUT/v${NB}_s${SD}.snap" log="$OUT/v${NB}_s${SD}.log"
  while :; do
    CDTSNAP="$snap" "$BIN" measure -2 1.2 "$T" "$NB" 0.04 "$SD" 40 "$BUDGET" "$MEAS" "$THERM" "$ck" "$out" >>"$log" 2>&1 \
      || { echo "[warn] measure returned nonzero N3=$NB s=$SD (see $log)"; sleep 2; }
    local dt ms
    dt=$(grep -o '"done_therm"[^0-9]*[0-9]\+'   "$out" 2>/dev/null | grep -o '[0-9]\+$')
    ms=$(grep -o '"meas_samples"[^0-9]*[0-9]\+' "$out" 2>/dev/null | grep -o '[0-9]\+$')
    [ -n "${dt:-}" ] && [ -n "${ms:-}" ] && [ "$dt" -ge "$THERM" ] && [ "$ms" -ge "$MEAS" ] && break
  done
  echo "[done] N3~$NB seed $SD"
}
export -f run_one

echo "[run] $PAR parallel replicas: volumes 2000/4000/8000 x seeds 1..6"
for NB in 2000 4000 8000; do for SD in 1 2 3 4 5 6; do echo "$NB $SD"; done; done \
  | xargs -P "$PAR" -n 2 bash -c 'run_one "$0" "$1"'
echo "[all done] results in $OUT"
