# Reproduction — carrier correction pass v7

Every command below was executed in this runtime. All reads of Source25, the planning inputs and
the previous runtimes are read-only; only paths under this runtime's `scratch/` are written.

## Bindings

| role | path |
|---|---|
| interpreter | `/tmp/opensip-architecture-review-env/bin/python` |
| Source25 | `/tmp/opensip-design-corrections/candidate-subject.v25` |
| frozen source manifest | `/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2/source-manifest.json` — sha256 `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` |
| planning inputs | `/tmp/opensip-design-corrections/claude-carrier-correction.v4` (v4 copies; not re-supplied this pass) |
| v6 inputs | `/tmp/opensip-design-corrections/claude-carrier-correction.v6` — **cited by digest, not copied** |
| this runtime | `/private/tmp/opensip-design-corrections/claude-carrier-correction.v7` |

Set once:

```sh
PY=/tmp/opensip-architecture-review-env/bin/python
SRC=/tmp/opensip-design-corrections/candidate-subject.v25
R=/private/tmp/opensip-design-corrections/claude-carrier-correction.v7
V6=/tmp/opensip-design-corrections/claude-carrier-correction.v6
PLAN=/tmp/opensip-design-corrections/claude-carrier-correction.v4
SQL=$R/scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql
DISP=$R/scratch/proposal/docs/coop/design-corrections/security/carrier-dispatch.v3.json
cd $R
```

## Order

C9 must run before C10 and before C4b, because both read `scratch/patched/`. C6, C7, C12, C13,
C14, C15, C16, C17 and C18 must run before the freeze, because it digests their reports.

```sh
# 1. owner and planning patches  -> scratch/patched/, scratch/patches/, scratch/out/c9-patches.json
$PY scratch/controls/apply-owner-patches.py $SRC $R $PLAN

# 2. carrier and frozen-member controls
$PY scratch/controls/c1.py                          $SRC       $R/scratch/out/c1.json
$PY scratch/controls/c2.py                          $SRC $SQL  $R/scratch/out/c2.json
$PY scratch/controls/c6-schedules.py                           $R/scratch/out/c6.json
$PY scratch/controls/c7-gate-bits.py                           $R/scratch/out/c7.json
$PY scratch/controls/c8-incompatibility-inventory.py $SRC      $R/scratch/out/c8.json
$PY scratch/controls/c12-d9-projection.py            $SRC      $R/scratch/out/c12.json
$PY scratch/controls/c13-migration-prefixes.py       $SRC $SQL $R/scratch/out/c13.json
$PY scratch/controls/c14-settlement.py               $R        $R/scratch/out/c14.json
$PY scratch/controls/c16-receipt-join.py             $SRC $PLAN $R/scratch/out/c16.json

# 3. root's own atomicity method, replayed against the corrected act B
$PY scratch/controls/c15-root-atomicity-replay.py \
    $R/scratch/controls $SQL $V6/ddl-atomicity.json $R/scratch/out/c15.json

# 4. new in v7
$PY scratch/controls/c17-strict-json-propagation.py  $R $V6    $R/scratch/out/c17.json
$PY scratch/controls/c18-selected-dispatch.py $SRC $SQL $DISP  $R/scratch/out/c18.json

# 5. validators (after C9)
$PY scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py \
    $SRC $R $R/scratch/out/c4-check.json
$PY scratch/controls/check-correction-v7.py $SRC $R $R/scratch/out/c10.json

# 6. negative controls (sandboxed under scratch/neg7 only; never writes the real trees)
$PY scratch/controls/c19-negative-v7.py $R $V6 $SRC $R/scratch/out/c19.json

# 7. freeze
$PY scratch/controls/freeze-output-manifest-v7.py $SRC $R
```

## Expected results

```
C1   rc 0                       C12  passed 42  failed 0
C2   rc 0                       C13  passed 50  failed 0
C4b  passed 87  failed 0        C14  passed 57  failed 0
C6   78653 schedules, 0 violations, coverage all held
C7   132 schedules, 0 violations, all four states observed
C8   rc 0                       C15  passed  7  failed 0   v5 ['carrier_format'] -> corrected []
C9   owner before-bytes match frozen manifest: [True, True]; F32 preserved: True
C10  passed 95  failed 0        C16  passed 22  failed 0
C17  passed 73  failed 0        C18  passed 20  failed 0
C19  drifts 20  detected 20  clean 19  undetected []
freeze: added 9, owner patches 2, planning patches 2, controls 16
```

C19's N1 is detected as a crash rather than a failed check: reintroducing the duplicate `admitted`
key makes the strict loader raise `ValueError: DUPLICATE KEY: admitted` before the check body runs.
That is the intended detection.

## Independent demonstration that the strict check can fail

```sh
$PY -c "import json,sys
def nd(p):
    s=set()
    for k,_ in p:
        if k in s: raise ValueError('DUPLICATE KEY: '+k)
        s.add(k)
    return dict(p)
json.load(open(sys.argv[1]), object_pairs_hook=nd)" \
  $V6/scratch/proposal/attempt-custody.schema.v1.json
# ValueError: DUPLICATE KEY: admitted
```

The same file loads without complaint under plain `json.load`. That difference is why the v6
control results do not cover the v7 bytes.

## Outputs

| path | content |
|---|---|
| `scratch/proposal/` | the nine selected files, at their stable repo-relative paths |
| `scratch/patched/` | patched copies of the two owner files and the two planning inputs |
| `scratch/patches/` | the corresponding unified diffs |
| `scratch/out/` | one JSON report per control |
| `scratch/output-manifest.json` | frozen digests, results, `notEstablished`, standing corrections |
| `scratch/REPORT.md` | the correction report and its admitted limitations |
| `scratch/neg7/` | negative-control sandboxes (disposable) |
