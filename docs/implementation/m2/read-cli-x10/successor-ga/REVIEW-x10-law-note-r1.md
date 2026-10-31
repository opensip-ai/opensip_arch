# Independent review: X10-SUCCESSOR-GA-r1

X10-LAW-NOTE: REQUIRED-FINDINGS

Reviewed 2026-10-31. Three BLOCKING findings concern this successor note's custody/binding completeness and one inaccurate scope assertion. They do not revoke the earlier `GUARD-AMENDMENT: ACCEPT` for the two exact guard diffs or purport to undo the supplied coordinator adoption receipts.

## Authority and verification

Request: `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/review/REQUEST-x10-law-note-c2b.md`, SHA-256 `8737b7cb7ed9e329719f25cadcd0b24062ea0031e4740f2cd865f96c8186a2c7`, matched.

Before substantive review, the canonical router returned exit 0, `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high`, for `check --provider codex --route R3-FRONTIER`. The note's Claude author and Codex reviewer are different vendors. Re-read live control indirection and the current ACTIVE-PLAN/MAP top; the precise current request selects this review. The MAP architecture checkpoint remains older than live architecture `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`; no older checkpoint was substituted for the pinned request.

All ten request-listed evidence hashes matched, and all ten files have no write permission bits. The one-member successor hash manifest matches the supplied note. The copied GA review matches the previous review by value (`243c5cce7bfc5dd564ecde2d1b28bc624ececf820bf5eca5ea0e7bf9dd3d2c89`). The note under review is SHA-256 `46fe3fd408b5126f97a2e3463429d3e716598255c69e3d329848836d0868a759`.

References: `R/` means `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/`; `NOTE` means `R/evidence/h5/guard-amend/guard-amend__X10-SUCCESSOR-GA-r1.md`. Product citations below are at H5 `76ce532aa1191aa79791d4822c0855de9bf5e55a`, resolved and read from the product Git object database. Architecture citations are at `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`.

## Answers to the requested scope

1. **Feature list and GA-2 assertion: substantively correct names and activation restrictions; not yet complete as a byte-pinned law note.** NOTE:23-31 names exactly the four H5 host features. Parsing H5's `crates/host/Cargo.toml` confirms the feature map below. The new feature has an empty array, no default, and is required by the allocation test target. NOTE:47-50 correctly cites exact equality and the guarded endpoint with no dev exception. H5's doctor file hashes to the previously accepted after-copy, `f50f76b81b637ed76d348518aca3046451e0917af22d7a9fa8f102e733ca92bc`; the creator file likewise remains `9e73b5d790fd2cf7b85be99d943255fbc792ac0da905f710fea47eca1b919c4f`. The stricter refusal of all dependency activation is already part of accepted GA-2. However, the note does not pin the manifest or spell its complete forwarding values, and its exclusive-consumer statement is false (XL-1, XL-3).

2. **Successor form and scope: correct identified passage, incomplete parent pin.** NOTE:3 and :21 identify X10 r4 item 5's third Pin bullet and limit replacement to host. NOTE:12-15 accurately quotes `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md:94` after line-wrap normalization. NOTE:40-43 preserves security/storage and the other clauses, with prior widenings retained. M3-O1 r2 `docs/implementation/m3/operability/o1/PROPOSAL-r2.md:310-312` supports the existing development feature forwarding/release restriction. No production feature is added to the enumerated set. Nevertheless, the parent is identified only by mutable path/revision/line, not exact bytes (XL-1). The extra exclusive-use sentence is not an accurate restatement of the accepted source (XL-3).

3. **Exact receipt references and binding clause: not satisfied.** The dispatch request supplies full hashes for both receipts and the prior review, and those files verify. NOTE:5-6 itself supplies only receipt names and an abbreviated review hash. It has no binding section or concrete architecture destination. Receipt v2 directs a by-value C2b binding and future H6 lock, but does not identify the actual architecture-relative destination/member map either. No pinned staged binding manifest or H6 lock is among this request's inputs. Thus the reviewed package establishes the instruction to bind, not completed by-value binding. XL-2 requires the note's exact references and binding clause; this review does not demand a completed H6 execution before the law note can be corrected and reviewed.

## Required findings

### XL-1 — BLOCKING — parent and H5 feature bytes are not pinned in the successor

**Sites:** NOTE:3, :23-26, :45-52; `R/evidence/h5/guard-amend/X10-SUCCESSOR-GA-r1.SHA256SUMS:1`.

The parent has a path and line number but no content hash or pinned architecture commit. The enforcement section uses abbreviated `76ce532…` and gives no host manifest hash. The one-entry hash manifest pins only the note itself. The names are correct, but the document called an exact feature-list successor leaves the existing forwarding arrays implicit and does not bind the complete H5 feature map to bytes. An exact dispatch hash for the note does not fill in its missing parent/product references.

