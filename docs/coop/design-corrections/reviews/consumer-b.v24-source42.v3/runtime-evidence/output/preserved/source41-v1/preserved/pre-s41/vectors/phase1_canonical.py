"""Phase 1: C/H helper, CVE1 eight types, raw lexical admission, raw-vs-parsed, semantic-vs-operational,
acyclic source->Plan->View->Proof->Evidence->Seal->Run joins.

Every vector is independently authored here; nothing is copied from a kit example. Classification per
vector: valid | invalid | explanatory (R-VALID-VS-INVALID-VS-EXPLANATORY).
"""
import hashlib
import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output/preserved/pre-s41/ref')
sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output/preserved/pre-s41/tools')
import canonical as K
import cve1
import schemas
import status as S
from jsonschema import Draft202012Validator

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
failures = []


def check(cond, label):
    if not cond:
        failures.append(label)
    return bool(cond)


def refusal(fn):
    try:
        fn()
        return None
    except K.AdmissionError as exc:
        return exc.boundary
    except cve1.CVE1Error as exc:
        return exc.code


# ------------------------------------------------------------------ R-H-HELPER
h_vectors = []
d_scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}
c = K.C(d_scope)
fr = K.frame("subject-scope", {"k": 1})
h_vectors.append({"class": "valid", "name": "scope-descriptor canonical bytes", "descriptor": d_scope,
                  "C_utf8": c.decode(), "rawSha256": hashlib.sha256(c).hexdigest(),
                  "schema": KIT.admit(d_scope, ID, "#/$defs/scope-descriptor")["ok"]})
h_vectors.append({"class": "valid", "name": "H frame layout", "domain": "subject-scope", "descriptor": {"k": 1},
                  "frameHex": fr.hex(), "H": K.H("subject-scope", {"k": 1}),
                  "check_sha256_frame_equals_H": hashlib.sha256(fr).hexdigest() == K.H("subject-scope", {"k": 1}),
                  "rawPayloadSha256": hashlib.sha256(K.C({"k": 1})).hexdigest(),
                  "rawPayloadDiffersFromH": hashlib.sha256(K.C({"k": 1})).hexdigest() != K.H("subject-scope", {"k": 1})})
check(h_vectors[-1]["check_sha256_frame_equals_H"] and h_vectors[-1]["rawPayloadDiffersFromH"], "H frame")
# key order by UTF-8 bytes including non-BMP, escaping, no normalization
kv = {"\U0001F600": 1, "￿": 2, "a": 3, "B": 4, "é": 5}
cb = K.C(kv)
h_vectors.append({"class": "valid", "name": "UTF-8 byte key order incl non-BMP", "C_utf8": cb.decode(),
                  "C_hex": cb.hex(), "keyOrder": [k for k in json.loads(cb)],
                  "note": "UTF-16 code-unit order would place U+1F600 (D83D..) before U+FFFF; UTF-8 byte order places it after."})
check([k for k in json.loads(cb)] == ["B", "a", "é", "￿", "\U0001F600"], "key order")
esc = {"s": "q\"b\\s/\b\t\n\f\r\x01\x1f\x7f é"}
ce = K.C(esc)
h_vectors.append({"class": "valid", "name": "string escaping", "C_utf8": ce.decode(), "C_hex": ce.hex()})
check(ce.decode() == '{"s":"q\\"b\\\\s/\\b\\t\\n\\f\\r\\u0001\\u001f\x7f é"}', "escaping")
nfc, nfd = {"t": "é"}, {"t": "é"}
h_vectors.append({"class": "explanatory", "name": "no Unicode normalization", "nfcHex": K.C(nfc).hex(), "nfdHex": K.C(nfd).hex(),
                  "H_nfc": K.H("subject-scope", nfc), "H_nfd": K.H("subject-scope", nfd)})
check(K.H("subject-scope", nfc) != K.H("subject-scope", nfd), "NFC vs NFD distinct")
bounds = {"min": -(2 ** 63), "max": 2 ** 64 - 1}
h_vectors.append({"class": "valid", "name": "integer boundaries", "C_utf8": K.C(bounds).decode()})
h_vectors.append({"class": "invalid", "name": "integer above range (typed)", "firstRefusal": refusal(lambda: K.C({"x": 2 ** 64})), "masksLater": False})
h_vectors.append({"class": "invalid", "name": "integer below range (typed)", "firstRefusal": refusal(lambda: K.C({"x": -(2 ** 63) - 1})), "masksLater": False})
deep_ok = {}
cur = deep_ok
for _ in range(31):
    cur["n"] = {}
    cur = cur["n"]
