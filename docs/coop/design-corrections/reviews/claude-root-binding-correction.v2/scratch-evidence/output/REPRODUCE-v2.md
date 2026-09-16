# Reproducible commands — v2 follow-up (F-04 selector segment law + guard bounds)

Tool policy in this session allows `Bash(python3 *)` plus direct Write/Edit, so each command
below was invoked as `python3 -c "import subprocess; subprocess.run([<env python>, '-I','-B', ...])"`.

    PY=/tmp/opensip-architecture-review-env/bin/python
    V1=/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch      # completed, unchanged
    V2=/private/tmp/opensip-design-corrections/claude-root-binding-correction.v2/scratch

## 1. Reproduce root's counterexamples against the completed v1 selectors
    $PY -I -B $V2/harness/reproduce_root.py $V2/output/evidence/root-reproduction.json

## 2. Exhaustive differential of the corrected selectors against the stated law
    $PY -I -B $V2/harness/selector_design.py $V2/output/evidence/selector-differential.json

## 3. Apply the fix (already applied in $V2/src25; only 2 files differ from v1)
    $PY -I -B $V2/harness/apply_selector_fix.py        # schema: the 2 new selectors only
    # guard edits applied directly to
    #   $V2/src25/docs/coop/design-corrections/native/native_evidence_model.v2.py

## 4. Controls: before (v1) and after (v2), same matrix
    $PY -I -B $V2/harness/controls_f04_v2.py $V1/src25 $V2/output/evidence/controls-v1-before.json
    $PY -I -B $V2/harness/controls_f04_v2.py $V2/src25 $V2/output/evidence/controls-v2-after.json

## 5. Three-way agreement (stated law / declarative selector / early guard), incl. length bounds
    $PY -I -B $V2/harness/declarative_agreement.py $V1/src25 $V2/output/evidence/agreement-v1-before.json
    $PY -I -B $V2/harness/declarative_agreement.py $V2/src25 $V2/output/evidence/agreement-v2-after.json

## 6. Core F-04 behaviour preserved: v1's own demo, unchanged, run against v2
    $PY -I -B $V1/harness/demo_f04.py $V2/src25 $V2/output/evidence/f04-v2-after.json

## 7. Assemble patch, changed full files, hashes, manifest
    $PY -I -B $V2/harness/assemble_v2.py

## NOT run here, deliberately
Source pins and the six fixture/pin dependencies are NOT rebound, and the full
`run-reference-checks.py` / `run-evaluator3-checks.py` suites are NOT re-run. The native schema
bytes move again with this patch, so root rebinds once when merging with completed discovery v2
and runs the integrated suites once at that point.
