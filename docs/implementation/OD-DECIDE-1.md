# OD-DECIDE-1: the lead decides; a panel and a red team first; the owner only when the lead cannot

Status: accepted owner decision; effective 2026-11-12 UTC.
Scope: who makes the decisions the lead would otherwise put to the project owner, and how. It changes no product
law. It also records three answers the owner gave in the same message.

## Owner instruction

> keep codex, and i agree with your two design decisions. for the decisions you ask me to make, i want to provide
> you with the authority to make the decisions yourself and only when you cannot decide, then you involve me. what i
> ask though is that you run the decision through a panel and red team when you need to make a decision as that
> will help you ensure that you have made the best decision that you could.

Everything below this line is the lead's wording and reading, not further quotation.

## The three answers

1. **Codex stays** as the cross-vendor reviewer. OD-REVIEW-1 and OD-PACE-1's review rules stand.
2. **The owner agrees with the lead's two design decisions** of 2026-11-12, both in the proposed design record
   C2A-ORDER-E1 (`docs/implementation/m3/host-pipeline-j/c2a-order-e1-r1/README.md` on branch `c2a-order-e1-r1`):
   - clause E1c option (a): the trust-floor record written at pipeline step R10 carries a separately reserved
     ExecutionId scoped to that act, rather than a successor to the trust record's shape;
   - clause E2: registration (R9) runs before the endpoint join; the pipeline law's table order is an erratum.
   The owner's agreement does not replace that record's cross-vendor review or its adoption. If the review rejects a
   reading the decision rests on (the record's open point O2), the decision comes back through the procedure below.

## The delegation

3. **The lead makes the decisions it would otherwise ask the owner to make.** The owner is involved only when the
   lead cannot decide.

### The procedure the owner asked for

For each such decision, before it takes effect:

- **A decision brief**: the question, why it must be decided now, the options (including "defer"), what each
  changes in law, code, durable records and user-visible behaviour, what each costs to reverse, and the texts that
  bear on it with exact citations.
- **A panel**: at least three independent reviewers who each read the brief and the cited texts and return a
  recommendation with reasons, without seeing each other's answers or the lead's preference. The panel is given
  different lenses (for example: the law's texts; security and failure behaviour; the user and the product; cost to
  reverse). When Codex is available it sits on the panel as the cross-vendor voice; when it is not, the decision
  says so and Codex sees it at its next review of the affected work.
- **A red team**: at least one reviewer whose only job is to break the option the lead intends to choose: find the
  input, state or reading under which it is wrong, unsafe or dishonest, and the cheapest attack on its reasoning.
  The red team sees the lead's intended choice; the panel does not.
- **The decision**, written by the lead with: the choice, the panel's recommendations and any dissent, the red
  team's strongest finding and how the decision answers it (or that it does not and why it stands), what would
  reverse it, and the controls that follow from it. Recorded as a numbered lead decision beside the work it governs
  and listed in the live map.

### When the lead cannot decide (and the owner is involved)

- the panel is split and no argument or text settles it;
- the red team finds a serious problem with every option that the lead cannot answer;
- the decision needs something only the owner has or can do: money, an account, a credential, a legal or
  commercial commitment, contact with a person or organisation outside the project;
- the decision would be hard or impossible to undo outside the two repositories (for example publishing, a
  release to users, deleting something that exists nowhere else);
- the decision would change what the owner has said the product is for, or set aside one of the owner's own
  recorded decisions.

In those cases the lead brings the brief, the panel's and red team's findings, and its recommendation.

## The lead's reading of the scope

- It covers design, law-reading, product-behaviour and process decisions, including those earlier lists marked
  "for the owner" (for example: what the launcher check verifies under ad-hoc signing; what an empty configured
  selection does publicly; remedy texts for failure rows; the open owner points of the delivery record).
- It does not change the standing rules on pushing (push after each green, reviewed integration; report each
  push), on review independence, or on the full lane before a merge.
- Signing: the owner's recorded signing decisions stand (ad-hoc signing for the TypeScript stage and, by
  OD-SIGN-RS1, for the Rust stage; no Apple Developer account until near completion). Decisions inside those
  decisions are the lead's under this procedure. A decision that needs a signing identity, notarization or an
  account is the owner's by the list above.
- The lead still reports every such decision to the owner when it is made, in plain words, so the owner can
  reverse it.
- Routine technical rulings on worker questions (which function owns a value, a test's shape, a fail-closed choice
  inside accepted law) are not "decisions the lead would ask the owner to make" and stay ordinary lead rulings,
  checked by the independent reviews as now.
