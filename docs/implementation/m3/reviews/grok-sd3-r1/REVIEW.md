# SD-3 r1

Verdict: ACCEPT-DESIGN-UNIT.

This accepts the proposed SD-3 design publication: the host launcher closure row, the loader row, and the `apps/launch/` layout entry under owner-selected O7 and M3-D r5 F-1 / item 29. It does not implement D1b, bind a contract, change product code or inventory, enforce confinement, put L in effect, or qualify a platform or product.

## Subject

`sd-3-r1-subject.json` is 1822 bytes, SHA-256 `270c16f080df68c709b0d4d33a816af4b07334339f3dc7eda5bed88a0ec17f74`. It names nine sorted unique members, and each staged file matches its pin. The unit directory is absent at architecture `e3e5e8b68f00073ea8c1626c2fc393e265ea89a0`. Product `bf4be44ffbaf02e8518c276882524831ee8e12c4` is clean, and that tree has no `apps/launch/` path and no `opensip-launch` path. `design-lock.json` remains 614747 bytes, SHA-256 `9c73578855ed10eb52dcd507a4498761045efa60c7a5899afb1726d35f43973f`, with 139 inventory successors ending at inventory v179 and 154 contract successors.

`successor.json` (7538 bytes, `ad0d818e516a5763e72a5e4fb37367687c4a6ee1c226966ac1fc812ac550fe7f`) carries five passage overrides and an empty supersession list. It does not assign contract number 155. That number is prospective only if no other contract binds first. `README.md` links `CONTRACT.md` and `selection.json` in the same directory.

## Authorities

All three parent pins and all five authority pins match the architecture commit.

| Pin | Bytes | SHA-256 |
| --- | ---: | --- |
| `08-decision-and-readiness-register.md` | 130283 | `de21a7e09096f2cf7b22f2700128e59581795278e46b80542745f5ca812395fe` |
| `14-repository-and-module-layout.md` | 65207 | `c7b10bf6d0f98d196d4509c5b972cd87f4af27bf9a56b9ffe5a240f93ee6287e` |
| `implementation-boundaries-and-build-plan.md` | 112850 | `8e6e8babd30bc3421f605efea9aae4b2d4a5c3c4cbfa4315bbf74cbe4ccbd33b` |
| `PROPOSAL-r5.md` | 209266 | `224b9228e9d7c0bc11c848c88cd2ed7fa7da8734208c45d70fbb678a97afec6d` |
| `M3-PLAN-r10.md` | 226011 | `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964` |
| `CF-P-RECORD.md` | 40007 | `6323a1b4df5a35ebb9b206466692d09f1ea477b37365b5179693e526c1352672` |
| `O7-OWNER-DECISION-2026-10-09.json` | 1676 | `625caf46fcbe4a4292d85e42f91f186223a7e68fc3b091ac8d7419b853e9b255` |
| owner-decision `review.json` | 414 | `f8b4dc2c0f27adab57ddfc1e82fc9fce1d96787680dfa3f3909abd533b5863d2` |

The O7 record is `ADOPTED-EXISTING-PROPOSAL`, with `sectionFSelectedAsRecommended` true and the instruction `adopt the existing O7 proposal`. Its review is ACCEPT for O7, D3, and D13. CF-1, D1b, provider launch, and effective L stay false on that record. Item 29 names SD-3 as the DR-G14 and DR-G22 rows plus a CH14 layout entry for `apps/launch/`, owned with F-1 and landing with D1b. F-1 places `opensip-launch` in the host's own signed release closure, has the host `posix_spawn` it, and leaves CF-1 to measure the signed hardened-runtime launcher. Proposal r5 requires `ACCEPT-DESIGN-UNIT` for SD-3.

## Passages

`evidence/passages.json` is the same five overrides as the successor. Each `before` text is the unique parent line named by its selector.

The layout override is chapter 14 line 30, the `cli/` row inside the `apps/` tree. The replacement keeps that row and inserts one following row, `launch/`, for the trusted first-party `opensip-launch` in the signed host closure, marked proposed. `report/` remains the next existing row. No other layout line is selected.