**Correction:** add the full parent path, architecture commit and SHA-256; the full H5 commit and host manifest SHA-256; and the complete feature entries (or an unambiguous byte-bound equivalent). Independently verified values for the successor are:

- Parent architecture commit: `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`.
- Parent `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md`: SHA-256 `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a`. Working-copy bytes equal that Git object.
- Product H5: `76ce532aa1191aa79791d4822c0855de9bf5e55a`.
- H5 `crates/host/Cargo.toml`: SHA-256 `0d9cf05ce826c07c29c41dea1da541cc13785272809d0fe2d400b10bcaebcbc9`.
- H5 `crates/host/src/lib.rs`: SHA-256 `dadee895cc3029ad51f330cc71fe1c8313988f009711e11a50af1f05686bbda0` (whole H5 file; distinct from H4 because of C2a's separate edits).

```toml
[features]
crash-matrix = ["opensip-storage/crash-matrix", "opensip-security/crash-matrix", "opensip-platform/crash-matrix"]
operability-dev-sinks = ["opensip-operability/operability-dev-sinks"]
harness-instrumentation = ["opensip-operability/harness-instrumentation"]
profile-allocations = []
```

This is the parsed H5 feature map rendered without comments; it is not a claim that the code block reproduces the manifest's complete physical section bytes.

### XL-2 — BLOCKING — missing exact provenance references and named binding destination

**Sites:** NOTE:4-6, :45-58; `R/evidence/h5/ADOPTION-GUARD-AMENDMENT-v2.md:6-12`.

Neither receipt is hash-referenced in the note. The review reference is truncated to `243c5cce…`. The note contains no clause stating the concrete architecture destination for itself, both receipts and the review by value. Receipt v2's direction to put them in “the C2b binding” and give an H6 design-lock commit is a required future action, not a concrete location or evidence of completion. The request's complete input hashes do not make the standalone successor's references complete.

**Correction:** add a binding/provenance table naming the actual architecture-relative destination for each of the four members and the complete source hashes for the three existing evidence files. Name the owning binding record/manifest, preserve v1 as historical and v2 as its binding-clause successor, and describe H6 as pending until its actual lock is supplied. Avoid a circular self-hash: the external binding manifest can pin the final successor note.

The verified existing evidence hashes are:

| Member | SHA-256 |
| --- | --- |
| `ADOPTION-GUARD-AMENDMENT.md` | `e33e273a3adc7cbeeccba702f421393a20e2523a3b308a79e2208414dbf730a2` |
| `ADOPTION-GUARD-AMENDMENT-v2.md` | `375e410806556584901e66039a22a9488583f28f6e9570c4877c3248a7c01cb7` |
| `REVIEW-guard-amendment.md` (supplied copy named `REVIEW-guard-amendment-GA-r1-ACCEPT.md`) | `243c5cce7bfc5dd564ecde2d1b28bc624ececf820bf5eca5ea0e7bf9dd3d2c89` |

### XL-3 — BLOCKING — exclusive allocation-target use contradicts H5

**Sites:** NOTE:32-36; H5 `crates/host/src/lib.rs:128-132`; H5 `crates/host/src/typescript_profile_tests.rs:6`.

The sentence “They are used only by host's test target `typescript_profile_allocations`” applies to both listed modules. H5's ordinary host library test module `typescript_profile_tests` directly imports `crate::typescript_profile_controls::{self as controls, Resolution}`. That module is included under `cfg(all(test, target_os = "macos"))`; the controls are included under `cfg(all(target_os = "macos", any(test, feature = "profile-allocations")))`. Therefore the controls have a consumer outside the allocation integration target, even without enabling the feature. This is a concrete existing source relationship, not a hypothetical production escape.

**Correction:** state that the feature exposes the allocation support seam and enables the controls on macOS, while the controls are also compiled and used by host's library tests under `cfg(test)`. Remove the blanket exclusive-consumer assertion. Preserve the exact no-default, no-forwarding, dependency-activation and no-debug-assertions refusal rules. The correction requires no guard or product source change.

## Carried context and non-claims

The previous review's stale source comment and validation-wrapper observations remain carried in `CARRIED-HARDENING-v15.md`; this note does not discharge them. The author's separate missing-`X10 r5` observation is also already carried there. This review does not certify that global absence claim or reopen platform's measurement admission; the proposed host successor does not rely on that alleged revision.

Read-only review: hashes, permission bits, Git objects, TOML parsing and source/document inspection. No tests, lane, staging script, design-lock regeneration, adoption, integration or external messages were performed. Only this verdict artifact was written. The values above make the corrections concrete; they do not silently repair or accept the frozen note. A corrected successor needs new frozen bytes and pins, followed by review. Acceptance/adoption of the earlier guard amendment remains a separate evidence class from acceptance and eventual binding of this successor, and neither implies qualification.

X10-LAW-NOTE: REQUIRED-FINDINGS
