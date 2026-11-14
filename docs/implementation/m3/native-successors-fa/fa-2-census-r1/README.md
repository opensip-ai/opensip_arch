# FA2-CENSUS-r1: section 9.8 states the symbol-census population rules (FA-2 contract successor)

2026-11-14. Author: Claude Opus 5.5 (claude-opus-5-5, R2-DEEP, medium), design-record author dispatched by the lead
coordinator. Status: **PROPOSED, r1, unreviewed.** It needs two independent reviews, the lead's assent and one
`contractSuccessors` entry in the product's `design-lock.json` before it binds anything. No product file changes.

Base: architecture main `3e87454844b5feabd7a31e21fc935c792c0c2d8b`; product main `e3cd0bf598e543be58f5e8ee1004278681bb5eeb`
(205 contract successors; FA-2 is the entry at 0-based index 85).

## Why this record exists

Three adopted errata amend FA-2's section 9.8 and each says that the FA-2 contract successor stating its text in §9.8,
with its lock entry, is owed:

- **E1** = `../../errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md` (r5, 32,962 bytes, sha256 `1dd70aa9…3232c1`), FCE1.9
  (`E1:210-214`): "a contract successor that overrides `section-9-8.md`, `README:282` and the §9.8 copy in
  `fa-2/successor.json:174`. It carries FCE1.2-FCE1.5 and FCE1.7's binding paragraph as operative text."
- **E2** = `../../errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md` (r5, 35,800 bytes, sha256 `56723546…6f031e`), FCE2.7
  (`E2:336-337`): "The owed FA-2 contract successor states v2 in §9.8, with E1 and this erratum."
- **E3** = `../../errata-2026-11-14b/ERRATUM-FA2-CENSUS-E3.md` (r5, 28,608 bytes, sha256 `83a1919b…382c5d`), FCE3.5
  (`E3:225`), and A9 (`E3:84-88`): until this successor is a `contractSuccessors` entry, every Plan that owes a census is
  refused by A6 check 4 (`E3:40`).

The receipts (`ADOPTION-FA2-CENSUS-E1.md`, `-E2.md`, `-E3.md` beside each erratum) adopt those exact bytes; every size
and digest above was recomputed from the bytes at the base and equals the receipt's.

## The form, and why

**One new contract successor in law VD2's form**, beside FA-2, not a replacement of FA-2:

| Kind | Parent and selector | What changes |
|---|---|---|
| passage supersession | `docs/v2/contracts/product-v1/native-evidence.md` line 3313 (329,013 bytes, `83b99783…`), superseding FA-2's override of that line by FA-2's exact record pin (38,659 bytes, `f6b105f4…`) | the §9.8 text. Its `before` is FA-2's `after` exactly (the `successor.json:174` copy E1 names); its `after` is the new §9.8 |
| line override | `fa-2/README.md` line 282 (37,836 bytes, `59381765…`) | row X-FA2-FG's emission duty: E1's words (`E1:60-62`) replace "rows for every first-party symbol, including those with no fact"; the rest of the line is unchanged (`E1:64`) |
| line override | `fa-2/section-9-8.md` line 1 (8,270 bytes, `2769b093…`) | the heading keeps its words and adds that the file is FA-2's rendering before the errata, that the current text is this record's, and that `9.8:N` keeps reading that file (the errata cite its lines) |

Precedent: `supervisor-d/sd-7` and `sd-8` (each one VD2 supersession of the previous record's NE:3540 override, named by
exact pin; commit `9fbaaf472` binds SD-8); `supervisor-d/d1b-integration/descriptions-r1` (adopted law files and their
receipts carried by value as candidates, with `lawFilesByValue`; commit `c4dfdb5f9`); FA-2 itself for the rendering file
whose bytes equal the override's `after` tail.

Why not a replacement FA-2 r3 record: it would have to leave FA-2's lock entry, and three bound successors take FA-2's
members as parents (`rust3-lim`, 0-based index 86, its two handshake copies; `supervisor-d/d2b-0-r2` and `d2b-0b-r1`,
indices 173 and 174, its record). A replacement also restates nineteen overrides and ten candidates that do not change. A second
plain override of line 3313 is refused by the verifier ("conflicting contract passage overrides",
`tools/verify_design.py:536-537`); a VD2 supersession is the verifier's form for a second meaning of one passage
(`:474-496`). This form changes no bound byte: it adds one record, its members and one lock entry.

## The new §9.8 (`section-9-8.md`, generated)