deep_bad = {"n": deep_ok}
h_vectors.append({"class": "valid", "name": "nesting depth 32 admitted", "refusal": refusal(lambda: K.C(deep_ok))})
h_vectors.append({"class": "invalid", "name": "nesting depth 33 refused", "firstRefusal": refusal(lambda: K.C(deep_bad)), "masksLater": False})
check(refusal(lambda: K.C(deep_ok)) is None and refusal(lambda: K.C(deep_bad)) == "TYPED_DEPTH", "depth")
big = {"s": "a" * (4 * 1024 * 1024)}
h_vectors.append({"class": "invalid", "name": "descriptor over 4 MiB", "firstRefusal": refusal(lambda: K.C(big)), "masksLater": False})
check(refusal(lambda: K.C(big)) == "C_DESCRIPTOR_TOO_LARGE", "4MiB")
# frame admission negatives
h_vectors.append({"class": "invalid", "name": "raw payload offered where frame required",
                  "firstRefusal": refusal(lambda: K.parse_frame(K.C({"k": 1}), {"subject-scope"})), "masksLater": False})
h_vectors.append({"class": "invalid", "name": "frame domain outside named set",
                  "firstRefusal": refusal(lambda: K.parse_frame(fr, {"fact"})), "masksLater": False})
tampered = bytearray(fr)
tampered[-2] = ord('2')
h_vectors.append({"class": "invalid", "name": "frame body altered (digest no longer the claimed H)",
                  "claimedH": K.H("subject-scope", {"k": 1}), "actualSha256": hashlib.sha256(bytes(tampered)).hexdigest(),
                  "parse": refusal(lambda: K.parse_frame(bytes(tampered), {"subject-scope"})),
                  "firstRefusal": "CAS_DIGEST_MISMATCH (store key != sha256(bytes))", "masksLater": False})
nc = K.PRODUCT_TAG + b"\x00subject-scope\x00" + (8).to_bytes(8, 'big') + b'{ "k":1}'
h_vectors.append({"class": "invalid", "name": "frame body not canonical", "firstRefusal": refusal(lambda: K.parse_frame(nc, {"subject-scope"})), "masksLater": False})
check(refusal(lambda: K.parse_frame(nc, {"subject-scope"})) == "FRAME_NOT_CANONICAL", "frame canonical")

# ------------------------------------------------------------------ R-CVE1-EIGHT-TYPES
cve_vectors = []
samples = [("null", None), ("false", False), ("true", True), ("unsigned-64", 0), ("unsigned-64", 2 ** 64 - 1),
           ("negative-signed-64", -1), ("negative-signed-64", -(2 ** 63)), ("NFC-UTF8-string", "café"),
           ("array", [1, "a", None]), ("string-keyed-map", {"b": 1, "a": [True]})]
for t, v in samples:
    enc = cve1.encode(v)
    dec = cve1.decode(enc)
    same = type(dec) is type(v) and dec == v
    cve_vectors.append({"class": "valid", "type": t, "value": v, "hex": enc.hex(), "decoded": dec,
                        "roundTrip": same and cve1.encode(dec) == enc})
    check(same and cve1.encode(dec) == enc, f"cve1 {t}")
for name, fn in [("u64 overflow", lambda: cve1.encode(2 ** 64)), ("i64 underflow", lambda: cve1.encode(-(2 ** 63) - 1)),
                 ("float", lambda: cve1.encode(1.0)), ("bytes", lambda: cve1.encode(b"x")),
                 ("non-NFC string", lambda: cve1.encode("é")),
                 ("decode trailing bytes", lambda: cve1.decode(b"\x00\x00")),
                 ("decode unknown tag", lambda: cve1.decode(b"\x08")),
                 ("decode non-NFC", lambda: cve1.decode(b"\x04\x00\x00\x00\x03e\xcc\x81")),
                 ("decode unsorted map", lambda: cve1.decode(cve1.encode("b").join([b"\x06\x00\x00\x00\x02", b"\x00"]) + cve1.encode("a") + b"\x00")),
                 ("decode duplicate map key", lambda: cve1.decode(b"\x06\x00\x00\x00\x02" + cve1.encode("a") + b"\x00" + cve1.encode("a") + b"\x00")),
                 ("decode non-canonical 07 non-negative", lambda: cve1.decode(b"\x07" + (5).to_bytes(8, 'big'))),
                 ("decode truncated", lambda: cve1.decode(b"\x03\x00\x01"))]:
    r = refusal(fn)
    cve_vectors.append({"class": "invalid", "name": name, "firstRefusal": r, "masksLater": False})
    check(r is not None, f"cve1 negative {name}")

