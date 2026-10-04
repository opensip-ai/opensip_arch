# Project-root custody, project admission and first registration — proposal X2 r10

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X2 of EXIT-PLAN.md, under owner.md §1b, §5, §7 and §8; the selected project registry owner (`project-registry-owner-selection-v2/owner.md`); the security contract S3 (discovery and custody), S7 (locks and leases) and S12; identity-and-evidence §2 and §5; and laws 458 (§3 and §5), 458b, 462, 465 item 4, 468 r5, 458c r6, 461 r3 (item 9, which requires this law) and X1. Every choice here is a lead decision, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each is dated and names the alternative it rejects. r2 answers Codex X2 r1 RF-1 to RF-7 against product f7acb6d (X1a integrated). r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Codex X2 r2 RF-1 to RF-4, and r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok X2 r3 RF-1 to RF-3, and r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok X2 r4 RF-1 (step 6 rechecks the current owners) and RF-2 (the floor step is ordered before item 7's lease, outside 7a). r4 bytes are preserved in PROPOSAL-r4.md. r5 was ACCEPTED by Grok on 2026-09-30. r6 is an amendment required by Grok X6 r1 RF-1: one narrow exception to item 7's fence rule for the read-only recovery selector. r5 bytes are preserved in PROPOSAL-r5.md. r6 was ACCEPTED by Grok on 2026-10-01. r7 is an amendment from implementing X2b-2: system Git configuration sources are refusal-only evidence, read without custody, because the custody rule refused every repository on a stock Mac. r6 bytes are preserved in PROPOSAL-r6.md. r8 answers Grok X2 r7 RF-1: item 1's no-follow premise admission governs only the Git evidence still in scope, and a system source is refused only as item 6a says, never for its location. r7 bytes are preserved in PROPOSAL-r7.md. r8 ACCEPTED by Grok on 2026-10-01. Not code. Library only: CLI enablement is X11.

**r9 (2026-10-04) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r8 bytes are preserved in PROPOSAL-r8.md (sha256 `c31d9a02…`, the subject Grok accepted in `reviews/grok-project-root-x2-r8`).

- **Where it comes from.** The accepted M3 law **M3-B r2**, configuration and discovery (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`). GROK2 accepted it on 2026-10-04 (`docs/implementation/m3/reviews/grok2-config-discovery-b-r2`, subject `92e65825…`, preserved as `PROPOSAL-r2.md`).
  - M3-B item 25 names this amendment as its successor S1, and M3-B item 21 gives its content. r9 carries that content and adds one lead decision: the order of item 3a's reads relative to items 2 and 3 (below).
  - It serves two M3 needs:
    - **M3-B's resolver (B1).** The project configuration file is read from the descriptor S3's selection judged, and the interactive local file is judged and read the same way.
    - **Owner decision D15, multi-repository workspaces** (`docs/implementation/m3/analysis-quality/PLAN.md:556`). The selected root W is in no repository, and declared member repositories below W each have a closed, conventional Git layout.
- **No product code changed.** The product is at main `3e64266`. M3-B's product citations were read at `30c5db1`, and every cited file is byte-identical at `3e64266`.
- **How it edits r8.** r8's sentences stay in place. Each addition is marked "(r9)", or is a short "r9" note; a note that needs more points here. The two new items are 3a and 6b. The lead decision is marked "r9, lead decision" in item 3a.

It changes the following and nothing else.

- **Item 1, premise scope.** The fact, the premise, the H-volume constraint and the "strictly below H" rule are unchanged. The objects the premise may admit gain:
  - `<root>/.opensip/local.json`, as a custody-checked configuration file (M3-B item 2's layer 4, the interactive local layer);
  - the directories the **downward** discovery walk custody-judges, from the root to each unit. Item 10 already says that item 1's scope "covers its custody-checked objects", and r9 names them;
  - for each admitted D15 member M: `M/.git` (the directory), `M/.git/config` and `M/.git/index`. These are exactly the three objects item 1 already admits for an enclosing repository, each through its own retained no-follow descriptor. **Nothing else under `M/.git`.** Any further Git object, such as `HEAD`, refs or `packed-refs`, is admitted only by C1's VCS-observation law (M3's snapshot unit), for every repository alike.
- **New item 3a, carrier capture.** S3's selection keeps the descriptor of the `opensip.json` it judged, and judges `.opensip/local.json` the same way when the invocation is interactive. B1 reads their bytes from those descriptors, at most 4 MiB. Their full metadata samples join item 3's held-fence recheck set.
- **Item 3a's order (lead decision; below).** Item 2's placement check and item 3's chain walk run first. Then come item 3a's reads, configuration resolution and X12 r4's pack admission, and then item 5's registry capture.
- **New item 6b, the member observation.** It runs at discovery, after the fence is released, on M3-B's discovery ledger. Its precondition is that item 6a's observation of W is "no repository". For each declared member it checks placement, then item 6a's admitted layout and exact index decoder, unchanged.
- **Item 8, rows.** No new code. Four new subjects:
  - under `PROJECT.ROOT_CUSTODY_REFUSED`: `member-vcs-unsupported:<reason>`, `member-outside-volume` and `workspace-root-inside-repository`;
  - under `PROJECT.SCOPE_LIMIT`: `members:<n>>64`.
- **Item 10, units.** M3-B's unit B1-b owns item 3a, and its unit B3-b owns item 6b.
- **Forbidden substitutes.** Every forbidden substitute applies to members. Four are added: item 6b without its precondition, a member admitted from the environment, any member Git object beyond the three, and any write under a member.

**Why it is safe** (M3-B item 21):
1. **No new evidence class.** The premise is the same per-filesystem fact (X2:18-22), applied to the same three Git objects and to custody-checked files of the same kinds.
2. **No new Git semantics.** Everything outside the closed layout still refuses as `vcs-unsupported`. r9 models nothing that r8 did not.
3. **One authority root.** W keeps the only ProjectId, marker, registry row and lease namespace. Members are never authority roots under W, and identity-and-evidence's identity rules (IE:41-58) are untouched.
4. **No write.** Nothing is created or written in any member: no `.opensip`, no index refresh, no config (M3-B item 15).
5. **The marker stays untracked by construction.** W is in no repository, so no index can track W's marker, and members are strictly below W, outside `.opensip`.
6. **The environment stays refusal-only.**
7. **Undeclared nested repositories keep S3's boundary.** Only W's own declaration, read as data from files W's owner controls under custody, crosses one.
8. **Read-only, per-read custody.** Every member byte the snapshot reads is re-checked between `lstat` and `open` (SL:313-315).

**Basis** (M3-B item 21). X2:18-49, X2:74-96, X2:163-215 and X2:250-280; `git_tracking.rs:1-18` and `:743-776`; SL:159-168. GROK2's r1 review of M3-B confirmed these eight points (its R7), and confirmed that a downward walk after the fence, on its own ledger, is compatible with item 9 (its R3).

**Rejected** (M3-B item 21):
- **Following a member's `.git` file (gitdir).** It would admit relocated repositories whose evidence lives outside M, which r8 refused for a reason that still holds (X2:213).
- **Running item 6b under the fence.** It grants nothing that the fence protects.
- **Admitting more Git objects in r9.** C1 has to define VCS state for single-root projects anyway, and one law should admit those objects for every repository alike.

**Controls** (M3-B item 21; B3-b's tests). Synthetic Git fixtures, created by tests in a private 0700 scratch under a synthetic H:
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

**Lead decision: item 3a's order (r9, under the owner's standing direction of 2026-09-30).** It was found while drafting r9.
- **The gap.** Neither M3-B nor r8 orders item 3a's reads, configuration resolution and pack admission (X12 r4) relative to item 2's placement check and item 3's chain walk. All are reads under the fence, so either order meets both laws. But the refusal differs: a root outside H that also has a refused pack ID would get either `outside-home` or X12's row 1.
- **Decision.** After S3's selection walk, item 2's placement check and item 3's chain walk run first. Then come item 3a's carrier reads, configuration resolution and X12 r4's pack admission, and then item 5's registry capture.
  - A misplaced root, or one whose chain fails, is refused before any configuration byte is read.
  - S3's selection walk still judges `opensip.json` where it examines it, and keeps its descriptor. Only the bytes wait.
  - This is consistent with item 5, whose placement check already runs "first" and refuses before any registry content read.
- **Rejected:**
  - **Reading the carriers, resolving and admitting packs straight after the selection walk.** The configuration of a root that item 2 or item 3 would refuse would be read, and a misplaced root could be refused on a pack row instead of its placement row.
  - **Leaving the order to B1-b.** A public refusal would then depend on the implementation.
- **Not decided here.** `members:<n>>64` still has no remedy text. It stays with successor S3 (see "The `PROJECT.SCOPE_LIMIT` remedy" below).

**Reconciliations with r8's text.** Each one states how M3-B item 21's text reads in this law. None changes M3-B's content.
- **Names.** M3-B's item numbers differ from this law's. In r9's text, "M3-B item N" is M3-B's, and a bare "item N" is this law's. M3-B's terms are its own:
  - W1 to W3 and M1 to M5 are M3-B item 19's clauses, and item 6b quotes M1 to M3;
  - B1, B1-b and B3-b are M3-B's sub-unit and units, and C1 is M3's snapshot unit;
  - "declared" means declared under M3-B item 20, and "interactive" is M3-B item 3's invocation mode.

  M3-B's short names are its own as well. Here SL is the security contract `docs/v2/contracts/product-v1/security-and-lifecycle.md`, and IE is `docs/v2/contracts/product-v1/identity-and-evidence.md`. The product paths are under `opensip/crates/security/src/custody/`.
- **`.opensip/local.json` and "never covers".** Item 1 never covers "OpenSIP's own operational files in the project, such as `.opensip/project-id.v1`". `local.json` lies under `.opensip/`, but it is not an operational file. It is a configuration carrier (M3-B item 2's layer 4), custody-checked like the S3 config file, and its custody refusal is item 8's config-file row, `CONFIG.CUSTODY_REFUSED` (M3-B item 2). The marker and every other operational file stay outside the premise.
- **The one ledger (item 9).** Item 9 charges everything "to one authoritative ledger for the operation (the session's or the gate's)".
  - Item 3a runs inside admission, under the fence, so its captures are charged to that ledger, within the 4 MiB per-record ceiling.
  - Item 6b, and the downward walk whose directories item 1 now names, are not part of admission. They run after item 7a's handoff, or the read session's equivalent release, on M3-B item 12's discovery ledger.
  - So item 9's one ledger stays the admission's.
- **The `PROJECT.SCOPE_LIMIT` remedy.** Item 8's remedy text ("This installation's project registry is at its lifetime capacity …") stays the remedy of the three registry subjects only. M3-B gives `members:<n>>64` no remedy text. Its item 24 rows are successor S3's content (M3-B item 25), so that remedy is S3's to state. r9 states none.
- **Where the new subjects apply.** M3-B item 24 decides when each new subject applies, and when a failure excludes a member instead of refusing. A member that a reader declared, and that fails item 6b, is excluded and disclosed, not refused. M3-B item 20 gives the two declaration branches.
- **Line citations.** Citations of the form X2:NNN, in M3-B, in other laws and in r9's own text, are to r8's lines, preserved in PROPOSAL-r8.md. This file's lines move with r9's header.

**Unchanged from r8:** everything else. That includes items 2 to 7a apart from the additions above; the registry capture, first registration, leases and the handoff; every forbidden substitute other than the r9 bullet; and "Not claimed". No new public code, row or detail.

**r10 (2026-10-04) carries two successors that name X2 r10, made as lead decisions under the owner's standing direction of 2026-09-30.** r9 was ACCEPTED by Grok on 2026-10-04 (`0d68e3a5…`; `reviews/grok-project-root-x2-r9`). r9's bytes, without the acceptance note, are preserved in PROPOSAL-r9.md. **Draft r10, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. Not code.

- **Where it comes from.**
  - **J1 r5**, the accepted host-pipeline law, cited as J1 (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, sha256 `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). Its successor row S7 reads "X2 r10 | security | item 6's creator branch withdrawn | J3a" (J1:852). J1 item 3 states it: "The branch 'or under the creator's `AdmittedInstallation` from 468c' (X2:202) is withdrawn, so first registration runs under an `OrdinaryWriteAdmission` only" (J1:287).
  - **J-RW r4**, the accepted resume/repair writer law, cited as JRW (`docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, sha256 `9c53bce7…`; accepted by Codex, `m3/reviews/codex-resume-repair-jrw-r4`). Its successor row RW-S1 gives this law item 4's join classification on the write gate only; new item 6c with its namespace-and-marker clause; item 8's "no new row"; and new wording for one forbidden substitute and for "Not claimed" (JRW:679). JRW item 3.4 is item 6c's content (JRW:346-371), and JRW item 2 gives its authorization (JRW:189-193). Cross-law item X-RW-5 also names item 6's leftover sentence (JRW:709).
- **Line citations.** In J1 r5, in JRW and in r10's own text, X2:NNN and r9:NNN are r9's lines, preserved in PROPOSAL-r9.md. This file's lines move with r10's text. REG is the selected registry owner, `docs/implementation/m2/project-registry-owner-selection-v2/owner.md` (sha256 `2d4b65c9…`). Its record successor, registry owner selection v3 (JRW RW-S2), is reviewed beside r10, and r10 does not rely on its bytes.
- **How it edits r9.** r9's sentences stay in place. Each change is marked "(r10, J1 S7)" or "(r10, JRW RW-S1)". The new item is 6c.
- **No product code changes here.** The code is J1 unit J3a's for S7, and J-RW unit J4b's for RW-S1.
  - **S7.** At product main `d2c00a9`, first registration has one entry, `register_on_gate`, on the write gate (`crates/security/src/custody/first_registration.rs:2183`). No creator entry exists, so S7 needs no code change, and J3a keeps it so (J1:881).
  - **RW-S1.** J4b implements item 4's write-gate join and item 6c (JRW:663).

**r10 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **S7.** First registration runs under X1's `OrdinaryWriteAdmission` only. The creator branch is withdrawn. | item 6 (r9:202) | J1:287, :852 |
| 2 | **RW-S1.** On the write gate only, item 4 decides item 6c's reservation join. Every other path keeps r9's classification and row. | item 4 (r9:184, :190) | JRW:346, :371, :663, :679 |
| 3 | **RW-S1.** New item 6c, reservation completion, with its namespace-and-marker clause: a present marker of any form requires the complete namespace. | item 6c | JRW:189-193, :346-371, :679 |
| 4 | **RW-S1.** Item 6's leftover sentence names item 6c. | item 6 (r9:256) | JRW:709 |
| 5 | **RW-S1.** Item 8: no new row. Three subjects no longer arise on the write gate from a state that meets item 6c's join. | item 8 (r9:366) | JRW:505-506, :513, :679 |
| 6 | **RW-S1.** The forbidden substitute "deleting or adopting a leftover reservation, namespace or marker" reads "deleting one; adopting one except through item 6c". | Forbidden substitutes (r9:421) | JRW:679 |
| 7 | **RW-S1.** "Not claimed: explicit recovery" excludes item 6c. | Not claimed (r9:433) | JRW:679 |
| 8 | **Units.** J3a for S7, and J4b for item 4's join and item 6c. | item 10 | J1:881; JRW:663 |

**r10 lead decisions.** Each is made under the owner's standing direction of 2026-09-30, and each names the alternative it rejects.
- **LD10-1. One revision carries S7 and RW-S1.** Both accepted laws name X2 r10 (J1:852; JRW:679, "shared with J1's S7"). They agree. J1 withdraws the creator branch, and JRW's writer is an X1 ordinary writer, never the creator act (JRW:174, :190). Each successor has its own rows in the table.
  - **Rejected:** RW-S1 in a later revision. JRW names r10, so another number would need a record note in J-RW's next revision.
- **LD10-2. In item 6c, the registry owner R is item 5's capture R0, and R0 plays R1's role.** The crashed process confirmed RESERVED, so this admission's one capture already holds the row (JRW:359). Item 6c publishes no RESERVED. Its ACTIVE replacement therefore reconfirms R0 as the predecessor, the role item 6 gives R1. The forbidden substitute "reconfirming R0 after RESERVED is confirmed" concerns a RESERVED that this admission published, so it does not apply.
  - **Rejected:** publishing RESERVED again to get an R1, which rewrites the row and which item 6c forbids (JRW:368); and a second registry read before ACTIVE, which item 6 already rejects.
- **LD10-3. No new classification.** On the write gate, a root that meets the join is RecoveryNeeded, and RecoveryNeeded then grants item 6c's completion. That includes a root whose marker is zero-length or a strict prefix, which r9 refuses before classification or classifies Contradiction (JRW:427-428).
  - **Rejected:** a new classification value. Every reader of the classification would have to match it, and no reader would see anything new: off the write gate, the row is r9's.
- **LD10-4. Item 6's leftover sentence is amended.** RW-S1's row lists items 4, 6c and 8, one forbidden substitute and "Not claimed". JRW's X-RW-5 also makes RW-S1 the change for item 6's "Each leftover is the registry owner's explicit-recovery case, which X2 does not implement" (X2:256; JRW:709). Left as written, that sentence would contradict item 6c.
  - **Rejected:** leaving it for a later revision.

**Unchanged from r9:** everything else. That includes items 1 to 3a, 5, 6a, 6b, 7, 7a and 9; item 6's steps, preconditions, replacement primitive and durable prefixes; every other forbidden substitute; and every other row. No new public code, class, exit, detail, subject or remedy.

## Problem

Under 461, an omitted ACL is unreadable at `check_descriptor_observation`. S3's directory custody requires that "the ACL was readable", so every ordinary project refuses.

Probes on this host (2026-09-30, read-only `ls -led` and `stat`):
- `/Users/sb/code`, `/Users/sb/code/opensip-ai`, `/Users/sb/code/opensip-ai/opensip` and its `.git` all omit the ACL.
- All four are on the same volume as H (`disk3s5`, the APFS data volume).
- The other mounted volumes (`/Volumes/Claude` and `/Volumes/Install ChatGPT`) are read-only HFS disk images mounted `noowners`.

Without the premise, no project root can be admitted. Without an admitted root, no ProjectId and namespace can be registered. Without a registered namespace, X3a's store binding (owner §8) and every project writer cannot exist. The product holds only the pure registry syntax (`identity::project_registry`) and the namespace lease carriers (`lifecycle::leases`). It has no native discovery, root admission, registration or lease acquisition.

## Decisions

1. **The evidence for project custody is the same omission premise, with a new, closed scope.**
   - **The fact is the same.** 458 item 3's Evidence B says that on a filesystem whose qualified row signs `installAclOmission: "no-acl-stored"`, an omitted ACL means no ACL is stored. That holds for every object on that filesystem. 458 §5 and 458c item 3 withheld it from projects by scope, not because the fact differs. This law widens the scope; it does not create new evidence.
   - **The premise.** It is the `AclOmissionPremise` of this invocation's receipt: the read receipt (458c-a) or the write receipt (X1), from the one producer.
   - **How it applies.** It applies only through `AclOmissionPremise::admits` on the retained descriptor being judged. That is the premise's own `fstatfs`: local, not union, type qualified.
   - **In addition, every object it admits must pass `is_home_filesystem`.** The premise covers only H's own volume.
   - **Objects it covers:**
     - the directories from H, exclusive, down to the project root;
     - the project root;
     - the directories S3's walk examines from the launch directory up to the selected root;
     - **(r9)** the directories the **downward** discovery walk custody-judges, from the root to each unit. Item 10 already says this scope "covers its custody-checked objects", and r9 names them;
     - `.opensip/` when it exists, as a project directory;
     - the project's custody-checked files: the S3 config file and, when unit discovery lands, the workspace marker files;
     - **(r9)** `<root>/.opensip/local.json`, as a custody-checked configuration file (M3-B item 2's layer 4). It is a configuration carrier, not an operational file (see the r9 header);
     - the Git tracking evidence of item 6a, and nothing else under `.git`: each enclosing repository's `.git` directory, its `config` file and its `index` file;
     - **(r9)** for each admitted D15 member M (item 6b): `M/.git` (the directory), `M/.git/config` and `M/.git/index`. These are exactly the three objects the bullet above admits for an enclosing repository, each through its own retained no-follow descriptor. **Nothing else under `M/.git`.** Any further Git object, such as `HEAD`, refs or `packed-refs`, is admitted only by C1's VCS-observation law, for every repository alike;
     - item 6a's fixed global Git configuration files under H, `H/.gitconfig` and `H/.config/git/config`, with the directories `H/.config` and `H/.config/git`. Each must be owned by the invoking user, with no group or other write, and one link for files.
       - Lead decision: these usually omit the ACL. Refusing on omission would break every user who has a global Git config, while the premise's fact (no ACL stored) is the same on H's volume.
   - **How the Git evidence in scope is admitted** (the `.git` evidence and the global files above; **r9:** including each admitted member's three objects):
       - Each is admitted only through its own retained no-follow descriptor, under the same premise and H-volume constraints.
       - Only a `.git` strictly below H counts, so the H-exclusive rule above still holds.
       - The lookups item 6a makes for names that must be absent (`commondir`, `config.worktree`) are custody-free negative lookups. Those names are never admitted as objects.
       - On this Mac, `.git` directories omit the ACL, so this scope is what lets ordinary repositories work.
       - Alternative rejected: refusing omitted-ACL tracking evidence. It would refuse every ordinary repository on a stock Mac.
   - **Item 6a's fixed system Git configuration files are not in this scope (r7, r8).** They are refusal-only evidence, opened by fixed path following links, with no custody judged and no premise or H-volume constraint applied. Item 6a refuses one only when it is unreadable, not a regular file, oversized, or fails the closed parse. Their location above H and off H's volume is not a refusal.
   - **Objects it never covers:**
     - OpenSIP's own operational files in the project, such as `.opensip/project-id.v1` (**r9:** `.opensip/local.json` is a configuration carrier, not one of these; see the r9 header);
     - the installation and its private descendants;
     - files read only as data, such as source and manifests read after custody;
     - any other object under `.git`: objects, refs, hooks, logs and the rest (**r9:** under a member's `.git` too);
     - a `.git` at or above H, or off H's volume (item 6a refuses it);
     - item 6a's fixed system Git configuration files (refusal-only evidence; see above);
     - anything off H's volume.
   - **Without a premise,** on a BASELINE-ATTESTED host, a V1 profile or a row without the member, every omitted ACL in scope refuses, as today.
   - **Alternative rejected:** a separate project-only profile member. The fact is per filesystem, and 458 item 6 already qualifies it per row; a second member would duplicate the qualification without adding evidence.
   - **Alternative rejected:** applying the premise to any qualified volume. External APFS volumes are commonly mounted ignoring ownership, and the qualification is by type name, so it cannot see that. A later law may widen this with an explicit `MNT_IGNORE_OWNERSHIP` refusal.

2. **Where a project root may be.** In M2 the selected project root must:
   - be strictly below H, on H's volume (`is_home_filesystem`);
   - not be inside `H/Library/Application Support/OpenSIP`;
   - not be H or any ancestor of H. Each of those contains the installation, or is shared by every project.

   A root elsewhere refuses on `PROJECT.ROOT_CUSTODY_REFUSED` with subject `outside-home`, before any registry read.

   Alternative rejected: arbitrary roots with a root-to-project walk outside H. Ancestors outside H, such as `/opt` or `/Volumes`, have no qualified custody profile, and this host has no case that needs them.

3. **The project chain walk.** Project admission walks with charged, retained, no-follow handles:
   - from `/` to H, exactly as 468 r5 step 0 does, under 465 item 4's scope;
   - then from H down to the selected root.

   **Each directory strictly between H and the root** must pass the external-ancestor predicate (458 item 1: no principal other than the invoking user or root holds a right beyond list, search and read). Item 1's premise applies to it.

   **The root** must pass S3's directory custody: owner is the invoking user or root; no other-write; no group-write unless the gid is in the explicit `--trust-group` set; no ACL write grant to others; ACL readable, or omitted under the premise.

   **Selection stays S3's.** The S3 discovery walk (launch directory upward, at most 256 levels, with the boundaries in precedence) selects the root. A custody failure at an ancestor stays a discovery boundary, as S3 says. The chain walk above runs after selection, over the selected root's chain. The selection walk is charged on the same ledger.

   **Recheck.** The chain is rechecked under the held fence as in 468 item 3's recheck set, with the project chain added. **r9:** item 3a's carrier samples join this set (see the r9 header).

   Alternative rejected: no ancestor check below H. A writable ancestor could rename the root during the operation. The registry incarnation key detects that only after the fact.

3a. **Carrier capture (r9, by M3-B item 21).** S3's selection keeps the descriptor of the `opensip.json` it judged (`project_admission.rs:240-252`), and `.opensip/local.json` is judged the same way when the invocation is interactive (M3-B item 3). B1, M3-B's resolver, reads their bytes from those descriptors, at most 4 MiB. Their full metadata samples join item 3's held-fence recheck set.
   - **Order (r9, lead decision; see the r9 header).** Item 2's placement check and item 3's chain walk run first, after S3's selection walk. Then come these reads, configuration resolution and X12 r4's pack admission, and then item 5's registry capture. No configuration byte is read for a root that item 2 or item 3 refuses.
   - A file reopened by name after the judgment is forbidden (M3-B item 2, which states this item for the resolver).
   - Owner: M3-B's unit B1-b (item 10, r9).

4. **What a project root admission is.** A private, non-Clone `ProjectRootAdmission`, produced only under a held installation fence: the 458c read session, or the 468 write gate for X1 writers. It holds:
   - the retained chain and root descriptor;
   - the canonical path bytes;
   - the root identity sampled from the retained root descriptor: device, inode, native birth, and the APFS volume UUID (`DirectoryVolumeObservation`);
   - the marker observation at `.opensip/project-id.v1`;
   - the complete registry classification from the registry owner's table:
     - **Eligible(N, ProjectId):** exactly one matching ACTIVE row;
     - **FirstUseCandidate:** marker positively absent, and no live binding to this locator or incarnation;
     - **RecoveryNeeded:** a matching RESERVED row;
     - **OneSided;**
     - **Contradiction.**

   It grants:
   - **Eligible:** namespace admission (item 7);
   - **FirstUseCandidate:** item 6's registration, under the write gate only;
   - **RecoveryNeeded, OneSided, Contradiction:** nothing.
   - **(r10, JRW RW-S1) Except RecoveryNeeded on the write gate,** when item 6c's join holds: item 6c's completion, and nothing else.

   It is never a write capability on its own. Read commands get only the classification and Eligible's namespace for read leases.

   **The native birth sampler.** It is the existing `RetainedDirectory::observe_birth` (`crates/platform/src/filesystem/directory_birth.rs`). X2 adds only its charged admission use: it is charged before it runs, and an unsupported or unreliable birth refuses, with no mtime or ctime substitute, as the registry owner says. There is no second native sampler. The sample is inert data until joined with the qualified premise and the root admission above.

   **Tracking.** Every classification that grants anything (Eligible, and FirstUseCandidate) also requires item 6a's tracking observation to show the marker path untracked. Otherwise the admission refuses on item 8's tracking row and grants nothing. **(r10)** So does RecoveryNeeded when it grants item 6c's completion.

   **The reservation join, on the write gate only (r10, JRW RW-S1).** Under the write gate, admission also decides item 6c's join, after item 5's one capture and whole-document validation and before any effect (JRW:346).
   - **The marker observation.** For that decision only, it keeps a marker that satisfies item 6c's P-PREFIX against a relevant RESERVED row's marker frame, instead of refusing it at once. r9 refuses such a marker as `marker-custody` when its ACL is omitted (`project_admission.rs:602-603`), and classifies it Contradiction when it is private (`:616`, `:684-685`).
   - **The outcome.** If the join holds, the root is RecoveryNeeded and gets item 6c's completion. If it does not hold, the admission ends on exactly r9's classification, row and subject.
   - **Every other path** keeps r9's observation, classification and row, byte for byte: the 458c read session, `doctor`, the read-only recovery selector (item 7), the settlement sweep and the ephemeral entry (JRW:175, :371).

5. **The registry read: X2 owns the first capture.** At f7acb6d, the write gate and the read session judge `project-registry.v2`'s custody without reading its bytes (`judge("project-registry.v2", None, …)`), and the retained `RequiredFile` keeps only a path and (device, inode). There is no retained capture to reuse, so X2 adds the producer:
   - **Order.** Item 2's placement check runs first. An outside-home or otherwise inadmissible root refuses before any registry content read.
   - **One capture.** Under the held fence, X2 makes one bounded, charged read of the complete registry: at most 4 MiB, through the retained I, no-follow, by the registry file whose custody the session or gate already judged. It retains the original file descriptor, its parent (I), and the file's full metadata sample: device, inode, size, mode, link count, owner, modified and changed times. It also retains the exact bytes and the decoded document.
   - **Validation.** The whole document is validated before any classification: canonical encoding, every row, ordering, and global uniqueness of live ProjectId, locator, incarnation and namespace. There is no early match. A malformed later row, or a whole-document duplicate, refuses even when an earlier row matches.
   - **The old name.** X2 requires positive no-follow absence of `project-registry.v1` under the retained I, and retains that observation.
   - **Rechecks.** Both the registry's full metadata sample and the v1 absence join item 3's recheck set, so an in-place rewrite of the registry fails the recheck.
   - **Unavailable, never empty.** A missing, unreadable, oversized or malformed registry, or a present or unreadable v1, is unavailable on the host I/O row or the incomplete row, never an empty registry.
   - **One read per admission.** Later consumers in the same admission never read the registry again. They use the current registry owner R of item 6: R0, this capture, for classification and for an Eligible root; R1 and then R2 after a first registration (item 6, item 7 and the item 7a handoff).
   - **Owner.** X2b owns this producer and its budget.

6. **First registration** follows the registry owner's ordinary first-use sequence exactly, under X1's `OrdinaryWriteAdmission` (f7acb6d) only, inside the same held fence. **(r10, J1 S7)** r9's branch "or under the creator's `AdmittedInstallation` from 468c" is withdrawn. On first use, registration runs on J1's attempt B, an ordinary writer, after the creator act has ended (J1:259-261, :287). It needs a FirstUseCandidate (item 4) with item 6a's untracked observation.

   **Preconditions before any effect.** All of these run first:
   - the registry owner's completed active-transition-recovery gate. Any active transition slot, including a terminal one not yet retired, refuses;
   - capacity: rows, bytes, and the worst legal all-registered transition wrappers, within the 4096-row profile (item 8's scope-limit row);
   - collision checks against all history;
   - occupancy of the candidate namespace path, positively absent no-follow;
   - the marker's positive absence;
   - item 6a's tracking observation.

   Each effect reserves its own post-effect confirmation work before it runs (467 item 6). Any failed or uncertain step latches, with no later registration step, no retry and no deletion.

   **The registry replacement primitive.** It is used for both RESERVED and ACTIVE, and is not a no-replace publication:
   1. Reconfirm the current registry owner R (item 6's rule: R0 before RESERVED, R1 before ACTIVE) by its retained descriptor and full metadata sample, together with its parent I. The original capture R0 is never reconfirmed after RESERVED is confirmed.
   2. Construct the complete canonical replacement document, and validate it with the same decoder.
   3. Write it to a fresh same-directory temporary name, created exclusively. Barrier that file (`F_FULLFSYNC`, the receipt's policy), and confirm it by identity and exact bytes.
   4. Atomically replace `project-registry.v2` with the temporary file (`rename`, replacing the predecessor).
   5. Confirm I's directory barrier, then recheck that the name holds the new file by identity.

   **Retained evidence advances with each authorized publication (a lead decision).** The admission keeps one current registry owner, R:
   - **R0.** R starts as item 5's capture.
   - **R1.** After a RESERVED replacement is confirmed (step 5 above), R becomes R1: the published file's retained descriptor (the temporary file's own descriptor, carried across the rename), the validated document built in step 2, and its post-publication metadata and name binding. R1 is the predecessor that ACTIVE's replacement reconfirms.
   - **R2.** After the ACTIVE replacement is confirmed, R becomes R2, and R2's exact ACTIVE row and document are the only source of Eligible and of the item 7a handoff.
   - **Provenance.** Each replaced capture becomes predecessor provenance. Its later disappearance is expected, not a recheck failure.
   - **What may change.** Only this transition may change R. Any other change to the registry name, its file or its metadata still fails the recheck.
   - **Positive absences.** These move to their new owners only through the writer step that publishes them:
     - the namespace path's absence becomes the published namespace's owner, at step 3;
     - `.opensip`'s absence, if it was absent, becomes its owner, at step 4;
     - the marker's absence becomes the marker's owner, at step 5.
   - **No second read.** No registry content is read again: the single initial capture plus the retained temporary-file owners and their validated bytes are the whole evidence. ACTIVE is never constructed from the candidate IDs alone, and no recheck is disabled.
   - **Alternative rejected:** a fresh admission between RESERVED and ACTIVE. It would add a second registry read, and R0 could still not serve as ACTIVE's predecessor.

   No-replace stays only for names that are genuinely new: the namespace directory and the marker. "Exclusive" in r1 meant only that the fence is held; r2 drops the word. Uncertainty at any step before step 5 completes stops before the next registration step.

   **The steps:**
   1. **Allocation.** Draw at most eight ProjectId candidates and eight UUIDv4 namespace candidates, each from independent OS-CSPRNG draws.
   2. **RESERVED,** through the replacement primitive.
   3. **Namespace.** Durably publish `I/host/projects/N`, holding exactly `writer.lease` and `readers.lease`, through a staged no-replace directory publication (467's primitives).
      - P0 has no `I/host` or `I/host/projects`. The first registration creates or admits each as 465 item 3 does: exact name, private custody, and a zero-rights owner allow on creation. Each also gets its own directory barrier and its parent's barrier, whether new or reused.
   4. **`.opensip` directory.** Create or admit `.opensip` under the retained project root, as 465 item 3 does:
      - exact name and S3 directory custody (item 1's premise applies);
      - a zero-rights owner allow on creation;
      - `.opensip`'s own directory barrier, then the containing project root's barrier.

      This applies to a reused `.opensip` too: existence is not a durability receipt. The retained `.opensip` handle and the root handle join the recheck set. A failed or uncertain confirmation stops before the marker.
   5. **Marker.** Create the 92-byte marker no-replace under the retained `.opensip`, with the zero-rights owner allow. Barrier the file, then `.opensip`'s directory barrier.
   6. **ACTIVE.** Recheck the current owners: the root; the `.opensip`, marker and namespace owners published by steps 3 to 5; the registry owner R1; the chain; and the tracking observation. Each is checked through its own retained descriptor and metadata. R0 and any replaced capture stay provenance and are not rechecked. Then replace RESERVED with ACTIVE through the replacement primitive.

   **Durable prefixes.** These are for X2c's tests. Until a publication is confirmed, its predecessor is the last guaranteed authoritative state. An unconfirmed write is not guaranteed absent from durable storage.
   - **Before RESERVED is confirmed:** R0 is the guaranteed state. RESERVED may also be durable; the act stops.
   - **After RESERVED is confirmed (R1):** R1 is guaranteed. The namespace, `.opensip` and marker are each guaranteed only once their own confirmation completes, and any of them may be partially present before that.
   - **Before ACTIVE is confirmed:** R1 (RESERVED) is guaranteed, and ACTIVE may also be durable.
   - **After ACTIVE is confirmed (R2):** R2 is guaranteed.

   Each leftover is the registry owner's explicit-recovery case. **(r10, JRW RW-S1)** Item 6c implements that case for an `allocationKind: random` reservation whose state meets its join. X2 implements no other leftover's recovery. Plain read admission never takes any of these barriers.

6a. **Tracking observation (both first use and eligible reuse).** This is a bounded, charged, custody-checked observation that does not depend on where S3's selection walk stopped. Lead decision: M2 supports one closed, conventional Git layout, and refuses every other layout on `vcs-unsupported` rather than modeling it.
   - **Finding repositories.** Walk the retained chain from the selected root upward to `/`. At each directory, look up `.git`, `.hg`, `.svn` and `.jj` no-follow.
   - **Refusals at any level:**
     - any `.hg`, `.svn` or `.jj`;
     - a `.git` that is not a directory (an indirection or worktree file);
     - a `.git` at or above H, or off H's volume (outside item 1's scope).
   - **Every enclosing repository.** Every enclosing `.git` directory is examined, not just the nearest. An inner repository does not prove that an outer index is clear.
   - **The admitted layout, for each repository.** The worktree root must be the `.git` directory's parent. That is proved, not inferred from the spelling, by all of the following:
     - **Effective configuration (lead decision).** M2 reads exactly Git's fixed configuration sources that can change the worktree root, bareness or path interpretation, and refuses anything it cannot bound. It does not model Git's configuration semantics.
       - **Sources, all read:**
         - **system:** `/etc/gitconfig`, `/Library/Developer/CommandLineTools/usr/share/git-core/gitconfig`, `/Applications/Xcode.app/Contents/Developer/usr/share/git-core/gitconfig`, `/opt/homebrew/etc/gitconfig` and `/usr/local/etc/gitconfig`. These are the documented default system paths of the Apple and Homebrew Git builds;
         - **global:** `H/.config/git/config` and `H/.gitconfig`, where H is the account database's home and never `$HOME`;
         - **repository:** the repository's own `config`.
       - **How they're read.**
         - **Global and repository sources:** each is opened no-follow, through a charged retained walk under item 1's custody, and capped at 64 KiB. Each is either positively absent (except the repository `config`, whose absence refuses) or admitted and parsed.
         - **System sources (lead decision, r7): refusal-only evidence.** Each is opened by its fixed path, following symbolic links (`/etc` is a link to `private/etc` on macOS), charged, and capped at 64 KiB. Each is either absent (`ENOENT` anywhere on the path) or read and parsed with the same closed parse. No custody is judged: their only effect is to refuse. They never admit, select or relax anything. Anyone who can write them already controls the machine's Git, so custody adds no protection, and requiring root ownership would refuse every Homebrew installation (`/opt/homebrew/etc` is user-owned and admin-writable) and every path through the sealed system volume. A system source that exists but cannot be read (permission, I/O, a non-regular file, over the cap) refuses as `vcs-unsupported`.
           - **Rejected:** root-ownership custody for system sources, which refuses stock and Homebrew Macs; skipping system sources, which Git honours for `core.worktree` and `core.bare`.
         - **The union** of all present sources is checked.
       - **The closed parse.** Sections, subsections, `key = value` lines, comments, and quoted values without line continuations. Section and key names are compared ASCII case-insensitively, as Git does; subsection names are compared exactly. Anything outside the subset refuses.
       - **Refusals (`vcs-unsupported`).** In any source:
         - an `include` or `includeIf` section, in any case;
         - any `core.worktree`;
         - `core.bare` set to anything but false;
         - any `extensions.*` key;
         - `core.repositoryformatversion` other than `0`;
         - `core.precomposeunicode` set to false;
         - any value the parse cannot bound.

         Version 0 means SHA-1 object names, so SHA-256 field widths never arise.
     - **The process environment.** Git honours environment variables that relocate or redirect the repository, worktree, index or configuration. If OpenSIP's own process environment holds any variable whose name starts with `GIT_`, or `XDG_CONFIG_HOME`, or a `HOME` different from H's spelling, the observation refuses as `vcs-unsupported`.
       - **Not an override.** The environment is read only to refuse, never to select a path, a root or a configuration source. So this is not an override of I or H under owner §1a, whose prohibition is on selecting from the environment.
     - **Linked worktrees.** `commondir` and `config.worktree` must be positively absent from the `.git` directory, which excludes linked worktrees and per-worktree config.
     - **Known limit (disclosed).** A Git build that uses another system configuration path is outside this fixed list. M2 claims tracking evidence only relative to the listed standard installations.
   - **The index, for each repository.**
     - **Read.** Read `index` no-follow, under custody (item 1), charged, at most 4 MiB.
     - **Integrity.** The trailing 20-byte SHA-1 over the preceding bytes must match.
     - **Header.** The signature must be `DIRC`, and the version 2, 3 or 4. The entry count gives exactly the entries that follow, with every byte consumed. Each entry hash is 20 bytes (SHA-1, as version 0 requires).
     - **Entries, exactly as Git's index-format documentation specifies.** Each entry has the 62-byte fixed part (ctime, mtime, dev, ino, mode, uid, gid, size, 20-byte object name, 16-bit flags), followed by:
       - **version 3, with the extended flag (0x4000) set:** a 16-bit extended-flags field before the path. Version 2 with that flag set refuses;
       - **versions 2 and 3:** the NUL-terminated path, then 1 to 8 NUL bytes of padding, so that the entry length is a multiple of 8. The flags' 12-bit name length must equal the path length, or be 0xFFF when the path is 0xFFF bytes or longer;
       - **version 4:** a variable-width integer N, the number of bytes to remove from the end of the previous entry's path, using Git's offset encoding (`value = b & 0x7f`, then, while `b & 0x80`: `value = ((value + 1) << 7) | (next & 0x7f)`). Then the NUL-terminated suffix, with no padding. N greater than the previous path's length refuses, and the first entry's previous path is empty.
     - **Extensions.** Each extension (4-byte signature, 32-bit size) is skipped by its size. A `link` (split index) or `sdir` (sparse directory) extension refuses. So does any unknown extension whose signature starts with a lowercase letter, since Git calls those required.
     - **No index.** A positively absent `index` means no tracked paths in that repository.
     - **The path.** The marker's path relative to that repository's worktree root is `<root relative to the .git parent>/.opensip/project-id.v1`. The relative root part must be ASCII; a non-ASCII part refuses, which avoids Unicode-normalization aliasing. It is compared ASCII case-insensitively, because APFS is case-insensitive here.
     - **Tracked.** The path is tracked if any decoded entry path matches it, whether or not the worktree file exists.
     - **Gitlinks.** An outer index's gitlink entry for an inner repository (mode 160000) is not a match, and it does not clear the outer index. Only an actual entry at the marker's path counts.
   - **No repository.** If no VCS marker is found up to `/`, the observation is "no repository". That is untracked only because every directory on the chain was looked up positively. A missing local `.git` alone is not evidence.
   - **Unreadable evidence.** Unreadable, oversized or malformed VCS, config or index evidence refuses, as does a checksum mismatch. None of it is ever treated as untracked.
   - **Rechecks.** For every repository consulted, the `.git` directory, `config` and `index` (by full metadata sample), the `commondir` and `config.worktree` absences, and every negative VCS lookup join the recheck set, on the same ledger. So do every global configuration source (by full sample, or by positive absence) and its walk. Each system source is rechecked by re-reading it: the same absence, or the same bytes.
   - **When it runs.** It runs for Eligible before any lease is taken, and for FirstUseCandidate before RESERVED. A registered marker that has since become tracked therefore refuses on the next admission, and takes no lease.
   - **Alternative rejected:** modelling Git's full configuration semantics, and relocated worktrees, linked worktrees, bare repositories, includes and SHA-256 repositories. Each adds unbounded or format-dependent evidence, and none is needed for an ordinary clone.
   - **Alternative rejected:** refusing index version 4. Its prefix compression is fully specified and simple to decode exactly, and refusing it would break repositories with `index.version = 4` or `feature.manyFiles`.

6b. **The member observation (r9, by M3-B item 21; owner decision D15).** It runs at discovery, after the fence is released, on the discovery ledger (M3-B item 12).
   - **Precondition.** Item 6a's observation of W is "no repository" (`NoRepository`; M3-B item 19's W2: no VCS marker at W or at any ancestor up to `/`).
   - **For each declared M, in ascending path order:**
     - **Placement:** M1 to M3, by positive no-follow lookups of `.git`, `.hg`, `.svn` and `.jj` at every directory strictly between W and M, and at M itself. M3-B item 19's clauses are:
       - **M1.** M is a directory strictly below W. It is reached without symlinks, on W's device (no mount change), at a depth of at most 256 segments.
       - **M2.** M holds `.git` as a directory and no other VCS marker. No directory strictly between W and M holds a VCS marker or `opensip.json`. M is not at or below `W/.opensip`.
       - **M3.** Members are disjoint: no member is at or below another.
     - **Layout:** item 6a's admitted layout, unchanged.
       - The effective configuration is the union of the fixed system sources, the global sources and `M/.git/config`, with item 6a's refusals verbatim: `include`/`includeIf`, `core.worktree`, `core.bare` other than false, `extensions.*`, `core.repositoryformatversion` other than 0, `core.precomposeunicode` set to false, and any value the parse cannot bound (X2:163-208; `git_tracking.rs:295-317`).
       - `commondir` and `config.worktree` must be positively absent (`git_tracking.rs:807`).
       - The environment check of item 6a runs once per pass (`git_tracking.rs:697-713`).
     - **Index:** item 6a's exact decoder, versions 2 to 4 with the checksum, refusing a `link` or `sdir` extension (`git_tracking.rs:429`). A gitlink in M's index marks a nested repository inside M, which stays a boundary.
   - **The workspace marker:** `W/.opensip/project-id.v1` lies in no member's worktree, by M1 to M3. This is asserted, not observed.
   - **Recheck:** the member evidence is not in the fenced recheck set, because it grants no project admission. C1's per-read custody re-check covers it at snapshot time (SL:313-315).
   - **Rows:** item 8's r9 subjects. When each applies, and when a failure excludes the member instead, is M3-B item 24's (see the r9 header).
   - **Owner:** M3-B's unit B3-b (item 10, r9). Its tests are the controls in the r9 header.

6c. **Reservation completion (r10, JRW RW-S1; JRW item 3.4).** It completes an ordinary first registration that a crash interrupted after RESERVED. It runs under the write gate only, in place of item 6, when item 4's write-gate join holds. It is the registry owner's explicit reservation recovery for an `allocationKind: random` row (REG:72-76). Law J-RW is the operation owner that authorizes it (REG:9, :74; JRW:189-192).
   - **Who and when.** An X1 ordinary writer, reached through J1 item 3's durable entry, inside the next admitted durable write request on the same root (JRW:165, :174). Never the creator act.
     - **Never on a read path:** not the 458c read session, `doctor`, the read-only recovery selector (item 7), the sweep or the ephemeral entry (JRW:175).
     - **Never in the process that crashed.** A failed or uncertain step still latches, with no later step and no retry (item 6; JRW:176).
   - **Authorization (JRW LD-2).** The write gate's `OrdinaryWriteAdmission`, for a durable request on the same root, whose locator and incarnation agree with the row. That is the authorization class, on the same root, that created the reservation. Completion runs as its own classified step in a later operation, never as the constructor's fallback (REG:74). An adopt-kind row still needs REG:76's fresh adoption context, and refuses.
   - **The join.** It is decided under the write gate, after item 5's one capture and whole-document validation (no early match), in full and before any effect: before any C-ACL, C-SUFFIX or namespace publication. All of these hold:
     1. Exactly one relevant live row, by item 4's relevance rule (`project_admission.rs:688-704`). Its status is RESERVED and its `allocationKind` is `random`.
     2. The row's locator (platform, path bytes) and incarnation (volume UUID, inode, birth) agree with the admitted root.
     3. **The namespace and the marker, together.** Exactly one of these holds:
        - **(a)** `I/host/projects/N` (N the row's `namespaceId`) is positively absent, **and** the marker is positively absent;
        - **(b)** N is present with exactly item 6's complete footprint: a private directory holding exactly two empty private lease files (REG:70). The marker is absent, exact with the row's ProjectId, or a file that satisfies P-PREFIX against the row's marker frame.

        Every other combination is not the join. **A present marker of any form, with N absent, is never the join:** exact, zero-length, a strict prefix, ACL-omitted or private (JRW N-R2, N-R9).
        - Item 6 publishes and confirms the complete N in step 3, before step 5 creates the marker (r9:239-247). The product enforces that order (`first_registration.rs:2260-2293`).
        - So under process death, a present marker implies a complete N. REG:76 already refuses the exact-marker case for that reason.
     4. `I/host` and `I/host/projects` are each absent, private, or P-ACL.
     5. Item 6's preconditions that a completion needs hold: the active-transition gate (`first_registration.rs:1310`), capacity for the ACTIVE document, item 6a's tracking observation (the marker path untracked), and the recheck set.
   - **The predicates (JRW items 3.1 and 3.2).** Each is judged under the fence, through the owner's retained parent, no-follow, charged before it runs, and before any effect.
     - **P-ACL.** All of these hold:
       1. The object is at its fixed name, at the step that creates or admits that name, on its parent's filesystem.
       2. It is owned by the invoking user. Its mode is exactly `0700` for a directory and `0600` for a file, and a file has one link.
       3. Its ACL is omitted (`CapturedAclState::NotReturned`). A NOACL sentinel, an inconsistent capture or a present ACL is not omission. A present ACL is judged as it stands, as in r9.
       4. A directory holds no entry but `.` and `..`, by one bounded scan. A file has length 0, or satisfies P-PREFIX.
     - **P-PREFIX.** A regular file that meets P-ACL clauses 1 and 2, whose ACL is omitted or judged private, and whose bytes are a strict prefix (the empty prefix included) of the marker frame of the row's ProjectId (`first_registration.rs:860`). The read is bounded by the frame's length plus one.
   - **Action.** Item 6's remaining steps, from the first incomplete one. R is item 5's capture R0, which already holds the RESERVED row (LD10-2).
     - **Step 3, in case (a) only.** Parents are created or admitted as step 3 says, with C-ACL where P-ACL holds. Then N is published from positive absence through a fresh stage. In case (b), the complete N is admitted, and its own and `projects`' barriers are reconfirmed (REG:70).
     - **Step 4.** `.opensip` is created or admitted.
     - **Step 5.** The marker is created. Or, in case (b) only, it is completed in place: C-ACL first if its ACL is omitted, then C-SUFFIX. Or, when it is exact, its file barrier and `.opensip`'s and the root's barriers are reconfirmed.
     - **Step 6.** Every current owner is rechecked: the root; the `.opensip`, marker and namespace owners, whether steps 3 to 5 published or admitted them; R0; the chain; and the tracking observation. Then RESERVED becomes ACTIVE through the replacement primitive, with a fresh temporary file, and R becomes R2.

     Item 7's namespace admission and item 7a's handoff then follow, as after a fresh registration.
   - **C-ACL and C-SUFFIX (JRW items 3.1 and 3.2).**
     - **C-ACL** appends exactly one zero-rights owner allow and samples again, through the fresh path's own step (`prepare_fresh_private_sample`, `private_access.rs:120-126`). The new sample must judge private, or the object refuses on its r9 row; the allow stays. Then the step's remaining checks and barriers run unchanged. This is 465 item 5's rule, applied to `I/host`, `I/host/projects` and the marker.
     - **C-SUFFIX** writes only the missing suffix, at an offset equal to the existing length. Then the file barrier (`F_FULLFSYNC`), `.opensip`'s directory barrier, and an exact-length capped read-back that must equal the frame, on the same device and inode. No existing byte is rewritten, so the marker only ever holds a prefix of its frame, or all of it.
   - **What it never does.**
     - It never deletes, truncates or renames an object away. It never adopts or touches an unpublished stage or a temporary file the crash left (REG:70; `first_registration.rs:1228`).
     - It never moves, abandons or rewrites the row, except to its ACTIVE. It never converts a random row to an adopt row, or the reverse.
     - It never changes a mode bit, and appends no ACE but the one zero-rights owner allow.
     - It never acts on a present marker while N is absent, and it takes no effect before the join is decided.
   - **Crash, budget and disclosure.** JRW item 6's rules govern a crash inside item 6c: each step only moves its object forward, so a run of crashes cannot cycle, and a step over a completed object is the ordinary admit path (JRW:468-484). Each step is charged to the gate's ledger before it runs, and reserves its post-effect confirmations, as item 6's steps do (item 9; JRW:514). It adds no code, row, subject or envelope member (item 8), and J1's `firstUse` stays false, because completion is not installation creation.
   - **Owner.** J-RW's unit J4b (item 10, r10).

7. **Namespace admission and leases.** **Ordering note (X3b r2 item 1).** Before this item takes any lease, with the fence held and no project lock, X3b's floor step runs once R is current (R0 for an Eligible root, R2 after a fresh registration). S7 writes trust state only under the fence and never under a lease. For `Eligible(N)`, or for a root this admission has just registered (R2), with N taken only from the ACTIVE row of the current registry owner R (R0 for an Eligible root; R2 after this admission's own first registration) and never from a caller, under the same held fence:
   - Confirm the namespace directory and both lease files under custody.
   - Take the S7 lease without blocking, starting from the existing `lifecycle::leases` two-lock implementation:
     - **SHARED-READ:** `readers.lease` LOCK_SH|LOCK_NB only.
     - **APPEND-WRITE:** `writer.lease` LOCK_EX|LOCK_NB only.
     - **EXCLUSIVE:** `writer.lease` LOCK_EX|LOCK_NB, then `readers.lease` LOCK_EX|LOCK_NB, both while the fence is held.
   - **Partial failure.** If any lock fails, release every project lock already taken, in reverse order, before the fence is released. A retry happens outside the fence under S7's existing backoff.
   - **Rules.** There is no lease without the fence, no waiting for a lease, and no upgrade. A busy lease is the busy row.
   - **The one exception (r6, lead decision): the read-only recovery selector.** `recover(ExecutionId)` takes SHARED-READ, which is `readers.lease` `LOCK_SH|LOCK_NB`, without the installation fence and without waiting. The fence stays prohibited on that path. This is identity-and-evidence §5's read-only recovery selector ("no fence acquisition and no wait on a writer") and owner §5's separately owned internal recovery selector, which is excluded from the fenced binding path. Its admission, binding reads and recheck are X6 r2 item 3's.
     - It is the only fence-free lease. Every other lease, including the settlement sweep's EXCLUSIVE leases (X6 item 7), stays under the fence.
     - It takes no `writer.lease`, writes nothing, and its lease can never be upgraded or promoted into a writer or into this item's `FencedNamespace`.
     - **Rejected:** taking the fence for recovery, which the selector's owners forbid; and a general fence-free SHARED-READ for every reader, which would bypass 458c's fenced observation path.

   The result is a private `FencedNamespace`: the held lease, the row snapshot, and the root admission. It still borrows the held fence. **X2d does not release the fence.** Item 7a decides when the fence is released.

7a. **The checked operation handoff (a lead decision; owner: unit X2e, after X2d and X3a-1).** One combined owner builds the operation context while the same fence is held:
   1. **Join.** Join the Eligible row, root admission, marker, tracking observation and `FencedNamespace` with X3a's `SelectedStoreEndpoint` from the same session or gate.
   2. **Transfer.** Move these into a private, non-Clone `ProjectOperation`:
      - the immutable row snapshot and selected generation;
      - the original project root, `.opensip`, marker and namespace owners;
      - the store endpoint and lineage owners.

      It is built by moving owners out of the fenced session or gate, never from copied fields.
   3. **X3b's carrier start (X3b r2 item 1).** It runs here, after the transfer and before the release, inside the same fence hold. X3b's floor step is not part of 7a: it runs earlier, before item 7 takes the lease (see the ordering note in item 7). X2 owns the ordering and X3b owns the steps (X3b-3 composes them).
   4. **Release the fence.** Only then is the fence released, per owner §8 and S7.

   **After the release.** The mutable registry and pair captures become provenance. An unrelated registration, or a same-schema core selection, cannot invalidate the pinned operation. Same-N move, retirement or store reselection stays excluded by the lease.

   **What it never does.** It never promotes a fenced provisional reader, reopens a session while holding the project lease, or reacquires the fence backwards.

   **Without X2e.** Until X2e lands, a `FencedNamespace` can only be dropped, which releases the lease and then the fence. X3a-1's endpoint and X3b's writers depend on X2e, not on X2d alone.

   **Alternative rejected:** X2d releasing the fence and returning `NamespaceAdmission`. The endpoint and lineage owners would not survive the release, and reopening them under the lease reverses the lock order.

8. **Refusal rows.** These use 468 item 6 and the existing `PROJECT.*` details. No new code is added; the owner allows only the three of 468.
   - **Root custody, an outside-home root, a chain predicate failure, or an unsupported volume, birth or profile:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subjects `outside-home`, `acl-unreadable`, `foreign-owner`, `mode`, `volume-unsupported`, `birth-unsupported` and the like. This is request-rejected, exit 2, `CONFIG.INVALID`.
   - **Config file custody:** `CONFIG.CUSTODY_REFUSED`.
   - **An explicit-path grammar or join problem:** `PROJECT.EXPLICIT_PATH_INVALID`, as S3 says.
   - **One-sided, contradiction or recovery-needed identity:** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `identity-recovery-required` or `identity-contradiction`.
     - **(r10, JRW RW-S1) No new row.** On the write gate, `identity-recovery-required`, `marker-custody` and `identity-contradiction` no longer arise from a state that meets item 6c's join (JRW RW-R1 to RW-R7). Every state outside the join keeps its r9 row and subject (JRW N-R1 to N-R9), and every other path keeps r9's rows byte for byte (JRW:505-506, :513).
     - The identity contract calls these admission refusals that require explicit recovery or adoption, and no identity detail exists.
     - Alternative rejected: a new code, which the owner's no-new-codes rule forbids.
   - **A tracked marker, or an unsupported or unreadable VCS, on first use or eligible reuse (item 6a):** `PROJECT.ROOT_CUSTODY_REFUSED`, with subject `marker-tracked` or `vcs-unsupported`.
   - **D15 members (r9, by M3-B item 21).** No new code. New subjects:
     - under `PROJECT.ROOT_CUSTODY_REFUSED`: `member-vcs-unsupported:<reason>`, `member-outside-volume` and `workspace-root-inside-repository`;
     - under `PROJECT.SCOPE_LIMIT`: `members:<n>>64` (M3-B item 24).

     When each applies, and when a failure excludes a member instead of refusing, is M3-B item 24's (see the r9 header).
   - **Registry capacity:** `PROJECT.SCOPE_LIMIT`, request-rejected, exit 2, `REQUEST.UNSATISFIABLE`, with no fault cause, and the S12 `field:count>limit` subject:
     - rows: `registry-rows:<n>>4096`, where n is the attempted resulting row count (4097 when the registry already has 4096 rows);
     - bytes: `registry-bytes:<n>>4194304`, where n is the canonical byte length of the resulting RESERVED or ACTIVE document, or of a worst-case later terminal spelling;
     - transition wrappers: `registry-transition-rows:<n>>4096`, where n is the namespace count of the worst legal all-registered transition wrapper.

     The remedy text is: "This installation's project registry is at its lifetime capacity. Registry entries are kept for the life of the installation and are never removed, so a new project cannot be registered here. Use a project that is already registered." It does not suggest discarding rows or compaction. **r9:** this remedy is the three registry subjects' only; it is not the remedy of `members:<n>>64` (see the r9 header).

     Actual work-budget exhaustion stays the separate `WORK.BUDGET_EXHAUSTED` row.
   - **Entropy failure, I/O and barriers:** the host I/O row.
   - **A busy lease:** the busy row (`LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`).
   - **Budget:** `WORK.BUDGET_EXHAUSTED`.

   Where S12 fixes a class for a detail, S12 prevails.

9. **Budget.** Everything is charged before it runs, to one authoritative ledger for the operation (the session's or the gate's), at the owner's caps. That includes every walk, sample, the registry capture and validation, replacement serialization, the VCS lookups and index read, original-owner rechecks, and reserved post-effect work. The selection walk is at most 256 levels. The registry and each Git index are each bounded by the 4 MiB per-record ceiling, and each Git config by 64 KiB. A larger registry is unavailable, and a larger index or config refuses as `vcs-unsupported`. The number of enclosing repositories is bounded by the chain length. **r9:** item 3a's captures are part of admission and are charged here. Item 6b and the downward walk are not: they run after item 7a's handoff, on M3-B item 12's discovery ledger (see the r9 header).

10. **Units after the law.** Each unit is reviewed with an inventory successor.
    - **X2a:** the scoped premise application (a `ProjectChainPolicy` over the shared walk code), the charged use of the existing birth sampler, and the project chain walk.
    - **X2b:** S3 root selection (no unit discovery), the item 5 registry capture producer, `ProjectRootAdmission`, and the item 6a tracking observation.
    - **X2c:** first registration (item 6), with the registry replacement primitive and the create-or-admit of `I/host/projects` and `.opensip`.
    - **X2d:** namespace admission and leases (item 7), returning `FencedNamespace` with the fence still held.
    - **X2e:** the checked operation handoff (item 7a). It depends on X2d and X3a-1, and X3a's store binding and X3b depend on it.
    - **Unit discovery** (S3's workspace units, markers, pruning and the 4096 cap) belongs to M3's analysis owner. Item 1's scope already covers its custody-checked objects. **r9:** item 1 now names them.
    - **(r9)** M3-B's unit B1-b owns item 3a, and its unit B3-b owns item 6b.
    - **(r10)** J1's unit J3a owns item 6's single admission (S7; J1:881), which needs no code change at `d2c00a9`. J-RW's unit J4b owns item 4's write-gate join and item 6c, with JRW's controls RW-C1 to RW-C4, RW-C8 and RW-C16 for them (JRW:663). Their X9 rows are J-RW's section of X9 r17 (JRW item 10).

## Forbidden substitutes

- the premise on OpenSIP's operational files, the installation, data-only files, or any object off H's volume;
- a caller-built filesystem sample or premise;
- an mtime or ctime birth substitute, or a device, fsid or marker fallback for volume identity;
- a partial or early-match registry scan;
- registration under a read receipt;
- a lease without the fence, other than item 7's read-only recovery exception (non-blocking SHARED-READ only, never under or into a writer); a waiting lease; or a lease upgrade;
- EXCLUSIVE without both project locks;
- releasing the fence before the item 7a handoff;
- an operation context built from copied fields or a released session;
- treating a missing local `.git` as untracked;
- stopping the tracking check at the nearest repository;
- interpreting an index path without the admitted layout;
- reading index paths without the exact per-version decoding;
- selecting any path or configuration source from the environment;
- reconfirming R0 after RESERVED is confirmed;
- extending the premise to any `.git` object other than the directory, `config` and `index`;
- changing the retained registry owner except through a confirmed publication;
- a no-replace publication of the existing registry name, or a registry replacement published before its file barrier;
- first registration over a tracked or unreadable marker;
- deleting a leftover reservation, namespace or marker; adopting one except through item 6c (r10, JRW RW-S1);
- a new public code;
- **(r9) D15 members:** every forbidden substitute above applies to members. In addition:
  - item 6b without the "no repository" precondition;
  - a member admitted from the environment;
  - any Git object of a member beyond `.git`, `config` and `index`;
  - any write under a member.

## Not claimed

- CLI enablement;
- unit discovery;
- explicit recovery, except item 6c's completion of a random-kind reservation (r10, JRW RW-S1); adoption, move, fork and retirement;
- project roots outside H or on other volumes;
- Linux;
- any qualified measured row for this macOS 27 host. It stays BASELINE-ATTESTED, so real project admission here refuses, and tests use synthetic signed profiles.
