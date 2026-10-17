# SD-9-r2 review

**Verdict: ACCEPT-DESIGN-UNIT.** SD9-R1-RF-1 and SD9-R1-RF-2 are resolved. No required findings or non-blocking observations. The reworded Q-SD9-3 is accepted as ruled below. This accepts the law record and its explicit policy; it does not complete the census, production wiring, assent or cross-law incorporation.

## Subject and evidence

Verified the 1,769-byte manifest, SHA-256 `b0ce2d27c78b12d8464bda9f82fa5dbe2f8cddc78946206d1069b06fc7ae2a1f`, and all four current member pins:

- sd-9-r2/README.md: 32,785 bytes, `23f249f24b248bab612f787f0e4f54998def07a43b9cf7cf44daff3cbe2a2977`.
- evidence/build_sd9.py: 4,538 bytes, `4b506bd182025a5d55f652f8ad49f48d6bc8a2522529fb598019bb8eb417d509`.
- evidence/check_sd9.output.json: 9,175 bytes, `e4d73a7ce2496046a8ad2b57ade1ab3cfb2b1e71b99f8048d4c3de5ece0c9f67`.
- evidence/check_sd9.py: 14,079 bytes, `539f7d14824a436bd9745ea82f8085e8ad25229bff4bd98fe885271959e8528f`.

Verified all four prior-round entries as well. The copied r1 REQUEST, REVIEW.md and review.json match their original /tmp review bytes exactly; the pinned r1 manifest remains `de7db21190f3d9b1d2c2d1e5f062f179843f2a09bcb418f25d7b7b1c9aabaf4a`.

Ran the three expressly permitted checks. The r2 checker's output matches its archive byte for byte, r2 build_sd9.py --check passes, and r1 build_sd9.py --check still passes. The r1 package is unchanged. Product revision remains `274dccc5eced53828f444fa44e62cdeffabc2d0c`; the builder validates architecture base `c6c7d4acf0d4836ef3bb72cb2bcb8950a75530a2`. The draft unit records compared by the builders are not subject members or accepted assent artifacts.

Compared both READMEs and both pairs of scripts. All authority hashes, product-source hashes, extracted prices and numeric model results are unchanged. The checker changes describe the partial subtotal and rename output keys; its cost formula and search are unchanged. Builder changes select the r2 paths, pin the prior review/manifest and record the new gates and outcome policy. No unrelated operative ledger/profile/projection change was introduced.

## SD9-R1-RF-1 — resolved

Section 5 now separates two operations that r1 conflated: deriving d_x by the exact minimum-power rule, and selecting the existing or new profile under an explicit retention policy. Each census records m_x and d_x; reused-policy outcome V also records i_x.

The three outcomes are exhaustive and mutually exclusive:

- E: all three derived coordinates equal the interim. The existing constructor is exactly census-derived.
- V: every derived coordinate is at most the interim, with at least one strict inequality. The constructor is retained as census-validated reused policy, explicitly never as census-derived.
- N: any derived coordinate exceeds the interim, regardless of the others. A new constructor uses all three exact derived coordinates; no per-coordinate mixing is allowed.

For V, i_x >= d_x >= 2*m_x establishes the required margin on every coordinate of the complete censused population. It does not establish that i_x is the smallest qualifying power of two, and the record no longer says it does. This resolves the original contradiction through the explicitly offered alternate-policy path rather than silently redefining derivation.

The landing table, X-SD9-1's three terminal outcomes, draft-record source labels and SD9-T6 agree. Equal, all-below, mixed equal/below, mixed one-above and all-above cases are covered. N carries the receipt-specific census-batch consequence of changing work_ledger.rs; E/V avoid that constructor edit. All outcomes require revalidation for a new first-party release or changed owner bound.

