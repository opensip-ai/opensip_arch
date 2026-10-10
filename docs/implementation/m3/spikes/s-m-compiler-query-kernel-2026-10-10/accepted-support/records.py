"""Case sets and append-only round ledgers, Q0 r13 sections 1 and 3.

These libraries admit records and preserve their history. They perform no
adjudication, scoring, producer execution or qualification.
"""
import fcntl
import os
from pathlib import Path

from canonical import Refusal, canonical, digest, parse, pin, sha256

CASE_KINDS = {"cell-observation", "finding", "refactor-pair", "determinism", "workload", "config-shape"}
ORIGINS = {"oracle-fixture", "validated-seed", "fix-reversal", "negative-lookalike", "curated-differential", "curated-adjudication"}
RECORD_KINDS = {
    "adjudicator", "freeze", "item", "vote", "escalation", "resolution", "carry",
    "calibration-result", "agreement", "drift-audit", "exposure", "supersede",
}
FREEZE_PINS = (
    "caseSetDigest", "ruleSpecSetDigest", "rubricSetDigest", "familyMapDigest",
    "heldOutSetDigest", "metricDefinitionsDigest", "preregistrationDigest",
)
HARD_COMPONENTS = (
    "propositionId", "rubricDigest", "ruleSpecDigest", "ruleProgramDigest",
    "detectorSemanticsMajor", "configurationDigest", "dependencySourceSetId", "preparedOutputSetId",
)


def require(condition, code):
    if not condition:
        raise Refusal(code)


def case_record(record):
    require(type(record) is dict, "CASE_NOT_OBJECT")
    required = {"caseId", "caseKind", "tier", "origin", "heldOut", "inputs", "rule",
                "subject", "requirement", "configuration", "expectedAnswer", "provenance"}
    require(required <= record.keys(), "CASE_FIELDS")
    require(type(record["caseId"]) is str and bool(record["caseId"]), "CASE_ID")
    require(record["caseKind"] in CASE_KINDS, "CASE_KIND")
    require(record["tier"] in ("T1", "T2", "T3"), "CASE_TIER")
    require(record["origin"] in ORIGINS, "CASE_ORIGIN")
    require(type(record["heldOut"]) is bool, "HELD_OUT_TYPE")
    if record["tier"] != "T1":
        require(type(record.get("family")) is str and bool(record["family"]), "CASE_FAMILY")
    for field in ("inputs", "rule", "subject", "requirement", "configuration", "expectedAnswer", "provenance"):
        require(type(record[field]) is dict and bool(record[field]), "CASE_" + field.upper())
    rule = record["rule"]
    require(type(rule.get("ruleId")) is str and bool(rule["ruleId"]) and pin(rule.get("ruleSpecDigest")), "CASE_RULE")
    inputs = record["inputs"]
    if record["tier"] == "T1":
        require(pin(inputs.get("fixtureManifestDigest")), "FIXTURE_MANIFEST")
    else:
        require(type(inputs.get("repository")) is str and bool(inputs["repository"])
                and type(inputs.get("commit")) is str and bool(inputs["commit"])
                and pin(inputs.get("treeDigest")), "CASE_REPOSITORY")
    if record["origin"] == "validated-seed":
        require(pin(inputs.get("controlTreeDigest")) and pin(inputs.get("mutantPatchDigest")), "SEED_PINS")
    answer = record["expectedAnswer"]
    kind = answer.get("kind")
    require(kind in ("determinate-positive", "determinate-negative", "must-abstain"), "EXPECTED_ANSWER")
    if kind == "determinate-positive":
        require(type(answer.get("expectedFinding")) is dict and bool(answer["expectedFinding"]), "EXPECTED_FINDING")
    if kind == "must-abstain":
        require(bool(answer.get("expectedDeficiency")) and type(answer.get("positiveSoundUnderDeficiency")) is bool, "EXPECTED_DEFICIENCY")
    if record["caseKind"] == "cell-observation":
        require(type(record.get("cell")) is dict and bool(record["cell"]), "EXPECTED_CELL")
    body = {k: v for k, v in record.items() if k != "caseDigest"}
    result = dict(body, caseDigest=digest(body))
    require("caseDigest" not in record or record["caseDigest"] == result["caseDigest"], "CASE_DIGEST")
    canonical(result)
    return result


