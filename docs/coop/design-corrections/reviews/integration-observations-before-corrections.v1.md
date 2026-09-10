# Remaining integration issues after interrupted Claude correction passes

Standing: Codex integration observations, **not an acceptance review** of Codex's
own edits. These issues remain open. The scope is the D-371 intended product;
none is deferred by silently shrinking the product to the historical preview.

1. **Execution grant composition (AR-07/08).** Security admits RepoExecutionGrantV2;
   workflows consume a synthetic flattened admission projection and native's
   AuthorizedExecutionV2 is only a preflight over asserted inputs. Define and
   exercise the actual host projection from a schema-valid, security-admitted
   grant to each consumer. Bind project, snapshot, exact argv/runner, class,
   tool closure, platform, effect table, current consent and operational grant
   reference. A caller-supplied `result=ADMIT` cannot be the real admission path.
   Native's multiple owner classes and 4096-owner preparation bound must compose
   with security's per-grant class and 64-owner bound without broadening authority.

2. **Owner-set digest and operational reference (AR-07/09).** Native currently
   projects each owner's file-manifest hash directly as ownerSourceDigest;
   security expects a host-computed owner-set digest and its comment names an H
   domain. Foundation expects a retained raw-hash preimage. Choose one closed
   owner-set record, including snapshot/dependency origin, sorted unique owner
   keys and manifest hashes, hash its canonical bytes with raw SHA-256, and prove
   the same preimage is used in the semantic grant and actual operational grants.
   Update stale native v1 authorization-reference descriptions to the actual v2
   grant or explicitly defined grant-set reference. Keep consent/nonce/expiry out
   of the semantic Plan.

3. **Machine platform identifiers (AR-06/08/13).** Workflow test records still use
   display aliases such as macos-arm64/linux-x86_64, while security/native grant
   admission uses macos-aarch64/linux-x86_64-gnu and the corresponding other two
   platform IDs. Normalize the machine contract and fixtures, preserve display
   aliases only through an explicit mapping, and test actual security-to-test
   admission across the four selected platforms.

4. **Preparation/core lifecycle surface (AR-08/13/14/15).** The seven previously
   placeholder trust/store grammars now have declared candidate syntax in S12 and
   the inventory. The explicit native preparation operation still needs an exact
   command and typed invocation-step contract joined to its grants and import
   result. Core update/repair/rollback selection must join S9's reader-first
   migration, current-core profile binding, floor continuity and lease semantics.
   Avoid inventing a second command inventory or treating generic update labels
   as a complete lifecycle design.

5. **Native/foundation semantic joins (AR-09/12/13).** Exercise native subject
   discriminator output against foundation v4's declaration-signature token
   preimage, and standard-library/Rust-dev-LLVM identities against the exact
   closure2 suffix projection. Verify that manifest digests use the signed metadata
   body preimage, not the signature envelope. Resolve effective scope/workspace
   bounds where native/security allow 4096 units and foundation scope records
   impose tighter bounds. Do not alter frozen foundation v4 without a new subject.

6. **End-to-end import and policy evidence (AR-09/11/12).** Workflow import admission
   now validates the real native payload schemas and all auxiliary records; its
   checker no longer uses invalid synthetic native payload stubs. Add actual
   cross-unit wrapper equality and retained-preimage replay cases, including
   SourceMapping's snapshot identity and source inventory binding. Validate the
   compiled policy/rule-program and policy-derivation links through a complete
   foundation proof/evidence/Run closure. Unit schema success alone is insufficient.

7. **Public security composition (AR-03/05/14).** The composed admit_root_chain
   entry point needs direct positive/negative cases using complete RootV1/V2
   records; the old reduced chain primitive remains fixture-only. Review grant
   shape admission before nested access, root-unit `.` handling for explicit
   workspace joins, and current-core profile binding across a real migration
   sequence. Synthetic signer/OS observations are still explicit TCB assumptions.

8. **Review suppression and clone explanation (AR-13).** Check persistence of a
   reviewed clone/candidate suppression when a new Run retains the same stable
   fingerprint: the current candidate identity includes RunId. Define which
   stable key the suppression follows and verify actual calendar expiry. For
   near-clone connected components, disclose the matched edges and scoring
   semantics rather than implying every member pair passed the threshold.

9. **Independent acceptance and source reconciliation (all ARs).** Preserve the
   substantive foundation CHANGES_REQUIRED review and Codex's dispositions.
   Foundation v4 and the later mixed security/native/workflow changes still need
   independent actual-Claude review of exact frozen bytes. Then run the required
   fresh blind consumer B review (DR-011-R10), reconcile inherited residuals,
   qualify the completeness of the 32 harness/owner mappings, and update the
   current reading path, inventory/classification, source map, decision act and
   central readiness register together. Do not award QUALIFIED/DEMONSTRATED from
   synthetic reference checks, self-review or quota-error responses.

Already corrected during Codex integration: delegated audit analysis gates;
missing required Coverage even with zero findings; same-kind imported-evidence
content changes; unbound E1–E3 re-evaluations; actual prior-detector E0 for detector
removal; invalid or caller-substituted import schemas; retained preimage corruption
before recovery writes; exact postimages before recovery commit; separate immutable
verification links; repeated workspace selection distinct from a single project
authority root. Their checks are retained, but their mixed-author bytes still need
the independent review above.
