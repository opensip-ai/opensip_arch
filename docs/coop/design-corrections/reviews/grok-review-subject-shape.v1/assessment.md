I’ll correct the review-subject digest adapter so `inputKit.parentSubjectSha256` is a legitimate parent field, without treating the kit manifest digest as parent. Work stays in `grok-review-subject-shape.v1`.I’ll copy the originals, then add the parent-field adapter and fail-closed digest checks without changing binder gates.**Verdict: `PROPOSED_FOR_ROOT_INTEGRATION`.** Successor bytes are only in `/tmp/opensip-design-corrections/grok-review-subject-shape.v1/`. Not bind, not B11 acceptance, not a v12 read. Frozen/source/live were not edited.

`review_subject_digest` now treats these as parent fields, and they must agree when more than one is declared:

- `subjectManifestSha256`
- `subject.manifestSha256`
- `inputKit.parentSubjectSha256`

`inputKit.manifestSha256` is the subset kit digest and is **never** parent. Binder still joins the extracted parent to frozen `design_spec.manifestSha256`. Verdict, findings, session, kit manifest `parentSubjectSha256`, and Codex assessment gates are unchanged.

**Fail-closed:** absent optional keys stay optional (top-only callers still work). A **declared** null, wrong type, non-object `subject`/`inputKit`, malformed (non-64-lowercase-hex) digest, missing parent field, or conflicting declared parents refuses. Kit digest alone refuses. Kit digest beside a valid parent is ignored as parent.

**Tests:** 15 new discriminators passed (alternate parent, kit-only refuse, conflicts, malformed/null/wrong-type). Existing 20 IDs preserved: **19/20** pass. `this-session-empty-raw-is-not-a-review` still points at `grok-application-successor-preparation.v1/response.raw.json`, which is now a completed Grok envelope; the original checker fails the same control. That is not a digest-adapter regression, and it was not rewritten to force 20/20.

Root can integrate `review_envelope.py` later. No binding or staging was run.
