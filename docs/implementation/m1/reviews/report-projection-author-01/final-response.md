I wrote the complete report-projection owner for AUDIT-G10 as an author candidate for root and fresh independent review, not approval. The reference check passes on the final files: all 20 pins verify and all 79 test cases give their exact expected result. Nothing in the architecture repo was edited, and no UI or product code was built or run.

**Files** in `/tmp/opensip-implementation/m1-report-projection-author-01`:
- **`report-projection.schema.json`**: the new schema, `$id …:evaluator3:report-projection:1`. Its raw SHA-256 (`02bc8b1b…1811`) is the value that goes into `projectionSchemaSha256s`.
- **`contract.md`**: the rules the schema can't express, limits, the R01–R24 map and the measurement plan.
- **`fixtures.json`**: test documents built from the witness corpus. `build_fixtures.py` regenerates it byte for byte, and the check enforces that.
- **`check.py`**, plus its output in `check-result.json`.
- **`successor.json`**: sha256 pins for every parent and candidate, plus replacement text for chapter 14 lines 339 and 556. The parent files themselves are untouched.

**How it works**
- **Parity:** the complete Envelope4 value is the only parity source, and its closed schema is unchanged. The embedded copy may differ from the JSON output only by dropping `agentHints` and, by default, `projectRoot`.
- **Renderer gating:** only the 8 HTML commands are accepted, and the checker derives that set from inventory4 and the prototype inventory. Each command has a required, exact `supportedReportViews` list and a fixed set of required and forbidden panels.
- **Panels:** evidence, graph, comparison, history and catalog. Each carries a state: present, omitted, unavailable, corrupt or incompatible, each with a fixed reason list. Three kinds of limit stay separate: limits recorded in the original analysis records, host trimming counts, and browser display limits. Every panel reuses existing records exactly: `CoverageResultV3`, graph `{request, response}` pairs, `comparison:2`, `AnalysisResult` with `FindingSurface`, policy `Rule` and `ReleaseCapabilityRegistryV1`. There is no untyped escape hatch.
- **Catalog:** a new private host projection that records its source (plan and policy digest, or a checked registry digest). There is no description text because no admitted source for descriptions exists. Rows grant no permission.
- **History:** only the audit baseline's source Run, requested explicitly. It is never replaced by a later Run.
- **Cross-record joins:** 38 of the cases are misjoins or budget-rule violations, and each must be refused with its own code, so a refusal for the wrong reason fails the check. Examples: graph Run or project mismatch, a hidden continuation page, wrong endpoint or relation, and coverage, comparison, history, plan or registry mismatches. Another 31 cases are shape or depth refusals (for example a non-HTML command, a latest view, an extra envelope field).

**Budgets (UQ-1).** These are development limits, explicitly not measured performance. Each one is recomputed by the checker from the owner schemas and measured record sizes:
- **Panel data limit:** 4 MiB, the accepted codec size.
- **Graph:** 6 slots of 1,000 rows each.
- **Evidence:** 3,956 entries.
- **History:** 1 Run, with up to 5,526 findings.

The prototype's 8 MiB graph cap and 20-run window are not inherited; they appear only as cases in the measurement plan.

The report needs a larger codec than the accepted 4 MiB / depth 32, for two reasons shown by the checker:
- **Size:** only about 5,526 realistic findings fit in 4 MiB, but Envelope4 allows 100,000. An 8,000-finding envelope is refused by the accepted codec and accepted by the report profile. The envelope ceiling is therefore 80 MiB, and the whole document 88,145,920 bytes.
- **Depth:** a policy rule that is valid at depth 32 on its own exceeds 32 once embedded. The report profile allows depth 38.

Required parity is never truncated. An oversized envelope fails required delivery using the existing `DELIVERY` details, and panel data that won't fit is dropped whole, in a fixed order.

**Things to know**
- **fit HTML is blocked by an existing gap.** fit declares `candidates` and `evidence-levels` as parity fields, but Envelope4 has no place to carry them for `kind=run`. Until the envelope owner adds one, fit HTML has to fail required delivery (RP-OBL-1). The projection doesn't add a substitute.
- **Changes from the P-5 sketch:**
  - The family name is `opensip.product.report-projection`, matching existing names.
  - History rows are not nested envelopes, which would need an invented request id and termination.
  - Repair-preview reads recipe data from the envelope, with no catalog panel.
- **Remaining obligations:** building the real report and measuring it (RP-OBL-2), registering the schema and codec with the generator (RP-OBL-3), and choosing which graph endpoints the host pre-loads (RP-OBL-4, which affects usefulness only).
- **Arch repo state:** it already had uncommitted changes when I started. None are mine, and every file I relied on is pinned by sha256 and verified by the check.
