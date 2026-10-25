# PCS2 owner delegation statement r2 (lead revision; CB5 of the configuration unit)

Capability route: R3-FRONTIER
Codex: gpt-6-astra / high
Claude: claude-opus-5-5 / high
Claude long-horizon lead: claude-opus-5-5 / high
longHorizonLead: true; the Claude lead owns this decision through binding.
Escalate when: review finds the delegation inconsistent with an accepted contract in a way the lead decision cannot settle; stop for the owner.
Escalation route: R4-EXCEPTIONAL only with owner authorization; not selected.
Independent review: Codex gpt-6-astra/high for this revision (the lead wrote it). r1 (Codex draft) had Claude review cb5-review/output/review.json.
De-escalate when: the statement is accepted and only mechanical binding remains.
Exceptional authorization: none.

Revises the Codex draft
`/private/tmp/opensip-implementation/continuation-authority-refresh-2026-10-22/r3-configuration-pcs2-owner-statement-r1/PROPOSED-OWNER-STATEMENT.md`
(sha256 23557292…c21a) after the Claude review (`cb5-review/output/review.json`,
REQUIRED-CHANGES F1-F6). Subject code: branch `claude/config-s4-on-main`, commit
7a85025 on main e39cee8.

## Lead decision (2026-10-25), under the owner's standing autonomy direction

**Selected:** the delegation reading below, for PCS2 only. **Rejected for now:** the
owner-string migration. **Reason:** migrating `semanticValidatorOwner` for PCS2
changes `tools/contracts/options.json` and `schemas/source-map.json`, hence
`tools/contracts/generator-closure.json`, whose hash is bound into the discovery and
snapshot-ledger census held-out receipts
(`crates/security/src/custody/discovery_census_held_out.json`,
`crates/security/src/snapshot_ledger_census_held_out.json`). The migration would
therefore force a held-out blind receipt refresh with no change in behaviour. The
migration is **scheduled**, not abandoned: it rides with the next planned
generator-closure change, when those receipts are refreshed anyway. The owner may
reverse this decision.

**Contrary evidence, recorded (F1).** The accepted wording leans toward the physical
reading: the contract says the owner "identifies handwritten exact admission"
(`implementation-boundaries-and-build-plan.md:768`); M3-B law names
`crates/host/src/configuration.rs` "as validator"; inventory239 says "semantic
admission belongs to crates/host/src/configuration.rs"; and the policy-document rows
name `crates/evaluator/src/policy.rs`, where that admission body lives. Under this
decision the one field `semanticValidatorOwner` carries two meanings across the
registry until the scheduled migration: the physical admission body (as for
policy.rs and the other rows) and, for PCS2 alone, the accountable host owner. This
succeeds B-S10's PCS2 ownership aspect.

## Normative text

1. For `urn:opensip:product-configuration:2` (declaredMajor 2, profile
   `opensip-exact-schema-reference-1`) the `semanticValidatorOwner`
   `crates/host/src/configuration.rs` designates the accountable host owner that
   integrates configuration semantics into the invocation and projects the owning
   refusal. For PCS2 only, it does not require the pure algorithm body to live in
   that file. Every other row keeps the physical meaning.
2. The host owner delegates the existing B1-a pure configuration algorithm and X12
   policy-pack admission to `crates/evaluator/src/configuration.rs`, with its
   generated table `crates/evaluator/src/configuration_tables.rs` and private
   controls `crates/evaluator/src/configuration_private_controls.rs`. The host
   facade keeps the exact typed interface and must not duplicate, weaken or replace
   the lower algorithm. No new resolver semantics, schema version, defaults,
   profile, refusal row or admission order is selected.
3. **The embedded schema factory (F2).** The host's share of X12 item 7, the fixed
   52-source embedded schema registry ("host-owned exact raw schema sources" at
   e39cee8), is delegated to `crates/evaluator/src/configuration_schema_sources.rs`
   so that the lower resolver can use it. Its source population and order still
   equal storage's; it performs no I/O or path lookup; it mints no authority. The
   accountable owner stays `crates/host/src/schema_sources.rs`, now a re-export
   facade whose tests and the macOS admission test still compare the population.
