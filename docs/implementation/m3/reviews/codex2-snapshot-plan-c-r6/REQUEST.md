CODEX2 review: M3-C r6, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 6. It is a narrow amendment. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r6.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r6 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r5.md` (`7f76052d…`), the r5 bytes you accepted in review, without the acceptance note.
- **The source of the amendment:** M3-E1 r3, the syntax law, accepted by Codex (`docs/implementation/m3/syntax-e/PROPOSAL.md`, arch `a59390a4b`). Read its item 14a (the `clones-near` result and census), item 14b (producer and stage coordinates of syntax-universe work, with X-C1 and X-C2), its successor rows X-C1 and X-C2, and its C cross-law notes.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `3e64266` (F8a, which changed only dependency-policy rows after `30c5db1`), read-only.

**Scope.** r6 applies **exactly** E1's two cross-law items and changes nothing else. Diff r5 against r6: every change should belong to X-C1 or X-C2, or to the header and the "r6 changes" table.

## What r6 changes

1. **X-C1, by lead decision: widen** (item 9).
   - **The rename.** r5's "core import-producer closure" is named the **core provider closure**. It is the same descriptor with `kind: provider`, so the same identity.
   - **A second admitted use.** It becomes the producer of syntax-universe work: the scope enumerator, view and fact producer, stage-spec producer, enumeration-binding enumerator and `CandidateProducerResultV1` producer. That use applies **only** to records whose universe is a `native.semantic-universe.syntax.v2` identity.
   - **`semanticClosures`.** It is a member **exactly when** a syntax universe is selected.
   - **Never on TypeScript or Rust records.** It never produces one.
   - **The core adapter closure** is unchanged.
   - **Rejected,** as E1 item 14b records: re-kinding the grammar closure, and a separate projection.
   - **Controls.** C2-T13 is narrowed, and C2-T13a is added.
   - **Item 16** adds the closure to its `semanticClosures` row, and one `exec-plan2` stage per syntax universe produced by it.
   - **Follow-on wording.** CRC-1's row and item 13's wording are updated.
2. **X-C2** (item 16, step 12). C4a builds `candidateSourcePaths` for every available syntax-only `clones-near` binding:
   - the scoped first-party body-eligible paths under the cell workspace (NE:959-970), plus any path an explicit scope names;
   - a canonical set of at most 100,000 paths;
   - a zero-path census as the explicit `[]`, never omitted (`enumeration-contract.v1.md:49`; `enumeration-plan.schema.v1.json`, `candidateSourcePaths`).

   C4-T21 is added, and C4a's unit row carries both Plan legs.

## Decide

1. **X-C1.** Is the widened use of the core provider closure faithful to E1 item 14b and lawful under IDS `closureKinds` (IDS:4726-4743) and `closureMembership` (IDS:4794-4803)? Is it still confined enough that it cannot produce TypeScript or Rust records, and do C2-T13 and C2-T13a test that?
2. **X-C2.** Does the census rule match E1 item 14a and the enumeration contract's candidate-only law (`enumeration-contract.v1.md:49`)?
3. **Scope.** Does r6 change anything else in r5?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. CRC-1, which now carries X-C1, needs its own `ACCEPT-DESIGN-UNIT`. This law still takes effect only once M3-L and X12 r4 are accepted. Do not commit.
