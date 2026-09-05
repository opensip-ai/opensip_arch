# Independent security behavior repair review v2

**OBJECT — original six counterexamples are repaired; three adjacent complete-report defects remain.** External replay passes **1303/1303**. All eight subject pins match before and after review.

Freeze manifest SHA-256: `97b7b1db982b244417e907b85c80e07d348e6b1ae1018a4d0eabc546fdd087f0`. Exact hashes, original-finding dispositions, complete counterexample inputs and reproducer source are in [the review JSON](security-behavior-independent-review.v2.json).

## SBR2-1 — Full-report SHA-256 grammar accepts a trailing newline

The new composed report schema uses ^[0-9a-f]{64}$. Under the actual Python/jsonschema regex engine, $ matches before a final newline. The full doctor reader accepts admittedManifestDigest containing 64 hex digits plus newline. Standalone host projection hex64 uses fullmatch and rejects the equivalent defect, so the complete report path still admits an invalid field encoding.

**Required repair:** Use an absolute end-of-input pattern compatible with the schema engines or a separate exact fullmatch/length check. Apply it consistently to every SHA-256 carrier including manifest, contract, policy and admission digests; retain complete-report newline suffix mutations.

## SBR2-2 — New UTF-8 caps lose schema field semantics in nested and array positions

bounded() chooses limits from only the immediate JSON key. Array items are traversed under numeric index strings, so scope.checks entries use the general 4096-byte cap rather than the adopted 128-byte ID/label cap. policyProvenance.authority also receives the generic cap; the schema supplies maxLength=512 characters rather than v25 512 UTF-8 bytes. The full reader accepts 256-byte check labels and 1024-byte policy authority. Host pair source_ref correctly enforces the latter byte bound, leaving inconsistent report acceptance.

**Required repair:** Drive UTF-8 limits from schema annotations or a path-aware typed walk so each array item and nested source-identity string retains its declared byte cap. Exercise equality/+1 in complete reports for every capped field family, especially labels inside arrays and all four source identity fields. Preserve the separately adopted whole-document/container limits.

## SBR2-3 — Embedded full reports still accept preview-excluded granted keychain acts

doctor_reader checks only CA-2 and CA-1 IN_PROCESS granted exclusions. Changing a valid granted CA-3 OUT_OF_ROOT_READ full report to CA-3 KEYCHAIN remains accepted as OC-1. The standalone host-record validator correctly excludes the same subtype regardless of context. KEYCHAIN is a legal report subtype for a denied attempt, but cannot appear granted in the preview.

**Required repair:** Share the immutable preview-exclusion predicate between embedded report and full host record validation. Reject granted CA-3/CA-4 subtypes outside the preview scopes already encoded in host_record_valid, while preserving valid denied subtype records. No external authority proof is required to check an unconditional preview exclusion.

The exact 260 journal oracles, paired clock/delay comparisons, independent OC predicates, repaired cleanup handling and composed malformed-field refusals are confirmed. Delegated bounds adoption is accepted as the intended design direction. Final high-water/restore/redaction/BLK and security activation joins remain separate; no production qualification, automatic acceptance, SATISFIED or register disposition is asserted.
