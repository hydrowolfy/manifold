#!/bin/bash
# CDT phase-scan supervisor (runs in WSL). See LESSONS 53 for why each piece exists.
#  - keeps exactly ONE scan running; restarts it if it EXITS (crash/OOM)
#  - WATCHDOG: kills + restarts it if it HANGS (heartbeat stale > 25 min)
#  - resets the heartbeat at each launch, so the watchdog cannot kill a process that is still
#    legitimately loading a multi-GB checkpoint (that bug caused a ~30x kill-loop)
#  - CHECKPOINTS ON A FAST LOCAL DISK (/mnt/d/cdt4ckpt) -- 1.3GB pickles stalled on a full C:
#  - SKIPS (5.0,0.0): N0 runaway makes it computationally intractable. Logged deviation; that point
#    is characterized from its provisional reads and reported UNCONVERGED.
set -u
DIR=/mnt/c/Users/Kirk/Downloads/cdt4scan
CK=/mnt/d/cdt4ckpt
cd "$DIR" || exit 1
mkdir -p out
if mkdir -p "$CK" 2>/dev/null && [ -w "$CK" ]; then
  echo "SUPERVISOR ckpt dir = $CK (D:)" >> out/START.log
else
  CK="$HOME/cdt4ckpt"; mkdir -p "$CK"
  echo "SUPERVISOR WARN: /mnt/d not writable, falling back to $CK" >> out/START.log
fi
if [ -f "out/base_T6_N42000.pkl" ] && [ ! -f "$CK/base_T6_N42000.pkl" ]; then
  cp "out/base_T6_N42000.pkl" "$CK/" && echo "SUPERVISOR copied base" >> out/START.log
fi

ARGS="--scan --scratch out --ckpt-dir $CK --ckpt-every 25 --cap-sweeps 1000 --skip 5.0:0.0"
echo "SUPERVISOR args: $ARGS" >> out/START.log

while true; do
  if grep -q "SCAN COMPLETE" out/START.log 2>/dev/null; then
    echo "SUPERVISOR: SCAN COMPLETE -- exiting $(date)" >> out/START.log; break
  fi
  if ! pgrep -f 'cdt4_phasescan\.py' >/dev/null 2>&1; then
    echo "WRAP_LAUNCH $(date)" >> out/START.log
    echo "LOADING $(date '+%H:%M:%S') | scan launching (reading checkpoint, no sweeps yet)" > out/heartbeat.txt
    nohup python3 -u cdt4_phasescan.py $ARGS >> out/run.log 2>&1 &
    sleep 120
    continue
  fi
  if [ -f out/heartbeat.txt ]; then
    now=$(date +%s); hbt=$(stat -c %Y out/heartbeat.txt 2>/dev/null || echo "$now")
    age=$(( now - hbt ))
    if [ "$age" -gt 1500 ]; then
      echo "WATCHDOG: heartbeat stale ${age}s -> killing hung scan $(date)" >> out/START.log
      pkill -9 -f 'cdt4_phasescan\.py'; sleep 15; continue
    fi
  fi
  sleep 60
done
