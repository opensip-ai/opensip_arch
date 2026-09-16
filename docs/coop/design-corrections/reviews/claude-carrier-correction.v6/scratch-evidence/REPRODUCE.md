# Exact reproduction (v6)

All commands ran from `/private/tmp/opensip-design-corrections/claude-carrier-correction.v6`, with
the reference interpreter invoked as a `python3` subprocess. Read-only against Source25, root's
supplied files and the v5 tree; every write lands under `scratch/`.

```
RUNTIME=/private/tmp/opensip-design-corrections/claude-carrier-correction.v6
SOURCE25=/tmp/opensip-design-corrections/candidate-subject.v25
REFPY=/tmp/opensip-architecture-review-env/bin/python
PLANROOT=/tmp/opensip-design-corrections/claude-carrier-correction.v4
V5=/tmp/opensip-design-corrections/claude-carrier-correction.v5
```

Reference environment as observed: CPython 3.12.13, SQLite 3.50.4, jsonschema 4.25.1. Driving
shell: CPython 3.14.6.

## 0. Bindings

Root supplied `ddl-atomicity.py`, `ddl-atomicity.json` and `root-F00-F37-proposed.json` in this
runtime. **None is modified**; all three are hashed in the output manifest under
`bindings.rootSuppliedThisRuntime`. The v5 `carrier-transition-counterexample.*` files are hashed
under `bindings.rootSuppliedEarlier`.

Planning inputs remain the immutable v4 copies (`fffb820d…` 25639 B and `b0fbe313…` 82112 B),
because no later runtime re-supplied them. Frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`; C10 asserts that both patched
owner files' before-bytes match it and that all eight historical members still do.

## 1. Controls, in order

```
python3 -c "
import subprocess
E='/tmp/opensip-architecture-review-env/bin/python'
S='/tmp/opensip-design-corrections/candidate-subject.v25'
P='/tmp/opensip-design-corrections/claude-carrier-correction.v4'
R='/private/tmp/opensip-design-corrections/claude-carrier-correction.v6'
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
 ([E,'scratch/controls/c15-root-atomicity-replay.py','scratch/controls',V,
   'ddl-atomicity.json','scratch/out/c15.json'],'C15'),
 ([E,'scratch/controls/c16-receipt-join.py',S,P,'scratch/out/c16.json'],'C16'),
 ([E,'scratch/controls/apply-owner-patches.py',S,R],'C9'),
 ([E,C,S,R,'scratch/out/c4-check.json'],'C4b'),
 ([E,'scratch/controls/check-correction-v6.py',S,R,'scratch/out/c10.json'],'C10'),
 ([E,'scratch/controls/c11-negative-v6.py',S,R,'scratch/out/c11.json'],'C11'),
 ([E,'scratch/controls/freeze-output-manifest-v6.py',S,R],'freeze'),
]
for cmd,name in runs:
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=R)
    print(name,'rc',r.returncode); print(r.stdout[-1200:])
    if r.returncode: print('ERR',r.stderr[-800:])
"
```

Ordering: **C6, C7, C12, C13, C14, C15, C16 before C9**; **C9 before C4b, C10 and C11**, because
those read `scratch/patched/`; C11 also reads the model reports.

## 2. Observed results, with the v5 comparison

| Control | v5 | v6 | Note |
|---|---|---|---|
| C1 inherited carrier | 16 probes | 16 probes, 0 failures | unchanged |
| C2 proposed carrier | 35 probes | 35 probes, 0 failures | unchanged |
| C6 schedules | 78653 / 0 violations / 7 coverage | 78653 / **0** / **8** coverage | pending-settlement interval added; the 77 spurious contradictions are gone |
| C7 PS05 gate | 132 / 0 | 132 / 0 | unchanged |
| C8 incompatibility | 8 of 9 types | 8 of 9 types | unchanged |
| C12 D9 projections | 39 passed | **42** passed, 0 failed | both evaluator3 selectors now asserted |
| C13 migration prefixes | 41 passed | **50** passed, 0 failed | act B atomicity, mid-DDL failure, partial-object refusal added |
| C14 settlement | 51 passed | **57** passed, 0 failed | lawful interval + composed commit/reader/sweep case |
| C15 atomicity replay | — | **7** passed, 0 failed | new |
| C16 receipt join | — | **22** passed, 0 failed | new |
| C4b carrier validation | 74 passed | 74 passed, 0 failed | unchanged |
| C10 bounded validator | 84 passed | **90** passed, 0 failed | scoped-identity and E3 checks added |
| C11 negative controls | 19 drifts / 17 detected | **21** drifts / **20** detected | A2 still undetected by design |

The single decisive number: `v5ActBSurvivingObjects = ["carrier_format"]` →
`v6ActBSurvivingObjects = []`.

## 3. Disclosed harness manipulations

C1 `L8*` and C2 `V09*` lift a trigger in an **in-memory** scratch database and reinstall it
verbatim, because the reserved terminal slot is unreachable by contiguous append in bounded time.
C13 and C15 inject one SQL failure into a **copy** of the DDL text. C11 drifts copies inside
`scratch/neg6/` sandboxes. Every SQLite database in every control is `:memory:`; no carrier or
ledger file was created, opened or migrated on disk.

## 4. Output freeze

`scratch/output-manifest.json` carries hashes for all 9 added files, both patched owner files and
both patched planning inputs with their diffs, all 14 controls, the corrected `notEstablished`
list, a `standingCorrections` block naming the two stale v5 metadata claims, and the named PS-01 /
PS-04 dependencies. `scratch/v5-evidence/` retains the v5 report, manifest and control outputs
with the nested v4 and v3 evidence, unchanged.