# ------------------------------------------------------------------ R-LEXICAL-ADMISSION / R-RAW-VS-PARSED
lex = []
raw_cases = [
    ("float token", b'{"schemaVersion":2.0}', "LEX_FLOAT_OR_EXPONENT"),
    ("exponent token", b'{"schemaVersion":2e0}', "LEX_FLOAT_OR_EXPONENT"),
    ("negative zero", b'{"n":-0}', "LEX_NEGATIVE_ZERO"),
    ("NaN", b'{"n":NaN}', "LEX_NONFINITE"),
    ("Infinity", b'{"n":-Infinity}', "LEX_NONFINITE"),
    ("integer above u64", b'{"n":18446744073709551616}', "LEX_INTEGER_RANGE"),
    ("integer below i64", b'{"n":-9223372036854775809}', "LEX_INTEGER_RANGE"),
    ("duplicate key", b'{"a":1,"a":1}', "LEX_DUPLICATE_KEY"),
    ("duplicate key with different value", b'{"a":1,"a":2}', "LEX_DUPLICATE_KEY"),
    ("lone surrogate escape", b'{"s":"\\ud800"}', "LEX_NON_SCALAR_UNICODE"),
    ("UTF-8 encoded surrogate bytes", b'{"s":"\xed\xa0\x80"}', "LEX_MALFORMED_UTF8"),
    ("malformed UTF-8", b'{"s":"\xff"}', "LEX_MALFORMED_UTF8"),
    ("float before duplicate (masking)", b'{"a":1.5,"a":2}', "LEX_FLOAT_OR_EXPONENT"),
]
for name, raw, want in raw_cases:
    got = refusal(lambda raw=raw: K.parse_raw(raw))
    masks = name.endswith("(masking)")
    lex.append({"class": "invalid", "boundary": "raw-input", "name": name, "rawHex": raw.hex(), "firstRefusal": got,
                "expectedByLaw": want, "masksLater": masks,
                "maskedCheck": "LEX_DUPLICATE_KEY (tokenizer reaches the float before the object pairs are complete)" if masks else None})
    check(got == want, f"lex {name}")
# string bound on raw input, counted in Unicode scalars against a Text (maxLength 4096) field
text4096 = "\U0001F600" * 4096
text4097 = "\U0001F600" * 4097
for name, s, ok in [("Text 4096 non-BMP scalars (16384 UTF-8 bytes)", text4096, True), ("Text 4097 scalars", text4097, False)]:
    raw = ('{"schemaVersion":2,"workspaceRoots":["' + s + '"],"pathPrefixes":[],"excludedPathPrefixes":[]}').encode()
    val = K.parse_raw(raw)
    res = KIT.admit(val, ID, "#/$defs/scope-descriptor")
    lex.append({"class": "valid" if ok else "invalid", "boundary": "raw-input then schema string bound", "name": name,
                "utf8Bytes": len(s.encode()), "scalars": len(s), "admitted": res["ok"],
                "firstRefusal": None if res["ok"] else "SCHEMA_MAXLENGTH(scalars)", "masksLater": False})
    check(res["ok"] == ok, f"string bound {name}")
# end-anchored identifier grammar vs historical bare-$ provenance selector
exec_nl = "exec1_" + "0" * 32 + "\n"
succ = KIT.stock_errors({"k": exec_nl}, "workflows/schemas/evaluator3/common.schema.json", "#/$defs/ExecutionId") if False else None
succ_ok = Draft202012Validator({"type": "string", "pattern": "^exec1_[0-9a-f]{32}(?![\\s\\S])"}).is_valid(exec_nl)
c2 = KIT.doc("coop/artifacts/c2-plan-stage-schema.v4.json")
c2_pattern = c2['planIntent']['wireTypes']['executionId'].get('pattern') if isinstance(c2['planIntent']['wireTypes']['executionId'], dict) else None
import re
hist_ok = bool(re.search(c2_pattern, exec_nl)) if c2_pattern else None
common_ok = KIT.admit(exec_nl, "workflows/schemas/evaluator3/common.schema.json", "#/$defs/ExecutionId")["ok"]
lex.append({"class": "invalid", "boundary": "schema pattern (end anchor)", "name": "exec1_ with trailing newline",
            "successorGrammarAdmits": succ_ok, "commonSchemaAdmits": common_ok,
            "historicalC2Pattern": c2_pattern, "historicalPatternAdmits(provenance only)": hist_ok,
            "firstRefusal": "SCHEMA_PATTERN_END_ANCHOR", "masksLater": False})
