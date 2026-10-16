# Review request: B2-D0-REFERENCE-r3, round 3 (the framework recognition reference; M3-B r9 item 16; B2-d plan r3 section 1)

A **design-unit review**. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**. Write ONLY `REVIEW.md` and `review.json` in `/tmp/opensip-implementation/reviews/codex-b2d0-reference-r3/`.

## Boundaries

- Read-only: no repository edits, commits or pushes.
- No product build or test.
- No network; no other panes; no delegation.
- Never read the private 413 fixture, signing keys, `~/Library/Application Support/OpenSIP`, held trees or any T2 store.
- **Permitted:**
  - reading, hashing, JSON parsing and Git queries;
  - running the checker and the mutants with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`, but only with **a copy of the reference directory under your own temporary directory**, so nothing in the repository is written. Both scripts write their JSON beside themselves. The arguments are `<architecture checkout> <python-packages snapshot>`, where the snapshot is `/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-d-reference-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1873 bytes, SHA-256 `ae983bcd6fbeddd986616e303aec1b8f720c4bde562124b59c0f129e60402641`, 7 members (README, the reference, the checker and its output, the mutants and their output, `successor.json`). Rehash every member, and every parent pin in `successor.json`.
- **Bases:** product main `a50ae96` (clean); architecture `1e938a466923ca2c7d1c45c6ddb7761c9019ed25` (the accepted plan r3).

## Authority

- **The B2-d plan r3,** `b2-d/PLAN-r3.md` (your `codex-b2d-plan-r3`, ACCEPT, with NBO-1 carried). Sections 1 to 4 define the five changes and their rules.
- **Law M3-B r9 item 16**, and NE §8 (`native-evidence.md:2749-2777`).
- **The B-S9 model** (contract successor 81) and the archived B2-c2 r2 `parse_jsonc` (your `codex-b2c2-r2`).
- **Product:** `crates/identity/src/toml.rs` (`parse_toml`'s profile and walk), `crates/identity/src/closure.rs` (the `recognitionId` check), and `schemas/sources/framework-recognition-plan-v1.schema.json`.

## Earlier rounds

- **Round 1** (`codex-b2d0-reference-r1`): three findings.
- **Round 2** (`codex-b2d0-reference-r2`): two findings, **RF-1** (the unseparated empty flow) and **RF-2** (a CR at the end of input).

The README's "r3 changes" and "r2 changes" tables map each finding to its fix, controls and mutant. The checker now runs 143 checks and there are 17 mutants.

## Decide

0. **The round-2 findings.** Is each one resolved, with no new defect? Look again at the YAML subset as a whole: is there any input it accepts that is not a `packages:` sequence of strings?

1. **Fidelity to the plan.** Does the reference call the model unchanged and apply exactly the five changes, each as the plan states? Is everything else the model's? Look closely at:
   - the byte handling: UTF-8 decoding for the model, `""` for a non-UTF-8 `package.json`, and every evidence hash taken over the bytes;
   - the Cargo replacement: its result shapes, its order, and the unparseable disclosure's `target/` convention;
   - the tsconfig selection, which keeps the model's first of `tsconfig.json` and `jsconfig.json`.
2. **The TOML profile.** Do `parse_cargo`'s byte cap, UTF-8 and BOM handling and node walk equal `parse_toml`'s? Is the recursion limit correctly the one labelled divergence?
3. **The YAML subset.** Does `parse_pnpm_packages` implement plan section 2 as revised for B2DPLAN-R1-RF-4? Is excluding plain scalars that a YAML parser would type as null, boolean, number or date sound and complete? Construct inputs it accepts that are not a `packages:` sequence of strings.
4. **FR-4 and FR-2.** Check:
   - the bound validator;
   - the per-unit all-or-nothing entry bound, which holds under an override;
   - explicit `[]` versus absent (the plan's r3 RF-1 and RF-2);
   - the state rule.
5. **Identity.** Does `unit_recognition`'s `recognitionId` equal what `closure.rs` checks? Is the provenance rendering right?
6. **Evidence.** Are the 110 checks and 12 mutants adequate? Is anything the plan promises unchecked? Note that the skipped-under-override mutant is caught by the reference's own schema validation.
7. **Binding.** Is `successor.json` right for contract successor 171 (parents, candidates, no passage override)?

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2D0REF-R3-RF-n` / `B2D0REF-R3-NBO-n`.
