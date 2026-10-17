# C2A-PLAN-r2 review

**Verdict: REQUIRED-FINDINGS — one required finding, two non-blocking observations.**

## Subject and verification

The 957-byte subject manifest hashes to `2e7166af52e6ef2812489ba3f292835e7f52c005fc502eac3ea5e099f82587c8`. All four members match:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `c2a/PLAN-r2.md` | 27921 | `7cc9d4cb8b7dea9c36bc708b721096a7908a66471a53b101341b3647fa1a6cc1` |
| `c2a/PLAN-r1.md` (history) | 15707 | `de404a2f5b2c8539dbebb07cd475c58afe4fa4cb77954e88fade9dcd07d1f20d` |
| `c2a/X-C2A-1-r1.md` (context) | 6036 | `3f0cd8fd7f8c5ea59bf5795487f8785ca60e7d2e8428f75730bdb2bd043fedd3` |
| `c2b/C2B-GATING-r1.md` (context) | 5508 | `18e18bec084b0f0fad32404c7fa024e0f50752d337786c0c10302e55c3529b9b` |

Bases: product `b7538549b727e13013f36d3b7c2e2917e767f3f2`; architecture `7e8f5377373a0b35a3ee15fa8424feb3c3733f59`. The product's changes since `3d1d771` are D2b-0b generation/binding changes, with no change to the cited admission/custody owners. Nine relevant product sources were compared directly with the pinned product base and match. C2PM-1's successor and review pins were checked against that base's design lock.

This was a read-only plan/source review. Independent JSON-size arithmetic used inert values only. No Cargo, rustc, builds, tests, lanes, network, delegation, installation, private fixtures, signing/private test key files, held trees or T2 data were accessed. Fixture signers are named only by source symbol. Only the requested two artifacts were written.

## Required finding

### C2APLAN-R2-RF-1: Correct the encoded-size derivation used for pre-allocation work charges

`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r2.md:92`

LD3 prices a Blob as 39 fixed bytes plus the decimal length and path. Its actual canonical encoding has 96 fixed bytes, including the 64 digest characters, before the decimal length and encoded path payload. For bytes=0 and path="p", the encoding is 98 bytes, rather than 41. Every inter-row comma is additional, except before the first row. UTF-8 and JSON escaping also mean path characters are not interchangeable with encoded payload bytes. LD10 promises an exact-length buffer charge computed before allocation; the published formula would undercharge by at least 57 bytes per Blob, before considering escaping. The per-Blob allocation costs are also incomplete as a concrete derivation: one object does not state the bytes for its chosen record/map representation and descriptor structure. Thus round-1 RF-4 is only partially resolved.

Required change: Correct the fixed Blob overhead to 96 and derive the full descriptor size using actual escaped UTF-8 string payload lengths, numeric digit lengths, array separators and the other descriptor members. Publish complete WorkCost prices for the actual owned path/Blob/container/index/descriptor representations and any encoding/hash buffers, with no double charging of borrowed trust evidence. Add independent predicted-versus-encoded size/charge vectors, including a non-ASCII or escapable path, a feasible byte boundary and aggregate exhaustion. Do not implement the 39-byte formula or an unpriced allocation behind the exact-length promise. Keep the 4 MiB cap and the isolated count predicate unchanged.

## Round-1 disposition

| Item | Assessment |
| --- | --- |
| RF-1: C2PM-1 | Resolved in substance. The signed root declaration, mandatory presence, independent analyzer check, exact copy, descriptor agreement, role-specific support and ordered guard set follow the bound contract. Existing parse/shape/body/platform/field prerequisites retain their order. The selected route has a real failure envelope, one public errors detail, absent termination domainDetail and derived origin. Host bugs must retain faultCause `host-invariant`, the actual allocated request id and the existing remedy. |
| RF-2: retention | Resolved. ClosureCandidate authorizes no context, Plan or selection; successful component admission requires whole-body/tree retention. Compiler and stdlib both remain covered. Synthetic fixtures use the ordinary reader and same verifier. C2a-1/2 alone do not unblock successful C2b-1. |
| RF-3: placement | Resolved at plan level. Trust read precedes D4 and C2a inside R10a/ER10a, and these return before handoff/draw. The reservation-set controls cover both refusal paths. Later selection adds no component admission. See NBO-1 for wording that must not suppress later retained-evidence failures. |
| RF-4: work/size | Partially resolved. Count-only versus upstream entry cap versus canonical byte cap is now correct; the shared scope and cross-component aggregate are explicit. The exact size/cost derivation still needs RF-1 above, and the production profile remains an explicit gate under Q5 below. |
| RF-5: field-use ownership | Resolved at plan level. Imports, E3 syntax production, C4a Plan/stage/binding membership, H view/fact/scope/inventory, item-14a candidate results, L cache prohibition and X12d's same-core detector join are assigned. CRC-2's mirror, symbol-inventory exclusion and candidate-result exclusion remain. “No cache2 at M3” does not grant a core closure any cache-key use. |
| NBO-1: platform | Resolved. The manifest os/arch token must match an artifact in the same authenticated release and one of the catalog's four tokens. Missing/mismatched artifacts refuse; core-inventory spelling is separate. |
| NBO-2: vectors/fixtures | Resolved. The two existing CRC-1 tests are named and no redundant identity implementation is proposed. The shared fixture module retains the exact joint predicate, existing bytes, source pin, synthetic label and existing root/signers. New projection fixtures carry the signed declaration and remain role-valid. |