check(succ_ok is False and common_ok is False, "exec1 newline refused")

raw_vs_parsed = []
logical = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}
floaty_raw = b'{"schemaVersion":2.0,"workspaceRoots":["."],"pathPrefixes":[],"excludedPathPrefixes":[]}'
floaty_parsed = dict(logical, schemaVersion=2.0)
bool_parsed = dict(logical, schemaVersion=True)
stock_float = Draft202012Validator({"const": 2}).is_valid(2.0)
raw_vs_parsed.append({"class": "invalid", "name": "2.0 as raw token", "boundary": "raw-input",
                      "firstRefusal": refusal(lambda: K.parse_raw(floaty_raw)), "masksLater": True,
                      "maskedCheck": "schema const=2 (never reached)"})
raw_vs_parsed.append({"class": "invalid", "name": "2.0 already-parsed object", "boundary": "typed-object",
                      "stockJsonSchemaConst2AdmitsFloat": stock_float,
                      "firstRefusal": KIT.admit(floaty_parsed, ID, "#/$defs/scope-descriptor")["typed"], "masksLater": False})
raw_vs_parsed.append({"class": "invalid", "name": "true for const 2 (parsed)", "boundary": "schema",
                      "admit": KIT.admit(bool_parsed, ID, "#/$defs/scope-descriptor"), "masksLater": False})
plain = json.loads('{"a":1,"a":2}')
raw_vs_parsed.append({"class": "explanatory", "name": "unhooked decoder silently keeps last duplicate",
                      "stdlibJsonLoadsResult": plain, "rawAdmission": refusal(lambda: K.parse_raw(b'{"a":1,"a":2}')),
                      "why": "after decode the duplicate is unobservable, so duplicate refusal must run on raw bytes"})
check(stock_float is True, "stock jsonschema admits 2.0 for const 2 (measured)")
check(raw_vs_parsed[1]["firstRefusal"] == "TYPED_FLOAT:2.0", "typed float")
check(raw_vs_parsed[2]["admit"]["ok"] is False, "bool const")

# ------------------------------------------------------------------ R-SEMANTIC-VS-OPERATIONAL and R-ACYCLIC-JOINS
PRJ = "prj1-" + "a1" * 32
inv = [{"path": "src/a.rs", "sha256": hashlib.sha256(b"fn a(){}\n").hexdigest(), "bytes": 9}]
sem_cfg = {"analysis": {"profileId": "default", "capabilities": ["inventory"], "budget": {"unit": "work-units", "limit": 1000}},
           "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": K.raw_digest(inv)}


