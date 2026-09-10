Corrected counter-review complete. Below, each finding states what I withdraw, what stands with exact evidence, and where I disagree with the challenge.

## Corrections by finding

**SEC-01. Withdrawn: "intrinsically impossible" and the prescription to relax measured kernel trust to a generic ABI.** What the sources actually establish is narrower. The profile template schema fixes the version selector tag as the constant EXACT-BUILD, and the OS ABI payload carries one `kernelSeries` and one `kernelFlavor` string. The runner table fixture states one release profile key per class, one class per platform, and that a profile named for a build the class does not run is never qualified. So per release the qualified population is exactly one macOS build per architecture and one Ubuntu kernel line-and-flavor per architecture, whichever the hosted image boots at release time. That is honest and refuses explicitly. Later releases re-measure, so profiles are not frozen to one fixture forever. The exact problem is therefore two things, not one: first, a support-population rule in which measurement classes double as the support set, which no current row reconciles, and the scope chapter already marks that reconciliation open at DR-119 and DR-126; second, an undisclosed macOS consequence, since the v8 product-consequence paragraph discusses Linux only, while the macOS launch predicate refuses on any build or dyld cdhash other than the runner image's. On the trust question I now agree with Codex: on Linux the trust properties are the Ubuntu-maintainer package, the archive key digest, Secure Boot and lockdown, and the Canonical UEFI CA; the flavor and series strings are identity of what was measured, not the trust anchor. Admitting a generic-flavor kernel would require measuring it on a class that boots it, which D-102 says is a successor-triggering class change, not a weakening of the predicate. On macOS, kern.uuid and cdhash are stronger than the trust argument needs, but changing them does need equivalent threat evidence, and I prescribe none. Reclassified: integration gap, MEDIUM, plus a LOW documentation hazard for the incomplete consequence paragraph.

**SEC-02. Correction accepted on all three points.** Ownership alone fails: `/tmp` is root-owned with sticky world-write, so a directory ownership rule passes it, and a file placed there by another account is owned by that account but the directory test never sees it. The rule set must be: the candidate config is a regular file owned by the invoking account with no group or other write bit; its directory and every ancestor inside the walk are not writable by other principals, so a sticky world-writable directory ends the walk; the walk also ends at the account home boundary and at a mount boundary; an explicit `--project` wins and is the recommended CI form; a candidate that fails custody inside the boundary refuses explicitly naming the path rather than being skipped silently, so a planted file cannot be ignored into a different root; and the resolved provenance records the deciding path and why the walk stopped. On the consequence: "other users' files enter the report" was overstated. What is established is that the ancestor becomes the selected project root and its tracked config supplies pins, holds, allowed scopes and the budget. The snapshot scope beyond that is host-owned, the delivery example shows a worktree change spec that includes untracked files, and the sealed VFS is streamed to the worker running as the victim. So the bounded, possible consequence is that files readable by the victim under the injected root can enter the victim's own snapshot, Coverage counts and cycle findings. It is not exfiltration to the attacker, and it is not proven for the preview's exact snapshot rules. Severity stays MEDIUM; classification stays newly discovered.

**SEC-03. "Permanently" withdrawn.** The correct statement: trust on that install stays expired until real wall time or a signed issue time reaches the poisoned instant, potentially years, and there is no reviewed recovery. Future excursion is confirmed by the v2 base text that a wall clock more than a day ahead of the high-water mark is accepted as time passing, and by the behavior model's time function, which takes the maximum of each observation and the stored mark before deciding expiry. Restore keeps the floor. Deleting the per-user trust database is the only exit, and it is precisely the rollback the design forbids. I withdraw the clamp and reset prescriptions: any recovery lowers a floor, so it needs an anti-rollback and expiry proof that does not exist. The honest required deliverable is a recorded decision at DR-112 between accepting and disclosing this outage class with a documented reinstall procedure, and adding a signed upper-bound time source with its own proof, with a G08 case either way. Severity stays MEDIUM.

