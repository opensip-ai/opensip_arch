Resumed independent delta review of author04 (same reviewer context as review 03, not a fresh session). **Verdict: changes-required**, with 4 new required findings and 5 advisories. The write-up is `m1-native-wire-owner-review-04/review.json` and `review.md`; probes, mutants and outputs are under `scratch/`.

**Custody:**
- **Before and after:** 80/80 files with none extra or missing, the inner manifest is 39+4+36 plus itself, all 36 architecture pins unchanged from candidate 03, Node pin unchanged.
- **`prior/` copies:** byte-equal to their originals, so the earlier failures, the vacuous-control disclosure, the length-cache bug and the corrected counts are preserved.
- **Bytecode:** none this time. Custody checks used `python3 -B` and read pins as text, never importing from a frozen subject. All runs used my copy with `-I -B` and a private pycache. Subjects 03 and 04 contain no `.pyc`.

**Reproduction from only the 39 inputs:** check 478/0, identical to the frozen output, and selftest 108/108. For root, I only saw the check output (478/0); no root selftest or isolation result existed yet, so I don't claim root passed.

**Review-03 findings:** RF-1 to RF-4 and all nine advisories are resolved for the cases they named; four leave the residue below.
- **Newline `..`:** my `x<LF>/../y` counterexamples are now refused and `a/..<LF>` is admitted.
- **Owner functions:** they no longer raise untyped exceptions.
- **Prepared sets:** the explicit/defaulted split works for all-fresh sets.
- **Error codes:** limit keys use `UNSATISFIABLE`, representability keys `PRECONDITION_FAILED`.
- **Canonical send schedule:** bound to the sender, and my review-03 mutants are now caught.
- **Independently reproduced:**
  - TS2 manifest frame of exactly 67,108,864 bytes (64 MiB) at 180,399 entries, and 67,108,865 one over.
  - My small plan: 6,685 bytes, or 6,834 with the reserved 149-byte Cancel.

**New required findings:**
1. **Defaulted prepared set bypasses the wire limit.** With 300 rows and one stale row, the owner falls back and keeps 299 usable rows; the new check only runs when the owner outcome is "admitted". The planner accepts a 299-entry prepared manifest, which the carrier then refuses (`ARRAY_BOUND`).
2. **ECMA patch reaches beyond its declared scope.** It patches every canonical validator copy, including the identity model's. Identity v3 `LogicalPath` flips `a/..<LF>` from refused to admitted, even though that document isn't a declared parent and its pattern has no lookahead, so the "unchanged" claim is false. Six non-parent documents change on my test strings (c2v3, rust2, identity v2/v3, workflows common, the relation registry). Patching only the native model's validator fails 0 checks.
3. **Relation-payload CanonicalPath not corrected.** `relation-payload-schemas.v2` still has the defective lookahead and admits `x<LF>/../y.rs`, contradicting "every occurrence". Four fact payload path fields use it.
4. **Reference sender doesn't enforce its Cancel rules.** It accepts a Cancel before Hello and a Cancel with the wrong `executionId` or `analysisOrdinal`; only its size is checked. Removing its payload-byte check fails 0 checks.

**Advisories:**
- **A-1:** dropping the generated-file phrase from the not-representable remedy fails 0 checks.
- **A-2:** the sender's per-frame limit re-check can't be reached by any accepted plan.
- **A-3:** a bad prepared path now outranks the owner's non-inert refusal; state that precedence.
- **A-4 (integration duties still open):**
  - promoting the pattern corrections into owner source through the source bridge;
  - production Rust/TS matchers;
  - the M3 sender;
  - generator work and the renderer rebase;
  - the D9 exit-contract successor;
  - the fact-plane relation payload path law.
- **A-5:** keep the exact pins; the Node system libraries are trusted, not pinned, and the open/process audit is not confinement.

**My mutants:** 6 of 10 were caught; the 4 uncaught ones are cited in RF-2, RF-4, A-1 and A-2.

**Not done:**
- **Not assessed:** no production admission, codec, runtime, sender, generator or platform qualification.
- **Rust regex lowering:** not run; the crate isn't available offline.
- **Relation payload paths:** not driven through a real fact-plane admission.
- **Author checks I relied on:** the 12 plan realizations, 17 remedy pairs and the 28-pattern ECMA comparison come from the author's checks in my copy, not my own code.
