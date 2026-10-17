# D3A-1-r2 review

**Verdict: REQUIRED-FINDINGS — two required findings, one non-blocking observation.** Both proposed amendments, **LD-D3A-18** and **LD-D3A-19**, are accepted as content amendments; the implementation is not accepted until the remaining lifecycle issues are fixed.

## Subject and checks

The 17,479-byte subject manifest hashes to `b6d4c56ef9f62468e2f1d24ca7b70f5de063675fb0286859fae88130fdb6e640`. **All 74 members match.** All 12 candidate files match product-map.json and its archives; all nine existing parents match product `b7538549b727e13013f36d3b7c2e2917e767f3f2`. The candidate is detached at that base and has exactly the declared nine modified and three new paths. The four authority pins in source.json match. The architecture base is `a87c1234b26544e65cd2d36b613f218da41b4e86`.

The only executed project check was the expressly permitted `python3 -I -B tools/check_operability.py source --repository .` in the candidate: **passed, 114 rows, no findings**. No Cargo, rustc, build, lane, network, delegation, installation, private fixture, signing key, held tree/store or T2 access occurred. Other results below are inspected pinned evidence, not tests rerun during this review. Only REVIEW.md and review.json were written.

## Required findings

### D3A1-R2-RF-1: Mark the unwind kill before attempting the reap so its confirmation is retained

`crates/components/src/supervisor.rs:1843`

The loop path fixes round-1 RF-9, but unwind still sends SIGKILL and calls try_reap before setting ladder.kill_at (1839-1855). try_reap captures tree_confirmed only when kill_at is already present (1710-1712). Therefore Drop from Handshaking or Running can successfully reap a root-only child with no saved confirmation. unwind then sets kill_at and settle falls back to confirm_tree after reap (1742-1744), when the root-only group is empty. This reports Incomplete for a successfully killed root-only group and performs the by-pid confirmation after losing the zombie-root hold. The new tree-report test covers the normal fault loop, while the Drop tests check group/scratch cleanup but not this report.

Required change: Record the unwind kill state before the first reap attempt, or explicitly capture the same pre-reap confirmation on every unwind reap path. Reuse that observation in settlement; never fall back to a by-pid confirmation after a successful reap. Add Drop/unwind controls from Handshaking and Running that inspect the resulting tree report (or a test seam capturing the settlement), including root-only and missed-member cases.

### D3A1-R2-RF-2: Close handle admission atomically with the final settlement drain

`crates/components/src/supervisor.rs:487`

The settled flag check and try_send are separate operations. A sender can observe false at :488, pause, let settle set the flag and drain the channel at :1797-1802, then resume and enqueue successfully at :492. Public run has already stopped servicing the receiver, so this trigger is neither merged nor counted as late; host_fault returns true and late_events remains unchanged. Acquire/Release ordering does not make the check/send pair atomic. The new public test sends only after run has returned and therefore misses this interleaving. The sequential late-send case is fixed, but the cross-thread lifecycle guarantee remains incomplete.

Required change: Give handle admission and settlement closing/draining one synchronization or linearization protocol, so every accepted pre-close trigger is accounted for and every post-close request is rejected/counts exactly once without a consumer turn. Preserve bounded nonblocking trigger handling. Add a deterministic concurrent control using barriers around the pre-send check and settlement close, and assert the return value, final count and absence of an unaccounted queued trigger.

## Amendment rulings

**LD-D3A-18: accepted.** Keeping an abandoned unreaped root's scratch is a sound custody/lifecycle consequence: removal cannot safely proceed while that root may still run. The amendment adds only `root-unreaped` to LD-D3A-17's retained-reason shape, with no invented errno or work-exhaustion claim. Its item-12 settlement content, item-20 retention rule and item-21 registry-literal addition agree. The code uses Retained(RootUnreaped), abandons the child hold, and requires a real zero exit for admissibility, so clean-first-cause plus unreaped still admits nothing. D3a-3 remains responsible for the stated ordinary registration. This does not widen user-cancellation/revocation authority, excuse a missed reap ceiling, or authorize removing a held root's scratch.

**LD-D3A-19: accepted.** A component's accepted control fault is a provider-spoken internal-failure report whose meaning belongs to the owning contracts. Explicitly including it in provider-protocol narrowly fills the closed-cause gap without inventing a new cause, D9 route, participant FAULT transition or process event. It follows the existing fault ladder and supervisor-fault cancel reason, and does not relabel a host-observed refusal. The control-fault fixture checks the cause, unchanged fd1 HelloAck bytes and only protocol-owned EOF/signal-death events. Text remains excluded; the promised length-only reduction is the later record owner's duty.

## Round-1 findings and requested controls

