#!/bin/sh
# Reproduce the Claude XA-01 + XA-02/CR-25 correction from frozen candidate25.
# Nothing here writes to candidate25 or to any root live tree.
#   $1 = frozen candidate25 root   $2 = a NEW empty scratch directory   $3 = python3.12 with jsonschema
set -e
SRC="$1"; WORK="$2"; PY="${3:-/tmp/opensip-architecture-review-env/bin/python}"
AUD="${AUD:-/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-crosscut-audit.v1}"
mkdir -p "$WORK"
cp -R "$SRC" "$WORK/successor"

# 1. the already-reproduced three-file XA-01 cap correction
"$PY" -I -B "$AUD/apply-reference-correction.py" --source "$SRC" --copy "$WORK/successor" --out "$WORK/xa01"

# 2. the XA-02 / CR-25 stages, in order
for S in stage1 stage2 stage4 stage5 stage6 stage9 stage10 stage11; do
  "$PY" -I -B "$WORK/apply-correction.py" --copy "$WORK/successor" --stage "$WORK/stages/$S.json" --out "$WORK/out-$S"
done
"$PY" -I -B "$WORK/apply-schema-stage.py" "$WORK/successor" "$WORK/out-schema"
"$PY" -I -B "$WORK/add-discovery-result-v2.py" "$WORK/successor" "$WORK/out-schema"
"$PY" -I -B "$WORK/version-fixtures.py" "$WORK/successor" "$WORK/out-fixtures"

# 3. explicit scratch-only pin rebinding, then the suites
"$PY" -I -B "$WORK/rebind-pins.py" --copy "$WORK/successor" --out "$WORK/source-pin-delta.json"
D="$WORK/successor/docs/coop/design-corrections"
( cd "$D/security" && "$PY" -I -B "$D/security/check-security-lifecycle.v1.py" --report "$WORK/security.json" )
( cd "$D/native"   && "$PY" -I -B "$D/native/check_native_evidence.v2.py" --report "$WORK/native.json" )
( cd "$D"          && "$PY" -I -B "$D/../../coop/design-corrections/check-integration.py" --report "$WORK/integration.json" )
"$PY" -I -B "$WORK/controls-xa02-cr25.py" --source "$WORK/successor" --out "$WORK/controls.json"
echo "Reproduced. Reference results only; no product qualification."
