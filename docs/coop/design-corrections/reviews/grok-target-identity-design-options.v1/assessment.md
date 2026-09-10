I'll start by reading the design-session inputs, the independent P4 finding, and the relevant design skill so the option comparison is grounded in the actual gap.The session is a coauthor draft, not the design-skill subagent loop. Next I’ll verify the input and source manifests, then read P4’s finding and the live identity/target laws.Input manifest matches. I’ll verify source24 next and read the identity, payload, attribution, and evaluation contracts that own this join.I’ll stay in source24’s current design/schema/reference trees and skip other-session helpers while locating the source manifest SHA.I’ll compute the current source manifest from source24 itself, then read the owning identity/payload/attribution contracts.I’ll read the matching, projection, inventory, and execution-input owners next so the option comparison can name exact successor joins.Pins match on the owning contracts. I’ll draft the option comparison and successor proposal from those laws, including the schema-admitted controls Codex needs next.Recommended correction: **Option B** — a versioned TargetAttribution sidecar that attests evaluation occupancy, not a payload rewrite and not a withdrawal of FILE/PACKAGE targets.

The gap is real: ordinary first-party file/package identities are path / packageName, while `ImportsPayloadV1.resolvedTarget` is opaque `SubjectIdV1` and native-id-first compare cannot occupy those inventory subjects. External occupancy remains lawful and is not enough. P4 C14 stays a stipulated complete-sufficiency construction, not an executed full-Run false result. A schema-admitted positive can prove representability without claiming extraction truth.

Independent comparison:

| Option | Verdict |
|---|---|
| **B** (refined P4 O4): provider-attested evaluation occupancy on TargetAttributionV2 | **Recommended.** Smallest coherent *join* between two already-lawful grammars. |
| **A** (P4 O3): kind-discriminated payload endpoint identity | Coherent competitor. Simplifies compare, remints every imports `fact2`, drops payload opacity, breaks current payload-isolation. |
| **C** (P4 O2): inventory native ids become SubjectIdV1 | Rejected. Breaks unary file/package source identities. |
| **D** (P4 O1): withdraw FILE/PACKAGE from `imports.targetKinds` | Not preferred. Contradicts portable file/package incoming analysis. |

Codex’s preference to keep portable inventory identities and avoid host namespace parsing is treated as a preference, not a requirement. Option B coincides with it for independent reasons: the defect is the join, not either grammar.

Concrete B draft:

- Keep payload `SubjectIdV1` and inventory path/packageName.
- Add `evaluationNativeId` on **TargetAttributionV2**. Do **not** reuse `logicalPath` or reverse null-on-first-party.
- `endpoint=target` matching compares occupancy identity to `E`, not payload string to `E`.
- First-party graph targets project onto inventory vertices; external targets keep opaque payload ids; no alias records.
- Host validates unique inventory match; it does not parse `file:` / `package:`, guess, or cache positive occupancy.
- V1 Runs keep V1 compare/projection. Successor schema/profile pins are required; deployed compatibility is not invented.

Required controls include schema-admitted FILE `src/lib/util.ts` ← `file:src/lib/util.ts` and PACKAGE `demo-app`+`package.json` ← `package:demo-app` positives, plus symbol/external/unknown/C15/N1–N14 refusals. Current `check-atoms` `resolvedTarget: "src/a.ts"` is a schema-invalid bypass and is not a positive.

Delivered (design draft only; source24 untouched; not acceptance or implementation-ready):

- `target-identity-design-options.md`
- `target-identity-design-options.json`
