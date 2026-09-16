# Exact reproduction (v5)

All commands ran from `/private/tmp/opensip-design-corrections/claude-carrier-correction.v5`, with
the reference interpreter invoked as a `python3` subprocess. Read-only against Source25, root's
planning inputs and the v4 tree; every write lands under `scratch/`.

```
RUNTIME=/private/tmp/opensip-design-corrections/claude-carrier-correction.v5
SOURCE25=/tmp/opensip-design-corrections/candidate-subject.v25
REFPY=/tmp/opensip-architecture-review-env/bin/python
PLANROOT=/tmp/opensip-design-corrections/claude-carrier-correction.v4
```

Reference environment as observed: CPython 3.12.13, SQLite 3.50.4, jsonschema 4.25.1. Driving
shell: CPython 3.14.6.

## 0. Bindings

**This runtime did not re-supply the planning inputs**, so the latest root-supplied bytes are the
immutable v4 copies, read read-only from there. Both are recorded in the output manifest:

| Bound input | SHA-256 | Bytes | Source |
|---|---|---|---|
| `commit-recovery-plan.v1.json` | `fffb820db40d84f87fb0b29b80950e495712719ebba4066824d243e0dc5b544b` | 25639 | v4 runtime |
| `implementation-boundaries-and-build-plan.md` | `b0fbe31305ffffe395564f807e1535beae7c62af978619e4c3b8e0b1dc0aec80` | 82112 | v4 runtime |
| `carrier-transition-counterexample.py` / `.json` | hashed in the manifest | — | supplied in this runtime |

Frozen Source25 manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.
C10 asserts that the before-bytes of both patched candidate25 owner files match that manifest, and
that all eight historical or frozen-schema members still match it.

## 1. Controls, in order

```
python3 -c "
import subprocess
E='/tmp/opensip-architecture-review-env/bin/python'
S='/tmp/opensip-design-corrections/candidate-subject.v25'
R='/private/tmp/opensip-design-corrections/claude-carrier-correction.v5'
V='scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
C='scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py'
runs=[
 ([E,'scratch/controls/c1.py',S,'scratch/out/c1.json'],'C1'),
 ([E,'scratch/controls/c2.py',S,V,'scratch/out/c2.json'],'C2'),
 ([E,'scratch/controls/c6-schedules.py','scratch/out/c6.json'],'C6'),
 ([E,'scratch/controls/c7-gate-bits.py','scratch/out/c7.json'],'C7'),
 ([E,'scratch/controls/c8-incompatibility-inventory.py',S,'scratch/out/c8.json'],'C8'),
 ([E,'scratch/controls/c12-d9-projection.py',S,'scratch/out/c12.json'],'C12'),
 ([E,'scratch/controls/c13-migration-prefixes.py',S,V,'scratch/out/c13.json'],'C13'),
 ([E,'scratch/controls/c14-settlement.py',R,'scratch/out/c14.json'],'C14'),
 ([E,'scratch/controls/apply-owner-patches.py',S,R],'C9'),
 ([E,C,S,R,'scratch/out/c4-check.json'],'C4b'),
 ([E,'scratch/controls/check-correction-v5.py',S,R,'scratch/out/c10.json'],'C10'),
 ([E,'scratch/controls/c11-negative-v5.py',S,R,'scratch/out/c11.json'],'C11'),
 ([E,'scratch/controls/freeze-output-manifest-v5.py',S,R],'freeze'),
]
for cmd,name in runs:
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=R)
    print(name,'rc',r.returncode); print(r.stdout[-1200:])
    if r.returncode: print('ERR',r.stderr[-800:])
"
```

Ordering: **C6, C7, C12, C13, C14 before C9**; **C9 before C4b, C10 and C11**, because those three
read `scratch/patched/`; C11 reads the model reports too. `apply-owner-patches.py` takes an
optional third argument, the planning-input root, which the negative controls use to point at a
drifted sandbox copy.

## 2. Observed results

| Control | Result |
|---|---|
| C1 inherited carrier laws | 16 DDL probes; 14/14 `reconcile_witness` rows reproduced |
| C2 proposed carrier | 35 DDL probes; migration m1–m12; dispatch on 5 databases; `chain_law` 2 now refused |
| C6 schedule controls | **78653** schedules, **0** violations, **7/7** coverage assertions; now with outcome coupling |
| C7 PS05 gate | **132** schedules, **0** violations, all four bit states |
| C8 incompatibility inventory | 8 of 9 schema-3 types admitted; exactly `SEAL` plus three alias-only ids refused |
| C12 D9 projections | **39** passed, 0 failed, against the real `StepTermination` schema |
| C13 migration prefixes | **41** passed, 0 failed; root's counterexample reproduced |
| C14 settlement | **51** passed, 0 failed |
| C9 patches | owner `+43/−1` and `+96/−0`; planning `+146/−2` and `+33/−2`; F32 preserved |
| C4b carrier validation | **74** passed, 0 failed |
| C10 v5 validation | **84** passed, 0 failed |
| C11 negative controls | **19** drifts, **17** detected; 2 undetected and documented |

## 3. Disclosed harness manipulations

C1 `L8*` and C2 `V09*` lift a trigger in an **in-memory** scratch database and reinstall it
verbatim from `sqlite_master`, because the reserved terminal slot at 9007199254740991 is
unreachable by contiguous append in bounded time. Every SQLite database in every control is
`:memory:`; no carrier or ledger file was created, opened or migrated on disk.

C11 copies the proposal tree, the controls, the two planning inputs and the model reports into
`scratch/neg5/{a,b}NN/` sandboxes and drifts the copies. The real trees are never written.

## 4. Output freeze

`scratch/output-manifest.json` carries the SHA-256 and byte length of all 10 added files, the
before/after and diff hashes of the 2 patched owner files and the 2 patched planning inputs, the
script and report hashes of all 12 controls, the `notEstablished` list, and the named PS-01 and
PS-04 dependencies. `scratch/v4-evidence/` retains the v4 report, manifest, control outputs and the
superseded v2 recovery draft, with the nested v3 evidence, all unchanged.