def chain(inventory, budget_limit, extra_receipt_exec):
    cfg = json.loads(json.dumps(sem_cfg))
    cfg["analysis"]["budget"]["limit"] = budget_limit
    v = dict(vcs, sourceInventoryDigest=K.raw_digest(inventory))
    snap = {"schemaVersion": 2, "projectId": PRJ, "sourceInventory": inventory, "resolvedConfigDigest": K.raw_digest(cfg),
            "scopeDigest": K.raw_digest(d_scope), "vcsDigest": K.raw_digest(v)}
    snapshot_id = K.identifier("snapshot", snap)
    spec = {"schemaVersion": 2, "requestedCapabilities": [], "policyPackIds": [], "parameters": []}
    grant = {"schemaVersion": 2, "projectId": PRJ, "principals": [], "analysisOperations": ["read-source"], "scopeDigest": K.raw_digest(d_scope)}
    plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": "c" * 64, "semanticClosures": [],
            "analysisSpecDigest": K.raw_digest(spec), "resolvedConfigDigest": K.raw_digest(cfg), "nativeContextDigests": [],
            "importIds": [], "policyDigest": "d" * 64, "waiverDigest": "e" * 64, "scopeDigest": K.raw_digest(d_scope),
            "budget": {"unit": "work-units", "limit": budget_limit}, "semanticGrantDigest": K.raw_digest(grant),
            "capabilityManifestBytesDigest": "f" * 64}
    plan_id = K.identifier("plan", plan)
    closure = "closure2:" + "1" * 64
    view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": [], "facts": [], "coverageIds": [], "producerClosure": closure, "schemaDigests": []}
    view_id = K.identifier("view", view)
    xplan = {"schemaVersion": 2, "planId": plan_id, "stages": []}
    xplan_id = K.identifier("execution-plan", xplan)
    proof = {"schemaVersion": 3, "planId": plan_id, "executionPlanId": xplan_id, "evaluatorClosure": closure, "ruleProgramDigest": "2" * 64,
             "evaluationInputRefs": [{"domain": "view", "digest": K.strip_prefix(view_id)}], "predicateProofs": [], "findingIds": [],
             "verdict": "pass", "evaluationState": "evaluated", "ruleResults": [], "waivedFindingIds": [], "executionDeficiencies": [],
             "executionInputsDigest": "3" * 64}
    proof_id = K.identifier("proof-bundle", proof)
    evidence = {"schemaVersion": 3, "planId": plan_id, "viewIds": [view_id], "coverageIds": [], "importIds": [], "findingIds": [], "proofBundleId": proof_id}
    evidence_id = K.identifier("semantic-evidence", evidence)
    seal = {"schemaVersion": 3, "planId": plan_id, "executionPlanId": xplan_id, "evidenceId": evidence_id, "evaluatorClosure": closure,
            "policyDigest": "d" * 64, "proofBundleId": proof_id, "verdict": "pass"}
    seal_id = K.identifier("evaluation-seal", seal)
    run = {"schemaVersion": 3, "projectId": PRJ, "snapshotId": snapshot_id, "planId": plan_id, "evidenceId": evidence_id,
           "evaluationSealId": seal_id, "capabilityManifestId": "c" * 64}
    run_id = K.identifier("run", run)
    receipt = {"schemaVersion": 2, "runId": run_id, "executionId": extra_receipt_exec, "namespaceId": "ns-local-1", "commitSequence": 7,
               "inventoryDigest": "4" * 64, "sealedAssurance": "replayable", "signerKeyId": "host-key-1"}
    recs = {"snapshot": snap, "plan": plan, "view": view, "execution-plan": xplan, "proof-bundle": proof, "semantic-evidence": evidence,
            "evaluation-seal": seal, "run": run, "commit-receipt": receipt}
    ids = {"snapshot": snapshot_id, "plan": plan_id, "view": view_id, "execution-plan": xplan_id, "proof-bundle": proof_id,
           "semantic-evidence": evidence_id, "evaluation-seal": seal_id, "run": run_id,
           "commit-receipt(operational, raw C digest)": K.raw_digest(receipt)}
    return recs, ids


base_recs, base = chain(inv, 1000, "exec1_" + "0" * 31 + "1")
schema_results = {k: KIT.admit(v, ID, f"#/$defs/{k}")["ok"] for k, v in base_recs.items()}
check(all(schema_results.values()), "chain schema validity")
_, op_changed = chain(inv, 1000, "exec1_" + "0" * 31 + "2")
inv2 = [dict(inv[0], sha256=hashlib.sha256(b"fn a(){ }\n").hexdigest(), bytes=10)]
_, sem_changed = chain(inv2, 1000, "exec1_" + "0" * 31 + "1")
_, budget_changed = chain(inv, 1001, "exec1_" + "0" * 31 + "1")
sem_vs_op = {
    "class": "explanatory",
    "note": "Identity-dependency vector over schema-valid descriptors built by the published recipes; NOT a claimed complete Run (no replay).",
    "schemaValidity": schema_results,
    "baseline": base,
    "operationalExecutionIdChange": {"changed": {k: base[k] != op_changed[k] for k in base},
                                     "runIdEqual": base["run"] == op_changed["run"]},
    "semanticSourceByteChange": {"changed": {k: base[k] != sem_changed[k] for k in base},
                                 "runIdEqual": base["run"] == sem_changed["run"]},
    "semanticBudgetChange": {"changed": {k: base[k] != budget_changed[k] for k in base}, "runIdEqual": base["run"] == budget_changed["run"]},
}
check(sem_vs_op["operationalExecutionIdChange"]["runIdEqual"] is True, "operational change keeps run")
check(sem_vs_op["operationalExecutionIdChange"]["changed"]["commit-receipt(operational, raw C digest)"] is True, "receipt differs")
check(sem_vs_op["semanticSourceByteChange"]["runIdEqual"] is False, "semantic change moves run")
check(sem_vs_op["semanticBudgetChange"]["changed"]["snapshot"] is True and sem_vs_op["semanticBudgetChange"]["runIdEqual"] is False, "budget change")
# operational configuration fields never enter semantic-configuration
op_cfg_extra = dict(sem_cfg, ui={"color": "never"})
sem_vs_op["uiFieldInSemanticConfiguration"] = {"admit": KIT.admit(op_cfg_extra, ID, "#/$defs/semantic-configuration")["ok"],
                                               "why": "semantic-configuration is closed over analysis/components/discovery/policy/evidence; UI/retention are operational (admission s1.1)"}
