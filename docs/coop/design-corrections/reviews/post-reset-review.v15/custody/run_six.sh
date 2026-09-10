#!/bin/zsh
# Reproduce the six recorded reference commands in a disposable full copy.
# Attempt 2: the interpreter is invoked directly rather than through a quoted
# shell variable, which is what made attempt 1 exit 127 before any command ran.
set -u
ROOT="$1"
OUT="$2"
PY=/tmp/opensip-architecture-review-env/bin/python
mkdir -p "$OUT"
cd "$ROOT" || exit 9

run() {
  local name="$1"; shift
  "$PY" -I -B "$@" > "$OUT/$name.log" 2>&1
  echo "$name exit=$?"
}

run foundation       docs/coop/design-corrections/foundation/run-reference-checks.py --report docs/coop/design-corrections/foundation/validation-report.json
run security         docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report docs/coop/design-corrections/security/security-lifecycle-report.v1.json
run native           docs/coop/design-corrections/native/check_native_evidence.v2.py
run workflows        docs/coop/design-corrections/workflows/run-reference-checks.py --report docs/coop/design-corrections/workflows/workflows-validation-report.json
run workflow-surface docs/coop/design-corrections/workflows/check_workflows.v1.py --report docs/coop/design-corrections/workflows/workflows-report.v1.json
run integration      docs/coop/design-corrections/check-integration.py --report docs/coop/design-corrections/integration-report.v1.json
