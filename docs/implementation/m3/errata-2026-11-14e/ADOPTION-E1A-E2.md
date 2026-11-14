# E1A-E2: adopted at r2 (lead, 2026-11-14 UTC)

`LC/j3d-ts/discovery-flags/ERRATUM-E1A-E2-r2.md`, sha256
`2896a7effe705e8d4c71f456d8920a3fb45ff0573abbc41d48bd204433617ac3` (12,770 bytes), is adopted as an erratum to the
bound erratum DISCOVERY-FLAGS-E1a r4 (control 8.4's 4,097-character leg) and to accepted M3-B r10 item 14a (the place
of the node-path check, for the sources at discovery and at the post-seal validation). Neither document is edited.
Accepted by both reviewers at these bytes: Codex `review-codex/VERDICT-E1A-E2-r2.md` (sha256
4fa62d91f3fbb87a603977ba494d66b22b4d223c19f1add18cb0078b93c6f04f), Claude `review-opus/VERDICT-E1A-E2-r2.md` (sha256
556ea391e6063b9b41b0322e746912987df6b5b6c01bebf3d07b0cb77aeec3de). History: r1 (each reviewer one required finding:
Claude E2-R1, the "not skipped" rule holds only for path candidates; Codex E1A-E2-RF-1, statement 3 must speak only
of a file the discovery walk encounters within its admitted, non-pruned scope), r2 by the lead (both ACCEPT).

What it binds (the text governs; this is a summary): a PATH candidate longer than item 14a's 4,096-character
node-path bound is `native.typescript-config-bound`, decided on the candidate's spelling, the comparison charged
first, after E1a 7.2's gate and before any open, observation, capture or load; it is not passed over in favour of the
next candidate; at the post-seal validation it is a rederivation result under E1a 2.4. E1a 8.4's 4,097-character leg
is that refusal with a base absent from the project. A file the walk encounters within its admitted, non-pruned scope
whose path exceeds `LogicalPath`'s limit remains the walk's refusal; nothing widens the walk.

Recorded with the adoption:
- Not decided here, owed to erratum E1c: an over-long PACKAGE candidate (a later candidate in an ancestor directory
  can be shorter and can be the file the compiler reads).
- Implementation (lead ruling, to be confirmed by both reviewers on the code): the check is made only in the host's
  two sources; the shared configuration vectors and the provider are unchanged, because the host refuses at discovery
  before any provider is launched; the provider-side statement is owed with the next provider change.
- For the owner's post-M3 review list (the compiler resolves or cannot read, the product decides differently):
  the pinned compiler has no path-length bound of its own; run directly on macOS it cannot read a configuration whose
  absolute path reaches 1,024 bytes, and on Linux 4,096; the product bounds project-relative characters and reads
  through the sealed snapshot's virtual host. A candidate with a single path component over 255 characters still
  ends as a capture invariant and not as a configuration refusal (Claude's standing advisory); the walk's own name
  refusal has no owned outcome row yet. Both go to the refusal-projection follow-up.
- Binding into the design repository is owed before the implementing unit (DISCOVERY-FLAGS-1) integrates into main.

It accepts requirements only: no implementation, price, census, integration or Run gate.
