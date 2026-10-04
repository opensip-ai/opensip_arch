# CODEX2 review — SYN-1 r1

**REQUIRED-FINDINGS** — one required finding and one non-blocking observation.

The outcome law, ERROR exception, schema copies and structural binding check out. The new route's universal subject requirement contradicts the unchanged native-model emissions and needs correction before acceptance.

Reviewed subject: `1e4d8b3bf3f5d5613eebb37893fc80f7a952aec9ac201d33b077a9c2993b0da4`, 11 members.

Successor: `docs/implementation/m3/syntax-e/syn-1/successor.json`, 19863 bytes, `b9da5c6d510f19c180227453d95a08fb4ad83cbb0ba45a1cc15a828639eb1dd8`. The excluded lead draft `syn-1-unit.json` is not accepted by this review.

## RF-SYN1-1 — Preserve the existing key subject forms

Location: the NE:3530 candidate row, `PASSAGES.md:92`, `successor.json /passageOverrides/3/after`, and the builder's `NE3530` string.

The row says:

~~~text
Each key carries its colon-suffixed subject, and the refusals are one sorted set.
~~~

Both frozen NEM and the selected B-S9 reference emit these three keys **without a subject suffix** at lines 2435, 2437 and 2442:

- `native.syntax-grammar-version-not-from-manifest`
- `native.syntax-grammar-bundle-not-in-closure`
- `native.syntax-normalizer-spec-not-in-closure`

For example, a grammar closure whose semantic version differs from the bundle's `parserVersion` produces the first bare key. Its output cannot satisfy the new universal colon-subject requirement while LD-6 preserves the native-model bytes. The newly added missing-closure key has no specified subject value either. The content checker proves the 25 prefixes, but does not compare their emitted subject forms. These observations come from source and AST inspection; no model was executed.

Keep the existing emissions, and replace the quoted sentence exactly with:

~~~text
Keys retain their defined subject form: existing §1.2 keys are unchanged, and item 5's admission-chain keys use that item's subjects where specified. `native.syntax-grammar-closure-absent` is emitted without a subject suffix. The refusals are one sorted set.
~~~

Carry that replacement through the builder, passages and record, refresh the subject pins, and include a read-only comparison of the inherited bare/suffixed forms. This repair leaves the key set, branch split, public route and NEM logic unchanged.

## NB-SYN1-1 — Name the empty arrays in the no-group case

`PASSAGES.md:52` says an explicit empty census and a successful no-group result are complete with empty arrays. For a nonempty census that parses successfully but yields no groups, `examinedPaths` must still equal the census; only `groupDigests` and `sourceBodies` are empty. E1 item 14a states that distinction, and EXM:1499-1503 refuses a complete envelope whose examined paths differ from its extent.

This is non-blocking because the preceding sentence and later parsed-path rule already require the right `examinedPaths`. Replace this exact fragment:

~~~text
An explicit `[]` census, and a successful result with no group, are `complete` with empty arrays;
~~~

with:

~~~text
An explicit `[]` census is `complete` with `examinedPaths: []`, `groupDigests: []` and `sourceBodies: []`. A successful result with no group is `complete` with `examinedPaths` equal to the census, `groupDigests: []` and `sourceBodies: []`;
~~~

## Requested decisions