The supporting `c2pm-body-r1` child materialized the optional manifest property and the shared analyzer-equality predicate; it did not itself implement authenticated closure projection or all public integration. At the pinned base, the native route rows, common public detail and typed outcome keys/mapper are also present. C2a should reuse and reproduce those current carriers rather than attribute all of them to that narrow body child or replace later accepted overlays with old complete copies. What remains is authenticated guard invocation, provenance and supported-role checks, full envelope integration at the actual boundary, retention, wiring and the requested controls. No body-only validation or already-published route row proves those duties.

Q1–Q4 from round 1 are applied: no digest-only successful context; C2PM-1 supplies the major; durable absence is distinguished from promised-tree failure; X-8 remains open and ephemeral results gain no domainDetail; fixtures remain under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. C2-T8's authoritative-surface refusal stays owed to J2; carrying the label discharges only C2a's stated half. Core roles remain independent of the component trust path, as NBO-2 clarifies.

## Q5 and Q6 rulings

**Q5: The C2a helper can consume a borrowed WorkScope; production wiring needs an explicit selected profile.** The cited D4/J1 ordering alone does not supply a numeric work profile for all C2a projection/verification work. Do not infer the snapshot or discovery profile from the caller's name, use an unbounded scope, or reset the scope per component. D4/J1's owner must name and review the profile, its caps, aggregate cost model and Budget projection before C2a-4's production acceptance. Record this as a dependency gate, alongside the delivery law. C2a-1's bounded helper can be developed and checked with explicitly identified test scopes before that selection; such boundary checks are not evidence for a production profile. The corrected allocation/encoding prices in RF-1 are required regardless of profile.

**Q6: Stage the independent candidate and fixture work; gate the custody-dependent verifier and wiring.** C2a-1 and C2a-2 may land as reviewed internal library work with no production authority. A pure verification kernel may also land early if its inputs and accounting are concrete, bounded and separately reviewable, and it confers no claim of delivered custody. Do not freeze or expose an operational custody interface that the unaccepted delivery law has not selected. C2a-3's production admitted constructor and C2a-4 wiring wait for that law/interface and Q5's production profile. Early synthetic tests must exercise the same eventual verification kernel and ordinary trust path; they cannot introduce a fixture-only admission bypass or count as completed production C2a/C2b admission.

## Cross-law memo assessment

As context, X-C2A-1 correctly identifies the gap between authenticated metadata and held tree bytes. X4B/463h supply catalog and component-manifest pairs; SL:35-38 names artifact metadata without selecting an archive profile or an extraction/custody implementation. The memo appropriately asks the delivery owner for a bounded hostile-archive profile, exact TreeCommitment verification, staging/publication, custody, lifecycle/Run pinning, charged reads and typed failures. A verified catalog is not custody.

The memo is input to that law, not acceptance of its proposed installer/store design. The future law must define precisely what each artifact digest hashes, the offline artifact handoff, the custody/immutability lifetime across R10a and Run retention, and the durable/ephemeral failure routes. Its “nothing installed” failure rule must address existing published releases and partial staging explicitly. No archive format, storage authority, installation action or exception to accepted retention/replay checks is approved here.

## Non-blocking observations

### C2APLAN-R2-NBO-1: Scope the no-new-admission statement to preserve fallible retention and re-admission

`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r2.md:81`

The new pre-draw placement is correct, but “never re-runs a check that could refuse” is too broad if read as an exemption from downstream retained-record validation or storage failure handling. NE:1493-1499 requires compiler/stdlib retained records to be re-admitted before comparisons; M3-C item 10:562 requires mint-time and Run-closure consumers to use the same admission functions. Existing native_context.rs:189-223 can still report missing, malformed, wrong-identity or wrong-kind retained objects. Copying/pinning bytes into Run retention can also fail without reopening component signature admission.

Suggested change: Say that row 8 adds no new component-manifest admission and never re-verifies signatures. Preserve the existing context/Run-closure checks and typed retention/I/O failures at their owning boundaries. Add a post-draw promised-object failure control that keeps its actual cause and does not become not-installed or a second R10a refusal.

### C2APLAN-R2-NBO-2: Keep the existing authenticated-core branch outside the component-only type gate

`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r2.md:163`

LD12 says AdmittedClosure is the only closure type accepted by the Plan, while only the component candidate/tree verifier constructs it. Core evaluator/detector/provider/adapter closures remain projections of the authenticated InitialCore receipt and do not pass through a component manifest, catalog or C2a-3 delivery gate. LD7 already says they remain unaffected, so the type wording should preserve that explicit distinction.

Suggested change: Scope the two-type rule to newly admitted component closures, or name an admitted-closure sum type with a separate authenticated-core constructor/branch. Preserve the no-trust-view case in which core roles remain available and no component closure is admitted; no core role may require the delivery law or fixture root.

