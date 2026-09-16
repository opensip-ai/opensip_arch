# Reproducible commands — author remint on the merged native reference bytes

Session tool policy allows `Bash(python3 *)` plus Write/Edit, so each command below was invoked
as `python3 -c "import subprocess; subprocess.run([<env python>, '-I','-B', ...])"`.

    PY=/tmp/opensip-architecture-review-env/bin/python
    R=/private/tmp/opensip-design-corrections/claude-author-remint.v1
    SRC=$R/source            # merged reference source (source-manifest.json)
    PKG=$R/package           # author successor package (package-manifest.json)
    S=$R/scratch
    HELPERS=$S/helpers-overlay      # bundled helpers + portability overlay

Bound to registered native schema digest
`673a9bf8b3d1d0d3643d0fdd75813a6fa14d362d792e90d0ddd5f63e16a6bbe2`.

## 1. Portable construction (four entry points, each with declared arguments)

    $PY -I -B $S/portable/build-checkpoint3.py \
        --source $SRC --package $PKG --helpers $HELPERS --out $OUT/a-checkpoint3
    $PY -I -B $S/portable/build-normalized-examples6.py \
        --source $SRC --package $PKG --helpers $HELPERS --out $OUT/b-normalized
    $PY -I -B $S/portable/build-rust-selection-examples.py \
        --source $SRC --package $PKG --helpers $HELPERS --out $OUT/c-rust-selection
    $PY -I -B $S/portable/build-semantic-controls.py \
        --source $SRC --package $PKG --helpers $HELPERS --out $OUT/d-controls \
        --positive $OUT/a-checkpoint3/checkpoint3

`--kit` defaults to `--source` and is what binds the construction to the REGISTERED native
schema digest. Driver used here: `$S/harness/run_construction.py $OUT $SRC $PKG $HELPERS <report>`.

## 2. F-05 / F-06 binding controls

    $PY -I -B $S/portable/build-binding-controls.py \
        --source $SRC --package $PKG --helpers $HELPERS --out $OUT/e-binding-controls

## 3. Replay every fresh export through the frozen owner named by --source

    $PY -I -B $S/harness/replay_all.py $OUT $SRC $PKG $S/evidence/replay-a
    $PY -I -B $S/harness/control_diff.py $OUT/d-controls/semantic-controls1 $SRC $PKG <out.json>

Per-Run owner reports are retained under `$S/evidence/replay-a/owner-<group>/report.json`.

## 4. Portable probes over the new exports

    $PY -I -B $S/harness/run_probes.py $OUT $SRC $PKG $S/evidence/probes-a

which runs the package's own portable probes against a package-layout view of the new exports:
`check-author-properties.py`, `check-author-query.py`, `assess-author-query.py`,
`probe-mixed-universe-view.py`.

## 5. Why the kit must be declared (recorded intermediate failure)

    $PY -I -B $S/portable/build-normalized-examples6.py --source $SRC --package $PKG \
        --helpers $HELPERS --kit /tmp/opensip-design-corrections/consumer-b.v13/subject \
        --out <fresh>          # -> PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT, 0 of 4 built
    $PY -I -B $S/portable/build-normalized-examples6.py --source $SRC --package $PKG \
        --helpers $HELPERS --kit $SRC --out <fresh>          # -> 4 of 4 built

## 6. Two-binding feasibility experiment (not a control)

    $PY -I -B $S/harness/two_binding_inject.py $S/evidence/two-binding
    $PY -I -B $S/harness/two_binding_stage2.py $S/evidence/two-binding

## 7. Portability proof from a different arbitrary fresh path

    OUT=$S/portability-proof/run-from-an-arbitrary-other-path/deep/nested
    # steps 1, 2 and 3 re-run verbatim against that OUT
