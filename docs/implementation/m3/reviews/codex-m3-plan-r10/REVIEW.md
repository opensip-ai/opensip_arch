# M3-PLAN r10 record review

**Verdict: ACCEPT.** No required findings; two non-blocking observations.

Subject: docs/implementation/m3/M3-PLAN.md, 226,011 bytes, SHA-256 ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964. Diff base: M3-PLAN-r9.md, 150,586 bytes, SHA-256 72bc7a135014072fd06b84211f0535a0fece8b14280d0dc16059e6240de54a17.

The assessment is confined to arch 17584e1f5 and product d2c00a9. Both overnight-log snapshots were read from their pinned Git objects: 315 lines at 249d74ab4 and 714 lines at 17584e1f5. Product HEAD has advanced, so later product or architecture work and untracked v137/v138 candidates are excluded. The lead answer about S-M and D13 is incorporated.

All 133 supplied pins match. The r9/r8/r7/r6/r5 change tables are preserved byte for byte. Accepting law subject hashes match the snapshots, and all 15 new locked design-unit manifests match their accepting reviews. Their 236 record, manifest, review, assent and member references match the committed cutoff bytes.

## r10 change rows

| Row | Assessment |
|---|---|
| 1 | **Header, pins and baseline.** All 133 supplied pins match their declared byte counts and hashes. r9 through r5 change tables remain byte-identical. Pinned product has 97 contract and 96 inventory successors, with v136 last in the inventory chain. |
| 2 | **Accepted laws.** Accepting subject hashes match pinned snapshots, including the five nested S2-S6 verdicts. L r5 and C r7 remain accepted in review, effective only with L in effect. |
| 3 | **Bindings, integrations and started units.** The 17 product commits and 15 contract additions match the stated order. P0, I1-a, X3a-2, X4-F2 and VD2-a/F8c are integrated; J2a, E2a and X4-F3 are started at the log cutoff. Planned v137/v138 are not recorded as selected or accepted. |
| 4 | **L gate and delta triggers.** FA-2 acceptance is on dca02900 and RUST3-LIM binds record 70f494d9 after FA-2. L-G10 and L-G11 are met; no changed joined wire/commitment bytes trigger an extra delta round. |
| 5 | **Owner critical path.** L-G1, L-G4, L-G5 and L-G9 remain open. The lead answer and ML5 gate both make S-M report dependent on owner-gated D13; O7 and D3/D13 therefore prevent day0. |
| 6 | **H and J4 timing.** Static dependency arithmetic reproduces H1/H4/H2/H3 at 7/8/9/9, J4e set at5, J3a set at6, J3b at9 and set at10. |
| 7 | **New edges.** X4-F3 gates J3b integration, with the same-commit alternative retained. S21 gates the named J3b and J3d wiring, and I1-a precedes E2s; the latter two gates are met. |
| 8 | **Carry-ins.** X3a-2 and X4-F2 are integrated. J-RW law acceptance does not imply J4 code or retirement of L11. X4T-c, F9, X3c-3 and J4 remain. D8-1 is assigned to X4-F3. |
| 9 | **New units and records.** VD2/VD2-a/F8c, SD-7, SD-5b, S21, X4-F3 and the X4T r12/r13 split match their source records. The routed B, E1, I1 and D record revisions are recorded at their accepted revisions. |
| 10 | **X9 r17 frame.** Section-by-section review is the recorded lead decision. Round1 and LD-RC-6 remain in review; predicted census and kill-set changes are not treated as run evidence. |
| 11 | **Cross-law routes.** The routed obligations retain their sources and first consumers. This includes H5 S-B large-scope wiring, H2 E2s parse-error wiring, H3 X-H3 inventory wiring, SD-5b, and the still-owed J1/E1/RW-S8 recording text. |
| 12 | **Lead decisions.** The r10 rows correspond to cutoff log entries and the cited law/record decisions. Rows with no log alternative say so; r10 itself makes no new decision. |
| 13 | **Owner items.** B1/B3 gate L; B2/B4 do not gate this host DAG. RUST3-LIM and SYN-NS FYIs reflect the cutoff record without turning recommendations or future measurements into owner decisions. |
| 14 | **Product state.** The 47 changed files and scaffold/verifier state match pinned Git objects. Existing implementation-line citations hold. The blanket exception wording has non-blocking observation NB-01. |
| 15 | **MC coordinate correction.** MC r6:874 and MC r7:885 contain the same Step15 structural-admission passage. r10 uses the correct r7 coordinate. |
| 16 | **Effort and remaining work.** The declared rollup is 72+7=79 law/successor/record units and 92+2=94 code/harness/probe sub-units, total173. X4-F3 remains unsized, successor bounds remain assumptions, and the whole-M3 total remains uncomputed. |

