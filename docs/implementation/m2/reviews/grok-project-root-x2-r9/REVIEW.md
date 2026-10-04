# X2 r9

**Verdict: ACCEPT.** r9 carries M3-B item 21, and the one added lead decision on item 3a's order is sound. The disclosed remedy gap stays with successor S3.

## Subject

`docs/implementation/m2/project-root-x2/PROPOSAL.md` is 55434 bytes, sha256 `0d68e3a5e70578d43f95c107adc803abacf98cc84b16e4171af1d0bc27003065`. `PROPOSAL-r8.md` is 39036 bytes, sha256 `c31d9a020f91650fb1c85f6697bffac1902bf3607d501e5821f48cd8c4b301b5`, the r8 subject. Every pin in this review's `hashes.txt` matches. Product main is `3e64266aa8729160cd22509dcfff95a3bb09fcea`. `git_tracking.rs`, `project_admission.rs` and `project_chain.rs` have the same blobs at `30c5db1`. The live M3-B file differs from accepted `PROPOSAL-r2.md` by the acceptance note only. `~/Library/Application Support/OpenSIP` is absent. No product cargo was run.

The diff against r8 is the r9 header, the title, the sentence that r8 was accepted, and body additions each marked `(r9)` or `r9`. Items 2 through 7a, the registry capture, first registration, leases, the handoff, and "Not claimed" stay as r8 wrote them, apart from those marked sentences.

## Item 21 is carried

M3-B item 21's normative text is in r9, with the names glossed as the header says.

- Item 1 gains `<root>/.opensip/local.json`, the downward-walk directories, and for each admitted member exactly `M/.git`, `M/.git/config` and `M/.git/index`. The fact, the premise, the H-volume constraint and the strictly-below-H rule stay.
- Item 3a keeps the `opensip.json` descriptor S3 judged (`project_admission.rs:240-252` opens and custody-judges that file inside `examine`) and judges `.opensip/local.json` the same way when the invocation is interactive. The byte read is at most 4 MiB, from those descriptors, and the metadata samples join item 3's held-fence recheck set. Reopening by name stays forbidden.
- Item 6b runs after the fence is released, on M3-B item 12's discovery ledger, only when item 6a's observation of W is `NoRepository`. For each declared member, in ascending path order, it checks M1 to M3 and then item 6a's layout and index decoder. The quoted M1 to M3 clauses are M3-B item 19's sentences. Member evidence stays out of the fenced recheck set.
- Item 8 adds `member-vcs-unsupported:<reason>`, `member-outside-volume` and `workspace-root-inside-repository` under `PROJECT.ROOT_CUSTODY_REFUSED`, and `members:<n>>64` under `PROJECT.SCOPE_LIMIT`. No new code.
- Item 10 assigns 3a to B1-b and 6b to B3-b.
- The forbidden-substitute list applies to members, and the four new substitutes are item 6b without its precondition, a member admitted from the environment, any member Git object beyond the three, and any write under a member.
- The eight safety points, the basis, the three rejected alternatives and the control fixtures are item 21's, including the X2:NNN ranges. Those ranges are r8's lines: X2:18-22 is the fact and the premise, X2:18-49 is item 1 through its rejected volume alternative, X2:74-96 is the admission and its tracking requirement, X2:163-215 is item 6a, X2:213 is the rejection of relocated and linked worktrees, and X2:250-280 is item 8 through item 10's custody-scope sentence. X2:280 is the sentence that item 1's scope already covers unit discovery's custody-checked objects.

## Reconciliations

`local.json` is on the objects-it-covers list as a configuration carrier, M3-B item 2's layer 4. Item 1's "never covers" bullet stays the operational-file bullet, with the marker as its example. Item 8 already has the config-file row `CONFIG.CUSTODY_REFUSED`, which is the custody refusal M3-B item 2 assigns to a project or local carrier.

Item 9 still charges admission to the session or gate ledger. Item 3a's captures are admission work under the fence, inside the 4 MiB per-record ceiling. Item 6b and the downward walk run after item 7a's handoff, or the read session's equivalent release, on the discovery ledger. That is M3-B item 12, and it matches r8's X2:231-248, where item 7a releases the fence at its last step. GROK2's r1 review recorded the same reading as R3.

Item 8's registry-capacity sentence stays the remedy of `registry-rows`, `registry-bytes` and `registry-transition-rows`. M3-B item 24 decides where the new subjects apply. A member that a reader declared, and that fails item 6b, is excluded and disclosed. M3-B item 20's two branches are the declaration rule r9 points at.

## Item 6b reuses the closed layout

Item 6a's refusal list at r8 lines 182-189 is the list item 6b repeats: `include`/`includeIf`, `core.worktree`, `core.bare` other than false, `extensions.*`, `core.repositoryformatversion` other than 0, `core.precomposeunicode` set to false, and any value the parse cannot bound. `check_config` at `git_tracking.rs:295-317` refuses those keys. `decode_index` at `:429` is the version 2 to 4 decoder with the checksum, and its comment refuses a `link` or `sdir` extension. `observe_tracking` at `:697-713` runs the environment check once at the start of a pass. `commondir` and `config.worktree` are required absent at `:807`. Item 6b adds no Git object and no new refusal.

## Item 3a's order

The decided order is S3's selection walk, then item 2's placement check and item 3's chain walk, then item 3a's carrier reads, configuration resolution and X12 r4's pack admission, then item 5's registry capture. A root that item 2 or item 3 refuses contributes no configuration bytes. Selection still judges `opensip.json` and keeps its descriptor.

Item 5 already says the placement check runs first and that an outside-home or otherwise inadmissible root refuses before any registry content read (r8 line 98). Registry capture stays after placement. X12 r4 item 8 runs `admit_policy_selection` immediately after configuration resolution, and resolution immediately after the selection walk and the carrier captures, and it runs before item 5. r9 puts placement and the chain walk before the captures, so resolution still follows the captures and pack admission still follows resolution, ahead of the registry capture. X12 r4's own header reads its "immediately after" phrase the same way: immediately after the captures, which follow those two checks. Both checks are reads under the fence. The rejected alternatives, reading the carriers straight after selection, or leaving the public subject to B1-b, would let a root outside H be refused on X12 row 1.

## The remedy gap

`members:<n>>64` has no remedy sentence in M3-B or in r9. The native model keys `SCOPE_LIMIT_REMEDY` per field (`native_evidence_model.v2.py:4080`), and X7 r2 records that X2 item 8 and S12 fix `PROJECT.SCOPE_LIMIT` for the registry subjects. r9 keeps that registry sentence on those three subjects and states no members remedy. M3-B item 25 gives item 24's rows to successor S3, the contract successor B-S1, and item 21 does not contain remedy text. Stating one here would add content S1 was not given. The row has no code yet. S3 is the successor that publishes it, and it is the place for the field's remedy. That deferral is acceptable for this law.

## Anything else

Nothing else in r8 changes. The opening sentence that r8 was accepted on 2026-10-01 is the note this request describes.
