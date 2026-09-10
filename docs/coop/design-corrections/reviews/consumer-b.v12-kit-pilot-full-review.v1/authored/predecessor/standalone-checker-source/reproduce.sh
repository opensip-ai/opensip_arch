#!/bin/sh
# From-scratch structural admission of the six exported graphs.
# No author helpers. Kit + exported stores only.
set -eu
cd /tmp/opensip-design-corrections/consumer-b.v12-fresh-export-admission.v1/output
exec /tmp/opensip-architecture-review-env/bin/python -I -B \
  standalone-checker/check.py
