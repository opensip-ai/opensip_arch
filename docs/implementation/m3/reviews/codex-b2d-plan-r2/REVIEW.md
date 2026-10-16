# B2-d plan r2 review

**Verdict: REQUIRED-FINDINGS.** Two required corrections remain.

Subject manifest SHA-256: `b8bff033a7092de1669b0557dcea2cbb6cd20cf60ceec8ee554f330be0706f20`.

The manifest and both pinned files match their recorded hashes and byte counts. Live product HEAD is `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609` with clean status; architecture HEAD is `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`. This is a plan review, not implementation acceptance.

## Required findings

### B2DPLAN-R2-RF-1: Keep recognition payload bounds under an explicit override

Location: PLAN-r2.md:149-153 and 180-183.

Section 3 exempts recognition from the entry-point bound under an explicit override, while section 4 retains recognized results as disclosure. A unit with 65537 Next.js routes and explicit discovery.entryPoints: [] therefore retains an effects.entryPoints array with 65537 items. The configuration array is within its own maxItems, but the retained recognition violates FrameworkRecognitionResultV1.effects.entryPoints.maxItems=65536. The declared validation of every FrameworkRecognitionV1/UnitRecognitionV1 output cannot succeed. Explicit precedence does not waive bounds on retained recognition payloads.

Required change: Apply the bounded, non-truncating recognition disclosure policy even when an explicit override supplies the effective entry set. Keep effective entryPoints state/source all/explicit and the exact explicit list; distinguish those from suppressed discovered effects and their overflow disclosure. Add explicit-empty and explicit-nonempty controls with over-bound recognized entries, including an individual result over 65536 and the distinct union overflowing across results, and require schema-valid output.

### B2DPLAN-R2-RF-2: Represent actual resolver absence as no winning leaf

Location: PLAN-r2.md:13 and 180-185.

The rule says only a Defaulted leaf is absent. At the pinned product base, configuration.rs defaults_document (lines 927-980) emits analysis/components/policy only, with no discovery.entryPoints. resolve constructs provenance solely from winners (lines 596-599), so a configuration with no entryPoints carrier has neither that semantic field nor a discovery.entryPoints provenance entry. It does not have a Defaulted leaf. The proposed exhaustive distinction omits the ordinary automatic-mode input and risks requiring a fabricated default, contrary to the empty-fold and unchanged-digest requirements.

Required change: Specify no resolved entryPoints field/no winning provenance leaf as the current automatic-mode case. Preserve Carrier provenance as explicit even for []; define any Defaulted branch only if such an input is actually supported. Run the planned absent/empty/higher-empty controls using actual configuration::resolve outputs, and keep the absent configuration and digest unchanged.

## Round-1 disposition

| Prior finding | Assessment |
| --- | --- |
| RF-1, state rule | Resolved for automatic recognition: the fifth reference change and no-known-entry/mixed vectors now cover FR-1. Explicit precedence remains separate. |
| RF-2, unit bound | Distinct-union and all-or-nothing handling fix the automatic case. The explicit exemption remains blocked by R2-RF-1. |
| RF-3, explicit empty | Carrier provenance, explicit empty sets and higher-empty replacement are correct. Actual absence remains unspecified by the stated rule: R2-RF-2. |
| RF-4, YAML grammar | Resolved at plan level by dash separation, conservative colon/tab restrictions, quoted alternatives and non-scalar exclusions. |
| RF-5, TOML profile | Resolved at plan level by mirrored byte/node limits, labelled recursion divergence, one parse-error disposition and deep/wide boundary controls. |
| RF-6, recommendation paths | Resolved by project projection, retained unit/recognizer identity, collision controls and resolver checks after mapping. |

## Requested checks for new issues

The broad automatic-mode `partial` rule is acceptable here. NE FR-1 requires `partial` for a config requiring evaluation without restricting that requirement to configs that infer entry points. The accepted B-S9 model already uses any result's unresolved choices to downgrade known entries. Extending that conservative treatment to the no-known-entry case does not introduce a new completeness claim. A vitest/jest config therefore need not be carved out for this plan; finer field-specific completeness would require a separately settled contract.

`None` for an unparseable Cargo workspace fact is consistent with the pinned B2-c instrument. discovery.rs:527 selects enclosing workspaces only for `Some(true)`, and lines 594 onward select `cargo-workspace` only for `Some(true)`, otherwise `cargo-package`. The plan preserves the separate parse-failure disclosure; treating the unknown fact as not a workspace for instrument classification does not establish that parsing succeeded.

The recommendation-only project path join leaves the unaccepted FR-6 through FR-8 proposals untouched. The declared-input interpretation and internal recommendation type remain acceptable as settled in round 1.

## Review boundaries

Read-only inspection and hashing only. No product build, test, generator, census or network access was performed. No installation, private fixture, signing key, T2 store or overlay was accessed. Neither repository was edited. Only this REVIEW.md and the accompanying review.json were written.