**SEC-04. Sharpened as requested.** Three things are distinct. Signed component trust revocation lives in the trust database as the revocation counter and the ST-REVOKED role state; the v1 DR-112 decision says an already-running component in that state is refused at every stage, and the behavior model implements that as a pure predicate over the three role states. Grant revocation is a REV record in the per-project journal whose sole writer is the operation holding the project lease. The lifecycle fence is global and is never waited on under a lease. Rechecks that exist: trust and epoch at operation start under the fence, epoch equality at lease acquisition through the lifecycle callback, and journal grant status at every effect request. What is missing is exact: when a global operation advances the revocation counter while a project operation holds its lease, nothing invokes the already-running predicate for that operation, nothing can append REV with reason trust-revoked to that project's journal because the refresh is not its writer, and nothing cancels the child. Per-request recheck is necessary but not sufficient, because a component with no handles, which is the shipped worker, makes no requests. Concurrency is real: trust writers hold the fence, a running analysis holds only its lease, and the census never waits. Bounded by the fact that in the preview the racing actor is the same account's own consented refresh against its own short analysis. Severity MEDIUM for the full product, LOW for the preview; classification stays a defect by omission at the DR-112 and DR-105 join.

**SEC-06. Reclassified; the dichotomy was false.** The scope chapter excludes automatic repository execution, and the delivery contract already contemplates an explicit per-project execution-capable grant. Codex's third branch is right: cargo-produced outputs such as build-script output directories, expanded macros and metadata can be produced by the user's own toolchain outside OpenSIP and admitted as sealed prepared inputs, the same family as the runtime, test and history import contracts. Rust can then carry native trait semantics for non-generated scopes with typed unavailability elsewhere. The precise unsatisfied items are: the grant clause's "with network disabled" has no enforcement primitive, since egress is disclosure-only under the truth table, so that clause must be restated as disclosed trusted-code execution or gain a primitive; repository-controlled code is outside the threat model's first-party TCB, so any in-host grant needs a principal class added at DR-105 before it is admitted; and the sealed prepared-input contract with provenance, snapshot correspondence and Coverage semantics is not designed. DR-128 is not reopened. Reclassified: known open contract at DR-117, DR-118 and DR-119 with one precise wording defect in the delivery base text. Severity MEDIUM.

**SEC-07. Reclassified; the contradiction claim is withdrawn.** No automatic upgrade bridge is deliberate and disclosed, and closed enums are versioned by majors, which is one architecture, not two. File 08 already owns the transition at the DR-110 and DR-130 row. The one concrete constraint that survives: activating an active TR-REPAIR role or non-empty kernel attestation keys cannot happen inside root schema one, because admission refuses both as semantic rules, and a root schema two cannot be chained into by a stage-one host. So the DR-130 transition contract must state fresh install as the path for that step, or design the root schema transition so that a schema-one reader can verify the chain into schema two. That is a design input for an open row, not a defect. Reclassified: known open contract, MEDIUM because signed update and recovery are in the intended scope.

**SEC-05. Confidence lowered.** I inspected the successor paths. The G15 selection model refuses an expired current root before any other check. The behavior model admits an ordinary payload from ST-EXPIRED back to ST-TRUSTED when the payload is valid and complete, so healing from expiry is intended at the state layer. What no text or model states is whether root N+1's signatures are verified against the keys of an expired root N during chaining. The omission is real but small, and the intent is legible. Reclassified: LOW, defect by omission, confidence medium.

**SEC-08. Correction accepted.** Frozen bytes must stay frozen. The applied manifest, the supplement, the security v8 headings and the v6 freeze are historical subjects and must not be rewritten. The remedy is a current annotation in the navigation or review README stating the adopted standing, noting that the observed-digest fields are authoring residue that the checker ignores, and warning that the duplicated section numbers must not be used as heading selectors. Any future pin-only successor may carry corrected strings; the applied one does not change.

**SEC-09.** Unchanged; nothing was challenged and nothing was overstated.

## Disagreements retained

I keep SEC-02 and SEC-03 as newly discovered defects rather than integration gaps, because both live inside accepted foundation and security units and neither has an owning open row that names them. I keep SEC-04 as a defect by omission rather than a known gap, because the already-running refusal is a recorded DECIDED value with no mechanism, which is an internal inconsistency, not a deferral. Overall readiness stays NOT_READY.

