# HSR-1: historical schema readers (identity contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit. It edits only arch, and changes no product file, code, class, exit code, route or public code. It needs Grok's `ACCEPT-DESIGN-UNIT`, with a review that lists `supersededPassages`, and the lead's root assent before it can be bound in the product's `design-lock.json`. It binds only after law HSR r1 is accepted.

**What it is.** Law HSR r1 (`../PROPOSAL.md`, item 9) names successor **HSR-1**: the identity-owner text that lets a retained record be admitted against the exactly selected earlier bytes of its schema document, by exact digest, from a closed table. It is the lead's decision B on E2s's stop (overnight log, "E2s stopped before review, correctly"). Unit HSR-a implements it, and E2s lands after HSR-a (law items 13 to 15).

**Law standing.** The law is in review with Grok in the same request (`reviews/grok-hsr-r1`). HSR-1 carries the law's items 3 to 8 and nothing else. If that review changes those items, HSR-1 is rebuilt to match.

**Product.** Main `43ea32a` (X3c-3), read only. Its lock (520,396 bytes, `97097b51…`) and `tools/verify_design.py` (43,946 bytes, `7b313de6…`) are byte-identical to `b7b87b7`'s, the base E2s stopped on. The lock has 101 contract successors and 5 contract passage supersessions. I1-L is bound at lock index 77, SYN-1 at 89 and SYN-1F at 90. The record is built and checked against `43ea32a`'s lock, read with `git show`.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **HSR** | `docs/implementation/m3/syntax-e/hsr/PROPOSAL.md`, law HSR r1, in review in the same request | pinned in the request |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes) | `c82404f3…` |
| **IDS** | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`, SYN-1F's complete copy, the selected identity schema bundle (200,510 bytes) | `73645b76…` |
| **I1L** | `docs/implementation/m3/preview-pack-i1/i1-l/successor.json`, bound (35,443 bytes) | `9c490137…` |
| **I1** | `docs/implementation/m3/preview-pack-i1/PROPOSAL-r3.md`, M3-I1 r3, accepted by CODEX2 | `204f8ee8…` |
| **SYN1 / SYN1F** | `docs/implementation/m3/syntax-e/syn-1/successor.json` (28,228 bytes) and `syn-1f/successor.json` (9,697 bytes), bound at `682991f` and `218465f` | `c1309a7c…`, `736f2fed…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes) | `83b99783…` |
| **VD2** | `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, the accepted law of contract passage supersession | `2e4f70b4…` |
| **VD** | `tools/verify_design.py` at product `43ea32a` | `7b313de6…` |

The precedents for the form are SD-7 and SD-8 (`supervisor-d/`), REG v3 (`m2/project-registry-owner-selection-v3/`), CRC-2 and ENUM-1 (`snapshot-plan-c/`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the supersession and the five overrides, each with its exact `before`, its `after` and the word-level changes, and the table's verification |
| `successor.json` | the record: two parents, five `passageOverrides`, one `passageSupersessions` entry, five candidates |
| `evidence/build_hsr_1.py` | builds the generated files, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_hsr_1.py` | read-only, independent checks |
| `evidence/verify_scratch.py` | the real VD in a throwaway worktree, with the scratch review and assent served from memory, plus VD2's refusals and the extension route |
| `../hsr-1-subject.json` | the subject manifest (generated) |
| `../hsr-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/grok-hsr-r1/hsr-1/review.json`; not part of the subject |

## What changes

Six entries. `PASSAGES.md` has the full texts.

| # | Kind | Parent | Selector | Change |
|---|---|---|---|---|
| 1 | **supersession** of I1-L's override | IE | line 214 | I1-L's exception paragraph to the major rule, kept verbatim. Before its last sentence, "Every other schema or domain change keeps this rule.", a **second reviewed exception** is added: SYN-1 and SYN-1F's single additive `source-parse-error`, under the existing majors and without migration. Unlike I1's member, it changes the bytes of two documents that retained records name by digest, so their earlier bytes stay readable as historical schema readers. The last sentence stays, and one more sentence states the extension rule. |
| 2 | override | IE | line 662 | The payload registry's `payloadSchemaDigest` bullet: the bytes are the document's selected current bytes or, for a retained record only, one historical reader's bytes. |
| 3 | override | IE | line 678 | `view.schemaDigests`: the same rule for a retained view. `SCHEMA_DOCUMENT_UNREGISTERED` still refuses anything else. |
| 4 | override | IE | line 808 | The payload registry section's last line, followed by a new subsection, **"Historical schema readers (contract successor HSR-1)"**: the closed table (H1, H2), minting, retained records, one reader per digest, identity, mixed stores and Runs, verification, and extension. |
| 5 | override | IDS | `/x-opensip-payload-registry/law/payloadSchemaDigest` | The registry's normative law string gains the same rule, the minting rule and the resolution order. |
| 6 | override | IDS | `/x-opensip-evaluator-profile/majorLaw` | One sentence is appended beside I1's: the second exception keeps every identifier major, and earlier digests are read by HSR-1's readers. |

