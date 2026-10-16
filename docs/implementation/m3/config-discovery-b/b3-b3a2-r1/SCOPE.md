# B3-b3a2 r1: the pre-run gate, the blind mode over the D15 terms (M3-B unit B3-b, sub-unit B3-b3a2)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1. Nothing held out has been opened.**

It implements B3-b3a2 of the B3-b plan r2 as amendment A5 states it (`../b3-b/PLAN-r2-A5.md`, A5-2; Codex `codex-b3b-plan-a5-r1`, ACCEPT):
- the blind mode is extended to the new terms over held-out entries, margins only, with B2-b4c's output allowlist unchanged;
- the receipt's binding covers the extended closure;
- the synthetic confidentiality and lifecycle controls are extended to the new terms;
- Codex accepts these exact bytes before any held-out store is opened (§4.3).

It also carries B3-b3b's run plan (`RUN-PLAN.md`) and run script (`evidence/run_b3b3b_blind.py`), so this one gate covers both the tool and the run. That follows the B2-b4c3 precedent (`codex-b2b4c3-prerun`).

**Base:**
- product main `2dd54ba`: B3-b3a1 bound, inventory v208, 170 contract successors;
- architecture `abbf48fb0`.

**No product source changes and no Rust changes.** The unit changes the census tool, the member model's docstring, the vectors' member-model pin and the blind controls.

## What it delivers

### The blind row is the full ledger's

- **`blind_measure(c, dm, rule, population)`** is new. It is the blind mode's measure over one held-out tree, and returns three things:
  - the walker model;
  - the reference population;
  - the tree's D15 terms.

  The terms are computed by `repository_terms`, the same function the lead-readable rows now use. So a held-out row and a lead-readable row are computed by one path: W at the tree's root, every source at its envelope, and the tree admitting no member.
