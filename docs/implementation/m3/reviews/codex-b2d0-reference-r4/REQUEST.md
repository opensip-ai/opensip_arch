# Review request: B2-D0-REFERENCE-r4, round 4 (the framework recognition reference; a binding-record correction only)

A **design-unit review**. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**. Write ONLY `REVIEW.md` and `review.json` in `/tmp/opensip-implementation/reviews/codex-b2d0-reference-r4/`.

## Boundaries

As in round 3:
- Read-only: no edits, commits or builds.
- No network, no other panes and no delegation.
- No private fixtures, keys, installation directory, held trees or T2 stores.
- You may run the checker and the mutants only from a copy under your own temporary directory.

## Why a round 4

You accepted round 3 (`codex-b2d0-reference-r3`, ACCEPT-DESIGN-UNIT, subject `ae983bcd…`). Binding it as contract successor 171 then failed `verify_design`, before any commit:
- `successor.json` listed its `parents` and `candidates` unsorted ("contract candidates paths must be sorted and unique");
- two of its parents are not accepted base or selected-contract paths, as `verify_design` requires of a parent: the plan `b2-d/PLAN-r3.md`, and the archived B2-c2 r2 `typescript_config_vectors.py`, which is a unit-review archive, not a contract member.

**The only change is `successor.json`:**
- `parents` and `candidates` are now sorted by path;
- the plan and the archived JSONC reading moved from `parents` to a new `authorities` list, with the same pins;
- the seven remaining parents are unchanged: the model, its loading closure and NE.

Every other member is byte-identical to round 3. A dry run of `verify_design`, with a scratch review and assent for this subject, passed, and its scratch files were removed.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-d-reference-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1952 bytes, SHA-256 `3bd9f9ece2f48c0da63837021e82d0f9a634ceb294534337d77fed224553fc8a`, 7 members.
- Compare every member with round 3's subject. Only `successor.json` should differ, and its pin set should equal round 3's, re-sorted and split.

## Decide

1. Is the correction exactly as stated, with no other change?
2. Is splitting `authorities` from `parents` right for a contract record? The JSONC reading is loaded by the reference but is not a base it modifies.
3. Does round 3's acceptance carry over otherwise unchanged?

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2D0REF-R4-RF-n` / `B2D0REF-R4-NBO-n`.
