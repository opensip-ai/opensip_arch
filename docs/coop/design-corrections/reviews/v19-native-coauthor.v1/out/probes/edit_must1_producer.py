"""CB7-MUST-1 (3/4): the producer admission boundary + close_run passing the owning dialect."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')

# --- native producer boundary -------------------------------------------------------------
P = W / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
s = P.read_text(encoding='utf-8')

SIG = '''def admit_coverage_result_v3(payload: dict, scope_descriptor: dict, unresolved_facts: list[dict],
                             payload_schema_digest: str | None = None) -> dict:'''
SIG_NEW = '''def admit_coverage_result_v3(payload: dict, scope_descriptor: dict, unresolved_facts: list[dict],
                             payload_schema_digest: str | None = None,
                             universe_dialect: dict | None = None) -> dict:'''
assert s.count(SIG) == 1
s = s.replace(SIG, SIG_NEW)

DOC = '''    commitment can neither invent the
    commitment nor pick the partition it is judged against.'''
HOOK = '''    refusals.extend(deficiency_cause_faults(entry))
'''
HOOK_NEW = '''    refusals.extend(deficiency_cause_faults(entry))
    # CB7-MUST-1 at the PRODUCER boundary. `universe_dialect` is the `languageVersionBinding.dialect`
    # of the universe the scope names, supplied by the caller that holds the retained universe record
    # - the reference producer and Run closure both do. It is CONTEXT, not payload: nothing here is
    # read from `payload`, so a provider cannot switch its own capability on by asserting a flag.
    #
    # This boundary judges ONE record and never sees the snapshot, so it applies the law only where
    # the scope carries its own paths: a `source-path` subject kind under a body-dialect relation.
    # The `symbol` branch needs the committed inventory and is therefore decided at Run closure by
    # `coverage_source_variant_prerequisite`, which is unconditional and does not depend on any
    # caller passing anything. A caller that supplies no dialect gets today's behaviour here and the
    # closure guard still refuses; that is the honest extent of this particular boundary.
    dialect_row = IM.RELATIONS.get(scope_descriptor["relation"]) or {}
    if (universe_dialect is not None and "bodyIdentityJoin" in dialect_row
            and dialect_row.get("subjectKind") == "source-path"):
        owed = source_variant_capability_support(
            universe_dialect, scope_descriptor["relation"], scope_descriptor["resolution"],
            list(scope_descriptor["subjects"]), True)
        if owed is not None:
            label = scope_descriptor["relation"] + "@" + scope_descriptor["resolution"]
            if entry["coverage"] == "complete":
                refusals.append("native.coverage-source-variant-unsupported-complete:" + label
                                + ":" + owed["nativeCause"])
            if entry.get("deficiency") != owed["deficiency"]:
                refusals.append("native.coverage-source-variant-deficiency-mismatch:" + label
                                + ":expected=" + owed["deficiency"] + ":declared=" + str(entry.get("deficiency")))
            if entry.get("nativeCause") != owed["nativeCause"]:
                refusals.append("native.coverage-source-variant-cause-mismatch:" + label
                                + ":expected=" + owed["nativeCause"] + ":declared=" + str(entry.get("nativeCause")))
'''
assert s.count(HOOK) == 1
s = s.replace(HOOK, HOOK_NEW)
P.write_text(s, encoding='utf-8')

# --- close_run supplies it ----------------------------------------------------------------
Q = W / 'docs/coop/design-corrections/foundation/identity-model.py'
t = Q.read_text(encoding='utf-8')
OLD = """            admitted=native_admission().admit_coverage_result_v3(coverage_payload,scope,unresolved,coverage['payloadSchemaDigest'])"""
NEW = """            # The owning universe's own dialect spec is handed to the producer boundary so the
            # SAME derivation runs there, on the same inputs, before closure re-derives it below.
            # It is looked up from the retained universe record, never from the coverage payload.
            _scope_dialect=(native_universes[scope['sourceUniverse']][2].get('languageVersionBinding',{})
                            .get('dialect') if scope['sourceUniverse'] in native_universes else None)
            admitted=native_admission().admit_coverage_result_v3(coverage_payload,scope,unresolved,coverage['payloadSchemaDigest'],_scope_dialect)"""
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)
Q.write_text(t, encoding='utf-8')
print('ok')