def case_set(records):
    rows = sorted((case_record(r) for r in records), key=lambda r: r["caseId"].encode("utf-8"))
    require(len({r["caseId"] for r in rows}) == len(rows), "DUPLICATE_CASE_ID")
    return b"".join(canonical(r) + b"\n" for r in rows)


def read_cases(raw):
    require(type(raw) is bytes and (not raw or raw.endswith(b"\n")), "CASE_SET_NEWLINE")
    rows = [parse(line) for line in raw.splitlines()]
    require(all("caseDigest" in r for r in rows), "CASE_DIGEST_MISSING")
    require(case_set(rows) == raw, "CASE_SET_NOT_CANONICAL")
    return rows


def read_ledger(raw):
    require(type(raw) is bytes and (not raw or raw.endswith(b"\n")), "LEDGER_NEWLINE")
    rows, seen, prev = [], set(), None
    for line in raw.splitlines():
        record = parse(line)
        require(type(record) is dict and canonical(record) == line, "LEDGER_NOT_CANONICAL")
        require(record.get("recordKind") in RECORD_KINDS, "RECORD_KIND")
        fields = {
            "adjudicator": ("voterId", "kind", "designatedExpert", "conflictedRules"),
            "item": ("itemId", "labelKey", "queue", "calibration", "presentationDigest"),
            "vote": ("itemId", "voterId", "label", "rationale", "triageMillis", "rubricDigest"),
            "escalation": ("itemId", "reason"),
            "resolution": ("itemId", "label", "method", "voteRecords"),
            "carry": ("sourceResolution", "labelKey", "components", "carried"),
            "calibration-result": ("voterId", "items", "correct", "knownFalseLabelledTrue", "passed"),
            "agreement": ("ruleId", "n", "rawAgreementPpm", "kappaPpm", "prevalencePpm", "triggered"),
            "drift-audit": ("ruleId", "sample", "seed", "results", "triggered"),
        }
        kind = record["recordKind"]
        require(all(k in record for k in fields.get(kind, ())), "RECORD_FIELDS")
        if kind == "adjudicator":
            require(record["kind"] in ("human", "agent") and type(record["designatedExpert"]) is bool
                    and type(record["conflictedRules"]) is list and bool(record["voterId"]), "ADJUDICATOR_RECORD")
            if record["kind"] == "agent":
                require(all(type(record.get(k)) is str and bool(record[k])
                            for k in ("modelFamily", "modelId", "contextClass")), "AGENT_REGISTRATION")
        if kind == "item":
            require(type(record["calibration"]) is bool and pin(record["presentationDigest"]), "ITEM_RECORD")
        if kind in ("vote", "resolution"):
            require(record["label"] in ("true", "false", "unclear"), "LABEL_RECORD")
        if kind == "vote":
            require(type(record["triageMillis"]) is int and record["triageMillis"] >= 0
                    and pin(record["rubricDigest"]) and type(record["rationale"]) is str
                    and bool(record["rationale"]), "VOTE_RECORD")
        if kind == "escalation":
            require(record["reason"] in ("disagreement", "unclear-gating"), "ESCALATION_RECORD")
        if kind == "resolution":
            require(record["method"] in ("agreement", "expert")
                    and type(record["voteRecords"]) is list
                    and all(v in seen for v in record["voteRecords"]), "RESOLUTION_RECORD")
            if record["method"] == "expert":
                require(bool(record.get("expertRationale")), "EXPERT_RATIONALE")
        if kind == "carry":
            # The source is commonly in a previous round's ledger. Do not
            # pretend the current chain alone proves its provenance.
            require(pin(record["sourceResolution"]) and type(record["carried"]) is bool
                    and type(record["components"]) is dict, "CARRY_RECORD")
        require(record.get("prevRecordDigest") == prev, "LEDGER_CHAIN")
        body = {k: v for k, v in record.items() if k != "recordDigest"}
        require(record.get("recordDigest") == digest(body), "RECORD_DIGEST")
        if not rows:
            require(record["recordKind"] == "freeze", "ROUND_NOT_FROZEN")
        else:
            require(record["recordKind"] != "freeze", "ROUND_ALREADY_FROZEN")
        if record["recordKind"] == "freeze":
            require(all(pin(record.get(k)) for k in FREEZE_PINS), "FREEZE_PINS")
        if record["recordKind"] == "supersede":
            require(record.get("replaces") in seen and bool(record.get("why")), "SUPERSEDE_REFERENCE")
        if record["recordKind"] == "exposure":
            require(record.get("scope") in ("case", "repository", "family")
                    and type(record.get("subject")) is str and bool(record["subject"])
                    and all(bool(record.get(k)) for k in ("who", "when", "what")), "EXPOSURE_RECORD")
        prev = record["recordDigest"]
        seen.add(prev)
        rows.append(record)
    return rows


