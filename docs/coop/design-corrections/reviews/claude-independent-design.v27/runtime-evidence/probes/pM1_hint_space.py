"""PROBE M1-A (v27) — exhaustive admissibility audit of the corrected logicalPath position.

My v26 M-1 said the position had TWO admissible spellings where the contract declared the
value meaningless. The bounded remedy is sufficient iff, for every (kind, occupancy) pair
the contract declares meaningless, EXACTLY ONE logicalPath value is admissible, and every
pair the contract declares meaningful keeps BOTH.

I enumerate the whole 4 x 3 x 2 space against BOTH corrected schemas rather than testing
the cases the author chose.
"""
import itertools, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v27/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)
from jsonschema import Draft202012Validator

TA = json.load(open(os.path.join(DC, 'foundation/target-attribution.schema.v2.json'), encoding='utf-8'))
OC = json.load(open(os.path.join(DC, 'native/occupancy-companion.schema.v1.json'), encoding='utf-8'))
U = '0' * 64


def ok(schema, inst):
    return not list(Draft202012Validator(schema).iter_errors(inst))


def build(kind, occ, lp):
    ta = {"schemaVersion": 2, "planId": "plan2:" + "a" * 64, "sourceFactId": "fact2:" + "b" * 64,
          "producerClosure": "closure2:" + "c" * 64, "targetUniverse": U,
          "targetNativeId": "mod:opaque-thing", "kind": kind, "occupancy": occ,
          "exported": "unknown" if kind == "symbol" else None,
          "logicalPath": lp, "packageManifestPath": None, "evaluationNativeId": None}
    oc = {"schemaVersion": 1, "candidateOrdinal": 0, "targetUniverseId": U,
          "targetNativeId": "mod:opaque-thing", "kind": kind, "occupancy": occ,
          "exported": ta["exported"], "logicalPath": lp,
          "packageManifestPath": None, "evaluationNativeId": None}
    if occ == "first-party":
        ta["evaluationNativeId"] = oc["evaluationNativeId"] = "src/a.ts"
    if kind == "package" and occ in ("first-party", "external"):
        ta["packageManifestPath"] = oc["packageManifestPath"] = "pkg/package.json"
    return ta, oc


KINDS = ["file", "symbol", "package", "unknown"]
OCCS = ["first-party", "external", "unknown"]
grid = {}
for kind, occ in itertools.product(KINDS, OCCS):
    row = {}
    for label, lp in (("null", None), ("path", "src/hint.ts")):
        ta, oc = build(kind, occ, lp)
        row[label] = {"TAv2": ok(TA, ta), "OCv1": ok(OC, oc)}
    grid["%s/%s" % (kind, occ)] = row

# The contract's own declared meaning (target-attribution logicalPath description +
# atom-evaluation-contract section 2 + provider-return producerSupply.modes):
#   hint MEANINGFUL only for kind in {file, symbol} with occupancy in {external, unknown}
MEANINGFUL = {(k, o) for k in ("file", "symbol") for o in ("external", "unknown")}

verdict = {}
for key, row in grid.items():
    kind, occ = key.split('/')
    both_ta = row["null"]["TAv2"] and row["path"]["TAv2"]
    both_oc = row["null"]["OCv1"] and row["path"]["OCv1"]
    admissible_ta = [l for l in ("null", "path") if row[l]["TAv2"]]
    admissible_oc = [l for l in ("null", "path") if row[l]["OCv1"]]
    meaningful = (kind, occ) in MEANINGFUL
    verdict[key] = {
        "contractSaysHintMeaningful": meaningful,
        "admissibleLogicalPath_TAv2": admissible_ta,
        "admissibleLogicalPath_OCv1": admissible_oc,
        "twoSpellingsTAv2": both_ta, "twoSpellingsOCv1": both_oc,
        "schemasAgree": admissible_ta == admissible_oc,
        "conformsToDeclaredMeaning":
            (both_ta == meaningful) and (both_oc == meaningful),
    }

res = {
    "totalCells": len(grid) * 2,
    "grid": grid,
    "verdict": verdict,
    "allCellsConformToDeclaredMeaning": all(v["conformsToDeclaredMeaning"] for v in verdict.values()),
    "schemasAgreeEverywhere": all(v["schemasAgree"] for v in verdict.values()),
    "meaninglessPositionsWithTwoSpellings": sorted(
        k for k, v in verdict.items()
        if not v["contractSaysHintMeaningful"] and (v["twoSpellingsTAv2"] or v["twoSpellingsOCv1"])),
    "meaningfulPositionsNarrowedByMistake": sorted(
        k for k, v in verdict.items()
        if v["contractSaysHintMeaningful"] and not (v["twoSpellingsTAv2"] and v["twoSpellingsOCv1"])),
}
json.dump(res, open(os.path.join(OUT, 'pM1-hint-space.json'), 'w'), indent=1)

print('%-22s %-11s %-18s %-18s %s' % ('kind/occupancy', 'meaningful', 'admissible TAv2',
                                      'admissible OCv1', 'conforms'))
for k in sorted(verdict):
    v = verdict[k]
    print('%-22s %-11s %-18s %-18s %s' % (
        k, v["contractSaysHintMeaningful"], ','.join(v["admissibleLogicalPath_TAv2"]) or '(none)',
        ','.join(v["admissibleLogicalPath_OCv1"]) or '(none)', v["conformsToDeclaredMeaning"]))
print()
print('total cells evaluated          :', res["totalCells"])
print('all cells conform to meaning   :', res["allCellsConformToDeclaredMeaning"])
print('both schemas agree everywhere  :', res["schemasAgreeEverywhere"])
print('meaningless pos. w/ 2 spellings:', res["meaninglessPositionsWithTwoSpellings"])
print('meaningful pos. over-narrowed  :', res["meaningfulPositionsNarrowedByMistake"])
