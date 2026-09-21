# Scoped retained time admission — successor proposal317

Unselected source proposal, not proof implementation or publication qualification. This incorporates actual315 source review and resolves the two explicit policy questions in actual Grok314 ADDENDUM and replaces its rejected predecessor traversal. Historical314 REVIEW/ADDENDUM remain unchanged. No wire-format change is proposed.312/313 schema versioning remains separate.

## Distinct evidence capabilities

An original S4 evaluation authenticates its exact source, before-image authority, original revocation context and recorded observation, and recomputes S4. Success may keep prior T. It is not proof that a floor was committed. Root/metadata OriginalContext.time requires successful non-report S4; an epoch node does not supply metadata tEval. A floor requires the exact successful L-writing S4 or successful S4.5-apply, plus the consuming clock event and admitted durable publication/context. S4.5 always replaces T, including equal L; ordinary Keep never does.

A third deliberately narrower capability is needed for recovery from missing old time proof: accepted recovery authority for a specific admitted before capsule. It is NOT complete historical RootAdmission/time admission, ordinary trust entry, or a reusable current-root grant. The API must distinguish all three, not pass a generic verified boolean or an optional check_time argument.

## Equal-L proof choice (explicit completion)

Only after both relied-on sides have admitted their exact L and corresponding proof, copy the proof of the strictly greater L. On equal L, retain the exact full NodeRef from the designated base image:

- Forward migration: the source BEFORE image (no target value exists).
- Ancestor transition: the target BEFORE image, preserving the target's existing equal floor provenance.
- Restore-recovery: the independently proven logical predecessor N, preserving the selected proven branch's provenance.

This designated-base rule applies even when the target BEFORE has ordinary S4 T and the source has S4.5 epoch T at the same L. Retain the target's exact ordinary T on that ancestor transition; do not add epoch-priority. If the base has epoch T, retain that epoch T. Two distinct epoch proofs at equal L use the same base rule, not serial or hash order. The successful epoch remains in the nonselected branch's retained audit/proof dependencies; selecting another already-admitted equal-L proof is not deleting or denying that recovery. S4.5's mandatory new-T replacement applies to its own clock publication, and ordinary Keep applies within its own evaluation; this explicit cross-branch carry rule changes neither. Restore equality retains N even if n holds a distinct epoch proof. Both closures remain required.

The other side's unequal proof identity at equal L is not itself a metadata identity fork. Both required source closures still admit; tie choice is not permission to avoid a missing competing proof. This choice uses neither hash ordering nor which side happened to be loaded first. It never merges proof records or rewrites a NodeRef to a current evaluation. The selected L is max; selecting proof does not change F's separate copy/max rule. Native producers and replay must apply the same case-specific rule. Ordinary Keep and S4.5's new proof rule remain unchanged. Actual315 review found the explicit base rule coherent subject to naming the mixed ordinary/epoch case above. This successor still requires independent review before a consumer is implemented.

## S4.5 accepted authority scope (explicit completion)

Recovery must be executable when the current old T is missing, including the common case where an accepted head's context.time points to that same input. Requiring recursive complete historical tEval through that head would erase the existing215/227 exception.

For S4.5 only, construct a private AcceptedRecoveryAuthorityForImage capability from:

1. Exact native current capsule under qualified custody/fence, with complete222 successor census, or an independently proven historical before image for replay. A caller's image, orphan admission/descriptor, numeric root version, cached boolean or structurally well-formed graph is insufficient. Current epoch application still binds the actual current native before capsule.
2. Closed capsule/record projection and exact heads.root admission NodeRef, root DocRef, RootBinding and rootVersion. The epoch's acceptedAuthority must equal this BEFORE head, never a payload root or later head.
3. Full time-free authenticity of that head's exact retained root ancestry: original anchor TCB/complete embedded chain, ordinary old/new quorum edges, authorized recovery edges and raw signature domains, intrinsic ordering/bindings, original edge revocation contexts. Use original authority/revocations, not current values to rewrite historical acceptance. No unsigned or self-selected root. Missing root/parent/authorization/raw body/envelope/history bytes remains unavailable.
4. Current complete retained revocation fact set with exact signed list/admitting-root ancestry and finite-union semantics. Apply current filtering to the held root's RECOVERY keys when authenticating the actual epoch. A cached empty fact set, omitted old history branch or malformed list is not absence.

P2 clock.timeEvidence remains a REQUIRED full NodeRef in the closed capsule. A missing field, null where the schema requires a NodeRef, malformed hash/length or other closed-record defect refuses. Only the referenced old T bytes are out of scope, not the locator shape. Root/history records' required context.time locators remain shape-checked as well.

This scope does not request historical OriginalContext.time targets or recursively replay historical floor/tEval predicates for the already accepted root/history edges. It also does not newly evaluate their original activation-time windows. Their standing is supplied by the independently admitted capsule/publication in step1; steps2–4 prove exact identity, time-free authorization and revocation prerequisites. This is an explicit operation-specific completion, not a claim the omitted historical time predicates were checked, and not the earlier314 blanket optional-integrity rule. Do not read a historical time target opportunistically and change the acceptance result according to whether it happens to be present. Required references remain structurally closed and field-present; the targets are outside this proof scope.

Current epoch body/envelope, signatures/recovery threshold, serial, exact eleven-field beforeRecord, exact pending challenge, counters, wall/monotonic/boot observation, signed-time interval/window/range checks and L preservation remain fully checked by the existing owner. Old authority expiry alone is not a recovery veto. Success publishes a new epoch T through the real clock revision and222 barriers. This capability cannot satisfy ordinary import, BEGIN/COMMIT, continuity or full restore proof. It grants no role state/head change. Subsequent metadata admission requires its own complete current S4 and normal guards.

