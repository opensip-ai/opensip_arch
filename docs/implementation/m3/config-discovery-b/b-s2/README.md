# B-S2 — contract successor S4: `vcs-observation` schema 3

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-B r2** (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, GROK2, `92e65825…`) names successor **S4** (MB:775): "IE `vcs-observation` schema 3 — per-member VCS rows; version-2 bytes unchanged for single-root projects", implemented by C1. MB item 22 gives its content (MB:685-689), and M3-C item 4 consumes it (MC:281-285; C1b "lands S4 after B-S2 is accepted"). This unit is design unit **B-S2** (MB:842; `M3-PLAN.md:211`).

**Product.** Main at `e093e90` (F8b's binding, 77 contract successors), read only. The record is built and checked against it.

## Short names

MB is M3-B r2. MC is M3-C r6, accepted by CODEX2 (`8274bca1…`); the live file is cited, and r6 did not change item 4. The other short names:
- **IE** `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes, `c82404f3…`), the only parent;
- **IDS** `docs/coop/design-corrections/foundation/identity-schemas.v3.json`;
- **the product copy** `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json`, which is byte-identical to the product's `schemas/sources/identity-v3.schema.json` (`311c1feb…`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: both overrides, with the exact `before` and candidate `after` |
| `successor.json` | the contract successor record (2 passage overrides on IE) |
| `schemas/identity-schemas.v3.b-s2-additions.json` | generated: the IDS fragment (`vcs-observation` as schema 2 or 3; `vcs-observation-v2`, `-v3`, `vcs-member-observation`) |
| `evidence/build_b_s2.py`, `check_b_s2.py`, `verify_scratch.py` | build, read-only content checks with byte vectors, real verify_design with a synthetic review and assent |
| `../b-s2-subject.json` | the subject manifest (generated) |
| `../b-s2-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What it changes

**IE §3.**
- IE:542 now says that B-S2 adds schema 3 for a D15 workspace.
- A new paragraph replaces the blank line IE:547, between the `vcsDigest` paragraph and "What `sourceInventory` contains". The blank line on each side is kept. The paragraph states:
  - **The record.** A project with at least one admitted D15 member hashes `{schemaVersion: 3, kind: "none", commitId: null, dirty: false, sourceInventoryDigest, members}`.
  - **The top level** is the workspace root's own observation. It is always `kind: none` under W2. `sourceInventoryDigest` keeps its meaning, the whole inventory.
  - **`members`.** 1 to 64 rows `{path, kind: "git", commitId, dirty}`, strictly ascending by `path` (a logical path relative to the project root). `commitId` is 40 lowercase hex. A member's `commitId` and `dirty` follow a single repository's rules.
  - **Schema 3 exactly when the project has an admitted member.** Otherwise schema 2 and its exact bytes, so no existing `snapshot2` changes.
  - **No `vcs-revision` correspondence** through a schema-3 observation.
  - **Unchanged.** The record name and the snapshot's `vcsDigest` selector.

**IDS (the fragment).** `#/$defs/vcs-observation` becomes `oneOf [vcs-observation-v2, vcs-observation-v3]`. `vcs-observation-v2` is IDS's current `vcs-observation`, copied unchanged and asserted equal to both IDS copies. `vcs-observation-v3` and `vcs-member-observation` are added. Nothing else in IDS changes. The same merge applies to the product copy.

**Byte vectors** (`check_b_s2.py`; identity §3 canonical JSON, IE:122-130):

| Sample (`sourceInventoryDigest` = SHA-256 of `[]`, `4f53cda1…`) | Canonical bytes | Canonical SHA-256 |
|---|---:|---|
| schema 2, `kind: none` | 154 | `fd32de2c047f0f64404b37dd3a66999c43af0952a1fe8773f100509489686209` |
| schema 2, `kind: git`, `commitId` `a`×40, `dirty: true` | 190 | `b7a78032ceacb5872b1306e904cd489b8946aac2171f75671de9ea5343a877c0` |
| schema 3, members `serde` (`0123…4567`) and `serde-json` (`fedc…ba98`), both `dirty: true` | 365 | `b6e0334aef83c204af82c1a083989252281fded6dce58a9005d8c69bc9f8f01f` |

The schema-2 samples admit under both the accepted `vcs-observation` and the new `oneOf`, with identical canonical bytes. That is the "version-2 bytes unchanged" property.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects.

**LD-1. Replace in place under the same record name.** `#/$defs/vcs-observation` admits exactly schema 2 or schema 3.
- Product Run closure reads the record by name: `crates/evaluator/src/run_links.rs:364` and `import_joins.rs:205` call `rd.record(…, "vcs-observation")`. The generator options name `#/$defs/vcs-observation` (`tools/contracts/options.json:758`), and the snapshot's `vcsDigest` selector names it too.
- Keeping the name keeps every consumer. `run_links.rs:370-373`'s `VCS_KIND_JOIN` (kind `none` if and only if `commitId` is null) holds at a schema-3 top level as written.
- **Rejected:** a new record name plus a changed `vcsDigest` selector. That changes the snapshot's digest annotation and every consumer to say the same thing.

**LD-2. The schema-3 top level is fixed: `kind: none`, `commitId: null`, `dirty: false`.**
- W2 is a hard precondition of membership (MB item 19; X2 r9 item 6b). A schema-3 record with any other top level is malformed, not a state. `dirty: false` is MC item 4's value for `NoRepository`.
- **Rejected:** a free top level, which would admit a self-contradictory record.

**LD-3. A member `commitId` is exactly 40 lowercase hex digits.**
- X2 refuses `extensions.*`, so `extensions.objectformat=sha256` is refused too, and only SHA-1 object IDs exist. MC item 4 resolves HEAD to a hash.
- **Rejected:** schema 2's `Text`, which admits non-commit strings for a field with one lawful shape. Schema 2 is unchanged.

**LD-4. Members are 1 to 64, `kind` const `git`, `path` order.**
- `path` is IDS `LogicalPath`, relative to the project root.
- The bounds are MB item 19's. The order is IE:137's `path` order. `git` is the only member layout (MB M2).
- An empty `members` is not schema 3: such a project uses schema 2.

**LD-5. Schema 3 exactly when there is at least one admitted member.**
- A workspace root whose declared candidates were all excluded (B-S1's reader branch) has no member, so it records schema 2 with `kind: none`. That is the record any non-repository root has today.
- The choice is a host observation, like the custody walk (IE:588-592). Replay cannot see security's member decision, because the boundary inventory is not Plan-retained (NE:813-815).
- **Rejected:** schema 3 with an empty `members` for every non-repository root, which changes existing schema-2 bytes for single-root projects.

**LD-6. No `vcs-revision` correspondence through schema 3 (fail closed).**
- IE:1835-1839's staleness function and NE:2722-2728 read a revision and dirty flag from the snapshot's observation. Schema 3's top level names none.
- A per-member correspondence, saying which member's revision an import maps to, needs its own successor. Imports of runtime, test and history evidence are M5 (MC item 4).
- **Rejected:** reading the first member's revision, which is a silent choice.

**LD-7. The line allocation with VCS-1.**
- MC's successor **VCS-1** (MC:1046) also targets IE:542-546, for item 4's meaning of `dirty`.
- B-S2 overrides only IE:542, the record and schema clause, and the blank IE:547. It leaves IE:543-546, where `dirty` is defined, to VCS-1. Otherwise the second of two overrides of one line would refuse as a conflict (`tools/verify_design.py:381-383`).
- If VCS-1 needs IE:542 as well, it must restate B-S2's `after` there as its own `before`, through VD2's explicit supersession.
- **Rejected:**
  - **Folding VCS-1 into B-S2.** It would carry MC's open reviewer question V2 (MC:1211) into this unit.
  - **Overriding IE:546.** VCS-1's natural anchor.

**LD-8. `sourceInventoryDigest` stays top-level and whole.** One digest names the one inventory (IE:639-641). Per-member inventory digests are not added, because nothing consumes them.

## Points for the reviewer

- **R1 (LD-1).** Is replacing `#/$defs/vcs-observation` in place by a schema-2-or-3 `oneOf`, under the same name and selector, sound? Is `vcs-observation-v2` provably the accepted record?
- **R2 (LD-2 to LD-5).** Is the schema-3 shape exactly MB item 22's and MC item 4's? Is anything in it unbounded or open?
- **R3 (LD-6).** Is failing closed on `vcs-revision` correspondence right for M3?
- **R4 (LD-7).** Does the line allocation leave VCS-1 a lawful, non-conflicting place?

## Conflicts and reconciliations with accepted laws

- **M3-B r2:** none. Schema 3's shape is MB item 22's, and single-root bytes are unchanged (MB:689, MB:705).
- **M3-C r6 (accepted):** item 4 consumes this shape. Its "each member's `commitId` and `dirty` follow the two bullets above" is kept through "the same rules as a single repository's". The line allocation with VCS-1 is LD-7.
- **X2 r9:** consistent. Member Git objects beyond `.git`, `config` and `index` are admitted only by C1's VCS-observation law, for every repository alike (X2 r9 item 1). B-S2 defines the record, not the reads.
- **X12 r4:** not touched.
- **B-S1:** none. B-S1 overrides IE:552 only.

No owner question is raised. OQ-1 is unaffected.

## Findings for other owners

- **BS2-F1 (M5).** A per-member `vcs-revision` source correspondence for schema-3 snapshots (LD-6).
- **BS2-F2 (C1b).** Materialize the fragment into `schemas/sources/identity-v3.schema.json`, regenerate `crates/contracts/src/generated/identity.rs`, and keep `VCS_KIND_JOIN` at the top level. Add member joins: `kind: git` with a non-null `commitId`, which the schema already enforces. Pin `check_b_s2.py`'s vectors.
- **BS2-F3 (C1b and I1-a, ordering).** The I1-L draft (`docs/implementation/m3/preview-pack-i1/i1-l/`) carries complete successor copies of IDS and of its product copy, with one operation member appended to the predicate enum. B-S2's fragment is a merge rule, not a copy, so the two do not conflict. Whichever lands second applies on top of the other. If I1-L is selected first, C1b applies B-S2's fragment to I1-L's product copy, whose `vcs-observation` is unchanged, so the `vcs-observation-v2` equality still holds. `check_b_s2.py` pins IDS and its m1 copy, so a later recheck there should name I1-L's copies.

## Binding

After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok2-b-s2-r1/review.json`;
- complete `b-s2-unit.json`;
- append the four pins to the product lock;
- run plain verify_design.

B-S2 has overrides only, no supersession, so it binds on the verify_design at main `e093e90` with no prerequisite. `verify_scratch.py` shows that with in-memory `SCRATCH-B-S2/` placeholders, at `--rev e093e90` and on the main checkout: the lock goes from 77 to 78 contract successors, and on the checkout 40 generation sources are verified.

## Controls owed by C1b

- A single-root `snapshot2` is byte-identical before and after S4: no repository, one repository, nested repositories.
- A two-member and a 64-member workspace record schema 3, with members in `path` order and each member's HEAD resolved through a loose ref or `packed-refs`.
- A workspace whose declared candidates were all excluded records schema 2, `kind: none`.
- The negatives in `check_b_s2.py` refuse at snapshot admission and at Run closure.

## Not claimed

- No product code, test or build was run. Only the evidence scripts ran, read-only.
- No law is amended. No VCS read is added: the reads stay MC item 4's.
- The 64-member bound is MB's, and provisional.
