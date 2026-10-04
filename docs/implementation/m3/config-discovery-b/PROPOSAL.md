# Configuration and discovery (M3-B) — proposal r4

**r4 ACCEPTED 2026-10-04 by GROK2** (`8e0803a8…`; `reviews/grok2-config-discovery-b-r4/`), with no required findings. r4's bytes, without this note, are preserved in `PROPOSAL-r4.md`. This file differs from them only in recording text, for GROK2's observations: the banner (NBO-1), and item 13's Output sentence, which now names `DiscoveryProvenanceV3` for every project (NBO-2). "RBS3" in r4's parentheticals means GROK2's r3 review of this law (`reviews/grok2-config-discovery-b-r3/`) (NBO-3).

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, during the overnight autonomous run. Law for unit **M3-B** of the accepted M3 unit plan (M3P:160). It covers three sub-units:
- **B1, the resolver:** Config2 layers, precedence and provenance (AQ:43-53, AQ:102-173), `resolvedConfigDigest` (IE:518-519) and FW-13 (COV:8104).
- **B2, discovery:** the S3 boundary (SL:105-332), NE §1.4 U-0 to U-9 (NE:619-948), FW-01 (COV:7852) and the host side of framework recognition (NE:2750-2777).
- **B3, multi-repository workspaces:** owner decision D15 (AQP:556), with the X2 successor it needs (M3P:160, M3P:374).

**r4, accepted (see the note above). Not code.** Product code waits for M3-P0 (M3P:159) and M3-L's acceptance (M3P:187). Every item below is a lead decision made under the owner's standing direction to proceed on the lead's recommendation. Each names the alternatives it rejects. Item 27 lists the one owner question and the points the reviewer should test hardest.

r2 answers GROK2's r1 review (`/tmp/opensip-implementation/reviews/grok2-config-discovery-b-r1/`, copied to `docs/implementation/m3/reviews/grok2-config-discovery-b-r1/`): two required findings and two non-blocking observations. GROK2 confirmed R1 to R7 apart from those findings. The r1 bytes are preserved as `PROPOSAL-r1.md` (sha256 `da014f54…`, 85,905 bytes).

**r3 is a record revision.** GROK2 accepted r2 on 2026-10-04 with no findings (`docs/implementation/m3/reviews/grok2-config-discovery-b-r2/`). The r2 bytes are preserved as `PROPOSAL-r2.md` (sha256 `92e65825…`, 94,762 bytes). The live file carried them with a 2-line acceptance note, which r3 removes. r3 applies only what has since been settled for this law: GROK2's rulings in its review of design unit B-S1, the three bound design units B-S1, B-S2 and B-S9, the acceptance of S1 and S2, and M3-L's cross-law item X10. It also re-pins this law's citations to accepted snapshots. It decides nothing new. The "r3 changes" table comes first, and the "r2 changes" table is kept below it with its reviewed citations. Diff r3 against `PROPOSAL-r2.md`.

## r4 changes

r4 answers GROK2's r3 review (`reviews/grok2-config-discovery-b-r3/`) and changes nothing else. r3's bytes are preserved in `PROPOSAL-r3.md`.

| Finding | Change |
|---|---|
| RF-1 | Item 24's directory-custody row stated "as above". After r3 rewrote the row above it, "as above" resolved to row 1's pair. The row now states row 2's pair explicitly: `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID`. Only the in-repository crossing moved to row 1 (RBS1 R2). |
| NBO-1 | Item 13's producer row now names `AdmittedBoundaryInventoryV3` for every project, per B-S1 LD-4. |

## r3 changes

Each row names its source. "RBS1 R2" means ruling R2 in GROK2's review of B-S1, not this law's reviewer question R2 (item 27).