check(sem_vs_op["uiFieldInSemanticConfiguration"]["admit"] is False, "ui refused in semantic config")

# acyclic joins: dependency edges read from the records themselves
refs = {
    "snapshot": [], "plan": ["snapshot"], "view": ["plan"], "execution-plan": ["plan"],
    "proof-bundle": ["plan", "execution-plan", "view"], "semantic-evidence": ["plan", "view", "proof-bundle"],
    "evaluation-seal": ["plan", "execution-plan", "semantic-evidence", "proof-bundle"],
    "run": ["snapshot", "plan", "semantic-evidence", "evaluation-seal"]}


def has_cycle(g):
    color = {}

    def dfs(n):
        color[n] = 1
        for m in g.get(n, []):
            if color.get(m) == 1 or (color.get(m) is None and dfs(m)):
                return True
        color[n] = 2
        return False
    return any(color.get(n) is None and dfs(n) for n in g)


acyclic = {"class": "valid", "edges": refs, "cycle": has_cycle(refs), "ids": base, "negatives": []}
check(not acyclic["cycle"], "acyclic")
neg_proof = dict(base_recs["proof-bundle"], evidenceId=base["semantic-evidence"])
r = KIT.admit(neg_proof, ID, "#/$defs/proof-bundle")
acyclic["negatives"].append({"class": "invalid", "name": "proof names EvidenceId (cycle attempt)", "schemaOk": r["ok"],
                             "firstRefusal": "SCHEMA_ADDITIONAL_PROPERTY(evidenceId)" if not r["ok"] else None,
                             "graphCycle": has_cycle(dict(refs, **{"proof-bundle": refs["proof-bundle"] + ["semantic-evidence"]})),
                             "masksLater": True, "maskedCheck": "dependency-graph cycle refusal"})
neg_ref = dict(base_recs["proof-bundle"], evaluationInputRefs=[{"domain": "run", "digest": K.strip_prefix(base["run"])}])
r2 = KIT.admit(neg_ref, ID, "#/$defs/proof-bundle")
acyclic["negatives"].append({"class": "invalid", "name": "proof input ref of domain run", "schemaOk": r2["ok"],
                             "firstRefusal": "SCHEMA_ENUM(ProofInputRef.domain excludes run)" if not r2["ok"] else None, "masksLater": False})
neg_ev = dict(base_recs["semantic-evidence"], runId=base["run"])
r3 = KIT.admit(neg_ev, ID, "#/$defs/semantic-evidence")
acyclic["negatives"].append({"class": "invalid", "name": "evidence names RunId", "schemaOk": r3["ok"],
                             "firstRefusal": "SCHEMA_ADDITIONAL_PROPERTY(runId)" if not r3["ok"] else None, "masksLater": False})
fer = KIT.admit({"domain": "semantic-evidence", "digest": "0" * 64}, ID, "#/$defs/FindingEvidenceRef")
acyclic["negatives"].append({"class": "invalid", "name": "finding evidence ref to evidence3", "schemaOk": fer["ok"],
                             "firstRefusal": "SCHEMA_ENUM(FindingEvidenceRef.domain)" if not fer["ok"] else None, "masksLater": False})
for n in acyclic["negatives"]:
    check(n["schemaOk"] is False, "acyclic negative " + n["name"])

out = {"H_helper": h_vectors, "cve1EightTypes": cve_vectors, "lexicalAdmission": lex, "rawVsParsed": raw_vs_parsed,
       "semanticVsOperational": sem_vs_op, "acyclicJoins": acyclic, "assertionFailures": failures}
S.dump('vectors/phase1-canonical.json', out)
S.dump('vectors/cve1-eight-types.json', cve_vectors)
print(json.dumps({"failures": failures, "counts": {k: len(v) if isinstance(v, list) else 1 for k, v in out.items()}}, indent=1))
sys.exit(1 if failures else 0)
