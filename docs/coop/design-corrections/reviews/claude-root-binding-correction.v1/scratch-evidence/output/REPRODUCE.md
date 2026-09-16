# Reproducible commands

All commands use Python 3.12 at /tmp/opensip-architecture-review-env/bin/python.
Under the session tool policy only `Bash(python3 *)` is permitted, so each command below was
actually invoked as:  python3 -c "import subprocess; subprocess.run([<env python>, '-I','-B', ...])"

SCRATCH=/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch
PY=/tmp/opensip-architecture-review-env/bin/python

## 0. Build the two trees (frozen candidate25 is never written)
$PY -I -B $SCRATCH/harness/... (see below; baseline25 and src25 are copies of candidate25
   docs/ excluding design-corrections/reviews/, plus the 3 review files the pin ledger requires)

## 1. Path-grammar evidence
$PY -I -B $SCRATCH/harness/regex_matrix.py $SCRATCH/harness/patterns.json

## 2. Apply the correction (already applied in src25)
$PY -I -B $SCRATCH/harness/apply_schema.py
$PY -I -B $SCRATCH/harness/apply_native_model.py
$PY -I -B $SCRATCH/harness/apply_enum_model.py
$PY -I -B $SCRATCH/harness/apply_prose.py
$PY -I -B $SCRATCH/harness/apply_harness_fixes.py      # separable, NOT normative
$PY -I -B $SCRATCH/harness/rebind_all.py               # scratch-only pin + fixture rebinding

## 3. F-04 before/after demonstration (same script, both trees)
$PY -I -B $SCRATCH/harness/demo_f04.py $SCRATCH/baseline25 $SCRATCH/output/evidence/f04-before.json
$PY -I -B $SCRATCH/harness/demo_f04.py $SCRATCH/src25     $SCRATCH/output/evidence/f04-after.json

## 4. Q-2 mixed-universe refusal boundary (same script, both trees)
$PY -I -B $SCRATCH/harness/probe_mixed_universe.py $SCRATCH/baseline25 $SCRATCH/output/evidence/mixed-universe-baseline25.json
$PY -I -B $SCRATCH/harness/probe_mixed_universe.py $SCRATCH/src25      $SCRATCH/output/evidence/mixed-universe-src25.json

## 5. Null-change control (proves the two harness defects are content-dependent, not mechanism-dependent)
$PY -I -B $SCRATCH/harness/make_nullchange.py
$PY -I -B $SCRATCH/nullchange25/docs/coop/design-corrections/foundation/run-evaluator3-checks.py \
   --out $SCRATCH/output/evidence/suites/ev3-nullchange25

## 6. Reference suites (cwd = the tree being checked)
$PY -I -B $SCRATCH/<tree>/docs/coop/design-corrections/foundation/run-reference-checks.py \
   --report $SCRATCH/output/evidence/suites/reference-<tree>.json
$PY -I -B $SCRATCH/<tree>/docs/coop/design-corrections/foundation/run-evaluator3-checks.py \
   --out $SCRATCH/output/evidence/suites/ev3-<tree>

## 7. F-05 / F-06 reference controls, built against FROZEN candidate25
$PY -I -B $SCRATCH/harness/build_variants.py
# then, per variant, the author package's frozen checker against frozen candidate25:
$PY -I -B /tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2/check-export.v4.py \
   --input  $SCRATCH/output/evidence/fcontrols \
   --claims $SCRATCH/output/evidence/fcontrols/<tag>.claims.json \
   --source /tmp/opensip-design-corrections/candidate-subject.v25 \
   --out    $SCRATCH/output/evidence/fcontrols/owner-<tag>

## 8. Helper successor (dead parameter removed) and its equivalence proof
$PY -I -B $SCRATCH/harness/make_helper_successor.py
$PY -I -B $SCRATCH/harness/verify_successor.py

## 9. Deliverable assembly
$PY -I -B $SCRATCH/harness/assemble.py
$PY -I -B $SCRATCH/harness/manifest.py