| Round-1 item | Assessment |
| --- | --- |
| RF-1: service fairness | Resolved on the active loop. Stderr/control reads are capped at 16 per turn and trigger consumption at 4. Control acquisition itself makes one bounded read. The first refusal stops retriggering that direction; later causes are retained once each. Thread-limited always-ready stderr, control-storm and trigger-storm controls exercise the intended scheduling guarantee. |
| RF-2: clean reap ceiling | Resolved. check_clean records clean_at; next_deadline includes it; reap_step expires it with ReapCeiling and settlement. The reap_blocked normal fixture checks unreaped, RootUnreaped, no admissible output and one settlement. |
| RF-3: EINTR deadline | Resolved. The original absolute deadline is checked after EINTR; expiry clears readiness and returns zero, including one zero-timeout sample. The always-EINTR injected control is bounded on its own thread. |
| RF-4: deferred shutdown | Resolved for the requested scheduling case. Shutdown waits for the older pending write and owed health report, uses ControlSession::send once, retains write offset and closes fd3 only after that frame finishes or the session actually refuses it. Cancel is deferred separately and T-2 does not wait. Stalled health-write and one-byte-write controls assert one shutdown and clean completion. |
| RF-5: settlement shape | Resolved with LD-D3A-18. Prepared decline consumes supervision with no spawned settlement; spawn failure is RunError; spawned settlements always carry ExitClass. NoScratch and optional exit are gone. |
| RF-6: health nonce | Classification resolved. The additive D2a detail is attached only to a healthReport nonce mismatch; other RF7 cases retain their family/class/bytes/buffering. The supervisor maps that detail to LivenessMissed/Liveness. Busy, wrong-nonce and sequence-gap controls remain distinct. See NBO-1 for evidence handoff wording. |
| RF-7: accepted fault | Resolved by accepted LD-D3A-19 and the control-fault fixture. |
| RF-8: independent death | Resolved for the requested ordering. Exit observation records whether the ladder had signalled; independent early death can be retained after EOF's provider-protocol trigger, while ladder-caused death is only its real process event. Brief-held fd1, past-drain and EOF-early cases cover those orderings. |
| RF-9: tree confirmation | Resolved on the ordinary fault-loop path, incomplete on unwind/Drop: R2-RF-1 above. |
| NBO-1: public late events | Sequential public late calls now reject/count, but the close/send race remains: R2-RF-2 above. |

The amendments do not cure either remaining code issue: one concerns confirmation lifetime, and the other concerns cross-thread trigger ownership.

## Lane and mutation evidence

The b753854 lane reports all 14 check rows successful. Its test comparison shows components **43 → 74**, platform **329 → 331**, with zero failures on both sides and no differing failure names. The additional D2a control exercises mismatch detail without changing the existing verdict vocabulary. Recorded Clippy uses warning-denied all-targets checks for components/platform; rustfmt covers the new and base-clean edited files; the workspace all-targets check passes.

The fixture is obtained from each build's compiler-artifact record, under the existing test-fixture launch seam. The package adds the authorized normal platform edge and test-only fixture feature, with no new external dependency or mint-census call. The live source check and recorded edge/feature/environment audits support the scoped restrictions: no production environment lookup, no new `let _ =`, and no unauthorized effect owner. Existing test-fixture argv/path/temp-directory helpers remain fixture-only.

The archived lane also records focused supervisor tests, environment checks, operability, no hit in the 19-file discovery census closure and passing verify_design with 175 successors. These are evidence of the submitted lane, not a claim of Linux support, real codec qualification or production wiring. The unit remains provider-only and library-only; D3a-2/3, D3b and D5 retain their stated obligations.

All 18 final mutations are recorded caught, including the seven round-2 mutations. The attempt history's uncaught second-settlement mutation is reasonably retired: successful settlement takes self.child, and a second settle cannot construct another Settlement even without the state guard. The guard remains defence in depth; take_settlement remains one-shot. That reasoning does not address the handle race in R2-RF-2. Likewise, the caught confirm-after-reap mutation covers the ordinary loop and does not establish the unwind path in R2-RF-1.

## Non-blocking observation

### D3A1-R2-NBO-1: Carry the health-refusal provenance into the deferred record owner

`crates/components/src/supervisor.rs:1212`

The supervisor now classifies the health nonce mismatch correctly, but its comment says the RF7 refusal is kept as evidence. receive_control consumes that RefusedFrame and emits only LivenessMissed plus the Liveness trigger; ControlSession retains state/sequence/stopping information, not that refusal detail. The observer API has no explicit refused-frame event. This is distinct from the expiry path, but the typed family/detail itself is not handed onward.

Suggested change: When D3a-3 adds the record projection, preserve an explicit reduced host-held discriminator for nonce mismatch versus window expiry and the control-owner refusal family, without retaining nonce/frame/detail text. Clarify the current comment so it does not claim a retained evidence object that the API drops.

