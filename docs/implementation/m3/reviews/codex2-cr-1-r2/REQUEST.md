CODEX2 re-review: **CR-1 r2**, the security and DR-103 host-vocabulary contract successor for law M3-C item 7, after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-cr-1-r2`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The CR-1 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 11 members** are r1's nine paths plus two new evidence files: `evidence/audit_schema.py` and `evidence/schema-audit.json`.
- **Not part of the subject:** `cr-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It now carries the r2 pins and the review path `docs/implementation/m3/reviews/codex2-cr-1-r2/review.json`. The builder emits that same path, so `--check` passes on the unit draft too, which clears your validation note.

**Product.** Main is `cd5958b` (`cd5958b3608f44a0035566c9d4500e5005c62e91`), read-only, with 82 contract successors. r2 is built and checked against `design-lock.json@cd5958b`, read with `git show`, not the live file. r1's base was `9c11c53`. The parents, the product schema input and the manifest fixtures are byte-identical at both commits.

**Sibling.** CRC-1 is in Grok's review. Its r2 was reviewed in `reviews/grok-crc-1-r2`, and r3, which changes only its review path, is in `reviews/grok-crc-1-r3`.

## What r2 changes

The diff base is the r1 subject, `f0a5c222…`, which you reviewed. Its exact bytes for every changed member, and the r1 subject manifest, are in this directory's `r1-members/`, verified against the r1 pins.

| Member | r1 | r2 |
|---|---|---|
| `cr-1/successor.json` | 7822, `a0e23ed1…` | 10694, `5ee9beac…` |
| `cr-1/completion/manifest-schema.completed.v1.json` | 24293, `ef991be7…` | 25128, `343dc517…` |
| `cr-1/PASSAGES.md` | 4955, `a33d719d…` | 8234, `12db39aa…` |
| `cr-1/README.md` | 19194, `c7cf5194…` | 29895, `525c3b0f…` |
| `cr-1/materialization-map.json` | 2307, `67413823…` | 3819, `c154a531…` |
| `cr-1/evidence/copies-report.json` | 3319, `f03d8b6c…` | 6311, `00c7a1ad…` |
| `cr-1/evidence/build_cr_1.py` | 21511, `b41e6257…` | 27780, `04fc3c0c…` |
| `cr-1/evidence/check_cr_1.py` | 9310, `166d9b35…` | 11940, `00d1ef76…` |
| `cr-1/evidence/verify_scratch.py` | 5840, `5cab1489…` | 6264, `f30ac855…` |
| `cr-1/evidence/audit_schema.py` | — | 7188, `9739bdc0…` (new) |
| `cr-1/evidence/schema-audit.json` | — | 18532, `fa29df6d…` (new) |

### RF-CR1-1: resolved by the lead's direction, not by the offered inert reading

The lead rejected your exact repair, which declared the still-required tree inert metadata. It would leave a claim-shaped object in every closure-only manifest, and every consumer would need a reading rule for it. **The lead directed instead that closure-only roles declare no command tree.** README LD-8 records this.

**1. The copy.** `commands` becomes role-scoped. The edits beyond r1's role enum are:
- `commands` is removed from the root `/required`. `/properties/commands` is unchanged: array, CommandSpec items, 1 to 4,096.
- A root `oneOf` is added, after `additionalProperties`, with two branches that are disjoint by `role`:
  - **analyzer:** `role` is `const` `analyzer`; `commands` is required, an array with at least one item. This is exactly as before.
  - **closure-only:** `role` is one of `toolchain`, `stdlib`, `rust-dev-llvm` or `grammar`, and `commands` is typed `null`. The root types `commands` as an array, so no value satisfies both. **`commands` must be absent.**
- Each branch carries a `$comment` saying this.

**Why this shape.** The product generator's keyword subset (`tools/security/generators/manifest_shape.py`, its `allowed` set) has no `if`/`then`, `not`, `dependentSchemas` or `false` schema. `oneOf` is the conditional form it has, and the unsatisfiable type is the narrowest way to say "absent".
- **Rejected: "absent or `[]`".** That gives two spellings, and it reopens whether an empty member is a declared tree.
- **Rejected: `maxItems: 0` for the closure-only branch.** It would emit `a.len() <= 0`, which clippy's deny-by-default `absurd_extreme_comparisons` refuses. `type: null` emits `matches!(v, V::Null)`, so the generator itself is unchanged.

**2. The texts.**
- **SL:70.** The table gains a "Command tree" column: required and non-empty for `analyzer`, "none: absent" for the other four. The closure-only rules say "it carries no command tree: `commands` is absent, so it asks for no mount and claims no root command".
- **The D4 join (in SL:70).** D4's EE-5a check examines every manifest that declares a tree. For a closure-only role, any declared tree is such a claim. It is refused by the closed schema at admission (RJ-6), and at D4 as an EE-5a claim by that existing route. How EE-5a judges an `analyzer` manifest's required tree is M3-D's and is unchanged.
- **A fourth override,** DR103 `/manifestSchema/fields/8/semantics` (the `commands` field). It makes the tree role-scoped in DR-103's own words. DR103 fields/8 also carries `"required": true`, a boolean that a passage override cannot change. The semantics string states the exception, and the copy is its executable form.
- **DR103 fields/7's semantics** now says "it carries no command tree".