4. **Invocation mode and visibility (F3).** `InvocationModeV1`, which B1-b unified in
   host, is now defined in the evaluator as copyable data and re-exported by host.
   The B1-b computation in `crates/host/src/invocation_mode.rs` remains its only
   production producer. The resolver carriers (`ResolverInputV1`,
   `CompiledDefaultsV1`, `ResolvedConfigurationV1` with its public
   `resolved_config_digest`, and the rest) become `pub` in opensip-evaluator, which
   security and storage depend on. Two kinds of construction are distinguished
   (Codex review of r2, required change 1):
   - *Authority-producing input assembly* stays with its owners: native
     `InvocationModeV1` observation in `crates/host/src/invocation_mode.rs`, and
     authenticated invocation-input assembly by its host/native producers.
   - *Pure resolver output* is constructed by the delegated resolver in
     `crates/evaluator/src/configuration.rs`, the one permitted producer of
     `ResolvedConfigurationV1` (with its computed digest) and of the resolver's
     intermediate and provenance data.
   Any value of these types is data and carries no admitted invocation authority.
   The CB6 check is the absence of production callers or producers that bypass those
   owners, or that treat freely constructed values as admitted invocation authority.
5. `crates/host/src/configuration_projection.rs` keeps the host's public refusal
   projection. The facade and host module joins keep resolver and projection
   reachable by the intended host consumers (doctor_ingress, outcomes,
   recommendation, snapshot_seal). A re-export is not evidence of a production
   analysis caller; none exists yet.
6. Ordinary and prepaid ledgers, all four starts, authenticated defaults, flags and
   mode, capture, lending, recheck, failure and cleanup ownership stay with their
   original owners. The X12 pure-admission no-ledger exemption is not extended to
   resolver allocation, repeated registry construction or native production. K7 stays
   owed.
7. PCS2 schema bytes stay sha256
   `591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d`; options
   `/sourceMappings/9`, registry `/sources/34` and source-map `/sources/42` keep their
   tuples. This statement mutates no map, schema or registration.
8. **Other owners (F4).** `configuration-disclosure:1` and `detector-manifest:1` keep
   their separate owner strings and obligations; neither is delegated. For
   `urn:opensip:preview-configuration:1` (admission-registry `/sources/15`,
   admission-source-map `/sources/51`, sha256 ada9e4a9…), the schema-one in-memory
   projection (B1-a item 11, PREVIEW_ID) now lives in the evaluator: it is covered by
   paragraph 2's delegation, and its inventory description is restated by CB6.
9. **What CB6 must describe (F5).** The successor inventory and descriptions cover:
   the host facade and projection; the evaluator resolver, table, private controls
   and schema sources; the deleted host table; the private-base fixture
   `crates/evaluator/tests/fixtures/configuration-private-base.json`; the relocated
   private-control tests and the changed host tests; `configuration_classes.json`
   (host-owned, now generator input for an evaluator table); `rustfmt.toml` (new
   pinned generator input, 150 bytes, sha256 0bb1629a…); the config-pinning
   generator and its updated control; the `exceptions.json` rows; the inventory239
   PCS2 schema description; the preview-configuration description; and the 11 COV
   owner rows that name `crates/host/src/configuration.rs`, which stay with host
   under paragraph 1.
10. **Review route (F6).** r1's own header asked for different-vendor R3/high review;
    its review ran at R2-DEEP/medium (Claude). The lead accepts that review as
    satisfying CB5 for r1's facts, because it found no factual error and its
    findings are all incorporated here; this r2 text gets its own Codex R3/high
    review.

No execution, owner-string change, new price, native feasibility, unit acceptance
or project qualification is claimed.
