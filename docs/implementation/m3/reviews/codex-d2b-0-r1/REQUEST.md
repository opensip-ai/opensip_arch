# Review request: D2B-0-r1 (the successor schema materialization, D2b plan r3 sub-unit D2b-0), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-0-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, generators or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing, Git queries, and these read-only commands:
  - `python3 -I -B tools/check_operability.py source --repository .` in the candidate worktree;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-0-r1/evidence/check_d2b0_preflight.py /dev/stdout`, which executes no generator or product code.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-0-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 46093 bytes, SHA-256 `8b5f799c471da120b1ac3d6c71cd2bafd9169aab8872f8da65786a9b02201119`, 167 members, the contract successor record `d2b-0-r1/successor.json` and its candidates exactly. Rehash every member.
- **Bases:** product `23b3871269c6553c96097084dd412b3aa95dec68` (the package base) and architecture `ae83833d05d956a0562e188f0ad04fc37a63944b`.
- **The lane base differs (LD-D2B0-8).** The lane of record, attempt 3, ran on `3e70bbf`. The package base adds D2b-1's code commit `d70af81` and the v218 lock commit, both disjoint from this unit's paths; D2b-1 touches identity only in `lib.rs`, additively. The post-rebase focused check, `evidence/d2b0-postrebase-check/postrebase.json`, ran on the package base under the lane lock with the candidate applied, and compares each result with attempt 3's. Judge whether this stands in for a full rerun.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b0`, detached at the product base. It has seven edited paths and two new ones, frozen as `d2b-0-r1/product/` copies with their parent and candidate pins in `product-map.json`.
- **Read first:** `d2b-0-r1/SCOPE.md`; then `successor.json`, `source.json`, `product-map.json` and `evidence/` (`preparation.json`, the lane of record `evidence/d2b0-checks-r1/`, and its runner, preparer, preflight and builder).

## Authority

- **The plan:** D2b plan r3 (`supervisor-d/d2b/PLAN-r3.md`, accepted, `codex-d2b-plan-r3`): §1's split and order (LD-D2B-1), and LD-D2B-13.
- **The successors:** FA-2 and RUST3-LIM (`native-successors-fa/fa-2/`, `rust3-lim/`), their accepted schema candidates and their materialization maps.
- **RCA-1's materialization** (`native-publication/rust3-identity-materialization-r1/`): the product handshake base, and the template for a materialization as a contract successor.
- `tools/verify_design.py`, `tools/contracts/` and `tools/security/discovery_census.py` at the product base.

**This unit proposes one narrow D2b plan amendment, LD-D2B0-A.** Judge it as an amendment to the accepted plan's text, quoted and replaced in SCOPE. Accepting this unit accepts the amendment, and a verdict with required findings against it rejects both.

## What to review

1. **LD-D2B0-A.** Check:
   - **Its evidence:** that `SubjectIdV1`'s pattern is outside `tools/contracts/runtime/patterns.ts`'s selected table; that the same pattern's three schemas are admission-only; and that the two root law keywords are outside `runtime/schema.ts`'s annotation set, the only unselected keywords in either schema.
   - **Its scope:** each replaced passage and its replacement, and that it moves the closure change, the blind refresh and the successor payloads' generated carriers to D2b-3 and D2b-4. Each of those units either uses typed Rust or TypeScript over the admitted schema, or takes the generator's pattern-profile and annotation extension under its own review.
   - **That nothing is lost:** LD-D2B-2, the codecs' schema checks, and LD-D2B-1's refresh obligation where the closure does change.
2. **The materialization.** Check:
   - the exact accepted bytes at the product paths;
   - the admission registry rows, its architecture copy, and the admission source map's rows and re-pointed `registryArchitectureSource`;
   - the identity `SOURCE_PINS`, and the host and storage embeddings, in pin order (LD-D2B0-5);
   - the identity compiler's two added annotation keywords (LD-D2B0-7), and that they change no evaluation;
   - that no generator table, generated output, carrier file, manifest, census receipt or tool changes. The preflight checks 99 tracked generator inputs and outputs and the receipt.
3. **LD-D2B-13:** the three-way handshake re-derivation and the reported differences from the maps' recorded hashes.
4. **The successor record (LD-D2B0-6):**
   - its three parents, each an accepted input of the current lock;
   - candidates that exactly cover the subject;
   - the pre-bind state: verify_design on the candidate refuses only for the unbound copy; with that copy accepted, generation sources are unchanged and admission sources are 52.
5. **The controls:**
   - the two host tests;
   - the lane: equal failure sets and the new passing tests (identity, host, storage, evaluator), rustfmt, Clippy, the focused tests, the census `--check` passing against the unchanged receipt, FW-01, the environment exceptions, the operability census and the census-closure check;
   - six mutations, each caught by its named detector.
   - lane attempts 1 and 2 (`evidence/d2b0-checks-r1-void-attempt1/`, `-attempt2/`) are void and history only: attempt 1 was killed before LD-D2B0-7 (the registry did not compile); attempt 2 was killed after the host comparison showed the hard-coded 50-source count in `crates/host/tests/admission_tests.rs`, now 52.
6. **LD-D2B0-7 and LD-D2B0-8:** the identity compiler's two annotation keywords, and the lane-base difference with its post-rebase check.
7. **The deferred decisions** (the generator route's namespaces, mappings, entry points and provider entry points): that deferring them leaves nothing unowned.
8. **No regression** in the accepted plan or the bound successors.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "productCodeAssessment": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "amendmentLDD2B0A": "ACCEPT" | "REJECT", "subjectManifestSha256": "8b5f799c471da120b1ac3d6c71cd2bafd9169aab8872f8da65786a9b02201119", "requiredFindings": [...], "nonBlockingObservations": [...], "blindReceiptStaysCurrent": true | false, "generatorInputsUnchanged": true | false, "productQualification": false}`. Use ids `D2B0-R1-RF-n` and `D2B0-R1-NBO-n`. `ACCEPT-DESIGN-UNIT` requires an empty `requiredFindings` list and `amendmentLDD2B0A: "ACCEPT"`.