## Schedule and scope

H1/H4/H2/H3 finish on days 7/8/9/9 from D2b at5. J4a and J4c finish at2 and1; J4b and J4d at4 and3. J4e finishes at5 after its predecessors and the X3c-3 set. Serialization then gives J3a set6, J3b9 and its set10. H5 remains22, J2b25, J3d28, M3-M31 and M3-X33.

The host chain is 2+2+3+3+2+3+1+3+3+3+3+3+2=33. X12d's set reaches J2b at22 with zero slack. The listed margins reproduce: C4c2; D3 against F1/G1a2; F1 against H5 4; I2 and J2c4; Rust5; F2/F3 6; C2b5; B2-a2 and B3-a3; G2-v9; R9; E3 14; H2/H3 10; J3a set19; J3b set15; J4e26. The freeze-slip formula remains 33+max(0,s-10).

No accepted-law edge is missing from the plan as a whole. The numeric table must be read with the consumer gates in the units and successor tables: notably E2s for H2's parse-error leg, X-H3 widening for H3's TS/Rust leg, and S-B for H5's large-scope path. These are conditional dates. X4-F3 gates J3b integration, not necessarily authorship, and the same-commit alternative remains valid. Its duration remains unsized.

Scope changes have authority: X4 r8 S11.9 for X4-F3; J1 r5 item14 for S21; E1 r4 change6 for I1-a/E2s; D r5 item24 for D4's own case(a) check; L r5 for L-G11; H r3 item25 for H1-H5; J-RW r4 item11 for J4a-J4e. No new r10 lead decision is introduced.

The owner-critical-path claim is accurate as a statement of the current dependency: L-G1/L-G4/L-G5/L-G9 remain, S-M's report needs owner-gated D13, and every host-chain unit needs L in effect directly or through predecessors. Owner answers do not themselves imply S-M complete or L effective. The source requires the S-M delta round and any forced O7 delta before dependent gates open.

## Drafter rulings

- **P0 unblocks D1-D4:** Follow MD5, not the abbreviated log sentence. MD5 Units after the law requires both integrated P0 and L in effect; D code is not authorized to start from P0 alone.
- **ASSIGNED / not yet sent:** In review is accurate at cutoff: the committed log records the successor batch sent, while ASSIGNED and the drafting note provide no acceptance. The same stale note coexists with actual ACCEPTED status in other records.
- **S-M / P5-8:** The status treatment is sufficient with the lead answer supplied in this review: S-M has not run because its report needs owner-gated D13 (B3). ML5 L-G1/L-G5 and the cutoff log corroborate the report gate. No new scheduling or owner decision is inferred.
- **MB r2 versus r4 citations:** Keeping r2 coordinates is valid for historical and unchanged premises. Cited rows do change: B-S1/B-S2 status, added B-S9, B1-a dependency, B2-a recorded duties, and F14 embedded citation coordinates. The plan already handles binding/dependency changes; NB-02 covers the omitted B2-a qualification. Caps, sizes, code-unit order and the B2-b edge underlying b=10 are preserved.

