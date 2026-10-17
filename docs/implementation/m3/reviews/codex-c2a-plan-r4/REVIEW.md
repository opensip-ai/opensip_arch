# C2A-PLAN-r4 review

Verdict: **ACCEPT** — no required findings; two non-blocking observations. This accepts the implementation plan, not implementation code, delivery authority, production profile selection or qualification.

## Subject and verification

The manifest is 2,602 bytes, SHA-256 `a0da4eb0a9c4049eaec79acac6efcdd584a974d675f8a52b7413e9ffe32ab859`. All twelve members match their pinned lengths and hashes. PLAN-r4.md is 41,183 bytes, SHA-256 `dad5a9de3a5260d1df4c2f9059481435af7c4f5a19b359ff8af9695333bf7c88`. Historical plans, the input memo/gating context and both scratch evidence sets were rehashed.

Live product HEAD `3742822e2823c3a7624aca3fea11220a46cffa16` and architecture HEAD `ce872a5bb5ebf846a1870a66511e3cb9b1e63136` match the manifest bases. The cited canonical/digest/identity, sealing, native-context and work-ledger authorities inspected are byte-equal to round 3’s b753854 base. The intervening product commit changes only the C1a4 blind gate files.

Read the subject, prior findings, scratch source/logs and relevant existing encoder/sealing/schema source. No scratch program, Cargo, rustc, build, test, lane or network operation was run. No private fixture, installation directory, key/private test key, held tree, T2 store/cache, other pane or delegation was accessed. Neither repository was edited. Only the two requested review artifacts were written.

## Findings resolved

**R3-RF-1 resolved.** C2a no longer constructs a JsonValue descriptor tree for the first encoding. The selected owned projection is one exactly reserved Vec<BlobRef>, with borrowed path/digest and u64 length; its charge is one object plus n*sizeof(BlobRef), with visited-entry edges. Ordering owns only the two priced index buffers. The initial descriptor encoding owns exactly one Vec reserved at D, charged as one object and D bytes before allocation. The corrected size formula includes escaped UTF-8 payloads, decimal widths and separators; the 4 MiB check precedes buffer allocation. The stack digit writer handles zero and the maximum admitted widths without String, formatting macros or decimal heap temporaries. The scratch hand encoder writes keys in canonical order and uses the canonical escape rules, including raw UTF-8 for non-controls. No removed map/key/string/tree-array allocation remains necessary for this selected representation.

The counting allocator snapshots exclude construction of the comparison JsonValue and the later output printing. The pinned log reports 14 canonical_bytes allocation/reallocation calls for a four-Blob/six-integer descriptor, versus one hand-encoder allocation; output equality, length 683, prediction 683 and capacity 683 agree. Source inspection supports that one-buffer result. This is recorded scratch evidence, not a claim that product implementation/allocation controls have already run. The exact-funded and one-byte/object-short controls and allocation source pin remain appropriate implementation obligations. NBO-1 clarifies the distinction between the canonical test oracle and production invariants.

IdentityCandidate::from_json remains a separate admission step bounded by the descriptor and SCHEMA_BUDGET under the accepted C1a3 precedent. Its exception is explicitly limited to its own internals; it does not excuse initial encoding allocations. The separately owned closure2 identifier is charged. Borrowed trust evidence is not charged twice, and charges accumulate in the original caller’s scope across components.

**R3-RF-2 resolved.** The plan replaces sort_unstable_by with an explicitly deterministic bottom-up merge over indices. Each comparator invocation is preceded by a fallible edge charge; failure returns Budget before comparing, so the correctness of a global estimate is no longer the enforcement mechanism. Two u32 index buffers cost two objects and 2*n*sizeof(u32); the manifest’s 100,000-entry limit fits that index type. Adjacent duplicates are checked in a separately charged pass.

