# Independent Grok review: required-delivery-selection v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement. Not fresh consumer B.
**Subject manifest:** `docs/implementation/m1/required-delivery-selection-v1-subject.json`
**Manifest SHA-256:** `62bc0033f1c7817e492fcad2e37202aaec978a199b02f33671db25da047ebc14`
**Members:** 18
**Verdict:** **ACCEPT-DESIGN-UNIT**

Bounded metadata process-output coordination: host `deliver_required` consumes one inert `RenderedResponse` and a caller-supplied `Write`, `write_all` then `flush`, and returns the settled exit only after both succeed. CLI acquires a duplicated stdout `File` (preserving EBADF) and maps handle/write/flush failure to the existing terminal `OUTPUT.SERIALIZATION_FAILED` / exit 4 with no second envelope. Not atomic stdout, not Run commit, not M1/M2 complete, not a blind consumer or release.

## Custody and parents

18/18 selection members match. Frozen implementation subject `docs/implementation/m1/trials/required-delivery-01/subject.json` SHA `33205467…5761` — **195/195**. Adjacent archive matches `archive-pin.json`. Candidates are exactly the subject minus `successor.json` (17). Parents pin-match: rust-provider-workspace-selection-v1 successor `28320aec…e8b2` / 7316 (live) and inventory v10 `6608fabd…8bc9` / 121810 (20 packages). All four map rows match frozen product, candidate product, and inventory v10 (`delivery.rs` already planned). Private copy only; original candidate `run-checks.py` path was not executed.

Owned files: new `crates/host/src/delivery.rs`, `crates/host/src/lib.rs`, `apps/cli/src/bootstrap.rs`, `apps/cli/src/terminal.rs`. Live has no `delivery.rs`. `Cargo.lock`, host `outcomes.rs`/`request.rs`, CLI `arguments.rs`/`main.rs`, and identity sources equal live. Candidate has **no** LogicalPath/ArrayOrder `descriptors.rs`.

Inventory `delivery.rs` still describes later atomic artifact/Run/browser duties; this unit implements only metadata write/flush.

## Wiring and semantics

`deliver_required(response, output: impl Write) -> io::Result<u8>` takes the response by value (no retry of the same object) and does not discover stdout, project, store, provider, assets, or network. `write_all` retries `Interrupted`, treats `Ok(0)` as `WriteZero`, and may leave a prefix visible; flush runs only after all bytes. Empty payloads still require a successful flush. Failure is `io::Result`, not evidence or commit authority.

CLI `terminal::stdout()` duplicates the real stdout fd into `File` so EBADF/EPIPE are not swallowed by the Stdout wrapper. Acquisition failure and delivery failure share the existing stderr diagnostic; stderr never receives a replacement envelope. Projection/`delivery_failure` remain host-owned. Human/JSON/completion bytes are produced before delivery and are not rewritten here.

Four host tests cover: short writes + first-write `Interrupted` with settled exits 0/2/4; every prefix cut `0..len-1` with no flush and no retry; `WriteZero`; flush failure after full output; empty-output flush. Existing CLI read-only-stdout tests still pass.

## Reproduction (private copy, Cargo/rustc 1.95)

| Check | Result |
| --- | --- |
| `cargo test --locked --offline --workspace --all-targets` | **34/34** (30 prior + 4 new delivery groups) |
| `cargo clippy ... --workspace --all-targets -- -D warnings` | pass |
| `cargo fmt --all --check` | pass |
| `Cargo.lock` | unchanged |
| Real CLI `version --format=json` / `help` / `completion bash` | exit 0; payloads contain success termination; no failure text |
| Real CLI readonly stdout (json and human) | exit 4; exact `OUTPUT.SERIALIZATION_FAILED` stderr; no second envelope |
| Real CLI broken-pipe stdout | exit 4; same stderr; no envelope on stderr |

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

## Limits

- Metadata process-output write/flush only. Not atomic artifact publication, Run association, browser launch, or durability/rollback.
- Public `Write` port is caller-supplied; host does not bind or authenticate the handle.
- Prefix-visible failure is documented, not hidden.
- Inventory description of `delivery.rs` remains the later full service; this unit is a bounded slice.
- Candidate does not include LogicalPath/ArrayOrder. Not M1/M2 complete, not fresh consumer B, not release/sandbox.
