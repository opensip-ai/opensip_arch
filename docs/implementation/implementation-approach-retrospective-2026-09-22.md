# Implementation approach retrospective

2026-09-22. Written when implementation leadership moved from Codex to Grok, with Claude Opus 5 remaining the reviewer. This note records the assessment of the architecture, design, and plan approach after product runtime 43 (`20d94ec`, inventory 62) and the joint ACL probe 445. It does not change selected law, accept source, or close a milestone.

## Progress against the plan

M1 is in place: build lanes, contracts, identity, and the help and version commands exist as accepted product. M2 is the current milestone. What is installed is the substrate that milestone needs. Product `20d94ec` is accepted runtime 43 on inventory 62. The run from the shared work ledger through reserved helpers, bounded readers, original-reader postchecks, and cache capture is a sequence of reviewed commits, each checked against the same accounting law. Probe 445r2 ran and its result is recorded.

The plan’s M2 exit is still ahead of that work. The build plan calls M2 done when pure replay, live security guards, the storage commit facade, and the carrier recovery join survive an opaque-API refusal suite and a crash, lock, and revocation matrix. Native capture accounting, operation ownership, profile and custody admission, initial creation, permits, publication, and current authority remain open. All 32 release gates remain unqualified. M3 through M6 have not started as product behavior. The recent commits are progress inside M2’s foundation. They are early progress against the plan’s definition of finishing M2.

## Where the design earned its cost

The expensive mistakes in this system are observations that look complete and are not: an empty writer list, a `NOACL` sentinel, a volume ACL bit, a directory link count, a link-count reachability check. The design is what made those look like failures instead of finished features.

The selected owner text requires two different ACL facts. External ancestors must show no write grant to any other principal. Private descendants must show no group or other access, including read and search. The code already had `Vec<AclWriter>`, which keeps only mutating allow entries. An empty writer list would have looked like a private directory. The design made that list insufficient before it was wired into creation. That is why the next capture module has to preserve every right and flag, and why an empty writer list cannot stand as private-access proof. Source findings for probe 445 record that obligation.

The same stop rule held for the probe. On the fixtures with no installed ACL, the attribute call omitted the ACL while the volume still reported ACL support. The design’s rule is that a volume capability bit and a successful syscall do not qualify a per-vnode fact, so 445 stayed a narrowing of the implementation choices. Claude’s earlier claim that the `NOACL` sentinel is positive proof of absence was withdrawn in route 446 after the kernel source showed that sentinel can be synthesized when ACL support is missing. The review caught a false premise before it became selected code.

The commit and crate boundaries have held the same way. Storage still cannot mint a published commit from a host boolean. The evaluator stays pure. Security does not import host. The shared ledger is one borrowed scope for the attempt, with a failure latch. Runtimes 37 through 43 were defects found against that shape: a nested scope that reported success after an inner failure, a cache hit that still had to be charged, an extra copied buffer, and a postcheck that had to see the original reader. The design did not prevent those defects. It made them local and rejectable.

Platform contact did the same thing where the design demanded a real check and refused a substitute. A link-count reachability test fails on APFS because a directory’s link count stays 2 while a stale path still opens. Birth time cannot be replaced with modification time. The Unicode data selected for the native model is version 15, which neither a newer Python environment nor the Rust standard library can stand in for. Those facts were not going to be designed correctly in advance. The design earned its keep by making the substitute count as a failure.

## Where the process spent time the design could not repay

The design can require an honest absence proof. It cannot name the macOS call that provides one. Getting from that requirement to a private capture draft went through an audit, a decoder, a route note that was later withdrawn, a probe, a corrected route, and a root qualification. The probe answered the question. The advice rounds around it cost more than they returned. One of them stated a premise that the kernel source later refuted.

Runtimes 37 through 43 show the other cost. The design already required one budget, precharge before the operating-system call, and a recheck of the original owners. Implementation turned that clause into seven accepted units, each with an inventory pin, a freeze, and a source review. Several of those reviews caught defects that belonged in the product. The unit size is also much smaller than the plan’s own M2 package, and the active-work log is thousands of lines of resume state in which each entry overrides the last. That ceremony is why a bad premise stayed out of the tree. It is also why a question the design cannot answer waited on a document before the experiment was allowed to run.

The milestone plan does a narrower job than the owner text. It is right about order: M2 before analysis, reports, and workflows, and no gate waived because a component test passed. It is not the spec implementation uses day to day. The live spec is the selected owner section plus the current runtime unit. The build plan’s header still describes itself as a proposal awaiting review, while implementation proceeds under later selected successors. The thick plan is a scope fence. The selected invariants are the part that changes the code.

## If this were started again

Follow the same approach. Keep the design in charge of authority and admission. Stop asking it to discover platform mechanics or to approve every intermediate draft.

Keep the part that changed the code. An observation and an authority stay different types. The two ACL predicates stay written down before any creator is wired. Storage still cannot mint a published commit from a host boolean. A new file still needs an inventory successor. A trust-boundary change still needs an independent review of exact bytes before it is selected. A passing component test still does not close a milestone or a release gate. Failed probes stay in the record.

Change when a question becomes an experiment, and how large a reviewed unit is.

End a design clause at the required fact and the forbidden substitute. Private descendants have no group or other access, including read and search, and an empty mutating-writer list cannot establish that. Do not go on to name the syscall, the sentinel, or the buffer size. Those are a bounded experiment with a written result. In the ACL lane, the kernel reading and the four-fixture probe were the work that answered the question. The earlier route note invented a premise, and a later round had to withdraw it. An unmeasured platform question should stay marked unmeasured until the probe exists, and the reviewer should see the probe result as part of the subject.

Review a coherent private slice once, after its tests, rather than selecting each step of the same law. The shared ledger, borrowed scope, precharge, original-reader postcheck, and cache capture were one accounting decision. The defects those reviews caught would still belong in the test suite of the larger slice. The extra selections mostly protected intermediate states that no caller was going to ship.

Narrow the native-lane lock to jobs that can interfere with each other. A read-only review of a runtime unit should not block a private probe in its own fixtures. The lock matters when two agents can mutate the same native setup. It also held the ACL measurement behind an unrelated review.

Keep one current status page and an archive. Hashes and resume instructions belong in the latest status entry. History belongs in the commits and the frozen review directories.

Give implementation a short selected charter once the owner text is accepted. The build plan remains the milestone order and the list of gates. It stops being a second spec, and it stops sitting in “proposal, implementation not authorized” while selected successors proceed under it.

Do not add more design time for Unicode tables, `fsync` errno sets, APFS link counts, or allocator behavior inside the system libraries. Those were contact with the machine. The useful rule was already there: a substitute does not count.

The repeatable version is the same gates, smaller design documents, experiments before route opinions, and reviews at the size of one shippable decision. The approach used through runtime 43 is the right one aimed one level too fine.

## What this note does not do

This retrospective does not relax a selected invariant, enlarge a review’s acceptance, or authorize skipping a source review for the private ACL capture draft. The next code unit remains the bounded descriptor ACL capture, with omitted, sentinel, and empty states kept distinct, followed by independent layout and source review before any product integration.
