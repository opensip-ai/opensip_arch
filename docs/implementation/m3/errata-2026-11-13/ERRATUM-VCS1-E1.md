# Erratum VCS1-E1: what a stored Git `dirty` value means after M3 (author draft, 2026-11-13)

Status: **PROPOSED.** It implements lead decision LD-DEC-7 item 8 (`LC/decisions/LD-DEC-7-durable-shapes/DECISION.md`,
`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), answering the red team's finding 6 (`REDTEAM.md`).
It is **additive**: one sentence and one disclosure; no accepted byte is edited.

Subject: the accepted contract passage VCS-1 r1, `docs/implementation/m3/snapshot-plan-c/vcs-1-r1/CONTRACT.md` (1,444 bytes,
sha256 `62e59de74e7e20512f972696ca7258872a5406fcbeb7d0731ad622497aedcf41`), which its record
`vcs-1-r1/successor.json` (2,849 bytes, sha256 `dcca6976…`) appends to identity-and-evidence line 546 as a passage override.

**Which record form applies.** VCS-1 is a lock input: the product's `design-lock.json` (main `1bd328f3`) binds it as a
`contractSuccessors` entry, record at `:8852`, subject manifest `vcs-1-r1-subject.json` at `:8857`, review
`reviews/grok-vcs1-r1/review.json`, assent `vcs-1-r1-unit.json` at `:8867`. So, unlike I1-E1 (whose texts were in no
lock entry), this correction needs a **contract successor** in the NE-4-4-DETAIL-UNITS-r1 form
(`../errata-2026-11-11/ne-4-4-detail-r1/`): a record, a subject manifest, a review, an assent and one new lock entry.
This file is its text. The record is owed, not generated here (VCS1-E1.6).

## VCS1-E1.1 The accepted sentence and what it leaves open

`vcs-1-r1/CONTRACT.md:3`: "**M3 meaning of `dirty` (VCS-1, accepted M3-C item4).** At M3, `dirty` means that cleanliness
has not been established. For a Git observation the host reads no Git object and cannot compare the working tree with
HEAD's tree, so it records `dirty: true` …"

`vcs-1-r1/CONTRACT.md:5`: "The same Git `dirty` meaning applies to each admitted D15 member's schema-3 observation …
Schema-2 and schema-3 fields, admission, member order, canonical bytes, inventory-digest meaning and historical retained
observations are unchanged. This passage changes no observed flag or retained identity by reinterpretation. It publishes
no Git object reader, per-path change set, new correspondence mapping, new record member, schema version …"

The meaning is scoped "At M3". What a stored `dirty: true` means once a Git reader exists is not stated in VCS-1, MC8
(`snapshot-plan-c/PROPOSAL-r8.md:320-331`) or IE (`identity-and-evidence.md:542-546`). Not located elsewhere (LD-DEC-7
panel A and C, `BRIEF.md:111`).

## VCS1-E1.2 The schema versions, from the schema source

- **Schema 2.** `vcs-observation-v2` (product `schemas/sources/identity-v3.schema.json:2701`; the design copy
  `docs/coop/design-corrections/foundation/identity-schemas.v3.json:2689`, `schemaVersion: {const: 2}`): `kind` is one of
  `none`, `git`, `hg`, `svn`, `jj`; `dirty` is a boolean.
- **Schema 3.** `vcs-observation-v3` (product `identity-v3.schema.json:2749`; contract successor B-S2,
  `config-discovery-b/b-s2/PASSAGES.md:31`): the top level is fixed `kind: "none"`, `commitId: null`, `dirty: false`
  (`const`). The Git value lives only in `members[]`, each a `vcs-member-observation` (`:2796`) with `kind` fixed to `git`.
- `#/$defs/vcs-observation` (`:2690`) is `oneOf [v2, v3]`. No other version exists.
- What the product writes (`crates/host/src/snapshot_seal.rs:329-336`): schema 2 `kind: none` with `dirty: false`;
  schema 2 `kind: git` with `dirty: true`; schema 3 with the fixed top level and each member `kind: git`, `dirty: true`.
  `hg`, `svn` and `jj` are never written: every other layout is refused as `vcs-unsupported` (MC8 `PROPOSAL-r8.md:321`).

So "`kind: git` in schema 2 and 3" means exactly two places: a schema-2 record whose `kind` is `git`, and each
`members[]` row of a schema-3 record.

## VCS1-E1.3 The amendment

An insertion after `vcs-1-r1/CONTRACT.md:5`, as a new paragraph of the passage:

> **After M3 (erratum VCS1-E1).** In a `vcs-observation` record of schema version 2 whose `kind` is `git`, and in every `members` row of a schema-version-3 record, the stored `dirty` value means "cleanliness not established", whatever value it holds and whenever the record is read, permanently. A producer of those two versions writes `dirty: true` for Git. A Git reader that establishes cleanliness emits a new `vcs-observation` schema version, and only that version can carry an established clean or dirty state. This sentence does not touch `kind: none` (schema 2's `NoRepository` record, and schema 3's fixed top level), whose `dirty: false` keeps its meaning. Disclosed: a Run whose snapshot holds a schema-2 or schema-3 observation can never satisfy a `vcs-revision` correspondence that requires a clean commit (NE:2722-2728), so it can never map a revision import, even after the Git reader exists.

## VCS1-E1.4 The red team's four attacks, checked

| Attack (`REDTEAM.md` finding 6) | How the sentence answers it |
|---|---|
| 1. VCS-1 scopes the meaning "At M3", not by schema version; re-keying it surprises a reader of VCS-1. | The sentence is added to VCS-1 itself and says it keys on the schema version, "whenever the record is read". VCS-1:3's M3 meaning is unchanged; the sentence states what it already implies for later readers (VCS-1:5: "This passage changes no observed flag or retained identity by reinterpretation"; this sentence keeps to that and reinterprets nothing). The schema version is inside the hashed record (`schemaVersion` is a required member), so a reader cannot miss it. |
| 2. "dirty in schema 2 and 3 means not established" misreads `kind: none, dirty: false`. | Scoped to schema-2 `kind: git` and schema-3 `members` rows. `kind: none` is named as untouched. |
| 3. A new version changes IDS's single def, which `snapshot.vcsDigest` selects by `#/$defs/vcs-observation`: bytes under a pinned schema id, so the cost is deferred, not avoided. | True, and not avoided here. The sentence only says the reader must use a new version. That version's schema change (a third `oneOf` arm, as B-S2 added the second; `b-s2/README.md:40`) and its pin and lock work belong to the Git reader's unit. |
| 4. Every pre-reader Run can never map a `vcs-revision` import; disclose it. | Disclosed in the sentence's last line. |

Also checked: the sentence stays fail-closed for current readers. Workflows' `StalenessRule` maps commit-equal-dirty to
`unverifiable` (`workflows-and-surfaces.md:511`), and IE's staleness function uses "both dirty flags"
(`identity-and-evidence.md:1839`). NE:2726 maps `vcs-revision` only when "its commit is clean".

The producer sentence ("A producer of those two versions writes `dirty: true` for Git") is a producer rule implied by
LD-DEC-7 item 8: no value of those versions can mean established. It is stated in the paragraph so that no later
producer of schema 2 or 3 writes `false` for Git.

## VCS1-E1.5 What this does not change

- No schema, no record member, no canonical bytes, no digest, no `snapshot2`, Plan or Run id. No product code
  (`snapshot_seal.rs` already writes `true` for Git).
- `hg`, `svn` and `jj` schema-2 records: not written by any host and not covered. If one is ever admitted, its `dirty`
  meaning needs its own text.
- B-S2's "a schema-3 observation establishes no `vcs-revision` source correspondence" (`b-s2/PASSAGES.md:31`) stands.

## VCS1-E1.6 Review and binding owed

- **Review: two independent reviewers** (LD-DEC-7 item 8 is a durable on-disk meaning: OD-PACE-1 rule 4, `OD-PACE-1.md:30-31`, which governs over
  OD-REVIEW-1 by `OD-PACE-1.md:67-68`).
- **Binding owed (not generated):** a contract successor carrying this paragraph, its subject manifest, the review, the
  unit assent and one `contractSuccessors` entry in the product's `design-lock.json`. Two forms are possible, and the
  choice is the binder's:
  - a replacement VCS-1 r2 record whose one override of `identity-and-evidence.md:546` restates VCS-1's text with this
    paragraph appended, naming VCS-1 r1 as its `previousCandidate`. That is the form
    `m2/predicate-matching-reference-selection-v2/successor.json` uses for the line its v1 overrode (`:1272`);
  - or a second successor on the same line. Of the 558 `successor.json` files under `docs/implementation/` (subject
    copies left out), only VCS-1 overrides `identity-and-evidence.md:546`. I did not establish whether the verifier
    admits two bound successors on one selector line, so I did not choose this form.
  Not generated, because the form is not settled and the text may change in review.
