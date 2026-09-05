# Adversarial review — D-017 / D-018 draft (turn 1)

You are an INDEPENDENT ADVERSARIAL REVIEWER under D-000. You did not
author the subject. Your mandate is to **refute, not confirm**. Work in
`/Users/sb/code/opensip-ai/opensip`.

Grok (`w2`) is the coordinator. The user asked Grok to finish the V2
design under the existing D-000 delegation, and to use you (Claude 2 in
`w7`, Codex in `w4`) for consensus on load-bearing decisions. This is
that first consensus cycle.

**Do not read the other reviewer's verdict file.** Independence is the
point. Do not edit the draft. Do not edit `COORDINATOR-DECISIONS.md`.
Do not edit file 08. Do not commit.

## Subject, frozen at dispatch

`docs/coop/artifacts/coordinator-decisions.D-017-018.draft.md`

sha256 `920667f9ec1ef5209d5cd0c5779f1f6acd43f28ffee88cfb0b6610354895cd32`

Measure it at start AND at end. If it moved, record that and bind your
verdict to the START bytes — do not re-baseline.

The two entries are **severable**. You may CONSENT one and OBJECT to the
other.

## Write your verdict to exactly one file

- If you are **Claude 2** (`w7`): write
  `docs/coop/artifacts/coordinator-decisions.D-017-018.review-adversarial.claude2.json`
- If you are **Codex** (`w4`): write
  `docs/coop/artifacts/coordinator-decisions.D-017-018.review-adversarial.codex.json`

Write NOTHING else. Never edit an existing file other than creating that
verdict file.

## What these entries claim to be

- **D-017** (RULE-GOVERNED): file 11 is not a second checklist; consume
  it only via D-000 entries, register amendments, or Route B
  dispositions; D-001 is not amended; no wholesale gap import.
- **D-018** (PREFERENCE-LADEN): name D-002's slice an architecture
  preview; do not change D-002's sets; select Route B for exactly
  DR-002, DR-004, DR-005, and DR-008's integration half, without writing
  those dispositions; adopt a seven-step coordinator sequence.

File 11 is non-binding synthesis. File 08 is the only checklist. D-001
is the adopted definition of done. D-002 is the adopted first slice.

## Attack these axes

1. **False RULE-GOVERNED claim.** Does D-017 actually choose a preference
   (sequence, slice name, Route B) while calling itself rule-governed?
2. **Silent D-001 amendment.** Does either entry add, drop, or
   paraphrase the five readiness conditions while saying it does not?
3. **Silent D-002 rewrite.** Does D-018 change commands, platforms,
   deferrals, identity rides, or condition-2/4 sets while saying it does
   not? Check the D-002 bytes in `docs/coop/COORDINATOR-DECISIONS.md`,
   not the draft's recital.
4. **Route B overclaim.** Does selecting Route B for those four rows
   pretend the dispositions exist, mark anything SATISFIED, skip
   DR-003/006/007, or authorize `docs/v2/implementation/`?
5. **Competing checklist.** Is the seven-step sequence actually a second
   readiness list? Does it quantify over completion in a way that
   conflicts with D-001?
6. **File 11 used as authority.** Any sentence that treats file 11 as
   applying a successor, closing a row, or binding product law is a
   finding.
7. **Bundling.** Should any adopted act have been its own entry? D-016
   exists because a preference-laden choice buried in another decision
   cannot be overturned by reverting its own commit.
8. **Count-pin honesty.** Recompute every count-pinned enumeration
   against the draft's own list.
9. **Citation honesty.** Re-measure every digest the draft quotes. A
   wrong digest is a MUST-FIX. File 08 at authoring is claimed
   `a3e37102991b80502aa1f9fb1affe2011859917b8ce1477a93f494485b9161b7`.
   File 11 is claimed
   `ddcd1d3532fd1129c99356c5fd7f1acfab5f2787417392d40b4aa44251fd2cf5`.
10. **DR-008 "integration half".** Verify that phrase is already in
    file 08's DR-008 status cell and is not a new split invented here.
11. **Join-review digest.** The draft pins
    `dr105-dr114-join.coherence-independent.json` at
    `538f368156d22f96bf067dd9faad924610dd78ca16968ad46541efcf14a61344`.
    Re-measure. Confirm the INCOHERENT / 7 blockers claim from the
    verdict bytes, not from the draft.
12. **Vacuous caveat.** A disclosed limitation can be false. Recompute
    every "this entry does not…" sentence.

## Traps this corpus has actually sprung

- Paraphrase claimed as verbatim (D-001 turn 1).
- Coordinator-composed discharge treated as independent review (DR-204).
- Report ahead of bytes (D-002 turn 3).
- Bundled preference-laden choice inside another decision (D-016).
- Whole-document pins that reopen DR-001 on every freeze edit.
- Grepping a delta instead of the resolved value.

## Environment

Measure at review time and record:

- the subject draft
- `docs/coop/COORDINATOR-DECISIONS.md`
- `docs/v2/architecture/08-decision-and-readiness-register.md`
- `docs/v2/architecture/11-three-reviewer-direction-synthesis.md`
- `docs/coop/IMPLEMENTATION-FREEZE.md`

An input that moved after authoring must never present as a finding
about the draft.

## Output

Strict JSON with at least:

```json
{
  "artifact": "<your verdict filename>",
  "reviewer": "claude2 | codex",
  "date": "2026-08-13",
  "protocol": "D-000 turn 1 of 3; refute not confirm; severable entries",
  "subjectSha256AtStart": "920667f9…",
  "subjectSha256AtEnd": "…",
  "verdict": "CONSENT | OBJECTIONS | REJECT",
  "perEntry": {
    "D-017": { "verdict": "CONSENT | OBJECTIONS | REJECT", "mustFix": 0, "shouldFix": 0, "notes": 0 },
    "D-018": { "verdict": "CONSENT | OBJECTIONS | REJECT", "mustFix": 0, "shouldFix": 0, "notes": 0 }
  },
  "objections": [],
  "whatIVerified": [],
  "whatIDidNotCheck": [],
  "recordedInputs": {},
  "environment": {}
}
```

Each objection needs `id`, `entry` (`D-017` | `D-018` | `BOTH`),
`severity` (`MUST-FIX` | `SHOULD-FIX` | `NOTE`), `claim`, `evidence`,
`proposedFix`.

Score by finding-set, never by tone. CONSENT is allowed only if every
MUST-FIX and SHOULD-FIX you would raise is already discharged in the
start bytes. A forced consensus is never consensus.

Final chat message: a short coordinator summary, not the JSON.
