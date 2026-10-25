# Configuration S4 on main (unit S4-MAIN-r1)

Lead: Claude claude-opus-5-5/high, 2026-10-25. Product subject: branch
`claude/config-s4-on-main`, commit 7a85025 on main e39cee8.

The S4 configuration successor (B-S10's configuration line: the pure resolver and
X12 admission moved into opensip-evaluator, a host facade and projection, the
config-pinning table generator) was staged on an unaccepted, never-compiled P+D
precursor. The lead rebased S4 onto main alone (lead decision `leadDecisionSplit`,
control CURRENT-STATE 2026-10-25). The snapshot pipeline continues as unit SP-1.

- CB1-CB4: `evidence/lane-summary.json` (candidate 18/18 pass; base differs only by
  S4's intended test relocation and additions).
- CB5: `PCS2-OWNER-STATEMENT-r2.md`, the lead-selected delegation reading for PCS2,
  with the owner-string migration deferred to the next generator-closure change
  (its hash is bound into the discovery and snapshot-ledger census held-out receipts).
- CB6: inventory v240 (seven additive rows) and this successor's description
  meanings.

Reviews, recorded as given:
- Code: Codex gpt-6-astra/high, verdict REQUIRED-CHANGES. It found no code correction
  necessary and supported the rebase and lane evidence; its one required change was the
  CB5 paragraph 4 wording, now corrected. It issued no ACCEPT-UNIT-CODE token.
- CB5 r1 (Codex draft): Claude claude-opus-5-5/medium, REQUIRED-CHANGES F1-F6, all
  incorporated in r2.
- CB6: Codex, this unit's binding review.
No production analysis caller, native authority, K7 or qualification follows.
