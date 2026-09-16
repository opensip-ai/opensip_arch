Done. Everything outside `scratch/` is pristine; v2 is untouched.

## What I delivered

**Bindings verified first:** all four bound inputs match `input-manifest.json`, and the frozen Source25 manifest `fa8cdc79…` verified across all **12869** members (0 missing, 0 mismatched). Two `__pycache__` files sit on disk outside the manifest — disclosed, benign.

**Task 1 — carrier (CR-04/CR-07/COV-03).** The defect is a joint unsatisfiability, which I established by execution rather than reading: **no** physical DDL anywhere in Source25 admits `SEAL` (all four carriers of the DDL text share the identical 14-member recordSchema-1 set), while the physical carrier *requires* `TERMINAL` at the reserved slot and schema 3 excludes it; and the physical `platform` CHECK enumerates exactly the four S8 **display aliases**, which S8 MUST-2 refuses as a grant platform. Resolution: a new `carrierFormat` axis distinct from `recordSchema` and `stateSchema`, and a new table whose single segregation CHECK carries `TERMINAL` as the *already frozen recordSchema-1 body* — so schema 3 is not widened and `TERMINAL` is never a public `JournalRecord`. Migration turned out to be expressible **entirely within the frozen constraints**: inherited rows verified byte-unchanged, legacy alias retained verbatim, second migration aborts.

**Task 2 — recovery (CR-08).** Ledger first, journal second, hazard resolved by exactly one bounded reopen then an honest owner-attributed `unavailable-busy`. 21/21 model cases, zero attempted mutations, ledger opened exactly once per case.

Two things worth your attention. First, **I found a defect neither you nor the followup had named**: the v8 witness carries `bodySha256`, the *tail body* digest, so it detects **no** interior substitution at all — under either chain law. carrierFormat 1 §5.4 claims "the chain head is in the witness"; it is not, and two frozen documents disagree. Second, **this corrected my own initial plan**: I had intended to propose a recursive chain, and the executed matrix shows that alone buys nothing observable, because the witness field is the binding constraint. All four stronger-authentication options are costed and **none is adopted**.

**Task 3 — gate/latch (CR-23).** Your ownership proposal is sound and I adopted it unchanged. The corrections land on the **followup**: its linearization point at "callback entry" is wrong (staging commits nothing, so a latch there must still refuse — your atomic `preparing → commit-admitted` is the right point), and its remedy (iv) is **not implementable as written**, since the closed schema-3 body has no sequence-valued member. Correlation moves to private metadata plus a reader rule. 15 exhaustive interleavings, zero violations.

## Two things I want to flag plainly

**My negative controls found four real gaps, two of them genuine holes in my own validator** — it checked trigger flags for carrierFormat 1 but not 2, and matched the segregation CHECK by text, so *deleting the CHECK passed*. The validator now re-derives every asserted frozen flag for both formats and carries 13 behavioural DDL probes. I'm reporting this because until those controls ran, my checker could not fail.

**Honest limits:** no OS durability, no real crashes or lock contention, no Rust compiled (the E0505/E0451 reasoning is an ownership argument, not a compiler result), F42 has no feasible model, every added fault case is `not-executed`. The inherited `prev_sha256` encoding is unpinned in the corpus — one DDL comment, zero call sites, zero fixtures — so I pinned it *prospectively* for carrierFormat 3 and cannot claim byte compatibility with any real historical instance. `REPORT.md` §7 carries nine remaining defects and open decisions, including that **CR-04/CR-07's original texts are not in the bound four**; I reconstructed their scope and then established the facts by execution instead of relying on either description.

No acceptance, readiness or self-acceptance is claimed. `scratch/output-manifest.json` freezes all 7 added files, both patch before/after pairs, and all 6 control script/report hashes; `scratch/REPRODUCE.md` has the exact commands, which I re-ran clean end-to-end.
