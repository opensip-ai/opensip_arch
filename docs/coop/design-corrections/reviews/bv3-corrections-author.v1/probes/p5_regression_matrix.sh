#!/bin/zsh
# P5: prove the added checks actually catch the ORIGINAL defects.
#
# Takes the corrected tree, reverts ONLY the SUBJECT files (schemas, registries and
# models) to their frozen v12 bytes while keeping the corrected CHECKERS and
# fixtures, then runs the suite. Every failure is a defect the new tests detect.
# A check that passes here would be one that cannot fail, and proves nothing.
set -u
B=/tmp/opensip-design-corrections/bv3-corrections-author.v1
P=/tmp/opensip-architecture-review-env/bin/python
R=$B/probes/regress-full
LOG=$B/logs/regress-full
FROZEN=/tmp/opensip-design-corrections/candidate-subject.v12

rm -rf $R $LOG; mkdir -p $LOG
cp -R $B/work/ $R/

# SUBJECT bytes reverted to frozen. Checkers, fixtures and corpora stay corrected.
for f in \
  docs/coop/design-corrections/foundation/identity-schemas.v2.json \
  docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json \
  docs/coop/design-corrections/foundation/identity-model.py \
  docs/coop/design-corrections/native/capability-manifest-domains.v2.json \
  docs/coop/design-corrections/native/native-evidence.schemas.v2.json \
  docs/coop/design-corrections/native/native_evidence_model.v2.py \
  docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json \
  docs/coop/design-corrections/workflows/schemas/policy-document.schema.json \
  docs/coop/design-corrections/workflows/schemas/repair.schema.json \
  docs/coop/design-corrections/workflows/workflows_model.v1.py ; do
  cp $FROZEN/$f $R/$f
done

$P -I -B - <<'PY'
import hashlib, json, os
R = "/tmp/opensip-design-corrections/bv3-corrections-author.v1/probes/regress-full"
for rel in ["docs/coop/design-corrections/foundation/source-pins.v1.json",
            "docs/coop/design-corrections/workflows/source-pins.v1.json",
            "docs/coop/design-corrections/native/source-pins.v2.json"]:
    full = os.path.join(R, rel); m = json.load(open(full))
    rows = m["files"] if "files" in m else m["pins"]
    for it in rows:
        t = os.path.join(R, it["path"])
        if os.path.isfile(t):
            raw = open(t, "rb").read()
            it["sha256"] = hashlib.sha256(raw).hexdigest()
            if "bytes" in it: it["bytes"] = len(raw)
    open(full, "w").write(json.dumps(m, indent=2) + "\n")
print("regression-copy pins measured")
PY

D=$R/docs/coop/design-corrections
for s in check-identity check-foundation check-array-orders; do
  $P -I -B $D/foundation/$s.py --report $LOG/$s.json >$LOG/$s.out 2>&1
  echo "foundation/$s exit=$? :: $(tail -1 $LOG/$s.out | cut -c1-90)"
done
$P -I -B $D/workflows/check_workflows.v1.py --report $LOG/workflows.json >$LOG/workflows.out 2>&1
echo "workflows exit=$? :: $(tail -1 $LOG/workflows.out | cut -c1-90)"
$P -I -B $D/native/check_native_evidence.v2.py --report $LOG/native.json >$LOG/native.out 2>&1
echo "native exit=$? :: $(tail -1 $LOG/native.out | cut -c1-90)"
echo "--- failing check ids (first 40) ---"
grep -h "^FAIL" $LOG/*.out | head -40
