I recommend **ACCEPT** for source42 at source level. There is no MUST, no SHOULD and no blocker. Source40's S40-01 and ADV40-01 are both resolved, and I found one new advisory that doesn't block. No application, readiness, blind reconstruction or product qualification is granted.

**Custody (measured before I set `verifiedManifest`).** Source42 manifest `f602fc7e…` and archive `2423c780…` match the header. All 12,913 members check out, 737,766,584 bytes in total. Parent41 (`eb7a4c48…`, 12,912 members) and last-reviewed40 (`3be45284…`, 12,911) are unchanged, and the declared chain 42→41→40 holds. The deltas are 16 changed and 1 added from v41, and 16 changed and 2 added from v40. All four working copies re-verified unchanged at the end.

**S40-01 resolved, including the capture follow-on.** Execution-inputs contract §3 now publishes the attribution rule, and §8 plus the model require receipts to capture the explicit returned views. I ran each tree's own code in its own process on v40, v41 and v42, closing full Runs on the same manifests (26/26):
- **Foreign scope named by an unsupported row's view:** v40 admits and closes it; v41 and v42 refuse (`COVERAGE_DERIVE`) at admission and in the Run. That is the existing §3 law, now enforced.
- **Returned view that no row owns:** the v40/41 builders dropped it and the Run failed. v42 captures it on no row and closes.
- **Receipt reminted to drop a selected view:** v40/41 admit and close it; v42 refuses (`SELECTED_COVER`).
- **One view shared by two capability cells on the same program:** it lands on both rows, with identical bytes and RunId on every tree.
- **Newly chosen deterministic rule:** universe and relation must sit on the same scope. A view with them on different scopes gets a new digest under v42. This is a published identity change, not the same observation admitted twice.
- **History:** each tree's own checker gives 76 → 86 → 95 execution-inputs cases and 46 → 54 enumeration cases, 0 mismatches. Every shared case is field-identical across trees, with equal RunIds.

**programEntry.** The clarification is consistent with the schema and the native entry law. The enforcement is confirmed at the enumeration owner, which Run closure calls (24 cases, v41 vs v42):
- **Now refused:** an explicit null entry in ts-tsconfig, js-allowjs or js-synthesized mode, with exactly `ENUMERATION_BINDING_PROGRAM_ENTRY`.
- **Unchanged:** defaults, explicit marker and build-config selections, Rust, syntax, and every unavailable binding.
- **Contract wording:** the text naming programEntry as an input to all three native binders is imprecise, but the construction table right after it settles it. It is not a material ambiguity.

**ADV42-01 (advisory).** Admission never checks that a receipt's views carry that receipt's producer.
- **Measured:** a captured view with a non-provider producer, even with a foreign planId, passes admission on all three trees. Only Run closure refuses it (`CLOSURE_FIELD_KIND`), so none of the measured shapes closes a Run.
- **Unexercised:** a Plan with two providers, where one provider's view is listed on the other's receipt. No maintained fixture has two providers, so I couldn't build it.
- **Why not a SHOULD:** it predates v40, no admitted Run was demonstrated, and the TCB is unchanged.

**Other scope.**
- **ADV40-01:** resolved; planning v8's bytes are preserved and now explicitly marked as history.
- **Closing digest law scope:** explicit enough; no clarification needed.
- **Composition §7 and policy-derivation3:** my source40 no-gap findings stand on unchanged bytes.
- **Pinned groups:** all six pass, as do all 17 evaluator children. Group output is byte-equal to the codex final-reference.v42 and root v3 runs. Two children differ from them only in path fields.
- **Planning:** 322 mappings, 198 paths in 20 packages, M0–M6, 54 recovery cases.
- **Package 19:** verified as author evidence, rebuilt from package15 plus the native-v2 overlay. The four TypeScript map negatives are executed.
- **Ported source40 probes:** all pass on v42.

**107 disposition rows.** Each has its own text, current owner and consequence; 36 rest on new source42 work and 71 on a quoted source40 basis. TCB-SCOPE-01 is assessed once, with 13 dependents. Still open:
- All 30 grades and 28 condition-2 obligations pending final application.
- 32 gates and 54 recovery cases unperformed; condition 5 not met.
- The D9 successor carried as a future obligation.
- Final application needs a new, different Claude origin.

**Limitations.**
- **Failed attempt:** the first programEntry probe run failed on my own harness, because the receipts directory didn't exist yet. It is preserved and not counted.
- **Not independently probed:** candidate-only attribution and the relation-column rule rest on reading plus unchanged shared checker cases.
- **Not re-closed:** explicit-null programEntry cases were tested at owner admission, not as independent full Runs.

Files are in `/private/tmp/opensip-design-corrections/claude-independent-design.v42`:
- review.md
- review.json