- **`blind_row`** takes the terms. Its margins and `passes2x` are the full ledger's: `full_ledger(m, terms, limits)`, the walker plus the reader, member and descent terms. The byte margin is taken at R = 4,096, as before.
  - The verdict is checked against the margins before the row is emitted.
  - Every failure in the terms is reduced to `MODEL`, as is a held-out tree that admits a member (`repository_terms`'s `require`). That includes a raise, an exit, or a disagreement between verdict and margins.
- **Carrier text stays in memory.** `verified_tree` keeps the carriers' text for the terms' parse, as for the lead-readable rows. Nothing of it is emitted: the row still holds only integers and booleans, and every exception is still discarded unprinted.

### The receipt

- **The format is unchanged** (LD-B3B3A2-1): the same top-level keys, the same measured-row and error-row keys, and the same error classes. `marginPermille` and `passes2x` now mean the full ledger's, and the receipt's `standing` says so. `validated_receipt`, `compose_held_out` and the Rust `blind_result` are untouched.
- **The bindings** gain `memberModel`, the pin of `tools/security/discovery_member_model.py`.
  - The tool's own pin was already bound, and the closure already holds the four D15 files (B3-b3a1). So a change to the census tool, the member model or any closure file makes a receipt stale.
  - The committed B2-b4c receipt is walker-only. Its bindings differ (tool, closure, member model), so it stays `outstanding: held-out (blind receipt stale)` until B3-b3b replaces it.

### The member model's docstring (B3-b3a1 NBO-1)

`read_envelope`'s docstring no longer claims every D15 read is opened no-follow:
- the carriers, the provider manifests, and item 6b's member and global sources are opened no-follow, as custody requires;
- item 6b's refusal-only system sources are opened by fixed path, following symbolic links (`open_fixed_regular_following`), and the file reached must still be regular.

The envelope itself (LD-B3B3A1-2) is unchanged. The model's bytes change, so the vectors' `memberModel` pin is regenerated. Nothing else in either record changes.

## The controls

`tools/tests/test_discovery_census_blind.py` keeps all 19 earlier controls, adapted to the measure's new shape: the fakes return the walker and zero terms. It adds six, and extends one:
- **`test_the_real_terms_over_canary_carriers_emit_only_the_full_ledger_margins`.** Each held-out tree's carrier now names the canary:
  - `held-a` has a `.cargo/config.toml` patching a crate named by the canary to a path named by it;
  - `held-b` has a `package.json` whose workspaces name the canary as a glob and as a path.

  The real walker model and the real D15 terms run over both trees. The rule is a synthetic one: nothing is pruned, and the reference's markers. The control checks:
  - nothing of the canary or the scratch path reaches the receipt, stdout or stderr;
  - the carrier was read (the reader term's edges are non-zero);
  - each row's margins equal the full ledger computed independently;
  - the walker alone has a wider edge margin.
- **`test_malformed_canary_carriers_are_measured_or_reduced_to_their_class`.** These carriers each name the canary:
  - a JSON error;
  - a TOML error;
  - non-UTF-8 bytes;
  - an oversize carrier (over the 4 MiB cap).

  Each reaches the real terms, is measured, and emits nothing.
- **`test_a_d15_failure_is_a_model_error`.** The terms raising, with the canary in the exception, and a held-out tree admitting a member are each `MODEL`, silently.
- **`test_the_margins_are_the_full_ledger`.**
  - A walker at an eighth of each limit, plus terms at another eighth, gives 4,000‰, not 8,000‰.
  - A walker that holds alone, plus terms over half the edge limit, measures and fails.
- **The lifecycle** gains two controls:
  - `test_a_full_ledger_failure_returns_the_caps`: the walker holds, the full ledger fails, `heldOutMargin` is `fails (blind census)` and the caps are `returned-to-law`;
  - `test_a_full_ledger_pass_holds`.
- **`test_drift_in_each_binding_makes_the_receipt_stale`** gains the member model.

## Lead decisions

- **LD-B3B3A2-1. The receipt's format is B2-b4c's, unchanged; its margins and verdict are the full ledger's.** A5-2 says "margins only, with B2-b4c's output allowlist unchanged". So no key is added. The full ledger is the walker plus non-negative terms, so its margins are at most the walker's in each dimension, and a full-ledger pass implies a walker pass. The single verdict is therefore the conjunction the lead-readable rows apply (`failing` counts a walker or a full-ledger failure).

  **Rejected:**
  - a new `fullLedgerMarginPermille` key beside the walker's margins. It widens the allowlist A5 keeps, and emits more per held-out entry than the verdict needs.
  - a schema version bump. The committed walker-only receipt would then refuse as malformed, and every ordinary `--check` on main would fail until B3-b3b. Under the current version it is stale, which is what it is.
- **LD-B3B3A2-2. One computation path.** `repository_terms` computes the terms for both the lead-readable rows and the blind rows. The lane's blind equivalence runs the blind mode's own `blind_measure` and `blind_row` over every lead-readable store. To let the blind join apply, it presents each entry to `blind_row` as held out. The lane asserts that each row equals that entry's full-ledger margins and verdict in the census record. The rows are the manifest's lead-readable ones, so no held-out store is opened.
- **LD-B3B3A2-3. A synthetic rule in the controls.** The Python controls are hermetic: no architecture checkout, so no reference rule. The real-terms controls use a stub rule (no pruned tree, and the reference's four workspace markers). Their subject is confidentiality and wiring, not the rule. The reference rule's fidelity is covered by the census `--check` and by B3-b3a1's measured-against-model control, both of which use the real rule.

## Checks

Lane r1, `evidence/b3b3a2-checks-r1/`. Attempt 1 (`b3b3a2-checks-r1-attempt1/`) failed only on the runner's own equality-projection allowlist. It matched the bare key `/memberModel`, which was right in B3-b3a1, where the key was new. Here the changed paths are `/memberModel/bytes` and `/memberModel/sha256`, so the allowlist now names them. Every other row of attempt 1 passed, and its three mutations were caught. The second attempt is the lane of record:
- **the security suite** at base and candidate, with equal failure sets and no new test (no Rust change; the vectors' pin changes);
- **the equality projection:** the census record is unchanged, and the vectors change only in `/memberModel`;
- **no Rust file edited;**
- **the measured-against-model control,** and every census, discovery, workspace and Git-tracking test;
- **the census vector check;**
- **the controls:** FW-01, walk storage, and the census tool's and blind receipt's controls (25);
- **the census `--check`** over the T2 cache: lead-readable stores only;
- **the blind equivalence** (LD-B3B3A2-2), over every lead-readable store;
- **environment, operability and verify_design;**
- **three mutations of the blind mode,** each of which must fail the blind controls:
  - `blind-terms-ignored`: the margins taken over zero terms;
  - `receipt-member-model-unbound`;
  - `member-admission-unchecked`: `repository_terms`'s `require` removed.

## The run (B3-b3b), after this gate is accepted

See `RUN-PLAN.md`. The run script pins the tool's and the member model's bytes to this candidate's. It runs only after this unit's code commit and lock are on main.

## Not claimed

- **No held-out store has been opened.**
- No receipt, and no held-out margin.
- No workspace margin (B3-b3c).
- No product code change.
- No qualification.

## Inventory

No new paths. No inventory successor.
