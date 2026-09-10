---
name: reference-suite-needs-cpython-312
description: "The opensip design-corrections reference checks refuse on any interpreter whose Unicode data is not 15.0.0, so they need CPython 3.12, not this host's default python3."
metadata: 
  node_type: memory
  type: project
  originSessionId: b20560e2-5bfb-45f8-9f75-19e13c979406
  modified: 2026-09-08T10:10:40.376Z
---

`docs/coop/design-corrections/native/native_evidence_model.v2.py` pins
`UNICODE_CASE_DATA_VERSION = "15.0.0"` and raises `ReferenceEnvironmentError` (an explicit
*environment fault*, distinct from a domain refusal) when `unicodedata.unidata_version` differs.

This host's default `python3` is **3.14.6 / Unicode 16.0.0**, so `check-identity.py` dies in under a
second there. `/Users/sb/.claude/security/agent-sdk-venv` has jsonschema but is also 3.14 — same
fault. A working reference environment as of 2026-09-08:

```
uv venv --python ~/.local/share/uv/python/cpython-3.12.13-macos-aarch64-none/bin/python3.12 <dir>
uv pip install --python <dir>/bin/python jsonschema referencing
```

CPython 3.12 → Unicode 15.0.0. `check-identity.py` then runs ~118 s and exits 0.

The launcher `run-reference-checks.py` pins 1100 source files but records **no** interpreter
precondition, so the reproducibility requirement is invisible until the run faults. Raised as an
advisory in the final peer assessment; no source path was changed for it. See
[[reference-hardening-peer-deliverable]].
