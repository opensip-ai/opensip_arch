# Proposed new evaluator3 Plan admission

This is an unaccepted joint09 successor of feature02 S2 and native section10.
It completes the reference binding that feature02 left open. It does not mint
Plans or implement storage, and it never runs during retained Run closure.

A NEW evaluator3 analysis Plan uses `new_plan_admission.bind(...).admit_new_plan`.
Its native and identity dependencies are private, selected host dependencies;
caller-supplied modules or registry dictionaries are not runtime authority.
The binding executes the unchanged native `admit_analysis_spec` function with
its `IM` dependency bound to the composed identity-model.v3 and registry. It
preserves the original order: actual-array cardinality, generic schema, closed
native capability vocabulary, then at-most-one parameter per registered row.
The legacy v2 registry does not recognize the new parameter and therefore
cannot enforce that final condition; the selected v3 registry does.

After these checks, execute feature02's unchanged new-Plan recognition duty.
If any requested language mode maps to TypeScript or Rust, exactly one parameter
must resolve to `foundation/framework-recognition-plan.schema.v1.json`. Keep
its raw schema bytes identical to the frozen feature02 owner so that its selected
schemaDigest does not change through JSON pretty-printing. Existing parameter
payload admission, snapshot/unit/recognition joins and retained-byte custody
remain mandatory before a host can construct a Plan; this spec-level helper
alone does not perform those operations. A syntax-only Plan does not acquire a
new recognition requirement.

A missing required parameter raises the internal key
`native.framework-recognition-parameter-required`. It is origin-dependent,
so no context-free internal alias is registered. For a known externally supplied
new-Plan spec, the existing request-rejected / REQUEST.PRECONDITION_FAILED law
uses one new public detail of that name with a parameter-specific remedy.
For a host-generated internal layer, it is operational-failed /
SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant; the failure envelope uses the
existing HOST.INVARIANT_VIOLATED detail. The host supplies the origin. An absent
or impossible origin refuses; the guard cannot infer it from the malformed spec.
No generic capability-name remedy is reused for a missing recognition parameter.
All existing native routes keep their old emitted values.

The new route belongs to the composed common4 StepTermination vocabulary used
by invocation5/envelope7. The legacy common schema does not support its new
public detail and is not a valid substitute at this boundary. Select the native
route registry, common vocabulary, public-detail registry, identity registry,
parameter bytes and both source bindings together. Do not separately publish
one side of the change.

Retained `close_run` and `open_run_closure` remain unchanged. The parameter row
is optional there, and historical Runs without it retain their identities and
read as not-plan-bound. The new-Plan guard mints nothing for a refused step;
it does not erase an earlier step's committed results or availability. Product
workflow settlement must preserve those records under the existing owners.

`check_new_plan.py` executes actual native helpers, selected identity parameter
lookup/cardinality, the appended feature duty, complete public refusal envelopes,
and every existing native public-route branch. `check_identity_integration.py`
separately executes actual reference retained/new Run closure and missing-byte
refusal. Fixtures and dependency objects remain synthetic. These checks do not
qualify compiler execution, default Plan construction, private runtime custody,
source selection, live processes or release gates, and no actual joint review
has occurred yet.
