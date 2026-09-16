"""Second attempt (the first, tools/edit_native_cases.py, refused: the file does not round-trip through json.dumps).

Usage: edit_native_cases_textual.py CASES_JSON

Textual insertion: the fixture and case objects are those defined in edit_native_cases.py (imported by exec of its
definitions, not re-typed). Each is spelled with json.dumps(indent=1) re-indented to the anchor's depth and inserted
immediately after the anchor fixture value / anchor case object, located by json.JSONDecoder.raw_decode, so every
original byte is kept. Verification: the edited file parses; its fixtures equal the original fixtures with the new one
inserted after the anchor (order included); its cases equal the original cases with the new one inserted after the
anchor; the original bytes are an exact prefix + suffix of the edited bytes around the two insertions. Also reports
where the json.dumps round-trip first differs, for the record.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
path = Path(sys.argv[1])
raw = path.read_bytes()
text = raw.decode("utf-8")
doc = json.loads(text)

# Reuse the exact fixture/case definitions of the first attempt without running its rewrite: execute its source up to
# the line that starts rewriting.
first = (HERE / "edit_native_cases.py").read_text()
defs = first[first.index("FIXTURE = "):first.index("fixtures = {}\n")]
ns = {"json": json, "doc": doc}
exec(compile(defs, "edit_native_cases.py(definitions)", "exec"), ns)
FIXTURE, CASE_ID, fixture, case = ns["FIXTURE"], ns["CASE_ID"], ns["fixture"], ns["case"]
AFTER_FIXTURE, AFTER_CASE = ns["AFTER_FIXTURE"], ns["AFTER_CASE"]

roundtrip = {}
for ensure_ascii in (False, True):
    dumped = (json.dumps(doc, indent=1, ensure_ascii=ensure_ascii) + "\n").encode("utf-8")
    at = next((i for i, (a, b) in enumerate(zip(raw, dumped)) if a != b), min(len(raw), len(dumped)))
    roundtrip[str(ensure_ascii)] = {"firstDifferenceOffset": at, "original": raw[max(0, at - 60):at + 60].decode("utf-8", "replace"),
                                    "dumped": dumped[max(0, at - 60):at + 60].decode("utf-8", "replace")}

decoder = json.JSONDecoder()


def indent_of(offset):
    line_start = text.rfind("\n", 0, offset) + 1
    return text[line_start:offset][:len(text[line_start:offset]) - len(text[line_start:offset].lstrip(" "))]


def spelled(value, indent):
    return json.dumps(value, indent=1, ensure_ascii=False).replace("\n", "\n" + indent)


# fixture: the value following the anchor key
key = json.dumps(AFTER_FIXTURE) + ": "
k = text.index(key)
assert text.count(key) == 1
_, fixture_end = decoder.raw_decode(text, k + len(key))
fixture_indent = indent_of(k)
fixture_insert = ",\n" + fixture_indent + json.dumps(FIXTURE) + ": " + spelled(fixture, fixture_indent)

# case: the object containing the anchor id
id_text = '"id": ' + json.dumps(AFTER_CASE)
i = text.index(id_text)
assert text.count(id_text) == 1
start = text.rfind("{", 0, i)
anchor_case, case_end = decoder.raw_decode(text, start)
assert anchor_case["id"] == AFTER_CASE
case_indent = indent_of(start)
case_insert = ",\n" + case_indent + spelled(case, case_indent)

assert fixture_end < start
new_text = text[:fixture_end] + fixture_insert + text[fixture_end:case_end] + case_insert + text[case_end:]
new = json.loads(new_text)
want_fixtures = []
for name, value in doc["fixtures"].items():
    want_fixtures.append((name, value))
    if name == AFTER_FIXTURE:
        want_fixtures.append((FIXTURE, fixture))
index = next(n for n, c in enumerate(doc["cases"]) if c["id"] == AFTER_CASE)
want_cases = doc["cases"][:index + 1] + [case] + doc["cases"][index + 1:]
checks = {
    "fixturesEqualOriginalPlusOne": list(new["fixtures"].items()) == want_fixtures,
    "casesEqualOriginalPlusOne": new["cases"] == want_cases,
    "otherTopLevelKeysUnchanged": {k: v for k, v in new.items() if k not in ("fixtures", "cases")} == {k: v for k, v in doc.items() if k not in ("fixtures", "cases")},
    "originalBytesPreservedAroundInsertions": new_text.replace(fixture_insert, "", 1).replace(case_insert, "", 1) == text,
}
if not all(checks.values()):
    raise SystemExit(json.dumps({"checks": checks, "roundtrip": roundtrip}, indent=1))
out = new_text.encode("utf-8")
path.write_bytes(out)
print(json.dumps({"checks": checks, "roundtrip": roundtrip, "beforeSha256": hashlib.sha256(raw).hexdigest(), "beforeBytes": len(raw),
                  "afterSha256": hashlib.sha256(out).hexdigest(), "afterBytes": len(out), "caseIndex": index + 1,
                  "cases": len(new["cases"]), "fixtureIndent": len(fixture_indent), "caseIndent": len(case_indent)}, indent=1))