| # | Change | Source |
|---|---|---|
| 1 | **Header.** r2's acceptance note is removed. r3 is a record revision. | `reviews/grok2-config-discovery-b-r2/` (ACCEPT, no findings) |
| 2 | **Item 24 row 3 now agrees with item 22 and row 1.** An explicit or config member when W fails W2 is a crossing into a repository that cannot become a member. It keeps row 1's `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` with `JOIN_CROSSES_NESTED_REPOSITORY`, so a project that never opts into D15 keeps S3's existing refusal. `workspace-root-inside-repository` is not applied to an explicit or config member. It is row 6's disclosure subject for a reader entry. Item 21's subject list now points to item 24 for when each subject applies. | RBS1 R2; BS1 LD-6; M3-PLAN r9, new-units row "M3-B record revision" and cross-law row "Ruling R2"; ON, "B-S1 accepted by GROK2" |
| 3 | **Item 24 rows 5 and 6: the member cap, as B-S1 settled it.** n counts the distinct repositories that the active branch's declarations name after placement, before X2 r9 item 6b reads any Git configuration or index. n > 64 refuses in **both** branches, and no member is dropped to fit, so row 6's exclusion no longer reaches the cap. Row 5 cites the subject's remedy, which B-S1 states at SL:1323. Row 6 also records what readers do when W fails W2: they declare nothing, and they disclose a literal entry inside a nested repository as `member-excluded` with subject `workspace-root-inside-repository`. | RBS1 R4, R5 and R2; BS1 LD-7, LD-10 and LD-17, and "Conflicts and reconciliations with accepted laws" |
| 4 | **The three design units are recorded as accepted and bound:** B-S1, with M3-C's SX-1, at product `9c11c53` (GROK2); B-S2 at `240a795` (Codex); and B-S9 at `8adfe0c` (Grok). Item 25's S3, S4 and S9 rows, its "Law versus contract" paragraph, the units table's gates and rows, and "Not claimed" say so. | ON, "B-S1 accepted by GROK2", "B-S2 accepted by Codex", "B-S9 accepted by Grok"; `reviews/grok2-b-s1-r1/`, `reviews/codex-b-s2-r1/`, `reviews/grok-b-s9-r1/` |
| 5 | **S9 is design unit B-S9,** split out of B-S1 by lead decision on 2026-10-04. The units table gains a B-S9 row, and B-S1's row no longer names S9. **B1-a depends on B-S9**, not on "B-S1 (S9 text)". B1-a embeds B-S9's string at `configuration.rs:24`, which `doctor_ingress.rs:216` reuses, and repins `configuration_tests.rs:338-343`. Item 4's S9 paragraph and item 25's S9 row point to B-S9. | BS1, "S9 is split out"; BS9, "What it is", "The change", "Binding"; `reviews/grok-b-s9-r1/REVIEW.md`, "Laws"; M3-PLAN r9, new-units row "B-S9" |
| 6 | **Two findings are settled by B-S1.** F9: B-S1's overrides of SL:286 and NE:4135 name `AdmittedBoundaryInventoryV3`. F10: SX-1 fixes the `.opensip/` rule, and item 22's sentence on a member's own `.opensip/` points to it. | BS1 §1 and §3 ("which also fixes MB finding F9 there"); `b-s1/PASSAGES.md` (SL line 286, NE line 4135) |
| 7 | **What B-S1 leaves to B's units.** B2-a implements SX-1's anchor and owes the `discovery-defaults.py` reference refresh. B2-a, B2-b and B3-b also owe the controls B-S1 lists for them. | BS1 LD-14, BS1-F3, "Controls owed by the implementing units" |
| 8 | **S1 and S2 are recorded as accepted:** X2 r9 and X12 r4, both accepted by Grok with no findings. | ON, "X2 r9 and X12 r4 accepted by Grok"; M3-PLAN r9, "Critical path" ("its successors X2 r9 and X12 r4 (**accepted**)") |
| 9 | **ML is cited by item** (M3-L's X10). r2's ML:494-509 is item 17 of M3-L r1, which r5 keeps. | ML X10 (r2, kept in r5); M3-PLAN r9, cross-law row "X10" |
| 10 | **Citations are re-pinned to accepted snapshots.** r2 cited live files, which have moved since or move with this revision's companion drafts. M3P lines move by −2 to `M3-PLAN-r4.md`. I1 lines move by −2 to `preview-pack-i1/PROPOSAL-r2.md`. X2 and X12 lines are unchanged in `PROPOSAL-r8.md` and `PROPOSAL-r3.md`, because each acceptance sentence sits inside an existing line. X4's live r7 file has no snapshot and is pinned by sha256. Item 10's quoted S2 passage is X12 r4's accepted text and keeps its own citations. The history tables keep their reviewed citations. | the cited live bytes at arch `6f85fe717` (M3P), `b412bce73` (I1), `bf3007f0f` (X2) and `0f69f15fc` (X12), each diffed against its snapshot |

Nothing else changes. The decisions, units, sizes, order and findings F1 to F14 are r2's, apart from the rows above.

## r2 changes

| Finding | Change |
|---|---|
| GROK2 RF-1 (a supplied `workspaceRoots` array must suppress reader membership) | Item 20 is restructured into two branches. **Array present:** an admitted `discovery.workspaceRoots` array, whether from the project or local layer or from `--workspace-root` (which is the flags layer of the same field, item 2), alone decides membership, and discovery is restricted to exactly those roots, never widened into a scan (NE:917-921; SLM:771-785; AQ:115). The readers declare no member; they may still record links whose directories lie inside members the array already admitted, and every other reader entry is recorded as dropped. **Array absent:** only then do the readers declare members. The same rule is stated in item 13's unit-source row, item 22 (the Config2 join), item 23's `--workspace-root` row, a new item 24 row for a dropped reader entry, and the forbidden substitutes. S3's content (item 25) now names the Config2-join text "exactly those roots, never widened". Item 20's controls add the config-tier cases. |
| GROK2 RF-2 (I1:388 freezes the order item 10 amends) | Item 10 no longer cites I1:381-388 as standing in full. I1:383-386 (the three row-count changes) stands. **I1:388's clause that X12 r3's order stands is withdrawn by S2 (X12 r4)**; the rest of I1:388's list stands. Item 10 now gives S2's exact text, including the withdrawal record, and item 25's S2 row says so. Found while fixing it: X12:136's "it is pure and runs before any custody" carries the same order. S2 records that its ordering sense is superseded too, and keeps X12:136's dependency correction (X12 does not depend on X1). |
| GROK2 NBO-1 (the census and the byte cap) | Item 12 now says the census bounds objects and edges only. Bytes are bounded separately by item 19's member cap and X2:272's per-record ceilings. |
| GROK2 NBO-2 (S3's "U-9 note" had no decision) | Item 22 now states the sentence: U-9 is unchanged, and its one fallback unit is at W's root; a member is never a second fallback site. S3's cell cites item 22. |

Nothing else changes in substance. The units, their sizes and their order are unchanged. (The r2 table keeps its reviewed citations. Its I1 lines are the live file's, +2 against `preview-pack-i1/PROPOSAL-r2.md`.)

## Short names

Line numbers were checked against the files named here on 2026-10-04. **r3 cites other laws and the M3 plan by accepted snapshot** (r3 change 10). r2 cited live files, and a live file that carries an acceptance note is 2 lines ahead of its `-rN` snapshot. Plans and designs whose live bytes have not changed since r2 are still cited live.

- **M3P** `docs/implementation/m3/M3-PLAN-r4.md` (r4, accepted; `e50f75d3…`). r2 cited the live r4 file (`1526c483…`, arch `6f85fe717`), so each M3P line here is r2's minus 2. The plan is now at r9, which records this law (`M3-PLAN-r9.md`, accepted by GROK2). This law keeps citing r4. **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6, accepted). **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; cited by section and line). **HD** `docs/implementation/m3/harness/DESIGN.md` (r13, accepted). The live AQP, OPP and HD bytes are unchanged since r2 (`1611014d…`, `4eca344b…`, `1f108399…`). **I1** `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md` (r2, accepted; `1eb47d1e…`). r2 cited the live file (`8cb31152…`), so each I1 line here is r2's minus 2. The exception is item 10's quoted S2 passage, which is X12 r4's accepted text and keeps its own citations of that live file. **ML** `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md` (M3-L r5, accepted in review by GROK2, `f654ee4e…`; it takes effect only when its gate is met), cited by item. r2 cited the lines of r1 (`PROPOSAL-r1.md`, `5e858c05…`), and r5 keeps r1's item numbers (ML X10).
- **T2R / T2F / T2M** `docs/implementation/m3/corpus/{README.md, FETCH-SPEC.md, t2-corpus-manifest.draft.json}` (T2b, accepted by GROK2; sha256 `3d355e72…`, `4ebe90a4…`, `c8cc48e1…`).
- **X2** `docs/implementation/m2/project-root-x2/PROPOSAL-r8.md` (r8, accepted; `c31d9a02…`). r2 cited the live r8 file (`c3ffc853…`), whose acceptance sentence sits inside line 3, so the lines are equal. **X2r9** `docs/implementation/m2/project-root-x2/PROPOSAL-r9.md`, successor S1 (accepted by Grok; `0d68e3a5…`). **X12** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r3.md` (r3, accepted; `11628912…`). Its lines equal those of the live r3 file r2 cited (`c9f0fd1a…`), whose acceptance sentence sits inside line 12. **X12r4** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md`, successor S2 (accepted by Grok; `adc9a88a…`). **X4** `docs/implementation/m2/live-guards-x4/PROPOSAL.md` (r7, accepted). X4 has no snapshot file, and its live bytes (`8eb4223e…`) are unchanged since its acceptance commit, arch `22c969a0f`.
- **AQ / IE / SL / NE / WS** `docs/v2/contracts/product-v1/{admission-and-qualification, identity-and-evidence, security-and-lifecycle, native-evidence, workflows-and-surfaces}.md`.
- **CH13** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`. **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`. **F03** `docs/v2/architecture/03-configuration-and-security.md`. **COV** `docs/v2/architecture/implementation-coverage.v1.json`.
- **SMAP** `docs/coop/design-corrections/current-source-map.proposed.md`. **PCS** `docs/coop/design-corrections/foundation/product-configuration.schema.v2.json`. **PCM** `…/foundation/product-configuration-model.py`. **DD** `docs/coop/design-corrections/discovery-defaults.py`. **SLS** `docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json`. **SLM** `…/security/security_lifecycle_model_v1.py`. **CINV** `docs/coop/design-corrections/workflows/command-inventory.v3.json`.
- **DRC** `docs/coop/completion/distribution-runtime-completion.v2.md`. **HFC** `docs/coop/completion/host-foundation-completion.v2.md` (the applied preview host foundation).
- **(r3)** **BS1 / BS2 / BS9** are the READMEs of the bound design units B-S1, B-S2 and B-S9: `docs/implementation/m3/config-discovery-b/b-s1/README.md` (`fd4bdcba…`), `b-s2/README.md` (`c1cebaad…`) and `b-s9/README.md` (`766de243…`). **RBS1** is GROK2's review of B-S1, `docs/implementation/m3/reviews/grok2-b-s1-r1/REVIEW.md` (`2a9e48a2…`). Its rulings are cited as RBS1 R2, R4 and R5. **ON** is the overnight log, `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry.
- Product paths are under `opensip/` at main `30c5db1`.

**Citation drift.** M3P:160 cites "AQP:537" for D15's successor clause. In the accepted bytes the D15 row is `PLAN-r4.md:535`, `PLAN-r6.md:554` and live `PLAN.md:556`. This law cites the live line. ML's cross-law finding X8 records the same drift for other AQP citations.

## Problem

**The product has a resolver slice, a root selector and nothing else.**
- `crates/host/src/configuration.rs` is X12's pack admission only. Its header says "Layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` arrive with M3 in this module" (`configuration.rs:1-4`). The module is `#[allow(dead_code)]` (`crates/host/src/lib.rs:49-52`).
- `crates/host/src/discovery.rs` is absent (M3P:118), and so is `crates/security/src/grants.rs`, which owns four M3 flags (M3P:126; COV:5277, 5317, 5337, 5377).
- X2b implemented S3's **upward** root selection (`crates/security/src/custody/project_admission.rs:303-384`). It custody-judges `opensip.json` but keeps no descriptor and reads no bytes (`project_admission.rs:240-269`). X2 left unit discovery to M3 (X2:280).

**Four accepted rules stand in the way of D15's shape** ("a workspace assembled from packages that live in separate repositories and refer to each other by path or by version", AQP:225):
- S3 makes every repository nested under the selected root "other custody roots ... never entered, and reachable only by their own `--project`", and a join into one refuses `JOIN_CROSSES_NESTED_REPOSITORY` (SL:163-168). It also says "There is no config 'project list' and no duplicate `--project` implicit multi-project mode" (SL:261-262).
- NE U-8 turns every nested repository into an `outside-project-boundary` exclusion (NE:816-836).
- X2 admits "one closed, conventional Git layout" (`crates/security/src/custody/git_tracking.rs:5-6`; X2:163). Its premise scope covers "nothing else under `.git`" than each **enclosing** repository's `.git`, `config` and `index` (X2:29).
- The accepted T2 Cargo rendering is a `.cargo/config.toml` `[patch.crates-io]` (T2F:120-123). NE §3.3 strips config-level `patch` from every Cargo invocation (NE:1743-1750). The npm and Python renderings were left to this successor (T2F:124; T2R:303).

**Two mechanical constraints found while drafting:**
- The platform ledger's hard caps are 65,536 objects and 131,072 edges (`crates/platform/src/work_ledger.rs:12-13`), and `with_limits` can only lower them (`work_ledger.rs:205-213`). A whole-repository downward walk of T2's large entries cannot fit; aws-sdk-rust alone has 245,250 blobs (T2F:105). SL leaves "bounding the host observation itself" to observation admission (SL:250-252).
- X12 orders pack admission "before ... X1 write admission, X2 project admission or any fence" (X12:125-130). A pack selected in the project file can only be read after S3 selects the root, and selection runs under the fence (X2:68, X2:74).

## Decisions

### A. B1, the resolver

#### 1. Six layers, one precedence, no seventh layer

**Decision.**
- The resolver has exactly six layers, from lowest to highest: compiled defaults, user-global, project, interactive local, environment, explicit flags.
- Discovery is **not** a layer. Discovery observations fold into the compiled-defaults layer only, with provenance `DISCOVERED:<recognizerId>@<version>`.
- **At M3 that fold is empty for the semantic configuration.** No discovered value is written into `analysis`, `components`, `discovery`, `policy` or `evidence`:
  - discovered units, membership, entry points, test globs and ignore conventions bind to the Plan through their own records: `membershipDigest` (NE:745), `FrameworkRecognitionV1` (NE:2752-2756) and the scope descriptor (NE:933-948);
  - absence of `discovery.workspaceRoots` and `discovery.entryPoints` keeps its meaning, "automatic" (AQ:115, AQ:156-157).
- A later recognizer may set a semantic field only through a reviewed host-owned mapping (DRC:595-596, applied here by analogy).
- **Merge.** A higher layer's scalar or whole array replaces the field, records merge by named field, and absence preserves the lower layer (AQ:106-107). `analysis.budget` is one atomic value (HFC:188-190). No `null` reset is accepted.

**Basis.** AQ:104-110 ("Discovery populates compiled default values ... Then global, project, interactive local and explicit flags override in order"); AQ:330-332 ("Discovery observations are folded into the trusted `defaults` layer"); CH13:59-61 ("There is no seventh configuration layer, provider-private override, or hidden environment input"); F03:14-21 (the six-layer order); HFC:159-168.

**Rejected.**
- Folding discovered units or entry points into `discovery.*`. It would make "absent means automatic" false, and it would bind one input twice, once in `resolvedConfigDigest` and once in `membershipDigest`.
- Discovery as a layer of its own: that is the seventh layer CH13:60 forbids.

**Forbidden.** A seventh layer; a provider-private or member-private precedence (item 22); a discovered value that outranks an explicit layer (AQ:108-109).

**Controls.**
- A configuration-free repository whose framework files change keeps the same `resolvedConfigDigest`, while its membership or recognition digest changes.
- Each layer's win and loss is tested at every adjacent pair. An array in a higher layer replaces a lower array whole.

#### 2. The carriers, their custody and what each layer admits

**Decision.**

| Layer | Carrier | Read when | Admitted fields |
|---|---|---|---|
| 1 compiled defaults | the authenticated release declaration registry and signed install profile | always | `analysis.profileId`, `capabilities` and `budget` (AQ:55-77, AQ:132-134); component defaults; the default policy selection is I1's and C4's (M3P:182), carried here with `DEFAULTED` provenance |
| 2 user-global | `I/host/settings.json` (lead decision; below) | always; absent is no layer | **semantic:** `analysis.budget` only. **Operational:** `retention.*`, `ui.color`, and whatever S-OP-5 admits (item 7). Any other key refuses `CONFIG.INVALID`; it is never silently ignored |
| 3 project | `<root>/opensip.json` (`project_admission.rs:34`) | always; absent is no layer | every PCS section |
| 4 interactive local | `<root>/.opensip/local.json` | interactive invocations only (item 3) | the same fields as layer 3 (HFC:167) |
| 5 environment | none | never | none. The layer is a typed constant: empty |
| 6 explicit flags | the host-built document from typed parsed flags | always | at M3 only `--workspace-root`, which maps to `discovery.workspaceRoots` (S3 `explicit-joins`; SL:174-178). The other six shared flags are not configuration (item 23) |

- **The global carrier's location (lead decision).** `I/host/settings.json`: the host-owned subtree under the installation that X2's first registration already creates (X2 item 6 step 3, X2:144-145). It is read through the installation session's private-access judgment, the owner that already judges `project-registry.v2`, never through X2's project premise (X2:39-47). Analysis never creates it. **Rejected:** `I/settings.json` at the installation's top level, which the closed P0 layout does not reserve; any path under H outside I, which would need a second custody owner.
- **Capture by retained descriptor.** The project and local carriers are read from the **same descriptor** whose custody S3 judged, at most 4 MiB, and their full metadata sample joins the held-fence recheck set. That is X2 r9 item 3a (item 21). A file reopened by name after the judgment is forbidden.
- **Custody refusal** of a project or local carrier is `CONFIG.CUSTODY_REFUSED` (SL:137-138; X2:250-270).

**Basis.** F03:28-31 (CFG-9: "only allowlisted analysis-affecting user-global keys enter analysis resolution"); HFC:163-168 (the preview's carriers and per-layer fields); CH13:52-56 (project decisions are explicit project policy, never adopted on a project's behalf); AQ:107-108 ("CI never probes the interactive local carrier").

**Rejected.**
- A global layer that admits the whole PCS. One user preference would then silently change every project's analysis, which is what CFG-9 forbids.
- Ignoring unknown global keys. AQ:30-31 refuses unknown keys, and no parse fallback may narrow a user's configuration.

**Forbidden.** A carrier read by name after its custody judgment; a global layer that sets `profileId`, `capabilities`, `components`, `discovery`, `policy` or `evidence`; any write to any carrier during analysis (item 15).

**Controls.** A per-layer allowlist matrix covers every PCS leaf against every layer. A swapped-file race between judgment and read refuses on the recheck. A global file with an unknown key refuses.

#### 3. Invocation mode: interactive or CI, never from the environment

**Decision.**
- The resolver takes one typed observation, `InvocationModeV1 { interactive: bool }`.
- The host entry computes `interactive` once: it is true exactly when standard input and standard error are both terminals. Every other invocation is CI (non-interactive).
- In CI the local carrier is never stat'ed, opened, parsed or resolved (HFC:196-197).
- The `CI` environment variable, and every other environment variable, is never consulted.
- J1, the X11 successor, wires the observation. If J1 adds an explicit automation flag, it does so through a CINV successor. The product inventory has no `--ci` today (CINV `sharedFlags`), although the preview had one (HFC:197).

**Basis.** AQ:107-108; SL:111-112 (`ci` is a named host observation); CH13:60 (no hidden environment input); SL:1105 (interactive consent is never in CI).

**Rejected.**
- Reading `CI` or similar variables: a hidden environment input.
- Treating a non-terminal local script as interactive. It would read `.opensip/local.json` in automation that cannot see it.

**Forbidden.** Any environment input to the mode; probing the local carrier in CI, including malformed or hostile local bytes rejecting a CI run (HFC:196-197).

**Controls.** A hostile `local.json` (malformed, oversized, wrong custody) has no effect in CI, and the trace shows no `lstat`. An interactive run consumes a valid `local.json` with layer-4 provenance.

#### 4. The resolution pipeline and its refusals

**Decision.** The resolver is pure over captured bytes and typed observations. It runs these steps in this order:
1. **Lexical admission** of each carrier: duplicate keys, Unicode, depth, size, exact integers and end-anchored patterns (AQ:10-41).
2. **Schema:** PCS v2, closed, with `schemaVersion` 2 (PCS root `additionalProperties: false`). Schema-one carriers go through item 11. An unknown key or schema major refuses (AQ:30-31).
3. **Per-layer allowlist** (item 2).
4. **Merge** (item 1).
5. **Logical paths.** `.` is the only root sentinel, and only for `workspaceRoots` and `ignorePaths`. `entryPoints` names a concrete source path. An explicit `workspaceRoots: []` refuses (AQ:112-118; PCM:23-27; PCS `minItems: 1`).
6. **Registry admission** (item 8):
   - the profile (`CONFIG_PROFILE_MISSING`, `CONFIG_PROFILE_UNREGISTERED`; AQ:334-335);
   - capabilities: membership of the NCM vocabulary, and a cell that is not `NOT-SELECTED` (AQ:62-74);
   - packs, through X12's `admit_policy_selection`, unchanged (`configuration.rs:42-58`);
   - waivers: the registry is empty at M3, so any waiver ID refuses;
   - component duplicates and pin/hold conflicts (AQ:118-120).
7. **Defaults completeness.** Missing compiled capabilities or budget is the host invariant `CONFIG_DEFAULTS_INCOMPLETE`, never a second zero-config spelling (AQ:134-137).
8. **Partition** into semantic and operational values by the classification registry (items 7 and 8).
9. **Normalize** semantic arrays to canonical sets by canonical item bytes. `components.allowedScopes` keeps its declared priority order (AQ:164-167; PCM:42-48).
10. **Validate** the semantic record against `identity-schemas.v3#/$defs/semantic-configuration` (AQ:158-159; the product copy is in `schemas/sources/identity-v3.schema.json`).
11. **Digest** (item 6).

**Refusal rows** (no new code):
- Invalid external input is `CONFIG.INVALID`: request-rejected, exit 2, with the existing details (AQ:28-30; SL:1302).
- Carrier custody is `CONFIG.CUSTODY_REFUSED` (SL:1302).
- An invalid compiled default, environment layer or host-built flags document is the host-invariant row, as X12 row 4 shapes it (`configuration.rs:102-110`).

**Lead decision: the `CONFIG.INVALID` remedy needs a successor.** The one remedy keyed to `CONFIG.INVALID` names only capability and policy selection (`configuration.rs:21-24`; X12-0). A bad path in `opensip.json` would receive that text. This law requires a remedy-text successor, through X12-0's route, that covers configuration documents generally (successor S9). **Rejected:** reusing the misleading text, or minting a new code, which the owner's no-new-codes rule forbids. **(r3)** S9 is design unit B-S9, accepted by Grok and bound at product `8adfe0c`. It carries the remedy, through X12-0's route, as complete successor copies of the two native-model files (BS9, "The change" and "The form"). B1-a embeds its string (item 25; units table).

**Basis.** AQ:8-41, AQ:102-173, AQ:330-335; PCM:9-51 (the reference resolver).

**Forbidden.**
- Schema validation after the merge, or a merge before every layer is admitted (AQ:26-28).
- Sorting before duplicate detection, so that a conflict is erased (HFC:191-193).
- A parse fallback that narrows a user's configuration (AQ:31-32).

**Controls.**
- AQ:183-187's retained cases: no-config mixed-native selection; explicit-entry override; exact schema numbers; unknown capability or path refusal; CI local non-consumption; semantic-versus-operational digest.
- Cross-implementation byte vectors. The design repo's PCM computes the expected `resolvedConfigDigest` for each fixture, and the product test pins the hex.

#### 5. Provenance

**Decision.** The resolver also returns a host-internal `ResolvedConfigurationV1`: the semantic record, the operational record, and per-leaf provenance. Each provenance entry carries:
- the deciding layer, one of `defaults|global|project|local|environment|flags`;
- the winning value;
- the carrier: its path relative to the root or to I, the SHA-256 of its exact bytes, and its source schema version (1 or 2);
- for a defaulted leaf, `DEFAULTED` or `DISCOVERED:<recognizerId>@<version>` with the evidence paths and digests.

Provenance is retained apart from source blobs. It never enters any digest. Doctor (OPP:354) and M4's disclosure read it.

**Basis.** AQ:109-110 ("Winning value, source layer and discovery evidence remain explainable"); AQ:172-173; the product's `configuration-disclosure-v1` declares "raw-layers-and-winning-layer-provenance-not-in-this-projection" in its `limitations` (`schemas/sources/configuration-disclosure-v1.schema.json`; registry row `schemas/registry.json:60-66`).

**Rejected.** Folding provenance into the semantic record. Moving a value from one layer to another would then change the Plan with no semantic change.

**Forbidden.** Secret values in provenance (F03:47-50); environment names or values in provenance (there are none to record).

**Controls.** The same value moved between layers keeps the digest, while its provenance differs.

#### 6. `resolvedConfigDigest`: what it covers and what it excludes

**Decision.**
- **The recipe.** `resolvedConfigDigest` = lowercase hex SHA-256 of the canonical bytes of the normalized semantic record. It is a raw digest, not an H-identity: AQ:167-168, IE:518-519, and PCM:51 (`hashlib.sha256(C.canonical(semantics))`).
- **It covers** exactly the five sections, `analysis`, `components`, `discovery`, `policy` and `evidence`, all always present, with an empty section spelled `{}` (AQ:128-133). `analysis` always holds `profileId`, `capabilities` and the complete budget. Other fields are present exactly when a compiled default or an explicit layer selected them (AQ:155-157, read with item 1).
- **It excludes:**
  1. all provenance (item 5);
  2. the operational record: `retention.*`, `ui.*`, and every future S-OP-5 field (AQ:168-170; item 7);
  3. transport and presentation: `--format`, the client correlation ID and the RequestId;
  4. selection and authorization inputs: `--project`, `--ephemeral`, `--trust-group`, `--trust-project-owner`, `--allow-backup-custody`, `--yes-policy` (item 23) and the invocation mode (item 3);
  5. the environment, which is empty;
  6. everything discovery produces: units, membership, recognition, D15 members and links. These bind through `membershipDigest`, `FrameworkRecognitionPlanV1`, `scopeDigest`, `vcsDigest` and the native contexts (AQ:170-172; IE:179, IE:182);
  7. carrier bytes and paths;
  8. secret values (F03:47-50). None exist at M3.
- `snapshot2` and `plan2` bind the digest as "resolved config" (IE:179, IE:182).

**Basis.** As cited in each clause.

**Rejected.**
- An H-identity with a domain tag. That would contradict AQ:167-168 and every retained `resolvedConfigDigest` pattern (`^[0-9a-f]{64}`, configuration-disclosure-v1).
- Including provenance or operational values, which AQ:168-170 forbids.

**Forbidden.** Any operational, presentation, authorization or environment value reaching the digest; a digest over un-normalized arrays.

**Controls.**
- Invariance: varying only excluded inputs gives the same digest.
- Sensitivity: varying any semantic leaf changes it.
- Permutation: input array order does not change it, except `allowedScopes`.
- The five sections are always present.
- PCM byte vectors (item 4).

#### 7. The nonsemantic operational partition: S-OP-5's lawful place, undecided

**Decision.** B1 builds the operational partition and its rules. It decides none of S-OP-5's names, sections, defaults or bounds (OPP:226, OPP:396, OPP:411). The rules:
- **O-1.** An operational field exists only when an accepted PCS successor names it and the classification registry (item 8) marks it `host.operability.nonsemantic` (DRC:587-596). PCS is closed and has no logging section (OPP:226).
- **O-2.** It uses the same six layers and the same provenance. Its per-layer allowlist is the successor's. B1's default for an unclassified future field is refusal.
- **O-3.** It never enters the semantic record, `resolvedConfigDigest`, `snapshot2`, `plan2`, a provider request or frame, Coverage, or any retained Run record. It may appear only in the operational record (OPP:249) and diagnostics.
- **O-4. Admissibility test.** A field is nonsemantic only if a control shows the same Plan inputs, facts, Coverage and findings across its admitted values. OPP:277's concurrency control is the model. A field that fails the test is either a release constant or a semantic budget (OPP:227).
- **O-5.** No environment input, ever (CH13:60; OPP:139).
- **O-6.** No secret value (F03:47-50).

**Basis.** DRC:587-596 ("`host.operability.nonsemantic` ... is permitted only for an explicitly host-reviewed operability field and cannot hide an analysis input"); OPP §3.5 (OPP:226-227); OPP §9's S-OP-5 row (OPP:411).

**Rejected.**
- Pre-defining an `operability` section here: that pre-empts S-OP-5.
- Overloading the existing `retention` section, which "governs the store and is not overloaded" (OPP:226).

**Forbidden.** An operational field without its classification row; an operational value in any semantic carrier; an operational field read from the environment.

**Controls.** The classification drift check (item 8) covers new fields automatically. B1-a ships an invariance-control template that S-OP-5's unit instantiates per field.

#### 8. FW-13: one registry, generated or drift-checked, typed refusal

**Decision.** Every vocabulary the resolver and discovery consume comes from one host-owned declaration source. It is generated or drift-checked, and an unknown record refuses typed.

| Registry | Source of truth | Product form | Drift check | Unknown value |
|---|---|---|---|---|
| Config2 input schema | PCS | new pinned source `schemas/sources/product-configuration-v2.schema.json`, with a `schemas/registry.json` row naming `crates/host/src/configuration.rs` as validator | the existing schema-pin checks, as for `configuration-disclosure-v1` (`schemas/registry.json:60-66`) | `CONFIG.INVALID` |
| Semantic record | IDS `semantic-configuration` | already in `schemas/sources/identity-v3.schema.json` | existing pin | host invariant |
| Field classes | PCS leaves × the two DRC classes | a generated table built from a reviewed mapping file | a test: every PCS leaf has exactly one class, and no row names a non-leaf | the build and test fail |
| Capability IDs | NCM `#/capabilities[].id` (AQ:62-66) | a generated enum | pin of NCM | `CONFIG.INVALID` |
| Capability availability, profiles | the authenticated release declaration registry (AQ:55-77) | an admitted input; tests use a `cfg(test)` synthetic registry | signature | disclosed (AQ:88-99) or `CONFIG_PROFILE_UNREGISTERED` |
| Policy packs | X12's `pack-registry.json` | existing | existing | X12 rows 1-4 |
| Waivers | none at M3 | empty | — | `CONFIG.INVALID` |
| Framework recognizers | NE §8's nine IDs (NE:2758-2760) | a generated enum | pin of NE | host invariant |
| Workspace declaration readers (D15) | this law's successor S3 (item 20) | a closed enum | pin | host invariant |
| Shared flags | CINV `sharedFlags` (seven) | a generated enum with each flag's class | pin of CINV | the CLI refusal (M4) |

**Basis.** SMAP:66 (FW-13: "generated or drift-checked projections and typed refusal of unknown records"); CH13:245-262; COV:8104-8121 (owner `crates/host/src/configuration.rs`).

**Rejected.** Hand-maintained lists in the resolver. The preview resolver's hand-coded partition (PCM:38-41) is reference evidence, not a product source.

**Forbidden.** A field, capability, recognizer or flag known to code but absent from its registry; a registry row with no code consumer; an unsigned capability claim (CH13:249-251).

**Controls.**
- Mutation tests: add a PCS leaf with no class (fails), remove a recognizer from code (fails), and rename a CINV flag (fails).
- One negative test per registry for an unknown value.

#### 9. No environment side channel

**Decision.**
- The resolver, discovery, the declaration readers and `grants.rs` read **no** environment variable. That includes `HOME`, `PATH`, `CI`, `NO_COLOR` and `TERM`.
- The account home comes from the account database (SL:107-109).
- The one environment read on these paths stays X2's refusal-only Git check (X2:192; `git_tracking.rs:321-346`), which never selects or relaxes anything.
- **Enforcement.** `clippy::disallowed_methods` for `std::env::{var, var_os, vars, vars_os}` in `crates/host` and `crates/security`, with an audited exception list. The list holds exactly `git_tracking::process_environment` and the test-only crash-matrix seams (`crates/platform/src/crash_barrier.rs`, which is outside these crates). A planted read is the negative control.

**Lead decision: the resolver gets no exception.** OPP §7 lists the configuration resolver among the audited exception owners (OPP:365-367). With layer 5 constant-empty, an exception would only open a side channel. M3-O records the refinement (finding F7).

**Basis.** CH13:59-61; AQ:107 ("The environment semantic layer remains empty"); SL:107-109; OPP:139 (F11, telemetry and limits by environment variable are forbidden).

**Rejected.**
- Honouring `NO_COLOR` for `ui.color: auto`. It is a common convention, but it would be the first environment input. If wanted, S-OP-6 can admit it as a declared operational input.

**Forbidden.** An environment read anywhere on the configuration or discovery path except X2's refusal-only check; a configuration value spelled into an environment variable for a child (that is the D law's, ML item 17).

**Controls.** The structural check and its planted negative control. A run with hostile `HOME`, `PATH`, `CI` and `XDG_*` values produces byte-identical resolution and discovery records, except where X2's refusal-only Git check refuses.

#### 10. Amendment to X12 r3 item 8: the order of pack admission

**Decision.** X12 item 8's "before: X1 write admission, X2 project admission or any fence" (X12:125-130) becomes:
- Pack admission runs **immediately after configuration resolution**. Resolution runs immediately after S3's selection walk and the carrier captures.
- It precedes X2's registry capture (X2 item 5) and every later step of project admission: registration (X2 item 6), any lease (X2 item 7), and every effect.
- It also precedes everything else X12 item 8 lists: provider spawn, snapshot, semantic universe, consumption of facts or Coverage, Plan construction and evaluation.
- It may therefore follow the fence acquisition of the 458c read session or the 468/X1 write gate, the selection walk, and the carrier reads.

**What stands, and what S2 withdraws (r2, RF-2).**
- Everything else in X12 r3 stands: rows 1 to 4, the `Supplied` refusal of bundled bytes, the `cfg(test)` registry, `check_plan_pack`, X12d, and item 8's rule that admission is pure, with no I/O, no lock and no ledger charge (X12:125).
- Of I1's M3 amendments to X12 (I1:379-386), the three row-count changes **stand** (I1:381-384).
- **I1:386's clause that X12 r3's order stands is withdrawn by S2.** I1:386's other clauses stand: rows 1 to 4, the `Supplied` refusal, the `cfg(test)` registry, `check_plan_pack` and X12d.
- This item never cites I1:379-386 as standing in full.

**S2's text (X12 r4, item 8).** This is the exact passage that replaces X12 r3's "the host runs `admit_policy_selection` first in an analysis request, before: X1 write admission, X2 project admission or any fence; …" (X12:125-130). The rest of item 8 (X12:132-138) stands, including the rule that the Plan builder takes the policy only from an `AdmittedPack` (X12:134), with one reading fixed: X12:136's "it is pure and runs before any custody" now means that admission itself performs no custody, because S3's selection judgment precedes it. X12:136's correction that X12 does not depend on X1 stands.

> **8. Order: pure, and before every effect (X12 r4, by M3-B item 10).** Pack admission does no I/O, takes no lock and is not charged to any ledger. The host runs `admit_policy_selection` immediately after configuration resolution, which runs immediately after S3's selection walk and the configuration carrier captures. It runs before X2's registry capture (X2 item 5) and every later step of project admission (registration, item 6; any lease, item 7), before any effect, and before any provider spawn, snapshot or semantic-universe construction, consumption of facts or Coverage, Plan construction and evaluation. It may follow the fence acquisition of the 458c read session or of the 468/X1 write gate, the selection walk and the carrier reads, all of which write nothing. A refusal therefore still leaves the record DR-G24 asks for and has nothing to clean up.
>
> **Withdrawal recorded.** This r4 order supersedes X12 r3 item 8's "before … X1 write admission, X2 project admission or any fence" (X12:126) and the ordering sense of X12:136's "runs before any custody". It also **withdraws the clause "the order" from M3-I1 r2 item 7's statement that "Everything else in X12 r3 stands"** (I1:388). The rest of I1:388's list, and I1:383-386, stand.

**Basis.** The pack ID can come from the project layer (AQ:47-52, the `policy` section). The project carrier is located and judged only by the selection walk, which runs under the fence (X2:68, X2:74). X12's rationale still holds: a refusal leaves DR-G24's record, with no evaluation, no `policyOutcome`, no facts or Coverage and no universe, and "nothing to clean up" (X12:132). Selection and the carrier reads write nothing, and dropping the session releases the fence.

**Rejected.**
- Reading the carriers before the fence. That reverses X2's charged, fenced selection (X2:68) and opens a gap between the read and the fenced admission.
- Allowing policy selection only from defaults and flags. It contradicts Config2's project-level `policy.packIds` (AQ:47-52).
- Admitting twice, once before the fence for flags and once after selection. It doubles the path and needs the same amendment anyway.

**Forbidden.** Pack admission after any registry capture, registration, lease or effect.

**Controls.** For a refused project-layer pack ID: no registry read, no RESERVED row, no lease, no journal, the session released, and X12 row 1 returned.

#### 11. Schema-one carriers

**Decision.**
- A `schemaVersion: 1` global, project or local file is admitted only through the exact preview carrier schema and lexical admission (HFC:150-158).
- It is projected in memory onto version-2 fields with `sourceSchemaVersion: 1` provenance. The mapping is 1:1 for `analysis.budget`, `components.request`, `components.pins`, `components.holds`, `components.allowedScopes` and `ui.color` (HFC:163-168).
- Any other version-1 field refuses. No file is rewritten. No grant is inferred.
- The preview's compiled defaults are never product defaults.

**Basis.** AQ:175-181.

**Rejected.** An automatic in-place migration. A migration is "a reviewable data patch through the workflow's configuration-write authorization, not a side effect of analysis" (AQ:179-181).

**Forbidden.** Rewriting a schema-one file; reading a version-1 field outside the mapping.

**Controls.** A round trip of each mapped field. Each unmapped version-1 field refuses. The file's bytes and mtime are unchanged after resolution.

### B. B2, discovery

#### 12. Where discovery runs, and its ledger

**Decision.**
- **Upward selection stays X2b's**, under the fence, as built (`project_admission.rs:303-384`).
- **Downward unit discovery and the D15 member observation** run **after** the installation fence is released, through X2's handoff (X2:231-248) or the read session's equivalent release. They run over the root descriptor that the operation context retains.
- **Discovery ledger profile (lead decision).** They are charged to one **discovery ledger** per invocation. It is created once, after the handoff, and never recreated after a failure (`work_ledger.rs:1-8`).
- **Its caps.** Its profile raises the platform's hard caps for this ledger only. A new constructor in `crates/platform/src/work_ledger.rs` is needed, because `with_limits` can only lower the caps (`:205-213`). Provisional caps: 2^20 objects, 2^21 edges and 2^30 bytes.
- **Measuring the caps.** Before B2-b lands, the harness counts directories and entries outside pruned segments for every pinned T2 tree, from `git ls-tree` with no repository code (T2F:41-55). B2-b's test records those counts and shows at least a 2× margin for every T2 entry. If any entry fails the margin, the caps return to this law for revision. **The census bounds objects and edges only (r2, NBO-1).** Bytes are bounded separately: by item 19's member cap together with X2:272's ceilings (4 MiB per index, 64 KiB per Git config) and S3's 4 MiB file-custody limit on marker and carrier files (SL:126-127).
- **Exhaustion** is `WORK.BUDGET_EXHAUSTED` (X2:268). It is never truncation (NE:871-878).

**Basis.** X2:231-248 (the fence is released after the handoff); SL:250-252 (observation bounding is the observation-admission owner's); SL:313-315 (per-read custody re-checks protect the later reads); `work_ledger.rs:12-13`, `:205-213`.

**Rejected.**
- **Running the downward walk under the held fence.** A walk whose length grows with repository size would hold every project's writers behind it.
- **Charging the walk to the session's ledger.** At 131,072 edges it cannot hold T2's large entries.
- **A silent partial walk.** That is truncation, which U-7 forbids.

**Forbidden.** Retrying on a new ledger after exhaustion; any downward walk under the installation fence; a discovery cap that truncates.

**Controls.**
- Exhaustion at exactly the cap, and one below it.
- A T2 census test of the margin.
- A recheck failure between `lstat` and `open` refuses, never retries (SL:313-315).

#### 13. The S3 boundary, implemented

**Decision.**
- B2-b implements S3's downward instrument natively, in `crates/security/src/custody.rs` and submodules (the SL:3 owners, COV:6702).
- B2-a provides the shared rule (item 14, U-4a) as **one** pure implementation, `crates/security/src/custody/discovery_rule.rs`. The host's native unit instrument consumes the same functions; neither restates them (SL:187-190).

The instrument's obligations:

| S3 obligation | Implementation |
|---|---|
| Directory custody (SL:121-126) and config-file custody (SL:126-127) | `judge_project_object` (`crates/security/src/custody/project_chain.rs:422-438`), under X2 r9 item 1's scope |
| `--trust-group` and `--trust-project-owner` (SL:127-130) | typed authorizations from `grants.rs` (item 23); configuration can grant neither |
| Unit sources and precedence (SL:174-185) | `explicit-joins` > `config-workspace-roots` > `automatic`, as an exclusive choice: a present admitted `discovery.workspaceRoots` array, from either tier, never falls through to automatic discovery (SLM:771-785; AQ:115). Discovery is then restricted to exactly those roots, never widened into a scan (NE:917-921), and it also suppresses D15 reader membership (item 20). A custody failure refuses for either explicit tier and excludes for the automatic one |
| Pruning by exact segment before any custody walk; one row per outermost anchor; never descending (SL:187-216) | production rows are always `markerCountBasis: not-enumerated` with `markerCount: null` (SL:206-211) |
| 4096 first-party unit cap; installed dependencies never counted (SL:216-222) | `PROJECT.WORKSPACE_UNIT_LIMIT` / `REQUEST.UNSATISFIABLE` with detail `WORKSPACE_UNIT_LIMIT:<n>><cap>` (SL:1303) |
| Explicit roots are exact roots (SL:224-249) | `normalize_explicit_root`; the `JOIN_*` refusals; the marker-less warning `EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER` |
| Depth bound of 256, exclusion `DEPTH` (SL:246-250) | the same constant as the upward walk (`project_admission.rs:44`) |
| Nested repositories and nested projects recorded, never entered (SL:146-157, SL:163-168) | unchanged, except for declared D15 members (item 22) |
| `.git` indirection is data, never followed (SL:159-161) | unchanged |
| The pruned-tree read set (SL:266-279) | C1's join; B2 exports the anchors |
| The admitted boundary inventory (SL:281-311) | `boundary_inventory(result)` produces `AdmittedBoundaryInventoryV3` for every project **(r4, RBS3 NBO-1)**, as B-S1 LD-4 makes version 3 the current discovery record because the SX-1 anchor is on every project (SLS `schemas.AdmittedBoundaryInventoryV3`; SL:286 and NE:4135 as overridden by B-S1) |
| Native custody (SL:313-315) | ACL reads, reuse of the O_NOFOLLOW handle, and the `st_dev`/`st_ino` re-check |
| Backup custody before the first source-derived write (SL:317-331) | the admission function is in `grants.rs` (item 23). J3 calls it at the first source-derived write. Law 464's constant-UNKNOWN classifier admits with `unknown-disclosed` |

**Output.** The closed `DiscoveryProvenanceV3` (SLS `schemas.DiscoveryProvenanceV3`) for every project (B-S1 LD-4).

**Basis.** SL:105-332; COV:6702-6716.

**Rejected.** A second, host-side copy of the shared rule. SL:187-190 states the rule once, and DD's entry points (`DD:80-367`) are the reference.

**Forbidden.** Following a symlink or a `.git` file; descending into a pruned tree for any reason; an ignore list supplied by a caller standing in for the boundary inventory (NE:841-842); a config "project list" or more than one `--project` (SL:261-262).

**Controls.**
- Every case in `security/discovery-cases.v1.json`, replayed natively, including the named sweeps:
  - `discovery-prunes-installed-dependencies-and-refuses-real-cap-typed`: 4200 installed manifests admit; 4200 first-party directories refuse; exactly 4096 admit;
  - `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`.
- Test owner: `crates/host/tests/discovery_tests.rs` (COV flag rows; CH14:498).

#### 14. U-0 to U-9 as implementation obligations

**Decision.** The host's native unit instrument, in `crates/host/src/discovery.rs`, implements NE §1.4 exactly:

| Rule | Obligation | Test |
|---|---|---|
| **U-0** (NE:637-662) | `admit_unit_roots` runs before membership, slicing or enumeration binding. Internal roots use `""` and canonical relative directories. A malformed internal root is the host invariant `NATIVE_UNIT_ROOT_REPRESENTATION`; a malformed external root is `native.explicit-root-grammar` | a `.` internal root refuses before any membership |
| **U-1** (NE:663-673) | One unit per directory and language family. TS/JS precedence is `tsconfig.json` > `jsconfig.json` > `package.json`, using the effective `allowJs` (NE:169-180). Co-located `rust` and `tsjs` units are both kept | `units-colocated-cargo-and-package-json-root-keeps-both-languages` |
| **U-1, effective `allowJs`** | Reading the `tsconfig` `extends` graph as data needs a first-party, bounded JSONC reader (lead decision). **C2's `TypeScriptConfigProjectionV2` must call the same function**: one implementation. No TypeScript runs before the Plan. **Rejected:** a crate, which needs a dependency-policy row for a small grammar; running `tsc`, which is a provider launch before the Plan | the extends chain, comments and trailing commas; a cycle refuses |
| **U-2** (NE:674-685) | Cargo workspace folding, parsing `Cargo.toml` `[workspace]` as data with the pinned `toml` crate (`crates/identity/Cargo.toml:15-17`). Explicit roots keep folding | `units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning` |
| **U-3** (NE:686-692) | Family by extension; the deepest unit of the file's own family wins | `units-nested-monorepo-deepest-within-language-and-workspace-folding` |
| **U-4** (NE:693-702) | Each inventory file is in exactly one row. `erasedFiles` is empty | a membership that covers the inventory other than exactly once refuses |
| **U-4a** (NE:703-743) | The shared rule, from B2-a only | `units-4200-installed-package-manifests-are-one-pruned-tree-not-a-cap-refusal` |
| **U-4b** (NE:744-815) | Markers, units, order, ordinals, rows and `membershipDigest` exactly as stated. Run closure re-derives them (`ENUMERATION_MEMBERSHIP_ORDER`, `ENUMERATION_MEMBERSHIP_ROW_DERIVATION`) | the nested-workspace fold; out-of-order mutations |
| **U-5, U-6** (NE:864-870) | Unchanged. Per-unit joining, with `narrowed=false` checked. Cross-unit edges are `external-module-boundary` on the importing side. **D15 does not change U-6** (finding F4) | owned by H and J; B supplies the unit records |
| **U-7** (NE:871-878) | The 4096 first-party cap, shared with security | as in item 13 |
| **U-8** (NE:816-863) | `require_admitted_boundaries`: the authoritative composition refuses with no inventory (`native.admitted-boundaries-required`). The subset test over `(path, reason)` gives `native.boundary-inventory-mismatch` / `REQUEST.PRECONDITION_FAILED`. Every anchor enters `excludedPathPrefixes`. D15's change is item 22 | `units-nested-repository-and-nested-project-are-excluded-*`; `units-boundary-inventory-whose-pruned-trees-disagree-*` |
| **U-9** (NE:879-905) | Exactly one syntax-only `DEFAULTED` unit when no `rust` or `tsjs` unit survives and the root is not at or below a boundary. It changes no row and is not counted toward U-7. Mixed repositories get no fallback. Zero units is the host invariant `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT` | a repository of bare `.py` and `.md` files; a mixed repository |
| **Config2 join** (NE:907-931) | Explicit roots are exact. A root without a marker is `CONFIG.INVALID` (`native.explicit-root-without-marker`). `ignorePaths` remove whole segments | `units-explicit-config2-workspace-root-without-marker-is-config-invalid` |
| **Scope descriptor** (NE:933-948) | `unit_scope_descriptor`; at most 1024 roots, otherwise `PROJECT.SCOPE_LIMIT` (SL:1323) | 1025 unit roots refuse without truncation |
| **Default selection** (AQ:76-99) | Every capability that is not `NOT-SELECTED` is requested per unit. An unavailable one is disclosed on `CommandEnvelope.availability` | covers the six `inventory/*` modes (COV:4226-4391) |

**The six `inventory/*` cells** (`ts-tsconfig`, `js-allowjs`, `js-synthesized`, `rust-cargo`, `rust-cargo-prepared`, `syntax-only`; COV:4226-4391) are owned jointly by `discovery.rs` and `snapshot.rs`. B owns the discovery half: the unit, mode and membership of each mode's T1 fixture. C1 owns the inventory bytes. Under NE:183-205, `rust-cargo-prepared` is read after U-1 yields a `rust` unit, and discovery does not distinguish it from `rust-cargo`. `syntax-only` has no compilation unit.

**Basis.** NE:619-948; COV:7066-7080 (NE:2's owners include `discovery.rs`).

**Rejected.** Any reading of NE §1.2 that mints a unit from a cell (NE:183-205 forbids it).

**Forbidden.** Rounding, truncating, re-deriving boundaries from caller ignores, or normalizing a retained `rootPath` (NE:650-652).

**Controls.** Every named `units-*` case in NE §1.4. The product test cites each case ID.

#### 15. FW-01: zero-config with no implicit effects or writes

**Decision.** Discovery, resolution, recognition and the D15 declaration readers:
- **write nothing**: no file, no directory, no configuration (not even a recommended one), no lockfile, no index, no `.opensip` (first registration is X2c's, under write admission only);
- **acquire nothing**: no network, no download, no install, no grant (AQ:346; AQ:342);
- **execute nothing**: no process, no repository code, no script, hook, build script, plugin or workspace glob program (AQ:345; SL:183-185);
- **read manifests as data** through exact parsers (NE:2762-2764).

A missing analysis closure is a prerequisite failure, never a fetch (CH13:47-49).

**Basis.** SMAP:54 (FW-01: "no implicit effects/config write"); COV:7852-7869; CH13:44-84; AQ:52-53 ("No configuration field executes code, imports ambient evidence, grants permission, selects an unregistered capability or rewrites a policy file").

**Rejected.** A "helpful" write of a discovered `opensip.json`. Applying a recommendation is a separate host operation with normal write authority (CH13:66-70).

**Forbidden.** Any `std::process`, socket or write API in `discovery.rs`, `configuration.rs`, `custody/discovery_rule.rs` or `grants.rs`, by structural check (OPP §7 at OPP:365-372).

**Controls.**
- **The read-only-tree control.** Discovery over a tree of 0555 directories and 0444 files gives byte-identical records to the same tree writable.
- **The canary control.** A fixture holds `build.rs`, a `postinstall` script, a `.cargo/config.toml` with `build.rustc-wrapper`, a `.npmrc` and a `pnpmfile.cjs`, each naming a canary path. No canary path is touched.
- **The structural check**, with planted negatives for spawn, socket and write.

#### 16. Framework recognition, host side (NE §8)

**Decision.**
- The host runs all nine recognizers (NE:2758-2760) before the Plan, over manifests as data.
- It produces one `FrameworkRecognitionV1` per `rust` or `tsjs` unit. C4 commits them in `FrameworkRecognitionPlanV1` (`schemas/sources/framework-recognition-plan-v1.schema.json`; validator `crates/host/src/plan.rs`, `schemas/registry.json:132-138`).
- **FR-1 to FR-5 hold exactly:**
  - a config that needs evaluation (`next.config.js`, `vite.config.ts`) yields `unresolvedChoices: ["config-requires-evaluation"]` and `entryPoints.state=partial`;
  - every effect carries `DISCOVERED:<id>@<version>`, and explicit configuration wins;
  - an unrecognized framework gives `observedHints`, `state=none` and `resolution-incomplete` universal negatives, with no refusal;
  - the bounds are 32 recognizers per unit, 64 evidence files per recognizer and 65,536 entry points per unit;
  - a version change is Plan-visible.
- **The provider side** (`providers/typescript/src/framework-recognition.ts`, the second owner at COV:7245-7250) **consumes** the committed recognition and never recognizes on its own authority.
- **Readers (lead decision).** `package.json` uses exact JSON admission (AQ:8-41), and `tsconfig` uses the JSONC reader of item 14. `Cargo.toml` uses the pinned `toml` crate. `pnpm-workspace.yaml` uses a **closed YAML subset reader**, for a `packages:` sequence of plain or quoted scalars only, chosen in B2-d under M3-P0's dependency policy. Bytes outside that subset yield FR-1's disclosure and no effect, never a guess.

**Basis.** NE:2750-2777; COV:7245-7259; CH13:59-61 (no provider-private override).

**Rejected.**
- Provider-side recognition. It would be a discovery input that arrives after the Plan from a provider's private reading, which CH13:60 forbids.
- A full YAML dependency for one key.

**Forbidden.** Evaluating any configuration file; reading a recognizer effect from anywhere but the declared files; a recognizer outside the registry (item 8).

**Controls.** One positive case and one `config-requires-evaluation` case per recognizer; the FR-4 bounds at exactly the bound and one past it; an `observedHints` case; a test that pins a recognizer version bump changing the recognition digest.

#### 17. Ambiguity and unsupported regions: how each is disclosed

**Decision.** Each class has one retained typed record, enters the Plan scope where it removes source, and is never Coverage `complete` or a "clean" claim (CH13:61-64; SL:243-245).

| Class | Record | Plan effect |
|---|---|---|
| Pruned dependency, VCS and build trees | `prunedTrees` (SL:187-216; NE:703-743) | `excludedPathPrefixes`; files are `host-ignore-convention` |
| Nested repositories and nested projects | `nestedRepositories`, `nestedProjects`; `excludedUnits` with a reason (NE:828-833) | `outside-project-boundary` rows; anchors are excluded |
| Custody- and depth-excluded units | `excludedUnits` (`DIRECTORY_CUSTODY:*`, `MARKER_CUSTODY:*`, `DEPTH`; SLS) | explicit unknown required scope, never examined-clean (SL:243-245) |
| Unsupported files | `unsupported-file` / `no-bundled-grammar` (NE:693-702) | inventoried, never analyzed |
| Files with no unit of their language | `syntax-only` / `no-program-unit-for-language` | no syntax, clone or semantic claim unless explicitly requested (NE:893-899) |
| Configs that need evaluation; unrecognized frameworks | FR-1 `unresolvedChoices`; FR-3 `observedHints` | `entryPoints.state` is `partial` or `none`; reachability negatives are `resolution-incomplete` |
| Capabilities this release does not declare | `CommandEnvelope.availability` notices (AQ:88-99) | advisory; no Coverage is minted |
| D15 ambiguity (item 20) | `DiscoveryProvenanceV3.workspaceDeclarations[].unresolved` | no member and no link is added |

**Rule.** Where two readings exist, discovery takes neither the broader nor the weaker one silently. It records the choice and selects the narrower scope. Silent narrowing of a *required* scope is itself forbidden (NE:867-868). The narrower scope is therefore disclosed as unknown required scope, never as absent.

**Basis.** CH13:61-64 ("ambiguity is disclosed rather than silently selecting a broader or weaker interpretation. Ignored and unsupported regions are scope information, never evidence that those regions are clean"); AQP:116 cites WS:467 for "zero findings never establish complete analysis".

**Rejected.** A best-effort pick, such as the first matching manifest or the most common framework.

**Forbidden.** Coverage `complete` over any excluded or unknown region; omitting a class from the records because it is empty (an empty list is still present).

**Controls.** Zero findings over an excluded region never yields complete Coverage. Each class's record appears in a golden fixture.

#### 18. Recommendation evidence for M4

**Decision.** `discovery.rs` exposes one pure function that returns the recommendation evidence CH13:67-73 names: detected evidence, proposed settings, default rationale, unresolved choices and the effect of each choice. Proposed settings are validated by the **actual** resolver of item 4 (CH13:69-71). M4's `recommend` command (BP:952) renders it. M3 wires no command (M3P:301).

**Basis.** CH13:66-75; AQ:345 (metadata discovery and recommend run no hooks or probes).

**Rejected.** Deferring the function to M4. The resolver check is easiest to prove now, while B1 is fresh.

**Forbidden.** Writing a recommendation; proposing a setting the resolver refuses.

**Controls.** Every proposed setting round-trips through the resolver; applying none of them changes nothing.

### C. B3, multi-repository workspaces (D15)

#### 19. The admitted shape

**Decision.** A **multi-repository workspace** is an admitted project whose selected root **W** satisfies W1 to W3, with 1 to 64 **member repositories** M that satisfy M1 to M5.

- **W1.** S3 selects W in `config`, `explicit` or `cwd-default` mode. `vcs-default` cannot occur, because it means W is itself a repository root (SL:141-144).
- **W2.** X2's enclosing tracking observation for W is `NoRepository`: no VCS marker at W or at any ancestor up to `/` (X2:209; `git_tracking.rs:587`, `:721`).
- **W3.** W passes X2 items 2 and 3 unchanged: strictly below H, on H's volume, and chain custody (X2:51-72).
- **M1.** M is a directory strictly below W. It is reached without symlinks, on W's device (no mount change), at a depth of at most 256 segments.
- **M2.** M holds `.git` as a directory and no other VCS marker. No directory strictly between W and M holds a VCS marker or `opensip.json`. M is not at or below `W/.opensip`.
- **M3.** Members are disjoint: no member is at or below another.
- **M4.** M passes X2 r9's member observation (item 21).
- **M5.** M is declared (item 20).

**References between packages:**
- **by path:** a Cargo `path` dependency, or an npm `file:` or `link:` specifier, resolving inside another member. That is DS-4, "Path dependencies live in the snapshot" (NE:1687). No link row is needed;
- **by version:** a registry requirement on a package that exactly one member provides, linked by a declaration (item 20). Satisfaction is decided **per consumer** by that ecosystem's resolver (item 22). An unsatisfied requirement keeps resolving outside the workspace, exactly as T2's edge rule says (T2R:191-195; T2F:118-119).

**Not admitted** (each typed and disclosed; item 24):
- W itself a repository, including a superproject with submodules;
- a member whose `.git` is a file (a submodule checkout or linked worktree);
- a member below a symlink or on another volume;
- more than 64 members;
- Python links (D9).

Nested repositories inside a member (its submodules or clones) stay boundaries. Undeclared nested repositories under W stay boundaries.

**The T2 reference shapes** (T2M:7752-10327; T2R:187-221):

| Workspace | Ecosystem | Members | Links (T2 overlay) | Declaration at W | Expected at M3 |
|---|---|---:|---:|---|---|
| `mr-rs-medium-serde-json` (T2M:7754) | cargo | 2 | 3 | `cargo-config-patch@1` | linked; Cargo honouring needs successor S5 |
| `mr-rs-large-aws-lambda-tokio` (T2M:7865) | cargo | 8 | 16 | `cargo-config-patch@1` | as above |
| `mr-ts-large-smithy-powertools` (T2M:8952) | npm | 2 | 5 | `npm-workspaces-members@1` | linked; TS resolution needs successor S6 |
| `mr-ts-very-large-smithy-sdk` (T2M:9097) | npm | 2 | 20 | `npm-workspaces-members@1` | 20 links; its 36 `none` and 2 `unknown` edges stay outside |
| `mr-py-medium-boto` (T2M:10263) | python | 2 | 1 | none at M3 (D9) | pinned, not analyzed |
| aws-cdk against aws-sdk-js-v3 at HEAD (T2R:306) | npm | 2 | — (33 unresolvable edges) | `npm-workspaces-members@1` | the negative case: unsatisfied requirements stay outside. Recorded, not built, in T2; B3-c builds it |

**T2 assembly has no `.git`** (T2F:56-62). So T2 exercises the declarations, links and multi-unit discovery, but not member custody. Member custody is exercised by Git fixtures in B3-b's tests, by T2 record successor S8's optional `git-conventional` assembly mode, and by T3.

**Basis.** AQP:225 and AQP:556 (D15); T2R:187-221; T2F:112-125.

**Rejected.**
- **W as a superproject with submodule members.** W's own index would hold gitlinks for the member paths, so the VCS view would be ambiguous, and submodule members are `.git` files, which the closed layout refuses. That shape is recorded for a later successor.
- **Members at any depth inside other members.** Disjointness keeps each source file in exactly one member's VCS view.
- **No cap on members.** Each member costs up to 4 MiB of index and 64 KiB of config (X2:272). 64 members bound that at about 260 MiB on the discovery ledger. The number is provisional and is revisited with T3.

**Forbidden.** A member at or above W; a member reached through a symlink; nested or overlapping members; a member when W is inside a repository.

**Controls.** One fixture per W and M clause, each with its negative.

#### 20. Declarations and the T2 renderings

**Decision.** A member exists only when declared. One fact chooses between two branches: whether the resolved semantic configuration holds an admitted `discovery.workspaceRoots` array (AQ:115). The branches follow S3's exclusive unit-source choice (SL:174-185; SLM:771-785).

**Branch A: the array is present (r2, RF-1).**
- **Where the array comes from.** The project or local layer (S3 `config-workspace-roots`), or `--workspace-root`, which is the flags layer of the same field and replaces a lower array whole (item 2; S3 `explicit-joins`). The global layer cannot set it (item 2). Both tiers are explicit intent, and they are treated alike here.
- **Membership.** Each root that lies inside a nested conventional repository below W makes that repository a member. A failure of custody, placement or layout **refuses** (SL:174-178). **No new Config2 field.**
- **Exactly those roots.** Discovery is restricted to exactly the array's roots, with `provenance=EXPLICIT`, and is never widened into a scan (NE:917-921), inside members as anywhere else. A member contributes only the units its named roots are.
- **The readers declare no member.** `cargo-config-patch@1` and `npm-workspaces-members@1` still read their files as data, but only to record **links** whose directories lie inside members the array already admitted. Every other reader entry is recorded as dropped in `workspaceDeclarations[].unresolved`, including an entry that names a repository the array did not admit. It is never admitted.

**Branch B: the array is absent (automatic, zero-config).** Only then do the **declaration readers** declare members, reading native files at W only, as data:
- **`cargo-config-patch@1`** reads `W/.cargo/config.toml`, or the legacy `W/.cargo/config`. Each `[patch.<registry>]` entry whose only key is a relative `path` inside W, and whose directory lies inside a nested conventional repository, makes that repository a member and records a Cargo link: the package name, the directory, and the version from that directory's `Cargo.toml`. An entry with `git`, `branch`, `rev` or `registry` keys, or a path outside W, is recorded as unresolved and ignored. This is T2's Cargo rendering, unchanged (T2F:120-123).
- **`npm-workspaces-members@1`** reads `W/package.json` `workspaces`. Each **literal** relative path that lies inside a nested conventional repository makes that repository a member and records an npm link: the `name` and `version` from that directory's `package.json`. **A glob entry never declares a member.** A glob that would match inside a nested repository is recorded as unresolved (`workspace-glob-crosses-repository`). This is the npm rendering T2F:124 left open, fixed here: `W/package.json` = `{"private": true, "workspaces": [<the overlay's npm link directories, sorted>]}`, generated from the overlay and not separately pinned, exactly like the Cargo file (successor S8).
- **Python:** no reader at M3. D9 decides Python support after M3's review (AQP:550), and "a `pyproject.toml` must not be given Cargo-workspace semantics by default" (AQP:478). `mr-py-medium-boto` keeps its pinned link map.

**Further rules:**
- **In both branches**, a reader link counts only when its directory lies inside an admitted member. Others are recorded as dropped.
- **Ambiguity.** Two members that provide one package name give no link (`ambiguous-provider`). A patch whose directory's `Cargo.toml` names another package gives no link (`patch-target-name-mismatch`).
- **Readers are not framework recognizers.** Their output is a custody input (membership) and a link set, not an entry-point default. They form their own closed registry (item 8). **Rejected:** overloading NE §8's nine recognizers, which would need an NE §8 successor and would mix a custody input into analysis defaults.

**Basis.** CH13:59-64 (discovered values enter with provenance; ambiguity is disclosed); SL:174-185; SLM:771-785 (an `if`/`elif`/`else`: a config array never falls through to automatic discovery); NE:917-921 (Config2 `workspaceRoots` and `--workspace-root` restrict discovery to exactly those roots, "never widened into a scan"); AQ:115 ("Omitting workspaceRoots selects automatic discovery"); T2F:118-124; T2R:217-221, T2R:303.

**Rejected.**
- **Automatic membership of every nested conventional repository under a non-repository W.** It would make the zero-config scope depend on whatever happens to be cloned under W, which is the broader reading CH13:62-63 forbids.
- **Members declared by path dependencies found inside units.** Boundaries would then depend on units, and units on boundaries, which is a fixpoint. A path dependency into an undeclared repository stays `input-closure-incomplete`, with the remedy "declare the member".
- **`pnpm-workspace.yaml` as the D15 npm rendering.** pnpm's linking of a version requirement to a workspace package depends on settings outside that file (`link-workspace-packages`, the `workspace:` protocol). The `package.json` `workspaces` form is the one that npm and yarn both read.
- **The Amazon workspace tool's own file.** Its format is a fact only the owner has (OQ-1). Until a reader is added, such a workspace needs one explicit declaration in `W/opensip.json`, and FW-14 counts that as one manual correction (HD:213).

**Forbidden.** Membership by glob; following a reader's path through a symlink; a reader that runs anything; a link into a non-member; **a reader adding a member, or widening discovery beyond the named roots, while an admitted `workspaceRoots` array is present** (r2, RF-1).

**Controls.**
- The four T2 workspaces in `vcs: none` mode give the overlay's exact link maps (T2M overlays, `overlayDigest`).
- A glob-crossing fixture; an ambiguous-provider fixture; a name-mismatch fixture.
- **Branch A from each source (r2, RF-1):** a project-layer array, a local-layer array and `--workspace-root` each suppress reader membership. In each case:
  - a reader's link into an array-admitted member is kept;
  - a reader entry naming any other repository is recorded as dropped, and that repository's paths stay `outside-project-boundary`;
  - discovery inside a member visits exactly the named roots.
- Branch B: with the array absent, the same reader files declare the members.

#### 21. The X2 successor: X2 r9

**Decision.** X2 r8 is amended as follows. Nothing else in X2 changes.

**Item 1, premise scope.** The fact, the premise, the H-volume constraint and the "strictly below H" rule are unchanged. The objects the premise may admit gain:
- `<root>/.opensip/local.json`, as a custody-checked configuration file (B1's layer 4);
- the directories the **downward** discovery walk custody-judges, from the root to each unit. X2:280 already says item 1's scope "covers its custody-checked objects", and r9 names them;
- for each admitted D15 member M: `M/.git` (the directory), `M/.git/config` and `M/.git/index`. These are exactly the three objects item 1 already admits for an enclosing repository (X2:29), each through its own retained no-follow descriptor. **Nothing else under `M/.git`.** Any further Git object, such as `HEAD`, refs or `packed-refs`, is admitted only by C1's VCS-observation law, for every repository alike.

**New item 3a, carrier capture.** S3's selection keeps the descriptor of the `opensip.json` it judged (`project_admission.rs:240-252`), and `.opensip/local.json` is judged the same way when the invocation is interactive. B1 reads their bytes from those descriptors, at most 4 MiB. Their full metadata samples join item 3's held-fence recheck set.

**New item 6b, the member observation.** It runs at discovery, after the fence is released (item 12), on the discovery ledger. **Precondition:** item 6a's observation of W is `NoRepository` (W2). For each declared M, in ascending path order:
- **Placement:** M1 to M3, by positive no-follow lookups of `.git`, `.hg`, `.svn` and `.jj` at every directory strictly between W and M, and at M itself.
- **Layout:** item 6a's admitted layout, unchanged.
  - The effective configuration is the union of the fixed system sources, the global sources and `M/.git/config`, with item 6a's refusals verbatim: `include`/`includeIf`, `core.worktree`, `core.bare` other than false, `extensions.*`, `core.repositoryformatversion` other than 0, `core.precomposeunicode` set to false, and any value the parse cannot bound (X2:163-208; `git_tracking.rs:295-317`).
  - `commondir` and `config.worktree` must be positively absent (`git_tracking.rs:807`).
  - The environment check of item 6a runs once per pass (`git_tracking.rs:697-713`).
- **Index:** item 6a's exact decoder, versions 2 to 4 with the checksum, refusing a `link` or `sdir` extension (`git_tracking.rs:429`). A gitlink in M's index marks a nested repository inside M, which stays a boundary.
- **The workspace marker:** `W/.opensip/project-id.v1` lies in no member's worktree, by M1 to M3. This is asserted, not observed.
- **Recheck:** the member evidence is not in the fenced recheck set, because it grants no project admission. C1's per-read custody re-check covers it at snapshot time (SL:313-315).

**Item 8, rows.** No new code. New **subjects** under `PROJECT.ROOT_CUSTODY_REFUSED`: `member-vcs-unsupported:<reason>`, `member-outside-volume` and `workspace-root-inside-repository`. Under `PROJECT.SCOPE_LIMIT`: `members:<n>>64` (item 24). **(r3)** Item 24 says when each subject applies. Under RBS1 R2, `workspace-root-inside-repository` applies to no explicit or config member. It is the disclosure subject of a reader entry when W fails W2 (item 24, rows 3 and 6).

**Item 10, units.** B3-b owns 6b. B1-b owns 3a.

**Why this is safe:**
1. **No new evidence class.** The premise is the same per-filesystem fact (X2:18-22), applied to the same three Git objects and to custody-checked files of the same kinds.
2. **No new Git semantics.** Everything outside the closed layout still refuses as `vcs-unsupported`. r9 models nothing that r8 did not.
3. **One authority root.** W keeps the only ProjectId, marker, registry row and lease namespace. Members are never authority roots under W, and the IE:41-58 identity rules are untouched.
4. **No write.** Nothing is created or written in any member: no `.opensip`, no index refresh, no config (item 15).
5. **The marker stays untracked by construction.** W is in no repository (W2), so no index can track W's marker, and members are strictly below W outside `.opensip`.
6. **The environment stays refusal-only.**
7. **Undeclared nested repositories keep S3's boundary.** Only W's own declaration, read as data from files W's owner controls under custody, crosses one.
8. **Read-only, per-read custody.** Every member byte the snapshot reads is re-checked between `lstat` and `open` (SL:313-315).

**Basis.** X2:18-49, X2:74-96, X2:163-215, X2:250-280; `git_tracking.rs:1-18`, `:743-776`; SL:159-168.

**Rejected.**
- **Following a member's `.git` file (gitdir).** It would admit relocated repositories whose evidence lives outside M, which r8 refused for a reason that still holds (X2:213).
- **Running 6b under the fence.** It grants nothing that the fence protects.
- **Admitting more Git objects in r9.** C1 has to define VCS state for single-root projects anyway, and one law should admit those objects for every repository alike.

**Forbidden.** Every forbidden substitute of X2 (X2:282-304) applies to members. In addition:
- 6b without the `NoRepository` precondition;
- a member admitted from the environment;
- any Git object of a member beyond the three;
- any write under a member.

**Controls.** Synthetic Git fixtures, created by tests in a private 0700 scratch under a synthetic H:
- a conventional member;
- a `.git` file;
- `core.worktree`;
- an `include`;
- `extensions.objectformat=sha256`;
- `commondir` present;
- a split index;
- a submodule gitlink inside a member;
- a `.hg` between W and M;
- W inside a repository;
- a member on another volume, where the platform allows it, or synthetic otherwise;
- 64 and 65 members.

Each refusal is tested with its subject.

#### 22. What members change in S3, U-8, the snapshot and the native contexts

**Decision.**

**SL S3 and NE U-8 (contract successor S3):**
- A declared member is **not** a nested repository and **not** a boundary. Automatic unit discovery enters it as if it were an ordinary directory of W. Nested repositories and projects inside it stay boundaries.
- `DiscoveryProvenanceV3` adds `memberRepositories: [{path, declaredBy: [{source, readerId?, readerVersion?, path?, contentSha256?}]}]` and `workspaceDeclarations[].unresolved`.
- `AdmittedBoundaryInventoryV3` adds `memberRepositories`, which never enters `excludedPathPrefixes`.
- U-8's subset test is unchanged over boundaries. A member path in the native derivation that is absent from `memberRepositories` refuses `native.boundary-inventory-mismatch`.
- `JOIN_CROSSES_NESTED_REPOSITORY` remains for a crossing into a repository that cannot become a member: one inside another nested repository, or any crossing when W fails W2.
- **The Config2 join keeps "exactly those roots, never widened"** (NE:917-921). S3's edit of that paragraph adds only that an exact root may lie inside a member (item 20, branch A). It does not relax exactness, and a present array suppresses reader membership (r2, RF-1).
- **U-9 is unchanged (r2, NBO-2).** It still keys off no explicit roots and no surviving `rust` or `tsjs` unit (NE:879-883). Units inside members count as surviving units, because members are not boundaries. Its one fallback unit is at W's root `""`. A member is never a second fallback site.

**A member's own `opensip.json` (lead decision).**
- A declared member that holds `opensip.json` is admitted as a member.
- **Its `opensip.json` is not a configuration layer of W.** It is recorded as `memberConfigs` provenance, disclosed as "not consulted", and stays the member's own project file when the member is analyzed alone.
- **Rejected:**
  - treating it as a boundary (ADV-3, SL:146-157). A package configured on its own could then never join a workspace, and the owner's daily use is both;
  - merging member configs into W's. That is a hidden seventh layer (CH13:60).

**A member's own `.opensip/`.** C1 treats it exactly as it treats the root's own `.opensip/`, under one rule that C1 must fix (finding F10). **(r3)** That rule is now fixed. SX-1, bound with B-S1, makes `.opensip` at the selected root and at each admitted member root an exact anchor: never entered, never source and never inventoried (BS1 §1). F10 is settled.

**The snapshot (contract successor S4, landed by C1).**
- `vcs-observation` (IE:542-546) is schema version 2 with a single commit. For a project with at least one member, it becomes schema version 3:
  - W's own observation, which is `kind: none` under W2;
  - plus `members: [{path, kind: "git", commitId, dirty}]`, ascending by path.
- **Single-root projects keep version-2 bytes**, so no existing `snapshot2` changes.

**Links (`WorkspaceLinkSetV1`, host-owned and Plan-bound through the contexts).** It holds `{schemaVersion: 1, members[], links: [{ecosystem: cargo|npm, packageName, providerMember, packageDir, providedVersion, declaredBy}], unresolved[]}`.
- B3 derives the declaration half.
- **Per-consumer satisfaction is decided at context construction** by the ecosystem's own resolver:
  - **Cargo:** the Rust adapter honours an admitted link only as a projected `[patch.<registry>]` path entry, under successor S5. Config-level `patch` in snapshot files stays stripped (NE:1750). Cargo itself then applies the patch only when the requirement matches.
  - **npm:** the TypeScript context resolves a bare specifier to a linked member's package directory only when the consumer's range accepts the provided version, under node-semver, and only through successor S6. With no link, `nodeModulesInReadSet=false` keeps every bare specifier `unresolved-module-specifier` with scope `external` (NE:1413-1418).
- **Rejected:** host-side satisfaction for Cargo, which would duplicate Cargo's own rule; writing `[patch]` into a member's `Cargo.toml`, which writes a member file (T2F:125).

**Basis.** SL:146-168, SL:281-311; NE:816-863; IE:542-546; NE:1399-1418, NE:1743-1752, NE:1786.

**Forbidden.** A member's file as a configuration layer; a link honoured without its successor; host-side Cargo satisfaction; a version-3 VCS observation for a single-root project.

**Controls.**
- The P3 fixture extended with members runs through both instruments (`admitted-boundary-inventory-joins-…`).
- A member's `opensip.json` changes nothing in W's `resolvedConfigDigest`.
- A single-root `snapshot2` is byte-identical before and after S4.

#### 23. The seven shared flags, the consent rule for members, and `grants.rs`

**Decision: D15 adds no flag and needs no consent.**
- Member admission is **selection, not authorization**: CINV's class `selection`, like `--workspace-root`.
- It grants no execution, no write, no custody waiver and no new authority root. Every member directory and Git object passes custody on its own.
- The declaration is the intent of W's owner, in files under custody, and every member is disclosed.

**Rejected:**
- a new authorization flag such as `--allow-member-repositories`. It would make the recognized shapes impossible without a flag and protect nothing that custody does not already protect;
- a new `--workspace-member` selection flag, which duplicates `--workspace-root`'s explicit role and needs a CINV successor.

The reviewer is asked to test this (R1).

**The seven flags at M3** (COV:5268-5407; CINV `sharedFlags`). M3 implements them as typed library admission with tests. M4 wires the CLI (BP:887-888).

| Flag | CINV class | M3 owner | Admission rule | D15 |
|---|---|---|---|---|
| `--project` | selection | `discovery.rs` (B2-b) | At most one explicit authority root, examined once (SL:132; SL:261-262) | selects W |
| `--workspace-root` | selection | `discovery.rs`, `configuration.rs` (B1-a, B2-b) | Repeatable; exact roots; the flags layer of `discovery.workspaceRoots`, so it replaces Config2's array (item 2); `explicit-joins` | may declare a member (item 20, branch A); like a Config2 array, its presence suppresses reader membership |
| `--ephemeral` | selection | `discovery.rs`, `configuration.rs` (B3-a) | A typed selection carried to J; not configuration; excluded from the digest (WS:242-247) | none |
| `--trust-group <gid>` | authorization | `grants.rs` (B3-a) | `AuthorizedGroups`: at most 64 gids (SLS `authorizedGroupIds`), built only from parsed invocation input; recorded in provenance; **configuration has no constructor** (SL:127-129) | applies to member directories and member Git evidence exactly as `judge_project_object` applies it to an enclosing repository (`project_chain.rs:422-438`) |
| `--trust-project-owner` | authorization | `grants.rs` (B3-a) | `ProjectOwnerWaiver`: only with explicit `--project`, otherwise `PROJECT.EXPLICIT_PATH_INVALID` (SLM:832-833). It waives only the owner check, on the directories under the explicit root and its config file, as the reference applies it (SLM:636, SLM:669-680), and never on marker files (SLM:665) | applies to member **directories**; **never** to member Git evidence or `local.json` |
| `--allow-backup-custody` | authorization | `grants.rs` (B3-a) | `BackupCustodyAcknowledgement`: per invocation; consumed only by the S3.1 admission at the first source-derived write (J3); writes no policy (SL:317-331). Under law 464's constant-UNKNOWN classifier it is recorded and never required | none |
| `--yes-policy` | authorization | `grants.rs` (B3-a) | `ConsentSource::PreExistingPolicy`: typed; no M3 consumer. M5's test and repair steps consume it (WS:1667; SL:1105-1106). Interactive consent in CI stays M5's refusal | none |

**`crates/security/src/grants.rs`: its M3 scope (lead decision).** CH14:401 describes the module as "Bind and verify exact execution, mutation and recovery permissions."
- **In scope at M3:** the four authorization records above, their typed constructors, and the pure S3.1 choice function.
- **Reserved, not built by B:**
  - C4's first-party semantic-grant projection (IE:524-540), if C4 places it here;
  - X4's planned `admit_repo_execution_grant` (X4:155, X4b), which never landed, and SL S10's repository-execution grant (M5, M5-EX; M3P:345-350);
  - SL S10.1's repair authorization (M5);
  - DR-G09 (COV:4631-4651, qualified at M6) and DR-G32 (M5).
- **Forbidden in `grants.rs` at M3:** any execution, mutation or recovery grant; any constructor from configuration; any I/O.

**Basis.** COV:5268-5407 (verification: "selection never grants execution/custody and configuration never impersonates explicit consent"); CINV `sharedFlags` (each flag's `join` text); SL:127-130; CH14:401; M3P:126, M3P:376.

**Controls.**
- `crates/host/tests/discovery_tests.rs` (the COV verification owner): applicability, provenance and precedence for each flag.
- A compile-fail test: no Config2 path builds an authorization.
- `--trust-project-owner` without `--project` refuses.
- A waived explicit root admits an other-owned member directory but refuses that member's other-owned `.git`.

#### 24. Refusal and disclosure rows (no new code)

| Condition | Row | Subject |
|---|---|---|
| A member path that fails grammar, or a crossing into a repository that cannot become a member | `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` (SL:1302, SL:1305) | `JOIN_PATH_GRAMMAR`, `JOIN_CROSSES_NESTED_REPOSITORY` |
| An explicit or config member that fails layout or placement | `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID` (X2:250-270) | `member-vcs-unsupported:<reason>`, `member-outside-volume` |
| An explicit or config member when W is inside a repository (W fails W2) | row 1's: `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` (SL:1302, SL:1305) | `JOIN_CROSSES_NESTED_REPOSITORY`. **(r3, RBS1 R2)** Item 22 and row 1 govern. This is a crossing into a repository that cannot become a member, so a project that never opts into D15 keeps S3's existing refusal. `workspace-root-inside-repository` is not applied to an explicit or config member; row 6 uses it |
| An explicit or config member that fails directory custody | row 2's: `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID` (X2:250-270) **(r4, RBS3 RF-1)** | the existing custody subjects |
| More than 64 members, **in either branch (r3, RBS1 R4)**. n is the number of distinct repositories that the active branch's declarations name after placement (M1 to M3), counted before X2 r9 item 6b reads any Git configuration or index | `PROJECT.SCOPE_LIMIT` / `REQUEST.UNSATISFIABLE` (SL:1323) | `members:<n>>64`. No member is dropped to fit, which would be truncation (item 12). The subject's remedy is the sentence B-S1 adds at SL:1323 (BS1 LD-17) |
| A member that a reader declared, and that fails any of the above **except row 5 (r3, RBS1 R4: the cap refuses in both branches)** | **not a refusal.** The member is excluded, with the reason in `workspaceDeclarations[].unresolved`; its paths stay `outside-project-boundary`. **(r3, RBS1 R2 and R5)** When W fails W2, the readers declare nothing and derive no link. A literal reader entry inside a nested repository is disclosed as `member-excluded` with subject `workspace-root-inside-repository`, and no other entry is recorded | — |
| A reader entry that is unresolved: a glob crossing, an ambiguous provider, a name mismatch, a non-path patch | disclosed in `workspaceDeclarations[].unresolved`; no member and no link | — |
| A reader entry while an admitted `workspaceRoots` array is present (item 20, branch A) that names a repository the array did not admit | disclosed in `workspaceDeclarations[].unresolved` as dropped; no member and no link | — |

Subjects are diagnostic data under S12.1's closed vocabulary, never new codes (SL:1323, SL:1508).

**Basis.** SL:1298-1330; X2:250-270; the owner's no-new-codes rule (X2:250).

### D. Successors and findings

#### 25. Successor list

| # | Successor | Kind | Content | Author | Lands with |
|---|---|---|---|---|---|
| S1 | **X2 r9** | **law** amendment (item 21, in this proposal). **(r3) Accepted by Grok with no findings** (X2r9) | premise scope; item 3a capture; item 6b member observation; subjects | lead (this law) | B1-b, B3-b |
| S2 | **X12 r4, item 8** | **law** amendment (item 10, in this proposal, which gives its exact text). **(r3) Accepted by Grok with no findings** (X12r4). Its item 8 is item 10's text, with the passages X12r4 marks as its own r4 lead decisions | the order of pack admission. Its text records the withdrawal of I1:386's clause that X12 r3's order stands, and of the ordering sense of X12:136. I1:381-384 stands | lead (this law) | B1-a |
| S3 | **SL S3 + NE §1.4 (U-8; U-9 unchanged, item 22; the Config2 join, keeping "exactly those roots, never widened", with a present array suppressing reader membership) + SLS** `DiscoveryProvenanceV3` / `AdmittedBoundaryInventoryV3` + the declaration-reader registry | **contract successor** (design unit B-S1; `ACCEPT-DESIGN-UNIT`). **(r3) Accepted by GROK2 and bound at product `9c11c53`**, with M3-C's SX-1 | items 19, 20, 22, 24 | this package | B3-b |
| S4 | **IE `vcs-observation` schema 3** | **contract successor** (design unit B-S2). **(r3) Accepted by Codex and bound at `240a795`** | per-member VCS rows; version-2 bytes unchanged for single-root projects | this package; implemented by C1 | C1 |
| S5 | **NE §3.3**: admitted Cargo links as projected `[patch]` path entries; the lock carrier for a patched resolution under `--locked` (NE:1786) | **contract successor** | item 22 | C3 / G1b | C3 |
| S6 | **NE §2.2 / §2.4**: the TS context binds `WorkspaceLinkSetV1`; per-consumer node-semver satisfaction | **contract successor** | item 22 | C2 | C2, F |
| S7 | **PCS `operability` section** | contract successor | not B's; item 7 leaves the slot | S-OP-5 | M3-O2 |
| S8 | **T2 record**: T2F §6 npm rendering (item 20) and an optional `git-conventional` member assembly | **harness record** (corpus unit; not a contract) | items 19, 20 | the corpus unit; K1a implements | B3-c |
| S9 | **`CONFIG.INVALID` remedy text** | contract successor (PUBLIC_ROUTE_REMEDIES, X12-0's route). **(r3) Design unit B-S9**, split out of B-S1 by lead decision on 2026-10-04: complete successor copies of the two native-model files (BS9). **Accepted by Grok and bound at `8adfe0c`** | item 4 | this package | B1-a |
| — | **SMAP** | **none needed** (lead decision) | SMAP:54 and SMAP:67 name owners and boundaries that already cover D15. D15's change is in S3 and §1.4, which those rows point to. **Rejected:** an SMAP row per shape, which would duplicate the corpus manifest. AQP:556's "SMAP/discovery successor if needed" is met by S3 | — | — |
| — | **CINV** | none (no new flag, item 23) | | | |
| — | **NE §8** | none (readers are not recognizers, item 20) | | | |
| — | **AQ §1.1** | none: B1 implements AQ within its latitude | | | |
| — | **NE U-6** | **not B's**; finding F4 | | | |

**Law versus contract.** Items 1 to 18 and 23 are law: they implement accepted contracts. S1 and S2 amend existing laws. S3, S4, S5, S6 and S9 are contract successors, each needing an `ACCEPT-DESIGN-UNIT` review. S8 is a harness record. **(r3)** S3, S4 and S9 have theirs: B-S1, B-S2 and B-S9 are accepted and bound. S1 and S2 are accepted.

#### 26. Cross-law findings

These are recorded for their owners. None changes an accepted outcome.
- **F1. Ledger caps against whole-repository walks.** The same 65,536 / 131,072 caps bound C1's snapshot custody walk, which reads every file, not just directories. C1 needs its own observation profile (item 12).
- **F2. Cargo links.** NE §3.3 strips config-level `patch` (NE:1750), so T2's Cargo rendering is unhonoured until S5. A patch also changes the consuming member's lock resolution, which `cargo metadata --locked` refuses (NE:1786). C3 must define the lock carrier: an imported workspace lock under DS-5's user-named source (NE:1688) is the lead's suggestion.
- **F3. TypeScript links.** With no install at M3, `nodeModulesInReadSet=false`, and every cross-member bare specifier is `external` (NE:1413-1418) until S6.
- **F4. U-6.** Cross-unit edges are unresolved `external-module-boundary` edges (NE:869-870). That holds for D15 members and equally for single-repository TS monorepos, whose packages are separate units (U-3). AQP §3's workspace rules (`ws-unreferenced-export`, AQP:189) over multi-unit universes need a U-6 successor. D15's value at M3 is sealed dependency sources (no `missing-dependency-source`), not cross-unit resolution.
- **F5. Harness placement.** X2 item 2 puts every project root strictly below H (X2:51-58). T2F §6 assembles workspaces under the runner's temporary root, which on macOS is outside H. K1 must assemble under a private directory below H, or run through a test seam with a synthetic H. B does not relax item 2.
- **F6. X12 order.** Item 10 (S2).
- **F7. OPP §7's exception list.** It names the resolver as an environment-read owner (OPP:365-367). Item 9 removes it; M3-O records it.
- **F8. Citation drift.** AQP:537 (see Short names).
- **F9. Record names.** SL:286 names `AdmittedBoundaryInventoryV1`, while NE:822 and SLS carry V2. This law cites V2. It is a note for the record-hygiene batch. **(r3) Settled by B-S1:** its overrides of SL:286 and NE:4135 name `AdmittedBoundaryInventoryV3` (BS1 §2 and §3; `b-s1/PASSAGES.md`).
- **F10. `.opensip/` in the snapshot.** No contract says whether the root's own `.opensip/` (marker, `local.json`) enters the source inventory. C1 must fix one rule, and item 22 makes members follow it. **(r3) Settled by SX-1**, bound with B-S1: `.opensip` at the selected root and at each admitted member root is never source (BS1 §1; item 22).
- **F11. The CI determination** is unspecified in the product contracts, and the preview's `--ci` did not carry over. Item 3 decides it; J1 may add a flag through a CINV successor.
- **F12. The global carrier's location** is unspecified in the product contracts. Item 2 decides `I/host/settings.json`.
- **F13. Un-ignoring.** CH13's table makes host ignore conventions "overridable through existing configuration precedence", but PCS has no field that un-ignores. This is a disclosed limitation, and a PCS successor if wanted.
- **F14. Plan impact.** B is larger than M3P's 2 + 3 + 3 days (M3P:202). By the unit sizes below, B2 finishes about day 8 rather than day 5, so C1, and with it the host chain (M3P:229), starts about 3 days later. B3 keeps slack before M3-X. M3P's next revision should record this, as I1 did for its own size.

#### 27. Open questions

**For the owner (one question; it blocks nothing in this law):**
- **OQ-1. The real Amazon workspace's shape.** Facts only the owner has:
  - Does the workspace root hold a file listing its packages, and what is its name and format?
  - Is the root ever itself a Git repository?
  - Are packages ever checked out as submodules or linked worktrees?
  - How do Rust and npm packages refer to each other there: patches, paths, or a vendored registry?

  The answers decide whether a third declaration reader is added (an S3 successor amendment), and whether T3's instance needs one manual correction (item 20).

**Lead decisions flagged for the owner's possible reversal (not blocking):**
- **D15 needs no consent flag** (item 23).
- **A launch inside a member selects that member alone.** S3 is unchanged. The workspace is selected from W, from any directory of W outside every member, or with `--project W`. **Rejected:** continuing the upward walk past a VCS marker to look for a workspace root. That would change the default scope of every repository that sits under a directory holding a manifest (SL:141-144, "default scope does not change with launch directory").

**For the reviewer (test these hardest).** In r1, GROK2 confirmed R1 to R7, subject to RF-1 (R1's minimal further consent: a supplied array is the membership) and RF-2. r2 asks only for confirmation of those fixes. **(r3)** GROK2 accepted r2 with no findings. r3 is a record revision, and its review request asks only whether each r3 change is faithful to its source.
- **R1.** Is a recognized native declaration at W enough intent to cross a repository boundary, with no consent flag (items 20, 23)?
- **R2.** Is X12's order amendment sound, and is "nothing to clean up" still true after the fence acquisition (item 10)?
- **R3.** Running discovery after the fence, on its own ledger profile, against X2 item 9's one-ledger rule (item 12).
- **R4.** The empty discovery fold, against AQ:104, AQ:155-157 and AQ:330-332 (item 1).
- **R5.** CI equals not-interactive, by terminal state (item 3).
- **R6.** The waiver's reach over member directories, and not over Git evidence (item 23).
- **R7.** Are S3 to S6 complete for D15's analysis value, and is anything else frozen in the way?

## Units after the law

**Gates.**
- **No product unit starts before M3-P0 is integrated and M3-L is accepted.** M3P:159 and M3P:187-193 make P0 and day 0 the start.
- Design units B-S1, B-S2 and B-S9 edit only arch, so they may proceed once this law is accepted. **(r3)** All three are accepted and bound: B-S1 at product `9c11c53`, B-S2 at `240a795` and B-S9 at `8adfe0c`.
- Inventory successor numbers are assigned by the lead at launch, after checking `git ls-files`.
- **Reviews:** design units need `ACCEPT-DESIGN-UNIT`. Product units with an inventory need `ACCEPT-UNIT` with `inventoryCandidateAssessment`.

| Unit | Kind | Content | Depends on | Size | Gates and cells |
|---|---|---|---|---|---|
| **B-S1** | design: contract successor | S3: the SL S3 and NE §1.4 passages, SLS V3 schemas and the reader registry, with M3-C's SX-1. **(r3)** S9's remedy text moved to B-S9. **Accepted by GROK2 and bound at `9c11c53`** | law | M | D15; SL:3; NE:2 |
| **B-S2** | design: contract successor | S4: IE `vcs-observation` schema 3, version-2 bytes unchanged. **(r3) Accepted by Codex and bound at `240a795`** | law | S | D15 (snapshot half) |
| **B-S9** (r3) | design: contract successor | S9: the `CONFIG.INVALID` remedy, as complete successor copies of the two native-model files (BS9). Split out of B-S1 by lead decision on 2026-10-04. **Accepted by Grok and bound at `8adfe0c`** | law | — (inside r2's B-S1 sizing) | S9 (item 4) |
| **B1-a** | product | `configuration.rs`: the pipeline (items 1, 4 to 8, 11), the PCS pinned source and its registry row, the generated classification table, the registries' enums, `ResolvedConfigurationV1`, the digest, PCM byte vectors, and the X12 order (item 10). **(r3)** B-S9's remedy string, embedded at `configuration.rs:24` (reused at `doctor_ingress.rs:216`), with the pin at `configuration_tests.rs:338-343` repinned (BS9). Pure; no I/O | P0, L, **B-S9** (r3; r2 read "B-S1 (S9 text)") | M | **FW-13** (COV:8104); AQ:183-187 cases; flags `--workspace-root` (layer 6) |
| **B1-b** | product | Carriers and mode: X2 r9 item 3a (the retained `opensip.json` and `local.json` descriptors); `I/host/settings.json` through installation private access; `InvocationModeV1`; the environment structural check (item 9) | B1-a | M | **FW-01** (no config write); SL:3 (config custody); flag `--project` |
| **B3-a** | product | `grants.rs`: the four authorization records, typed constructors, the S3.1 choice function, and the `--ephemeral` selection type | P0, L | S | flags `--allow-backup-custody`, `--trust-group`, `--trust-project-owner`, `--yes-policy`, `--ephemeral` (COV:5268, 5308, 5328, 5368, 5348) |
| **B2-a** | product | `custody/discovery_rule.rs`: the shared rule (U-4a; DD's entry points). **(r3)** It implements SX-1's `.opensip` anchor, and its evidence carries the `discovery-defaults.py` reference refresh for that anchor and D15's `memberRepositories` (BS1 LD-14, BS1-F3) | P0, L | M | **NE:2** (U-4a); SL:3 |
| **B2-b** | product | The S3 downward instrument (item 13), the discovery ledger profile (item 12, a platform change), `DiscoveryProvenanceV2`, the boundary inventory, and the T2 census margin test | B2-a, B1-b, B3-a | L | **SL:3** (COV:6702); FW-01; flags `--project`, `--workspace-root` (COV:5288, 5388) |
| **B2-c** | product | `discovery.rs`: the native unit instrument U-0 to U-9 (item 14), the JSONC reader shared with C2, the scope descriptor, default selection | B2-b | L | **NE:2** (COV:7066); **6 `inventory/*` cells** (COV:4226-4391), discovery half; FW-01 |
| **B2-d** | product | Host-side recognition (item 16), the YAML subset reader, and the recommendation evidence (item 18) | B2-c | M | **NE:9** (COV:7245); FW-01 |
| **B3-b** | product | D15: X2 r9 item 6b in `git_tracking.rs`; the readers (item 20); members in V3 records; `WorkspaceLinkSetV1`; item 24's rows | B2-c, B-S1 | L | **D15**; SL:3 (successor); X2 r9 |
| **B3-c** | harness | The FW-14 outputs: `config-shape` cases (HD:213) for the five T2 workspaces and the negatives of items 19 to 21; manual-correction counts; S8's npm rendering and `git-conventional` mode | B3-b, S8, K1a | M | **FW-14** (COV:8125); Q8 measured |

**Order:**
- B1-a → B1-b;
- B2-a → B2-b → B2-c → B2-d;
- B3-a is parallel and lands before B2-b, which consumes it;
- B2-c → B3-b → B3-c.

**Downstream:**
- C1 needs B2-c (and B-S2 for members);
- C4 needs B1-a (the digest), B2-c (membership) and B2-d (recognition);
- C2 and C3 author S5 and S6.

**Test owners:**
- `crates/host/tests/discovery_tests.rs` for the flags (COV verification owner; CH14:498);
- `crates/host/tests/workflow_tests.rs` for FW-01, FW-13, SL:3, NE:2 and NE:9 section routing (COV:6702-6716, 7066-7080, 7245-7259, 7852-7869, 8104-8121);
- `tests/qualification/README.md` for FW-14 and the `inventory/*` cells.

**Controls the bound design units add (r3).** B2-a, B2-b and B3-b also owe the controls in B-S1's "Controls owed by the implementing units" (BS1). B1-a repins the remedy test (BS9, "Binding").

## Forbidden substitutes

Each item lists its own. Across all items:
- **Layers:**
  - a seventh layer, a provider-private or member-private precedence, or a discovered value outranking explicit intent;
  - any environment input to configuration, discovery, recognition, declarations or grants.
- **Effects:**
  - any write, spawn, network use, install or repository-code execution during resolution or discovery;
  - a configuration write as a side effect.
- **Digest:**
  - provenance, operational, authorization, presentation or environment values in `resolvedConfigDigest`;
  - discovered unit content in it.
- **Custody:**
  - a carrier read by name after its judgment;
  - following a symlink or a `.git` file;
  - a member admitted by glob, through a symlink, or when W is inside a repository;
  - a reader adding a member, or discovery widened beyond the named roots, while an admitted `discovery.workspaceRoots` array is present (from any layer, or `--workspace-root`);
  - any Git object of a member beyond `.git`, `config` and `index`;
  - `--trust-project-owner` reaching Git evidence;
  - configuration building an authorization.
- **Order:** pack admission after any registry capture, registration, lease or effect.
- **Bounds:**
  - truncation;
  - a retry on a new ledger;
  - a downward walk under the installation fence.
- **Vocabulary:**
  - a new public code;
  - a new shared flag;
  - an unregistered field, capability, recognizer, reader or flag.
- **Shipping too early:** honouring Cargo or npm links before S5 or S6; a version-3 VCS observation before S4.

## Not claimed

- No product code, test, measurement or corpus fetch was run for this record. The product was read at `30c5db1` only.
- No contract, schema, gate, register row or threshold is changed here. S3 to S6 and S9 are named, not written. **(r3)** S3, S4 and S9 have since been written and bound as B-S1, B-S2 and B-S9. This law still writes none of them.
- No command is wired; CLI delivery is M4 (BP:887-888). There is no Linux or AL2023 claim.
- No confinement claim. No provider launches under this law (ML item 17; M3P:308).
- D15's analysis value at M3 is bounded by findings F2 to F4. There is no cross-unit resolution and no Python link.
- The member cap (64) and the discovery ledger caps are provisional.
- T3, the real Amazon instance, waits on OQ-1 and the licence (AQP:217).
