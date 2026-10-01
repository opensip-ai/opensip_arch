Grok review: X12-0, the remedy-text contract successor that widens the one published `CONFIG.INVALID` remedy (law X12 r3 item 7, your X12 r1 RF-2). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-config-remedy-x12-0-r1. If you run anything, use only the scratch scripts named below or read-only commands. Run git only read-only.

Law: `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` r3 (accepted by you on 2026-10-01; the reviewed bytes are `PROPOSAL-r3.md`). Item 7 "Remedy keying" and "Units after the law" define X12-0: widen the one `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` string and every published copy of it, so it stays true for the three external-configuration capability keys and for rows 1, 2 and 3a. In substance it must say: name a registered capability id and state at most one row per (capabilityId, languageMode, workspaceRoot); name exactly one bundled policy pack id; supply no policy document of your own. The exact bytes are this review's to judge. The public code stays `CONFIG.INVALID`, and no detail or alias is added. X12-0 depends on nothing and precedes X12b.

## Subject

Pins are in hashes.txt:
- `docs/implementation/m2/config-remedy-x12-0-subject.json` (the subject manifest);
- `docs/implementation/m2/config-remedy-x12-0/`, which holds `successor.json`, `README.md` and `evidence/build_x12_0.py`, `evidence/check_remedy.py` and `evidence/verify_scratch.py`.

They are untracked in arch until acceptance. The product is main at b642c45 (X12a integrated, inventory v104 selected), read-only. A clean worktree is at `/Users/sb/code/opensip-ai/opensip-x12-0`, detached at b642c45, with **no product change**. There is no schema, registry, generated-code, inventory or product change, so there is no inventory successor (v107 is not used).

## What it does

Two line overrides, both on line 1158, the table's one `CONFIG.INVALID` row:
- parent `docs/coop/design-corrections/native/native_evidence_model.v2.py` (319376 bytes, sha256 `7d1c0acf…abab8be`), the frozen v2 source the law names;
- parent `docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py`, the selected reference copy. That unit's README says the current native reference "becomes reference/native_evidence_model.py of this unit". Its line 1158 is byte-identical.

Before:

> the configured capability selection is invalid: name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot)

After (367 ASCII characters):

> the configured capability or policy selection is invalid: for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party

The README tabulates the next step the string gives for each key: the three native keys, and row 1 (an unregistered ID and `count:<n>`), row 2 and row 3a.

## Judgment calls: please rule on each

1. **Conditional wording ("for capabilities, …; for policy, …").** A flat list of all four instructions would tell a caller with a capability error to also name a pack, which is not a true next step outside an analysis request. The conditional form keeps each instruction scoped to the selection it governs. The capability sentence keeps its published words byte for byte, so the two predicates `foundation/check-identity.py` applies to this string (`registered capability id from the native capability matrix` and `(capabilityId, languageMode, workspaceRoot)`) still hold.
2. **"written exactly as name:version".** Law item 3 fixes the spelling and byte-exact matching. Naming it gives the bare-name, `:01`, uppercase and trailing-whitespace cases of row 1 a usable next step. Rejected: omitting it, which leaves those callers with "name a bundled id" and no form.
3. **"of your own or from a third party".** `SuppliedProvenance` is `User` or `ThirdParty`. "Of your own" alone would not plainly cover a component-offered document (row 2, third-party; NT-1 second limb).
4. **No row 3 wording.** Row 3 carries detail `POLICY.IMPERATIVE_KEY_REFUSED` and its own remedy, so it is not a key of this string.
5. **Both live copies, and no historical copy.** Every other accepted file that contains the string is review evidence under `docs/coop/design-corrections/reviews/` (v19 and v20 before-images, work trees, diffs, tool logs). Overriding those would falsify what was reviewed then. Rejected: overriding only the v2 source, which would leave the selected reference copy saying something different under the same code.
6. **No product change.** No product file contains any `PUBLIC_ROUTE_REMEDIES` string. The product's `schemas/sources/native-v2.schema.json` and generated `report.ts` carry only the `remedyKeyingConstraint` prose, which stays true, so there is no schema, generation or drift change. X12b embeds the string and tests it byte for byte (item 10). Rejected: adding a product constant now, which would be an inventory change with no consumer.
7. **Comment and constraint prose unchanged.** The source comment above the table (lines 1150 to 1156) records the ownership-tuple widening and stays true. The published `remedyKeyingConstraint` says "THIS IS CURRENTLY SATISFIED", and it stays satisfied after this widening.
8. **Line selectors.** verify_design allows `{"line": n}` on text parents and refuses it only on JSON parents. The precedent is source-selection-v3's override of `workflows_model.v1.py` line 380.
9. **check-identity.py is not run.** The native model refuses Python 3.14.6's Unicode 16.0.0 case data (it declares 15.0.0) with `ReferenceEnvironmentError` at import. This Mac has no Python with Unicode 15.0.0 case data (the system 3.9 has 13.0.0). `check_remedy.py` instead applies the overrides in memory, parses each result with `ast` without importing it, and checks: one changed line, the same table keys and other values, both copies equal, the two check-identity remedy predicates, the X12 conditions, ASCII, and at most 1024 characters (DomainDetail.remedy is BoundedText).

## Checks

- `check_remedy.py`: passed for both parents.
- `verify_scratch.py /Users/sb/code/opensip-ai/opensip-x12-0` (the real verify_design, with X12-0 appended over the real lock, review and assent synthetic in memory): passed; 72 contract successors, 16 inheritance rows, v104 selected, 40 generation sources, 48 admission sources and 15 aliases verified.
- Live verify_design over the unchanged worktree passes.
- `build_x12_0.py` reruns produce the same bytes.
- Full workspace on the unchanged worktree, two runs: 1366 passed, 0 failed, 3 ignored each time (the b642c45 baseline; nothing changed). Clippy `--workspace --all-targets -D warnings` and fmt are clean. `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is the widened string true for `native.requested-capability-unregistered`, `-mode-unregistered` and `-duplicate-ownership-tuple`, and for X12 rows 1 (including `count:<n>`), 2 and 3a?
- Does it say the three things item 7 requires, in substance?
- Is it the right wording? If you would change bytes, give the exact replacement string.
- Are both live copies, and only those, overridden? Is any other published copy missing?
- Rule on the judgment calls.
- Is the successor well-formed for selection, and is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of `config-remedy-x12-0-subject.json`;
- "successor": {path, bytes, sha256} of `config-remedy-x12-0/successor.json`.

This is a contract successor, so it has no `inventoryCandidateAssessment`.

Write REVIEW.md and review.json. Do not commit.
