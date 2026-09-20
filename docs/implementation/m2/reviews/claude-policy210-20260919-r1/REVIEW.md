# Independent review — frozen `operational-policy-checkpoint-210`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 210 product bytes — the existing security-owned operational-file descriptor policy exposed as a workspace mechanism with typed diagnostic causes, and `storage::CapturedMarker` delegating to it on its **retained** `File` (my 205 N-1). Supplied uid/groups remain caller assertions; no parent-chain custody, lease, host grant, admission or public wire code is claimed. The owner ran no exact-210 host lane (128 qualifies 208 only) and says so. No cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `add6aac991f5cb3d845ac38ef8d920cebb55ea50d8cd67fb070d1c8cb30d48bf`, 4,101,596 B = request = `archive-pin.json` |
| Members | 389, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355, none unpinned |
| Parent | equals **my own verified 208 extraction**; three changed: `security/lib.rs`, `security/custody.rs`, `storage/store_root.rs`; none added/removed |

## 2. Owner checks re-run (fresh scratch, offline, locked)
security 167/167, storage 92/92, strict workspace Clippy clean.

## 3. What changed (diffs read in full)
- `custody.rs`: three visibility changes only — `pub enum Refusal`, `pub enum NativeRefusal`, `pub fn inspect_operational_file` — plus the existing replacement regression now calling the public facade. **No predicate token changed.** `Refusal::code()` stays private, so the wire-style strings (`HARD_LINKED`, `UNLINKED`, …) are not exported; the module itself stays private (`mod custody;`).
- `lib.rs`: `pub use custody::inspect_operational_file as inspect_operational_file_policy` and the two enums re-exported as `OperationalFilePolicyFailure` / `CustodyPredicateFailure`, with doc comments that say what is *not* established (actor context, pathname, ancestors, filesystem, lease; "success is neither lasting exclusion nor admission of previously captured bytes").
- `store_root.rs`: `CapturedMarker::inspect_file_policy(uid, groups)` — a one-call delegation on `&self.file`; private; one new macOS test.
- **API shape:** the public function takes `(&File, uid, &groups)` and nothing else — no `Scope`, no `waive_owner`. A caller *cannot* ask for an owner waiver or the configuration 4 MiB cap; the operational scope is fixed inside. No duplicated predicate exists in storage (grep: the only policy logic outside `custody.rs` is the delegation).

## 4. Same-descriptor and cause preservation — checked by mutation (7 mutants, `io/mutation210.json`, `mutation210b.json`)
| Mutant | Result |
|---|---|
| `observe_marker` keeps a by-name **reopened** descriptor (my 205 survivor, re-applied) | killed |
| storage takes the uid **from the file being checked** (self-certification) | killed (`ForeignOwner` for uid+1 no longer refuses) |
| storage ignores the supplied groups | first attempt **did not compile (my lifetime error — not counted)**; corrected mutant killed |
| storage widens the supplied groups with the file's own gid | killed (`GroupWrite` expected) |
| public policy function evaluated in `ConfigurationFile` scope | killed (sparse >4 MiB test + replacement test) |
| public policy function swallows predicate refusals | killed |

The new storage test is the cross-crate form of the 205 custody test: capture → policy Ok → `ForeignOwner` for another uid → original renamed and made `0o602` (`OthersWrite`), `0o620` (`GroupWrite`; Ok once the owning gid is supplied), hard-linked (`HardLinked`), unlinked (`Unlinked`) — all while a clean replacement sits at the marker name and is itself admissible. Each refusal arrives as the typed `Predicate(cause)`, distinct from `Observation(_)`; nothing is collapsed to a boolean. **205 N-1 closed**: a storage-side caller can now join bytes and policy on the same object.

## 5. Findings
No defect. Notes for the first caller:
- **N-1 (design, low)** the join is *available*, not *forced*: `observe_marker` still returns `Present(CapturedMarker)` whether or not policy was sampled, and nothing in the type distinguishes a checked capture from an unchecked one. In 205 I suggested a single security-side "observe + policy" entry so a caller cannot forget; root chose delegation, which keeps uid/group provenance handling in security and is fine. Before an admitting caller exists, make forgetting unrepresentable on the storage side instead — e.g. admission consumes only a `PolicySampledMarker` that `inspect_file_policy` returns by value. Not a 210 defect (no caller).
- **N-2** `CustodyPredicateFailure` exports every variant of the shared enum, including ones the operational scope can never produce (`TooLarge`, `NotDirectory`, `Absent`). The doc comment says so. A future exhaustive `match` in a consumer will have dead arms; acceptable for a workspace-internal diagnostic type, worth revisiting if it ever nears a public projection (my 200 N-1 on `UNLINKED` still applies).
- **N-3** the policy is a *sample*: the test itself shows the same descriptor going Ok → refused → Ok as the file changes. The doc comment states this; any admitting caller needs the sample inside the held lease/exclusion window, which remains owed.
- **N-4** the fixture takes the uid from the file for convenience and says "Test fixture's uid only: production provenance must be the actor" — and the self-certification mutant proves the production path does not do that.

## 6. Limits
macOS, unprivileged; scratch copies only (`build210-*`, `target210-*`, created after asserting absence), restored from frozen bytes; nothing deleted; build targets excluded from `hashes.txt`. No host-isolation run by me or the owner for these bytes. ACL-bearing files and Linux were not exercised (unchanged, still declared unsupported/owed).

## 7. Verdict (bounded)
**210 exposes the existing S7 operational-file predicate without changing it, with an API that cannot express a waiver or the configuration cap, keeps the wire-style codes private, and lets storage apply the policy to the very descriptor that supplied the marker bytes; six behavioural mutants — including self-certified uid, ignored or widened groups, wrong scope and a reopened descriptor — are all killed, and typed causes are preserved end to end. 205 N-1 is closed.** No approval of actor provenance, custody chain, leases, admission, installation or cumulative readiness.
