# C2A-PLAN-r3 review

Verdict: **REQUIRED-FINDINGS** — two required findings, no non-blocking observations.

## Subject and verification

Manifest `docs/implementation/m3/snapshot-plan-c/c2a-plan-r3-subject.json`: 1,775 bytes, SHA-256 `4c02809d2000e6a582c1c89623af24112abfaf02a1069e80c1a9da5c8e64f7cf`. All eight members match their pinned lengths and hashes. The subject is 37,343 bytes, SHA-256 `3150a64e3a6d41bba10700b5a068e9f4931c9f212d27743bb1c49b62deb051c7`. Live product HEAD is `b7538549b727e13013f36d3b7c2e2917e767f3f2`; architecture HEAD is `a87c1234b26544e65cd2d36b613f218da41b4e86`, matching the manifest bases.

Read the round-2 request/verdict, revised plan, pinned scratch source/output and the cited product authorities. Inspected local standard-library source without executing it. Independently checked the size arithmetic using inert Python JSON, which reproduced all four descriptor lengths (201, 336, 538, 436). The scratch program was not run. No Cargo, rustc, builds, tests, lanes, network, private fixtures, installation directories, keys, held trees, T2 stores/caches, other panes or delegation were used. Neither repository was edited.

## Required findings

### C2APLAN-R3-RF-1 — Price the encoder’s integer-formatting temporaries before encoding

Priority: P2. Location: `docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r3.md:170`.

The published encoder price accounts only for the growing output Vec. canonical.rs:317-320 also creates a fresh String and writes the decimal representation for every Integer before appending it. A closure descriptor has n+2 such integers (each Blob.bytes, protocolMajor and schemaVersion). These temporary allocations occur in the first canonical_bytes call, outside the separately bounded IdentityCandidate admission. At the recorded 34,662-row boundary, there are 34,664 integer-formatting temporaries in addition to the output-buffer growth; the logarithmic objects price does not cover them. The 4D byte price is explicitly for output-buffer reallocations, with no published temporary-string price. Thus the every-allocation-before-it-is-made promise and round-2 RF-1 remain partially unmet.

Required change: Publish and precharge a conservative allocation/object and capacity-byte price for all integer-formatting temporaries in this first encoding, or use an encoder path that formats integers in a stack buffer and prices its remaining allocations. Keep the identity-admission exception scoped to IdentityCandidate internals. Add allocation-price controls with several Blobs and large decimal widths, plus a budget that funds the output buffer but cannot fund the omitted temporaries; it must refuse Budget before the unfunded allocation.

### C2APLAN-R3-RF-2 — Replace the sorting comparison estimate with a sound charge

Priority: P2. Location: `docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r3.md:168`.

n * ceil(log2(n+1)) is not an upper bound on sort_unstable_by comparator calls. Read-only inspection of the available std source (core/src/slice/sort/unstable/mod.rs::sort and shared/smallsort.rs::insertion_sort_shift_left / insert_tail) shows unconditional insertion sort for lengths through 20 on ordinary supported targets. Twenty distinct paths in reverse byte order require 1+...+19 = 190 comparisons; the published sorting price is only 20*ceil(log2(21)) = 100 edges. The body reader does not guarantee Blob ordering, so this is a valid projection input. The separate adjacent-duplicate pass does not pay for these additional sorting comparisons. The abstract O(n log n) complexity guarantee does not establish this concrete coefficient-one price.

Required change: Charge each comparison before it occurs through a fallible bounded ordering implementation, or publish a proved conservative bound for the chosen implementation and precharge it. A deterministic explicitly bounded sorting algorithm is also acceptable. Preserve Budget as a typed failure and do not reset the caller scope. Include reverse-ordered 20-path and adversarial larger-order controls that compare actual comparator work with the funded price; a scope permitting only the current estimate must not perform unfunded comparisons.

## Requested rulings

1. **R2-RF-1: size corrected; work pricing still incomplete.** The Blob formula `96 + d(N) + e(P)` and full-descriptor formula with fixed overhead 175 and `max(n-1,0)` separators agree with `canonical.rs`. Escaping correctly counts UTF-8 bytes, quotes/backslashes, short escapes and remaining controls. The boundary descriptor has base 198 bytes and rows of 120 bytes plus separators: `198 + 121*34,662 - 1 = 4,194,299`; the next row is 4,194,420. The recorded real-encoder result agrees. Predicting D before encoding and refusing Encoding before output-buffer allocation is appropriate. The count predicate remains distinct from feasible production admission.

   Conservative published prices are acceptable; exact allocator/RSS measurements are not required. `size_of`-based representation prices and a conservative output-growth bound can be used when they cover the chosen supported representation. Three- and seven-member maps fit a single 11-slot leaf; on the supported 64-bit layout the tuple-based allowance is conservative even including leaf metadata. The output-buffer doubling allowance is acceptable for its own reallocations. These allowances do not remove the obligation to price additional owned temporaries or establish a sound bound on comparator work. RF-1 and RF-2 identify those omissions. The proposed future allocation/aggregate controls are suitable obligations, not evidence that those controls already ran.

   Borrowed ordinary-reader evidence correctly incurs no second ownership charge. The explicitly bounded IdentityCandidate admission under the 4 MiB descriptor and 64 MiB schema-work budget follows accepted LD-C1A3-4 and snapshot_seal.rs:390-394; no additional requirement to charge its internal allocations to WorkScope is imposed here. That exception does not encompass the separate initial descriptor encoding. The id’s owned-record charge is appropriate. The kernel’s SHA-256 edge formula is a conservative block bound (not an exact block count for every residue); length checks and the body digest remain funded in the same scope.

2. **R2-NBO-1: resolved.** LD-C2A-1 now scopes row 8 to selection without new component-manifest admission or signature verification. Context re-admission, Run-closure admission, and retention/I/O failures retain their existing owners. The promised-object failure control preserves its actual post-draw cause, without not-installed relabelling or a second R10a refusal.

3. **R2-NBO-2: resolved.** LD-C2A-12 separates Component, constructed only after C2a-3 retention, from Core, constructed from authenticated InitialCore role projections. Core roles require no component catalog, delivery law or fixture root; the no-trust-view control preserves that distinction.

4. **Q5: applied.** D4/J1’s production profile, caps, aggregate pricing and Budget projection are a named C2a-4 gate. Helpers borrow the caller’s scope without per-component resets. Explicitly identified bounded test scopes do not establish a production profile.

5. **Q6: applied.** C2a-1, C2a-2 and pure C2a-3k can stage early without production authority. The bounded in-memory verification kernel confers no custody or admitted constructor. The production Component constructor waits for delivery custody; C2a-4 also waits for the production profile and D4. Synthetic inputs use the same kernel and ordinary trust path.

6. **No other regression identified.** C2PM-1’s authenticated declaration, ordered guards, exact protocol copy, role support and origin-sensitive public carriers remain explicit. Whole manifest/tree retention gates component admission; compiler and stdlib requirements remain intact. Admission still completes inside R10a/ER10a before the draw. The same-release platform join, field-use ownership matrix, joint fixture predicate, existing signer names/root, count/byte limits and X-8/ephemeral refusal limits remain preserved. The cross-law memo remains context, rather than accepted delivery authority.

Acceptance requires correcting the two published work prices and their corresponding control obligations. It does not require running a prohibited lane for this plan review.
