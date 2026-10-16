# B2-d0: the framework recognition reference (M3-B r9 item 16; B2-d plan r3 section 1)

**Lead design record, 2026-10-16. Proposed, round 3; it needs Codex design review. It would be bound as contract successor 171.**

## r3 changes (Codex `codex-b2d0-reference-r2`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2D0REF-R2-RF-1:** `packages:[]` with no separation | The empty flow form needs at least one space after `packages:`. `packages:[]`, with or without a comment, is refused and disclosed through recognition; `packages: []` and `packages: [] # c` are accepted. Mutant: `yaml-empty-flow-unseparated`. |
| **RF-2:** a CR at the end of input | Only CRLF pairs are normalized. Every remaining CR, at the end of input included, is refused before parsing. End-of-input CR after a block item, after the empty flow form and in a comment are refused and disclosed; LF, CRLF and no-final-newline forms are accepted. Mutant: `yaml-eof-cr-stripped`. |

## r2 changes (Codex `codex-b2d0-reference-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2D0REF-R1-RF-1:** a bare `packages:` is null, not an empty sequence | A block-form key needs at least one item. `packages: []` stays the empty form. The bare key and a comments-only value are refused, and recognition discloses them (`config-requires-evaluation`, `partial`). Mutant: `yaml-null-packages-accepted`. |
| **RF-2:** YAML characters | The whole document, comments included, is checked before parsing against YAML 1.2's c-printable set, less TAB, a bare CR, DEL, the C1 block, NEL, U+2028, U+2029 and an inner BOM. NUL in plain, single-quoted, double-quoted and comment text, DEL, C1, NEL and both separators are refused and disclosed; non-ASCII scalars are accepted. Mutant: `yaml-characters-unchecked`. |
| **RF-3:** Python's decimal-digit limit | The parse lifts Python's integer string-conversion limit (4,300 digits) and restores it afterwards, so integer admission matches `parse_toml`, which keeps literals unnarrowed. The byte and node bounds still hold. Controls: 4,300, 4,301 and 100,000 digits beside usable package and workspace tables, plus the limit restored. Mutant: `toml-python-digit-limit-kept`. |

B2-d's product oracle. `reference/framework_recognition_reference.py` loads the selected native model (contract successor 81, `b-s9/reference/native_evidence_model.py`) at its accepted bytes, with its loading closure pinned as B2-c0 pins it. It calls the model's `recognize_frameworks` unchanged, then applies exactly the five changes of the accepted plan r3 (`b2-d/PLAN-r3.md`; Codex `codex-b2d-plan-r3`):

1. **`Cargo.toml` is parsed** on `parse_toml`'s profile: 4 MiB, UTF-8 without a BOM, and at most 1,000,000 value nodes, counted as its walk counts.
   - The model's regex results are replaced by results decided on the parsed `workspace` and `package` tables.
   - Every parse error gives one disclosure (`cargo-package`, `inferred`, `<unparseable>`, `target/`, `Cargo.toml-not-toml`) and an unknown Cargo-workspace fact.
   - The `toml` crate's recursion limit is the one labelled divergence. Its controls are product-only (B2-d2).
2. **`tsconfig.json` and `jsconfig.json` are parsed** by item 14a's JSONC reading, the archived B2-c2 r2 `parse_jsonc`, pinned, within its 64 KiB file bound. A failure gives `inferred` and `tsconfig-not-jsonc`.
3. **`pnpm-workspace.yaml` is read by the closed YAML subset** (`parse_pnpm_packages`, plan section 2). Outside it, the result carries `config-requires-evaluation` and no effect.
4. **FR-4 and FR-2.**
   - The bound validator (32 results, 1 to 64 evidence files) runs on every result.
   - The entry bound is per unit and all or nothing over the distinct union of entry points (65,536). It holds under an explicit override too.
   - Explicit entry points, which are a resolved `discovery.entryPoints` field won by a carrier, `[]` included, give `{state: all, source: explicit}`.
5. **The state rule:** `partial` on any unresolved choice; otherwise `all` with entries; otherwise `none`.

It also provides the pieces B2-d1 and B2-d2 need:
- the Cargo-workspace fact (`cargo_workspace_fact`);
- the `DISCOVERED:<id>@<version>` rendering;
- `UnitRecognitionV1` rows, with their derived `recognitionId`.

Inputs are bytes. Every evidence hash is taken over the file's bytes, and paths stay unit-root-relative (FR-6 to FR-8 are not applied).

## Evidence

**`evidence/check.py` runs 143 checks** (`evidence/checks.json`), all passing:

| Group | What |
| --- | --- |
| recognizers | One positive case per recognizer, and its config-requires-evaluation, parse-failure or negative case; `observedHints` |
| changes | Model equality on eight inputs the changes do not touch. Each change's effect against the unwrapped model: `[workspace.dependencies]` alone, a header inside a string, an unparseable `Cargo.toml`, an invalid or over-64-KiB tsconfig, an outside-subset `pnpm-workspace.yaml`, the state rule's four cases, and a non-UTF-8 `package.json` |
| bounds | The validator at 32/33 results and 0/64/65 evidence files, called directly. The per-unit entry bound at 65,536 and 65,537 split across results, with overlap, and alone in one result, each with no override, explicit `[]` and an explicit list |
| toml | 4 MiB and one past; 1,000,000 nodes and one past; usable tables beside deep and wide fields; decimal integers of 4,300, 4,301 and 100,000 digits (r2); a BOM; the workspace fact |
| yaml | 14 accepted productions and Unicode scalars; 50 refused forms, including the plan's r2 cases (terminal colon, colon-tab, a dash without separation, a bare dash), this unit's r2 and r3 cases (a null value, forbidden characters, an unseparated empty flow, an end-of-input CR) and the bound; recognition's disclosure of two of them |
| explicit | Absent, explicit `[]`, explicit non-empty, and recognized results kept as disclosure |
| identity | The `recognitionId` preimage (`opensip.product.v1`, domain, length, canonical record), a version bump changing it, and the provenance rendering |

**`evidence/mutants.py` runs 17 negative controls** (`evidence/mutants.json`), each weakening one change. The checker fails on every one:
- the Cargo regex kept;
- JSONC or YAML unchecked;
- the entry bound per result, or skipped under an explicit override;
- the state rule reverted;
- explicit `[]` read as absent;
- a plain-scalar colon admitted;
- the dash separation dropped;
- the node limit off by one;
- the byte cap dropped;
- the evidence bound dropped;
- the three r2 mutants: a null value accepted, characters unchecked, and Python's digit limit kept;
- the two r3 mutants: an unseparated empty flow accepted, and an end-of-input CR stripped.

The skipped-under-override mutant is caught by schema validation: the output carries 65,537 entries, over `maxItems`.

**Run:** `python3 -I -B evidence/check.py <architecture> <python-packages snapshot>`, then `mutants.py` with the same arguments.

## Not changed

- No byte of the model, of NE, of a schema or of the product.
- No FR-6 to FR-8.
- No qualification.
