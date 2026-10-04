#!/bin/sh
# CF-P probe runner (throwaway). Builds and runs in a scratch dir under DARWIN_USER_TEMP_DIR.
# Usage: sh run.sh [node-binary]   (writes cfp-run.log next to the binary)
set -u
D="$(getconf DARWIN_USER_TEMP_DIR)cfp-probe"; mkdir -p "$D"; cd "$D" || exit 1
for f in cfp.c t_named.c t_reason.c provider.sb tool.sb; do [ -f "$f" ] || { echo "missing $f in $D"; exit 1; }; done
nice -n 10 clang -O1 -Wall -o cfp cfp.c 2> build.log            # build.log keeps the SDK deprecation diagnostics
nice -n 10 clang -Wall -Wno-deprecated-declarations -o t_named t_named.c
nice -n 10 clang -Wall -o t_reason t_reason.c
BASE="$(realpath "$D")/runs-$(date +%Y%m%dT%H%M%S)"; mkdir -p "$BASE"
NODE="${1:-}"
{
  sw_vers; uname -a; xcrun --show-sdk-path; xcrun --show-sdk-version; clang --version | head -1
  # synthetic canary in the host's own exec-time environment (E-ENV b)
  CFP_CANARY_HOST=cfp-host-canary-7f3a perl -e 'alarm shift; exec @ARGV' 240 nice -n 10 ./cfp harness "$(realpath cfp)" "$BASE" $NODE
  echo; echo "=== SIDE t_named (sandbox_init SANDBOX_NAMED), exit reason read from the zombie"
  perl -e 'alarm shift; exec @ARGV' 20 ./t_reason ./t_named 2>/dev/null
} > cfp-run.log 2>&1
echo "log: $D/cfp-run.log"
