# ADDENDUM — author fault-run evidence vs independent nine detections

**Standing:** evidence correction only. REVIEW.md (`5bfc6aaa…bfba`, 3412 B), findings.json (`f26363f7…a4c0`, 1250 B) and pins.json (`96e16c45…1903`, 1785 B) are **unchanged**. Codec ACCEPT-UNIT for inert decode is **not** withdrawn. Author **nine-kill claim in frozen `fault-results.r1.json` is not valid**. No product edits.

---

## Author frozen `fault-runs-r1` is FileNotFound, not a semantic kill

Every frozen `fault-runs-r1/<variant>/check.stderr` ends:

```
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/opensip-implementation/project-registry-codec373/fault-runs-r1/<variant>/probe'
```

`check_faults.py` relocates argv with `s.replace(str(H.resolve())+'/', str(d)+'/')`. Recorded compile/probe commands in `compile-r1.json` / `probe-compile-r2.json` use `/tmp/opensip-implementation/project-registry-codec373/...`. `H.resolve()` for the archived checker is the checkpoint extract directory, **not** that prefix, so **no argv token was rewritten**. rustc `-o` still targeted the live `/tmp/.../project-registry-codec373/` tree (or a missing sibling). `check_differential.py --probe` was pointed at `.../fault-runs-r1/<variant>/probe`, which **never existed**. Nonzero exit was FileNotFound, then counted as `detected: true`. That is **not** a structured mismatch and **not** a typed assertion.

Do not treat author `fault-results.r1.json` as nine semantic kills. Root’s planned runner (explicit source/output paths, verify binaries exist, count only structured mismatch / expected typed assertion) is the right fix.

---

## Independent replay: nine real detections

Baseline (frozen extract + pinned identity rlib `0155345b…`, rustc 1.95.0):

```
rustc --edition=2024 --crate-name project_registry_prototype --crate-type=rlib \
  grok-out/codec-build/lib.rs \
  --extern opensip_identity=<pinned rlib> -L dependency=<368 deps> \
  -o grok-out/codec-build/libproject_registry_prototype.rlib -D warnings
rustc --edition=2024 grok-out/codec-build/probe.rs \
  --extern opensip_identity=<pinned rlib> \
  --extern project_registry_prototype=grok-out/codec-build/libproject_registry_prototype.rlib \
  -L dependency=<368 deps> -L dependency=grok-out/codec-build \
  -o grok-out/codec-build/probe -D warnings
source-audit364-env/bin/python -I -B check_differential.py \
  --probe grok-out/codec-build/probe \
  --output grok-out/differential-live.json
```

**37412** cases, **0** failures, corpus/outcomes hashes equal author r2.

Faults: each mutant `project_registry.rs` compiled **to that variant’s own** `probe` (explicit `-o`), then the same `check_differential.py --probe <variant>/probe`. Logs: `grok-out/fault-replay/fault-runs-r1/<name>/`. All nine **compiled** and **failed the harness for semantic reasons**:

| Variant | Independent detection |
|---|---|
| accept-4097-rows, accept-duplicate-namespace, ignore-live-{project,locator,incarnation}-uniqueness, wrong-marker-prefix-length | `assert not failures` after JSON `failures` (e.g. `row-count-4097` expected `R` actual `A:4097:false:4097`) |
| accept-extra-fields, lose-adoption-kind, wrong-projection-values | probe **panic** on typed round-trip / projection `assert_eq!` (intended detection route in author README) |

None of these independent logs is FileNotFound. Source acceptance of the **unmutated** codec may stand on the 37412-way match; the **author nine-kill file does not**.

---

## Terminal `exit 1` vs “all 9”

The background bash wrapper printed all nine `detected 1` lines and wrote `fault-results-live.json`, then hit a leftover debug `assert hashlib.sha256(...differential-r2.json...) == 'need'`. That **post-loop** assert is why the task is `exit 1`. It is **not** a tenth failed fault and **not** a surviving mutant. Structured result: **9/9 independently detected** after a passing baseline.

---

## Unchanged

Original 373 REVIEW/findings/pins bytes above. Not S9.3, not native, not product. Root’s runner correction is future evidence, not this addendum’s acceptance.
