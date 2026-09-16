# consumer-b.v24-source39.v2 — session standing

**Origin.** This is a continuation of the same original fresh blind origin
`9d3dfb70-b2d3-498c-a3c1-f8de9e488514`. It is an additional self-audit of the
existing reconstruction against the unchanged normative source39 kit. It does not
claim fresh-origin independence anew. It is not a new design kit, acceptance, or a
replacement for the source39.v1 finding s39-M1.

**Runtime.** `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2`.
`output/` did not exist at start. Everything this session wrote is under `output/`.

**Inputs read.**
- `charter.md` and `requirements.json`, read fully.
- `subject/`, the normative kit. `consumer-input-manifest.json` has SHA-256
  `c2f2f88d2e3bebfa8fa1b521cb76d2584483eb922973d6e555fe05a15da4ad80`, parent
  `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`, and all 104
  members verified (`vectors/phase0-custody.json`).
- Own prior outputs, read-only:
  - `consumer-b.v24-source39.v1/output`, copied byte-exact to `preserved/source39-v1/`
    with a SHA-256 manifest;
  - the original `consumer-b.v24/output`, hash manifest only
    (`preserved/consumer-b.v24-output.manifest.json`).
- The standard library and `jsonschema`/`referencing` in
  `/tmp/opensip-architecture-review-env/bin/python -I -B`, invoked through
  `python3` subprocess wrappers.

**Not read or used.** Harness files beside the charter (launch.py, prompt.md,
preparation.json, process.json, public-events.jsonl), LIVE, coauthor or reference
implementations, other consumer or root artifacts, the web, private or session logs,
and agents. No root replay result, diagnostic, expected answer or corrected export
was supplied, and none was used.

**Prior history is immutable.** The original consumer-b.v24 and source39.v1 results
stay as recorded. The source39.v1 MUST **s39-M1** (U-4b assigns no tsjs `unitKind`
while `UnitMembershipV1` enters PlanId) is carried unchanged as CHANGES_REQUIRED.
This session does not invent the missing mapping.

**Order of work.**
1. Preserve v1 bytes (`port_and_preserve.py`).
2. Self-check the prior exported bytes with the unchanged ported code
   (`tools/selfcheck_prior.py` → `selfcheck/pre-summary.json`).
3. Build an independent schema- and registry-driven retained-closure walker
   (`tools/reference_census.py`, `ref/retained_graph.py`) and measure every v1 store
   before any correction.
4. Correct only helper defects derived from the kit (HC-33 onward, pre/post preserved).
5. Re-execute the phase chain from phase 0 with complete raw exports.
6. Construct independent retention/reference-class negatives with first refusal and
   masking.
7. Write checkpoints 0–11, requirement status, and blind-review md/json.

**Not claimed.** Product readiness, commit/push, application, and any future
qualification (real OS/compiler/crypto/SQLite, host authentication, synthetic TCB).
