# Review parent-subject digest adapter

**Standing.** Actual Grok coauthor application-tooling correction. Not independent review, not blind ACCEPT, not bind/assembly/application. Frozen/source/live were not edited. Active `consumer-b.v12` was not read. Refused consumer-b.v11 layout is **parser-shape evidence only**.

**Verdict: `PROPOSED_FOR_ROOT_INTEGRATION`.** Successor `review_envelope.py` admits `inputKit.parentSubjectSha256` as a parent field and never treats `inputKit.manifestSha256` as parent.

## Problem

`review_subject_digest` collected only `subjectManifestSha256` and `subject.manifestSha256`, dropping nulls via `.get`. Blind consumer JSON (charter did not require those two fields) declares:

- `inputKit.parentSubjectSha256` = frozen parent (`a70f5830…`, accepted24)
- `inputKit.manifestSha256` = normative subset kit (`ea2fa750…`, different)

Binder `bind-review-receipts.v1.py` joins `review_subject_digest(review) == design_spec.manifestSha256` (the **parent**). Using the kit digest as subject would bind the wrong bytes or refuse a legitimate parent declaration. Omitting the parent field refuses a charter-legal shape.

This adapter does **not** waive verdict, findings, session, kit `consumer-input-manifest.json` `parentSubjectSha256`, Codex assent/assessment, or coauthor gates. B11 remains refused as a reconstruction; this is metadata shape for a **future** valid blind.

## Fail-closed meaning

| Declaration | Result |
|---|---|
| Optional parent key **absent** | Not required (existing top-only or nested-only callers unchanged) |
| Parent key **declared** null / non-string / non-64-lowercase-hex | Refuse (not silently dropped) |
| Declared `subject` or `inputKit` not an object | Refuse |
| No parent field at all | Refuse |
| Two or more declared parents that differ | Refuse |
| `inputKit.manifestSha256` only | Refuse (kit is not parent) |
| Parent + kit digest both present, kit different | Admit **parent**; kit ignored as parent |

Stricter than current `.get` + filter-None when a parent key is **explicitly null** beside another valid parent: old code would ignore the null and admit the other; new code refuses a declared invalid value. Absent keys stay optional. That is the fail-closed rule for “declared.”

## Binder

`bind_one` still: hash-check review file, `require_verdict`, `require_findings_none`, `review_subject_digest == expected` (frozen parent), public envelope decode, session ≠ coauthor, design vs blind sessions distinct, input-manifest `parentSubjectSha256`, assessment `parentSubjectSha256`. Unchanged. No bind was run here.

## Tests

`check-review-envelope.v2.py`: **34 passed**, 1 failed.

Existing 20 IDs preserved. **19/20** pass. `this-session-empty-raw-is-not-a-review` still points at `grok-application-successor-preparation.v1/response.raw.json`, which is now a completed Grok envelope (`stopReason=end_turn`). Original checker fails the same control in this environment. Not caused by the parent-field change. Decoder correctly treating that completed envelope as Grok public JSON is not application authority.

New guards all passed: alternate parent admits parent ≠ kit; kit-only refuses; top/nested vs `inputKit.parentSubjectSha256` conflict refuses; agreeing declared parents admit parent; uppercase/short/null/wrong-type refuse; non-object `inputKit`/`subject` refuse; omitted nested `{}` still admits top-level; B11-shaped record labeled parser-shape, not acceptance.

## Limits

- No actual binding or staging.
- B11 verdict is not accepted.
- Root must integrate these bytes; this directory is not live tooling.
- The brittle 20th environmental check was not rewritten to manufacture 20/20.