**3. Evidence.** `evidence/audit_schema.py` checks the copy with jsonschema 4.25.1 (`Draft202012Validator`), an engine independent of the generator:
- the parent reproduces all 11,010 verdicts of the product shape fixture (`manifest268-shape.ndjson`), which is the oracle the generated Rust shape is tested against;
- the copy changes **none** of them;
- 100 role variants on the fixture's five valid base manifests behave as LD-8 requires. `analyzer` is valid only with its tree. Each closure-only role is invalid under the parent, and valid under the copy only with `commands` absent: a tree, `[]` or `null` refuses;
- the copy uses only the generator's keywords.

**4. Product impact,** recorded in `materialization-map.json` for C2a:
- **The generated shape is regenerated.** The root node checks `commands` only when present and gains a one-of term, and two branch nodes are added. The generator itself is unchanged.
- **`component_manifest.rs:171`** indexes `m["commands"]` unconditionally, so `command_checks` must run only when `commands` is present. The schema makes that exactly role `analyzer`.
- **The fixtures need no change** (by the audit). C2a adds closure-only cases: CR-T1 to CR-T4, plus the new CR-T7 (closure-only `commands` as a tree, `[]` or `null`, and `analyzer` without `commands`, all refusing RJ-6) and CR-T8 (D4: a complete signed `grammar` manifest with no tree passes R10a).

### NB-CR1-1: applied as LD-9

CR-T4 is your exact text. SL:70 now says that a closure-only entrypoint is a regular-file entry, "never a directory or symlink". An `analyzer` entrypoint keeps RJ-3's existing in-tree resolution and executable check.
- **Rejected:** refusing `analyzer` symlink entrypoints, which is a new restriction outside CR-1;
- **Rejected:** resolving closure-only symlinks.

### Other changes

- **Stale names.**
  - The Binding section and the unit draft name `codex2-cr-1-r2`.
  - This request names CRC-1's review directories as they stand.
  - r1's request in `codex2-cr-1-r1/` is left as the record of r1.
- **The base.** The scripts default to `cd5958b`.
- **`verify_scratch.py`.** Asserts four overrides, and gains `--before-crc-1`.
- **Cross-law, for M3-D's next revision.** MD:729 (EE-3b) counts "a `commands` entry for role `analyzer`" as an excluded claim, and MD:731 (EE-5a) counts a root-command claim. DR-103 still requires an `analyzer` manifest to carry its root command. How D4 admits any `analyzer` manifest under those rows is M3-D's to state. CR-1 leaves the `analyzer` tree exactly as before.

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, and each was run twice. `--deps` is a scratch directory holding jsonschema 4.25.1, installed offline from `~/opensip-deps/wheels`.
- **`audit_schema.py --deps <dir>`**: identical to `schema-audit.json`. It covers 11,010 cases and 100 variants.
- **`build_cr_1.py --check`**: identical, the unit draft included. It also confirms that the audit audits this copy.
- **`check_cr_1.py`**: passes at `cd5958b` (the default) and at `--rev 9c11c53`.
- **`verify_scratch.py --rev cd5958b`**: 82 to 83, with four overrides, no supersession, and inventory `v134` and 55 inheritance rows unchanged. The checkout at `cd5958b` also gives 82 to 83, with 40 generation sources and 48 admission sources verified.
- **With CRC-1, both orders:**
  - `--after-crc-1` (CRC-1 then CR-1) and `--before-crc-1` (CR-1 then CRC-1) each give 82 to 84. Both read CRC-1 from disk, which is now its r3 draft.
  - The lead also bound CR-1 with CRC-1 r2's exact bytes (subject `e71ee47d…`), served in memory from `reviews/grok-crc-1-r3/r2-members/`: 82 to 84 in both orders. That harness is a lead check, not a subject member.

## Decide

1. **Is RF-CR1-1 resolved by the lead's direction?** Do closure-only manifests carry no command tree in the copy, in SL:70 and in DR103 fields/8? Is the D4 join right, including leaving the `analyzer` question to M3-D?
2. **The schema shape (LD-8).**
   - Is the `oneOf` with a `null`-typed, unsatisfiable `commands` sound and the narrowest lawful form inside the generator's subset?
   - Is the audit sufficient evidence that no existing case changes?
   - Is the generated-code impact recorded correctly for C2a?
3. **NB-CR1-1 (LD-9).** Is CR-T4's role scoping applied correctly?
4. **Did anything else change?** Diff `r1-members/` against the r2 members.
5. **Does anything you accepted in r1 no longer hold at `cd5958b`?**

## Running the evidence (optional)

From `docs/implementation/m3/snapshot-plan-c/cr-1/`:
- **Dependencies:** `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-cr-1-r2/deps jsonschema==4.25.1`
- `evidence/audit_schema.py --deps <that dir>`. Leave out `--write`.
- `evidence/build_cr_1.py --check`
- `evidence/check_cr_1.py`, and the same with `--rev 9c11c53`
- `evidence/verify_scratch.py --rev cd5958b`, and the same with `--after-crc-1` or `--before-crc-1`
- `evidence/verify_scratch.py`, which uses the checkout

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"findingResolution"`: RF-CR1-1 and NB-CR1-1;
- `"subjectManifestSha256"`: a single string, the sha256 of `cr-1-subject.json`. The lead's r2 value is `4e1b169b241212b5b6b250de0fdd85888c9a390168f766ba9a7d33968426484c`.
- `"successor"`: `{path, bytes, sha256}` of `cr-1/successor.json`. The lead's r2 value is 10694 bytes, `5ee9beace59c0c45b13fafe5e60cdd74afa7cbf281c3901cc7dfa3693f2365af`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
