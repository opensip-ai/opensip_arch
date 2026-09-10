#!/bin/zsh
# Runs selected reference suites in the DISPOSABLE repinned copy only.
# Usage: zsh run-suites.sh [foundation identity security native workflows integration]
# NOTE: this is NOT the canonical final six. Root runs the canonical six after final source and
# pins. Each suite's verdict is read from its own report JSON, not from a shell exit status.
set -u
set -o pipefail
R=/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/disposable/checker-run.v1/docs/coop/design-corrections
PY="/tmp/opensip-architecture-review-env/bin/python"
for s in "$@"; do
  case $s in
    foundation)  echo "--- foundation/check-foundation.py";        ( cd $R/foundation && $PY -I -B check-foundation.py --report foundation-report.json ) ;;
    identity)    echo "--- foundation/check-identity.py";           ( cd $R/foundation && $PY -I -B check-identity.py --report identity-report.json ) ;;
    security)    echo "--- security/check-security-lifecycle.v1.py"; ( cd $R/security && $PY -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json | cut -c1-200 ) ;;
    native)      echo "--- native/check_native_evidence.v2.py";     ( cd $R/native && $PY -I -B check_native_evidence.v2.py ) ;;
    workflows)   echo "--- workflows/run-reference-checks.py";      ( cd $R/workflows && $PY -I -B run-reference-checks.py --report workflows-validation-report.json ) ;;
    integration) echo "--- check-integration.py";                   ( cd $R && $PY -I -B check-integration.py --report integration-report.v1.json ) ;;
  esac
done