Nothing else changes. Every schema shape, enum, H domain and recipe, every registry, generated file, product copy and inventory keeps its bytes and meaning. The check script shows that the two IDS strings are the only change to that document.

## The table

| Row | Document | Historical bytes | Accepted architecture copy | Retired by |
|---|---|---|---|---|
| H1 | `native/native-evidence.schemas.v2.json` | 280,357 bytes, `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773` | `docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json` (selected through source-selection-v3) | SYN-1, whose product copy is 280,738 bytes, `93a39da8…` |
| H2 | `foundation/enumeration-plan.schema.v1.json` | 19,975 bytes, `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c` | `docs/implementation/m2/admission-runtime-selection-v1/schemas/sources/enumeration-plan-v1.schema.json` | SYN-1F, whose product copy is 20,005 bytes, `cc29483f…` |

- **Why exactly these two.** A retained record names a schema document by digest only through a payload-registry document: `payloadSchemaDigest`, a parameter's `schemaDigest`, `view.schemaDigests` and the `schema` proof-input-ref (IE:661-678). E2s changes five product schema sources. Two of them are payload-registry documents. The other three (execution inputs, subject inventory, identity schemas) are not, so no record carries their digest and they need no row. The check script proves both halves on the text, and against the product corpora at `43ea32a`: each row's digest occurs in the twelve corpora, and no digest of the other three occurs in any.
- **Why these copies.** Each is the copy the product's base source maps name for that document (`schemas/source-map.json` and `schemas/admission-source-map.json` for native-v2, `schemas/admission-source-map.json` for the enumeration plan), and each is in the lock's accepted set with exactly the row's digest. The foundation design copy of the enumeration plan (`docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json`) holds the same bytes; the table names the copy the product read.
- **Reference closure.** Neither document references another document, so each reader's closure is its own bytes.

## Why this form: the lock, selector by selector

`build_hsr_1.py` reads the lock at `43ea32a` and finds each key's current meaning.
- **IE:214 is taken by I1-L.** It carries I1-L's bound override, and no later record supersedes it. A second override refuses ("conflicting contract passage overrides", VD:409-411), and `verify_scratch.py`'s probe shows it. Law VD2 admits a **contract passage supersession** instead: the entry names I1-L's record by exact pin, with the same parent and selector, and its `before` is I1-L's `after`. The review must list `supersededPassages`, equal to the record's `supersedes` list.
- **IE:662, IE:678 and IE:808 are free.** No bound record overrides them, so each takes a plain override whose `before` is the raw line.
- **The selected IDS is SYN-1F's copy.** It is the last complete identity-schema copy in the chain. CRC-2 overrides two of its pointers. No bound record overrides `/x-opensip-payload-registry/law/payloadSchemaDigest` or `/x-opensip-evaluator-profile/majorLaw` there, so both take plain overrides.
- **Untouched on purpose:**
  - **NE §4 step 6** (NE:1939-1943) and **NE §7.2** (NE:2703). Both state the minting rule and the digest preimage, and both stay true: minting names the current bytes, and a historical reader's digest is still the raw SHA-256 of a whole document. The new IE subsection names step 6 as a minting boundary.
  - **WS:490.** It states the same digest preimage for the workflow import registry.
  - **IE:641-643.** "Schema digests cover the exact complete registered schema document bytes" stays true of a reader's bytes, and the reader's references resolve within its own bytes.
  - **IDS's `registered-schema-document` strings** (`view.schemaDigests` and `byDomain/schema`). They name "a schema document on the closed x-opensip-payload-registry list", and override 5 says which bytes of a listed document count.
  - **Every product copy**, including the product identity schema source, as CRC-1 LD-7 and CRC-2 LD-4 decided: annotation prose that no code dispatches on.
  - **The admission registry and `verify_design`.** The admission registry admits one source per schema `$id`, by design ("Historical native and policy documents with the same schema ID are refused as current sources", `m2/admission-runtime-selection-v1/README.md`:9). Historical readers are not admission sources. HSR-a compiles them separately (law item 13).

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them. The law's LD-H1 to LD-H12 are the substance; these are the form.

**LD-1. IE:214 is superseded in VD2's form, and I1-L's text survives verbatim.**
- **Rejected: a raw override of IE:214.** VD refuses it as conflicting (probe below).
- **Rejected: a new paragraph on a free line.** I1-L's "Every other schema or domain change keeps this rule" would stay in force beside a second exception that contradicts it.
- **Rejected: a complete IE copy.** It would move the selected IE for every successor in flight.

**LD-2. The reader table lives in IE text, at the end of the payload registry section (IE:808).**
- **Rejected: a new IDS member.** A JSON Pointer override changes one string and cannot add a member, so it would need a complete IDS copy, which forks the selected text that CRC-2 and SYN-1F carry.
- **Rejected: a standalone registry document with a `verify_design` extension.** It adds a second authority, a VD change with its own law and an F8c-style re-pin, and buys nothing: the table's digests already bind the bytes.
- **Rejected: rows in the admission registry.** VD refuses a second source with the same `$id`, by design.
- **Why IE:808.** The subsection follows the payload registry that names every carried document, and later extensions supersede one line.

