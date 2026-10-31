# Adoption receipt: TSR-1, the TypeScript resolution profile, with native-schema successor NSS-TSR1-S1, 2026-10-29

**Decision LD-COORD-TSR1 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1.**

TSR-1 (`TSR-1-r4.md`) is adopted as a native successor that publishes the choices item 10
(`snapshot-plan-c/PROPOSAL.md`:571) and NE §2.2–2.4 had left unpublished: X-C2B1-1 to X-C2B1-6. It has three parts:
- **Part P:** the resolution profile, pinned to TypeScript 6.0.3 and keyed by the admitted compiler and stdlib
  closure's `semanticVersion`. Any other version refuses before PlanId.
- **Part R:** refusal termination, through aliases to the existing `native.typescript-config-unresolved`
  (CONFIG.INVALID) and NE:3530's REQUEST.PRECONDITION_FAILED row. It adds no new public code.
- **Part S, NSS-TSR1-S1:** a pure-widening native-schema successor. It admits `""` as the project-root spelling at
  exactly `honoredOptions.baseUrl`, `rootDirs[]` and `paths[].substitutions[]`, and keeps `$id` and major version 2.

## What was reviewed

| Artifact | sha256 |
| --- | --- |
| **Adopted subject:** `TSR-1-r4.md` (93,986 bytes; the reviewed bytes, never edited) | `be654c41dcc310206fca27aa3feaddd9c1d5d9c1f3eeb7f8652dd0026c4e99f3` |
| **R3 review r4 (`TSR-1: ACCEPT`, no findings):** `REVIEW-r4.md` | `c22434c25f7d4cb53b539012f7e4f94be81e657b1fd8bbec632d0ebd50750a71` |
| Request r4 | `1a85297bd4ab4b7cbe3668b6f514dbfb04a3caaf87d3505f252893f745fd3bc1` |
| Earlier rounds: REVIEW-r1 (RF-1..10), r2 (R2-RF-1..5) and r3 (R3-RF-1), all REQUIRED-FINDINGS and resolved | listed in `HANDOFF-ADOPTION.md` |
| The author's handoff: `HANDOFF-ADOPTION.md` | `65b396b13edfedc71583902e4a4f663c70da670bcc668eba1c12546a0fdf39e9` |
| The verification: `VERIFY-r2.md` | `753b880601e7ac6af98b101ef794a00ee8f05f6b3acfa374defbc2a3cea5408d` |
| The interpretation evidence manifest: `work/evidence-manifest.sha256` (67 files) | `267dac82707eee29b20b1f04a81f612c6a9ba21b14f3575b7025ce1f73a09d91` |
| The plan: `PLAN.md` (LD-Q-3) | `493ff39120e80537ec7d5a8cc76b9485fcf19d94322b5bd9fefca2a9b6b95bd2` |

- **The reviewer:** codex-tsr1-r1, Codex gpt-6-astra/high, R3-FRONTIER, in w15:p1, over four rounds. It is a
  different vendor from the Claude author (opensip-tsr1, Opus 5.5 high, w12:p1) and the Claude coordinator.
- **The origin:** the C2b-1 escalation `../c2b1/ESCALATION-X-C2B1-r1.md`, and coordinator ruling LD-Q-3.

## The coordinator's adoption conditions, and where they are met

1. **NE:527-546 (effective `allowJs`/`checkJs`) is unchanged, with 6.0.3 parity shown.** TSR-1 P-0.1 meets this: the
   6.0.3 computed option at `_tsc.js`:18175-18180 is identical to NE:545's 5.6.3 citation. The reviewer confirmed it
   in REVIEW-r1 §9.1 and REVIEW-r2 §2.
2. **Part S** has a named successor identity, `""` at exactly three locations, a pure-widening proof (every existing
   record, vector and retained identity unchanged), the encoding `C("")` = `22 22` under the unchanged H, and the
   carrier and model chain C2b-1b must move. TSR-1 §11 meets this. The reviewer held Part S in scope with no R4 needed
   (REVIEW-r1 §6).

## The authority

The owner's decision OD-AUTO-1 (2026-10-29, the top of `control-2026-10-06/ACTIVE-PLAN.md`) delegates law changes
to the coordinator after an R3 different-vendor review. This adoption:
- publishes new native law, and widens the native schema at three locations;
- changes no cap, charge law, capacity, count or route. Its priced work is C2b-1b's, under M1a C1 (§9);
- adds no public code.

## Disclosed limits (TSR-1 §15), accepted with adoption

- **Restriction 3.** Fourteen Part P options, and top-level `references`, refuse CONFIG.INVALID when set away from
  their admitted values. These include `isolatedModules: true`, `verbatimModuleSyntax: true`,
  `moduleDetection: "force"` under bundler, `typeRoots`, `jsxImportSource: "preact"`, and `references` in a program
  with roots. These are common in modern templates. The review rejected the alternative, a false strip disclosure.
  **The coordinator commissions TSR-2** (honouring these options) as a follow-on; see LD-Q-7.
- **Other limits:**
  - stripped options with true reasons and disclosed effects: `importHelpers`, `outDir`, `declarationDir` and
    `rootDir`;
  - case-sensitive matching;
  - `null` refuses;
  - stricter `package.json` parsing;
  - no `npm-shrinkwrap.json`.

## What this adoption does not accept

It does not accept C2b-1b's implementation, its pricing, the controls TSR1-C1..C31, the carrier and model moves, or
binding. Those are C2b-1b's, under R2-DEEP.

## Binding

At C2b-1b's binding, these are copied unchanged into the architecture repository, and the inventory records them:
- `TSR-1-r4.md`;
- this receipt;
- the evidence directory, pinned by its manifest.

## Owner notification

On 2026-10-29 this is flagged to the owner in the coordinator's session summary as an owner-delegated law change,
with restriction 3 called out. The owner can reverse it.
