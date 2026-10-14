#!/bin/zsh
# U-5a: run the six cold runner variants in sequence; each takes the lane itself. Stops at the first failure.
P=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
W=/tmp/opensip-implementation/sm-cold-ts-2026-10-13
for pair in sealing:run_set.py transfer:run_transfer.py cohort:run_cohort.py synthesized:run_synthesized_ts.py replay:run_sized_replay_r2.py; do
  d=${pair%%:*}; f=${pair##*:}
  echo "START $d $(date +%T)"
  (cd $W/$d && $P -I -B $f > run.log 2>&1) || { echo "FAILED $d"; exit 1; }
  echo "DONE $d $(date +%T)"
done
echo ALLDONE
