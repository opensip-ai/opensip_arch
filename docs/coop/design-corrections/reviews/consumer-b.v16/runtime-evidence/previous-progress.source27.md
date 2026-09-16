I've completed the required normative audit and re-bound everything to the new kit. Here is where this continuation stands.

## Input custody (v15)

- `consumer-input-manifest.json` SHA-256 measured **73f9c13e…7da7c4** = declared; parent **a1ae88ef…0227a** = declared; **101/101 files byte-exact**, no extras, none missing. This verifies the *disclosed* kit only — not a claim to hold the complete candidate.
- Kit delta vs the prior disclosed kit: **10 changed, 0 added, 0 removed**. The ones that changed my reconstruction: the new `x-opensip-digest-domains.scope` clause (+ matching §3 wording), and `logicalPath` must now also be null when `kind=unknown` (atom contract + both attribution schemas).
- Helper paths rebound to v15 with the complete pre-rebind tree preserved at `output/lib.before-image.v14/`; a guard asserts **0 residual prior-path references**. Content-bearing labels (capability-manifest `profile`) were rebound too, so new identities are bound to this kit rather than silently reproducing a prior identity.

## The audit found four real defects in my own prior work

The continuation instruction's pointer was correct — *global blob retention and closure-tree membership are different obligations*, and my prior pass satisfied only the first:

1. **V15-D1** — grammar bundle manifest, every grammar definition and the normalizer specification were globally retained but **not members of the selected `kind=grammar` closure tree**. Measured: 5 × `native-evidence-1.2:PRESENT_IN_THE_RETAINED_TREE` with `globallyRetainedInCas: true`.
2. **V15-D2** — Rust `standardLibraryComponentDigests[].sha256` were not members of the closure named by `rustcDevLlvmDigest`, despite `retention: closure-tree-member`.
3. **V15-D3** — *root cause*: my schema walker replaced a `$ref` with its target and **discarded sibling keywords**, so most annotated native sites were invisible (1 site reached on `TypeScriptNativeContextV2` instead of 9). That is why the prior pass never exercised these joins at all.
4. **V15-D4** — my TypeScript Run declared `ts-tsconfig` while carrying `allowJs=true` and a `.js` program root; §1.2 makes that `js-allowjs`. Corrected across context, universe, `WorkspaceUnitV2` and every enumeration cell.

All four are **reconstruction defects, not normative ambiguity**, and the original failing output is preserved in `progress.v15.json`.

Two genuine normative observations: `x-opensip-digest-law.retention` declares four members but three of its own sites use `derived` (SHOULD), and `sites: 68` against 76 measured (advisory).

## Current measured state

Five complete positive Runs (syntax-code, typescript, rust, rust-partial, syntax-data), each: schema + published-keyword admission → retained closure **0 refusals** → whole-store export → **fresh-process replay byte-match** → 14 tamper/identity controls refused. Plus **22 native-join negative controls** (each reminting and reclosing the entire graph) and **17 protocol traces** reaching all five declared terminal kinds.

Two honest masking notes: the `stdlibMerkleRoot-wrong-kind` mutation refuses first at the tree-member join, and the direct-member control refuses first at `STAGE_SPEC_PRODUCER_PLAN_SELECTED` because one provider closure is the direct member for several roles.

## Not yet executed

Phases **6, 7, 8, 10, 11** entirely; `R-HIDDEN-MISMATCH-PER-LANGUAGE`; `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`; Phase 4 is mid-flight. `blind-review.md`/`.json` are not written yet — I will not write a verdict while that much required scope is outstanding. No root admission or agreement is claimed anywhere.
