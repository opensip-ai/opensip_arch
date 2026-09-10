# Unified product design direction review

D-371 adopts one intended-product design implemented in stages. This review
accepts the direction/scope correction; **the full product design remains in
progress**. Remaining contracts are tracked in the [central register](../../v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness).

Codex authored the five fixed subject files. Actual Claude Code model
`claude-fable-5-1` provided initial advice and then independently reviewed the fixed
files using read-only tools. The CLI response reports no permission denials.
The second independent verdict is ACCEPT with zero MUST_FIX and zero SHOULD_FIX.
The first review requested two SHOULD_FIX corrections: explicitly identify
the scoped membership successor and assign the advisory integration boundary
to its existing owners. Both findings and the rejected first subject remain
in the review record.
Codex's author assent is recorded in D-371 and is not independent review.

| Record | SHA-256 |
|---|---|
| [First subject, retained](subject.v1.json) | `7da09c8b1372ce9d0b7d5dd0571c072824f0e11f3c4188a807e005c21dee8fa3` |
| [First review, changes required](claude-review.v1.md) | `72ae7b0dc4e00099aea20886a58e78ec4bb273a59736b5a003d59278b46f1890` |
| [Subject manifest](subject.v2.json) | `d60dc2b5fb018fed340dddc485ff4eb1cd346e98460e64496dac118dc8c14845` |
| [Adoption act](D-371-design-target.v1.md) | `b7a27b77b80f0c5d720403676aa5e4fa41bdd17fbbc063f236e5aa3f43288c37` |
| [Claude initial advice](claude-direction.md) | `d2e35ccf933c8a99cd9237026ffe0aec010fbd6a36e81f9b7653780edd133ea2` |
| [Claude final review](claude-review.v2.md) | `c94f909e3a137500bd9c6dae1ba29158905aecfb6602b07dc21c0994d58b22f2` |
| [Machine verdict](claude-review.v2.verdict.json) | `39d5cc30e2ee63658a11aa23af012a1afb87cee2e74c4e49f282e95787276fb1` |

The initial advice agreed on language-independent host contracts, native
provider evidence, explicit scope and substantive identity/evidence/retention
closure. The final subject also updates the live completion-goal preface with
an explicit custody successor, and includes advisory integration contracts
without promising a bundled model or a complete Map application. The preceding proposal accepted by the user was one complete intended-product
design, resolving full-scope architectural gaps before implementation, with
preview only a delivery milestone. This describes the conversation context;
it is not an additional verbatim user quote. These
refinements were submitted for independent review, not silently attributed to
Claude's initial advice. Raw prompts and responses are retained alongside the
readable records.

The four live design edits are START-HERE and architecture files 08, 10 and 12.
The fixed subject includes the adoption act. Before-images are retained in
`before.v1/`; reviewed after-images are in `subject.v2/`. Downstream recording
adds the coordinator entry and this record and narrowly refreshes operational
inventories. It does not change reviewed design bytes.

[Legacy custody results](legacy-custody.v1.json) record the old D-369 checker's
three failures: the existing root README divergence and the two D-371-authorized
live register/goal changes. Historical review snapshots and application pins
remain unchanged. Claude's first review also expected a second file-08 document
custody item; the actual checker has only its register custody item, and the
measured three-failure set was supplied to the second review. [Recording validation](validation.v1.json) checks subject
hashes, new local links, current inventory and the expected failure set.
Claude's semantic content review is distinct from Codex's mechanical hash and
link validation. Neither establishes implemented behavior, complete full-product
contracts, runtime safety or release qualification.

Recording detail: the coordinator file was absent from both operational
inventories at task opening. Its requested content refresh therefore adds its
missing entry, alongside the new review README, rather than reporting a
nonexistent old entry as refreshed. Both are within the reviewed six-path
recording scope; this is not a repository rescan.
