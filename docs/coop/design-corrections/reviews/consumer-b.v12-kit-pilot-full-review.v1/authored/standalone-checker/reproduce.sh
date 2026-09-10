#!/bin/sh
# Successor pilot full review: original 80-file kit + two new export stores.
set -eu
cd /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-full-review.v1/output
exec /tmp/opensip-architecture-review-env/bin/python -I -B \
  standalone-checker/check.py
