# Additional architecture and design audit

Codex found one reproducible discovery defect, one public-contract overlap and
one advisory observation-boundary question in this additional pass against
**frozen candidate25**. A separate author correction fixes the discovery defect
in reference code. Candidate25 and its historical acceptance remain unchanged;
that acceptance does not cover the new correction. Implementation readiness
remains pending.

## Findings

| ID | Finding and effect | Evidence and disposition |
|---|---|---|
| XA-01 | Workspace limits are applied before excluding nested authority roots and before applying explicit native workspace selection. A nested repository with 4200 packages can reject its parent's one-unit analysis. Explicitly selecting just the root admits in security but refuses in native discovery. | [Original observations](discovery-observations.json), [corrected observations](discovery-corrected.json), [three-file proposal](reference-proposal/changed-source.json). Required correction; independently unreviewed. |
| XA-02 | Pruned-tree counts are exact over a supplied marker inventory. The product prose calls them hidden-marker totals while excluding discovery walks in those trees. Obtaining that inventory and handling an unenumerated tree need explicit assessment. | [Observation probe](pruning-observation.json). Advisory design question, not a demonstrated filesystem/custody violation. An optional versioned representation is proposed; its integration is not claimed complete. |
| XA-03 | Identity §5 gives exit 2 for unavailable required evidence known before evaluation; graph-query §7 and its public entry give exit 4 for known purged/expired/corrupt/unavailable observations. The ownership prose does not explicitly select that exception. | [Fresh public calls](query-availability-observations.json): retained control returns, four unavailable states consistently return exit 4. Proposed narrow selector preserves the graph owner and existing results. |

[Proposed resolutions](design-corrections.proposed.md) give the exact intended
changes and limits. The [review queue](review-queue.json) keeps independent
review and subsequent integration open. These author results must not be fed to
an origin that is still described as a blind consumer.

## Scope and results

This was a broad cross-contract pass over the five product contract areas and
their source/authority map, with focused reads and executable probes at their
boundaries. The table records the questions assessed; it is not an assertion
that every historical document, every schema branch or all 26 million lines of
review evidence received a fresh semantic read. Historical evidence was retained,
not re-accepted. No actual Grok or Claude review occurred during this pass.

| Area | Assessment in this pass |
|---|---|
| Product scope and staging | One intended product remains selected; delivery availability and typed absence do not silently reduce default requested capabilities. |
| Configuration and discovery | Explicit override, nested custody and count ordering assessed; XA-01 and XA-02 recorded. |
| Identity and canonical admission | Read exact-number/profile separation, operational-ID exclusion, typed digest ownership and current output-major selection; no additional defect demonstrated in those inspected joins. |
| Evaluation and proof | Read complete replay versus owner admission, subject census, required-work accounting, Kleene truth versus visible deficiencies, and fault origin rules; prior blind reconstruction remains required. |
| Security and lifecycle | Read discovery, clock floors/recovery, live revocation and one-writer/read/exclusive lock composition; corrected reference passes existing security cases. No OS or cryptographic qualification inferred. |
| Native capability and completeness | Assessed native/default ownership, resolution versus examined coverage, dynamic target propagation, native/import sufficiency and wire negotiation boundaries; XA-01 affects native selection. Compiler correctness is not established by synthetic inputs. |
| Clones and advisory evidence | Assessed exact/normalized/structural facts, near/cross-language candidates, import exclusion and suppression limits; no semantic-equivalence or deletion authority inferred. |
| Imports and runtime/history | Assessed shared wrapper, mandatory correspondence, staleness, observation bounds and target granularity; runtime coldness remains bounded evidence. |
| Baselines and PR gating | Assessed portable custody, current trust for prior executable closures, counterfactual evidence extents, detector removal, required coverage and hidden-regression gating. |
| Repair | Assessed per-target evidence, separate apply/recovery authorization, immutable receipt/idempotence and fresh verification. Reference projections do not establish real filesystem safety. |
| Storage, history and query | Assessed immutable assurance versus availability, pin-aware purge, rebuild versus evidence authority, explicit historical selection, cursor/budget disclosures and error routes; XA-03 recorded. No graph engine or performance claim made. |
| Outputs and readiness | Assessed shared inventory/parity, advisory boundary, inherited applicability, independent-review requirements and separate release qualification. No readiness state activated. |

Mechanical scan: **13 contract documents, 31 local links (none missing), 47
schema documents (no Draft 2020-12 structural errors)**. This includes retained
schema profiles and does not assert equivalence between majors. Exact source
hashes and results are in [contract-structure.json](contract-structure.json).

The isolated discovery proposal passes:

- Seven new observations: normal root, genuinely oversized first-party scope,
  installed dependency pruning, two excluded nested authority cases, and the
  security/native explicit-root pair.
- **464/464 security cases and all 11 security sweeps**.
- **375/375 native cases**, with **zero qualified product cells**.
- **412 integration checks**, with no failures.

These are author reference checks, with the existing trusted synthetic
observations. [Source-pin rebinding](author-pin-delta.json) is explicit and
applies only to the separate author copy. It grants no independent acceptance.
No current product code or frozen candidate source was changed.

## Reproduction and remaining work

Use Python 3.12 with the existing reference dependencies. The scripts accept an
extracted candidate25 root; do not run a patch against that frozen source.

```sh
python -I -B probe-discovery.py --source /path/to/candidate25 --out /new/original.json
python -I -B apply-reference-correction.py --source /path/to/candidate25 --copy /path/to/separate-copy --out /new/proposal
python -I -B probe-discovery.py --source /path/to/separate-copy --out /new/corrected.json --expect-corrected
```

The local author copy is
`/tmp/opensip-design-corrections/codex-crosscut-successor.v1`; its complete
three-file changes and rebinding script are retained here. The original source
is selected by manifest SHA-256
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.

Next: independently assess these findings and proposed resolutions, incorporate
accepted corrections and exact selectors, freeze a successor and obtain the
required substantive review. Any selected XA-02 representation needs its own
schema/model integration and controls first. Reconcile blind-consumer inputs and
application bindings against the final successor. Existing author examples,
residual proposals and historical consumer reports retain their actual standing.
This audit does not complete original independent reconstruction, final
application review or implementation authorization.