S4.5 challenge uses its specifically owned prerequisites; this proposal does not add epoch-signature prerequisites to issuing a challenge. Safe ABORT retains its separate exact215 guards, numeric clock and outside-ceremony accepted-document causes, never L/T replacement or trust entry. No generic restrictive bypass is introduced.

## Locating consumption without fabricated predecessor records

314's load(records, capsule.previous) is invalid. previous is a bare consistency hash; ordinary historical capsules need not be stored as records. Use only full typed EventRef, PublicationRef and actually retained CapsuleImage NodeRef edges. EventHead can predate an empty-event publication.

The retained event chain provides a candidate-discovery path: start from the admitted capsule's eventHead, follow exact previous EventRefs under the single operation budget, and inspect typed clock-write/continuity/restore events. A matching clock-write must carry kind:new with proof equal to the selected T and evaluation equal to that proof. Clock writes that keep T have a distinct fresh evaluation, not another floor. An event's mere presence in a file or a successful search does not establish durable consumption.

For that candidate, load its evaluation's exact beforeImage NodeRef and validate its original input and clock projection. The before-image raw digest locates the bounded by-predecessor bucket in222; an exact consuming descriptor candidate must have this predecessor, same store, adjacent revision/nativeBefore, matching actual event, and exact recomputed after clock. Reconstruct AFTER only from the descriptor's afterProjection plus its full PublicationRef. Admit its durable-current context via the native exact current capsule or independent222 original direct-terminal proof, not from the candidate descriptor alone. Complete bucket/fork/behind/error/capacity laws remain mandatory. A candidate event cannot choose an orphan descriptor merely because its bytes match.

At a continuity/restore boundary, use the explicit full retained BEFORE-image edges and the selected-L rule above. New-store revision1/previous:null does not discard source proof. Ancestor max may select either store. Restore N can supply the logical branch but max still selects the supporting proof by value. Do not blindly choose source or N without comparing L. Exact existing event/intent/carrier joins still own whether the carry actually occurred; the event chain alone is not a transition validator.

Retention is recursive over required typed dependencies, not just the latest live pointer. Every retained event's previous EventRef remains live, including events preceding the current eventHead. Every continuity event needed to explain carried T retains sourceBeforeImage and any targetBefore.image plus their required dependencies. Superseding the live sourceFence does not remove that earlier continuity event from the event chain or reclaim its image. A restore's proof images and original direct terminal witness remain live. Under222's no-GC rule, none of these may be compacted away. Any future compactor needs a reviewed successor that preserves an equivalent complete proof and its locator; this proposal grants no cleanup authority.

Consequently a lawful carry producer must leave a full path from the resulting capsule through retained events or its live fence to the image supplying selected L. That reachability is a publication invariant, not an asserted cached flag. Readers fail unavailable on a missing required EventRef/image, malformed edge, cycle or exhausted operation budget. They never scan unrelated lifetime records or silently select the other equal-L proof. This makes retention explicit using existing typed edges; no reverse index or new wire member is introduced.

This is a proposed bounded discovery strategy, NOT a proven total algorithm. In particular, the reviewer must check whether every lawful current/proven capsule exposes enough edges to the establishing event and descriptor, whether old retained event-chain gaps are allowed by existing retention, and whether durable-publication proof can be found without an unowned reverse index. If not, specify the exact missing owner/retention datum; do not silently search lifetime storage or invent a raw capsule at a bare hash. Generic structural DFS is not this semantic proof.

## Required adversarial validation before consumer implementation

- First accepted root whose context.time equals now-missing old T; recovery succeeds only with independently admitted current standing and all non-time authority/history bytes.
- Missing parent, original recovery authorization, original revocation branch, current list, malformed required time reference, orphan head, rolled-back current capsule or foreign head must not use the exception.
- Epoch node supplied as metadata/root tEval rejected; S4 Keep evaluation accepted only after its complete ordinary prerequisites, not via recovery-scoped capability.
- Equal-L distinct T in both ancestor directions and restore, unequal values, one missing source proof, identical refs, changed envelopes and misleading digest order.
- Empty-event outcomes, repeated Keep writes, cross-store first revision, selected target proof, S4.5 equal-L replacement, abandoned clock descriptors, competing proven successors, absent dependency and exhausted shared budgets.

Native313 only emits closed input nodes and target references. It does not implement any capability or discovery strategy above. No product source selection, implementation readiness or overall M2 approval follows from this source proposal.

## Consumer scope must cover the whole prerequisite path

The S4.5 exception is not implemented by deleting two fields from a generic DFS. Current/proven capsule standing has its own narrowly scoped native-custody/publication/census constructor. That constructor must not eagerly replay old clock evaluations through descriptor events or role-event clock.by links and thereby reintroduce the same missing-old-T dependency. Closed records, locator identities, store/revision/projection/event ordering, independent original direct durability witness, current census and physical custody remain checked according to222. Structural publication proof cannot manufacture accepted standing from arbitrary supplied bytes; native/current standing is a qualified physical premise, and historical standing requires the independent original proof chain.

This source proposal does not yet specify a complete native scoped traversal implementation. Before implementation, enumerate the exact fields and predicates requested at each operation-specific constructor, including event/operation paths. An omitted target must be genuinely outside the requested predicate, never a silently failed required read. If a purportedly independent standing proof in fact requires the missing historical time input, report that unresolved dependency; do not turn it into success or call a partial graph a complete proof.315's source approval and316's literal bindings do not settle that implementation obligation.
