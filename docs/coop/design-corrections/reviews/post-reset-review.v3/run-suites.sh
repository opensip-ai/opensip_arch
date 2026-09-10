#!/bin/zsh
PY=/tmp/opensip-architecture-review-env/bin/python
S=/tmp/opensip-design-corrections/post-reset-review.v3/scratch/docs/coop/design-corrections
R=/tmp/opensip-design-corrections/post-reset-review.v3/reports
: > $R/exit-codes.txt
(cd $S/foundation && $PY -I -B run-reference-checks.py --report $R/foundation-launcher.json --report-dir $R/foundation-reports > $R/foundation.stdout 2>&1; echo "foundation exit $?" >> $R/exit-codes.txt)
(cd $S/security && $PY -I -B check-security-lifecycle.v1.py --report $R/security-lifecycle-report.rerun.json > $R/security.stdout 2>&1; echo "security exit $?" >> $R/exit-codes.txt)
(cd $S/native && $PY -I -B check_native_evidence.v2.py > $R/native.stdout 2>&1; echo "native exit $?" >> $R/exit-codes.txt; cp $S/native/native-evidence-report.v2.json $R/native-evidence-report.rerun.json)
(cd $S/workflows && $PY -I -B run-reference-checks.py --report $R/workflows-launcher.json > $R/workflows.stdout 2>&1; echo "workflows exit $?" >> $R/exit-codes.txt; cp $S/workflows/workflows-report.v1.json $R/workflows-report.rerun.json)
(cd $S && $PY -I -B check-integration.py --report $R/integration-report.rerun.json > $R/integration.stdout 2>&1; echo "integration exit $?" >> $R/exit-codes.txt)
echo done >> $R/exit-codes.txt
