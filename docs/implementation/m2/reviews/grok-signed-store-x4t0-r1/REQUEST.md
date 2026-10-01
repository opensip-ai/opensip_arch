Grok review: X4T-0, the test-only signed accepted-store generator, with inventory v87. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-signed-store-x4t0-r1. If you build, use a CARGO_TARGET_DIR under that directory.

Law: `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` r5 (accepted), items 12 and 13, including the "Test-only record constructor" lead decision.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x4t0`, based on 99f1c35. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
- **Arch:** v87 (provisional; parent v84, renumbered at integration), `signed-store-inventory-v87-subject.json` and `signed-store-inventory-v87/`.

## What it does

The code is in `trust/accepted_store_fixture.rs`, declared only under `#[cfg(test)]`.
- **`generate(&Spec) -> AcceptedStore`.** Roles are set to chosen targets: Trusted, Expired, StaleRevocation, QuorumLost, Revoked or Unbootstrapped.
- **Built on a real P0 publication.** Root, revocation, catalog and payload manifest are signed with the public quorum62 seeds through the existing test signing helpers.
- **Records** are built through a single `encode` path (canonical bytes, then the closed-shape `admit`):
  - root and metadata admissions;
  - revocation history;
  - time evidence and the signed time source;
  - per-role acceptance and conditioning events, with their `RoleChangeV1` and `PublicationEventV1`;
  - the revision-2 descriptor;
  - the retained-phase `TrustCapsuleV1` as `state.v1`.
- **Round trip.** `current_record_bindings::bind`, `publication_events::bind_events` (replaying the capsule's roles and head), `capsule_clock` then `bind_retained_head`, and `capture_p2` on a written scratch installation all accept it.
- **Source pin.** Only `root_payload.rs`'s `cfg(test)` declaration names the module.

## Judgment calls: please rule on each

1. The phase transition is approximated: the clock-write goes unevaluated→evaluated while the capsule is retained. Its real semantics belong to X4B. Is X4T-a's stricter reader likely to need more?
2. Acceptance uses `EV-PRESENT-PAYLOAD` with closure payload evidence and a clock-write input.
3. The payload closure has no members; the manifest lists them.
4. Only documents are signed. The admissions, history and time evidence have no signature field.
5. The P0 capsule is also written to `trust/records/` so that `beforeImage` resolves.
6. Recovery is not offered as a target.
7. v87 is provisional.

## Checks

- Workspace: 1199/0, on two runs. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch (v84 then v87) passes.

## Decide

- Is it strictly test-only, with no release or production path?
- Do the records it builds genuinely pass the existing binders, rather than bypassing a check?
- Is it fit to drive X4T-a's cases?
- Rule on the judgment calls.
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of signed-store-inventory-v87-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v87, parent (the v84 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

Note: X4T r5, now accepted, also requires X4T-0 to write each role's accepted.by so that it names one of the current descriptor's events, and expects X4T-a's own loads to accept the store. Check that the generator meets this.
