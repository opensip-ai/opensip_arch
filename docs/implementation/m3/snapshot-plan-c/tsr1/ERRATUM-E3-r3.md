# TSR-1 erratum E3: a remedy that fits the unchanged public record (R-10.3), r3 (coordinator, 2026-10-30)

**Status: PROPOSED.** This text is under R3 different-vendor review (`REQUEST-E3-r3.md`). It takes effect only when
the coordinator records its adoption, owner-delegated under OD-AUTO-1, in a separate receipt
(`ADOPTION-E3.md`), which pins this file's sha256. This file is never edited after review.

**r3 answers R3 review r2** (`REVIEW-E3-r2.md`, E3-R2-RF-1): §4 now binds this exact file, and the receipt pins its
sha256; C30c is added to C2b-1b's execution list. Nothing else changes. r1 and r2 are kept unchanged as review history.

**r2 answered R3 review r1** (`REVIEW-E3-r1.md`):
- **RF-1:** the clause no longer promises a visible member, because `subjectBoundLaw` can elide it.
- **NB-1:** C30b's boundary checks are isolated.
- **New:** a long-path control.

r1 is kept unchanged.

**What it amends:** the adopted TSR-1, `TSR-1-r4.md` (sha256 `be654c41dcc310206fca27aa3feaddd9c1d5d9c1f3eeb7f8652dd0026c4e99f3`;
receipt `ADOPTION-TSR-1.md`). It is independent of the deferred erratum S2 (LD-Q-17). E3 is on the path: Part R ships
with C2b-1b, which the first Run needs (`../coordinator/PATH.md` row 3).

**Why:** C2b-1b escalation X-C2B1B-4 (`../c2b1b/ESCALATION-REMEDY-r1.md`).
- **The two rules that cannot both hold:**
  - R-10.3 requires one exact remedy: S10b's text (`REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED`, 646 bytes), followed by a
    clause of 1,545 characters. That is 2,191 characters in total;
  - R-10.3 also says "The public record, the D9 row and the detail vocabulary are unchanged". The public carrier
    `DomainDetail.remedy` is `BoundedText`, `maxLength` 1024, in common-v1, common-v3 and common-v4.
- **The evidence:** with the long constant, `outcomes_tests::the_typescript_configuration_detail_is_admitted` fails
  `schema_valid`, and `every_row_projects_to_its_item_10_termination` fails for row 59 (executed on `claude/c2b1b`).
  The TSR-1 review rounds did not check the remedy against `BoundedText`.

## 1. Superseded text, and its replacement

**In R-10.3, the quoted clause is replaced.** The clause that begins "`; or, for the options OpenSIP resolves under
TypeScript 6.0.3: give every compilerOptions member …`" and ends "`… whose type, if present, is module or commonjs`"
is replaced by exactly these 290 ASCII bytes:

> `; or, for an option OpenSIP resolves under TypeScript 6.0.3, correct the value, path, spec, bound, package.json or toolchain member the subject identifies, as the TypeScript 6.0.3 resolution profile states; a long subject keeps only its leading characters and the sha256 of the full subject`

S10b's 646 characters plus this clause make 936 characters, within `BoundedText.maxLength` 1024.

The rest of R-10.3 stands:
- the remedy is S10b's text, followed with no other change by this clause, under the same key;
- it is copied byte for byte to every selected carrier;
- the public record, the D9 row and the detail vocabulary are unchanged.

**In TSR1-C30, the last sentence is replaced.** "and the remedy names each prerequisite" becomes "and each refusal's
detail carries §7's raw attribution, bounded by the inherited `subjectBoundLaw`. When the subject fits, it is
unchanged and names the failing member. When it does not, it keeps the leading window and the sha256 of the full raw
subject, and the member may not be visible".

## 2. What does not change

- **The limits themselves.** Every limit and prerequisite the long clause listed remains law where TSR-1 states it
  (§§1–7 and the §7 refusal table). E3 shortens only the remedy **text**. It changes no limit, no refusal, no phase
  order, no alias and no key.
- **The record, the vocabulary and the D9 row.** The public record and the detail vocabulary are unchanged, and the
  D9 row stays `CONFIG.INVALID`, exit 2.
- **The subject law (r2).** §7's raw attribution and the inherited `subjectBoundLaw` (`native-v2.schema.json`:829;
  `outcomes.rs`:933-948) are unchanged. E3 does not change the subject order, does not require a retained untruncated
  subject or any diagnostic store, and does not widen any carrier. The clause describes the existing bounded attribution
  honestly.

## 3. New controls

- **TSR1-C30b (the remedy fits its carrier):**
  - the remedy keyed by `native.typescript-config-unresolved` is at most `BoundedText.maxLength` (1024) characters;
  - `schema_valid` passes for a `StepTermination` carrying it, under common-v1, v3 and v4;
  - the product constant and both native-model copies are byte-identical;
  - its length is checked against the schema's `maxLength` as read from the schema, not from a hard-coded number.
- **The boundary checks (r2, NB-1).** For each loaded schema, a schema-only boundary pair, a remedy of exactly
  `maxLength` and one of `maxLength + 1` characters, is accepted and rejected respectively, and the rejection is
  attributed to `domainDetail.remedy`. The pair includes a non-ASCII scalar, so that counting UTF-8 bytes cannot pass
  as counting characters. These checks are kept separate from the exact-text and copy-equality checks.
- **The mutation:** weaken the schema-length check, and the boundary pair fails.
- **TSR1-C30c, a long-path attribution control (r2, RF-1):**
  - **The long case:** a refusal whose raw subject exceeds the bound, for example a 1,013-character configuration
    path holding `{"compilerOptions":{"strict":null}}`. It carries exactly the bounded subject `subjectBoundLaw`
    yields: the leading window, the marker and the sha256 of the full raw subject. That digest is checked against an
    independent recomputation. It also carries the exact revised remedy.
  - **The short case:** an ordinary short-path refusal carries its unelided subject, naming the member.

## 4. What remains gated

E3 accepts no implementation. C2b-1b implements the remedy constant and the model copies, and runs C28's remedy
clause, C30, C30b and C30c.

At C2b-1b's binding, the following are copied unchanged into the architecture repository beside TSR-1, and the
inventory records them:
- `ERRATUM-E3-r3.md`, this exact file;
- its adoption receipt, which pins this file's sha256.

r1 and r2 are review history, and are not bound.
