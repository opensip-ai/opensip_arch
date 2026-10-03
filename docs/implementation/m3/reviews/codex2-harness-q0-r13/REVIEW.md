# CODEX2 — M3-Q0 r13

**Verdict: ACCEPT.** R12-01 is resolved. No new required finding; the two existing non-blocking observations remain.

| Reviewed subject | Bytes | SHA-256 |
|---|---:|---|
| DESIGN.md (r13) | 151216 | `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4` |
| exploratory-quality-envelope.schema.v1.json (r13) | 60241 | `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6` |
| DESIGN-r12.md | 148609 | `72e70548b78843699bde2176231b909af6b549e7b30921b687bb1d6b463f2c36` |
| exploratory-quality-envelope.schema.v1-r12.json | 60031 | `d05472ec700d8e8282b220f3d0d0b9530d00eafbe8f981eeeebf4c801a75d961` |

## Decisions requested

**R12-01 is resolved.** [The availability rules](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:891) require actual root creation, observed reaping and valid monotonic timestamps for a root-reaped duration. A launch that creates no root, or a root that was not reaped, retains its slot with `run-failed` and null informational timing. A failed run whose root was reaped may keep its known duration. The platform reasons remain mandatory, the row remains incomplete, and this informational duration remains outside elapsed aggregates and budgets.

[ENV's invariant](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:5) matches these rules. The [new calibration case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:918) represents the original failed-before-root counterexample truthfully. The [three reference cases](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1085) reject missing timing without the failure reason, accept null timing for a failed launch with no root, and accept known timing for a failed run whose root was reaped.

**No substantive change beyond the requested amendment.** The full DESIGN diff adds only the revised availability rules, calibration/reference cases, response table and revision metadata. The schema diff changes only its description. Its structure and the existing performance nulling, aggregate, budget and Linux-settlement rules are unchanged.

## Required findings

None.

## Existing non-blocking observations

- **C2-Q0-R12-N01, unchanged:** the retained [macOS-known-elapsed case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1071) and [unqualified reaping model](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1074) should be restricted to Linux or explicitly superseded. The operative r12/r13 rules already override the old macOS conclusions.
- **C2-Q0-R12-N02, unchanged:** the [macOS-within rejection case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1087) belongs under the semantic validator heading. The structural schema has no OS-dependent condition; it does correctly reject the informational field on a complete row.

## Review limits

Acceptance applies to the exact r13 design subjects. Static review included the full comparison, hashes and sizes, schema structure/reference inspection and independent review slices. The schema has 41 closed object definitions, no floating-point types and no unresolved local references. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run. No runtime home was accessed and no commit was created. All writes are confined to the requested r13 review directory.
