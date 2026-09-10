#!/usr/bin/env python3
"""p19: does a HYPOTHETICAL document call contaminate the registered-law memo?

Executed during the review as a heredoc; retained here as the exact code that produced
logs/p19-cache-isolation.json.

relation_annotation_closure takes `document` as a parameter so a caller can ask about a
hypothetical schema. It also memoises registered results in _RELATION_LAW_CLOSURE. If a
hypothetical call ever wrote that memo, a refused hypothetical could poison -- or a permissive
hypothetical could whitewash -- subsequent REGISTERED admission. Tested in both orders.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")


def fresh(tag):
    s = importlib.util.spec_from_file_location(tag, F / "identity-model.py")
    m = importlib.util.module_from_spec(s)
    sys.modules[tag] = m
    s.loader.exec_module(m)
    return m


def verdict(M, name, doc=None):
    try:
        M.relation_annotation_closure(name, doc)
        return "ADMIT"
    except Exception as e:
        return str(e).split(":")[0]


BARE = {"$ref": "#/$defs/DigestHex"}


def poisoned(M):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d["$defs"]["FilePayloadV1"]["properties"]["stray"] = dict(BARE)
    return d


out = {}

# order 1: hypothetical REFUSAL first, then registered
M = fresh("c1")
out["hypotheticalFirst"] = {
    "hypothetical": verdict(M, "file", poisoned(M)),
    "thenRegistered": verdict(M, "file"),
    "memoAfter": sorted(M._RELATION_LAW_CLOSURE)}

# order 2: registered first, then hypothetical, then registered again
M = fresh("c2")
r1 = verdict(M, "file")
memo1 = sorted(M._RELATION_LAW_CLOSURE)
h = verdict(M, "file", poisoned(M))
memo2 = sorted(M._RELATION_LAW_CLOSURE)
r2 = verdict(M, "file")
out["registeredFirst"] = {"registered": r1, "memoAfterRegistered": memo1,
                          "hypothetical": h, "memoAfterHypothetical": memo2,
                          "registeredAgain": r2}

# a PERMISSIVE hypothetical must not whitewash a registered refusal either
M = fresh("c3")
d = copy.deepcopy(M.RELATION_DOCUMENT)
out["permissiveHypothetical"] = {"hypothetical": verdict(M, "file", d),
                                 "memoAfter": sorted(M._RELATION_LAW_CLOSURE),
                                 "registered": verdict(M, "file")}

out["memoOnlyEverPopulatedByRegisteredCalls"] = (
    out["hypotheticalFirst"]["memoAfter"] == []
    or out["hypotheticalFirst"]["memoAfter"] == ["file"])
out["hypotheticalNeverWritesMemo"] = (
    out["registeredFirst"]["memoAfterRegistered"]
    == out["registeredFirst"]["memoAfterHypothetical"])
out["registeredVerdictUnaffected"] = (
    out["registeredFirst"]["registered"] == "ADMIT"
    and out["registeredFirst"]["registeredAgain"] == "ADMIT"
    and out["hypotheticalFirst"]["thenRegistered"] == "ADMIT"
    and out["hypotheticalFirst"]["hypothetical"] == "RELATION_DIGEST_UNANNOTATED")
out["NO_CACHE_CONTAMINATION"] = (out["hypotheticalNeverWritesMemo"]
                                 and out["registeredVerdictUnaffected"])
print(json.dumps(out, indent=2))
