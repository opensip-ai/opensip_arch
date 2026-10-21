# D2b plan r3, amendment A2: the codecs in three parts, and the HelloAck's descriptor context

**Lead plan amendment, 2026-10-17. Unreviewed; proposed with D2b-3a r1 for Codex to judge.** Accepting D2b-3a accepts this amendment. It amends the accepted D2b plan r3 (`PLAN-r3.md`; Codex `codex-d2b-plan-r3`) as amendment A1 (`PLAN-r3-A1.md`) already amends it. Law M3-D r5 is unchanged: item 10, the materialization maps and every carrier row stand as written. Nothing else in the plan changes.

## Why

1. **Size.** Section 1 makes each of D2b-3 and D2b-4 a whole codec: the receive side (the decode, the schema checks, LD-D2B-15's admission, the commitments, the table events), the send side (the payload builders, LD-D2B-9's schedule constructor, the HOST-SEND-SCHEDULE sender), the successors' payloads, and the replays (trial 07 and the successors' vectors, D2b-T4 and T5). One review of all of that would be very large. A2 splits each codec in three, each part with its own lane and review, as B3-b's A1 split B3-b2.
2. **A context gap.** LD-D2B-15's context names "the verified `providerBuildId`" but not the other descriptor values the TS2 HelloAck must equal. The source:
   - handshake-v1 `x-opensip-wire-law.typescriptDescriptorBinding.rule`: "Each providerDescriptorFields member of HelloAck equals the same-named member of the verified provider descriptor and each runtimeDescriptorFields member equals the verified runtime descriptor (delivery.v2 identity.hostValidation). Any mismatch is PROVIDER.PROTOCOL_VIOLATION before a source byte. The verified providerBuildId remains the source of FactCandidateV1.producerVersion."
   - with `providerDescriptorFields` = providerBuildId, protocolMajor, typescriptVersion, typescriptCompilerSha256, typescriptStdlibMerkleRoot, defaultWorkBudgetProfileId, defaultWorkBudgetProfileSha256, and `runtimeDescriptorFields` = nodeVersion, v8Version, modulesAbi, platformId;
   - and `TypeScriptHelloAckV2`'s description: "typescript-semantic major-2 HelloAck. Every HelloAckV1 member kept, including all provider/runtime descriptor verification; protocolMajor 1 -> 2 and the fixed capability array -> the negotiated echo; identityVersions added."

   Section 0 already gives D2b "the handshake checks: exact identity echoes". Rust3 needs no such entry: its HelloAck echo fields are the Hello's own `expectedIdentity` (`rustIdentityBinding`), which "the frames sent" already covers.

## A2-1. The split (section 1)

- **Section 1's table, the D2b-3 row.**
  - Current: "| **D2b-3** | The TS2 codec: contextual admission, payload builders, schedule and sender, FA-2 | D2b-T4, D2b-T5 (TS2); §4's TS2 controls | D2b-1, D2b-2, D2b-0, D2b-0b |" (as A1 states its dependencies).
  - Replacement, three rows:
    - "| **D2b-3a** | The TS2 receive side: each worker frame's envelope, closed schema (the carrier-typed decode for the inherited frames, the product schema for the extern ones), LD-D2B-15's contextual admission over TS2's admission rows, the received-byte commitments and their provenance, the table events, and the conversion into the generated carriers; LD-D2B-18's HelloAck exact-echo gate; LD-D2B-2's TS2 depth bounds | §4's RF-1 provenance and commitment controls and RF-2's schema and contextual-admission controls, for TS2 | D2b-1, D2b-2, D2b-0, D2b-0b |"
    - "| **D2b-3b** | The TS2 send side: the host payload builders, LD-D2B-9's schedule constructor (REQUEST-WIRE-ACCOUNTING), the HOST-SEND-SCHEDULE sender with LD-D2B-7's Cancel law and LD-D2B-18's sender half (the Hello's array from the selection), and the TS2 participant the supervisor drives (D3a's `Participant`) | §4's RF-2 builder and sender controls, for TS2 | D2b-3a |"
    - "| **D2b-3c** | FA-2 for TS2 (LD-D2B-16): the census request and the census payloads' admission, with LD-D2B-2's bound recomputed over them; trial 07's TS2 replay and FA-2's vectors; D2b-T4 and D2b-T5 (TS2) | §4's RF-3 FA-2 controls and the successors' vectors, for TS2 | D2b-3a, D2b-3b |"
- **Section 1's table, the D2b-4 row.**
  - Current: "| **D2b-4** | The Rust3 codec: contextual admission, payload builders, schedule and sender, FA-2 and RUST3-LIM | D2b-T4, D2b-T5 (Rust3); §4's Rust3 controls | D2b-1, D2b-2, D2b-0, D2b-0b |".
  - Replacement, three rows: **D2b-4a** (the Rust3 receive side, with the retained framePrecheck, T016 and T020, RUST3-SPOOL and the spool entry of LD-D2B-3 item 3), **D2b-4b** (the Rust3 send side and participant, with RUST3-LIM's builder side of LD-D2B-17), and **D2b-4c** (FA-2 and RUST3-LIM's admission for Rust3, trial 07's Rust3 replay and the successors' vectors, D2b-T4 and D2b-T5 for Rust3), with the same dependencies as D2b-3a to D2b-3c, D2b-4a also on D2b-3a's shared carrier interpreter.
- **Section 1, the order** (as A1 states it).
  - Current: "**Order:** D2b-1, then D2b-2, then D2b-0, then D2b-0b with its blind refresh, then D2b-3 and D2b-4. D2b-0b is integrated before D2b-3 or D2b-4 consumes either successor payload."
  - Replacement: "**Order:** D2b-1, then D2b-2, then D2b-0, then D2b-0b with its blind refresh, then D2b-3a, D2b-3b and D2b-3c, and D2b-4a, D2b-4b and D2b-4c, each triple in that order. D2b-0b is integrated before any part consumes either successor payload."

Every other place the plan names D2b-3 or D2b-4 now means the part that holds the code in question. For the receive side, that is D2b-3a or D2b-4a; for the builders, the schedule and the sender, D2b-3b or D2b-4b; for the successors' payloads and the replays, D2b-3c or D2b-4c.

## A2-2. The context (LD-D2B-15)

- **LD-D2B-15, the context it is supplied** (`PLAN-r3.md`:142).
  - Current: "… the verified `providerBuildId`, the host-admitted target domain, …".
  - Replacement: "… the verified `providerBuildId`; for TS2, the verified provider and runtime descriptors' `providerDescriptorFields` and `runtimeDescriptorFields` values (handshake-v1 `typescriptDescriptorBinding`; D4 supplies them from the verified signed descriptors, the `providerBuildId` among them); the host-admitted target domain, …".

## A2-3. The mutations (section 4)

- **Section 4, the D2b-3 and D2b-4 mutations** (`PLAN-r3.md`:265-273). The list is unchanged, and each mutation is now run in the part that holds its code:
  - **D2b-3a and D2b-4a:** an echo member ignored; a commitment computed from a re-encoding (killed by the provenance assertion); the stage correlation unchecked; the batch counter unchecked. D2b-4a also: the spool charged at the candidate's length.
  - **D2b-3b and D2b-4b:** a limits member changed (the Hello's limits, which the TS2 HelloAck does not echo).
  - **D2b-3c and D2b-4c:** a census token mismatch accepted. D2b-4c also: the reference scope's count not reconstructed.

## Not changed

The law, LD-D2B-1 to LD-D2B-18 apart from A2-2's one addition, section 3's duty allocation, section 4's controls (each run in its part), and amendment A1.