`section-9-8.md` here is the rendering of the supersession's `after` after its first line (`No framing, process or
compiler is exercised.` and a blank line); the build script checks that they are equal. It is FA-2's text with three
changes and nothing else:

1. The sentence at `9.8:3-5` is replaced by E1's reading, `E1:54`, word for word.
2. The sentence at `9.8:56-57` is replaced by E1's reading, `E1:58`, word for word.
3. After the first paragraph (`9.8:11`, where `E1:66-67` inserts), one inserted text: the incorporation of passages
   I1-I11 of the three errata by exact line ranges of the pinned files, one sentence on which erratum governs where they
   differ (quoting the errata's own rule), and the stated-rules block with its syntax.

Incorporation, not a second copy: the passages stay in the errata's bytes, and the three errata and their receipts are
members of this record (candidates, and `lawFilesByValue`), so the design lock pins the law text it incorporates. The
passages, in their inserted order:

| Passage | Lines | Content | Errata instruction |
|---|---|---|---|
| I1 | E1:74-78 | rule `…typescript.v1`, its sentences | `E1:66-67`, `:72` |
| I2 | E1:82-111, columns "#", "Declaration class", "Rule" | C1-C28 | `E1:80` |
| I3 | E1:122 | relations under v1 | `E1:120` |
| I4 | E1:132 | widening | `E1:130` |
| I5 | E1:160 | one binding per closure | `E1:158` |
| I6 | E3:19-95 | the carrier, A1-A10 (form, A3 table, writer, A5, the Plan-time checks of A6, A7's binding classes and replay table RT-1 to RT-7 with O1-O7, A8, A9, A10) | `E3:17` ("after E1's binding paragraph") |
| I7 | E2:53-71 | rule `…typescript.v2` | `E2:51` |
| I8 | E2:103-104 to "moves to v2." | v1 withdrawn | FCE2.3, cited by `E3:30` |
| I9 | E3:159 | rule `…typescript.v3` | `E3:157` |
| I10 | E3:130-147, line 141 included | statement 4 and the F3 sentences | `E3:128` |
| I11 | E3:167-168 to "moves to v3." | v2 withdrawn | FCE3.3, cited by `E3:30` |

The default rule is stated outside I1-I11, by `E1:54`, now the section's first sentences. "What remains prohibited" is in
the incorporated text and is not restated: no `complete` census until a binding exists (`E1:160`); a census is admitted
as `complete` only under A10's three conditions (`E3:90-95`); A6 refuses every other owing Plan before spawn; the default
rule never binds a TypeScript closure (`E3:30`).

## The stated-rules block (for the host generator, unit CR1b-LOCK)

§9.8 states the syntax; this restates it for the generator's author.

- **Where.** In the lock's `contractSuccessors` records, the current meaning of `native-evidence.md` line 3313: the
  `after` of the last `passageSupersessions` entry, in lock order, whose `parent` is that file and whose `selector` is
  `{"line": 3313}`. The verifier keeps that chain linear (VD2), so the last link is the current meaning. FA-2's own
  override has no block; a text with no block states no rule.
- **Delimiters.** The block is the lines strictly between the one line that is exactly
  `` ```opensip-stated-population-rules-v1 `` (the opening fence occurs exactly once in the text) and the next line that
  is exactly three backquotes. Lines are split on LF.
