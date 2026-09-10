#!/bin/zsh
# Selected suites in the v3 DISPOSABLE repinned copy only. NOT the canonical final six.
set -u
set -o pipefail
R=/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/disposable/checker-run.v1/docs/coop/design-corrections
PY="/tmp/opensip-architecture-review-env/bin/python"
for s in "$@"; do
  case $s in
    foundation)  echo "--- check-foundation.py";  ( cd $R/foundation && $PY -I -B check-foundation.py --report foundation-report.json ) ;;
    identity)    echo "--- check-identity.py";    ( cd $R/foundation && $PY -I -B check-identity.py --report identity-report.json ) ;;
    security)    echo "--- check-security-lifecycle.v1.py"; ( cd $R/security && $PY -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json | cut -c1-120 ) ;;
    native)      echo "--- check_native_evidence.v2.py"; ( cd $R/native && $PY -I -B check_native_evidence.v2.py ) ;;
    workflows)   echo "--- run-reference-checks.py"; ( cd $R/workflows && $PY -I -B run-reference-checks.py --report workflows-validation-report.json ) ;;
    integration) echo "--- check-integration.py"; ( cd $R && $PY -I -B check-integration.py --report integration-report.v1.json ) ;;
  esac
done
