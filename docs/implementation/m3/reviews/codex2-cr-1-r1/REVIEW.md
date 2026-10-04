# CODEX2 review — CR-1 r1

**REQUIRED-FINDINGS** — one required finding and one non-blocking observation.

The closed role table, completed-schema copy and structural binding are sound. The closure-only command rule needs an explicit join to D4's rejection of root-command claims before this design unit can be accepted.

Reviewed subject: `f0a5c22231a4a6c942817ce8fd311f1edf0ad58f298e8c8d9eff3cbbaa46a3d9` (9 members).

Successor: `docs/implementation/m3/snapshot-plan-c/cr-1/successor.json`, 7822 bytes, `a0e23ed18868b888f9f6c8b464fb6f2efc8bb2d423146048b9370b42122fb471`. The lead's `cr-1-unit.json` is excluded from this verdict.

## RF-CR1-1 — Distinguish required command metadata from a root-command claim

Location: `successor.json`'s SL:70 insertion; DR-103 `/manifestSchema/fields/8/semantics`; `README.md:158`.

DR-103 requires `commands` and defines the tree as “the declarative command grammar this component asks the host to mount.” Its required parentless entry is defined as the component's mounted root command (DR103:902-904). CR-1 retains this structure, keeps every other DR-103 rule applicable, and says that the host never mounts or dispatches closure-only commands.

D4, however, refuses a manifest **claiming** a root command at R10a (M3-D r3:731; PPBS:717-725). Refusal precedes mounting. A complete first-party `grammar` manifest with the required parentless command can therefore still be classified as an excluded mount request under the retained definition. `README.md:158` answers whether it becomes mounted, which does not settle whether its declaration claims a root command.

Make the role-scoped interpretation explicit: the required closure-only CommandSpec is inert structural metadata, its required root is not a mount request or EE-5a claim, and actual authority claims still refuse. This is a clarification of the commands rule; it does not require dropping fields or changing the schema again.

One exact repair is:

1. Add an insert-only DR-103 override at `/manifestSchema/fields/8/semantics`. Preserve the exact existing string, then append:

~~~text
 Under CR-1, for roles toolchain, stdlib, rust-dev-llvm and grammar, this tree is required structural metadata only. The sole parentless entry still binds to manifest.name under RJ-2; it does not request a host root-command mount, creates no mounted namespace and is never mounted or dispatched. Its required presence is not an EE-5a root-command claim at D4/R10a. Claims of project hooks, root-command authority or contribution-granted probes remain refused at R10a.
~~~

2. In the SL:70 candidate insertion, replace:

~~~text
and the host mounts and dispatches none of its commands.
~~~

with:

~~~text
and the host mounts and dispatches none of its commands. The required closure-only `commands` tree, including its sole parentless command bound to `manifest.name` by RJ-2, is inert structural metadata rather than a request for a host root-command mount; its presence alone is not an EE-5a root-command claim at D4/R10a. Project-hook, root-command-authority and contribution-granted-probe claims remain refused at R10a.
~~~

3. Replace `README.md:158` with:

~~~text
3. **M3-D (D4 at R10a).** MD:718 already admits "the role closures of MC item 7's table". D4's exclusions EE-1 to EE-5a (MD:728-731) apply to closure-only manifests too. For these four roles, DR-103's required command tree is inert structural metadata, not a request to mount a host root command, and its required presence is not an EE-5a claim. A project-hook, root-command-authority or contribution-granted-probe claim still refuses at R10a.
~~~

The JSON review contains the complete new override, including the exact parent pin and before/after strings. Carry these strings and the fourth override through the builder, passages, record and checker, then refresh the subject pins. C2a/D4 review must show that a complete signed closure-only grammar manifest with the mandatory metadata command passes R10a, that its metadata never reaches command inventory, mounting or dispatch, and that EE-5a authority-claim refusals remain. This review requests no product execution.

## NB-CR1-1 — Keep CR-T4 scoped to the existing analyzer rules

`README.md:150` says a symlink entrypoint refuses for every role. The existing owner at `9c11c53` instead resolves the analyzer entrypoint through in-tree symlinks, then checks its resulting file and executable bits (`component_manifest.rs:301-341`); CMC:123-125 describes that resolution. CR-1's new regular-file naming rule applies to closure-only roles. The proposed control would add a separate analyzer restriction.