The build-plan overrides are the DR-G14 row at line 1018 and the DR-G22 row at line 1026. Each keeps its stage (`M3` and `M6`) and its existing paths, and appends `` `apps/launch/` (SD-3 host-closure launcher) ``.

The register overrides are DR-G14 at line 359 and DR-G22 at line 367. The header at line 344 is gate, claim, harness, required retained evidence, owner, assurance stage, threshold, and historical status. Only the evidence cell changes. Gate id, claim, harness, owners, stage, threshold, and `OPEN` are byte-identical. DR-G14 stays `TypeScript V1 shape IMPLEMENTABLE; V2 rule not QUALIFIED` and `all supported roles/platforms; exception only by explicit product approval and never labeled self-contained`. DR-G22 stays `PROPOSED; not QUALIFIED` and `pass all declared platforms or remove platform support`. The evidence additions name the host-associated signed launcher closure and the host-to-launcher and launcher-to-target loader traces. They do not add an exception, a platform, or an allowlist member.

## What the contract selects

`opensip-launch` is a mandatory member of the host's own signed release closure. Its source home is `apps/launch/`. Provider and tool targets keep their separately admitted closure associations. `selection.json` records no new component role, closure kind, command, wire member, loader-member list, product workspace change, product inventory change, or launcher implementation.

The installed path comes from the existing signed host release layout. Distribution law already requires an immutable full-tree path/type/mode/length/digest commitment, and lifecycle law already requires a signed full-tree path/type/mode/length/digest closure. A basename or `PATH` search does not supply that association, and this unit defines no new release-manifest schema and no fixed platform-independent install directory. The loader path comes from the existing qualified DR-G22 loader allowlist. The host canonicalizes target, scratch, closure, and loader paths; the launcher refuses a noncanonical path. The macOS Seatbelt symbol stays a dynamically resolved declared dependency. Absence follows F-4's disclose rule, and a present interface whose apply or check fails is refusal. Link-time import of `sandbox_init_with_parameters`, either `sandbox_init` mode, and ambient `sandbox-exec` stay rejected, as F-1 and F-3 already reject them.

F-1's record bound, descriptor classes, status pipe, parent-death and core-limit controls, apply/check/`A`/exec order, and settlement classes stay as already written. This unit does not select a launch-record codec or a numeric failure-code list. Those representation gaps stay owed, with an owner, before D1b is the first consumer. SD-5b still owns the J1 confinement-refused projection and the existing-code detail test. D1a remains the production spawn mechanism. CF-1 still owes the signed hardened notarized launcher measurement, and CF-2 still owes its output carrier. Ad-hoc CF-P and the S-P / S-M prototypes do not meet CF-1.

No Cargo package, source stub, inventory row, or generated per-file table is added. Inventory 179 stays the current inventory. D1b's later product unit still owes its own census and additive inventory successor.

## Checklist

`cases.json` is a synthetic checklist of ten boolean duties and eleven cases. Its standing says it is not release or execution proof. One case leaves every duty true and expects `checklist-satisfied`. Each of the other ten sets exactly one duty false and expects `duty-open`: missing launcher, wrong host association, unsigned prototype, different executed bytes, ambient launcher, unqualified loader, undeclared runtime, noncanonical loader, unadmitted target, and declaration without a real trace. The satisfied case is abstract duty evidence. It is not a signature check, a loader measurement, or an admission.

The staged `check_sd3.py` was executed as that checklist only. Its stdout is byte-identical to `evidence/checks.json`: `passed` true, eleven cases, five passages, gate standing and bars unchanged, product implementation false, and platform qualification false. The same checker confirms the register cells outside evidence and the build-plan path append. The layout wording above was checked against the parent line directly.

The in-memory binding simulation is not this review's evidence and is not independent assent. `verify_design.py` was not run. After this acceptance the lead still supplies substantive assent, runs the actual design verification, and makes the separate architecture and product-lock commits. Nothing is pushed.
