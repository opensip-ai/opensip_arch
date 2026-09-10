# Fallow design review record

Codex is the author and integration lead. Claude Code, using Anthropic model
`claude-fable-5-1`, is the independent peer reviewer and edited none of the
subject files. The user explicitly requested this collaboration.

## Scope and provenance

Claude's initial advice came from selected OpenSIP architecture chapters,
D-369/readiness material, and selected Fallow docs and sources. It was not an
exhaustive repository audit. The [initial response](claude-initial.md) states
that scope; the [original CLI result](claude-initial.json) records the actual
model and session. [The dispatch](claude-initial-prompt.txt) is retained.

Codex independently read the source catalogue in the borrow register, including
comparison, rule-pack, and changelog sources that Claude explicitly did not
recheck in the first concrete review. Claude used read-only file tools and did
not claim to execute the hash checks or the D-369 checker. Codex owns those
structural measurements. Neither party ran Fallow's analyzers or validated its
performance claims in this exercise.

## Review history

- Initial advice: useful architecture lessons, with no acceptance of a patch.
- Exchange 1: [fixed subject](subject.v1.json), [review](claude-review.v1.md),
  [structured verdict](claude-review.v1.verdict.json), and
  [dispatch](claude-review.v1.prompt.txt). CHANGES_REQUIRED: one MUST_FIX and
  three SHOULD_FIX. All failed findings and original snapshots remain intact.
- Exchange 2: [corrected fixed subject](subject.v2.json), [actual review](claude-review.v2.md),
  [structured verdict](claude-review.v2.verdict.json), and [dispatch](claude-review.v2.prompt.txt).
  ACCEPT with zero MUST_FIX and zero SHOULD_FIX. Claude resolved all four
  first-review findings and recorded no remaining design disagreements.
  The listed mechanical recording preconditions are executed as described below.

## Corrections and reconciled decisions

FR-M1: restore the V2 README's task-opening bytes. Both READMEs belong to the
D-369 custody set; the adopted reading path uses START-HERE, file 10, and the
current-design catalog. FR-S1: require the exact D-370 coordinator heading,
this review record, actual review evidence and author assent before recording.
FR-S2: name sealed Snapshot or per-subject content identity in the inspection
handoff. FR-S3: add the new design/record inventory entries, refresh changed
navigation content digests, and regenerate the current-design catalog.

Claude and Codex also reconciled the initial advice: recommendation must not
inherit doctor's no-analysis mode or its resource budget; only items claiming
Control evidence must resolve Control references, while Map may have its own
labeled observations; metric honesty is a future reporting constraint, not a
blanket ban on deterministic metrics. A real design supplement is needed in
addition to the source map. The first review records Claude's agreement with
these corrections explicitly.

## Validation boundary

The [before summary](d369-before-summary.json) records the existing D-369
checker failure: root `README.md` already differed from its preserved
publication images at task opening. It is not modified here. The recording
requires the same failure set afterward, preserved preview/readiness bytes,
valid links including fragments, correct inventory content hashes, and a clean
patch-whitespace check. Passing documentation checks does not qualify product
behavior. The historical document-custody script exits zero even on FAIL and
is not used as evidence of success.

## Adoption and recording

[D-370](../COORDINATOR-DECISIONS.md#d-370--fallow-informed-product-design)
records adoption of the exact [v2 act](D-370-design-adoption.v2.md) and corrected
subject. [Codex assent](codex-assent.v1.json) is separate from Claude's
independent review. The coordinator heading and this record supply the exact
link targets required by the act. Only this record's final content digest is
refreshed in the two inventories, as the reviewed inventory delta permits.

[Validation](validation.v1.json) records the fragment-aware links, subject and
preservation hashes, inventory-delta checks, catalog parity, and unchanged
D-369 failure set. The [retained D-369 report](d369-after-report.json) is a full
checker report, not a claim that its pre-existing README failure passed.
[Recording receipt](recording-receipt.v1.json) gives the actual final inventory
whole-file hashes; the inventory delta's review-time hashes remain historical.

No row grade, future capability qualification, or implementation authorization
is granted. Nonblocking peer notes remain in the final verdict and author
assent, including the explicit, non-exhaustive inbound-reference samples that
omit the new catalog backlink. Those counts were retained exactly as reviewed.

## Fixed evidence digests


- [subject.v1.json](subject.v1.json): `cfd761d14324bc8a213777e9b9be5b73a9d34a1cae4b5ce24875be943643557b`
- [subject.v2.json](subject.v2.json): `c4f71969371e2dd3bc7d235065d387f3c16084926e35c67c36d17378fedbb5ba`
- [claude-initial.md](claude-initial.md): `5c79df44ed884c3cd250e4a92a5ab15628fd4e72eafab27f4f54e84dc2a94bd9`
- [claude-review.v1.md](claude-review.v1.md): `04e3d29e4d193ffe41f349e842a026f0de2e702adfbab3eb67f8b9a786ae5fd4`
- [claude-review.v2.md](claude-review.v2.md): `6bb359bfb87201c10dcb6476604fdf334a41ef143b0c7cd9f0c8104b7a48edbb`
- [D-370-design-adoption.v2.md](D-370-design-adoption.v2.md): `6655baaa89cb4f308fae97777816cf492fa45fb240cc7014ec94719b578405c3`
- [codex-assent.v1.json](codex-assent.v1.json): `42af4f9bc34a4581710e39753c6899cb93e6d7d710929cd5f4046709988b3f76`
