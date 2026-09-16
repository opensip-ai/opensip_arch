# Application-tooling re-review (v2) — origin 36063855-9467-40d0-a2fd-7afba09a957f

**Verdict: TOOLING_REVIEW_PASS** — tooling only. Not a final application ACCEPT, not design acceptance, no grades awarded.

Same independent origin as v1, no author origin resumed. The v1 artifact is retained unchanged; this is a separate v2 artifact.

## Custody

- `input-manifest.json` SHA256 = `8370a139d4ee7f449b0d39be011362618f8dfb1a17bc27b378586d16241d60a5` — **matches**.
- All **26** files verified byte-exact (SHA256 and byte length). No extra entries, none missing.
- **8 changed** files re-read completely. **11 unchanged** files reuse the v1 full read, with custody established mechanically: each carries a v2 manifest digest byte-identical to the v1 entry this same origin read completely. **7 new** files: the staged generator read fully; `check-retain-public.v1.py` read at head plus targeted search and then executed in full; the staged finalizer verified byte-identical to the already-read original; the four counterexample-fixture files hashed and executed as the suite's contrast case.
- Nothing written outside this runtime's `scratch/`, `review.md` and `review.json`. Both the v1 and v2 inputs trees were verified clean afterwards — no unlisted entries, no `__pycache__` (I ran every probe under `-B` this time).

## All eleven findings are fixed and independently re-verified

| | Correction | Verified by |
|---|---|---|
| **F1** MAJOR | retain `:87` now uses the Grok+Claude union | all four Claude author origins now **REFUSED** (v1: all four retained) |
| **F2** MAJOR | `refuse_coauthor_process` hoisted to `:59`, both vendors | coauthor standing and author-origin `--resume` now **REFUSED** for claude |
| **F3** MINOR | private filter vendor-independent; sanitized envelope written under the retained name | **zero** sentinel leaks; a non-whitelisted key is dropped too |
| **F4** MAJOR | `verify-applied.py` delegates to the shared selector | **0 of 8** shapes diverge (v1: 4 of 8) |
| **F5** MAJOR | assent digest checked at `:124`, re-checked at `:480`, verified ref recorded at `:571` | line-order proof + **executed** refusal with no `out/` created |
| **F6** MINOR | `HERE/'files'` with exact pins asserted before *and* after copy | both pins match; zero `/tmp` literals remain |
| **F7** MINOR | launch metadata records the union | sole change in the file |
| **F8** MINOR | suites re-executed in a disposable copy with source hashes bound | envelope **35/0**, retain **69/0**, no tool changed its own inputs |
| **F9** INFO | `--report` required *and* refuses to overwrite | all three contract cases confirmed |
| **F10** INFO | private dirs matched at any path component | 14/14 matrix rows, including the declared new expectations |
| **F11** INFO | DR-011-R10 attributed to the blind session id | static read; no assertion disturbed |

Two corrections came out **stronger than the remedies I proposed**: `public_view`'s Claude branch became an explicit 12-key allowlist rather than the denylist I suggested, and `--report` became required-and-non-overwriting rather than merely defaulted, so prior evidence cannot be destroyed.

The F8 result is worth singling out. The freshly executed retain report is **byte-identical** to the manifest-pinned historical `check-retain-public.v2.report.json` (`bdbee494…`). That historical evidence is not merely carried forward — it is exactly reproducible by the corrected tools.

## Correcting my own v1 severity on F6

Root found something my v1 probe missed, and it matters. I checked only that the directory `/tmp/opensip-design-corrections/application-assembly.v1/files` existed; I did not descend to the two files inside it. I confirmed root's sharper finding independently: `docs/operations/generate-current-design-catalog.py` does **not** exist under that base (the finalizer does). Since the generator is first in the v1 copy list, the v1 assembler would have raised `FileNotFoundError` on its first iteration. F6 was a hard break, not the provenance-and-portability concern I rated MINOR. The corrected version fails closed on support drift instead.

## Cohesion: nothing weakened, nothing silenced

+69/−19 lines across 8 files, 9 assertions added, **2 removed — and both are exactly the intended replacements** (the Grok-only exclusion, and the local digest selector). **No test identifier was dropped** from either disposable suite. The one informational expectation that changed — F10's nested-private case — was declared by root in advance and is labelled a NEW EXPECTATION in my probe source rather than quietly flipped. Historical reports are still copied as history under distinct names from the fresh `current-*` runs, and the pre-compaction retainer is retained and executed as an explicit counterexample rather than deleted. No scope creep, no new product scope, no generic checklist.

## Four residual items, none blocking

**G1 (MINOR)** — the F3 fix correctly made the private filter vendor-independent, but `GROK_PRIVATE_BASENAMES` contains generic names a Claude reviewer could author. I confirmed authored `summary.json` and `plan.json` are dropped from retention. Not silent: both appear in `custody.excludedPrivateSources`, and `review.md`, `review.json` and probe deltas are retained. Remedy: scope the basename set by vendor, keeping the stdout-name and nested-directory rules unconditional.

**G2 (INFO)** — the second assent re-check at `:480` runs after `accepted_files` is populated, so `ref()` may resolve against the frozen snapshot rather than the live root. Impact is minimal: the assent content is read once at `:125` before any output and the recorded digest is the verified `assent_ref`, so nothing emitted depends on that read, and the primary pre-output guard is unaffected. I could not determine whether the assent is pinned inside the accepted subject, because the real candidate-subject manifest is not an input. Remedy: check `digest(root / assent_ref['path'])` explicitly.

**G3 (INFO)** — `freeze-application.py` is unchanged and still re-asserts only the finalizer selftest, not the new current-tool receipt. Defence-in-depth only: the stage cannot exist unless `prepare-validation` succeeded, and it already asserts exit 0 and empty failure lists.

**G4 (INFO)** — the F9 remedy reached the envelope suite but not `check-retain-public.v1.py`, which writes fixed report names into its own directory with no guard, including one manifest-pinned name. Currently harmless: the rewrite is byte-identical and the orchestration runs it from a disposable copy. Latent if the tools ever change.

## Scope I did not perform

The full application root is still unavailable, so the assembler, `prepare-validation`, `freeze`, `verify-applied` and the two reference-suite runners were **not run end to end**. F5 was verified by executing the assembler *prologue* truncated at line 131 plus an AST line-order proof; F8 by extracting and running the bounded lines 86–109 block in a disposable directory. Both are bounded scopes, stated as such rather than presented as full runs. Per instruction I did not re-run the finalizer's 20+7 cases: those bytes are unchanged and no changed file touches that call path, so the v1 result carries forward.

No Grok or Claude CLI was run; no session directory, `.claude` log, or private content of any kind was read; every sentinel was an invented synthetic string. **All 32 product gates remain unperformed and condition 5 remains NOT MET.** Design acceptance is a separate question this review does not reach, and this verdict is not and cannot be a final application ACCEPT.

Per-finding dispositions, reproducers and remedies are in `review.json`; probe sources and results are under `scratch/`.
