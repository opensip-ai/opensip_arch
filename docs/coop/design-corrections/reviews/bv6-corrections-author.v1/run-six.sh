#!/bin/zsh
# Runs the six reference commands in the DISPOSABLE repinned copy only.
# The proposed source copy (work/) is never repinned here; root refreshes pins after final source.
set -u
R=/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/disposable/checker-run.v1/docs/coop/design-corrections
PY="/tmp/opensip-architecture-review-env/bin/python"
echo "--- 1 foundation/check-foundation.py"
( cd $R/foundation && $PY -I -B check-foundation.py --report foundation-report.json 2>&1 | tail -2 )
echo "--- 2 foundation/check-identity.py"
( cd $R/foundation && $PY -I -B check-identity.py --report identity-report.json 2>&1 | tail -2 )
echo "--- 3 security/check-security-lifecycle.v1.py"
( cd $R/security && $PY -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json 2>&1 | tail -2 )
echo "--- 4 native/check_native_evidence.v2.py"
( cd $R/native && $PY -I -B check_native_evidence.v2.py 2>&1 | tail -2 )
echo "--- 5 workflows/run-reference-checks.py"
( cd $R/workflows && $PY -I -B run-reference-checks.py --report workflows-validation-report.json 2>&1 | tail -2 )
echo "--- 6 check-integration.py"
( cd $R && $PY -I -B check-integration.py --report integration-report.v1.json 2>&1 | tail -2 )