## Non-blocking observations

**M3P-R10-NB-01 (P3): The blanket claim that only Cargo.toml and generator pins changed among files cited below needs a narrower scope.**

Location: docs/implementation/m3/M3-PLAN.md:257; r10 changes row 14 (line 89).

Product git diff cd5958b d2c00a9 changes Cargo.lock, which the Operability row cites; the delta adds only the two scaffold package entries. The new scaffold row also cites newly added crates/components/src/lib.rs, crates/syntax/src/lib.rs and crates/syntax/Cargo.toml. The identity/contracts row itself records changes to design-lock.json and the verifier as well as the generator pins.

Suggested recording change: Limit the assertion to pre-existing owner implementation files with retained line citations, and explicitly except the new scaffold files, Cargo.lock, design-lock.json, the verifier and its pins.

Non-blocking because: The preceding per-unit change list and the table disclose these changes correctly. The retained implementation-line citations, no-tracing observation and scaffold descriptions remain accurate; this wording does not hide an unrecorded unit or move a gate.

**M3P-R10-NB-02 (P3): The MB citation note lists three affected areas, but the cited unit-table range also includes B2-a, whose recorded duties were expanded.**

Location: docs/implementation/m3/M3-PLAN.md:38; M3-B row at line 305.

MB r2 line 844 describes the shared rule only. MB r4 line 876 also assigns the SX-1 .opensip anchor and the discovery-defaults.py refresh for that anchor and D15 memberRepositories. MB4 r3 changes rows 6 and 7 explicitly record these duties, already settled by bound B-S1. MB r2 line 803 also has different M3P line coordinates in MB4 line 834; the F14 estimate and B2-b integration edge remain unchanged.

Suggested recording change: Add the B2-a implementation/evidence duties to the MB4 qualification and optionally summarize them in the B2-a scope cell. Retain MB r2 coordinates for historical citations and the unchanged timing premises.

Non-blocking because: The plan cites MB4 and its change tables, includes bound SX-1 before B2-a, and retains the correct B2-b dependencies. This adds precision to the scope summary without changing authority, size, order or arithmetic.

## Evidence qualification

REG v3 was untracked at the cutoff. The supplied r10 manifest is f931f315… (455 bytes), while the cutoff batch REQUEST.md and hashes.txt pin 0bd640d3… (454 bytes). Reconstructing only that manifest from the cutoff member entries reproduces SHA-256 0bd640d3f0c210dfa70a5fb9c167f92f2870162ae6882e5aefffde0adb4f44e2. The plan's line65 is historically correct; the supplied different manifest revision is not used to promote any cutoff status. This checks the historical fingerprint, not unavailable original member bytes. REG v3 and X2r10/X3cr9/X3br11/X4Tr13 remain in review, as does X9r17 round1 and LD-RC-6.

Product successor counts and order come from each of the 17 immutable product commits. The selected inventory is the v136 tail of the 96-entry chain, not a post-cutoff candidate. L-G10 uses FA-2 manifest dca02900…; L-G11 uses accepted RUST3-LIM record 70f494d9… and binds after FA-2. Neither joined subject changed, so neither extra delta trigger fired.

The MC:874 to MC:885 correction was checked against both snapshots: the Step15 structural-admission passage is identical at those respective coordinates. Effort is the stated approximate rollup, 79+94=173, rather than a new duration estimate. Unsized successors and owner dates remain unsized; the whole-M3 total remains uncomputed.

No repository edits, commits, delegation, product builds, Cargo commands, tests, measurements or matrix runs were performed. No real OpenSIP home or private 413 UUID fixture was accessed. Only this review directory was written. Static scratch inspection used nice19 with isolated HOME/TMPDIR.

Supporting local evidence: acceptance-and-history-audit.json, dag-and-effort-audit.json, mb-citation-evidence.json, product-table-file-audit.json, overnight-cutoff.diff and pin-verification-initial.json.
