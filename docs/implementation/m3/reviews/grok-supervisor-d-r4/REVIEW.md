# M3-D r4 — REQUIRED-FINDINGS

Subject `docs/implementation/m3/supervisor-d/PROPOSAL.md`, 202935 bytes, sha256 `114e9e106ce92374df6d961b96cace40356d6fdb89bff346a92d35f898e966dc`, matching the pin. Base is accepted r3, `9679dbc4…`. The r3 and r2 history tables are byte-identical to r3's. The diff's other hunks are the r4 changes table, re-cited line numbers, or the record updates that table names.

r3 required no findings. Its one observation, the r2 history sentence, is corrected at PROPOSAL.md:18 and the acceptance note is removed at PROPOSAL.md:20.

Product reads are `git show 052d3cb`. `crates/security/src/component_manifest.rs` is 21818 bytes, sha256 `d70c75b1…`, the same blob at `3e64266` and at `3fe7eb5`. No commit from `052d3cb` to `3fe7eb5` touches `crates/platform`, `crates/contracts`, `crates/security`, `crates/identity` or `schemas/`.

## LD-R4-1

EE-5a's "root command" is a claim on the host-owned root namespace. PPBS:719-720 excludes a manifest claiming a project hook, root command, or contribution-granted probe. PPBS:700's EE-3b input names policy, persistence, rendering, termination, and host-lifecycle authority, and names no command. AQ:343 says a component cannot acquire those powers by declaring a root command. AQ:345 gives every command to the closed host inventory and excludes root-parser extensions. D-012 clause 2 keeps the root namespace host-owned and flat, and keeps the grammar below one mounted root declarative and host-interpreted. Clause 3 forbids claiming or aliasing a reserved name. DR103:899-904 requires one parentless entry, and its name must equal `manifest.name`. DR103:926 permits depth below that root and nothing above it.

The predicate admits a lawful analyzer: one parentless entry named for the component, any depth below it, and no reserved root-namespace key. CMS `$defs/command` is closed (`additionalProperties: false`, fields name, description, aliases, parent, visibility, options, args, scope, outputModes). `outputModes` is not a right to render, and `scope` only tells the host whether to enter a project scope. EE-3b keeping only the capability form matches PPBS:700 and PPBS:720.

(b) and (c) match the security code. Lines 178-184 refuse a tree outside the one name-bound root. Lines 257-270 build the key set the law names (manifest name, manifest aliases, parentless-entry aliases) and refuse a reserved name. Both `validate` and `validate_inventory` call that function. Live-name collisions stay RJ-2, in `validate` only (lines 271-276), which is CR-1 r4's CR-T9 correction. In-tree collisions stay RJ-2.

(a) is CR-1's D4 join: a closure-only role (`toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`) that declares `commands` is an EE-5a claim, refused by the closed schema (RJ-6) once C2a materializes it, and at D4 when the tree is presented there (CR-T8). Until then the generated shape admits `analyzer` only, so (a) has no product member. Hooks and probes stay in the EE-5a row without a new structural predicate; r4's amendment is the root-command arm.

PROPOSAL.md:776 states that division accurately, including that (a) waits for C2a and that a value RJ-2 or RJ-6 refuses never reaches R10a. D4's arm is the backstop DR-G29 requires, which is why CR-T8 can present a closure-only tree at D4's interface. Production still has one route for each condition.

D4-T4's last bullet does not. It says a source pin shows the checks for (a), (b) and (c) running in both entry points. (b) and (c) do. (a) is not in the pinned file. That is RF-1.

## LD-R4-2

`REQUEST.UNSATISFIABLE` with `PROVIDER.NOT_SELECTED` is an honest existing route for a request-class excluded form once SD-7 widens the remedy. The request is well formed and the host has made no error, so the class is request-rejected 2 and the code is the unsatisfiable code. The detail is the existing public detail for a well-formed request the product has made no promise to serve. NES:523 allows reuse when the code-keyed remedy is a true next step, and requires the author to widen that string when it is not. NEM:1159 today says the capability is not selected for that language mode. The law says that sentence is widened, not shipped, and D4-T2's remedy assertion follows SD-7. The subject `excluded-form:<class>` tells the caller which form was refused. No new public code is added.

The rejected alternatives do not fit. A host-invariant is J1:315's route for a malformed library request (NE:3573). SD-5's `EXTENSION.ADMISSION_REJECTED` / `PAYLOAD-NOT-ADMISSIBLE` is the bound route for an installed signed manifest. `CONFIG.INVALID`'s remedy says the request is malformed. An absent detail still leaves the failure envelope owing a detail (NES:522). A dedicated code would be an owner decision; this law discloses that choice and keeps the existing code under the widening constraint.