- **Rows.** Each line is one row: the RFC 8785 form of a JSON object with exactly the keys `a2Sha256`,
  `bindsRoleSubprotocol`, `rule`, `standing` (that is their RFC 8785 order). Rows are strictly ascending by the UTF-8
  bytes of `rule`, and no two share an `a2Sha256`.
  - `rule`: a rule id, `native.symbol-census-population.<name>.v<N>`.
  - `a2Sha256`: lowercase hex sha256 of `{"populationRule":"<rule>","schemaVersion":1}` (E3 A2's bytes); a reader
    recomputes it.
  - `standing`: `prospective` (an E3 A3 row; the rule is stated for A6 check 4 and A9) or `historical` (stated only for
    reading retained evidence, E3 A7; never satisfies A6).
  - `bindsRoleSubprotocol`: for `prospective`, `rust-semantic` or `typescript-semantic`, the one role subprotocol of
    the A3 row; for `historical`, `null`.
- **Failure.** Anything else: the reader refuses the block and reads no rule as stated (so every owing Plan stays
  refused). `evidence/build_fa2_census.py` `stated_rules` is a reference reader.

The block's rows, with digests computed here from the A2 bytes:

| rule | standing | binds | A2 bytes | sha256 of the A2 bytes | E3 prints |
|---|---|---|---|---|---|
| `native.symbol-census-population.default.v1` | prospective | `rust-semantic` | 81 | `6f2726992d65dfcf33700abcad964a9b1aad82178976ee2a2b508e66b7a84671` | `E3:27`, equal |
| `native.symbol-census-population.typescript.v1` | historical | null | 84 | `18c187c85b012882dd9ce022d8f4a907210456c2dd4f24d7cc614633cde12307` | not printed |
| `native.symbol-census-population.typescript.v2` | historical | null | 84 | `9610e54655c714ab30cbd54bd09d76fff993543b65f3c2d16eaa3a753f081600` | not printed |
| `native.symbol-census-population.typescript.v3` | prospective | `typescript-semantic` | 84 | `c10552a44dc8086d300fc647f8607eda22f7327f00560302d42469ca8b8f85c7` | `E3:28`, equal |

## What this does not change

No byte of FA-2, of the errata or of any bound file. No wire member, token, schema (the census schema stays as `E1:182-185`
says), frame, deficiency, cause, D9 code, internal key, binding or closure. It writes no A2 member and binds no closure
to a rule: binding is CENSUS-RULE-1b's packaging under A8. It accepts no code and lifts no prohibition by itself: A10
still needs a Plan that passes A6 and code accepted as conforming to v3.

## Evidence

`evidence/build_fa2_census.py` (standard library only) builds `section-9-8.md`, `successor.json` and
`../fa-2-census-r1-subject.json` from pinned inputs and checks, before writing: every input's size and sha256; FA-2's
NE:3313 `before` and that its `after` is FA-2's `section-9-8.md`; that the two replaced sentences are E1 FCE1.1's
quotations and unique; each incorporated range's first and last lines; E3:141's missing quote marker; A3's two rows
against the block's prospective rows and E3's printed digests; and that the reference reader reads the block back.
`--check` rebuilds and compares without writing.

## Binding owed (not made here)

Two independent reviews of this subject (review records whose `subjectManifestSha256` is the subject's, with verdict
`ACCEPT-DESIGN-UNIT`, no required findings, and `supersededPassages` listing exactly the record's one `supersedes`
object); the lead's unit assent `fa-2-census-r1-unit.json` (pins of the subject, one review, the record); and one
`contractSuccessors` entry appended to the product's `design-lock.json` (record, subject, review, assent pins), checked
by `tools/verify_design.py`. Then the host generator (CR1b-LOCK) reads the block.

## Open points for the reviewers and the lead

1. **Incorporation versus inline copies.** `E1:211` says the successor "carries FCE1.2-FCE1.5 and FCE1.7's binding
   paragraph as operative text". This record carries the replaced sentences inline and the inserted passages by exact
   reference, with their files pinned by value. If inline copies are required, the build script can generate them from
   the same ranges; the stated-rules block is unaffected.
2. **E3:141 has no block-quote marker** while statement 4's other lines (`E3:130-147`) do. I10 includes it, since
   `E3:149` binds "statement 4" and the receipt states 4(c)'s substance (`RcE3:12`). Editorial in the bytes; confirm.
3. **v1 and v2 are "stated" but not bindable.** `E1:54` says "Only a rule stated in this section can be bound"; E2 asks
   that v2 be stated (`E2:22-23`, `:336-337`); E3 withdraws v2 and A3 makes v1 and v2 unknown for packaging and Plans
   (`E3:30`). The record states both as `historical` and cites E3 A3 as governing. The errata decide this; no new rule.
4. **The interim readings stay in the text.** `E1:54` (now the section's first sentences) and `E1:160` keep "while the
   carrier of bindings does not yet exist" and "Until the carrier … exists"; E3 A5 (`E3:34`) ends them. Kept word for
   word, with the precedence sentence.
5. **Position of I7-I11.** E1 and E3 fix where I1-I6 go; E2 and E3 give no position for v2, v3 and the withdrawals. I
   placed them after A10. No meaning depends on the order.
6. **"The worker delivers it".** After `E1:54`'s longer reading, the next sentence's "it" follows "Rule ids are
   immutable (erratum FA2-CENSUS-E1)." The referent is still the census; E1's reading made this, and it is not reworded.
7. **E2's lines on C3, C5, C16, C18, C19 and C27 (`E2:73-96`)** are outside E2's quoted insertion and are not
   incorporated. They are readings of v1's cells under statements 1-3; confirm that statements 0-3 alone carry them.
8. **RT-7 labels two rows** (`E3:66-67`, one per provider). The rows are disjoint; a replay implementer should key them
   by provider and label.
9. **Rust.** From adoption (A5) a Rust census needs an A2 member naming `default.v1`; none exists and Rust Plans are
   gated (lead ruling 3 on CENSUS-RULE-1b). `E1:192-193`'s "until then it needs none" is commentary, not inserted.