**Ruling on reworded Q-SD9-3: accepted.** LD-S9-RF1 is a coherent, distinct, reviewed retention rule for this admission ledger. R9's exact derivation remains the source of d_x and of the existing snapshot profile; it is not changed for the snapshot ledger. SD-9 explicitly selects the additional policy of retaining that already reviewed finite profile for R10a/ER10a when the complete census proves its margin. Thus V does not conflict with R9 provided every downstream record preserves its census-validated-reuse standing. X-CI-1 supports the precedent for cross-ledger reuse; it does not itself authorize indefinite reuse, which is why this review expressly accepts SD-9's separate rule. The equality-only alternative is not required.

This ruling applies to SD-9. It does not silently amend X-CI-1's separately owned final installation-profile rule merely because the two censuses may share a population and batch.

## SD9-R1-RF-2 — resolved

The numerical evidence is now consistently an edge-only boundary of S(c) = C2a1(c) + B_open(c) + T(c) + K(c), for a single illustrative component. The object counts are partial and no byte coordinate is computed. The arbitrary-aggregate size claim, all-coordinate fit claim and unsupported full-admission capacity have been removed. Statements distinguishing conservative bounds from actual comparison charges prevent interpreting the subtotal boundary as an exact executed admission threshold.

The revised output reproduces r1's snapshot subtotal boundaries: 1,069,536,384; 1,064,704,785; 1,010,568,235; and 796,181,735 bytes. Partial object counts remain 19; 6,319; 93,119; and 612,019. Kernel shares remain 99.61%, 99.19%, 94.50% and 75.62% of the subtotal. The renamed keys and model standing accurately limit those numbers. No new cap is introduced.

M remains owed to C2a-3 and now includes the reviewed representation's allocations, owned keys/slices, insertion and comparison work without imposing a minimum allocation shape. X-SD9-2 separately requires priced M, final accepted/revalidated CI bounds and implemented D4 bounds before a complete A(Sigma) census or production fit claim. Accepting the interim does not satisfy that completion gate.

The controls now address the original validation requirements: T2 independently enumerates executed charges and compares them with conservative bounds; T3 includes D4-2 and M exhaustion; T4 waits for the complete three-coordinate model; T4b demonstrates why a subtotal fit does not establish admission; and multi-component exhaustion drops earlier capabilities and exposes no partial admitted set. When implementing the over-limit controls, use actual executed work or a fixture known to attain the relevant bound: exceeding a conservative bound allowance alone must not be treated as proof that an actual run exhausted it. T2's distinction remains applicable to those controls.

## Carried rulings, scope and remaining work

R1's accepted policy and ownership rulings remain intact. R10a and ER10a each own one non-replaced admission ledger; the trust-read budget remains separate. D4 work is counted once per admitted set, component work across the whole set. Later launch rechecks and Run retention remain on their owners' ledgers. Exhaustion retains typed Budget until J2 projects existing row 11, including the pre-attempt ephemeral operational envelope; no corruption, missing/not-installed or excluded-form projection is substituted.

The revised controls inspect the actual failure envelope and preserve J-C10b's reservation property on durable 3a, all first-use 3b outcomes and ER10a. Successful sub-step capabilities remain private until complete admission and are dropped on failure. The no-pre-bound explanation is explicitly qualified as the selected policy. The provisional transfer/map/kernel shape still authorizes no streaming-interface change or omitted verification.

The unchanged snapshot_profile caps remain explicit interim policy, not census coverage. Production qualification/use still waits for X-SD9-1 after X-SD9-2, with exactly one recorded E/V/N outcome. C2a-3 owes its representation and price; CI/D4 final bounds must be revalidated; the complete census and wiring controls remain unexecuted. Root assent and J1/M3-D incorporation remain owed. None is supplied by this design acceptance or by successful package checks.

Only REVIEW.md and review.json were written in the requested directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build or lane was run and the lane lock was not taken. No network, prohibited fixture/key/installation material, held trees or entries, T2 store/overlay/cache, other pane or delegation was used. Only the three expressly permitted project checks were executed.
