# B2-d implementation plan r3 review

**Verdict: ACCEPT.** Both round-2 required findings are resolved at plan level. No new blocking issue found. One nonblocking editorial observation remains.

## Subject verification

Manifest SHA-256: `45440a5090d27db5c462c516f18c08d9522d12b7784566eab14bd64c0a32c0c8`.

The manifest and all three members match their recorded byte counts and SHA-256 values. PLAN-r3.md is 24,822 bytes, SHA-256 `b7e3da8dcb51649e0ba0021b85bb688eae8cd4a82f7542c1277e06c335ddecca`. Live product HEAD is `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609` with clean status; architecture HEAD is `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`.

Reviewed the full r3 plan, its diff from r2, the round-2 findings, and the relevant pinned resolver, recognition schema, NE FR-1 through FR-5 and M3-B item 16 authorities.

## Required-finding disposition

**B2DPLAN-R2-RF-1: resolved.** The r3 changes table and section 3 now apply the distinct-union, all-or-nothing recognition bound regardless of explicit configuration. Overflow removes entry effects from every retained result and preserves the disclosure on each previously entry-bearing result. Explicit configuration changes the effective entry set and state/source, not the validity requirements for retained recognition. Section 4 preserves the exact explicit list, including empty, and gives it `all`/`explicit` precedence. The controls cover individual-result overflow and aggregate overflow across results, with explicit-empty and explicit-nonempty lists, and require schema-valid recognition output. This closes the former route to an effects.entryPoints array exceeding its schema maxItems of 65,536. Section 3's general partial-state wording is read subject to its express override cross-reference and section 4's effective-state rule.

**B2DPLAN-R2-RF-2: resolved.** Section 4 now defines automatic mode as no resolved discovery.entryPoints field and no provenance entry. That matches configuration.rs defaults_document and resolve's winner-derived provenance at the pinned base. There is no invented Defaulted input or fabricated default leaf. Carrier-backed arrays remain explicit even when empty, including higher-empty replacement. Both recognition and recommendation controls use actual configuration::resolve outputs and preserve the absent configuration and digest.

## New-problem assessment

The revisions preserve the earlier accepted distinction between bounded retained discovery disclosure and explicit effective entry points. They do not add a discovery configuration layer or alter the resolver digest. The other round-1 fixes remain present: FR-1 state correction, strict YAML subset, declared TOML resource profile and labelled recursion divergence, and unit-root projection for project recommendations. The previously reviewed conservative partial rule and Cargo unknown-workspace classification are unchanged. No new blocking issue is introduced by the r3 diff.

## Nonblocking observation

**B2DPLAN-R3-NBO-1 — superseded historical wording (PLAN-r3.md:20).** The historical r2 changes table still says only a defaulted leaf is absent. The r3 table and section 4 clearly supersede this. Remove the old sentence or mark it superseded to prevent accidental reuse; this does not block acceptance.

## Scope and boundaries

This accepts the implementation plan only. B2-d0's reference acceptance/binding and the subsequent implementation reviews, inventory gates and prescribed validation remain future work. It does not accept implementation, integration, qualification or completion of B2 or M3-B.

Read-only inspection and hashing only. No product build, test, generator, census or network operation was run. No prohibited installation, private fixture, signing key, T2 store or overlay was accessed. Neither repository was edited. Only REVIEW.md and review.json in this review directory were written.