1. **Outcome law:** the four outcomes, whole-file rule, no byte rewriting, Coverage precedence, owed-but-unexamined clone bodies, typed bounds and native crash residual match E1 items 10, 11 and 18. The wasm-only memory/trap/module behavior is marked inactive. The `clones-near` result is a candidate envelope with no Coverage; its parsed-only paths, partial pairs, unsupported census case, no-envelope fault/cancellation rule and whole-group retention match item 14a. The retention prefix includes the 100,000 distinct-body limit. NB-SYN1-1 clarifies the successful empty-result wording. E2a appropriately owns the byte layout.
2. **ERROR:** LD-2 is sound. The pinned runtime defines `ts_node_is_error` exactly as `ts_node_symbol == ts_builtin_sym_error` (`node.c:524-526`). The reserved values are 65535 and 65534; runtime metadata makes ERROR visible and ERROR_REPEAT hidden (`language.c:219-222`). The Rust binding's ids ≥65534 exception permits reserved lookup, not visible ERROR_REPEAT nodes (`binding_rust/lib.rs:629-630`). All five inspected upstream files match E0's pins. E0 reports 8,351 identical native/wasm trees, two independently written serializers, and 41 syntax-error files. This is sufficient support for the reserved-symbol decision; E2b still must enforce both directions of flag agreement. E0 is not production qualification.
3. **Keys:** all 25 prefixes are present: eleven existing keys, thirteen E1 admission-chain keys, and the new closure-absence key. The normalization-map key correctly fills item 19's omitted listing. Seven chain keys apply to both branches, one build-mismatch key to native, and five module/ABI/symbol-table keys to inactive wasm. Pre-Plan `request-rejected` / `REQUEST.PRECONDITION_FAILED` routing is correct, and absence of an entire closure deserves its own key. RF-SYN1-1 fixes the subject-format inconsistency.
4. **Backend fault:** the row uses the accepted host-invariant composition: `operational-failed` / 4 / `SYSTEM.OUTCOME.ILLEGAL_STATE`, detail `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>`. No Coverage, candidate envelope or Run follows; no backend retry occurs. Native abort, stack overflow and allocation failure remain declared untyped process-loss risks. X-J1 is the correct owner route: widen row 52 at J-ε and add the backend-fault row before `outcomes.rs` projects these conditions. Unregistered native keys stay in the operational record with no new public detail code.
5. **Copies and (f):** each copy differs only by the two ordered `source-parse-error` insertions and the registry-rule restatement. The design/product relation is preserved, and the product parent equals the pinned product source. No bound JSON override is lost. Other cause lists, descriptions, deficiencies, unavailability reasons and startup bytes remain unchanged. Startup's terminal reason sets are separate; its Coverage entries reference the native schema owner by URN. Joint binding and E2s materialization with SYN-1F preserve the foundation mirrors.
6. **NEM:** no logic change is required for the cause itself: the model reads the cause registry as data, and its D9 map does not attempt total coverage of the native-context admission keys. The new execution joins belong to E2b. A byte-identical model successor would add no behavior. RF-SYN1-1 removes the output-format requirement that conflicts with the retained emissions. Runnable reference assembly must supply the selected schema data; no NEM import or execution was performed here.
7. **Selection:** the record has three exact accepted parents, five free line selectors, ten candidates and eleven subject members. The law snapshot is eligible as a candidate. Real scratch verification passes alone and in the proposed chain, preserving inventory and inheritance. Standalone verification proves structural eligibility only: actual binding still requires SYN-1F jointly, CRC-1 beforehand if unbound, real independent review and root assent. This review gives no verdict on the sibling units.

## Validation and boundaries

All 22 request pins and 11 subject members matched initially and again before writing the verdict. Product HEAD remained `cd5958b3608f44a0035566c9d4500e5005c62e91`.

The supplied build `--check` and independent content checker passed. Scratch verification passed at `cd5958b` alone (82 → 83), in the order SYN-1 / CRC-1 / SYN-1F / SYN-NS (82 → 86), and on the current checkout (82 → 83). The checkout run verified 40 generation sources, 48 admission sources and 15 aliases without executing generators or runtime code. All five command stderr files are empty.

Evidence is saved here in `input-checks.json`, `build-check.json`, `content-check.json`, `verify-base.json`, `verify-chain.json`, `verify-current.json`, `supplemental-source-audit.json` and `final-pin-audit.json`.

Repository access was read-only. All commands ran at nice 19, with Python `-I -B`. Only the supplied evidence scripts ran, plus read-only inspection and review-file writes; the authorized scratch verifier was the only executed product tool, using an in-memory lock, review and assent. No cargo, builds, tests, generators, crash-matrix command, NEM/native checker execution, delegation, repository edits or commits. All writes are under this review directory. The actual OpenSIP home and private 413 UUID fixture were not accessed.