The reference bound n*ceil(log2 n) is conservative: there are ceil(log2 n) width-doubling passes, and each pass’s disjoint merges use at most n-1 comparisons in total. Actual charges follow the calls rather than consuming a fictitious worst-case number. The scratch uses usize indices to demonstrate the algorithm; the proposed product price correctly follows its chosen u32 representation. The pinned log reports reverse 20 at 40 comparisons within 100 and a maximum observed 44,749 comparisons over the listed reverse/sorted/interleaved/pseudo-random cases up to 4,097 entries. Its callback returns false before a comparison once funding is consumed. The recorded one-short control supports that mechanism. NBO-2 corrects the description of the old-estimate control and the empty-input notation.

## Non-blocking observations

### C2APLAN-R4-NBO-1 — Keep canonical equality in controls and the production invariant allocation-free

`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r4.md:119`.

The request and r4 change table describe equality with canonical_bytes as a control, which is consistent with the single-allocation encoder. LD-C2A-3 additionally says inequality produces an Internal refusal, which could be read as requiring a second production canonical_bytes encoding. That reading would rebuild the omitted JsonValue tree and reintroduce the allocations r4 removes. The C1a3 precedent instead checks the hand-encoded length against the prediction in production and uses canonical equality controls.

Suggested change: State explicitly that canonical_bytes equality is test-only and that the production Internal guard checks allocation-free invariants such as encoded length D. Keep the counting/equality oracle outside the funded production encoder. The recorded scratch vector exercises Unicode, quote, backslash, newline and a general control; retain the planned full vector controls for the other short escapes and the exact/one-short WorkScope tests rather than treating those as already demonstrated by the scratch log.

### C2APLAN-R4-NBO-2 — Distinguish a sufficient old estimate from a deliberately insufficient comparison allowance

`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r4.md:234`.

The new merge sort needs at most n*ceil(log2 n), which never exceeds r3’s n*ceil(log2(n+1)) estimate for n >= 2. A scope funding that entire old estimate therefore need not exhaust; reverse 20 uses only 40 comparisons while the old estimate funds 100. The scratch actually limits funding to min(old_estimate, actual_comparisons-1), so it demonstrates the one-comparison-short case, not exhaustion at the full old estimate. Precharging every actual comparator call is sound regardless.

Suggested change: Have the full-old-estimate control succeed without any unfunded comparison, and separately require actual_comparisons-1 funding to refuse Budget before the next comparison. Correct the sentence promising Budget for either case. Define the reference comparison bound as zero for n < 2 and duplicate-pass work as n.saturating_sub(1), covering the empty-tree helper case without underflow.

## No-regression disposition

No other regression identified from rounds 1–3. The corrected Blob/descriptor size formulas and byte/count distinction remain intact. C2PM-1’s authenticated declaration, exact protocol copy, ordered guards, role support and origin-sensitive routes remain explicit; no providerProtocol inference is introduced. The platform token still joins the selected manifest row to the same release’s artifact. The core-role field-use matrix and named consumer controls remain owned by C3/E/C4a/H/L/X12d, with the CRC mirror and symbol-inventory/candidate-result exclusions preserved.

A ClosureCandidate still grants no context, Plan or selection authority. Whole retained manifest/tree verification gates Component admission; the pure kernel grants no custody. Core admission remains an independent authenticated InitialCore branch, including the no-trust-view case. Component admission stays inside R10a/ER10a before the draw; row 8 adds no component-manifest admission or signature verification. Downstream context/Run re-admission and post-draw retention/I/O failures remain at their owners with their real causes. RTC/X-8 and ephemeral-detail limitations are preserved.

D4/J1 production work-profile selection remains a named C2a-4 gate. Early C2a-1/C2a-2/C2a-3k library work uses bounded test scopes and grants no production authority; the production constructor/wiring still waits for delivery custody and the named dependencies. Fixture construction preserves existing signer names/root and the exact joint predicate without adding a key or bypass. Required future tests, warning-denied Clippy, source pins, route reproduction and mutations remain stated obligations. This review performs none of those prohibited lanes and accepts no production component delivery.
