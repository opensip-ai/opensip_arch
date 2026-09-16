# Application-tooling follow-up review (v3) — origin 36063855-9467-40d0-a2fd-7afba09a957f

**Verdict: TOOLING_REVIEW_PASS** — scoped to the G1–G4 follow-ups. Not a final application ACCEPT, not design/blind/source acceptance, no grades.

Same independent origin as v1 and v2, both retained unchanged and re-verified byte-identical here. Read-only throughout.

## Custody

- `input-manifest.json` SHA256 = `7e1e0165c9800c8c937b40598056a4f18fa056efaa700952dcb57711bd4fd47f` — **matches**.
- All **26** files verified byte-exact (SHA256 and byte length). No extras, none missing, nothing new, nothing removed since v2.
- **6 changed**, **20 unchanged**. Read account: `check-retain-public.v1.py` and `freeze-application.py` read **fully** in v3 (the former for the first time in any of my reviews — v2 saw only its head). The other four changed files carry v2 full reads by this same origin plus the **complete, untruncated** unified diff against those exact v2 bytes — one changed line each for the assembler and `prepare-validation`, two for the retainer, one hunk for `retain_public`. I state that as a custody basis rather than dressing it up as a fresh full read.
- Unchanged files reuse earlier full reads on verified digest identity. The four counterexample-fixture files remain historical contrast material — hashed and executed, not line-reviewed.
- Writes confined to this runtime's `scratch/`, `review.md`, `review.json`. The v1, v2 and v3 inputs trees all verified clean afterwards — no modifications, no unlisted entries, no `__pycache__`.

## All four follow-ups are implemented as described and independently verified

**G1 — vendor-scoped private names.** The helper gained an optional `vendor` parameter defaulting to `"grok"`, guarded by `assert vendor in ("grok","claude")`; both retainer callsites pass it. **60/60** matrix cases and **6/6** vendor-guard cases: `summary.json`/`plan.json` private for Grok, exempt for Claude; all **15** other conservative private names still excluded for *both* vendors; private directories at **any** path component still unconditional for both; five invalid vendor strings all refuse. The ordering matters and is right — the stdout check runs *after* the vendor branch, so the exemption **cannot** defeat the raw-stdout rule. End-to-end through the real retainer, **12/12**: authored `summary.json`, `plan.json`, `review.md` and `work/probe.py` retained; `system_prompt.txt`, `events.jsonl` and nested `work/compaction/note.txt` excluded and declared in custody; zero sentinel leaks.

**G2 — live-root assent re-check.** Line 480 is now `digest(root / assent_ref['path']) == assent_ref['sha256']`, with no `ref()` or `source_path()` in the expression. I ran a side-by-side differential using the assembler's *own* helper definitions, in a namespace where the assent sits inside `accepted_files` and the snapshot copy differs from the live one: the v2 expression resolves to the snapshot and its outcome is insensitive to live-root mutation, while the v3 expression reads the live bound copy and flips to false when that copy is tampered. The pre-output check at line 124 is untouched and still executes as the governing guard — a tampered assent refuses with *"Root design assent changed after binding"* and no `out/` directory is created.

**G3 — freeze requires the current-tool receipt.** Seven new assertions sit at lines 44–57, **before** `before.mkdir()` and well before the stage manifest, retained manifest and archive. **20/20** cases: the positive control freezes; refusals cover missing receipt, one run, three runs, wrong suite name, both runs the same suite, duplicate `sourceFiles` paths, receipt claiming application performed, source sha drift, source byte-length drift, source content drift on disk, missing source, report sha drift, report content drift on disk, missing report, non-zero exit code, a report with a non-empty `failed` list **even when its hash matches**, a report claiming application performed, and path traversal in both `sourceFiles` and `report`. In all 19 refusals **none** of the four freeze outputs appeared.

**G4 — distinct fresh report paths.** Both `--report` and `--envelope-report` are required, asserted distinct by resolved path and asserted non-existent, at lines 20–21 — before module setup (23) and before the first suite execution (53). **7/7** contract cases, and in every refusal **zero** files were created, including the fresh path supplied alongside the offending one, which is what actually demonstrates the refusal precedes execution. Independently re-measured in disposable copies with exact helpers and the historical fixture: retain **69 passed / 0 failed**, 69 unique IDs, existing40 **40/40**; its embedded envelope report 20/20; envelope suite **35 passed / 0 failed**, existing20 **20/20**. No tool changed its own inputs. Against my own v2 measurement the IDs are **identical in set and in order** for both suites — nothing dropped, nothing added.

Worth noting: the freshly generated retain report is *still* byte-identical to the manifest-pinned historical `check-retain-public.v2.report.json` (`bdbee494…`). Adding required CLI arguments did not perturb report bytes, so the historical evidence stays history while remaining exactly reproducible.

## Cohesion: nothing weakened, nothing silenced

+33/−8 lines across 6 files; 10 assertions added; **3 removed, and all three are exactly the intended in-place replacements** (`ref()`→`digest(root/…)`, and the two 2-arg→3-arg helper calls). Test identifiers **79 → 79**, none removed. Both suites reproduce the same control IDs in the same order as my v2 run, with the `existing40`/`existing20` subsets intact. Every changed line maps to a declared follow-up; no unrelated design-suite changes, no new product scope.

## Preserved failure

`preparation-failure.md` records that the initial preparation mistakenly treated the flattened review-only finalizer as a top-level mutable source, hit `FileNotFoundError` before any manifest or launch, launched no Claude process, and verified existing partial input copies identical before continuing. I checked the custody claim independently: the flattened copy, the staged `files/` copy and both v2 copies are all byte-identical (`d3f8d4ce…`), and both assembler support pins still match the staged bytes. The claim holds. That no process was launched is attested by the record and is not verifiable from these inputs.

## Two INFO observations — explicitly not blocking

**H1** — the retain suite reads one external absolute path (`…grok-application-successor-preparation.v2/prepared/retain-application-review.successor.v1.py`, at lines 607–617) that is neither manifested nor hash-pinned, unlike the `public-custody-before-compaction.v1` fixture v3 correctly bundled. It exists here and the control passes; if absent the suite would raise and staging would fail closed. I flag it only because this is the same class of dependency as the original F6, whose path turned out to actually be missing. Bundling and pinning it would be consistent hardening — **optional, not required for this verdict**.

**H2** — because the stdout rule correctly beats the G1 exemption, an authored file whose name equals `launch.stdoutName` would be replaced by the sanitized envelope. Reaching that needs a deliberate misconfiguration (the Claude default is `response.json`) and the exclusion is declared in custody either way. **No action needed.**

## Scope I did not perform

G3 was a **bounded guard execution**, not an end-to-end freeze of a real application package: the full application root is absent, so a minimal synthetic stage satisfied freeze's earlier preconditions to reach the new block. G2's line-480 check was verified statically and by expression differential, **not** reached by execution, because it sits after draft and source-delta stages whose fixtures are not among these inputs; the line-124 check *was* executed. The assembler, `prepare-validation` and `verify-applied` again were not run end to end. The 69 and 35 counts are my own measurement; root's separate claim of 15 focused controls was not supplied to me and is neither confirmed nor disputed. No CLI was run, no session directory or private log was read, and every sentinel was invented.

**All 32 product qualification gates remain unperformed and condition 5 remains NOT MET.** Design acceptance is a separate question this review does not reach, and this verdict is not and cannot be a final application ACCEPT.

Per-follow-up dispositions, reproducers and evidence are in `review.json`; probe sources and results are under `scratch/`.
