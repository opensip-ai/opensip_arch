# Independent review — OpenSIP status reconciliation r123

**Verdict: REQUIRED-FINDINGS**

The frozen `subject.json` hashes to `05c5bfa82da6898c995ccbc68db95077c8545e9439ba6d8dd052f1358b176fa5`. All 1,247 declared members are unique ordinary files and match their declared sizes and SHA-256 values.

The underlying status records otherwise reconcile correctly. The first 402 accepted-work entries are preserved by value and the only additions are E403 and E404. Their archived reviews, lead records, member archives, and architecture history support planning-publication standing only. The candidate keeps product head `e39cee850864df377d0a4d54287348b752257874`, inventory 239 with 199 successors, and 187 contract successors unchanged. The execution-at-cutoff records also keep D5, C2b, the C2a3 compiler job, and the finite storage/ABI probe outside accepted work and do not convert queued or live observations into results. Permitted read-only Git ancestry checks confirmed the recorded architecture and product heads and the declared publication commits.

## Required finding

### STATUS-R123-RF-1 — Medium — the mutable front door routes current r123 claims to r122 records

`draft/docs/implementation/m3/IMPLEMENTATION-STATUS.md:3` still summarizes E401–E402 as the current delta even though this candidate's delta is E403–E404. More materially, lines 5, 11, 235, 269, and 275 link the current update protocol, accepted-work ledger, binding ledger, decision register, unit register, and source record under `status/2026-10-21-r122/`. This contradicts `draft/docs/implementation/m3/status/2026-10-22-r123/UPDATE-PROTOCOL.md:15`, which requires the mutable front door to point to the current reviewed revision.

The accepted-work link demonstrates the concrete failure: the front door says that the linked ledger checks 404 records, but its r122 target contains 402 records. A reader following the machine-record links therefore receives the prior board rather than the r123 records that substantiate the page. The factual link check does not detect this because the stale r122 targets exist.

Correct the current-board links to their `status/2026-10-22-r123/` counterparts and update the line 3 delta summary to identify E403/E404 as planning publications with no code, inventory, contract, execution, unit-acceptance, or qualification effect. Keep links that are explicitly labeled historical, such as the r122 owner packet and advisory records, on their historical targets. Recheck the front-door assertions against the linked r123 ledger, register, source, protocol, and unchanged binding/decision records.

## Evidence limitations

- This is a status-only review. It does not re-review accepted code or authority meanings and does not authorize publication, implementation, native execution, owner choices, inventory or contract binding, or qualification.
- No compiler, build, test, formatter, linter, native executable, fixture, control, driver, or process inspection was run. Execution-state conclusions are limited to the frozen time-bounded records.
- Private, store, installation, key, T2, and undeclared data were not accessed.
- M3 and the whole project remain incomplete; all gates outside the two narrow planning-publication scopes remain open according to their owning authorities.
