#!/bin/zsh
# Development whole-suite run ONLY.
#
# Copies the candidate source to a DISPOSABLE tree, refreshes the three unit pin
# manifests there by MEASURING the current bytes, and runs every unit checker.
#
# The refreshed pins live only in the disposable copy. They are NOT candidate
# bytes and are NOT evidence that the candidate's pins are correct: root owns the
# final pin refresh and seal after all recording edits. Presenting this output as
# accepted-candidate pin proof would be false.
set -u
B=/tmp/opensip-design-corrections/bv3-corrections-author.v2
P=/tmp/opensip-architecture-review-env/bin/python
DEV=$B/devtest
LOG=${1:-$B/logs/devtest}

rm -rf $DEV; mkdir -p $DEV $LOG
cp -R $B/work/ $DEV/

$P -I -B - <<'PY'
import hashlib, json, os
DEV = "/tmp/opensip-design-corrections/bv3-corrections-author.v2/devtest"
MANIFESTS = [
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
    "docs/coop/design-corrections/native/source-pins.v2.json",
]
refreshed = {}
for rel in MANIFESTS:
    full = os.path.join(DEV, rel)
    manifest = json.load(open(full))
    # foundation/workflows use {"files": [...]}, native uses {"pins": [...]}.
    rows = manifest["files"] if "files" in manifest else manifest["pins"]
    changed = []
    for item in rows:
        target = os.path.join(DEV, item["path"])
        if not os.path.isfile(target):
            changed.append({"path": item["path"], "fault": "missing"})
            continue
        raw = open(target, "rb").read()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != item.get("sha256"):
            changed.append({"path": item["path"], "from": item.get("sha256"), "to": digest})
        item["sha256"] = digest
        if "bytes" in item:
            item["bytes"] = len(raw)
    open(full, "w").write(json.dumps(manifest, indent=2) + "\n")
    refreshed[rel] = changed
print(json.dumps({"devPinRefresh": refreshed}, indent=2))
PY

echo "=== unit checkers (disposable copy) ==="
D=$DEV/docs/coop/design-corrections
for s in check-foundation check-identity check-product-quality check-product-configuration check-array-orders; do
  $P -I -B $D/foundation/$s.py --report $LOG/$s.json >$LOG/$s.out 2>&1
  echo "foundation/$s exit=$? :: $(tail -1 $LOG/$s.out)"
done
$P -I -B $D/workflows/check_workflows.v1.py --report $LOG/workflows.json >$LOG/workflows.out 2>&1
echo "workflows exit=$? :: $(tail -1 $LOG/workflows.out)"
$P -I -B $D/native/check_native_evidence.v2.py --report $LOG/native.json >$LOG/native.out 2>&1
echo "native exit=$? :: $(tail -1 $LOG/native.out)"