An exact replacement for the CR-T4 line is:

~~~text
- **CR-T4.** A closure-only manifest whose entrypoint is a regular file with mode `0644` admits. The same entrypoint on an `analyzer` manifest still refuses `ENTRYPOINT_NOT_EXECUTABLE_FILE`. A directory entrypoint refuses for every role. A closure-only entrypoint that names a symlink refuses; an `analyzer` entrypoint keeps the existing RJ-3 resolution and executable-file checks.
~~~

If rejecting analyzer symlink entrypoints is intended, name that additional decision and its effect on existing manifests before C2a's implementation review.

## Requested decisions

- **Exactness:** both accepted parent pins and all three before strings match; every after only inserts. The five mapping rows exactly match MC r7 item 7. Header labels and indentation differ without changing the mapping. The role-source, mismatch and core-role rules match MC:368-385; the added closure-only rules are the disclosed LD-3 choice.
- **LD-3:** no component session, empty capabilities/permissions, and a regular-file entrypoint without an executable requirement fit the four retained-byte roles. E1 can use its fixed bundle-manifest JSON inside the existing closed tree. Tools still need their own D launch law. Commands need RF-CR1-1.
- **Other fields:** `compatibility.providerProtocol` stays a required positive integer and grants no session authority. Closure-only roles do not negotiate a provider session. Dependencies retain complete-closure/no-implicit-fetch rules and may be empty. All six declarations retain existing digest-reference or host-approved typed-absence rules; sibling release evidence does not require adding files to E1's closed tree. No further schema exception or refusal code is needed.
- **Copy and selection:** the 24,293-byte schema is precisely the 24,193-byte parent with only `/properties/role` widened, in the parent's serialization. Its unchanged `$id` and major are reasonable for an additive vocabulary extension; old hosts fail closed. Explicit candidate selection is appropriate for an input outside `verify_design`, with the disclosed review responsibility at materialization. The application evidence pins remain intact.
- **Role audit:** the arch `builder` case and all 55 product shape role cases stay negative. Independent decoding of the semantic fixture confirms `REQUIRED/role` is absent and `TYPE/role` is `builder`, with both raw pins intact. No existing negative role case becomes one of the added roles.
- **Consequential passages:** SL, BP:699-720, IE and NE supply no contrary role vocabulary or second kind derivation. DR-103's command meaning is the unresolved join. D:314's analyzer-only tuple remains correct for the sole launched role; its DRC:507 citation describes the older vocabulary. LD-5 explicitly qualifies the completion contract's old role and executable-entrypoint statements. The disclosed `closure2.protocolMajor` projection remains C2a's unchanged owner choice.
- **Structural eligibility:** the real scratch verifier accepts CR-1 alone, after CRC-1, and on current main. These synthetic bindings establish record eligibility, not acceptance of this design.

## Validation and boundaries

All 33 request pins and all 9 subject members matched. The subject members and both parent pins were rechecked before writing the verdict. `check_cr_1.py --rev cd5958b` passed.

`build_cr_1.py --check` returned **1**, solely for excluded `cr-1-unit.json`: the builder still generates the original `codex-cr-1-r1` review path while the lead draft uses `codex2-cr-1-r1`. Every generated subject file and the subject manifest compare identically. The full command is not reported as passed.

Scratch binding passed at base `9c11c53` (79 → 80), after CRC-1 (79 → 81), and on checkout `cd5958b3608f44a0035566c9d4500e5005c62e91` (82 → 83). Inventory v134 and 55 passage-inheritance entries remain unchanged. The current run verifies 40 generation sources, 48 admission sources and 15 aliases without generator/runtime execution. Outputs are saved in `content-check.json`, `build-check.json`, `verify-base.json`, `verify-after-crc.json`, `verify-current.json`, `supplemental-read-audit.json` and `final-pin-audit.json` here.

Repository access was read-only. All commands ran at nice 19; the authorized scratch verifier was the only executed product tool. No cargo, builds, tests, product generator, crash-matrix command, delegation, repository edits or commits. All review writes are in this directory. The actual OpenSIP home and private 413 fixture were not accessed.
