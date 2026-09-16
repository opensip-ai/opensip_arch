# Independent Grok review: native-runtime-selection v3

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Verdict: ACCEPT-DESIGN-UNIT**
**subjectManifestSha256:** `ccbdcfef1998a6e87ed38bfbfb23a61ddd220a0e6b906a9201ee110b30c5c30e`
**requiredFindings:** none

Selector-packaging correction of uninstalled v2. Same 35 owned runtime inputs, same dependency TCB, same frozen runtime-02 export and isolation evidence. **Not** complete M2, native execution, universe/Plan/Run/replay, or release. V2 review and root assent remain historical; v2 was **not** selected because private activation refused before any live source or lock write. This verdict does not itself activate v3.

## Custody

| Manifest | Bytes | SHA-256 | Members |
| --- | ---: | --- | ---: |
| Selection `native-runtime-selection-v3-subject.json` | 25474 | `ccbdcfef…c30e` | **112/112** |
| Reused v2 candidates | 109 | byte-identical | subset of v3 |
| New account docs | 2 | README + `activation-correction.json` | plus new successor |
| Implementation (unchanged v2 export) | 46356 / 254 files | `68a9e7b6…9d08` | not rewritten |

Successor candidates **111** = subject files minus `successor.json`. Overlap with v2 subject: **109** files unchanged; v2 successor is **not** a v3 candidate. `previousCandidate` pins v2 subject `6a761425…0a97`. Materialization map **35/35** still pinned as v3 candidates (v2 custody paths). Live lock **10/15** `e1282724…9f0d` unchanged; neither v2 nor v3 successor is in it.

Work stayed under `/tmp/opensip-implementation/m2-grok-native-runtime-selection-v3-review/review`. Frozen/live/history not edited.

## Parent-selection mechanism (the actual v2 refusal)

`verify_design.successor_chain` (frozen runtime-02 checker, unchanged):

- Inventory successors add **candidate** inventory bytes to the contract accepted-parent set (`repository-file-inventory.v12.json`).
- They do **not** add the inventory **successor record** (`native-owners-inventory-v12/successor.json`).
- Contract successors add their own successor record plus that unit’s candidate inputs.
- `contract_successor` then requires every `parents[]` row `path/bytes/sha256` to equal an accepted base or selected inventory.

Private activation stderr (90 bytes `26baf62f…db77`), after v2 formal review and root assent, before any live write:

`Design verification failed: contract parent is not an accepted base or selected inventory`

Independently reconstructed the live accepted-parent set (10 inventory candidates + 15 contract records and their candidate inputs). Against that set:

| Parent | Live class | v2 | v3 |
| --- | --- | --- | --- |
| `admission-runtime-selection-v1/successor.json` | contract record | match | match |
| `capability-totality-reference-selection-v1/successor.json` | contract record | match | match |
| `exact-schema-profile-selection-v1/successor.json` | contract record | match | match |
| `recognition-derived-reference-selection-v1/successor.json` | contract record | match | match |
| `repository-file-inventory.v12.json` | inventory **candidate** | match | match |
| `native-owners-inventory-v12/successor.json` | inventory **record** | **MISSING** | **removed** |

v3 parents are sorted unique, count **5**, all exact live matches. No passage overrides. This is a selector correction, not a verifier bypass.

Did **not** fabricate a 16th live contract binding, review, or assent. Parent-membership simulation uses the real `contract_successor` predicate only.

## Source-byte equivalence

All 109 v2 candidate pins are present in v3 with identical path/bytes/sha256, including:

- 35-file materialization map and every mapped product input
- identity TCB policy `58399e31…`, unicode-15 tables/generator/raw UCD, capability/plan/context/case owners
- implementation-subject `68a9e7b6…` (254-member export)
- host/provider isolation receipts and preflight evidence

No frozen runtime-02 rewrite. No live product or lock change. TCB accept remains the v2-reviewed exact three packages; this unit does not reopen Hangul/memory-safety as a new claim.

## Limits (not waived)

Same runtime-02 bounds: not complete M2, native execution, universe/Plan/Run/replay, Syntax-10, custody/publication, or signed release. Hangul TCB is still bounded exact-bytes accept, not a memory-safety proof. Root continuing the Rust binder is out of this unit. After this review, root assent and **private activation of v3** (appending this successor as the 16th contract against live 10/15) remain separate; do not treat this verdict as that activation.

94 workspace tests and 07–09 corpora were **not** rerun: those bytes are unchanged from the v2 review.

## requiredFindings

[]
