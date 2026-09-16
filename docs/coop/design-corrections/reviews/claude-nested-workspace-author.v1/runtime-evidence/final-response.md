I fixed the crash: nested Cargo workspace folding now picks an enclosing workspace that is actually a unit, so `discover_units` no longer raises `StopIteration`. The contract prose now says the same, and new controls cover it. No new error code was needed.

**Setup and reproduction.** Manifest39 and all 12,909 members checked out and were copied into this runtime; a final recheck showed frozen39 unchanged. A path-only copy of root's probe gave the same rows as root's `report.json`.

**Cause.** `discover_units` picked the deepest enclosing workspace manifest as the fold target, then looked it up among units with `next(...)`. A workspace manifest below another workspace unit is itself folded, so it never became a unit, and the lookup had nothing to find. The same exception escaped enumeration admission, whose handler at `enumeration_model.v1.py:667` only catches the typed admission errors. Before the fix, 918 of 8,504 inputs in an exhaustive small sweep crashed, and so did 12 of my 24 named scenarios.

**Why a surviving unit and not a refusal.** U-4b.2 folds into a workspace unit, and only a unit can hold `memberPackageRoots`. The shallowest enclosing workspace manifest always becomes a unit, and workspace units never nest, so exactly one unit always encloses a folded directory. No published rule makes this layout an error, so a refusal would reject input the contract already decides. I make no claim about whether Cargo accepts such a layout.

**Changes.**
- **Model:** a single shallowest-first pass that folds each `Cargo.toml` directory into the deepest enclosing workspace unit. The second pass with the `next(...)` lookup is gone.
- **Contract:** a U-4b.2 clarification in `native-evidence.md`.
- **Controls:**
  - one new native case covering automatic folding, explicit `.` / `.`+`nested` / `nested` / `nested/pkg`, a boundary, pruning, membership rows and scope prefixes;
  - four consumer24 M3 rows;
  - two enumeration cases, one refused with `ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION` and one admitted.

No schema bytes, codes, pins, planning or TS/JS lines changed.

**Results.** Every input that returned before the fix returns byte-identical output after it, and all 918 crashing inputs now return. Suite results:

| Suite | Before fix | After fix |
|---|---|---|
| native | 380/380 | 381/381 |
| consumer24 | 183/183 | 187/187 |
| enumeration | no mismatches | no mismatches (+2 cases) |
| integration | 412 passed | 412 passed |
| security | 464/464 | 464/464 |
| identity | 1596 passed | 1596 passed |
| workflow projection | 838 ok rows | 838 ok rows |

- **New controls fail against the frozen39 model:** consumer24 M3 crashes with `StopIteration`, and enumeration lets `StopIteration` escape.
- **Native checker against frozen39:** it aborts with a `TypeError` in its own step resolver, because later steps read the faulted result. A diagnosis run of the new case's discovery steps shows the underlying `StopIteration`.
- **Apply check:** the system `patch -p1` on the frozen39 files reproduces all five corrected files exactly.
- **All background processes finished** before the review was built.

**Things to know for integration.**
- **Pins must be updated by root.** Registered pins in five pin files still hold the old hashes of the five changed files. Without an update, the native checker reports `PIN-MISMATCH` and security reports `sourcePinsValid: false`. I ran the post-fix suites on a copy with only those pin entries updated; the delta itself touches no pin file.
- **Possible merge overlap in the model.** One model hunk's context lines include unchanged TS/JS lines 3950–3952. If the unitKind author edited those exact lines, that hunk needs a 3-way merge; I didn't read their work.
- **Sweep limits.** It covers Rust markers only, six directories and explicit selections of at most two; boundaries are covered only by named scenarios. I wrote its oracle myself, so it isn't independent.

**Failed attempts, all kept with receipts.**
- The first case insertion refused to rewrite because the file doesn't round-trip through `json.dumps`; I redid it as a text insertion that keeps every original byte.
- Two harness runs failed because output directories didn't exist: the first unpinned security run and the control-copy setup. The control-copy tool had already changed the copy before failing, so I recorded the copy's actual state with a separate check instead of rerunning.
- The first review build tried to read its own unfinished receipt.

This is not acceptance, readiness, frozen40 or a repin; root's full references and independent review follow integration.

Files are in /private/tmp/opensip-design-corrections/claude-nested-workspace-author.v1 (every command's receipt is under `receipts/`):
- review.md
- review.json
- correction.patch
- delta-manifest.json