```json
{
  "reviewer": "Claude (claude-fable-5-1), Lens B counter-review pass",
  "lens": "B: security, distribution, protocol and operational correctness",
  "readiness": "NOT_READY",
  "corrected_findings": [
    {
      "id": "SEC-01",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "withdrawn": "Claim that the mechanism is intrinsically incapable; claim that all future profiles equal one fixture; prescription to relax measured kernel identity to a generic ABI.",
      "stands": "Per release, exactly one qualified OS build per macOS architecture and one kernel line/flavor per Ubuntu architecture, each equal to the hosted runner image at release time; measurement classes double as the support population; macOS consequence undisclosed.",
      "evidence": [
        "docs/coop/completion/security-schemas.v8/tcb-profile-template.schema.json /supportedVersionOrBuildSelector/tag const EXACT-BUILD (line 29)",
        "docs/coop/completion/security-fixtures.v8/profile.example.linux-x86_64.azure-6.17.json single kernelSeries/kernelFlavor strings (lines 25-27)",
        "docs/coop/completion/security-fixtures.v8/qualification-runners.json /rule and one releaseProfileKey per class (lines 6, 12, 21, 30, 39)",
        "docs/coop/completion/security-fixtures.v8/profile.P-MACOS-ARM64-25G83-APFS.json /acquisition/launch/0 and /2 refusesOn",
        "docs/coop/completion/security-completion.v8.md §8.6 lines 628-632 (Linux only)",
        "docs/coop/artifacts/coordinator-decisions.D-102.turn2.draft.md line 307 (class changes trigger a successor)",
        "docs/v2/architecture/10-mvp-and-future-scope.md line 40 (baselines open at DR-119/126)"
      ],
      "required_correction": "At DR-119/126 with a D-102 class successor: allow more than one release-measured profile per platform, each measured on a class that boots that build; state the resulting support population in file 10; extend §8.6 to macOS. Keep the measured kernel trust predicates unchanged unless equivalent evidence is supplied.",
      "companion": "LOW documentation_hazard: v8 §8.6 omits the macOS per-build consequence.",
      "owner": "DR-126, DR-119, D-102 fleet successor, DR-G22",
      "confidence": "high on the mechanism; product impact depends on the unreconciled support decision"
    },
    {
      "id": "SEC-02",
      "severity": "MEDIUM",
      "classification": "newly_discovered_defect",
      "withdrawn": "Ownership-only correction; the phrase that other users' files enter the report as an established consequence.",
      "stands": "The ancestor walk trusts any regular opensip.json up to the filesystem root with no custody test on the file or the walked directories; a sticky world-writable root-owned directory defeats an ownership-only rule.",
      "evidence": [
        "docs/coop/completion/host-foundation-completion.v2.md §2 lines 113-117; §1 lines 45-49 (custody checks are for the operational root only)",
        "docs/coop/completion/host-foundation-completion.v2.md §3 lines 166-167, 179-186 (layer-3 fields)",
        "docs/coop/artifacts/delivery.v2.json line 299 (worktree changeSpec includes untracked files; snapshot scope is host-owned)"
      ],
      "bounded_consequence": "Established: another principal selects the project root and its pins/holds/allowedScopes/budget for the victim's run. Possible, not proven for the preview's exact snapshot rules: victim-readable files under the injected root enter the victim's own snapshot, Coverage counts and cycle findings. No exfiltration to the attacker.",
      "required_correction": "Config custody: regular file owned by the invoking account, no group/other write; no walked directory writable by other principals (sticky world-writable ends the walk); stop at account home and mount boundaries; explicit --project overrides and is recommended for CI; custody failure inside the boundary refuses explicitly naming the path, never skips silently; provenance records the deciding path and stop reason; G12/G18 fixtures.",
      "owner": "DR-103/DR-104 host foundation (Lifecycle + security), DR-G12/DR-G18",
      "confidence": "medium-high"
    },
    {
      "id": "SEC-03",
      "severity": "MEDIUM",
      "classification": "newly_discovered_defect",
      "withdrawn": "The word permanently; the clamp and reset prescriptions.",
      "stands": "A single future wall-clock excursion advances the durable high-water mark unboundedly; trust on that install stays expired until real or signed time reaches that instant, potentially years; restore keeps the floor; no reviewed recovery exists and the only exit is deleting the trust database, which is the forbidden rollback.",
      "evidence": [
        "docs/coop/completion/security-completion.v2.md §4.2 lines 277-288 (wall clock more than 24h ahead accepted as time passing)",
        "docs/coop/completion/security-completion.v8.md §4.2 lines 210-217; §5.5 lines 303-305",
        "docs/coop/completion/security-behavior-model.v3.py lines 170-173 (high=max(now,high) then EXPIRED)",
        "docs/coop/completion/security_unit_lib_v8.py lines 1068-1072"
      ],
      "required_correction": "Recorded DR-112 decision: either accept and disclose the outage class with a documented reinstall procedure, or add a signed upper-bound time source with its own anti-rollback and expiry proof; a G08 case for excursion-then-correction in either branch. No floor may be lowered without that proof.",
      "owner": "DR-112 (Security + release), DR-G08",
      "confidence": "high"
    },
    {
      "id": "SEC-04",
      "severity": "MEDIUM (full product); LOW (preview)",
      "classification": "newly_discovered_defect",
      "withdrawn": "Nothing; scope sharpened.",
      "distinctions": "Signed trust revocation = trust.sqlite revocation counter and ST-REVOKED role state with alreadyRunning=refuse (DECIDED). Grant revocation = journal REV, sole writer is the operation holding the project lease. Lifecycle fence is global and never waited on under a lease.",
      "existing_rechecks": "Operation start under the fence (v8 §3.3); epoch equality at lease acquisition (lifecycle_verified_generation); journal grant status at every effectRequest (verify_effect_request).",
      "exact_missing_path": "After a global operation advances revocationVersion while a project operation holds its lease: no invocation of the already-running predicate for that operation, no writer able to append REV trust-revoked to that project's journal, no cancellation of the child. Per-request recheck would not cover a component that makes no requests.",
      "evidence": [
        "docs/coop/completion/security-completion.v1.md §4.3 lines 395-400",
        "docs/coop/completion/security-behavior-model.v3.py lines 124-129 (continuation predicate) and 135-137 (REVOKE transition)",
        "docs/coop/completion/security-schemas.v8/journal-record.schema.json lines 617-627",
        "docs/coop/completion/security_unit_lib_v8.py lines 794-796",
        "docs/coop/completion/security-completion.v8.md §5.4 lines 250-260",
        "docs/coop/completion/lifecycle-carrier.contract.v2.json callbacks lifecycle_writer_authorized and lifecycle_gc_authorized",
        "docs/coop/completion/lifecycle-carrier.cases.v2.json /cases[id=live-operation-survives-selection-change]"
      ],
      "required_correction": "Specify the live invalidation path (observer of the revocation counter in the running host, REV trust-revoked appended by that operation's own writer, cancel and teardown, bounded latency) or retract alreadyRunning=refuse for the preview and record the window; G09 case.",
      "owner": "DR-112 and DR-105 join (Security), DR-G09",
      "confidence": "medium-high"
    },
    {
      "id": "SEC-05",
      "severity": "LOW",
      "classification": "newly_discovered_defect",
      "withdrawn": "Bricking as the likely reading; HIGH-side wording.",
      "stands": "No text or model states whether root N+1 signatures are verified against an expired root N's keys during chaining. The state layer intends healing (PRESENT from ST-EXPIRED admissible); the selection model refuses an expired current root before any other step; neither models chain verification.",
      "evidence": [
        "docs/coop/completion/security-behavior-model.v3.py lines 142-148",
        "docs/coop/completion/compatibility-selection-model.v8.py line 160 (ROOT-EXPIRED)",
        "docs/coop/completion/security-completion.v1.md §3.1 lines 312-314; §4.6 lines 420-426",
        "docs/coop/completion/security_unit_lib_v8.py lines 261-265"
      ],
      "required_correction": "One clause: intermediate-root expiry is ignored during chain verification, the newest root must be unexpired at tEval, rootVersion anti-rollback holds; one retained case.",
      "owner": "DR-112, DR-G08",
      "confidence": "medium"
    },
    {
      "id": "SEC-06",
      "severity": "MEDIUM",
      "classification": "known_open_contract",
      "withdrawn": "The sandbox-or-shallow-Rust dichotomy; any implication that DR-128 reopens; the HIGH severity.",
      "stands": "Three precise unsatisfied items: (1) the delivery base grant clause promises network disabled with no enforcement primitive, since PT-NET-EGRESS is disclosure-only; (2) repository-controlled code is outside the threat model's first-party TCB, so any in-host grant needs a principal class before admission; (3) the sealed prepared-input contract for toolchain-produced outputs (build-script output, expanded macros, metadata) with provenance, snapshot correspondence and Coverage semantics is undesigned.",
      "evidence": [
        "docs/coop/artifacts/delivery.v2.json lines 534-539 (withGrant: with network disabled)",
        "docs/coop/completion/security-completion.v1.md §6.1 lines 556-563 (six tokens DISCLOSURE-ONLY)",
        "docs/coop/completion/security-completion.v8.md §1 lines 98-108",
        "docs/v2/architecture/10-mvp-and-future-scope.md line 45 (automatic execution excluded) and lines 74-77",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md §7 (import family)"
      ],
      "required_correction": "Restate the grant clause as disclosed trusted-code execution or supply a primitive; add the principal class at DR-105 before any in-host grant; design the prepared-input contract alongside the runtime/test/history import contracts; state Rust depth as native semantics for non-generated scopes with typed unavailability elsewhere.",
      "owner": "DR-117/DR-118/DR-119 with DR-105",
      "confidence": "medium-high"
    },
    {
      "id": "SEC-07",
      "severity": "MEDIUM",
      "classification": "known_open_contract",
      "withdrawn": "The claim of contradiction with D-371; the prescription to reserve extension points or relax closed-schema admission now.",
      "stands": "One concrete constraint for the DR-110/130 transition contract: an active TR-REPAIR role or non-empty kernelAttestationKeys cannot exist inside root schema 1 (admission refuses both), and a stage-1 host cannot chain into a root schema 2; the transition must state fresh install or design a schema-1-verifiable chain into schema 2.",
      "evidence": [
        "docs/coop/completion/security_unit_lib_v8.py lines 250-258",
        "docs/coop/completion/compatibility-matrix.completed.v5.json S-SCHEMA row (readers [1,1], no bridge)",
        "docs/coop/completion/distribution-runtime-completion.v2.md §3 lines 168-177",
        "docs/v2/architecture/08-decision-and-readiness-register.md line 411 (DR-110/130 row OPEN for full product)"
      ],
      "required_correction": "Record the root-schema transition rule inside the DR-110/130 contract; no change to accepted admission.",
      "owner": "DR-110/DR-130/DR-111",
      "confidence": "medium"
    },
    {
      "id": "SEC-08",
      "severity": "LOW",
      "classification": "documentation_hazard",
      "withdrawn": "Any remedy that edits the applied manifest, supplement, security v8 or freeze v6 bytes.",
      "stands": "Stale self-descriptions and observed-digest residue in frozen subjects; duplicated §10-§12 headings in security v8.",
      "required_correction": "Current annotation in navigation or the review README: adopted standing, observedSha256 is checker-ignored residue, duplicated headings must not be used as selectors; corrected strings only in a future pin-only successor.",
      "owner": "D-369 custody (DR-201–205 owners)",
      "confidence": "high; digests not recomputed by me"
    },
    {
      "id": "SEC-09",
      "severity": "LOW",
      "classification": "documentation_hazard",
      "withdrawn": "Nothing.",
      "owner": "DR-112, DR-114, DR-123",
      "confidence": "high"
    }
  ],
  "disagreements": [
    "SEC-02 and SEC-03 remain newly_discovered_defect: both sit inside accepted units with no owning open row that names them.",
    "SEC-04 remains a defect by omission: alreadyRunning=refuse is a DECIDED value with no mechanism, an internal inconsistency rather than a deferral."
  ],
  "additional_sources_read_this_pass": [
    "docs/coop/completion/security-fixtures.v8/qualification-runners.json (full)",
    "docs/coop/completion/security-schemas.v8/tcb-profile-template.schema.json selector and tag constraints",
    "docs/coop/artifacts/coordinator-decisions.D-102.turn2.draft.md class and successor lines",
    "docs/coop/completion/security-behavior-model.v3.py lines 118-177",
    "docs/coop/completion/compatibility-selection-model.v8.py lines 160-183",
    "docs/coop/completion/check-security-unit.v8.py chain/expiry references",
    "docs/coop/artifacts/delivery.v2.json lines 286-307"
  ]
}
```