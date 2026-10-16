# B2-D1 inventory v210 review

**Verdict: REQUIRED-FINDINGS.** One new inventory description states false input restrictions. All checked structural, pin, coverage and census requirements pass. The accepted code is not reopened.

## Required finding

**B2D1INV210-R1-RF-1 — correct the reader description**

Location: candidate inventory line 1847, row `crates/host/src/yaml_subset.rs`.

The description says **CRLF-only line breaks** and describes a plain scalar as having **no indicator**. The accepted unit permits **LF or CRLF**, refusing bare CR, and rejects indicators only **at the start** of a plain scalar. Existing accepted vectors establish both distinctions:

- accept-block-plain and accept-no-final-newline contain LF line endings and are accepted.
- accept-plain-flow-characters-inside accepts `a[b]{c},d`, which contains indicator characters inside the scalar.

These are false restrictions in a newly added description, rather than incomplete inherited descriptions. Replace them with LF-or-CRLF/bare-CR-refused and no-leading-indicator wording, then refresh affected pins. No code change, test run or inherited description override is needed. The review JSON records a nonaccepting verdict because this exact candidate is not ready to bind; the requested ACCEPT values cannot be confirmed yet.

## Verified pins and integration

Rehashed the staged 698-byte subject manifest: `c727ac20885745ff6b2b2836f2a32371304b7dd5bfbcfdbf80e0ba214c2c2897`. All three members match their recorded sizes and hashes. Independently verified:

- Parent v209: 708,851 bytes, `c20976abdf1003c42091ea8b27e2814749975e6cf5a4909c63ffebf9cf5a9deb`.
- Candidate v210: 711,522 bytes, `499a2a061d37ad80eb0764a532bf3237430a6782b238fe455e5668434ecf866c`.
- Successor record: 5,537 bytes, `853f8a7c220c8ef4eb8f4283ab28176c3ce2a03044af01550e8532ea07f59f16`.
- Accepted code review and code-subject pins match; the review is ACCEPT-UNIT with no required findings and names the exact accepted code subject.
- All six integrated code/package paths match their accepted archived bytes. This is an integration-byte check, not a code re-review.

Live product HEAD is `46ed61aec70b61f8805521ccbc8b3db57ac49f69`, clean. Architecture HEAD is `f2c7e448863577cba44a7fe9c0d9c8c80a6ccd8a`.

## Inventory assessment

The candidate grows from **1,285 to 1,289 rows**, adding exactly the four stated new paths. Every inherited row is equal by value. Paths are sorted and unique, and the candidate is a strict superset. All non-file top-level values are unchanged, including the **20 packages and nine pending decisions**.

The four new rows have appropriate packages and roles: host reader/source, host tests/test, host vectors/fixture, and tooling vector generator/builder. Only the vector JSON is marked generated. The other three descriptions accurately stay within the accepted unit and its evidence. The reader description needs the correction above.

The inherited lib.rs description remains true: the new reader is private. The inherited FW-01 test description remains true: the covered production discovery/configuration closure still has the stated structural restrictions and planted controls. Both are incomplete about the new reader, but neither is false; no override is required.

The candidate covers all **1,191 tracked product paths**. The exact **98 inherited planned, still-absent paths** are retained unchanged, agree with inheritedPlannedFilesRetained, and gain no implementation claim. addedFiles agrees exactly with the four-row delta.

## Integration census

Ran only the explicitly permitted source check: `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`. It reports **passed true, 114 rows, no findings**, matching the staged census. The census checker and exception-file pins match current product bytes.

The exception record contains **439 mint-audit rows**. Both the checker and exceptions file are byte-identical to the pre-B2-d1 product base, confirming the unchanged census. No mint authority is added. The successor and census explicitly claim no product qualification.

## Boundaries

Only read-only hashing, JSON parsing, Git queries and the permitted source census were performed. No compiler, Cargo, tests or lane was run. No repository, stage or control file was edited. No prohibited private fixture, installation, signing key or held tree was read; no network, other pane or delegation was used. Only REVIEW.md and review.json were written in this review directory. Assent, publication and inventory lock binding remain separate future actions.
