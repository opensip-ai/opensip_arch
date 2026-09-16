The Rust3 field inventory is finished and all its checks pass. I only wrote inside `/tmp/opensip-implementation/m1-rust-wire-translation-01`, made no commits and approved nothing. The gap-resolution proposals are still unaccepted proposals.

**What's there**
- **Every member is covered.** All 231 members of `rust-provider-protocol.v2.json` `$.wireSchema` have a row: 5 envelope, 21 frames, 101 payload and 104 definition members. There are also 59 rows for members reached through its `external` definitions, 76 new schema-native members and 6 new frames, for a 26-frame Rust3 vocabulary.
- **Per row:** source path, pinned sha256, selector and exact original text. Also:
  - the v2 wire type and the Rust3 wire type, and where each type comes from;
  - the disposition, and whether an owner actually settles it;
  - the schema ref, and the rules that sit outside the schema, each checked at its file and line.
- **Checks, via `tools/build.py`:**
  - 0 failures; two runs gave byte-identical output;
  - 199 wire-type cross-checks with 0 mismatches;
  - 131 `$ref`s followed from the Rust3 successor records, none unresolved, and none reaching the superseded native-evidence definitions;
  - 34 member-list comparisons, each against a declared expected difference;
  - 55 citation line anchors and 41 rule-owner anchors;
  - probes showing that schema validity is not CBOR admission.
- **Selftest:** `--selftest` catches all 12 deliberate mutations. Logs are in `logs/`.

**Genuine unresolved issues (only an owner can close these)**
1. **PreparedOutput frames (R3-G9):** they are still in the major-3 state machine, but their inherited payloads refer to rust-v1 rows that §0:130 supersedes. No major-3 payload definition exists.
2. **subjectScopeCommitment (R3-G4):** Rust v2 puts one per-stage value in every key; §4.1a and the startup coverage rules require a separate value per key. P-1 covers TypeScript only.
3. **Ordering (R3-G17):**
   - v2 allows Cancel in START; `protocol3-transitions` does not.
   - v2 allows Unavailable only before the first output; P3-25 has no such guard.
   - v2's prepared-output order text contradicts the dependency-source and NativeContextVerified steps.

   §0 supersedes only `phaseValues`.
4. **DependencySourceManifestV3.manifestSha256 (R3-G11):** its digest is defined over the frame that contains it, and no recipe is given. Entry order and `packageKey` grammar are also unstated.
5. **Missing definitions or names:**
   - DependencySourceChunk has no member types; DependencySourceAccepted and the envelope have no record names (R3-G10, R3-G3).
   - The domain behind each coverage commitment is unstated (R3-G12).
   - StageResultV2 is marked superseded but has no successor (R3-G13).
   - ProviderFault, Cancel and Cancelled member types and nullability are unstated, and so is which phases `observedPhase` may take (R3-G14).
   - SnapshotEntryV2 variant member types are unstated (R3-G15).
   - Some identity echo substitutions are never listed (R3-G16).
6. **AnchorRefV1 (R3-G5):** CBOR types are unstated, and `fact-ref` conflicts with mandatory fact2. P-2 would resolve that conflict but is unaccepted.
7. **Pending root action:**
   - **Common-control owner (R3-G18):** the claimed owner, `control-protocol-contract.v2`, marks itself `CANDIDATE-NOT-APPLIED` and `binds NOTHING`, so root still has to confirm the owner chain.
   - **Citation defect (R3-G19):** `resolutions.md` cites `check-rust-provider-protocol.py` as "checkRust2", but that file is the v1 checker. The real v2 checker computes none of the stage or stream commitments.

**Things you should know**
- The native-evidence `CoverageKeyV2` (5 members) and Rust v2's own `CoverageKeyV2` (8 members) are both on the Rust3 wire. They must be kept apart by schema `$id`.
- `docs/implementation/README.md` changed on disk while I was working. I re-read and re-pinned it, and the new text changes no Rust3 result.
- The rest of the architecture tree has uncommitted or untracked edits. The pins record the bytes as I read them, and the build stops if any of them change.

Files are in `/tmp/opensip-implementation/m1-rust-wire-translation-01`:
- `translation.md`
- `fields.json`
- `coverage.json`
- `tools/`
- `logs/`
