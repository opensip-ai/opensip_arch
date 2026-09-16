I've corrected all three review-06 findings in `m1-report-projection-author-07`. The check passed from the pinned subject and from the exact frozen copy with the cwd set to the copy, the architecture checkout, and `/`; all four runs had identical outcomes. Nothing was committed, pushed or installed; independent review and root assent are still required.

**Freeze-ready subject:** `subject-files.json`, SHA-256 `b880ff9a3053a78f5fb020586de844305c9c3ce5f186024d0c3c508b90e176aa`, lists 19 files. The closure is 85 pinned files and 3 listings, re-verified after the runs; the only additions are the three accepted coverage-unit files. Envelope5 is unchanged (`45de2b0a…789d`).

**Command:** `TMPDIR=<abs dir> python -I -B <copy>/check.py --architecture ARCH --subject-strict --out <abs path>`

**Counts:**
- 193 report cases (30 accept) on 19 bases; 40 envelope cases (12 accept).
- 22 aggregate cases; 68 delivery goldens over 17 scenarios, 8 of them labelled as generic compositions.
- 8 pending goldens and 19 static-parity goldens.
- Coverage: 323 rows, all valid with no workaround.
- 22 source compiles; document cap 27,828,517 B.

## RPR6-1: dir_fd-relative opens and cwd scope — corrected
- **Hook:** every open or listing event with a non-absolute path (relative names, dir_fd-relative names, bare fds) is refused before any byte is read, whatever the cwd or target. Nothing is cwd-normalized or exempted, in trace mode too.
- **Cwd independence:** declared paths are made absolute before the hook, so the result does not depend on the cwd.
- **Scratch:** removed with my own absolute-path unlink/rmdir that never follows symlinks; `shutil` is no longer used.
- **In-process probes:** the reviewer's PoC (a) (fd on the architecture parent, cwd `/`) and PoC (b) (non-governed target, architecture cwd), plus an fd listing, a relative open and a relative scandir. All five were refused, and cwd was restored.
- **Side effects:** no architecture `__pycache__` appeared, and every scratch TMPDIR was left empty.
- **Limits stay explicit:** a trusted host is assumed; hard links, native extensions and concurrent-writer races are out of scope; there is no general process confinement claim.
- **History:** subject-06's failed wrong-cwd root run and review-06 are preserved.

## RPR6-2: fabricated skipped detail — corrected
- The recorded-detail list now excludes skipped and cancelled steps and keeps optional-step failures. A skipped step must carry exactly the owner skip termination, with no detail; this is enforced in both the ledger and the envelope join.
- **One rule for every interrupted carrier**, aligned with correction05 but not adopting it:
  - a nonempty recorded list is carried exactly in `errors`;
  - an empty list means failure carriers need `errors: []`, which stays pending, and run carriers omit `errors`.
- **Cases:**
  - the reviewer's probe E is refused;
  - a proper error alone is accepted;
  - a cancelled step with a detail is accepted only when that detail is not carried;
  - run carriers: no detail with `errors` absent is accepted; empty `errors` is refused by schema; the real detail is accepted; omitting or inventing a detail is refused.
- A new delivered golden covers an audit run carrier (pivot rejected, primary committed) carrying the pivot's detail.
- C01 and C02 now reference correction05 (`34556f3f…`) and state the final rebase duties. The optional-Run successor stays pending and the settled D9 aggregate is unchanged.

## RPR6-3: analyze `--baseline`, optional delivery, bindings — resolved concretely
- **Grammar:** `opensip analyze [--ephemeral | --baseline PATH]`, with a `--baseline` flag record, exact inventory selectors, and passage overrides at workflows lines 1097 and 1103. The default profile is code-regression. Audit-only flags are not added.
- **Variants:**
  - no-pivot: delegated primary analysis, then comparison, then render;
  - with-pivot: pivot analysis, delegated primary, then comparison with the pivot step, then render;
  - ordinary analyze keeps its self gate.
- **`--ephemeral` with `--baseline`:** refused before planning (`EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`, exit 2). If planned anyway, the owner DAG check would give `VERDICT_GATE_UNBOUND` (no pivot) or `EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` (pivot), which is why the refusal belongs before planning.
- **Owner contradiction, resolved explicitly:** golden `analyze-ephemeral-required-authority` said "--baseline adopt". Analyze never writes tracked intent and §8 reserves that for the `baseline adopt` mutation, so the golden text is corrected with exact before/after. Class, code and exit are unchanged. Note that this changes the inventory5 bytes.
- **Evidence:**
  - Every variant has full representative StepSpecs that validate against the owner StepSpec schema, the binding schema and the whole InvocationRecord.
  - All plannable variants pass the owner `validate_dag`.
  - The owner `run_invocation` was executed on four scenarios per variant, and its aggregate and exit matched the report model every time.
- **Optional delivery:**
  - Owner goldens bind an optional export step to analyze, so `analyze/primary-with-optional-export` is now a planned variant.
  - The sink-selection source is undeclared, tracked as RP-OBL-X01 (not an M1 blocker, required before M5).
  - The optional-render goldens are relabelled as generic profile compositions and no longer claim builtin plan admission.
- **repair-preview:** the evidence source is bound as the object `{runId: <bound Run>}`, and the `{step}` form is excluded. Subject-06's string form is refused by the owner schema.
- **P01:** not an M1 exit blocker, required before M5, and not a waiver of import features.

## A2 and K01
- **A2:** the query fixture's `visitedNodes` is corrected from 4 to 1 at line 512, matching executed owner neighbors pages.
- **K01:** coverage is rebased on the accepted v3 (`1388fd68…`). The unit's accepted status and subject manifest are checked, and v3 must equal v2 plus exactly `assets.rs = M1`. The validator passes base and overlay with no workaround. The historical v2 negative and an M6 control are kept. K01 is closed.

## Still open
- **M1 blockers:** RP-OBL-C01 (empty pre-Run interruption form) and RP-OBL-C02 (optional-Run selection successor).
- **M5 blockers:** RP-OBL-P01 and RP-OBL-X01. L01 is open and non-blocking.
- All 11 report feature blockers and AUDIT-G10 remain open, so the project is not complete.
- The separate evidence, timing and catalog candidates are referenced but not adopted.
- The planning, grammar and fixture records are proposals; the owner-model runs use synthetic results; no runtime, browser, generator, performance or product qualification is claimed.
- The architecture checkout already had uncommitted edits in `foundation/`; I didn't touch them, and the pins record those exact bytes.

Per-finding dispositions are in `contract.md` §2. The four run results and `closure-evidence.json` are in `scratch/`.
