# Exact reproduction (v4)

All commands ran from the runtime root
`/private/tmp/opensip-design-corrections/claude-carrier-correction.v4`, with the reference
interpreter invoked as a `python3` subprocess. Read-only against Source25, root's planning inputs
and the v3 tree; every write lands under `scratch/`.

```
RUNTIME=/private/tmp/opensip-design-corrections/claude-carrier-correction.v4
SOURCE25=/tmp/opensip-design-corrections/candidate-subject.v25
REFPY=/tmp/opensip-architecture-review-env/bin/python
V3=/tmp/opensip-design-corrections/claude-carrier-correction.v3
```

Reference environment as observed: CPython 3.12.13, SQLite 3.50.4, jsonschema 4.25.1. Driving
shell: CPython 3.14.6.

## 0. Bindings

Root supplied the latest planning inputs at the runtime root (not under `inputs/`), so the v3
four-file manifest no longer applies verbatim. The bound bytes for this pass are:

| File | SHA-256 | Bytes |
|---|---|---|
| `commit-recovery-plan.v1.json` | `fffb820db40d84f87fb0b29b80950e495712719ebba4066824d243e0dc5b544b` | 25639 |
| `implementation-boundaries-and-build-plan.md` | `b0fbe31305ffffe395564f807e1535beae7c62af978619e4c3b8e0b1dc0aec80` | 82112 |

Re-verified this pass: the v3 four-file input manifest (all four match), and the frozen Source25
manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`. C10 additionally
asserts that the **before-bytes of both patched candidate25 owner files match that frozen
manifest**, and that all eight historical or frozen-schema members still match it.

Root's delta from the v3 planning inputs, confirmed by diff before any work: the PS05 atomic
bit-state paragraph, the `PreparedCommit` Drop clause, the public-adapter/orphan-SEAL clause, the
F32 typed-route fix (expectedBehavior plus `verificationOwner` moving to
`crates/host/tests/retention_tests.rs`), and the separately owned syntax/provider/registry
sections. The F32 fix is asserted preserved by both C9 and C10.

## 1. Controls, in order

```
python3 -c "
import subprocess
E='/tmp/opensip-architecture-review-env/bin/python'
S='/tmp/opensip-design-corrections/candidate-subject.v25'
R='/private/tmp/opensip-design-corrections/claude-carrier-correction.v4'
V='scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
C='scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py'
runs=[
 ([E,'scratch/controls/c1.py',S,'scratch/out/c1.json'],'C1'),
 ([E,'scratch/controls/c2.py',S,V,'scratch/out/c2.json'],'C2'),
 ([E,'scratch/controls/c6-schedules.py','scratch/out/c6.json'],'C6'),
 ([E,'scratch/controls/c7-gate-bits.py','scratch/out/c7.json'],'C7'),
 ([E,'scratch/controls/c8-incompatibility-inventory.py',S,'scratch/out/c8.json'],'C8'),
 ([E,'scratch/controls/apply-owner-patches.py',S,R],'C9'),
 ([E,C,S,R,'scratch/out/c4-check.json'],'C4b'),
 ([E,'scratch/controls/check-correction-v4.py',S,R,'scratch/out/c10.json'],'C10'),
 ([E,'scratch/controls/c11-negative-v4.py',S,R,'scratch/out/c11.json'],'C11'),
 ([E,'scratch/controls/freeze-output-manifest-v4.py',S,R],'freeze'),
]
for cmd,name in runs:
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=R)
    print(name,'rc',r.returncode); print(r.stdout[-1200:])
    if r.returncode: print('ERR',r.stderr[-800:])
"
```

Ordering matters: **C9 before C4b, C10 and C11**, because all three read `scratch/patched/`.
**C6 and C7 before C10 and C11**, because both read the model reports.

## 2. Observed results

| Control | Result |
|---|---|
| C1 inherited carrier laws | 16 DDL probes; `SEAL` refused; machine ids refused; 14/14 `reconcile_witness` rows reproduced; `body_sha256` proven domain-framed |
| C2 proposed carrier | 35 DDL probes; migration m1–m12 with inherited rows byte-unchanged; dispatch correct on 5 databases; anchor-field discrimination matrix |
| C6 schedule controls | **78653** schedules over 14 configurations, **0** violations, **7/7** coverage assertions held |
| C7 PS05 gate | **132** schedules, **0** violations, all four bit states observed, permit single-use, fetch-OR idempotent, CAS from state 2 fails |
| C8 incompatibility inventory | frozen carrier admits 8 of 9 schema-3 types; refuses exactly `SEAL` and the three alias-only machine ids |
| C9 patches | owner `+35/−1` and `+54/−0`; planning `+110/−2` and `+29/−2`; F32 fix asserted preserved |
| C4b carrier validation | **74** passed, 0 failed |
| C10 v4 validation | **84** passed, 0 failed |
| C11 negative controls | 14 drifts, **13** detected; A2 undetected and reported as such |

## 3. Disclosed harness manipulations

C1 `L8*` and C2 `V09*` lift a trigger in an **in-memory** scratch database and reinstall it
verbatim from `sqlite_master`, because the reserved terminal slot at 9007199254740991 is
unreachable by contiguous append in bounded time. C1 asserts
`reinstalledTriggerTextIsFrozenText True`. Every SQLite database in every control is `:memory:`;
no carrier file was created, opened or migrated on disk.

C11 copies `scratch/proposal`, `scratch/controls`, the two planning inputs and the two model
reports into `scratch/neg4/{a,b}NN/` sandboxes and drifts the copies. The real trees are never
written. The model drifts deliberately reintroduce the exact bug each control was written to
catch; the artifact drifts break an invariant the validator asserts.

## 4. Output freeze

`scratch/output-manifest.json` carries the SHA-256 and byte length of all 8 added files, the
before/after hashes and unified-diff hashes of the 2 patched owner files and the 2 patched
planning inputs, the script and report hashes of all 9 controls, the `notEstablished` list, and the
named PS01/PS04 dependencies. `scratch/v3-evidence/` retains the v3 reports, the v3 recovery draft
and the pre-renumbering fault-case bytes unchanged.
