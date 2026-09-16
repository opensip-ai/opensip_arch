# Prepared reviewer probes — NOT EXECUTED in this review session

Bash was denied for this whole session, so none of these commands ran and no
`results/` exist yet. Every write goes under this review directory. The snapshot,
product working tree and architecture checkout are only read. Python runs with
`-B`/`PYTHONDONTWRITEBYTECODE=1` so no `__pycache__` lands in the snapshot. Note
that the snapshot's own `tests/conformance` loader would otherwise write one into
`tools/`.

```sh
REVIEW=/tmp/opensip-implementation/m1-canonical-review-01
SNAP=/tmp/opensip-implementation/m1-canonical-subject-01
ARCH=/Users/sb/code/opensip-ai/opensip_arch
export CARGO_TARGET_DIR="$REVIEW/target"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$REVIEW/results"

# 1. Subject binding (expects 8b2c3125…ef07, 13 rows, no extra files)
shasum -a 256 /tmp/opensip-implementation/m1-canonical-subject-01.json
python3 -B "$REVIEW/probes/verify_manifest.py"

# 2. Root validation against the frozen snapshot (not the working tree)
(cd "$SNAP" && cargo test --workspace --locked --offline) > "$REVIEW/results/test.txt" 2>&1
(cd "$SNAP" && cargo clippy --workspace --all-targets --locked --offline -- -D warnings) > "$REVIEW/results/clippy.txt" 2>&1
(cd "$SNAP" && cargo fmt --all --check) > "$REVIEW/results/fmt-check.txt" 2>&1
(cd "$SNAP" && python3 -B -m unittest discover -s tests/conformance -v) > "$REVIEW/results/unittest.txt" 2>&1
(cd "$SNAP" && python3 -B tools/verify_design.py --architecture "$ARCH") > "$REVIEW/results/verify-design.txt" 2>&1

# 3. Dependency graph and build inputs (no provider/Node prerequisite expected)
(cd "$SNAP" && cargo metadata --locked --offline --format-version 1) > "$REVIEW/results/metadata.json"
(cd "$SNAP" && cargo tree --locked --offline -e normal,build,dev --target all) > "$REVIEW/results/tree-all-targets.txt"
(cd "$SNAP" && cargo tree --locked --offline -e normal,build,dev) > "$REVIEW/results/tree-host.txt"

# 4. Probes
python3 -B "$REVIEW/probes/gen_corpus.py"
(cd "$REVIEW/probes/rust" && PROBE_CORPUS="$REVIEW/probes/corpus.hex" PROBE_OUT="$REVIEW/results/rust-outcomes.txt" \
  cargo test --locked --offline -- --nocapture --test-threads=1) > "$REVIEW/results/rust-probes.txt" 2>&1
python3 -B "$REVIEW/probes/compare_reference.py"
python3 -B "$REVIEW/probes/test_verifier_probes.py" -v > "$REVIEW/results/verifier-probes.txt" 2>&1
```

`--test-threads=1` is needed because the amplification probe resets a
process-global peak-allocation counter. Its peaks undercount the transient
old+new copy inside `realloc`.

## What would change the provisional static assessment

- Any manifest row, byte count or extra file mismatch: the subject is not the one reviewed.
- Any failure in step 2: reported as-is. A pass is not relabelled from the
  initial validation run.
- Any `PANIC`, any accept/refuse or canonical-byte disagreement with
  `canonical.py`, any `canonicalLongerThanInput`, or any H golden mismatch in
  `results/reference-differential.json`.
- Any failing Rust probe whose expectation is not itself shown to misread §3.
  The expectations were derived by static reading and could be wrong, as the
  author's 699050 boundary expectation was.
- Any non-`test_observed_*` failure in the verifier probes.
