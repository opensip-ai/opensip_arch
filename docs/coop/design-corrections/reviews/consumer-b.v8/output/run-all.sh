#!/bin/sh
# Executable from-scratch reconstruction command for OpenSIP DR-011-R10,
# blind consumer B.  Recomputes every identity and validates every complete
# positive graph from the input kit alone.
#
#   sh /tmp/opensip-design-corrections/consumer-b.v8/output/run-all.sh
#
# Exit status is nonzero if any suite reports a FAIL or any Run fails to close.
set -e
PY=/tmp/opensip-architecture-review-env/bin/python
W=/tmp/opensip-design-corrections/consumer-b.v8/output/work
O=/tmp/opensip-design-corrections/consumer-b.v8/output

echo "=== 0. input manifest: verify all 46 file hashes ==="
$PY -I -B "$W/verify_manifest.py"

echo
echo "=== 1. canonical encoder C, H frames, lexical admission, CVE1 ==="
$PY -I -B "$W/t_smoke.py"

echo
echo "=== 2. capability-manifest admission (ADM-TYPE/CLOSED/DOMAIN/ORDER) ==="
$PY -I -B "$W/t_capman.py"

echo
echo "=== 3. TypeScript Run: complete positive graph ==="
$PY -I -B "$W/t_ts.py"

echo
echo "=== 4. TypeScript negatives and cross-record laws ==="
$PY -I -B "$W/t_ts_neg.py"

echo
echo "=== 5. TypeScript configuration-graph variants ==="
$PY -I -B "$W/t_ts_config.py"

echo
echo "=== 6. Rust mixed-edition workspace, ownership selection, H preimages ==="
$PY -I -B "$W/t_rust.py"

echo
echo "=== 7. rust-cargo-prepared and the prepared/execution boundary ==="
$PY -I -B "$W/t_prepared.py"

echo
echo "=== 8. compiler-free syntax-only Runs ==="
$PY -I -B "$W/t_syntax.py"

echo
echo "=== 9. imported evidence ==="
$PY -I -B "$W/t_import.py"

echo
echo "=== 9b. findings, fingerprints and the citation closure ==="
$PY -I -B "$W/t_finding.py"

echo
echo "=== 10. provider protocol major 3 state law and traces ==="
$PY -I -B "$W/t_protocol.py"

echo
echo "=== 11. invocation, availability, public failure envelopes, D9 ==="
$PY -I -B "$W/t_workflow.py"

echo
echo "=== 12. baseline audit, comparison axes, authorization, repair, RC-1 ==="
$PY -I -B "$W/t_part3.py"

echo
echo "=== 13. measured design gaps ==="
$PY -I -B "$W/t_gaps.py"
$PY -I -B "$W/t_gaps2.py"

echo
echo "=== 14. object table + blob export, then RE-VERIFY FROM THE EXPORT ALONE ==="
$PY -I -B "$W/export.py"

echo
echo "=== 15. summary ==="
$PY -I -B "$W/summarize.py"
