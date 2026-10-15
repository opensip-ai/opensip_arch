# B2B3-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS**.

The subject manifest is 452 bytes with SHA-256 `363011fbe31f299e39cd1482b7365d58910d995cf0620771f29a6802a7913389`. Its sole member, `docs/implementation/m3/config-discovery-b/b2-b3/PLAN-r1.md`, independently rehashes to 15,863 bytes and SHA-256 `9203c27d6eb00f9aac62833704eb1573795ebda3c458939058ec00806570bbf1`. Both pins match. Product HEAD matches `3b3ab6e0e354c8f81e4ac030ed3102757be43085` and has a clean porcelain status; architecture HEAD matches `47bee3b55292a973e90bbff6e81e3c509b28f3c0`.

The plan remains within parent plan r4 section 1.3. The three-way split is sound, and section 0 accurately describes the existing primitives and missing plumbing. It leaves B2-c, B3-b, J1, M4 and qualification separate. A retained-root lending view, a read-session equivalent release, one discovery ledger, parent-relative no-follow observations, the owner waiver confined to the explicit selection root, and no invented downward mount boundary are appropriate choices. The decisions need the corrections below before implementation.

## B2B3PLAN-1: Complete the native-name handling contract

Location: PLAN-r1.md LD-B2B3-2 and section 3 steps 1-3.

visit_entry_names passes OS dot entries to the visitor (directory_entries.rs:417-418 explicitly asserts both). The plan applies LogicalPath/platform rejection to each listed name, so following it literally refuses every ordinary listing on . or ... It also specifies only the 255-scalar segment bound, omitting MC:274 and LogicalPath::parse's 4096-scalar complete-path bound. A path can exceed that bound well before depth 256.

Required correction: Explicitly charge returned OS names, discard exactly . and .. before logical-name validation or child observation, and validate each resulting root-relative LogicalPath including its total scalar limit. Specify the same refusal/detail for an overlong path. Add successful ordinary-listing controls and 255/256 segment and 4096/4097 complete-path boundary controls.

## B2B3PLAN-2: Allow metadata-only custody rejection without requiring an ACL capture

Location: PLAN-r1.md LD-B2B3-3, LD-B2B3-6 and section 3 judged-object rule.

LD-3 makes any core custody of NotObserved an invariant fault and says every marker is judged before core execution; LD-6 forbids opening nonregular markers and promises their normal SYMLINK/NOT_A_REGULAR_FILE reasons. Those entries cannot acquire descriptor ACLs. The current core Judge::markers calls custody for every present marker, and custody matches the ACL before reference_order examines kind. Thus a FIFO or symlink marker represented honestly as NotObserved hits the planned invariant fault instead of the promised public custody result. Section 3's statement that every judged object is opened conflicts with the same case.

Required correction: Define a metadata-only early-rejection path in the core that preserves reference custody order and never opens nonregular markers. NotObserved should fault only when judgment actually reaches an ACL-dependent check. Retain honest uncaptured state; do not invent an empty ACL. Reconcile the every-judged-object wording, and test FIFO/socket/symlink markers both alone and alongside a valid marker against the oracle, including no-open traces.

## B2B3PLAN-3: Resolve and admit configuration between the two admission phases

Location: PLAN-r1.md LD-B2B3-12 numbered sequence.

The seam runs phase 1 and phase 2 in step 1, then resolves the winning workspaceRoots in step 2. ReadSession::admit_project_carriers documents the opposite contract at installation_read.rs:245-253: configuration resolution and pack admission run on the captured carriers before complete_project_admission. Phase 2 captures/classifies the registry and rechecks the admission. Running it before resolution gives an invalid configuration the later phase's work and potentially its refusal precedence.

Required correction: Specify phase 1, carrier-based resolution and required admission (with CLI provenance), phase 2, then successful equivalent release and walking. Add a control that resolution/admission failure never reaches phase 2 or downward observation, alongside the flag precedence controls.

## B2B3PLAN-4: Pin the existing configuration module now

Location: PLAN-r1.md LD-B2B3-11.

The plan defers both discovery.rs and configuration.rs until B2-c. crates/host/src/configuration.rs already exists and implements B1-a resolution. MB item 15 explicitly requires the structural prohibition in configuration.rs as well as discovery_rule.rs and grants.rs. The proposed scan therefore omits an existing required module while claiming the FW-01 structural pin.

Required correction: Include current configuration.rs and its production-reachable includes in the B2-b3 structural pin with planted spawn/socket/write negatives. Defer only the nonexistent discovery.rs until its owning unit creates it.

## B2B3PLAN-5: Cross-check evidence and final records, not only paths and kinds

Location: PLAN-r1.md section 3 Cross-check against the oracle.

The promised comparison projects walker_population to paths and kinds. The bound adapter also deliberately projects evidence: its final return strips vcs from unprobed/pruned/depth-257 directories. A walker can have identical paths and kinds while leaking such vcs evidence and reporting a false nested repository. Conversely it can omit observed VCS evidence and miss a boundary. Neither defect is detected by the stated comparison; the existing pure-core replay cannot establish that native capture supplied the right evidence.

Required correction: Compare the relevant native population evidence, especially vcs presence/kind/target and custody inputs, and feed native captures through the core to compare all available partial-provenance fields, complete boundary inventory and refusal/detail against the current bound reference. Keep workspaceDeclarations pending. Include pruned anchors and depth-257 directories carrying hidden vcs annotations, ordinary nested VCS/project boundaries, explicit/config chains and metadata-only marker rejection. Do not claim equality for deliberately unobserved ACLs; define that projection explicitly.

## Non-blocking observations

- **B2B3PLAN-NBO-1**: LD-4's 257 descriptor statement should distinguish retained ancestors from temporary descriptors. Opening a depth-257 directory to observe its four markers can require an additional descriptor beyond root plus depths 1-256; the listing stream also opens an independent descriptor. Keep EMFILE as a refusal and state the actual peak in code/census.
- **B2B3PLAN-NBO-2**: LD-7's unreadable/malformed gitdir target=null rule should explicitly preserve budget exhaustion and changed-identity failures as whole-operation refusals, consistent with section 3, rather than swallowing them as an unavailable target.

## Decision accounting and verification limits

LD-1, LD-4, LD-5, LD-7, LD-8, LD-9, LD-10 and LD-13 are sound subject to the non-blocking clarifications above. LD-2, LD-3, LD-6, LD-11 and LD-12 require correction. The walker specification and controls are consequently insufficient as written. LD-13's trace should record actual primitive calls, including by-name absence probes, rather than intended traversal alone.

Evidence was obtained by read-only source/authority inspection, hashing, JSON parsing and Git queries. In particular, the parent r4 plan, MB r5 items 12/13/15, MC:268-296, the bound reference's walker_population and evidence projection, and the named native admission, custody, listing and scenario primitives were inspected. No reference code was imported or executed. No tests, Cargo, builds, lane, network, private fixture or held-out reads were used. This is a plan review, not an implementation or product qualification. No code, binding or law was changed. Only REVIEW.md and review.json were written; neither repository was edited.
