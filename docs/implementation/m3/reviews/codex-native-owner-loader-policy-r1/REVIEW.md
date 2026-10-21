# Review: native-owner generator loader policy r1

**Verdict: ACCEPT-DESIGN-UNIT**

This verdict accepts only the frozen pure policy-data successor. It does not accept materialization code, helper installation, checker results, generated outputs, blind refresh, or product qualification.

The subject manifest has the requested SHA-256 (`9db286689839d22ef19260fca36f7a20978dce68d65e851d6f7c3cae7335ea16`). All five declared members match their sizes and digests, the staged file set is exact, the successor's four candidates exactly equal the manifest members other than the successor, and `passageOverrides` is empty. The evidence manifest and all three evidence members also rehash exactly.

The product and architecture repositories remain at the requested bases `19549dcb29c1e2c77f53419f18db8d0c451259aa` and `62ec9231b0d4d04a68c3f67698484bae78f123a5`, with no tracked changes. All three parent bytes rehash exactly through the current product design lock: the loader policy is an accepted contract 5 member, the typed registry is an accepted contract 96 member, and the generator closure is an accepted current contract 180 member. Each corresponding record, subject, review, and assent pin also rehashes.

## Required findings

None.

## Verified design

- The loader policy retains exactly 11 unique file rows. Relative to the accepted M1 parent, its only differences are the `bytes` and `sha256` values for `tools/contracts/package.json`, `tools/contracts/runtime/patterns.ts`, and `tools/contracts/runtime/schema.ts`. Paths, order, schema version, kind, and every other field are unchanged.
- Every candidate policy row joins exactly by path, byte length, and SHA-256 to the accepted 352-row contract 180 generator closure. This includes the eight unchanged rows and all three refreshed rows.
- The lane record is value-equal to its parent. All three `trustedUsages` rows are value-equal in full, including kind, file, digest, line, column, spelling, reason, request/mode where present, and target list. The sole `unfollowedDynamicLoaders` row is also value-equal. No loader, target, exception, call site, compiler pin, position, spelling, capability, or limitation changes.
- The prospective `tools/typescript-lanes.json` differs from accepted F8c at exactly one value: the generator lane's `toolPolicy` points to this new immutable policy path. Its 160 file pins, Node byte/digest pin, and all three lane records are otherwise unchanged.
- Neither `tools/typescript-lanes.json` nor the policy artifact is a member of the 352-row generator closure. The selected ordinary generator inputs, recipe metadata, output list, and discovery reference products therefore do not change in this design.
- The frozen unchanged-main evidence records the selected ancestor generator policy refusing first at the stale `tools/contracts/package.json` pin. The prospective report and provider lanes pass while the generator lane still refuses under the currently selected ancestor policy. These bounded results explain the data refresh; they do not constitute a checker run under a fabricated acceptance or prove complete materialization.
- Current main still contains the selected ancestor typed registry and pre-materialization helper bytes. Contract 180 supplies the accepted immutable prospective helper and closure authority; this proposal does not derive authority from unaccepted working code or install those bytes.
- Complete materialization, corrected owning controls and all three TypeScript lanes, independent code-unit review and assent, exact integration, new-path inventory binding, and the separately reviewed one-run blind refresh remain required before census-dependent consumption.

## Non-blocking observations

None.
