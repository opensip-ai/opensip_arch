#!/bin/sh
# Silent until fullcheck reaches a terminal state. Diagnostics go to the sidecar log.
set -eu
EXIT=/tmp/opensip-implementation/m1-grok-typescript-boundary-review-04/review/results/fullcheck.exit
LOG=/tmp/opensip-implementation/m1-grok-typescript-boundary-review-04/review/results/fullcheck.log
SIDE=/tmp/opensip-implementation/m1-grok-typescript-boundary-review-04/review/results/watch-fullcheck.side.log
PATTERN='fullcheck.sh'

while [ ! -f "$EXIT" ]; do
  if ! pgrep -f "$PATTERN" >/dev/null 2>&1; then
    # Race: process may have exited between the file check and pgrep.
    [ -f "$EXIT" ] && break
    echo "process gone without exit file" >>"$SIDE"
    tail -20 "$LOG" >>"$SIDE" 2>/dev/null || true
    echo "FAILED: fullcheck process exited before writing exit file"
    exit 1
  fi
  sleep 30
done
code=$(cat "$EXIT")
if [ "$code" = 0 ]; then
  echo "DONE"
  exit 0
fi
echo "FAILED: fullcheck exit $code"
exit 1
