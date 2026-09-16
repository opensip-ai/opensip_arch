# Exact reproduction

All commands were executed from the runtime root
`/private/tmp/opensip-design-corrections/claude-carrier-correction.v3`, with the reference
interpreter invoked as a `python3` subprocess. Everything is read-only against Source25 and the
bound inputs; every write lands under `scratch/`.

```
RUNTIME=/private/tmp/opensip-design-corrections/claude-carrier-correction.v3
SOURCE25=/tmp/opensip-design-corrections/candidate-subject.v25
REFPY=/tmp/opensip-architecture-review-env/bin/python
V3SQL=scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql
```

Reference environment as observed this session: CPython 3.12.13, SQLite 3.50.4,
jsonschema 4.25.1. The driving shell used CPython 3.14.6.

## 0. Verify the bindings before any work

```
python3 -c "
import json,os,hashlib
R=os.environ.get('RUNTIME')
m=json.load(open(os.path.join(R,'input-manifest.json')))
ok=True
for f in m['files']:
    b=open(os.path.join(R,'inputs',f['path']),'rb').read()
    h=hashlib.sha256(b).hexdigest()
    g=(h==f['sha256'] and len(b)==f['bytes']); ok=ok and g
    print('OK ' if g else 'FAIL', f['path'])
print('BOUND_INPUTS_VERIFIED',ok)
"
```

Frozen Source25 manifest, and a full member sweep:

```
python3 -c "
import json,os,hashlib
p='/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2/source-manifest.json'
m=json.load(open(p))
print('MANIFEST_SHA', hashlib.sha256(open(p,'rb').read()).hexdigest())
root=m['snapshotRoot']; bad=[]; missing=[]; n=0; tb=0
for f in m['files']:
    fp=os.path.join(root,f['path'])
    if not os.path.exists(fp): missing.append(f['path']); continue
    b=open(fp,'rb').read(); n+=1; tb+=len(b)
    if hashlib.sha256(b).hexdigest()!=f['sha256'] or len(b)!=f['bytes']: bad.append(f['path'])
print('verified',n,'bytes',tb,'missing',len(missing),'mismatched',len(bad))
print('SOURCE25_VERIFIED', (not missing) and (not bad) and n==m['fileCount'] and tb==m['totalBytes'])
"
```

Observed: `MANIFEST_SHA fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`,
12869 members verified, 735108187 bytes, 0 missing, 0 mismatched, `SOURCE25_VERIFIED True`.
Two files exist on disk outside the manifest, both `__pycache__` byte-compiled artifacts of
`design-corrections/foundation/identity-model.v3.py` and `canonical.py`. They are benign
byproducts of a prior session and are not manifest members.

## 1. Controls, in order

```
python3 -c "
import subprocess,os
E='/tmp/opensip-architecture-review-env/bin/python'
S='/tmp/opensip-design-corrections/candidate-subject.v25'
R='/private/tmp/opensip-design-corrections/claude-carrier-correction.v3'
V='scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
C='scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py'
runs=[
 ([E,'scratch/controls/c1.py',S,'scratch/out/c1.json'],'C1'),
 ([E,'scratch/controls/c2.py',S,V,'scratch/out/c2.json'],'C2'),
 ([E,'scratch/controls/c3.py','scratch/out/c3.json'],'C3'),
 ([E,'scratch/controls/apply-carrier-correction.py',R],'C4a'),
 ([E,C,S,R,'scratch/out/c4-check.json'],'C4b'),
 ([E,'scratch/controls/c5-negative-controls.py',S,R,'scratch/out/c5-negative.json'],'C5'),
 ([E,'scratch/controls/freeze-output-manifest.py',S,R],'freeze'),
]
for cmd,name in runs:
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=R)
    print(name,'rc',r.returncode)
    print(r.stdout[-1200:])
    if r.returncode: print('ERR',r.stderr[-800:])
"
```

C4a must run before C4b and C5, because both read `scratch/patched/`.

## 2. Observed results

| Control | Result |
|---|---|
| C1 inherited carrier laws | 16 DDL probes over 8 selected frozen members; `SEAL` refused by the frozen CHECK; machine platform ids refused; display alias admitted; 14/14 `reconcile_witness` rows reproduced; `body_sha256` proven domain-framed |
| C2 proposed carrier | 35 DDL probes; migration m1–m12 with inherited rows byte-unchanged; `openDispatch.allCorrect True` over five databases; anchor-field discrimination matrix |
| C3 recovery and gate models | 21/21 recovery cases pass, 0 mutations, ledger opened exactly once per case, journal at most twice; 7/7 gate cases; 15 exhaustive latch interleavings, 0 violations |
| C4a patches | `commit-recovery-plan.v1.json` +110/−2; `implementation-boundaries-and-build-plan.md` +25/−2 |
| C4b reference validation | 82 passed, 0 failed |
| C5 negative controls | 12 deliberate drifts, 12 rejected |

## 3. Disclosed harness manipulations

Two probes (C1 `L8*`, C2 `V09*`) lift a trigger in an **in-memory** scratch database and
reinstall it verbatim from `sqlite_master` before the probe, because the reserved terminal slot
at 9007199254740991 is unreachable by contiguous append in bounded time. C1 asserts
`reinstalledTriggerTextIsFrozenText True`. No frozen file, no input and no on-disk carrier was
modified; every SQLite database in every control is `:memory:`.

C5 copies `scratch/proposal`, `scratch/patched` and `inputs` into `scratch/neg/nNN/` sandboxes
and drifts the copies. The real trees are never written.

## 4. Output freeze

`scratch/output-manifest.json` carries the SHA-256 and byte length of all 7 added files, the
before/after hashes of both patched planning inputs with their unified diffs, and the script and
report hashes of all 6 controls, plus an explicit `notEstablished` list.
