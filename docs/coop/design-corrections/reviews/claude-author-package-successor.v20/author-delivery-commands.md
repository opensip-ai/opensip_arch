# Reproducible commands — native-v2 author package rebuild (author-package-migration.v1)

Reference interpreter, always `-I -B`:

    PY=/tmp/opensip-architecture-review-env/bin/python        # or any interpreter with the same pinned env
    SRC=<successor source root holding docs/coop/design-corrections>   # root: the FROZEN successor
    PKG15=<author package v15 root>                            # artifact-manifest 6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e
    OVERLAY=<migration overlay root>                           # overlay-manifest.json pins every package15 base digest
    OUT=<fresh directory>

## 1. Rebuild the package from inputs (constructs, assembles, verifies, probes, compares ids)

    $PY -I -B $OVERLAY/rebuild-author-package.v2.py \
        --source $SRC --package $PKG15 \
        --package-manifest-sha256 6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e \
        --overlay $OVERLAY --out $OUT [--source-manifest <frozen file-list JSON>]

The new package is `$OUT/package` (manifest `$OUT/package/artifact-manifest.json`). The run record is `$OUT/rebuild-report.json`, with per-command receipts under `$OUT/work/receipts/`.

The rebuild constructs these groups, each with `--source $SRC --package <constructor tree> --out <fresh>`:
- `build-checkpoint3.py`
- `build-normalized-examples6.py`
- `build-rust-selection-examples.py`
- `build-binding-controls.py`
- `build-normalization-map-controls.py`
- `build-semantic-controls.py --positive <checkpoint3>`

## 2. Re-verify an assembled package against a source

    $PY -I -B $OUT/package/verify-package.py --source $SRC --out <fresh>
    $PY -I -B $OUT/package/probe-native-v2.py --source $SRC --package $OUT/package --out <fresh>.json

`verify-package.py` refuses unless `$SRC` equals the pinned `source-manifest.json`. A package built on a provisional capture must be rebuilt, not re-pinned, for a different frozen source.

## 3. Standing

This is AUTHOR construction and self-consistency evidence under owner replay. It is not independent review, blind acceptance or qualification, and must never be supplied to a blind consumer.