The warrant sentence at PROPOSAL.md:817 quotes NE:3577-3579 as NE's own rule for an excluded-form request. Those lines are the rule for a NOT-SELECTED capability cell. The route does not depend on that splice, because the next sentences require the widening and name SD-7. NBO-1 gives the replacement, including the changes-table clause and row 57's source column.

## LD-R4-3 and SD-7

The split matches the first consumer of each remainder. `MemoryBudgetBelowCeiling` lands with D3a before J2b's first provider stage. The two tool bounds land with C3b. `confinement-refused` lands with D1b and only if O7 is decided as recommended. None gates D4. Each still needs J1's matrix row and a detail chosen by SD-5's existing-code test. Whether a contract row is also owed is SD-5b's question, as the law says.

Reading SD-5's bound row through item 24 until SD-7 binds is lawful. The bound condition text still contains r3's parentheticals, including "a `commands` entry for role `analyzer`" and the remedy "declare a project hook, root command or probe" (SD-5 `PASSAGES.md`). The law says those parentheticals describe D's representation, the row routes whatever D4 refuses as `ExcludedForm`, and no route depends on the old wording. That is the same disclosed pattern as a later conformance successor.

SD-7's form constraint matches `verify_design` at `052d3cb`. A second passage override of the same parent and selector with a different override object raises `conflicting contract passage overrides`. Passage supersession selects an inventory row description, so it is not the form that changes NE:3540. The law therefore sends (a) to a superseding form: B-S9's complete-copy form, or a `verify_design` successor. The drafter chooses. (b) widens `PROVIDER.NOT_SELECTED` in B-S9's selected model copy. (b) lands before J2a projects item 25. (a) is recommended before D4's integration review. Neither gates D4.

## Record items

M3P9:323's D items are applied. D4-T1 samples when R10a or ER10a returns the refusal, and D4-T2 samples when R1 returns, before step 1's render draw. J1:344 is that sample, and J1:347 is the later render draw, which is not bound to the analysis attempt. First use is route 3b for `Published`, `LostRace` and `NotPristine` (J1:233-238); `created` is set for `Published` or a refusal after the rename (J1:239-243). D4-T1 runs once for each result. SD-6 is recorded as landed: J1 r4 places R10a (J1:325) and ER10a (J1:426, J1:431) and J-C10b (J1:343-349), and MC r7 narrows item 16 row 8 to a selection among the manifests R10a admitted (MC r7 item 16, the row 8 cell). SD-5 is accepted, bound, and split into the done route and SD-5b. F7 cites M3-H r3 item 4 (MH:242-263) and X-H2 (MH:859): discard the candidates and admit the terminal Coverage. FA-1, bound at `f97c02b`, is the native successor that replaces NE:3849-3850.

Item 17 follows L r5 item 12.1. That item counts stderr and retains no text, and L's own note says the D law's departure closes. The r2 history table still records the old departure sentence, which is what a history table keeps.

J1's remapped pins that this round checked resolve to the r4 bytes: the ExecutionId draws and reservations (J1:175-195, with the durable draw at J1:177, the ephemeral and render draws at J1:178-179, and the prelude at J1:176), R10a in the order (J1:308-328), the session open (J1:455-458) and the census after the handoff (J1:459), and matrix rows 18, 19, 27, 28, 30, 46 and 49 inside J1:638-709. M3P r6 carries the gate sentences at the lines r4 cites: "CF-P → D-law acceptance" at M3P:83, the D row at M3P:211, day 0 at M3P:255, and "D-law acceptance after CF-P" at M3P:259. The quoted gloss "D-law acceptance needs CF-P" is r3's paraphrase of that row, moved down two lines with the snapshot. MC items 7, 12 and 16 keep their numbers; item 7 is the role-to-kind table, item 12 names the adapter scratch bound, and item 16 row 8 is the narrowed selection.

J1 does not yet contain matrix row 56. S20 at J1:774 says item 10 has no such row until the successor lands. Item 24, the SD-5 cell and X-D4-J1-2 say J1 records row 56. That does not change D4's envelope. NBO-2 gives the replacement.

Section F remains an O7 placeholder. Its one touched line is an M3P re-citation.

## RF-1

D4-T4's source pin, PROPOSAL.md:804.

Replace that bullet with:

> **a source pin** shows that the security owner's checks for (b) and (c) run in both `validate` and `validate_inventory` before any value reaches D4 (`component_manifest.rs:178-184` and `:268-270`, both called from `:414`), and that (a) is absent from those bytes. (a) is CR-1's closed schema (RJ-6) once C2a materializes it. The live-name check (`:271-276`) runs in `validate` only and is not this pin.
