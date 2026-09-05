# Host foundation design evidence v1

Author: Codex distribution-fixtures agent. Proposed evidence for the lead-authored
`host-foundation-completion.v1.md`; this is not an independent review of that
document, a live register application, product code, or product qualification.

The retained replay passes **210/210 checks**: 182 input/expected cases, ten
source pins, and eighteen schema/contract joins. All inputs and expectations are
in `host-foundation-cases.v1.json`; the checker retains actual results. Expected
outcomes are authored separately from the model, which performs strict parsing,
schema validation, precedence resolution, sorting, temporary-file reads and,
where `solverExecuted` is true, the independently reviewed dependency search.
No expected result is used by the model. Reports contain no temporary absolute
paths or timestamps. The schema's carrier-specific `$defs` must be selected by
the host; its top-level union describes user file documents only.

| Finding / gates | Concrete evidence and boundary |
|---|---|
| WA-4 / G18 | `root-*`, `pkg-*`, `tar-*`: separate payload/account-state roots; OS executable/account observations override hostile argv/PATH/HOME/XDG; shared core and separate accounts; tar user ownership versus package root ownership; private operational state; unsafe ancestor, symlink, wrong owner, writable and setuid observations refuse; read-only absence has no creation. Root initialization effect names are a reference plan, not an executed publication or fencing claim. |
| WA-11 / G12, G18 | `project-*`, `search-*`: real temporary directory search chooses nearest regular marker or explicit root; no match uses cwd; help/version/core doctor have zero search reads; native APFS/ext4 identity observations admit, unsupported/locality/birth cases refuse with the prescribed projection; I/O failure remains distinct; changed incarnation quarantines. The same retained object remains the same identity across a native-observed rename; lifecycle v2 separately owns registry path update and fencing. |
| WA-12 / G12, G18 | Configuration cases exercise the six-layer order, atomic budgets, exact scope restrictions, fixed profile/capabilities, empty pin/hold clearing, whole-array replacement, preserved winning values/order/provenance, and separate canonical resolver projection. CI and non-TTY cases use malformed, directory and dangling-symlink L4 fixtures and record no L4 lstat/open/read. `doctor-same-config-no-analysis` uses the same reader and has no analysis admission or effects. |
| WA-12 numeric / G12, G18 | `strict-*`, `file-byte-bound-*`, `array-bound-*`, `budget-*`: 4 MiB equals/one-over, 32 container levels equals/one-over, 128 item arrays equals/one-over, integer work budget bounds, canonical positive ASCII flag grammar, strict UTF-8/duplicate/surrogate/nonfinite/trailing/unknown-member refusals. Parser-depth positives exercise the parser independently; the closed preview schema permits fewer nested semantic structures. |
| WA-12 resolver / G18 | `resolver-dangling-*` and `resolver-dependency-only-*` call selection v3 using its pinned admitted-input fixture index. Dependency-only pins/holds are allowed when the dependency is in the resolved closure; unrelated pins/holds refuse. Shape/precedence boundary cases do not manufacture a 128-release admitted index: they end at configuration resolution, explicitly before dependency admission. |
| WA-13 / G09, G12, G18 | `policy-*`: only host-owned global or registered-namespace file paths are read; repository candidates/caller project keys are not sources; absent policy is explicit empty deny-by-absence; scope/closure/mode/leaf symlink failures refuse; held-fence precondition refuses before reads; real atomic replacement with restored mtime produces a newly read digest. No policy file creates a GRANT. |
| G03 / G04 | `search-zero-read-*` and the pinned doctor/cache contract preserve no-project help/version/core-doctor isolation. No process, timing or RSS qualification is claimed here. |

`configuration.status == ACCEPT` means only the selected configuration carrier
and its resolution succeeded. `completionStage` is `CONFIGURATION-ONLY`,
`analysisAdmitted` is always false, and `solverExecuted` states whether the
reviewed selection model was additionally invoked. Winning arrays are preserved
verbatim as parsed values and ordering; sorting occurs only in
`resolverProjection`, after duplicate-ID detection. This does not create a
sealed PlanId, live component lock, project namespace or authority.

Native account, executable identity, ownership, filesystem and project birth
observations are injected reference inputs. The model does not implement
`getpwuid_r`, native executable discovery, `statx`, retained-handle races or
durable lifecycle locking. Real temporary files exercise reader behavior on the
review machine only. The root observation interpreter requires the complete
trusted chain as its input; it does not discover that chain. The policy adapter
checks the leaf no-follow/private-owner mode while ancestor custody and the held
fence are explicit trusted observations. The lifecycle v2 unit and eventual
G18 platform qualification own those physical guarantees.

Policy carrier validation and canonical bytes deliberately reuse **frozen
security v2**, whose policy carrier is unchanged in the in-progress security v3
successor. Each `snapshots[].digest` is the domain-separated digest of that
individual file using `opensip.metadata.policy.1`; it is **not** the combined
effective `permissionPolicyDigest` for global/project permission evaluation.
The final security v3 combination/broker/journal join is separate. Empty-policy
canonical bytes and these per-file digests are retained in the report.

The parent normative document is pinned as a dependency, not frozen as an
authored subject of this unit. The evidence freeze lists only this agent's
schema, model, cases, checker, report and notes. An independent reviewer must
review these bytes before an application can cite them as accepted evidence.

Replay with Python 3.12 and jsonschema 4.25.1:

```sh
/tmp/opensip-architecture-review-env/bin/python docs/coop/completion/host-foundation-check.v1.py --report /tmp/host-foundation-replay.v1.json
cmp docs/coop/completion/host-foundation-report.v1.json /tmp/host-foundation-replay.v1.json
```

The reference environment path is a review setup convenience, not a product
toolchain path. An equivalent environment with the pinned dependencies works.
