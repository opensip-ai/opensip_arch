# CODEX2 review: SYN-1 r2

**Verdict: ACCEPT-DESIGN-UNIT.** RF-SYN1-1 and NB-SYN1-1 are resolved. No required findings or new non-blocking observations.

This accepts the 12-member subject `docs/implementation/m3/syntax-e/syn-1-subject.json`, SHA-256 `4ed2d9ba30e825a6f738f39e3b92462e61268f3bef0c13894154f15aa64c9828`. The successor is `docs/implementation/m3/syntax-e/syn-1/successor.json`, 28228 bytes, SHA-256 `c1309a7cd091f062713671c3cbd5371797c87569dbd74f903935882cefce2f6c`. The lead's excluded unit draft is not part of the subject.

## RF-SYN1-1: resolved

The NE:3530 route row now refers to the exact emitted forms in the new NE:306 table. It no longer requires a colon suffix on every key. All 25 keys have a row: eleven unchanged model keys, thirteen E1 admission-chain keys and the unit's grammar-closure absence key.

The supplied content checker statically parses the literal emissions in NEM and both selected B-S9 copies. All eleven templates match, including the order and separators of the eight suffixed keys. The class mismatch remains `<languageId>:declared=<syntaxClass>:registered=<syntaxClass>`, with the declared value from the manifest row and registered value from the registry.

Exactly five keys are bare:

- `native.syntax-grammar-version-not-from-manifest`
- `native.syntax-grammar-bundle-not-in-closure`
- `native.syntax-normalizer-spec-not-in-closure`
- `native.syntax-grammar-closure-absent`
- `native.syntax-grammar-bundle-not-the-registry`

Manual inspection of E1 item 5, A3-A12 and the T-native paragraph confirms the chain subjects. The map-check alternatives, runtime pin, execution model, module validation, export, ABI and symbol-table subjects retain their meanings. Branch assignment is correct: nineteen keys on both branches, one selected T-native key and five inactive T-wasm keys.

The audit is sufficient for this static design review. It compares emitted templates rather than prefixes, requires complete key coverage, checks the bare set, and reproduces `key-forms.json`. Its global law-spelling guard is supplemented here by reading each corresponding admission-chain row in context. No model was imported or executed. The lead's mutation probes were not rerun; the exact equality guards that reject those changes were inspected.

## LD-13 and LD-14

The bare absence key is appropriate when no grammar closure is installed and no descriptor or closure id exists. A named but unretained, malformed, misidentified or wrongly kinded closure is a distinct native-context refusal. NEM's `retained()` receives the location subject `grammarBundle.closureId`; the absence key does not replace that case.

The table's placement in §1.2 is sound: it sits beside the context checks, and the §10 route row points to it without breaking the route table or its final exit rule.

The fixed tokens refine E1's open subjects without changing its checks. A5's five field names match E1:247. A8 covers engine identity, limit names and runtime compatibility (E1:250). The four compiled-table comparison fields match E1:257; `linked-symbol-table` distinguishes E1:259's separate recomputation. Fixed member paths and `<treePath>` distinguish actual member names from the literal `path` check word. The normalizer `<name>` scope preserves the previously disclosed E-7 widening.

README O-1 records an inherited NE/J1 enumeration gap for two native-context keys. The original NE:3530 text and model bytes are unchanged. That remains the named owners' follow-up and introduces no new required change to this amendment.

## NB-SYN1-1 and unchanged parts

The no-group wording is the exact replacement offered in r1. An empty census has empty `examinedPaths`, `groupDigests` and `sourceBodies`. A successful no-group result over a nonempty census retains `examinedPaths` equal to that census and empties only the two group/body arrays.

The diff confirms five changed members, six unchanged members and one new evidence member. Both JSON copies, the materialization map, copies report, verifier and law snapshot remain byte-identical to r1. The record retains its standing, parents, selectors and all five `before` strings. Only two `after` strings change: NE:306 gets the exact NB replacement and appended table; NE:3530 gets its new form-reference sentence. The other three `after` strings are unchanged. Candidate pins and the new evidence member are the corresponding record changes.

## Validation and scope

All 34 supplied pins and all 12 subject members matched. The reviewed subject is also preserved under this directory's `reviewed-subject/`. Local supporting evidence is `pin-audit.json`, `r1-r2.diff` and `amendment-audit.json`.

Each allowed check ran once:

| Check | Result | Log |
|---|---|---|
| Builder with `--check` | Identical; five overrides, eleven candidates | `build-check.log` |
| Content checker with product path | Pass; 25 forms, three model copies, five bare keys | `content-check.log` |
| Scratch verifier at `392499e` | Pass; 83 to 84 | `verify-current-base.log` |
| Scratch chain at `392499e` | Pass; 83 to 86 | `verify-chain.log` |
| Scratch verifier at `cd5958b` | Pass; 82 to 83 | `verify-build-base.log` |
| Scratch verifier on checkout | Pass; 83 to 84; 40 generation sources, 48 admission sources, 15 aliases | `verify-checkout.log` |

Only `design-lock.json` changed between the build base `cd5958b` and review base `392499e3a42ab9f45d517b8c267a83031abf3863`. The native schema source and verifier are byte-identical. The harness preserves selected inventory and inheritance, and reports five SYN-1 overrides without supersession. Its reviews and assents are synthetic; actual root assent and binding remain the lead's steps. Chain well-formedness is evidence about composition, not an acceptance verdict on SYN-1F or SYN-NS.

Repositories remained read-only. No delegation, cargo, builds, tests, crash-matrix command, native-model import/execution or commit occurred. Commands ran at `nice -n 19`, with the requested Python interpreter and `-I -B`. Every write is confined to this review directory; neither protected home nor the private 413 fixture was accessed.
