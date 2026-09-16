The review is written, and the verdict is **CHANGES_REQUIRED**: no MUST issues, three new SHOULD issues and eight advisories. Everything was run from verified disposable copies. The frozen snapshot still matches its manifest afterwards (12,900 files, nothing changed or added), and no checker or probe changed a copy file.

**Checks run:**
- **Subject:** the manifest, the archive with every member, and parent36 all verified. The delta from source36 is 1 file added and 15 changed.
- **Reference groups:** all six passed (evaluator3, foundation, integration, native, security, workflows).
- **Planning checks:** both passed (320 mappings, 198 paths, 20 packages); all 54 recovery cases are still not executed.
- **Author package v14:** its verifier passed. That covers seven valid Runs, three reminted negative controls that complete replay refuses, three binding controls and seven query checks. Its "author-assisted, built against source33" provenance is recorded unchanged.
  - I could not find the literal A9/A10 limitation text in the current package files, so those limitations are recorded as your charter states them.

**SHOULD issues:**
1. **S37-01 – Cause order has no owner.** Nothing defines the order of a Run's deficiencies before the D9 reducer picks the primary, or which Coverage record `coverageId` should name. The sealed proof keeps deficiencies only as sorted sets, so no verifier can recover that order. On one actual indeterminate Run:
   - either of two deficient Coverage records, or none, gives a schema-valid termination;
   - the native helper returns `COVERAGE.BUDGET_EXHAUSTED` while the entry detail names `resolution-incomplete`;
   - three concurrent conditions produce six different valid `reasonCodes` sequences.

   Class and exit are the same in every case, which is why this is SHOULD rather than MUST.
2. **S37-02 – Report hooks conflict with the product boundary.** The prototype report inventory (R02, R24) selects "registered external report hooks" running in a worker lane. Admission §5 excludes that: the host owns rendering, and hooks and imperative contributions are not admitted. No module in the plan owns it.
3. **S37-03 – Query `advisory` flag not fully enforced.** The graph-query response schema accepts `advisory: true` on `run.show` and `finding.list`. The contract says it is true for exactly four operations.

**Four independent probes, all of which discriminate:**
- **Cross-unit:** evaluator proofs and graph queries return the same facts per subject across two universes.
- **Target/proof boundary:** an indeterminate proof against zero complete query rows is still disclosed as incomplete search.
- **Retained graph query:**
  - a package endpoint without a manifest path is refused as malformed before any Run or availability check;
  - the purged, expired, corrupt and unavailable states all map to `HOST.IO_FAILURE` exit 4;
  - cursor binding and visit caps behave as specified.
- **Fully reminted false results:** three mutants (fail turned to pass, an unknown turned to known-false, an execution deficiency erased) get new valid identities. Structural admission accepts them; complete replay and the public graph query refuse them. The SEAL adapter was assessed only by reading its source, which delegates to `close_run`.

**Advisories:**
- The carrier DDL checks only the first character of hex fields, and does not enforce `first_generation` before the format row exists.
- `MIGRATION.CORRUPT` is used for a project-key mismatch that may really be a swapped carrier.
- Two recovery conclusions (`unknown-carrier-incompatible`, `split-brain-custody-condition`) have no public error route.
- An unknown availability value is silently ignored.
- A complete-replay mismatch in a graph query falls under the corrupt-bytes row.
- Some standing notes are stale.
- The superseded schema annotation is accepted as designed.

**Dispositions and assumption:**
- All 107 disposition rows are present, each with `appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`.
- All 30 author grades stay PENDING.
- DR-201..205 are ROUTING-ASSESSED-ONLY-NOT-APPLIED.
- TCB-SCOPE-01 is assessed once: coherent as a scope choice, not qualified, and S37-02 is the one planning text that conflicts with it.
- The 30 residuals and 28 condition-2 obligations are retained, and all 32 qualification gates remain unperformed.

**Limits:**
- No grade, activation or implementation authorization is granted.
- This is not a blind reconstruction, and source36 acceptance is not treated as covering source37.
- Part of the S37-01 reproducer applies the D9 reducer text to constructed conditions, because no product host finalizer exists.
- Dependency totality, imported evidence, wire version tokens and repair disclosures were assessed by reading and the reference groups, without independent probes.
- The two ~737 MB working copies remain in `work/`, along with an unused `probes/make_copy.py`.

Files are in `/tmp/opensip-design-corrections/claude-independent-design.v37`:
- review.md
- review.json
- probes/
- receipts/
