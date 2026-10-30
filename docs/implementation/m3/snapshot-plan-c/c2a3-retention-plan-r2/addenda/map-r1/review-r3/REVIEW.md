VERDICT: ACCEPT-ADDENDUM

No required findings remain within this plan-addendum and conditional source-accounting scope. This accepts the proposed representation, pricing selection and explicitly amended bootstrap policy. It does not establish implemented complete M, native execution, unit acceptance, integration, census, fit, cap adoption or qualification.

References below are relative to the frozen `review-r3-subject/`, not the working directory recorded in `subject.json`'s `frozenRoot`.

Numbered findings and closure:

1. **C2A3-MAP-R1-RF-1: CLOSED.** `build_ledger.py:75-132` now expands the const/mutable null tests, runtime selection, address/cast forwarding, correctly ordered alignment predicate, and reconciled RawVec/Unique/NonNull pointer chain. Lines 91-92 retain the slice-construction forwarding boundary; lines 181-203 and 222-253 use the reconciled allocation and drop routes. The additional conversion, fat-pointer and arithmetic expansions address the related reachable families. Traversing all eight ledger roots confirms that the older imported `raw_ptr`, `raw_nonnull`, `inner_ptr`, `vec_ptr`, `vec_slice`, `vec_deref`, `candidate_blobs` and `iter_new` definitions are not reachable. The funding import remains byte-identical provenance rather than an exemption for those wrappers.

   The regenerated rows reproduce as follows:

   | Row | Model visits | Selected allowance |
   |---|---:|---:|
   | Per-Blob local | 870 | 1024 |
   | Component fixed local | 895 | 1024 |
   | Slot fill/drop dispatch per component | 198 | 256 |
   | Admission loop per component | 549 | 1024 |
   | Preparation fixed | 644 | 1024 |
   | Admission fixed | 1130 | 2048 |
   | Funding fixed | 682 | 1024 |
   | Funding scan per Blob | 217 | 256 |

   Each new selection is the next power of two covering its model row. Funding retains its accepted sufficient literals. No literal changes from round 2 are needed for these revised totals.

2. **C2A3-MAP-R1-RF-5: CLOSED.** `ADDENDUM.md:115-124` expressly extends the standalone first-refusal bootstrap through the scope result, public Budget conversion and final typed return to the public caller. It also covers an already-latched incoming scope without entering the closure. This is a bounded, candidate-independent instrumentation exclusion, not retrospective payment by a refused debit. CI/pin/resource cleanup remains outside it. After COMPONENT succeeds, `build_ledger.py:319-325` supplies the 55-visit `single_wrapper` row inside COMPONENT, covering the represented success transports/Ok mapping and later-failure public mapping. The set route retains its separately prepaid frame. The unfunded public mapping identified in round 2 is therefore resolved.

3. **RF-2, RF-3 and RF-4 remain CLOSED; no new required finding.** Slot storage is initialized once without replacing a live empty Vec. The explicit funding roots preserve the larger audited loop scaffolds and source helper multiplicities. The unsupported fit multiplier remains removed, and the map comparison remains labelled as an order estimate.

Non-blocking notes and answers to the remaining questions:

- **Option B and kernel re-review:** the amendment is sound. Each accepted Blob still has an equal-path retained entry with its exact length and digest; the authenticated body digest is then checked. The six charge sites, immediately preceding positions, refusal order and published K price are preserved. A disordered or duplicate input need not always refuse if the required correct entries are encountered; the safety property is that it cannot admit incorrect required bytes. C2a-3's sole producer supplies candidate order. Section 6 identifies the necessary signature/source-guard/test/mutation re-review, and §8 makes the disorder and initial-debit controls mandatory. The kernel still allocates and copies no payload.
- **Removing the collector announcement comparison:** this is lawful under the explicit amendment. The named accepted controls do not independently require that particular hexadecimal comparison when CI verifies the pinned stream and K rehashes the actual bytes against the candidate. Section 2.3 accurately states that a false announcement alone is no longer checked by the collector, preserves the authorized producer, and keeps the finish-before-publication condition. No kernel digest check is removed.
- **Accounting and inherited counts:** the reconciled construction, reserved-capacity push and normal drop routes are coherent under the declared logical accounting and primitive assumptions. The exact first-loop and raw-pointer audit inputs are applicable. Section 5's conditional Zip dominance argument explains reuse for `Zip(Iter, IterMut)`, including mutable-slice forwarding and early exit; it does not assert compiler specialization. Retain its exact-source confirmation in the implementation proof. It would also be useful for the checker to enforce the legacy-pointer reachability exclusion, which I checked independently here.
- **Failure and cleanup coverage:** successful-prefix accounting plus a single terminating failure ceiling is conservative in the proposed model. The failed Blob's buffer drop is 176 visits, covered by its unused successful push/element-drop rows; earlier elements drop once under their own rows. Funding retains its one 128-visit post-debit error reserve. These are source-model ceilings under the declared carrier/leaf assumptions. CI-owned cleanup, receipt-owned core cleanup and whole-candidate typed failure/latch controls retain their own obligations; none becomes trusted bootstrap work.
- **Native widths:** 128/264 remain the S1 slot-size premises. The new prototype test asserts RetainedTree/index entry/core roles/Failure/Collector as 256/40/136/32/40. This improves the implementation gate but is unexecuted evidence in this review. Exact-candidate native carrier, allocation, compiler/drop, feature and failure-path controls remain required; the logical transport model is not a hardware-traffic or RSS result.
- **Bootstrap and zero components:** moving the constant COMPONENT debit before CI open is coherent as the expressly reviewed policy amendment. After success it funds the former funding bootstrap; after refusal the new exact endpoints apply. The enumerated n=0 frame path is a bounded zero-allocation control exception preserving the inherited zero-charge requirement. Later core resource cleanup remains receipt-owned, and no CI work or arbitrary caller work inherits the exclusion.
- **Formulas and fit record:** the staged component debits agree with `M_edges = 2048 + 1280F + 128E`, the 40F index storage, payload records and 2B copy streams. The actual nonempty frame is `3072 + 1280n` edges, with two shared storage records. The stated sum of per-component frame bounds exceeds that actual charge by `3072(n-1)` edges, `2(n-1)` objects and `(64*3072 + 256)(n-1)` bytes. The zero frame remains zero. All four illustrative rows and cap fractions reproduce. They cover M plus one component's frame only; K, CI, C2a-1 and D4 remain additional. X-SD9-1/2 stay open, and no aggregate fit, census result or cap change follows.
- **Editorial:** §9 preserves round 2 intermediate totals, while §§4-5 and §10 contain the current round 3 totals. Label §9's figures explicitly as historical when publishing the accepted record to avoid confusing 755/758 with the current 870/895. This does not affect the current ledger or verdict.

Verification: live controls still select this PLAN.md at R2-DEEP, and preflight returned `ROUTE-OK R2-DEEP codex gpt-6.1-sol/high`. The manifest and all ten members matched their declared SHA-256 values and sizes before substantive review. The proposed product files match Git `b4ac8ff0dc72bdd59325691a36bccaa5f54efc34` and are byte-identical to the round 2 product files; the whole proposed diff matches that commit against `5579e0dcddc30c56d51c0b5ac4ec55e384f80598`. Its added carrier-width control was read as source only. The funding import matches the accepted file. Both permitted scripts ran with `python3 -I -B` under a read-only output interceptor: CALL-TREE.json, LEDGER.json and ledger-report.json reproduced byte-for-byte without writes. No build, test or product code ran; no private data, keys, installations, stores or T2 cache were accessed. Only REVIEW-r3.md was written.

Verified subject SHA-256: `ffdedab271bb4e1469fc98ecd5ffb58b6910a0fe7f3059ae3a8265cd5f5c93c1`.