**LD-3. The IDS law string and the major law gain the rule by plain overrides on SYN-1F's copy.** The registry law is the normative machine-readable statement IE names, and the major law already records I1's exception. Leaving either unchanged would leave the selected IDS silent where IE speaks.
- **Rejected:** overriding I1-L's no-longer-selected IDS copy, which nobody reads.

**LD-4. No vector, no new code, no product copy change.** Historical readers refuse through existing refusals. Product copies are annotation prose.

**LD-5. Binding.** After `ACCEPT-DESIGN-UNIT`, and only once law HSR r1 is accepted, the lead appends HSR-1's entry in a binding-only product commit, before HSR-a.
- **Rejected:** binding before the law is accepted; binding inside HSR-a's commit, which mixes review subjects.

## Cross-law items

1. **Later IDS copies.** VD does not enforce which copy is selected. Any later complete identity-schema copy must carry HSR-1's two strings in place, as SYN-1F's carries CRC-1's and CRC-2 overrides it. Review must hold this.
2. **Later table rows.** Each successor that changes the selected bytes of a payload-registry document supersedes HSR-1's IE:808 override and adds exactly one row per retired digest (law item 8). `verify_scratch.py` shows that route binds.
3. **E2s and HSR-a.** Law items 13 to 15.

## Points for the reviewer

- **R1 (faithfulness).** Is HSR-1 exactly law HSR r1's items 3 to 8, neither wider nor narrower?
- **R2 (form).** Is the supersession well formed under VD2, and are SYN-1F's copy and plain overrides the right IDS target (LD-1 to LD-3)?
- **R3 (I1-L survives).** Does every sentence of I1-L's text survive, with only the second exception and the extension sentence added?
- **R4 (the table).** Are H1 and H2 the right rows, with the right bytes and copies, and is it right that the three other documents E2s changes get none?
- **R5 (binding).** Does the record bind after main's chain with your review's `supersededPassages`, and does any selected passage still conflict?

## Binding

HSR-1 binds on VD at main `43ea32a`, on top of all 101 contract successors. After `ACCEPT-DESIGN-UNIT` and the law's acceptance:
1. copy the review into `docs/implementation/m3/reviews/grok-hsr-r1/hsr-1/review.json`;
2. complete `hsr-1-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append the four pins to the product lock;
4. run plain VD.

The review must carry this `supersededPassages` list, exactly:

```json
[{"record": {"path": "docs/implementation/m3/preview-pack-i1/i1-l/successor.json", "bytes": 35443, "sha256": "9c490137998222627a011eec72af8c0ed3bb568e3085725fdf11b8610d42c6a1"}, "parent": {"path": "docs/v2/contracts/product-v1/identity-and-evidence.md", "bytes": 135448, "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"}, "selector": {"line": 214}}]
```

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo or a test.
- **`evidence/build_hsr_1.py`**, then `--check`, which reports identical bytes for every generated file, the unit draft included.
- **`evidence/check_hsr_1.py`** passes at `43ea32a`. It checks the parents, the supersession's target and current meaning, I1-L's sentences in order, each override's key and raw text, the table against accepted bytes, carriage in the corpora, the rule's clauses, the absence of new em dashes, and this README's naming of every passage and both digests.
- **`evidence/verify_scratch.py`** in a throwaway detached worktree of product main `43ea32a` (`/Users/sb/code/opensip-ai/opensip-hsr-check`), with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`. Its output is pinned in the review request (`reviews/grok-hsr-r1/evidence/local-binding-check.json`), and the worktree was then removed.
  - **Baseline:** the literal CLI on main's lock passes, with 101 contract successors and 5 contract passage supersessions. The overlay run agrees.
  - **With HSR-1 appended:** PASS, with the worktree as implementation and without it. There are 102 contract successors and 6 contract passage supersessions. The inventory chain, inheritance and supersessions, generation and admission sources, and verified inputs equal the baseline's.
  - **Refusals:** a review without `supersededPassages` ("contract passage supersession is not listed by its review"); a review with `[]` ("contract review superseded passages differ from the record"); HSR-1 with a raw override of IE:214 ("conflicting contract passage overrides"); after HSR-1, a second supersession of I1-L's IE:214 ("double supersession: the named passage is not the current meaning"); after HSR-1, a different override of IE:808 or of the payload-registry law pointer ("conflicting contract passage overrides").
  - **The extension route:** after HSR-1, a probe successor that supersedes HSR-1's IE:808 override and adds one row binds: PASS, 103 contract successors.
  - **The literal CLI on the appended lock** stops at the SCRATCH placeholder, as for earlier units. The overlay run is the binding result.

## Not changed, and noted

- **No refusal code, class, exit or route is added.**
- **No product file is touched.** No code, test or build was run, and the reference checkers were not run.
- **No identity moves.** HSR-1 changes which bytes read a retained record. It changes no recipe, domain, prefix or major.

## Owner flag

Every later change to a payload-registry document under its existing major now carries a row: the product keeps the retired bytes compiled in, by digest, for as long as any retained record may name them. Today that is about 300 KB for H1 and H2.
