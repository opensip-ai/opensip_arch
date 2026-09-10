#!/bin/sh
set -eu
cd /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated
exec /tmp/opensip-architecture-review-env/bin/python -I -B \
  checker/check.py
