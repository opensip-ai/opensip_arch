# Proposed169: reconcile recovery admission with the S7 lease boundary

Owner investigation, not selected law or implementation. Parent: frozen marker-routes-reference-checkpoint-167 (SHA25648608156abb79ecffab1a4d014ea594e82a74220e24f0b23720df10e71ccfc6f), reviewed by actual Claude. Product context: frozen168, still independently unreviewed at drafting. No source mutation accompanies this proposal.

## Concrete conflict

- candidate/docs/v2/contracts/product-v1/security-and-lifecycle.md S7 (around738–747) requires fence→nonblocking project lease for every lease: "no lease without the fence". Operation end releases lease before any later fence acquisition. SHARED-READ uses readers.lease LOCK_SH|LOCK_NB and coexists with APPEND-WRITE. Namespace registry admission is under the fence.
- candidate/docs/v2/architecture/commit-recovery-readonly.v3.md §2 prohibits the install fence and any waiting "for the whole algorithm", but its Step0 then says "Take the SHARED-READ project lease per S7 and obtain the custody-admitted store binding ... registry". It never states that lease admission happened before the algorithm.
- Actual lifecycle/src/leases.rs correctly follows S7: IdleActor.try_fence→FenceHeld.project_lease→fence released, ProjectHeld remains. It offers no fence-free acquisition. Do not invent one just to satisfy the narrower paragraph.

These statements need an explicit boundary before host composition. The kernel and existing SQL/file candidates take already supplied context and cannot resolve it by themselves.

## Recommended correction to review

1. A recovery invocation first uses the ordinary host admission phase: acquire the install fence using S7's existing bounded policy (up to5s), validate the registry/store binding and acquire SHARED-READ once, nonblocking. Release the fence after handoff, retain the admitted project lease/binding for the entire recovery read and its consuming observation. No writer lease or upgrade is taken.
2. The bounded read-only recovery algorithm starts only after that admission succeeds. Step0 should **receive and validate the already-held admitted SHARED-READ context**, not acquire a second lease. From that point onward the existing prohibitions apply: no install fence, writer lease, writes, waits, repair or grant. Exactly one ledger snapshot and at most two journal snapshots/four W/four floor reads remain unchanged.
3. Explicitly state end-to-end scope: a public invocation may use the existing bounded fence wait in its preceding normal admission phase; the recovery read itself waits on no lock/writer. A fence/project-busy admission returns the existing admission failure and never starts the ledger/journal algorithm. This is not a hidden claim that the entire command is fence-free.
4. S7 should cross-reference this boundary so callers do not bypass its registry/lease ordering. A nested caller already holding the right admitted SHARED-READ context reuses it; it must not acquire the fence while holding that lease. A caller holding an incompatible mode must release/re-admit at the outer operation boundary under existing laws, never upgrade in place or restart a latched committing session.
5. No writer settlement, namespace registration, currentness/authority grant, new public vocabulary or changed flock compatibility follows. No change to the pure Python models is needed: they model admitted projections/lease compatibility, not this physical host entry point. Their passing lanes do not prove a real admission owner exists.

## Questions for actual Claude's independent review

Check whether an existing selected owner already explicitly resolves this apparent conflict; quote it if so. Otherwise assess whether the recommended boundary preserves the intended S7/readonly guarantees, including invocation-level wait disclosure, reuse without reacquisition, namespace registry/custody retention and no settlement/authority. If it does, a narrowly frozen reference correction to the two owners (with manifest rebindings) can be authored and independently reviewed before host integration. Do not change frozen/product sources or claim this proposal accepted. An alternative must preserve registry consistency and no fence while holding a project lease; merely adding a fence-free constructor is not an adequate resolution.
