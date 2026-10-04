**ACCEPT — J-RW r4, law and contract-soundness review.** Both required r3 findings are resolved. No required findings; one non-blocking historical citation correction.

Reviewer: Codex. Subject: `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, 118,261 bytes, SHA-256 `9c53bce7185399511340b3313d55379395cd7029d375cb7006a514f859ab617f`. Product source was judged at `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1`; the observed HEAD was the same commit. The r3 diff base matches `9aa304106bfe7926cee4f43ed5c51dadcc906c0920ed97751c7cd78f4d2b6dee`.

**JRW-R3-01 is resolved.** Independent text enumeration of `selected_ddl()` at `d2c00a9` yields these counts:

| Fragment | Tables | Explicit indexes | Triggers | Total |
|---|---:|---:|---:|---:|
| ATTEMPT_DDL | 1 | 0 | 3 | 4 |
| PAIR_DDL | 2 | 0 | 6 | 8 |
| AVAILABILITY_DDL | 1 | 1 | 3 | 5 |
| recovery_material::DDL | 1 | 0 | 3 | 4 |
| recovery_pins::DDL | 1 | 0 | 0 | 1 |
| pin_transactions::DDL | 1 | 0 | 3 | 4 |
| **Total** | **7** | **1** | **18** | **26** |

All 26 kind/name pairs match the pinned r3 source census. The corrected response row, item 3.3 and RW-C17 now agree with source. RW-C17 requires enumeration by kind and name, fails on a mismatch and forbids changing DDL to match the prose. The seven table names and explicit index name match the selected fragments. k remains 26; the six per-fragment totals, RW-C5 and the positive-view stop rule/N-L0 fallback are text-identical to r3. No product schema change was requested or performed.

**JRW-R3-02 is resolved.** Item 2 and LD-16 explicitly authorize C-TRUST/C-TDIR as steps of the mandatory floor publication on the authenticated closure and pending write. They require the publication to confirm and its owner to advance before the original clocked continuation refusal is returned. They manufacture no admitted view and grant no lease. RW-S5 now names X4T r13 after accepted r12 and preserves r12's clock, write-ahead and lease-free refusal rules.

This matches X4T r12 `:170-175` and `:205`, and the integrated source:

- `current_trust_admission.rs:1032-1066` checks the stored-state join, authenticates the closure and admits revocation/policy before S4 and EV-CLOCK. S4 refusals return at `:1094-1105`, before a clocked result can reach publication.
- `:243-289` distinguishes the admitted view from the clocked refusal while providing floors/time/pending-write access for both. `:1113-1125` retains the clocked refusal with its admitted time and pending write.
- `floor_publication.rs:973-995` applies check 3, requires a pending write and `needs_write`, then publishes at `:993` before `into_view` at `:995`. Publication failures return first. After successful publication, the clocked variant returns its stored refusal (`current_trust_admission.rs:286-289`), never a view.
- Report-only mode stores no pending write (`current_trust_admission.rs:1091-1093`), so neither publication nor its completion runs. Earlier refusal paths likewise reach no publication.

The non-reference proof remains sound on the clocked path: the closure is checked and authenticated before EV-CLOCK. A named torn/misbound member would already have refused that closure. The successor bucket remains outside the reference-directed read set (X4T r12 `:76`, `:193`). The fence, retained-handle predicates, P-ACL/P-PREFIX bounds and dependency-before-pointer order are retained.

RW-C18 covers each of RW-T1, RW-T2 and RW-T3 with a required floor advance and a clocked refusal: completion, confirmed publication/owner advance, unchanged continuation refusal, no view/lease/later step, then repeated refusal at an equal or greater tEval. RW-C19 covers native parent failures as `HOST.IO_FAILURE`, custody and non-prefix failures as `installation-incomplete`, and budget refusal as `WORK.BUDGET_EXHAUSTED`, ahead of the clocked result. It also requires earlier refusals and report-only reads to remain effect-free. RW-C14/RW-C15 carry the clocked-path invariants, and J4d owns the new controls. These are future implementation obligations; none was run here.

The integrated test source at `floor_publication_tests.rs:801-852` supports the stated write-ahead/refusal sequence and the sticky-refusal example. Its contents were read only. RW-C18 does not incorrectly require every subsequent refusal to have no anchor publication; it requires the unchanged refusal and monotone tEval.

**Re-pins and scope.** All five X4T mappings are exact passage matches: r11 `97-102` to r12 `164-169`, `102` to `169`, `120` to `193`, `141` to `216`, and `153` to `233`. The acceptance review pins X4T r12 to `cf566db721c0dd3b24aabdbf4613062c59ecbf52d7f64ebed507016f9f9643fb`. The new integrated Admission, fenced-read, refusal-code and test-source citations hold at `d2c00a9`. The unchanged earlier floor-publication passages and storage DDL were checked from immutable Git objects. Cargo.lock identifies libsqlite3-sys 0.38.2 at `168-169` and rusqlite 0.40.2 at `322-323`.

The lead's X1 edit correctly names `ordinary-platform-x1/PROPOSAL-r1.md`; that snapshot matches `d747adf076b698a053748dc52ee1e2e61d4ddbbf6643b6e298a0049bd5dcfd5d`. The live amendment was not used. J1 r5 `:815` supports the landed source-repair-command correction; M3-PLAN r9 `:284` supports the added X3b/registry owner list. Those record notes do not claim the remaining recommendation/sub-unit records have landed.

All 26 r3-to-r4 hunks were inspected. Every substantive change fits the two responses or their declared re-pins/record notes. J-C22's closing bold delimiter was incidentally lost at `:576`, with no contract-text change.

**JRW-R4-NB-01 — correct historical TrustRow line labels (P3, non-blocking).** Location: `PROPOSAL.md:90`, `:26`, `:407`, `:461-462` and `:820`.

The row mapping is unchanged, but X4-F2's introductory lines move it two lines. At `cd5958b`, Continuation is `:93`, HostIo `:98`, Budget `:99`, and Incomplete's subject `:105`. At `d2c00a9`, these are `:95`, `:100`, `:101` and `:107`. The mapping blocks `cd5958b:87-112` and `d2c00a9:89-114` have identical text. Consequently, the operative r4 current citations are correct, while several retained labels saying `:100`/`:107` at `cd5958b`, and the blanket claim of unchanged source lines, are inaccurate. My r3 review also carried those historical label errors.

Recommendation: describe unchanged mappings with a two-line shift. Repin retained labels to `d2c00a9:100/107`, or use `cd5958b:98/105` for historical citations, and qualify `:820`. This is non-blocking because the current source and the law agree on every relevant refusal row and both r3 required findings are resolved.

**Verification and acceptance boundary.** All **45 supplied pins plus the SQLite source pin** matched at the beginning and end. The subject remains the exact 118,261 reviewed bytes. `static-audit.json` records the DDL enumeration, unchanged RW-C5/fallback checks, passage maps and source-line shift; snapshots and the complete diff are retained alongside it.

Only read-only law/source inspection and scratch text/hash analysis were performed, using Python `-I -B` at `nice -n 19` with isolated HOME and TMPDIR under this directory. No Cargo, builds, tests of any kind, SQLite fixtures, wraparound loops, matrix runs, repository edits, commits, pushes or delegation occurred. No real home or private 413 fixture was used. All writes stayed under `/tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r4`.

ACCEPT applies only to these J-RW r4 law bytes. J4 sub-units and RW-S1 to RW-S6 still need their own reviews. This acceptance establishes no future runtime pin or control result, accepts no inventory unit, and supplies no evidence to retire L11.
