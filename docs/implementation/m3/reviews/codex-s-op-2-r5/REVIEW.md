# S-OP-2 r5 review

**Verdict: REQUIRED-FINDINGS.** SOP2-R4-01, -02 and -03 are resolved. Both r4 non-blocking observations are taken up. One new required finding concerns an unmapped deletion from the wire-schema common rules.

Subject: `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, 129,029 bytes, sha256 `a75afe9cede097dd52e8c83862060a8debd1b298e2320ab9321068745601b15b`. All 37 pinned inputs match their live bytes. Line references below use this exact r5 subject unless expressly marked r4.

## Required finding

### SOP2-R5-01 — P2: restore object-key and reader-order rules

**Location:** item 13c, lines 515–527; item 13a, lines 451–465; K7 at line 558. See `subject-diff.txt` and `object-rule-check.json`.

The suffix edit also deletes r4 line 508:

> Objects have exactly the listed keys, written in the listed order. Readers accept any order, but no extra, missing or duplicate key.

There is no replacement. The remaining wire-spelling table fixes canonical encodings, while item 13a sends nested field values back to item 13c's complete predicate. Duplicate-key rejection and exact header validation remain explicit, but neither restores the writer-order/reader-any-order distinction for composite objects. A reader's required treatment of a reordered composite is consequently unspecified, where r4 stated it directly.

For example, K7 `{"bytes":1,"truncated":false}` and `{"truncated":false,"bytes":1}` are the same JSON value. Both occupy 29 bytes, within K7's 48-byte V. r4 expressly admits either order and re-encodes in canonical order. r5 no longer expressly requires admission of the second spelling. This is a contract regression, not an observed product-reader failure or a claim that raw private values can pass through the reader.

The deletion is absent from the response table at lines 29–33 and contradicts line 35's statement that nothing else of substance changed.

**Fix:** restore the Objects common rule, or its operative equivalent. State that writers use the listed order; readers accept any order; and each composite has exactly the keys permitted by its selected form, without extra, missing or duplicate keys. Preserve item 13a's existing parsing/header rules. Extend C-4 with a permuted-key composite reader positive that canonicalizes on re-encoding, plus nested extra/missing-key negatives. Canonical writer round trips remain byte-identical. The three r5 fixes need no redesign.

## Resolution of prior findings

| Finding | Resolution | Evidence |
|---|---|---|
| SOP2-R4-01 | Resolved | Items 16–17, especially 633–645 and 658–689; C-7 at 938. One flag read selects one source tally. Direct and pre-scope outcomes occupy separate partitions in one atomic file snapshot. Transfers are not outcomes. |
| SOP2-R4-02 | Resolved | Item 17 at 724–767; C-7 at 938. The admission CAS precedes gate access. A lost admission CAS never issues a syscall. Every subsequent CAS loser path is specified. Frozen outcomes reflect recorded state. |
| SOP2-R4-03 | Resolved | Item 13c at 520–526 and 559–562; C-4/C-5 at 935–936. No trimming or partial matches. Suffix refusal follows each grammar; lawful K12 path/tail suffixes survive E encoding. |
| SOP2-R4-NB-01 | Resolved | C-7 expressly pauses between the first and second sink increments. F counts unfinished calls, not absent projections. |
| SOP2-R4-NB-02 | Resolved | Standing/short names at 104–114 and pins. Fixed accepted r4/r6 plan files replace the mislabeled drifting context. r4 G7/O1 references and r6 G7/O1 rows match. |

The prescope accounting partitions each captured source tally into disjoint classes. Per level,

`(E_pre − T) + (T − O_pre) + O_pre = E_pre`.

The direct partition separately sums `(E_direct − O_direct) + O_direct = E_direct`. T and O_pre are loaded in one immutable snapshot, and snapshot loads precede enqueue tally loads. Publication ordering establishes `O_pre ≤ T ≤ E_pre` and `O_direct ≤ E_direct`, so all differences are non-negative. Published written outcomes are delivered counts outside every loss matrix. The captured flag determines whether E_pre−T is unpersisted or drain-abandoned.

A producer that read the flag clear before capability grant stays in the prescope source. Its later push does not increment the direct file tally. The writer keeps draining beyond its first pass. C-7 covers this case, physical transfer before publication, published transfer before outcome, completed delivery, and the no-capability case. At each specified pause one projection is represented exactly once.

For the marker, the admission CAS separates logical marker admission from each syscall's gate admission. The finalizer's skipped transition excludes every later successful admission CAS and therefore every later syscall. Unconfirmed means admission was recorded without a recorded completion. The suppression/completion losers publish only post-freeze observations. A writer paused after an open gate load may issue one admitted unit after closure; that accepted mechanism's suitability remains an S-OP-7/X3D decision.

## Evidence and limits

`law-checks.json` records finite abstract checks over atomic operations: 1,045 partition states and 156 captured freezes, 1,050 arithmetic cases, 150 marker states and 23 merged completed states covering all five outcomes, 10 pre-cutoff drop orders, six lawful suffix round trips, and nine identity/code/name suffix negatives. They found no counterexample to the revised three fixes. `object-rule-check.json` records the exact text deletion and the JSON-equivalent K7 permutations. These are scratch law models using read-only inputs; they do not run product code, tests, builds or timing measurements, or prove Rust memory ordering and snapshot reclamation.

The review preserves the accepted bounded per-sink cells and the stated limitation that logging cannot record the required envelope's own subsequent write outcome. The exit code and ordinary termination path carry that outcome. Deferred S-OP-1/-5/-6/-7/-9/-10/-12 and O4/O7/O9 remain deferred. No new issue beyond SOP2-R5-01 was found in the r5 diff.

This verdict concerns successor text only. Item 24's later recording unit needs its own ACCEPT-DESIGN-UNIT and single-string subjectManifestSha256. It is not an inventory unit.

All new files were written only under this review directory. No repository edit, commit, push, delegation, product build, Cargo command, test, real OpenSIP-home access, or 413-fixture access occurred. Scratch runs used Python 3.14.6 with `-I -B`, `nice -n 19`, and a private 0700 TMPDIR under the review directory.
