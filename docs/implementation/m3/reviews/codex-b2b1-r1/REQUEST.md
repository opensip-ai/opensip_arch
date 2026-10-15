# Review request: B2-B1-r1 (platform primitives; M3-B unit B2-b, sub-unit B2-b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b1-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries, and `python3 -I -B tools/check_operability.py source --repository <tree>`, are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b1-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b1-r1-subject.json`: 6429 bytes, SHA-256 `85da7c59ebce7b0b05edd20bbdc64af4c2b69f5d23fe37fcd134c6ee7a1f15f7`, 29 members. Rehash every member.
- **Bases.**
  - Product `7d0ac1b59df9a099a4d8edc05d8600f46dd63923`, clean: B2-b0 is bound as contract successor 164, and inventory is v191.
  - Architecture `4fbc0c65011af58948f01986c79061443598a798`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b1` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 191 and contract successors 164 are unchanged. No inventory successor is proposed (LD-B2B1-1).

## Authority

- The accepted B2-b plan r4, section 1.1 (`codex-b2b-plan-r4`), including its B2BPLAN-5 resolution: the identity-carrying observation.
- M3-B r5 item 12, the discovery ledger profile.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The discovery profile.**
   - Is it exactly MB's provisional caps?
   - Is it the only path above the global caps, with `with_limits` unchanged?
   - Is the failure latch retained?
   - Is "created once, never recreated" correctly left to the owner, B2-b3?
2. **`observe_child`.**
   - One no-follow `fstatat` under the existing name grammar, never opening, creating or following.
   - `ENOENT` only is absence.
   - The kind comes from `S_IFMT`.
   - `from_stat` matches `from_metadata`'s fields.
   - The accounted cost is the existing single status read.
   - All new items are macOS-only.
3. **`matches`.** Is comparing device, inode and kind against the later-opened descriptor sufficient for B2-b3's swap refusal? `Absent` must never match.
4. **Tests.**
   - The kinds, absence and the grammar.
   - Unchanged times.
   - Same-kind replacement of a directory and of a file.
   - The kind mismatch.
   - The exact charge.
   - The profile's exact caps, one beyond, the latch and `with_limits`.
5. **LD-B2B1-1.** No inventory successor, because no path is added.
6. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - Equal failure sets for platform, security and host.
   - All-targets Clippy on all three.
   - rustfmt, with its classification.
   - The tools tests, the census and verify_design.
   - The eight mutations, each caught.
7. **Scope.** There is no caller, walker, custody or environment read, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "85da7c59ebce7b0b05edd20bbdc64af4c2b69f5d23fe37fcd134c6ee7a1f15f7",
  "implementsPlanR4Section11": true,
  "discoveryProfileOnlyPathAboveCaps": true,
  "withLimitsUnchanged": true,
  "observeChildNoFollowNoOpen": true,
  "identityCarriedAndMatchSound": true,
  "sameKindReplacementDetected": true,
  "accountedCostSound": true,
  "macosOnlyLinuxUnchanged": true,
  "ldB2B1_1Sound": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 8,
  "inventoryUnchanged": 191,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record, then makes the product code commit. Nothing is pushed.
