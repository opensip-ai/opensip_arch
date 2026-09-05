# Security behavior fixture package, version 2

PROPOSED design evidence. Author: Codex security fixture sub-agent. No register edit and no qualification claim. Run with the pinned review environment:

```
/tmp/opensip-architecture-review-env/bin/python docs/coop/completion/security-behavior-check.v2.py --report /tmp/security-behavior-independent-report.json
```

The authoring script retains structured inputs and independently stated expected projections. The checker imports a separately written reference model; it never reads expectations to decide model behavior. Every actual result is retained in the report, including complete journal segments and report/authorization validation results. Golden projections plus whole-result hashes in the report support independent inspection; the checker does not claim that a projected assertion checks unspecified members.

Coverage includes all 343 CORE/INDEX/COMPONENT continuation combinations; before-write/after-write/after-sync crash prefixes for L-1 through L-8 across the two OS design axes; concrete revocation, expiry, cleanup-death and duplicate-revocation schedules; all 25 pairs of doctor check statuses; full doctor report objects; full 19-member host authorization records and their 15-member consent scopes; deletion and corruption mutations; 90/365-day expiry, 24-hour future tolerance, 2-of-3 and 3-of-5 threshold observations, and 30-day/one-renewal waiver boundaries. Model clock perturbations never enter the journal ordering rules.

Five local executions observe the constructed child environment and ambient read/write/exec/loopback network behavior. Their evidence is local only, and ambient probes intentionally succeed while the corresponding modeled grant is denied. They demonstrate the absence of a broker-mediated barrier; they are not confinement tests. The actual executable under test is a probe, not OpenSIP. Windows and in-host component execution remain excluded.

The host authorization acceptance context is synthetic and explicitly marked `SYNTHETIC-RECORDED-CONTEXT-NOT-ADOPTION`. Fixture context authorizes a model branch for inspection; it does not assert that any design or product admission is recorded. Full host records contain recorded contract hashes and synthetic admission references; no invented admission hash is presented as a real accepted artifact. The final SATISFIED package must bind the accepted successor as its real product admission source. Capture hex inputs for post-report byte counts are authored transcript fixtures, not OS network captures.

## Integration decisions still required

1. Adopt the security successor's monotonic *evaluated* time high-water repair before relying on `MONOTONIC-TIME`. Whole-set restore cases assume a restore is detected or the independent anchor fails validation; they do not assert that matching rolled-back local files can detect themselves. The final witness/restore design must provide that observation before these cases can be application-grade.
2. Adopt the doctor FC-REDACT successor replacing the impossible prohibition on every one-character secret prefix/suffix with classified-secret noninterference, full-secret absence, and no secret-derived preview/hash. The checker changes the classified secret and project path and requires bit-identical output; high-entropy unclassified diagnostics deliberately survive tier-2 scrubbing.
3. `FC-JOIN-BLK-STILL-ROUTED` is an obsolete-condition assertion when the scoped security successor records BLK-1 through BLK-4 dispositions. Retain the historical class as `SUPERSEDED-CONDITION`, citing that successor, instead of fabricating a passing assertion that blockers remain routed after they are disposed. Every surviving rule (CA2 denied, CA1 in-process denied, keychain deferred, permissionRef unpopulated, host/component actor split) has independent input cases here.
4. FX-10 is conditional in-host-mode coverage. The child-process-only decision makes its current execution `REENTRY-REQUIRED`; the fixture explicitly refuses execution rather than pretending an in-host test ran. Repair, replay, keychain and third-party cases likewise carry typed absences. Their existence never authorizes re-entry.
5. The lead adopted these proposed bounds under delegated D-367 authority for final integrated recording: general strings 4096 UTF-8 bytes; each collection 4096 entries; whole report 16 MiB UTF-8; container depth 32; IDs/labels 128 bytes; accepted v25 source identity strings 512 bytes; diagnostics 1024 bytes. The fixed preview catalog fits comfortably. G12 (doctor), G32 (actor reports), and G20 when SDK projection consumes the same envelope execute the boundary corpus; G22 is not assigned by analogy. Four-platform memory/latency measurements can falsify the cap choice; cap overflow or lost mandatory members is OC5, never healthy omission. ASCII/non-ASCII equal/+1, source-identity, collection/depth, and independent total-byte boundary cases are authored here. Limits are checked on UTF-8, not character count. The compact reference serializer is used for exact model output-byte accounting; production readers must also cap incoming raw bytes before parsing. This delegated adoption awaits the final integrated decision record.
6. Execution still owes actual OpenSIP adapters, four supported platform runs, process-tree supervision, complete report OS traces, SQLite crash/power-loss durability, authorization/context custody, crypto verification and OS trust evidence at the named gates. The local model does not prove these. Security vector crypto evidence is a separate unit; this package consumes trusted/authorized signature observations as inputs and does not forge cryptographic evidence from booleans.

## Model boundaries reviewers should inspect

The journal model uses an explicit serialized writer schedule. It is not a scheduler, filesystem durability implementation, or grant-journal SQL implementation. Input clock and transport-delay annotations are adversarial inert data; they must not change decisions. The fixture matrix cannot establish an unimplemented single-writer lock protocol. Inverse calls are modeled identities, not actual restoration of product files; production qualification must run real declared inverses and exercise detectable inverse failure.

Doctor degraded cases retain raw source bytes and independent before/after observations. The reference observer records zero writes, locks, executions and network actions; executing the real doctor under an observation harness is still required. The JSON Schema intentionally allows additive members on doctor reader positions. The separate host-record validator checks v25's closed authorization and scope envelopes, field-preserving projection, subtype domains, policy carrier, byte counts, deadlines, and known-context reference equality.

`FC-REPLAY-NAMED` and `FC-REPAIR-NAMED` are non-executable stage dispositions. Their compact typed-absence representation is a fixture descriptor; it is not a new wire refusal or a substitute for G08's existing `CONTINUE-REPLAY-NOT-DESIGNED` vocabulary. No D9/exit number, RunId recipe, proof of global rollback detection, production crypto success, or completion status is minted by this package.

## Turn-2 repair evidence

SBR-1: inverse application attempts now distinguish repeated idempotent recovery from the logical restored set. Completed RCO retains its inverse until CLN. A death after inverse application but before CLN sync replays the inverse and preserves completed outcome history.

SBR-2: all 260 original crash-prefix cases carry an independently authored exact durable prefix and complete post-recovery result. The checker compares every member, not only retryCount. Every clock/delay pairing compares complete normalized outputs.

SBR-3: OC4 is an empty-check pre-check refusal; independently supplied execution events determine refusal and report-integrity failures. Forged OC4/5 labels fail. Output/construction failure has a no-report OC5 execution result. Readers without event custody explicitly report the limit of structural OC4/5 verification.

SBR-4/SBR-6: schema and semantic validation compose into one accepted/refused path. Complete embedded consent scopes are closed and action-dependent. Missing fields, malformed objects, wrong endpoint domains, nested additions and wrong environment types refuse without exceptions. Doctor extension positions remain additive.

SBR-5: legal resolution derives from the synthetic recorded context, its admitted class/subtype scope, explicit invocation consent, exact attempt/binding comparison and immutable preview exclusions. Coherent CA2/IN_PROCESS forged grants refuse. Valid denied records remain consumable.

The SHOULD advisory is also addressed: a differing consent-record ID has a required explicit authorization-record cross-reference, and evidence/environment/consent optional additions have positive reader cases.

This frozen unit is a behavioral repair review only. The final security v2 normative high-water/restore/journal join remains a separate required integration review, and no application-grade row closure is requested here.
