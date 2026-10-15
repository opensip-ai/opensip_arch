# B1B-PLAN-r2 and M3-B r5 review

Verdict: **REQUIRED-FINDINGS**

Verified the 843-byte subject manifest, SHA-256 `0becb1c863b7f808548f61173222aa59fe71af0806fc95a8482a6438e4b419dc`, and all three members by byte count and SHA-256. PLAN-r1 is byte-identical to the prior staged history. Product HEAD is `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`, clean; architecture HEAD is `93960ed5327615ead9af08845a4bc27ce3409e76`, with no tracked differences.

M3-B r5 changes only the title, banner, new r5 changes block and item 9 Enforcement bullet; every intervening and following byte is preserved against live r4. No unrelated law change was found.

Round-1 RF-01 is resolved at plan level: corrected inherited-recheck facts, explicit charged negative observations for the project carrier and interactive local leaf or parent, fence-held rechecks, and appearance controls. RF-03 is resolved: the separate analysis path retains descriptors and captures carriers before the registry phase; legacy admission keeps its non-capturing selection, reads, charges, rechecks, refusals and latching. Concrete compatibility controls cover both read-session and write-gate wrappers. RF-02 is partly addressed by proposing the law correction, enumerating test locations, restricting exceptions to test targets, adding a pin test, planting reads in both crates and adding environment equivalence. Its remaining defect is RF-01 below.

## B1B-PLAN-R2-RF-01: Describe the existing HOME exceptions accurately

Severity: medium. Location: PROPOSAL-r5.md:24,321; PLAN-r2.md:140.

The proposed law authorizes the real HOME only for comparison against a fixture home, and the plan repeats that condition. Three enumerated calls do something else: installation_routing_tests.rs:1024-1025, ordinary_writer_tests.rs:116-117 and read_premise_tests.rs:104-105 construct HOME/Library/Application Support/OpenSIP and call exists() to assert installation absence. Only installation_root.rs:787 compares the account-derived home against the environment value. All current call sites are represented by the listed files, but the proposed purpose restriction does not cover three of those actual uses. Consequently the list is not exact against the pinned product in the sense requested, and round-1 RF-02 is not fully resolved.

Required correction: Revise the proposed item-9 bullet and plan to distinguish the single comparison from the three test-only installation-absence probes, naming their concrete enclosing test items and limiting each exception to its actual use. Alternatively explicitly plan to remove those probes and pin the reduced post-change exception set. Do not describe the existing probes as fixture comparisons. Correct the associated change-table description.

Evidence at the pinned product base:

- crates/security/src/custody/installation_routing_tests.rs:1024-1025
- crates/security/src/custody/ordinary_writer_tests.rs:116-117
- crates/security/src/custody/read_premise_tests.rs:104-105
- crates/security/src/custody/installation_root.rs:787

## B1B-PLAN-R2-RF-02: Keep marker custody and refusal-only Git behavior in the controls

Severity: medium. Location: PLAN-r2.md:151,157; compare section 1.1 at line 83.

Two controls rely on false claims about existing checks. The carriers row says a .opensip and local.json appearing in CI never refuse because nothing observed them. Section 1.1 correctly retains the marker lookup: observe_marker still opens and judges .opensip and observes project-id.v1 in every mode, and ProjectRootAdmission::recheck repeats that observation. An appearing wrong-custody directory or a changed marker can therefore refuse independently of local.json. Separately the hostile-environment control says a Git-free fixture prevents X2 refusal. observe_tracking checks the environment before repository discovery; hostile HOME or XDG_CONFIG_HOME refuses even when no repository exists. Carrier capture and pure resolution can be tested without that tracking step, but the plan must say so rather than promise an impossible Git-check outcome.

Required correction: Narrow the CI appearance control to a custody-valid .opensip with no project-id.v1, proving no local-carrier lookup or refusal attributable to local.json while retaining ordinary marker/custody refusals. Add or retain a contrasting marker/custody refusal assertion. State that the carrier/resolver environment-equivalence control stops before tracking, or separately assert the permitted Git environment refusal; remove the claim that repository absence disables that check.

Evidence at the pinned product base:

- crates/security/src/custody/project_admission.rs:561-603,806-825
- crates/security/src/custody/git_tracking.rs:321-339,692-718
- MB items 3 and 9; PLAN-r2.md section 1.1

## Non-blocking observation

B1B-PLAN-R2-NBO-01: The change table says fifteen test-only environment variables. The pinned source contains 17 disallowed-method call sites: one production vars_os call and 16 test-only calls, covering 13 distinct test variable names (HOME occurs four times). Use those counts, or omit the count. The proposed B1-b child marker is additional and does not yet exist.

## Whole-plan assessment

The scope matches MB:876 and its FW-01, SL:3 and --project cells. Section 0 now accurately distinguishes the chain identity/birth/custody checks from full registry metadata equality, and describes the existing carrier, private-capture and duplicate-mode APIs correctly. Project/local captures retain the judged descriptor, forbid reopen by name, bound reads to 4 MiB, charge the operation ledger and join the held-fence recheck set. The intended placement/chain, carrier/resolution/pack, registry ordering matches X2 r9 and MB item 10.

Optional global capture remains sound at plan level: positive absence joins the installation session recheck, present captures use private access, custody failure latches and analysis creates neither the file nor its parent. The absent-prefix case must obey the same positive absence rule under the existing parent. The unified invocation type and stdin/stderr terminal conjunction introduce no environment input and remain unwired until J1.

Per-crate Clippy configuration, audited item-level allowances, exact source/configuration pinning and planted production reads in each crate are appropriate mechanisms. The current scan found all 17 disallowed-method call sites represented by the proposed locations: one production read and 16 test reads. Test confinement is supported by test targets or cfg(test) modules. The HOME purpose restriction is why mbR5ExceptionListComplete is false despite positional coverage. Its intended test must not validate only call locations while overlooking the permitted use.

The refused-project-pack control correctly excludes registry capture, RESERVED rows, leases and journals. No-write sampling covers FW-01. The two controls identified above require correction before the full control plan can be accepted. This review accepts no code, binding, production wiring or product qualification; the proposed law correction still awaits acceptance/publication.

Only read-only reading, hashing, JSON parsing and Git queries were used. No Cargo, tests, builds, lane or network was run. No private fixture, installation directory, signing keys or held trees were read. Neither repository, the stage, control files nor the prior review was edited. Only REVIEW.md and review.json in this review directory were written.