def append_record(path, record):
    """Validate the existing chain under an exclusive lock, then append and sync.

    No repair of torn files, replacement, truncation, or update API is provided.
    All writers of one round must use this function.
    """
    path = Path(path)
    flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW | os.O_CLOEXEC
    fd = os.open(path, flags, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        with os.fdopen(os.dup(fd), "rb") as reader:
            raw = reader.read()
        rows = read_ledger(raw)
        require(type(record) is dict and "recordDigest" not in record and "prevRecordDigest" not in record, "CALLER_CHAIN_FIELDS")
        body = dict(record, prevRecordDigest=rows[-1]["recordDigest"] if rows else None)
        result = dict(body, recordDigest=digest(body))
        line = canonical(result) + b"\n"
        read_ledger(raw + line)
        written = 0
        while written < len(line):
            written += os.write(fd, line[written:])
        os.fsync(fd)
        return result
    finally:
        os.close(fd)


def freeze(path, inputs):
    """Digest the seven exact input byte sets; validate the case-set bytes."""
    require(set(inputs) == set(FREEZE_PINS), "FREEZE_INPUTS")
    read_cases(inputs["caseSetDigest"])
    for key, raw in inputs.items():
        require(type(raw) is bytes, "FREEZE_INPUT_BYTES")
        if key != "caseSetDigest":
            require(canonical(parse(raw)) == raw, "FREEZE_INPUT_NOT_CANONICAL")
    return append_record(path, dict(recordKind="freeze", **{key: sha256(raw) for key, raw in inputs.items()}))


def carry_comparison(old, new, old_outputs, new_outputs):
    """Inputs authorize carry; unexplained changed outputs additionally requeue."""
    fields = HARD_COMPONENTS + ("truthInputDigest",)
    require(all(k in old and k in new for k in fields), "LABEL_KEY_FIELDS")
    same = {k: canonical(old[k]) == canonical(new[k]) for k in fields}
    inputs_equal = all(same.values())
    changed_outputs = canonical(old_outputs) != canonical(new_outputs)
    return {"components": same, "carried": inputs_equal and not changed_outputs,
            "requeue": not inputs_equal or changed_outputs,
            "determinismDefect": inputs_equal and changed_outputs}


def held_out_eligible(case, ledger_bytes):
    """Exposure is permanent, including if its record was later superseded.

    The caller supplies every prior round's ledger as well as the current one;
    a new freeze does not reset the history.
    """
    if not case["heldOut"]:
        return False
    subjects = {"case": case["caseId"], "repository": case["inputs"].get("repository"), "family": case.get("family")}
    return not any(r["recordKind"] == "exposure" and subjects[r["scope"]] == r["subject"]
                   for raw in ledger_bytes for r in read_ledger(raw))
