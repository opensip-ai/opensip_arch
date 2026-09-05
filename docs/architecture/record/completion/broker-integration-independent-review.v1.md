# Broker integration independent review v1

**ACCEPT — 0 MUST-FIX, 0 SHOULD-FIX**, within the exact conditional broker integration scope. Reviewer: Codex distribution fixture author; authored none of the broker subjects.

Subject: `broker-bootstrap.freeze.v4.json`, SHA-256 `ab83b12f1de37ac36788d4ddc01c5f47760af6e8058a53ce1d944989124dc3c9`. All seven subject pins and 31 dependency pins matched before and after execution. The 93-check wrapper and 273-check courier reports replayed byte for byte into external files. Another 78 independent checks passed and replayed byte for byte; their executable and observations are retained in `broker-integration-independent-probes.v1.py/.json`.

The review covered the retained v3 bootstrap parser, schema, TypeScript API and physical courier implementation, plus v4's exact security receipt, host request join and full-result security joins. Independent probes challenge closed response shape, strict integer bounds, request/commit/journal-order matching, result reference grammar, refusal teardown, foreign/forged/wrong-class handles, and caps before file access. Both effect classes reject wrong operations, generations, tokens, binding and scope. HE-2 additionally requires the exact sealed snapshot/member and whole-component prefix; HE-1 preserves state-class and byte-cap constraints. Retained physical tests cover immutable staging, hard links/symlinks/FIFO, held-directory custody, digest/length failures, single-use writes and actual 16 MiB/64 MiB boundaries.

This verdict does **not** accept security v6 or authorize adoption. The broker receipt correctly records custody without security acceptance. The security unit has a separate review, and any security successor needs its own acceptance plus a bounded broker rebind confirmation. Existing security findings are not waived here.

The reference runs do not qualify asynchronous transport concurrency, four native platforms, durable journal/witness recovery, operation leases or GC fencing. Those remain separate design joins and implementation qualification gates. No live register or product status was changed.
