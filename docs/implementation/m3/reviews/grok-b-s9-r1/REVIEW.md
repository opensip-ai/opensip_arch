# B-S9 r1 — ACCEPT-DESIGN-UNIT

Design unit B-S9, the `CONFIG.INVALID` remedy as complete successor copies of the two native-model files. Verdict **ACCEPT-DESIGN-UNIT**. No required finding. The remedy string stays the 706-character text in the README and in both copies.

Subject manifest `docs/implementation/m3/config-discovery-b/b-s9-subject.json` is 1,694 bytes, sha256 `dbe62e5b6e577b76fb6ceff2b8ce58ebed9354ac320a0a98bc14e4ee62c0dd24`. Successor `docs/implementation/m3/config-discovery-b/b-s9/successor.json` is 3,371 bytes, sha256 `aeb9ed95f170f82b0a42c858d8e784d7f6391314330d86ec0b0ed7cb92b72dff`. All 21 pins in `hashes.txt` match. `b-s9-unit.json` is the lead draft and is not part of the subject.

## The string

The new remedy is 706 ASCII characters, inside `BoundedText`'s 1,024. It keeps, byte for byte, both predicates `foundation/check-identity.py` applies at 7212-7217 (`registered capability id from the native capability matrix` and `(capabilityId, languageMode, workspaceRoot)`) and X12's policy words (`name exactly one bundled policy pack id`, `written exactly as name:version`, `supply no policy document of your own or from a third party`).

It is a true next step for every key that reaches public detail `CONFIG.INVALID` once B1 lands.

- External configuration of `native.requested-capability-unregistered`, `-mode-unregistered` and `-duplicate-ownership-tuple` still reaches detail `CONFIG.INVALID` (`native-evidence.schemas.v2.json` route registry). The capability clause is the X12-0 sentence, unchanged.
- X12 r4 rows 1, 2 and 3a still use detail `CONFIG.INVALID` (live rows at PROPOSAL.md:179-182). Row 3 stays `POLICY.IMPERATIVE_KEY_REFUSED`. The policy clause is unchanged.
- M3-B r2 item 4 (accepted bytes PROPOSAL-r2.md:130-153; live PROPOSAL.md is that text plus the two-line acceptance note, so the S9 sentence is live MB:155) sends invalid external configuration input to `CONFIG.INVALID`. Lexical admission, unknown keys, an unsupported schema major, a per-layer allowlist miss, Config2 logical paths, an explicit empty `workspaceRoots`, profile admission, waiver ids, evidence ids, and component duplicates and pin/hold conflicts each have a clause in the string. Schema-one user fields in `preview-configuration.schema.v1.json` are exactly the item-11 mapping, so an unmapped version-1 field reaches the caller as an unknown key or an unsupported `schemaVersion`.
- `CONFIG_DEFAULTS_INCOMPLETE`, host-built flags, and the environment layer stay host-invariant (item 4). They do not use this string.
- `CONFIG.CUSTODY_REFUSED`, `PROJECT.ROOT_CUSTODY_REFUSED` and `PROJECT.EXPLICIT_PATH_INVALID` are registry members. SL S12.1 rule 2 makes them the public detail while SL:1302 keeps D9 code `CONFIG.INVALID`. `native.explicit-root-without-marker` is itself a registry member (public-detail-registry.v1.json). Those keys stay outside the string, as the README says.

The product carriers on current main are still the X12-0 string: `configuration.rs:24`, the length-367 pin at `configuration_tests.rs:338-343`, and `doctor_ingress.rs:216`. This unit changes no product file. B1-a embeds the new string later.

## The copies and the selection

`check_b_s9.py` recomputes each effective parent from the e093e90 lock. Each copy differs from that parent, and from the raw parent, in line 1158 only. Both parse with `ast`. `PUBLIC_ROUTE_REMEDIES` keeps every other key and value. The two copies differ from each other exactly as their raw parents do: 12 unified-diff lines, three deletions inside `admit_capability_manifest`, which is CT's correction, carried. `build_b_s9.py` run twice rewrote identical bytes for both copies, `copies-report.json`, `successor.json` and the subject manifest.

The record has three parents, `passageOverrides` empty, and seven candidates equal to the subject minus the record. That is a sound way to end X12-0's two line-1158 meanings. CT's README already selects a complete copy of this file and leaves the historical file untouched. `verify_design.py` has no selection concept: it accepts a parent that is already accepted and not overwritten (`tools/verify_design.py:221-229`), and neither native-model file is a generation source. The same file is pinned at `generator-closure.json:1746` and `typescript-lanes.json:804` (40714 bytes, sha256 `c13d231e…`), which is the working-tree file.

`verify_scratch.py` with the real verifier:

| Base | Successors before | After B-S9 | Rejected second override | Rejected VD1 supersession | Later override of the copy's line 1158 | Later override of an old line 1158 | Later override of an old other line |
|---|---|---|---|---|---|---|---|
| `e093e90` | 77 | 78 | conflicting contract passage overrides | passage supersession must select an inventory row description | PASS | REFUSED | PASS |
| `0ceb9ad` | 78 | 79 | same refusal | same refusal | PASS | REFUSED | PASS |
| checkout `240a795` | 80 | 81 | same refusal | same refusal | PASS | REFUSED | PASS |

The checkout run verified 40 generation sources. The selected inventory and inheritance were unchanged. Probe 3c, an override of an old file's line other than 1158, still passes. That residual is the same one CT already carries, and the README holds it: later edits of `PUBLIC_ROUTE_REMEDIES` override the B-S9 copies. A verify_design rule against that would be the VD2-class change LD-1 and LD-4 reject. The hazard is acceptable.

## Laws

M3-B r2 item 4's "through X12-0's route" stays the `PUBLIC_ROUTE_REMEDIES` text successor. The binding form is the copy, which needs no verify_design change. The units table puts S9 in B-S1 (live MB:841 and MB:843). The lead's split of 2026-10-04 is a unit-plan change. Bound B-S1 already says S9 is B-S9 and that B-S1 touches no native-model file. X12 r4 keeps rows 1, 2 and 3a on `CONFIG.INVALID` and does not change the policy words. X12-0's meaning on the two parents becomes historical through the selection statement. Nothing else frozen is in the way.

## Non-blocking

**NBO-1.** The README and the standing name e093e90 and 77 to 78. Current main is `240a795`, with I1-L, B-S1 and B-S2 bound (80 successors). The only bound entry on either parent is still X12-0's line 1158 at all three revisions, and B-S9 binds on each. The standing's derivation stays accurate. No byte change.

**NBO-2.** The table's last row cites NE:3571 for a configured `NOT-SELECTED` cell and points it at the capability-id clause. That key's public detail is `PROVIDER.NOT_SELECTED` (NE:3577-3579 and the route registry). The remedy string does not need a clause for it. On the next touch, list the key with the other exclusions. Do not change the 706-character string.
