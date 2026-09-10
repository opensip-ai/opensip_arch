#!/bin/sh
set -eu
cd /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-producing-law-selfaudit.v1/output
exec /tmp/opensip-architecture-review-env/bin/python -I -B \
  standalone-checker/check.py
