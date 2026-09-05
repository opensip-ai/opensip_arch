#!/usr/bin/env python3
"""Exact architecture conformance checker for retention-tiers.v21.json.

The sole admitted invocation is ``python3 -I -B``.  This checker is an
architecture test instrument: it grants no application, product, freeze,
seal, integration, release, or production authority.
"""

from __future__ import annotations

import sys

STARTUP_REFUSAL = (
    "RT21-CHECKER-UNSUPPORTED-INVOCATION: use python3 -I -B "
    "check-retention-custody-v21.py"
)
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import dataclasses
import datetime
import functools
import gc
import hashlib
import inspect
import json
import os
import pathlib
import re
import types
import typing
from collections import deque
from collections.abc import Mapping as MappingABC
from types import MappingProxyType
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "retention-tiers.v21.json"
RT21_STATUS = "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REVIEW"
PROJECT_A = "prj1-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
PROJECT_B = "prj1-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TX_BOUNDARY = "ONE_PROJECT_LEDGER_TRANSACTION"
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")

EP8 = "evaluation-proof.v8.json"
EP8_CHECKER = "check-evaluation-proof-v8.py"
EP8_REVIEW = "ep8-rt13.review-independent-cold-reconstruction.json"
EP7 = "evaluation-proof.v7.json"
EP7_CHECKER = "check-evaluation-proof-v7.py"
EP6 = "evaluation-proof.v6.json"
EP6_CHECKER = "check-evaluation-proof-v6.py"
EP5 = "evaluation-proof.v5.json"
EP5_CHECKER = "check-evaluation-proof.py"
C2 = "c2-plan-stage-schema.v3.json"
C2_CHECKER = "check-c2.py"
RI = "resolved-inputs.v2.json"
RI_CHECKER = "check-resolved-inputs.py"
FACT_PLANE = "fact-plane.v1.json"
RT13 = "retention-tiers.v13.json"
RT13_CHECKER = "check-retention-custody-v13.py"
RT_CORE = "check-retention-custody.py"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"
RT14_REVIEW = "retention-tiers.v14.review-independent-prefreeze.json"
D9 = "d9-exit-contract.v1.13.json"
D9_CHECKER = "check-d9-v1.13.py"
D9_REVIEW = "d9-exit-contract.v1.13.review-independent-prefreeze.json"
RT15 = "retention-tiers.v15.json"
RT15_CHECKER = "check-retention-custody-v15.py"
RT15_ADJUDICATION = "retention-tiers.v15.adjudication-v14-and-e8-preimage-response.json"
RT15_REVIEW = "retention-tiers.v15.review-independent-prefreeze.json"
RT16 = "retention-tiers.v16.json"
RT16_CHECKER = "check-retention-custody-v16.py"
RT16_ADJUDICATION = "retention-tiers.v16.adjudication-v15-verifier-boundary-response.json"
RT16_REVIEW = "retention-tiers.v16.review-independent-prefreeze.json"
RT20 = "retention-tiers.v20.json"
RT20_CHECKER = "check-retention-custody-v20.py"
RT20_ADJUDICATION = "retention-tiers.v20.adjudication-v19-review-response.json"
RT20_REVIEW = "retention-tiers.v20.review-independent-prefreeze.json"
ARCHITECTURE_PLAN = "ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md"

PINS: dict[str, str] = {
    RT20: "89684a06cc5fb7f23d6e14ab82034957c5268ab218c442915be0212329c310a2",
    RT20_CHECKER: "52003c08dc115744c0119158e8d615a3bd37fa9bb55692e48ceed78a56ebe3e2",
    RT20_ADJUDICATION: "4d9441682981ed54d758e6afda3c661bd2e20e8da0f6f99991b2e178080e7843",
    RT20_REVIEW: "474e5c34c4859f879a9f6f1883175cac155615d73bc45c6d00579444d40fcb30",
    RT16: "f34c6986f8b95f492f075f3dfb51ad81c487b289fcdbdc7d499bd3b55dc93c06",
    RT16_CHECKER: "85e022289048cdb695a9180637c6cbebc05e7778eeb03479c40965ea77cc9010",
    RT16_ADJUDICATION: "94dd62701676123f23ec7b51ea91f548bf9f757eb9833d6fe009f8d25b07ef87",
    RT16_REVIEW: "d673fd0a96c58931a6219757c0bed4c76366065db08d5b9fbd0207d5d977e87a",
    RT15: "52d4739c326ce406b8511a1301a2156301c5643a79bf9339cc3246a292a60253",
    RT15_CHECKER: "ef6e92d8c9a8ce0f4a12c47d7091e2dd7b40061388601f5fcff77bf44b8611ec",
    RT15_ADJUDICATION: "c19d9f95885b06d820499196e8ab3b18a597a622b137300352a6f2376223be8a",
    RT15_REVIEW: "d8348a7805c4dd12b54b7cfde2e49198d197306752d283d4bf09e96023ef48a3",
    EP8: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    EP8_CHECKER: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    EP8_REVIEW: "f4599b32a9f1b93049111b9e86debd19419902c9c5f4fb886f8d0dc9c330567e",
    RT13: "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    RT13_CHECKER: "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    RT_CORE: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    RT14: "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    RT14_CHECKER: "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    RT14_REVIEW: "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
    D9: "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    D9_CHECKER: "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    D9_REVIEW: "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
    EP7: "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    EP7_CHECKER: "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    EP6: "74f35668afae2efb57070ff9a2897d373a91b42cc1cbbc87f3c673f872ca4bce",
    EP6_CHECKER: "0a7ac122a598bb7b9454b1b3c46c586f6fd551a2a1ebcf5584665f875457c5f0",
    EP5: "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    EP5_CHECKER: "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    C2: "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    C2_CHECKER: "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
    RI: "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    RI_CHECKER: "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
    FACT_PLANE: "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "d9-exit-contract.v1.12.json": "17aa2161619ca6abae209dd2b2eda3a16d533718f1697cc31b87325feaa4b2d4",
    "check-d9-v1.12.py": "32566f4f56d81ead4e3f2582ef3a6e934ca1fa0ca4172b13124e952018ec9c8a",
    "d9-exit-contract.v1.12.review-independent-prefreeze.json": "1e6486db60e24a6ba9eef06ca8c2808a09376917189dd330f7808567fe31bd4c",
    "d9-exit-contract.v1.11.json": "09ab6b579173bdbd9575d46e7df96b8279a0bb12512638e25ad56e28d16e9895",
    "check-d9-v1.11.py": "9b637adee48432bb5388ce51212d59a1965044d2c1d5f6b6a4a3dd8ed519000a",
    "d9-exit-contract.v1.11.review-independent-prefreeze.json": "df1e89324a6c7645e96f69a2cc924731e4e37eeea64c10058cdd4cfcdfdbbcec",
    "d9-exit-contract.v1.10.json": "bf1d7eb0ab24de89f665f46c25377195a2721fc7fcb62f3aa449d0887b705b7b",
    "check-d9-v1.10.py": "77f86334a0ee016960224880fe75ef2b9b44d3adf20799c8354e992fbf19cca6",
    "d9-exit-contract.v1.10.review-independent-prefreeze.json": "7faefdf8f2c19e39ad9fdd6fba8df6f08c586aa73b7e5ab7ed917ae4c223e476",
    "d9-exit-contract.v1.9.json": "bc3c2b48d3615bc262166a698d3a3559bc2fa2fbd2f637de0dbf943309194404",
    "check-d9-v1.9.py": "956e41e279e758af5dd5e342a5404f334f6223add72abdb1340c85fafa2bd936",
    "d9-exit-contract.v1.9.review-independent-prefreeze.json": "409e55ddcc2121da5624a112728cd2d126586411a9abe06435c64d1c02b71373",
    "d9-exit-contract.v1.8.json": "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    "check-d9-v1.8.py": "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    "d9-exit-contract.v1.8.review-independent-prefreeze.json": "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "d9-exit-contract.v1.6.json": "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py": "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    ARCHITECTURE_PLAN: "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
}

ROOT_ORDER = [
    "artifact", "version", "status", "claimId",
    "supersedesAsArchitectureCandidate", "dependencies",
    "semanticBasisProjection", "operationalCustodyProjectionContract",
    "semanticLeaseProtocolV3", "storageAndLineage", "custodyPolicy",
    "authority", "integrationState", "semanticOwnershipBoundary",
    "invariants", "assurance", "retainedResiduals", "sealRecommendation",
    "rawPhysicalIdentityContract", "verifiedSemanticRtApiContract",
]

# Complete returned-value vocabulary.  RT21 does not return general Python
# objects.  The reflective RT20 graph denominator is therefore retained only
# as predecessor evidence, never as the RT21 production boundary.
INERT_VALUE_REGISTRY: tuple[dict[str, str], ...] = (
    {"id": "null", "disposition": "leaf", "exactType": "NoneType"},
    {"id": "boolean", "disposition": "leaf", "exactType": "bool"},
    {"id": "integer", "disposition": "leaf", "exactType": "int"},
    {"id": "utf8-string", "disposition": "leaf", "exactType": "str"},
    {"id": "immutable-bytes", "disposition": "leaf", "exactType": "bytes"},
    {"id": "immutable-tuple", "disposition": "traverse", "exactType": "tuple"},
    {"id": "readonly-string-map", "disposition": "traverse",
     "exactType": "MappingProxyType[str, InertValue]"},
)
INERT_EDGE_REGISTRY: tuple[dict[str, str], ...] = (
    {"id": "mapping-key", "from": "readonly-string-map",
     "to": "each exact string key"},
    {"id": "mapping-value", "from": "readonly-string-map",
     "to": "each value"},
    {"id": "tuple-item", "from": "immutable-tuple",
     "to": "each ordered item"},
)
INERT_VALUE_IDS = tuple(row["id"] for row in INERT_VALUE_REGISTRY)
INERT_EDGE_IDS = tuple(row["id"] for row in INERT_EDGE_REGISTRY)
INERT_HOST_OPERATION_IDS = (
    "derive_operational_custody_projection_v1",
    "validate_raw_object_resolution_v1",
    "reduce_expiry_v1",
    "reduce_release_v1",
    "reduce_crash_reclaim_v3",
    "reduce_resolve_and_pin_v2",
    "is_retention_local_unavailable_v1",
)
INERT_SNAPSHOT_FIELDS = (
    "schemaVersion", "kind", "snapshotId", "candidate", "rt13",
    "ep8DerivationReceipt", "fixtureProjection", "hostOperationIds",
)
INERT_MAX_NODES = 500_000
INERT_MAX_DEPTH = 256

# Closed ordered declaration of every semantic edge extractor used by the
# returned-object quarantine.  The selftest deletes every row independently;
# production traversal refuses any missing, duplicate, reordered, or unknown
# declaration before visiting the root.
GRAPH_EDGE_REGISTRY: tuple[dict[str, str], ...] = (
    {"id": "runtime-referents", "from": "every admitted traverse kind",
     "to": "each CPython gc.get_referents direct strong referent"},
    {"id": "mapping-keys-values", "from": "Mapping",
     "to": "each items() key and value"},
    {"id": "sequence-items", "from": "list/tuple/deque",
     "to": "each ordered item"},
    {"id": "set-items", "from": "set/frozenset",
     "to": "each iterated item"},
    {"id": "memoryview-backing-object", "from": "memoryview",
     "to": "obj"},
    {"id": "slice-start", "from": "slice", "to": "start"},
    {"id": "slice-stop", "from": "slice", "to": "stop"},
    {"id": "slice-step", "from": "slice", "to": "step"},
    {"id": "code-constants", "from": "types.CodeType",
     "to": "each co_consts item"},
    {"id": "bound-method-owner", "from": "bound Python method",
     "to": "__self__"},
    {"id": "bound-method-function", "from": "bound Python method",
     "to": "__func__"},
    {"id": "builtin-bound-owner", "from": "bound builtin/method-wrapper",
     "to": "__self__"},
    {"id": "partial-function", "from": "functools.partial",
     "to": "func"},
    {"id": "partial-args", "from": "functools.partial",
     "to": "args"},
    {"id": "partial-keywords", "from": "functools.partial",
     "to": "keywords"},
    {"id": "function-globals", "from": "Python function",
     "to": "__globals__"},
    {"id": "function-closure-cells", "from": "Python function",
     "to": "each __closure__ cell"},
    {"id": "function-defaults", "from": "Python function",
     "to": "__defaults__"},
    {"id": "function-kwdefaults", "from": "Python function",
     "to": "__kwdefaults__"},
    {"id": "function-annotations", "from": "Python function",
     "to": "__annotations__"},
    {"id": "function-attributes", "from": "Python function",
     "to": "__dict__"},
    {"id": "function-code", "from": "Python function", "to": "__code__"},
    {"id": "function-builtins", "from": "Python function",
     "to": "__builtins__"},
    {"id": "function-doc", "from": "Python function", "to": "__doc__"},
    {"id": "function-module", "from": "Python function",
     "to": "__module__"},
    {"id": "function-type-params", "from": "Python function",
     "to": "__type_params__"},
    {"id": "function-annotate", "from": "Python function",
     "to": "__annotate__"},
    {"id": "module-dictionary", "from": "module", "to": "__dict__"},
    {"id": "cell-contents", "from": "closure cell", "to": "cell_contents"},
    {"id": "object-attributes", "from": "non-class object",
     "to": "__dict__"},
    {"id": "object-slots-mro-mangled", "from": "non-class object",
     "to": "all inherited slots after Python name mangling"},
    {"id": "object-class", "from": "non-builtin object", "to": "__class__"},
    {"id": "class-dictionary", "from": "class", "to": "__dict__"},
    {"id": "class-bases", "from": "class", "to": "__bases__"},
    {"id": "class-mro", "from": "class", "to": "__mro__"},
    {"id": "property-accessors", "from": "property descriptor",
     "to": "fget/fset/fdel"},
    {"id": "property-doc", "from": "property descriptor", "to": "__doc__"},
    {"id": "property-name", "from": "property descriptor", "to": "__name__"},
    {"id": "wrapped-descriptor-function",
     "from": "classmethod/staticmethod descriptor", "to": "__func__"},
    {"id": "descriptor-owner", "from": "builtin descriptor",
     "to": "__objclass__"},
    {"id": "class-metaclass", "from": "class", "to": "__class__"},
    {"id": "frame-globals", "from": "frame", "to": "f_globals"},
    {"id": "frame-locals", "from": "frame", "to": "f_locals"},
    {"id": "frame-back", "from": "frame", "to": "f_back"},
    {"id": "frame-builtins", "from": "frame", "to": "f_builtins"},
    {"id": "frame-code", "from": "frame", "to": "f_code"},
    {"id": "frame-trace", "from": "frame", "to": "f_trace"},
    {"id": "frame-generator", "from": "frame", "to": "f_generator"},
    {"id": "generator-frame", "from": "generator", "to": "gi_frame"},
    {"id": "generator-code", "from": "generator", "to": "gi_code"},
    {"id": "generator-yieldfrom", "from": "generator", "to": "gi_yieldfrom"},
    {"id": "coroutine-frame", "from": "coroutine", "to": "cr_frame"},
    {"id": "coroutine-code", "from": "coroutine", "to": "cr_code"},
    {"id": "coroutine-await", "from": "coroutine", "to": "cr_await"},
    {"id": "coroutine-origin", "from": "coroutine", "to": "cr_origin"},
    {"id": "async-generator-frame", "from": "async generator",
     "to": "ag_frame"},
    {"id": "async-generator-code", "from": "async generator",
     "to": "ag_code"},
    {"id": "async-generator-await", "from": "async generator",
     "to": "ag_await"},
)
GRAPH_EDGE_IDS = tuple(row["id"] for row in GRAPH_EDGE_REGISTRY)

# Exact ordered runtime-kind denominator.  Dispatch follows this order.  A
# non-atomic value that matches none of these admitted kinds is a controlled
# refusal, never a clean leaf.  Selftest deletes each declaration.
GRAPH_RUNTIME_KIND_REGISTRY: tuple[dict[str, str], ...] = (
    {"id": "atomic-exact", "disposition": "leaf"},
    {"id": "opaque-runtime-exact", "disposition": "leaf"},
    {"id": "slice", "disposition": "traverse"},
    {"id": "code", "disposition": "traverse"},
    {"id": "mapping", "disposition": "traverse"},
    {"id": "sequence", "disposition": "traverse"},
    {"id": "set", "disposition": "traverse"},
    {"id": "memoryview", "disposition": "traverse"},
    {"id": "bound-python-method", "disposition": "traverse"},
    {"id": "bound-builtin", "disposition": "traverse"},
    {"id": "partial", "disposition": "traverse"},
    {"id": "python-function", "disposition": "traverse"},
    {"id": "module", "disposition": "traverse"},
    {"id": "closure-cell", "disposition": "traverse"},
    {"id": "property", "disposition": "traverse"},
    {"id": "wrapped-descriptor", "disposition": "traverse"},
    {"id": "builtin-descriptor", "disposition": "traverse"},
    {"id": "class", "disposition": "traverse"},
    {"id": "frame", "disposition": "traverse"},
    {"id": "generator", "disposition": "traverse"},
    {"id": "coroutine", "disposition": "traverse"},
    {"id": "async-generator", "disposition": "traverse"},
    {"id": "declared-nonbuiltin-object", "disposition": "traverse"},
    {"id": "unknown-runtime-type", "disposition": "refuse"},
)
GRAPH_RUNTIME_KIND_IDS = tuple(
    row["id"] for row in GRAPH_RUNTIME_KIND_REGISTRY)
GRAPH_RUNTIME_DISPOSITIONS = {
    row["id"]: row["disposition"] for row in GRAPH_RUNTIME_KIND_REGISTRY
}

# Independently declared semantic-child denominator.  It is intentionally not
# generated from GRAPH_EDGE_REGISTRY.  CPython's direct strong-referent oracle
# supplies the general case; only runtime values for which that oracle is
# observably incomplete have an explicit closed exception row.
GRAPH_SEMANTIC_CHILD_DENOMINATOR: tuple[dict[str, Any], ...] = (
    {"id": "atomic-exact", "oracle": "LEAF-AUDIT", "requiredEdges": []},
    {"id": "opaque-runtime-exact", "oracle": "LEAF-AUDIT", "requiredEdges": []},
    {"id": "slice", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "slice-start", "slice-stop", "slice-step"]},
    {"id": "code", "oracle": "EXPLICIT-GC-EXCEPTION", "requiredEdges": [
        "code-constants"]},
    {"id": "mapping", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "mapping-keys-values"]},
    {"id": "sequence", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "sequence-items"]},
    {"id": "set", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "set-items"]},
    {"id": "memoryview", "oracle": "EXPLICIT-GC-EXCEPTION", "requiredEdges": [
        "memoryview-backing-object"]},
    {"id": "bound-python-method", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "bound-method-owner", "bound-method-function"]},
    {"id": "bound-builtin", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "builtin-bound-owner"]},
    {"id": "partial", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "partial-function", "partial-args", "partial-keywords"]},
    {"id": "python-function", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "function-globals", "function-closure-cells",
        "function-defaults", "function-kwdefaults", "function-annotations",
        "function-attributes", "function-code", "function-builtins",
        "function-doc", "function-module", "function-type-params",
        "function-annotate"]},
    {"id": "module", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "module-dictionary"]},
    {"id": "closure-cell", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "cell-contents"]},
    {"id": "property", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "property-accessors", "property-doc", "property-name"]},
    {"id": "wrapped-descriptor", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "wrapped-descriptor-function"]},
    {"id": "builtin-descriptor", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "descriptor-owner"]},
    {"id": "class", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "class-dictionary", "class-bases", "class-mro",
        "class-metaclass"]},
    {"id": "frame", "oracle": "EXPLICIT-GC-EXCEPTION", "requiredEdges": [
        "frame-globals", "frame-locals", "frame-back", "frame-builtins",
        "frame-code", "frame-trace", "frame-generator"]},
    {"id": "generator", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "generator-frame", "generator-code",
        "generator-yieldfrom"]},
    {"id": "coroutine", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "coroutine-frame", "coroutine-code",
        "coroutine-await", "coroutine-origin"]},
    {"id": "async-generator", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "async-generator-frame", "async-generator-code",
        "async-generator-await"]},
    {"id": "declared-nonbuiltin-object", "oracle": "CPYTHON-GC-REFERENTS", "requiredEdges": [
        "runtime-referents", "object-attributes", "object-slots-mro-mangled",
        "object-class"]},
    {"id": "unknown-runtime-type", "oracle": "REFUSE", "requiredEdges": []},
)
GRAPH_SEMANTIC_CHILD_IDS = tuple(
    row["id"] for row in GRAPH_SEMANTIC_CHILD_DENOMINATOR)
GRAPH_REFERENT_ORACLE_EXCEPTIONS: tuple[dict[str, Any], ...] = (
    {"runtimeKind": "memoryview",
     "reason": "gc.get_referents(memoryview) exposes managedbuffer, not obj",
     "requiredEdges": ["memoryview-backing-object"]},
    {"runtimeKind": "code", "reason": "gc.get_referents(code) is empty",
     "requiredEdges": ["code-constants"]},
    {"runtimeKind": "frame", "reason": "gc.get_referents(frame) is empty",
     "requiredEdges": [
         "frame-globals", "frame-locals", "frame-back", "frame-builtins",
         "frame-code", "frame-trace", "frame-generator"]},
)
GRAPH_POSITIVE_CASE_IDS: tuple[str, ...] = (
    "mapping-value", "mapping-key", "mappingproxy", "list", "tuple",
    "deque", "set", "frozenset", "memoryview-backing", "object-dict",
    "object-slot", "mangled-slot", "inherited-mangled-slot",
    "bound-method-owner", "bound-method-function", "builtin-bound-owner",
    "function-globals", "function-closure", "cell-contents",
    "function-default", "function-kwdefault", "function-annotation",
    "function-attribute", "module", "partial-function", "partial-args",
    "partial-keywords", "object-class", "class-dictionary", "class-bases",
    "class-mro", "property-accessor", "wrapped-descriptor-function",
    "descriptor-owner", "class-metaclass", "frame-globals", "frame-locals",
    "frame-back", "generator-frame", "coroutine-frame",
    "async-generator-frame", "runtime-referent-function", "slice-start",
    "slice-stop", "slice-step", "code-constant", "function-code",
    "function-builtins", "function-doc", "function-module",
    "function-type-param", "function-annotate", "property-doc",
    "property-name", "frame-builtins", "frame-code", "frame-trace",
    "frame-generator", "generator-code", "generator-yieldfrom",
    "coroutine-code", "coroutine-await", "coroutine-origin",
    "async-generator-code", "async-generator-await",
)
CELL_TYPE = type((lambda item: lambda: item)(None).__closure__[0])
BUILTIN_BOUND_TYPES = tuple(dict.fromkeys(
    cls for cls in (
        types.BuiltinMethodType, getattr(types, "MethodWrapperType", None),
    ) if isinstance(cls, type)))
DESCRIPTOR_TYPES = tuple(dict.fromkeys(
    cls for cls in (
        getattr(types, "MemberDescriptorType", None),
        getattr(types, "GetSetDescriptorType", None),
        getattr(types, "MethodDescriptorType", None),
        getattr(types, "WrapperDescriptorType", None),
        getattr(types, "ClassMethodDescriptorType", None),
    ) if isinstance(cls, type)))
ATOMIC_RUNTIME_TYPES = (
    type(None), bool, int, float, complex, str, bytes, bytearray,
    range, type(Ellipsis), type(NotImplemented), object,
    type(REF_RE),
)
OPAQUE_ATOMIC_RUNTIME_TYPES = (
    type(typing.NoDefault),
    type(datetime.datetime_CAPI),
)
SAFE_OPAQUE_RUNTIME_TYPE_KEYS = (
    ("Token", "MISSING"),
    ("_abc", "_abc_data"),
    ("enum", "_auto_null"),
    ("enum", "_not_given"),
    ("genericpath", "ALLOW_MISSING"),
)
GRAPH_MAX_NODES = 500_000
GRAPH_MAX_DEPTH = 256
PROTECTED_ROOTS = [
    "artifact", "claimId", "storageAndLineage", "custodyPolicy",
    "integrationState", "assurance", "sealRecommendation",
    "rawPhysicalIdentityContract",
]
REMOVED_RT14_ROOTS = [
    "capabilityClosure", "leaseProtocol", "d9Derivation",
    "identityStabilityFromRT12", "contextualD9Rejoin",
]

OLD_PATTERNED_REFS = [
    "sha256:8484848484848484848484848484848484848484848484848484848484848484",
    "sha256:9191919191919191919191919191919191919191919191919191919191919191",
    "sha256:9292929292929292929292929292929292929292929292929292929292929292",
    "sha256:9393939393939393939393939393939393939393939393939393939393939393",
    "sha256:a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1",
    "sha256:b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0",
    "sha256:c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0",
    "sha256:e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5",
    "sha256:e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6",
    "sha256:f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0",
    "sha256:f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1",
]
DISCOVERED_OLD_PREIMAGES = [
    "sha256:11e923bffcc99c94372d7b575d733b79787da09d5d06286732c691b1158828fa",
    "sha256:16c2fca9e371936458d01576b4ca311c22d166a45539ccbc9104823d0b10db47",
    "sha256:21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9",
    "sha256:249a77c07b91bd865b4873c586ea4e41681be89d8d227590bfc44a3b33402ac5",
    "sha256:b4834d2eb7324dbde0aa0c9c461bedaae1ba6317b02fd441612b96dd4b4778bf",
    "sha256:d6a8d086d9ee0f2693f599ce39ecf90c0be65fd9a9127ddfd95572a2c95c3e04",
    "sha256:e3be6c3634ac045fd02d4753ac61ed6d9b82ea161e106c143de69a2f196467a5",
]


class DuplicateKeyError(ValueError):
    pass


class FloatForbidden(ValueError):
    pass


class AuthorityError(RuntimeError):
    pass


class ResolutionError(ValueError):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def _reject_float(_value: str) -> Any:
    raise FloatForbidden("floating-point JSON values are forbidden")


def _reject_constant(value: str) -> Any:
    raise FloatForbidden(f"non-finite JSON value is forbidden: {value}")


def parse_json_bytes(source: bytes, label: str) -> Any:
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: invalid UTF-8") from exc
    return json.loads(
        text, object_pairs_hook=_pairs, parse_float=_reject_float,
        parse_constant=_reject_constant,
    )


def pretty(value: Any) -> bytes:
    return (json.dumps(
        value, indent=2, ensure_ascii=True, sort_keys=False, allow_nan=False,
    ) + "\n").encode("utf-8")


def compact(value: Any, *, sort_keys: bool = False) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=sort_keys,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cas(data: bytes) -> str:
    return "sha256:" + sha256(data)


def domain_digest(domain: str, data: bytes) -> str:
    return cas(domain.encode("ascii") + b"\x00" + len(data).to_bytes(8, "big") + data)


def exact_recursive_equal(actual: Any, expected: Any, path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return f"{path}: type {type(actual).__name__} != {type(expected).__name__}"
    if isinstance(expected, dict):
        if list(actual) != list(expected):
            return f"{path}: key order/set {list(actual)!r} != {list(expected)!r}"
        for key in expected:
            found = exact_recursive_equal(actual[key], expected[key], f"{path}.{key}")
            if found:
                return found
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return f"{path}: length {len(actual)} != {len(expected)}"
        for index, (left, right) in enumerate(zip(actual, expected)):
            found = exact_recursive_equal(left, right, f"{path}[{index}]")
            if found:
                return found
        return None
    return None if actual == expected else f"{path}: {actual!r} != {expected!r}"


def parse_pinned_json_bytes(source: bytes, label: str) -> Any:
    """Parse inherited pinned data without narrowing its historical number model."""
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: invalid UTF-8") from exc
    return json.loads(
        text, object_pairs_hook=_pairs, parse_constant=_reject_constant,
    )


D9_INTERPOSITION_SPECS: Mapping[str, Mapping[str, str]] = MappingProxyType({
    "check-d9-v1.7.py": MappingProxyType({
        "kind": "eager-function", "target": "V16",
        "seam": "_load_v16_checker",
        "astSha256": "61cbcbef59ae3a3d048309af15c6660ff28d665df6b20a35508998902871e385",
    }),
    "check-d9-v1.8.py": MappingProxyType({
        "kind": "eager-function", "target": "V17",
        "seam": "_load_v17_checker",
        "astSha256": "a9f72020a2781459b6cf4290a56f522a6edfcb78905e8382d4e969ad8ce2769b",
    }),
    "check-d9-v1.11.py": MappingProxyType({
        "kind": "eager-loader-method", "target": "_BOOTSTRAP_AUTHORITY",
        "seam": "DeferredAuthorityLoader.load",
        "astSha256": "ecb90aee992743e47a0e62f26968bc432ab985e1d0e9fb6bd058243e7e55afaf",
    }),
    "check-d9-v1.12.py": MappingProxyType({
        "kind": "eager-loader-method", "target": "_BOOTSTRAP_AUTHORITY",
        "seam": "DeferredAuthorityLoader.load",
        "astSha256": "ecb90aee992743e47a0e62f26968bc432ab985e1d0e9fb6bd058243e7e55afaf",
    }),
    "check-d9-v1.13.py": MappingProxyType({
        "kind": "eager-loader-method", "target": "_BOOTSTRAP_AUTHORITY",
        "seam": "DeferredAuthorityLoader.load",
        "astSha256": "ecb90aee992743e47a0e62f26968bc432ab985e1d0e9fb6bd058243e7e55afaf",
    }),
})


EXPECTED_EP8_REQUIRED_API = (
    "assert_store_continuity",
    "derive_dependency_edges",
    "derive_raw_proof_requirements",
    "derive_semantic_requirements",
    "derive_transitive_requirements",
    "encode_semantic_object_binding",
    "resolve_semantic_object_bindings",
    "resolve_stored_evaluation",
    "validate_bundle",
)


class InternalEP8InvocationSurface:
    """Verifier-internal exact RT13-derived EP8 surface; never returned."""
    __slots__ = ("_api", "_sealed")

    def __init__(self, module: types.ModuleType, names: tuple[str, ...]) -> None:
        if names != EXPECTED_EP8_REQUIRED_API or len(names) != len(set(names)):
            raise AuthorityError("preserved RT13 requiredCheckerApi drift")
        api = {name: getattr(module, name) for name in names}
        if any(not callable(value) for value in api.values()):
            raise AuthorityError("EP8 internal required export is noncallable")
        object.__setattr__(self, "_api", MappingProxyType(api))
        object.__setattr__(self, "_sealed", True)

    def __getattr__(self, name: str) -> Any:
        try:
            return self._api[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, _name: str, _value: Any) -> None:
        raise AttributeError("InternalEP8InvocationSurface is immutable")


def _deep_frozen_data(value: Any) -> Any:
    """Return an immutable graph containing JSON data and no executable edge."""
    if value is None or isinstance(value, (bool, int, str, bytes)):
        return value
    if isinstance(value, list):
        return tuple(_deep_frozen_data(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_deep_frozen_data(item) for item in value)
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise AuthorityError("data-only receipt key is not a string")
        return MappingProxyType({
            key: _deep_frozen_data(item) for key, item in value.items()
        })
    raise AuthorityError(f"data-only receipt contains {type(value).__name__}")


def _fixture_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    fixtures = copy.deepcopy(candidate["verifiedSemanticRtApiContract"]
                             ["rawObjectResolutionConformance"]
                             ["fixtureGoldens"])
    projection = {
        "schemaVersion": 1,
        "kind": "VERIFIED_RAW_OBJECT_FIXTURE_PROJECTION",
        "fixtures": fixtures,
    }
    projection["projectionCommitment"] = cas(compact(projection, sort_keys=True))
    if [row.get("recordCount") for row in fixtures] != [7, 5] or \
            [row.get("unitCount") for row in fixtures] != [2, 3] or \
            not all(row.get("rawObjectSnapshot", {}).get("records")
                    for row in fixtures):
        raise AuthorityError("RT16 exact byte-bearing fixture projection drift")
    return projection


def _exercise_exact_ep8_surface(
        authority: "FrozenAuthority", module: types.ModuleType,
        fixture_projection: dict[str, Any],
) -> dict[str, Any]:
    """Invoke all nine authenticated APIs, return only closed derived data."""
    rt13 = authority.parsed[RT13]
    names_raw = rt13["capabilityClosure"]["source"]["requiredCheckerApi"]
    if not isinstance(names_raw, list) or any(not isinstance(x, str) for x in names_raw):
        raise AuthorityError("RT13 requiredCheckerApi is not a string array")
    names = tuple(names_raw)
    surface = InternalEP8InvocationSurface(module, names)
    vector = next(
        row for row in authority.parsed[EP8]["positiveVectors"]
        if row.get("id") == "EP8-POS-NOMATCH-PASS"
    )
    fixture = copy.deepcopy(vector["trustedStoreFixture"])
    store = module._open_test_project_store(fixture)
    if any(hasattr(store._state, name) for name in (
            "_candidate", "_candidates", "_inventory", "_cache")):
        raise AuthorityError("EP8 authenticated probe store is not cold")
    candidate = vector["evaluationAuthorityCandidate"]
    eas_ref = candidate["evaluationAuthorityAdmission"][
        "evaluationAuthoritySealRef"]
    calls: list[str] = []

    def invoke(name: str, *args: Any) -> Any:
        if name not in names:
            raise AuthorityError(f"undeclared EP8 invocation: {name}")
        calls.append(name)
        return getattr(surface, name)(*args)

    handle = invoke("resolve_stored_evaluation", store, eas_ref)
    if handle._candidate != candidate:
        raise AuthorityError("EP8 cold authority reconstruction drift")
    continuity = invoke("assert_store_continuity", store, handle)
    bundle_findings = invoke("validate_bundle", vector["bundle"], handle)
    resolved = invoke("resolve_semantic_object_bindings", handle)
    roots = invoke("derive_semantic_requirements", handle)
    edges = invoke("derive_dependency_edges", vector["bundle"], handle)
    proof_refs = invoke("derive_raw_proof_requirements", vector["bundle"], handle)
    closure = rt13["capabilityClosure"]["semanticClosure"]
    binding_rows = closure["semanticObjectBindings"]
    encoded = [invoke("encode_semantic_object_binding", row)
               for row in binding_rows]
    expected_requirements = {
        row["recordCasRef"]: row["requiredForCapability"] for row in proof_refs
    }
    targets = {edge["toRef"] for edge in edges}
    seeds = {ref: capability for ref, capability in expected_requirements.items()
             if ref not in targets}
    transitive = invoke("derive_transitive_requirements", seeds, edges)
    resolved_projection = []
    resolved_ok = set(resolved) == {row["semanticDomain"] for row in binding_rows}
    for row in binding_rows:
        entry = resolved.get(row["semanticDomain"], {})
        raw = entry.get("bytes")
        if entry.get("binding") != row or not isinstance(raw, bytes) or \
                cas(raw) != row["recordCasRef"]:
            resolved_ok = False
            continue
        resolved_projection.append({
            "semanticDomain": row["semanticDomain"],
            "binding": copy.deepcopy(row),
            "record": copy.deepcopy(entry["record"]),
            "recordBytesHex": raw.hex(),
        })
    if continuity is not True or bundle_findings != [] or \
            not resolved_ok or roots != closure["semanticRoots"] or \
            edges != closure["dependencyEdges"] or \
            proof_refs != closure["proofRefs"] or \
            transitive != expected_requirements or encoded != sorted(encoded) or \
            len(encoded) != len(set(encoded)) or set(calls) != set(names):
        raise AuthorityError("EP8 exact nine-API result/authority probe drift")
    try:
        surface.resolve_stored_evaluation({}, eas_ref)
        raise AuthorityError("EP8 raw store authority accepted")
    except TypeError:
        pass
    try:
        surface.derive_semantic_requirements({})
        raise AuthorityError("EP8 raw handle authority accepted")
    except TypeError:
        pass
    other_store = module._open_test_project_store(copy.deepcopy(fixture))
    try:
        surface.assert_store_continuity(other_store, handle)
        raise AuthorityError("EP8 cross-store handle accepted")
    except ValueError:
        pass
    call_counts = {name: calls.count(name) for name in names}
    expected_counts = {name: (2 if name == "encode_semantic_object_binding" else 1)
                       for name in names}
    if call_counts != expected_counts:
        raise AuthorityError("EP8 exact call-count receipt drift")
    results = {
        "storeContinuity": True,
        "bundleValidationFindings": [],
        "semanticObjectBindings": copy.deepcopy(binding_rows),
        "resolvedSemanticObjects": resolved_projection,
        "semanticRoots": copy.deepcopy(roots),
        "dependencyEdges": copy.deepcopy(edges),
        "rawProofRequirements": copy.deepcopy(proof_refs),
        "transitiveRequirements": copy.deepcopy(transitive),
        "semanticBindingEncodingSha256": [sha256(row) for row in encoded],
    }
    receipt = {
        "schemaVersion": 1,
        "kind": "VERIFIED_EP8_DERIVATION",
        "projectId": vector["bundle"]["projectId"],
        "acceptedVectorId": vector["id"],
        "sourceArtifactSha256": PINS[EP8],
        "sourceCheckerSha256": PINS[EP8_CHECKER],
        "requiredCheckerApi": list(names),
        "exactCallCounts": call_counts,
        "fixtureProjectionCommitment": fixture_projection[
            "projectionCommitment"],
        "results": results,
        "resultsCommitment": cas(compact(results, sort_keys=True)),
    }
    receipt["receiptCommitment"] = cas(compact(receipt, sort_keys=True))
    return receipt


class FrozenAuthority:
    def __init__(self) -> None:
        self.buffers: Mapping[str, bytes] = {}
        self.identities: dict[str, tuple[int, int, int, int]] = {}
        self.parsed: dict[str, Any] = {}
        self.modules: dict[str, types.ModuleType] = {}
        self.read_counts: dict[str, int] = {}
        self.interposition_receipts: dict[str, dict[str, Any]] = {}
        self.ep8_receipt_data: dict[str, Any] | None = None
        self.fixture_projection_data: dict[str, Any] | None = None
        self.temporary_module_receipts: dict[str, dict[str, Any]] = {}
        self.pre_exec_read_counts: dict[str, int] = {}
        self.pyc_before: dict[str, tuple[int, int, int, int]] = {}

    @staticmethod
    def _identity(path: pathlib.Path) -> tuple[int, int, int, int]:
        stat = path.stat()
        return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns

    @staticmethod
    def _path_for(name: str) -> pathlib.Path:
        base = HERE.parent if name == ARCHITECTURE_PLAN else HERE
        return (base / name).resolve(strict=True)

    def _pyc_state(self) -> dict[str, tuple[int, int, int, int]]:
        cache = HERE / "__pycache__"
        if not cache.is_dir():
            return {}
        return {str(path.resolve()): self._identity(path)
                for path in cache.glob("*.pyc")}

    def freeze(self) -> None:
        if not (sys.flags.isolated == 1 and sys.flags.ignore_environment == 1 and
                sys.flags.no_user_site == 1 and sys.flags.dont_write_bytecode):
            raise AuthorityError("isolated no-pyc interpreter flags drifted")
        resolved_seen: set[pathlib.Path] = set()
        staged: dict[str, bytes] = {}
        self.pyc_before = self._pyc_state()
        for name, expected in PINS.items():
            path = self._path_for(name)
            if path in resolved_seen:
                raise AuthorityError(f"dependency alias escaped read-once rule: {name}")
            resolved_seen.add(path)
            before = self._identity(path)
            source = path.read_bytes()
            self.read_counts[name] = self.read_counts.get(name, 0) + 1
            after = self._identity(path)
            if before != after:
                raise AuthorityError(f"dependency changed while read: {name}")
            if sha256(source) != expected:
                raise AuthorityError(f"dependency hash drift: {name}")
            self.identities[name] = before
            staged[name] = source
        if set(self.read_counts) != set(PINS) or \
                any(count != 1 for count in self.read_counts.values()):
            raise AuthorityError("dependency content read count is not exactly one")
        self.buffers = MappingProxyType(staged)
        self.pre_exec_read_counts = dict(self.read_counts)

        for name in PINS:
            if name.endswith(".json"):
                self.parsed[name] = parse_pinned_json_bytes(self.buffers[name], name)
        for name in (RT20, RT20_ADJUDICATION, RT20_REVIEW,
                     RT16, RT16_ADJUDICATION, RT16_REVIEW,
                     RT15, RT15_ADJUDICATION, RT15_REVIEW, EP8, EP8_REVIEW,
                     RT13, RT14, RT14_REVIEW, D9, D9_REVIEW):
            self.parsed[name] = parse_json_bytes(self.buffers[name], name)
        self._validate_reviews()

        sys_path_before = tuple(sys.path)
        cwd_before = os.getcwd()
        local_modules_before = {name for name in sys.modules
                                if name.startswith("verified_") or
                                name.startswith("opensip_check_")}
        for name in (RT13_CHECKER, RT_CORE, RT14_CHECKER):
            self.modules[name] = self._execute_verified(name)
        self._build_ep8_closure()
        self._build_d9_closure()
        if tuple(sys.path) != sys_path_before or os.getcwd() != cwd_before:
            raise AuthorityError("verified source execution changed cwd or sys.path")
        local_modules_after = {name for name in sys.modules
                               if name.startswith("verified_") or
                               name.startswith("opensip_check_")}
        if local_modules_after != local_modules_before:
            raise AuthorityError("local verified source entered sys.modules")
        if self.read_counts != self.pre_exec_read_counts:
            raise AuthorityError("verified execution performed a nested content read")
        if self._pyc_state() != self.pyc_before:
            raise AuthorityError("pyc state changed during verified execution")

    def _validate_reviews(self) -> None:
        ep_review = self.parsed[EP8_REVIEW]
        rt14_review = self.parsed[RT14_REVIEW]
        d9_review = self.parsed[D9_REVIEW]
        rt15_review = self.parsed[RT15_REVIEW]
        rt16_review = self.parsed[RT16_REVIEW]
        rt20_review = self.parsed[RT20_REVIEW]
        if ep_review.get("verdict", {}).get("decision") != "PASS":
            raise AuthorityError("EP8/RT13 joint review is not PASS")
        verdict14 = rt14_review.get("verdict", {})
        blockers14 = rt14_review.get("blockingFindings")
        if verdict14.get("decision") != "REJECTED-BY-DEPENDENCY" or \
                not isinstance(blockers14, list) or len(blockers14) != 1 or \
                blockers14[0].get("id") != "RT14-PF-01-REJECTED-D9-AUTHORITY":
            raise AuthorityError("RT14 dependency rejection binding drift")
        verdict9 = d9_review.get("verdict", {})
        if verdict9.get("decision") != "PASS" or \
                verdict9.get("blockingFindingCount") != 0 or \
                d9_review.get("blockingFindings") != []:
            raise AuthorityError("D9 v1.13 PASS binding drift")
        subjects = d9_review.get("reviewBinding", {}).get("exactSubjects", [])
        observed = {row.get("path"): row.get("sha256") for row in subjects
                    if isinstance(row, dict)}
        if observed != {D9: PINS[D9], D9_CHECKER: PINS[D9_CHECKER]}:
            raise AuthorityError("D9 exact review subjects drift")
        d9_window = d9_review.get("hashWindow", {}).get("start", {})
        if len(d9_window) != 28 or any(PINS.get(name) != digest
                                      for name, digest in d9_window.items()):
            raise AuthorityError("D9 28-input review window drift")

        verdict15 = rt15_review.get("verdict", {})
        finding_ids = [row.get("id") for row in rt15_review.get(
            "blockingFindings", []) if isinstance(row, dict)]
        if verdict15.get("decision") != "REJECT" or \
                verdict15.get("blockingFindingCount") != 2 or finding_ids != [
                    "RT15-PF-01-VERIFIED-SNAPSHOT-CLOSURE-ESCAPE",
                    "RT15-PF-02-D9-CONSUMER-ORACLE-NOT-PINNED-IMPLEMENTATION",
                ]:
            raise AuthorityError("RT15 exact two-blocker review binding drift")
        rt15_subjects = {row.get("path"): row.get("sha256")
                         for row in rt15_review.get("exactSubjects", [])
                         if isinstance(row, dict)}
        if rt15_subjects != {
                RT15: PINS[RT15], RT15_CHECKER: PINS[RT15_CHECKER],
                RT15_ADJUDICATION: PINS[RT15_ADJUDICATION]}:
            raise AuthorityError("RT15 review exact subjects drift")
        window_rows = rt15_review.get("inputHashWindow", {}).get("rows", [])
        if len(window_rows) != 15 or any(
                row.get("startSha256") != row.get("endSha256") or
                PINS.get(row.get("path")) != row.get("startSha256")
                for row in window_rows if isinstance(row, dict)):
            raise AuthorityError("RT15 review hash window drift")

        verdict16 = rt16_review.get("verdict", {})
        finding_ids16 = [row.get("id") for row in rt16_review.get(
            "blockingFindings", []) if isinstance(row, dict)]
        if verdict16.get("decision") != "REJECT" or \
                verdict16.get("blockingFindingCount") != 3 or finding_ids16 != [
                    "RT16-PF-01-RETURNED-SNAPSHOT-D9-AND-RT14-REACHABLE",
                    "RT16-PF-02-RETURNED-EP8-ADAPTER-SURFACE-INCOMPLETE",
                    "RT16-PF-03-D9-V110-DATACLASS-SEMANTICS-INTERPOSED",
                ]:
            raise AuthorityError("RT16 exact three-blocker review binding drift")
        rt16_subjects = {row.get("path"): row.get("sha256")
                         for row in rt16_review.get("exactSubjects", [])
                         if isinstance(row, dict)}
        if rt16_subjects != {
                RT16: PINS[RT16], RT16_CHECKER: PINS[RT16_CHECKER],
                RT16_ADJUDICATION: PINS[RT16_ADJUDICATION]}:
            raise AuthorityError("RT16 review exact subjects drift")
        hash_window16 = rt16_review.get("inputHashWindow", {})
        if hash_window16.get("result") != \
                "PASS/NO-INPUT-HASH-OR-IDENTITY-DRIFT" or \
                hash_window16.get("frozenDependencyCount") != 47:
            raise AuthorityError("RT16 frozen review hash window drift")

        verdict20 = rt20_review.get("verdict", {})
        finding_ids20 = [row.get("id") for row in rt20_review.get(
            "blockingFindings", []) if isinstance(row, dict)]
        if rt20_review.get("decision") != "REJECT" or \
                verdict20.get("decision") != "REJECT" or \
                verdict20.get("blockingFindingCount") != 1 or \
                finding_ids20 != [
                    "RT20-PF-01-INDEPENDENT-SEMANTIC-CHILD-DENOMINATOR-INCOMPLETE",
                ]:
            raise AuthorityError("RT20 exact one-blocker review binding drift")
        subject_rows20 = rt20_review.get(
            "exactByteReviewBasis", {}).get("subjects", [])
        subjects20: dict[str, str] = {}
        for row in subject_rows20:
            if not isinstance(row, dict) or \
                    row.get("sha256AtStart") != row.get("sha256AtEnd"):
                raise AuthorityError("RT20 review subject window drift")
            subjects20[row.get("path")] = row.get("sha256AtStart")
        if subjects20 != {
                RT20: PINS[RT20], RT20_CHECKER: PINS[RT20_CHECKER],
                RT20_ADJUDICATION: PINS[RT20_ADJUDICATION]}:
            raise AuthorityError("RT20 review exact subjects drift")
        if rt20_review.get("exactByteReviewBasis", {}).get(
                "inputHashDrift") is not False or \
                rt20_review.get("exactByteReviewBasis", {}).get(
                "inputIdentityDrift") is not False:
            raise AuthorityError("RT20 review input window drift")
        retained20 = rt20_review.get("retainedGateResults", {})
        lineage20 = retained20.get("predecessorAndPinLineage", {})
        raw20 = retained20.get("rawFixturesLeasesPurgeAndRoots", {})
        if lineage20.get("pinCorruptions") != \
                "55/55 refused before validation callback" or \
                lineage20.get("physicalAlias") != "REFUSED" or \
                lineage20.get("result") != "PASS" or \
                retained20.get("ep8", {}).get("result") != "PASS-RETAINED" or \
                retained20.get("d9", {}).get("result") != "PASS-RETAINED" or \
                raw20.get("result") != "PASS-RETAINED":
            raise AuthorityError("RT20 retained narrow-pass binding drift")

    def _execute_verified(self, name: str) -> types.ModuleType:
        source = self.buffers[name]
        module = types.ModuleType("verified_" + name.replace(".", "_").replace("-", "_"))
        module.__file__ = f"<verified:{name}>"
        module.__dict__["__verified_source_sha256__"] = PINS[name]
        code = compile(source, module.__file__, "exec", dont_inherit=True, optimize=0)
        exec(code, module.__dict__)
        return module

    @staticmethod
    def _interposition_node(source: bytes, name: str,
                            spec: Mapping[str, str]) -> tuple[ast.AST, int]:
        tree = ast.parse(source.decode("utf-8"), name)
        matches: list[ast.AST] = []
        kind = spec["kind"]
        target = spec["target"]
        for node in ast.walk(tree):
            if kind in ("eager-function", "eager-loader-method") and \
                    isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                    isinstance(node.targets[0], ast.Name) and \
                    node.targets[0].id == target:
                matches.append(node)
        if len(matches) != 1:
            raise AuthorityError(
                f"{name}: interposition selector matched {len(matches)} targets")
        node = matches[0]
        digest = sha256(ast.dump(node, include_attributes=False).encode("utf-8"))
        if digest != spec["astSha256"]:
            raise AuthorityError(f"{name}: interposition target AST drift")
        return node, node.lineno

    def _execute_interposed(self, name: str, replacement: Any) -> types.ModuleType:
        spec = D9_INTERPOSITION_SPECS.get(name)
        if spec is None:
            raise AuthorityError(f"{name}: undeclared interposition")
        source = self.buffers[name]
        _node, target_line = self._interposition_node(source, name, spec)
        module = types.ModuleType("verified_" + name.replace(".", "_").replace("-", "_"))
        module.__file__ = f"<verified:{name}>"
        module.__dict__["__verified_source_sha256__"] = PINS[name]
        code = compile(source, module.__file__, "exec", dont_inherit=True, optimize=0)
        if sys.gettrace() is not None:
            raise AuthorityError("preexisting trace would broaden interposition boundary")
        fired = 0
        restored = 0
        restore: Callable[[], None] | None = None

        def tracer(frame: Any, event: str, _arg: Any) -> Any:
            nonlocal fired, restored, restore
            if frame.f_code is not code or event != "line":
                return tracer
            if restore is not None and frame.f_lineno != target_line:
                restore()
                restore = None
                restored += 1
            if frame.f_lineno != target_line:
                return tracer
            if fired:
                # Decorated class statements can report the decorator source
                # line again while completing the same statement. The AST
                # target remains one statement and receives no second patch.
                return tracer
            kind = spec["kind"]
            if kind == "eager-function":
                seam = spec["seam"]
                original = frame.f_globals.get(seam)
                if not callable(original):
                    raise AuthorityError(f"{name}: eager function seam absent")
                frame.f_globals[seam] = lambda: replacement
                restore = lambda: frame.f_globals.__setitem__(seam, original)
            elif kind == "eager-loader-method":
                loader = frame.f_globals.get("DeferredAuthorityLoader")
                original = getattr(loader, "load", None)
                if not callable(original):
                    raise AuthorityError(f"{name}: eager loader seam absent")
                setattr(loader, "load", lambda _self: replacement)
                restore = lambda: setattr(loader, "load", original)
            else:
                raise AuthorityError(f"{name}: unknown interposition kind")
            fired += 1
            return tracer

        sys.settrace(tracer)
        try:
            exec(code, module.__dict__)
        finally:
            sys.settrace(None)
            if restore is not None:
                restore()
                restore = None
                restored += 1
        if fired != 1 or restored != 1:
            raise AuthorityError(
                f"{name}: interposition receipt fired={fired} restored={restored}")
        target = spec["target"]
        if target in ("V16", "V17") and getattr(module, target, None) is not replacement:
            raise AuthorityError(f"{name}: eager function did not consume replacement")
        if target == "_BOOTSTRAP_AUTHORITY" and \
                getattr(module, target, None) is not replacement:
            raise AuthorityError(f"{name}: eager loader did not consume replacement")
        self.interposition_receipts[name] = {
            "kind": spec["kind"], "target": target,
            "astSha256": spec["astSha256"], "matchCount": 1,
            "firedCount": fired, "restoredCount": restored,
        }
        return module

    def _execute_registered_exact(self, name: str) -> types.ModuleType:
        """Execute exact bytes with real module/dataclass semantics, then remove."""
        source = self.buffers[name]
        digest = PINS[name]
        stem = "".join(ch if ch.isalnum() else "_" for ch in name)
        module_name = f"verified_{stem}_{digest[:24]}"
        if module_name in sys.modules:
            raise AuthorityError(f"temporary verified module collision: {module_name}")
        module = types.ModuleType(module_name)
        module.__file__ = f"<verified:{name}:{digest}>"
        module.__dict__["__verified_source_sha256__"] = digest
        code = compile(source, module.__file__, "exec", dont_inherit=True, optimize=0)
        inserted = False
        poisoned = False
        try:
            sys.modules[module_name] = module
            inserted = True
            if sys.modules.get(module_name) is not module:
                raise AuthorityError("temporary module insertion identity drift")
            exec(code, module.__dict__)
            if sys.modules.get(module_name) is not module:
                poisoned = True
                raise AuthorityError("temporary module mapping poisoned during exec")
        finally:
            if inserted and sys.modules.get(module_name) is not module:
                poisoned = True
            if inserted:
                sys.modules.pop(module_name, None)
            if module_name in sys.modules:
                raise AuthorityError("temporary module restoration failed")
        if poisoned:
            raise AuthorityError("temporary module identity was not stable")
        authority_type = getattr(module, "Authority", None)
        fields = tuple(getattr(authority_type, "__dataclass_fields__", {}))
        params = getattr(authority_type, "__dataclass_params__", None)
        expected_fields = (
            "snapshots", "predecessor", "predecessor_review", "rt14",
            "rt14_review", "v19_checker", "v19_authority",
        )
        if not dataclasses.is_dataclass(authority_type) or \
                fields != expected_fields or params is None or not params.frozen or \
                tuple(inspect.signature(authority_type).parameters) != expected_fields:
            raise AuthorityError("v1.10 real frozen dataclass semantics drift")
        shared = {
            "snapshots": MappingProxyType({"probe": b"exact"}),
            "predecessor": {"version": "v1.9"},
            "predecessor_review": {"decision": "PASS"},
            "rt14": {"version": 14},
            "rt14_review": {"decision": "REJECTED-BY-DEPENDENCY"},
            "v19_checker": types.SimpleNamespace(name="v1.9"),
            "v19_authority": types.SimpleNamespace(name="authority"),
        }
        left = authority_type(**shared)
        right = authority_type(**shared)
        frozen_rejected = False
        try:
            left.predecessor = {}
        except dataclasses.FrozenInstanceError:
            frozen_rejected = True
        if left != right or not repr(left).startswith("Authority(") or \
                not frozen_rejected:
            raise AuthorityError("v1.10 generated dataclass behavior drift")
        self.temporary_module_receipts[name] = {
            "sourceSha256": digest, "moduleName": module_name,
            "collisionChecked": True, "identityStableDuringExec": True,
            "restoredToAbsent": True, "isDataclass": True, "frozen": True,
            "orderedFields": list(expected_fields), "generatedEquality": True,
            "generatedRepr": True, "frozenMutationRejected": True,
        }
        return module

    def _snapshot_name(self, value: Any, allowed: set[str]) -> str:
        try:
            name = pathlib.Path(value).name
        except TypeError as exc:
            raise AuthorityError("snapshot lookup is not path-like") from exc
        if name not in allowed or name not in self.buffers:
            raise AuthorityError(f"unknown snapshot input requested: {name}")
        return name

    def _snapshot_json(self, value: Any, allowed: set[str]) -> Any:
        name = self._snapshot_name(value, allowed)
        return copy.deepcopy(self.parsed[name])

    def _snapshot_hash(self, value: Any, allowed: set[str]) -> str:
        name = self._snapshot_name(value, allowed)
        return PINS[name]

    def _build_ep8_closure(self) -> None:
        ep5 = self._execute_verified(EP5_CHECKER)
        c2mod = self._execute_verified(C2_CHECKER)
        rimod = self._execute_verified(RI_CHECKER)
        ep6 = self._execute_verified(EP6_CHECKER)
        ep7 = self._execute_verified(EP7_CHECKER)
        ep8 = self._execute_verified(EP8_CHECKER)
        source_modules = {
            EP5_CHECKER: ep5, C2_CHECKER: c2mod, RI_CHECKER: rimod,
            EP6_CHECKER: ep6, EP7_CHECKER: ep7, EP8_CHECKER: ep8,
        }
        ep6_allowed = set(ep6.PINNED)
        ep7_allowed = set(ep7.PINNED)
        ep8_allowed = set(ep8.PINNED)
        if ep6_allowed != {EP5, EP5_CHECKER, C2, C2_CHECKER, RI,
                           RI_CHECKER, FACT_PLANE} or \
                ep7_allowed != {EP6, EP6_CHECKER} or \
                ep8_allowed != {EP7, EP7_CHECKER}:
            raise AuthorityError("EP8 transitive declared pin closure drift")

        def module_lookup(filename: str, _synthetic: str) -> types.ModuleType:
            if filename not in source_modules:
                raise AuthorityError(f"unknown in-memory module requested: {filename}")
            return source_modules[filename]

        all_data = {EP8, EP7, EP6, EP5, C2, RI, FACT_PLANE}
        c2mod.load = lambda name: self._snapshot_json(name, all_data)
        rimod.load = lambda name: self._snapshot_json(name, all_data)
        ep5._ACTIVE_GRAMMAR = copy.deepcopy(
            self.parsed[EP5]["normativePreimageGrammar"])
        ep5._load_module = lambda path, name: module_lookup(
            pathlib.Path(path).name, name)
        ep5._load_c2_module = lambda: c2mod
        ep5._sha256_file = lambda path: self._snapshot_hash(path, all_data)
        ep5._load = lambda path: self._snapshot_json(path, all_data)

        ep6.load_json = lambda path: self._snapshot_json(path, ep6_allowed)
        ep6.sha_file = lambda path: self._snapshot_hash(path, ep6_allowed)
        ep6._load_module = module_lookup
        ep6._EP5, ep6._C2, ep6._RI = ep5, c2mod, rimod
        ep7.load_json = lambda path: self._snapshot_json(path, ep7_allowed)
        ep7.sha_file = lambda path: self._snapshot_hash(path, ep7_allowed)
        ep7._load_module = module_lookup
        ep7._EP6 = ep6
        ep8.load_json = lambda path: self._snapshot_json(path, ep8_allowed)
        ep8.sha_file = lambda path: self._snapshot_hash(path, ep8_allowed)
        ep8._load_module = module_lookup
        ep8._EP7 = ep7

        before = dict(self.read_counts)
        old_cwd = os.getcwd()
        try:
            os.chdir("/")
            ep8._EP7 = None
            if ep8._ep7() is not ep7:
                raise AuthorityError("delayed EP8->EP7 resolution escaped snapshot")
            ep7._EP6 = None
            if ep7._ep6() is not ep6:
                raise AuthorityError("delayed EP7->EP6 resolution escaped snapshot")
            ep6._EP5 = ep6._C2 = ep6._RI = None
            if ep6._modules() != (ep5, c2mod, rimod):
                raise AuthorityError("delayed EP6 module resolution escaped snapshot")
            ep_findings = ep8.check(copy.deepcopy(self.parsed[EP8]))
        finally:
            os.chdir(old_cwd)
        if ep_findings:
            raise AuthorityError(f"authenticated EP8 checker failed: {ep_findings[0]}")
        if self.read_counts != before:
            raise AuthorityError("EP8 internal invocation changed outer read counters")
        self.modules.update(source_modules)
        self.fixture_projection_data = _fixture_projection(self.parsed[RT16])
        self.ep8_receipt_data = _exercise_exact_ep8_surface(
            self, ep8, self.fixture_projection_data)

    def _build_d9_closure(self) -> None:
        v16 = self._execute_verified("check-d9.py")
        v17 = self._execute_interposed("check-d9-v1.7.py", v16)
        v18 = self._execute_interposed("check-d9-v1.8.py", v17)
        v18._sha_file = lambda name: self._snapshot_hash(name, set(v18.PINS))
        v110 = self._execute_registered_exact("check-d9-v1.10.py")
        snapshots = self.buffers
        v111_authority = types.SimpleNamespace(
            snapshots=snapshots,
            predecessor=self.parsed["d9-exit-contract.v1.10.json"],
            predecessor_review=self.parsed[
                "d9-exit-contract.v1.10.review-independent-prefreeze.json"],
            rt14=self.parsed[RT14], rt14_review=self.parsed[RT14_REVIEW],
            v18=self.parsed["d9-exit-contract.v1.8.json"],
            v17=self.parsed["d9-exit-contract.v1.7.json"],
            v16=self.parsed["d9-exit-contract.v1.6.json"],
            v110_checker=v110, v110_authority=None,
            v18_checker=v18, v17_checker=v17, v16_checker=v16,
        )
        v111 = self._execute_interposed("check-d9-v1.11.py", v111_authority)
        v112_authority = types.SimpleNamespace(
            snapshots=snapshots,
            predecessor=self.parsed["d9-exit-contract.v1.11.json"],
            predecessor_review=self.parsed[
                "d9-exit-contract.v1.11.review-independent-prefreeze.json"],
            v110=self.parsed["d9-exit-contract.v1.10.json"],
            rt14=self.parsed[RT14], rt14_review=self.parsed[RT14_REVIEW],
            v18=self.parsed["d9-exit-contract.v1.8.json"],
            v17=self.parsed["d9-exit-contract.v1.7.json"],
            v16=self.parsed["d9-exit-contract.v1.6.json"],
            v111_checker=v111, v111_authority=v111_authority,
            v18_checker=v18, v17_checker=v17, v16_checker=v16,
        )
        v112 = self._execute_interposed("check-d9-v1.12.py", v112_authority)
        v113_authority = types.SimpleNamespace(
            snapshots=snapshots,
            predecessor=self.parsed["d9-exit-contract.v1.12.json"],
            predecessor_review=self.parsed[
                "d9-exit-contract.v1.12.review-independent-prefreeze.json"],
            v112_checker=v112, v112_authority=v112_authority,
        )
        v113 = self._execute_interposed(D9_CHECKER, v113_authority)
        if v113.V17 is not v17 or v113.V17.V16 is not v16:
            raise AuthorityError("authenticated D9 V17.V16 chain identity drift")
        required = ("derive_class", "derive_codes", "reduce_concurrent", "check")
        if any(not callable(getattr(v113, name, None)) for name in required) or \
                not callable(getattr(v113.V17.V16, "derive_class", None)):
            raise AuthorityError("authenticated D9 public API is incomplete")
        retained = v113.check(
            copy.deepcopy(self.parsed["d9-exit-contract.v1.8.json"]),
            copy.deepcopy(self.parsed["d9-exit-contract.v1.7.json"]),
            copy.deepcopy(self.parsed["d9-exit-contract.v1.6.json"]),
        )
        if retained:
            raise AuthorityError(f"authenticated D9 check export failed: {retained[0]}")
        self.modules.update({
            "check-d9.py": v16, "check-d9-v1.7.py": v17,
            "check-d9-v1.8.py": v18, "check-d9-v1.10.py": v110,
            "check-d9-v1.11.py": v111, "check-d9-v1.12.py": v112,
            D9_CHECKER: v113,
        })

    def end_stat_check(self) -> None:
        for name, identity in self.identities.items():
            if self._identity(self._path_for(name)) != identity:
                raise AuthorityError(f"dependency metadata changed after snapshot: {name}")
        if self.read_counts != self.pre_exec_read_counts or \
                set(self.read_counts) != set(PINS) or \
                any(count != 1 for count in self.read_counts.values()):
            raise AuthorityError("dependency was reread")
        if self._pyc_state() != self.pyc_before:
            raise AuthorityError("pyc state changed after snapshot")


def _component(tag: int, value: str) -> bytes:
    data = value.encode("utf-8")
    return bytes([tag]) + len(data).to_bytes(4, "big") + data


def _blob(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + len(value).to_bytes(4, "big") + value


def encode_raw_key(item: Mapping[str, str]) -> bytes:
    return _blob(
        0x75,
        _component(0x76, item["recordCasRef"])
        + _component(0x77, item["projectId"])
        + _component(0x78, item["recordKind"]),
    )


def _object_refs_blob(object_refs: list[dict[str, str]]) -> bytes:
    rows = sorted(encode_raw_key(item) for item in object_refs)
    if len(rows) != len(set(rows)):
        raise ValueError("duplicate raw object key")
    return _blob(0x79, b"".join(rows))


def derive_unit_id(project_id: str, capability: str,
                   object_refs: list[dict[str, str]]) -> str:
    preimage = (
        b"opensip.semantic-custody-unit-id.v3\x00\x70"
        + _component(0x72, project_id)
        + _component(0x74, capability)
        + _object_refs_blob(object_refs)
    )
    return "unit3:sha256:" + sha256(preimage)


def encode_unit(unit: Mapping[str, Any]) -> bytes:
    return (
        b"\x70" + _component(0x71, unit["unitId"])
        + _component(0x72, unit["projectId"])
        + _component(0x74, unit["requiredForCapability"])
        + _object_refs_blob(unit["objectRefs"])
    )


def _merkle(items: list[bytes]) -> bytes:
    ordered = sorted(set(items))
    if not ordered:
        return hashlib.sha256(b"\x02" + _blob(0x30, b"opensip.evaluation-proof.v2")).digest()
    level = [hashlib.sha256(b"\x00" + len(item).to_bytes(8, "big") + item).digest()
             for item in ordered]
    while len(level) > 1:
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            if index + 1 < len(level) else level[index]
            for index in range(0, len(level), 2)
        ]
    return level[0]


def semantic_closure_commitment(units: list[dict[str, Any]]) -> str:
    root = _merkle([encode_unit(unit) for unit in units])
    preimage = (
        b"\x30" + _blob(0x31, b"opensip.evaluation-proof.v2")
        + _blob(0x32, b"semantic-capability-closure-v3")
        + _blob(0x33, root)
    )
    return cas(preimage)


def derive_operational_projection(
        closure: dict[str, Any], source_bundle_ref: str,
        source_closure_ref: str) -> tuple[dict[str, Any], bytes, str, str]:
    units: list[dict[str, Any]] = []
    for source in closure["units"]:
        refs = sorted(copy.deepcopy(source["objectRefs"]), key=encode_raw_key)
        units.append({
            "unitId": source["unitId"], "projectId": source["projectId"],
            "requiredForCapability": source["requiredForCapability"],
            "objectRefs": refs,
        })
    units.sort(key=encode_unit)
    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for unit in units:
        for row in unit["objectRefs"]:
            key = row["projectId"], row["recordCasRef"], row["recordKind"]
            if key in unique:
                raise ValueError("operational projection has duplicate unit owner")
            unique[key] = copy.deepcopy(row)
    required = sorted(unique.values(), key=encode_raw_key)
    projection = {
        "schemaVersion": 1,
        "projectId": closure["projectId"],
        "sourceEvaluationProofBundleCasRef": source_bundle_ref,
        "sourceSemanticCapabilityClosureCasRef": source_closure_ref,
        "sourceSemanticCapabilityClosureCommitment": closure["closureCommitment"],
        "normalizationAlgorithm": "OPEN-SIP-OPERATIONAL-CUSTODY-KEY-ORDER-V1",
        "operationalUnits": units,
        "requiredObjectRefs": required,
    }
    encoded = compact(projection)
    return projection, encoded, cas(encoded), domain_digest(
        "opensip.operational-custody-projection.v1", encoded,
    )


RECORD_TYPES: dict[str, dict[str, Any]] = {
    "source-bytes": {
        "expectedValueType": "FixtureSourceBytesRecordV1",
        "selector": "/sourcePath", "idField": "sourcePath",
        "selectedValueType": "FixtureSourcePathV1",
    },
    "predicate-semantics": {
        "expectedValueType": "FixturePredicateSemanticsRecordV1",
        "selector": "/predicateId", "idField": "predicateId",
        "selectedValueType": "FixturePredicateIdV1",
    },
    "policy": {
        "expectedValueType": "FixturePolicyRecordV1",
        "selector": "/policyId", "idField": "policyId",
        "selectedValueType": "FixturePolicyIdV1",
    },
    "fact": {
        "expectedValueType": "FixtureFactRecordV1",
        "selector": "/factId", "idField": "factId",
        "selectedValueType": "FixtureFactIdV1",
    },
    "coverage": {
        "expectedValueType": "FixtureCoverageRecordV1",
        "selector": "/coverageId", "idField": "coverageId",
        "selectedValueType": "FixtureCoverageIdV1",
    },
    "replay-plan": {
        "expectedValueType": "FixtureReplayPlanRecordV1",
        "selector": "/planId", "idField": "planId",
        "selectedValueType": "FixtureReplayPlanIdV1",
    },
    "resolved-activation-graph": {
        "expectedValueType": "FixtureResolvedActivationGraphRecordV1",
        "selector": "/graphId", "idField": "graphId",
        "selectedValueType": "FixtureGraphIdV1",
    },
}
RECORD_COMMON_PREFIX = ["schemaVersion", "projectId", "recordKind"]
RECORD_COMMON_SUFFIX = [
    "requiredCapability", "unitLabel", "dependencies", "payload",
]
DEPENDENCY_FIELDS = ["projectId", "recordCasRef", "recordKind", "role"]
REQUEST_FIELDS = [
    "projectId", "recordCasRef", "recordKind", "expectedValueType",
    "selector", "requiredCapability",
]
RESULT_FIELDS = [
    "schemaVersion", "kind", "projectId", "recordCasRef", "recordKind",
    "expectedValueType", "selector", "requiredCapability",
    "validatedByteLength", "validatedDigest", "validatedBytesHex",
    "selectedValueType", "selectedValue",
]


def _closed_object(value: Any, fields: list[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or list(value) != fields:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", f"{label} ordered fields")
    return value


def validate_raw_object_resolution(raw_bytes: Any, request: Any) -> dict[str, Any]:
    """Pure RawObjectResolutionConformanceV1 validation in normative order."""
    if type(raw_bytes) is not bytes or len(raw_bytes) == 0:
        raise ResolutionError("BYTES_NOT_PRESENT", "nonempty immutable bytes required")

    # Length and digest are computed before any parse or selector use.  The
    # bounded UInt64 length and digest-to-CAS equality are the complete physical
    # integrity gate for this API; no identity or receipt substitutes for bytes.
    length = len(raw_bytes)
    if length > 2**64 - 1:
        raise ResolutionError("BYTE_LENGTH_INVALID", "length exceeds UInt64")
    digest = sha256(raw_bytes)
    if not isinstance(request, dict) or list(request) != REQUEST_FIELDS:
        raise ResolutionError("REQUEST_SHAPE_MISMATCH", "closed request fields")
    expected_ref = request.get("recordCasRef")
    if not isinstance(expected_ref, str) or not REF_RE.fullmatch(expected_ref) or \
            expected_ref != "sha256:" + digest:
        raise ResolutionError("CAS_MISMATCH", "SHA-256(raw bytes) differs from recordCasRef")

    try:
        record = parse_json_bytes(raw_bytes, "RawObjectResolutionConformanceV1 bytes")
    except (DuplicateKeyError, FloatForbidden, ValueError, json.JSONDecodeError) as exc:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", type(exc).__name__) from exc
    kind = request.get("recordKind")
    declaration = RECORD_TYPES.get(kind) if isinstance(kind, str) else None
    if declaration is None:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "record kind is not registered")
    fields = RECORD_COMMON_PREFIX + [declaration["idField"]] + RECORD_COMMON_SUFFIX
    _closed_object(record, fields, "record")
    if record.get("schemaVersion") != 1 or type(record.get("schemaVersion")) is not int:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "schemaVersion")
    if not all(isinstance(record.get(key), str) for key in (
            "projectId", "recordKind", declaration["idField"],
            "requiredCapability", "unitLabel", "payload")):
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "record scalar types")
    dependencies = record.get("dependencies")
    if not isinstance(dependencies, list):
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependencies array")
    for index, dependency in enumerate(dependencies):
        _closed_object(dependency, DEPENDENCY_FIELDS, f"dependency[{index}]")
        if not all(isinstance(dependency.get(key), str) for key in DEPENDENCY_FIELDS):
            raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependency scalar types")
        if not PROJECT_RE.fullmatch(dependency["projectId"]) or \
                not REF_RE.fullmatch(dependency["recordCasRef"]):
            raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependency identity")

    if request.get("expectedValueType") != declaration["expectedValueType"]:
        raise ResolutionError("EXPECTED_TYPE_MISMATCH", "closed type name")
    if request.get("selector") != declaration["selector"]:
        raise ResolutionError("SELECTOR_MISMATCH", "record-specific selector")
    if request.get("projectId") != record["projectId"]:
        raise ResolutionError("PROJECT_MISMATCH", "projectId")
    if request.get("recordKind") != record["recordKind"]:
        raise ResolutionError("RECORD_KIND_MISMATCH", "recordKind")
    if request.get("requiredCapability") != record["requiredCapability"]:
        raise ResolutionError("CAPABILITY_MISMATCH", "requiredCapability")
    selected = record[declaration["idField"]]
    return {
        "schemaVersion": 1,
        "kind": "RAW_OBJECT_USABLE",
        "projectId": request["projectId"],
        "recordCasRef": request["recordCasRef"],
        "recordKind": request["recordKind"],
        "expectedValueType": request["expectedValueType"],
        "selector": request["selector"],
        "requiredCapability": request["requiredCapability"],
        "validatedByteLength": length,
        "validatedDigest": "sha256:" + digest,
        "validatedBytesHex": raw_bytes.hex(),
        "selectedValueType": declaration["selectedValueType"],
        "selectedValue": selected,
    }


def raw_key(project_id: str, record_ref: str, record_kind: str) -> dict[str, str]:
    return {
        "projectId": project_id,
        "recordCasRef": record_ref,
        "recordKind": record_kind,
    }


def _semantic_ref(domain: str, raw_bytes: bytes) -> str:
    return domain_digest("opensip.rt15.fixture-semantic-binding.v1/" + domain, raw_bytes)


def _raw_bytes_commitment(rows: list[dict[str, Any]]) -> str:
    framed = b"".join(
        len(bytes.fromhex(row["rawBytesHex"])).to_bytes(8, "big")
        + bytes.fromhex(row["rawBytesHex"])
        for row in sorted(rows, key=lambda item: item["request"]["recordCasRef"])
    )
    return domain_digest("opensip.rt15.raw-object-bytes-closure.v1", framed)


def build_fixture(fixture_id: str, project_id: str,
                  specs: list[dict[str, Any]]) -> dict[str, Any]:
    if not specs:
        raise ValueError("fixture requires records")
    built: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for spec in specs:
        name = spec["name"]
        kind = spec["kind"]
        declaration = RECORD_TYPES[kind]
        dependencies: list[dict[str, str]] = []
        for dependency_name, role in spec.get("dependencies", []):
            if dependency_name not in built:
                raise ValueError("fixture specifications must be topological")
            target = built[dependency_name]
            dependencies.append({
                **raw_key(project_id, target["recordCasRef"], target["recordKind"]),
                "role": role,
            })
        record = {
            "schemaVersion": 1,
            "projectId": project_id,
            "recordKind": kind,
            declaration["idField"]: spec["selectedValue"],
            "requiredCapability": spec["capability"],
            "unitLabel": spec["unitLabel"],
            "dependencies": dependencies,
            "payload": spec["payload"],
        }
        raw_bytes = compact(record)
        record_ref = cas(raw_bytes)
        request = {
            "projectId": project_id,
            "recordCasRef": record_ref,
            "recordKind": kind,
            "expectedValueType": declaration["expectedValueType"],
            "selector": declaration["selector"],
            "requiredCapability": spec["capability"],
        }
        result = validate_raw_object_resolution(raw_bytes, request)
        row = {
            "request": request,
            "rawBytesHex": raw_bytes.hex(),
            "expectedResult": result,
            "dependencies": copy.deepcopy(dependencies),
        }
        rows.append(row)
        built[name] = {
            "name": name, "recordCasRef": record_ref, "recordKind": kind,
            "capability": spec["capability"], "unitLabel": spec["unitLabel"],
            "root": bool(spec.get("root")), "rawBytes": raw_bytes,
            "selectedValue": spec["selectedValue"],
        }

    graph: list[dict[str, str]] = []
    for row in rows:
        for dependency in row["dependencies"]:
            graph.append({
                "fromRef": row["request"]["recordCasRef"],
                "toRef": dependency["recordCasRef"],
                "projectId": project_id,
                "role": dependency["role"],
            })
    graph.sort(key=lambda edge: (
        edge["fromRef"], edge["toRef"], edge["projectId"], edge["role"],
    ))

    proof_refs = [{
        "identityKind": "raw-cas",
        "projectId": project_id,
        "recordCasRef": item["recordCasRef"],
        "recordKind": item["recordKind"],
        "requiredForCapability": item["capability"],
    } for item in built.values()]
    proof_refs.sort(key=lambda item: encode_raw_key(item))

    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for item in built.values():
        groups.setdefault((item["capability"], item["unitLabel"]), []).append(
            raw_key(project_id, item["recordCasRef"], item["recordKind"]),
        )
    units: list[dict[str, Any]] = []
    for (capability, _label), refs in groups.items():
        ordered_refs = sorted(refs, key=encode_raw_key)
        units.append({
            "unitId": derive_unit_id(project_id, capability, ordered_refs),
            "projectId": project_id,
            "requiredForCapability": capability,
            "objectRefs": ordered_refs,
        })
    units.sort(key=encode_unit)

    bindings: list[dict[str, str]] = []
    roots: list[dict[str, str]] = []
    for item in built.values():
        if not item["root"]:
            continue
        domain = "rt15-fixture-" + item["recordKind"] + "-v1"
        semantic_ref = _semantic_ref(domain, item["rawBytes"])
        bindings.append({
            "projectId": project_id, "semanticDomain": domain,
            "semanticRef": semantic_ref, "recordCasRef": item["recordCasRef"],
            "recordKind": item["recordKind"],
        })
        roots.append({
            "identityKind": "semantic-commitment", "projectId": project_id,
            "semanticDomain": domain, "semanticRef": semantic_ref,
            "recordKind": item["recordKind"],
            "requiredForCapability": item["capability"],
        })
    bindings.sort(key=lambda item: compact(item, sort_keys=True))
    roots.sort(key=lambda item: compact(item, sort_keys=True))
    commitment = semantic_closure_commitment(units)
    closure = {
        "schemaVersion": 3,
        "projectId": project_id,
        "sealedCapability": "replayable",
        "semanticObjectBindings": bindings,
        "semanticRoots": roots,
        "proofRefs": proof_refs,
        "dependencyEdges": graph,
        "units": units,
        "closureCommitment": commitment,
    }
    closure_bytes = compact(closure, sort_keys=True)
    closure_ref = cas(closure_bytes)

    run_id = "run1:" + sha256(("opensip.rt15.fixture-run.v1\x00" + fixture_id).encode())
    availability = []
    for unit in units:
        availability.append({
            "schemaVersion": 2, "projectId": project_id, "runId": run_id,
            "unitId": unit["unitId"],
            "objectStates": [{**copy.deepcopy(key), "state": "AVAILABLE"}
                             for key in unit["objectRefs"]],
        })
    availability_fixtures = [{
        "id": fixture_id + "-ALL-AVAILABLE", "runId": run_id,
        "stateOverrides": [], "expectedEffectiveCapability": "replayable",
    }]
    availability_sha = sha256(compact({
        "unitAvailabilityRecords": availability,
        "availabilityFixtures": availability_fixtures,
    }, sort_keys=True))

    proof_bundle = {
        "schemaVersion": 1, "projectId": project_id,
        "proofRefs": proof_refs, "dependencyEdges": graph,
        "semanticRoots": roots,
    }
    proof_bundle_bytes = compact(proof_bundle, sort_keys=True)
    proof_bundle_ref = cas(proof_bundle_bytes)
    projection, projection_bytes, projection_ref, projection_digest = \
        derive_operational_projection(closure, proof_bundle_ref, closure_ref)

    snapshot_records = [{
        "recordCasRef": row["request"]["recordCasRef"],
        "rawBytesHex": row["rawBytesHex"],
    } for row in rows]
    snapshot_preimage = compact(snapshot_records, sort_keys=True)
    snapshot_id = "snapshot1:sha256:" + sha256(
        b"opensip.rt15.raw-object-snapshot.v1\x00"
        + len(snapshot_preimage).to_bytes(8, "big") + snapshot_preimage,
    )
    snapshot = {
        "schemaVersion": 1, "snapshotId": snapshot_id,
        "projectId": project_id, "records": snapshot_records,
    }
    commitment_input = {
        "proofBundleCasRef": proof_bundle_ref,
        "semanticClosureCasRef": closure_ref,
        "semanticClosureCommitment": commitment,
        "availabilityCanonicalSha256": availability_sha,
        "operationalProjectionRef": projection_ref,
        "operationalProjectionDigest": projection_digest,
        "rawObjectSnapshotId": snapshot_id,
    }
    commitments = {
        "rawBytesCommitment": _raw_bytes_commitment(rows),
        "fixtureCommitment": domain_digest(
            "opensip.rt15.raw-object-resolution-fixture.v1",
            compact(commitment_input, sort_keys=True),
        ),
    }
    return {
        "fixtureId": fixture_id,
        "status": "FIXTURE-ONLY/NEW-BYTE-DERIVED/NOT-RT13-NOMATCH",
        "projectId": project_id,
        "recordCount": len(rows),
        "unitCount": len(units),
        "resolutionRows": rows,
        "dependencyGraph": graph,
        "proofBundleCanonicalBytesHex": proof_bundle_bytes.hex(),
        "proofBundleCasRef": proof_bundle_ref,
        "semanticClosure": closure,
        "semanticClosureCanonicalBytesHex": closure_bytes.hex(),
        "semanticClosureCasRef": closure_ref,
        "unitAvailabilityRecords": availability,
        "availabilityFixtures": availability_fixtures,
        "availabilityCanonicalSha256": availability_sha,
        "operationalProjection": projection,
        "operationalProjectionCanonicalBytesHex": projection_bytes.hex(),
        "operationalProjectionRef": projection_ref,
        "operationalProjectionDigest": projection_digest,
        "rawObjectSnapshot": snapshot,
        "commitments": commitments,
    }


PRIMARY_SPECS = [
    {"name": "source", "kind": "source-bytes", "selectedValue": "src/rt15_fixture.rs",
     "capability": "replayable", "unitLabel": "replay", "dependencies": [],
     "payload": "pub fn rt15_fixture() -> bool { true }"},
    {"name": "predicate", "kind": "predicate-semantics", "selectedValue": "pred:rt15-byte-custody",
     "capability": "verifiable", "unitLabel": "verify", "dependencies": [],
     "payload": "all selected raw objects validate before semantic use"},
    {"name": "policy", "kind": "policy", "selectedValue": "policy:rt15-exact-bytes",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("predicate", "predicate-semantics")],
     "payload": "identity-only retained objects are unusable"},
    {"name": "fact", "kind": "fact", "selectedValue": "fact:rt15-source-present",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("source", "source-content")],
     "payload": "fixture source bytes are present"},
    {"name": "coverage", "kind": "coverage", "selectedValue": "coverage:rt15-byte-closure",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("fact", "coverage-fact"), ("predicate", "coverage-predicate")],
     "payload": "predicate and source fact are covered", "root": True},
    {"name": "replay", "kind": "replay-plan", "selectedValue": "plan:rt15-replay",
     "capability": "replayable", "unitLabel": "replay",
     "dependencies": [("source", "replay-source"), ("policy", "replay-policy")],
     "payload": "replay from exact selected bytes"},
    {"name": "graph", "kind": "resolved-activation-graph", "selectedValue": "graph:rt15-primary",
     "capability": "replayable", "unitLabel": "replay",
     "dependencies": [("coverage", "activation-coverage"), ("replay", "activation-replay")],
     "payload": "complete primary fixture graph", "root": True},
]

ALTERNATE_SPECS = [
    {"name": "source", "kind": "source-bytes", "selectedValue": "src/rt15_alt.rs",
     "capability": "replayable", "unitLabel": "replay-a", "dependencies": [],
     "payload": "pub const ALT: u8 = 15;"},
    {"name": "predicate", "kind": "predicate-semantics", "selectedValue": "pred:rt15-alt",
     "capability": "verifiable", "unitLabel": "verify", "dependencies": [],
     "payload": "alternate fixture predicate"},
    {"name": "fact", "kind": "fact", "selectedValue": "fact:rt15-alt",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("predicate", "fact-predicate")],
     "payload": "alternate fixture fact", "root": True},
    {"name": "replay", "kind": "replay-plan", "selectedValue": "plan:rt15-alt",
     "capability": "replayable", "unitLabel": "replay-a",
     "dependencies": [("source", "replay-source"), ("fact", "replay-fact")],
     "payload": "alternate replay plan"},
    {"name": "graph", "kind": "resolved-activation-graph", "selectedValue": "graph:rt15-alt",
     "capability": "replayable", "unitLabel": "replay-b",
     "dependencies": [("replay", "activation-replay"), ("predicate", "activation-predicate")],
     "payload": "alternate fixture graph", "root": True},
]


def synthetic_specs(record_count: int, unit_count: int) -> list[dict[str, Any]]:
    if record_count < unit_count or unit_count < 1:
        raise ValueError("invalid generated fixture cardinality")
    kinds = list(RECORD_TYPES)
    specs: list[dict[str, Any]] = []
    for index in range(record_count):
        kind = kinds[index % len(kinds)]
        declaration = RECORD_TYPES[kind]
        group_index = index % unit_count
        capability = "verifiable" if group_index % 2 == 0 else "replayable"
        dependencies = [] if index == 0 else [(f"r{index - 1}", "generated-parent")]
        specs.append({
            "name": f"r{index}", "kind": kind,
            "selectedValue": f"{declaration['idField']}:generated:{record_count}:{index}",
            "capability": capability, "unitLabel": f"unit-{group_index}",
            "dependencies": dependencies,
            "payload": f"generated payload {record_count}/{unit_count}/{index}",
            "root": index >= max(0, record_count - 2),
        })
    return specs


RAW_OBJECT_STATES = {
    "AVAILABLE", "OUTAGE", "PURGED", "EXPIRED", "CORRUPT",
    "MISSING-DEPENDENCY",
}
LEASE_STATES = {"HELD", "RELEASED", "RECLAIMED_STALE"}
STATE_FIELDS = [
    "schemaVersion", "projectId", "ledgerSequence",
    "lastIssuedFencingToken", "objects", "lease",
]
OBJECT_STATE_FIELDS = ["projectId", "state", "recordCasRef", "recordKind"]
LEASE_FIELDS = [
    "leaseId", "projectId", "ownerId", "ownerLivenessToken", "ownerAlive",
    "previousFencingToken", "fencingToken", "state", "acquiredAtSequence",
    "expiresAtSequence", "pinnedRefs", "pendingExpiryRefs",
]
EVENT_FIELDS: dict[str, list[str]] = {
    "expiry": ["kind", "projectId", "transactionBoundary", "atSequence", "targetRefs"],
    "release": ["kind", "projectId", "transactionBoundary", "atSequence",
                "leaseId", "ownerId", "fencingToken"],
    "crash-reclaim": [
        "kind", "projectId", "transactionBoundary", "atSequence", "leaseId",
        "expectedOwnerId", "expectedOwnerLivenessToken", "expectedFencingToken",
        "successorFencingToken", "scopeRefs", "observedOwnerAlive",
    ],
    "resolve-and-pin": [
        "kind", "projectId", "transactionBoundary", "atSequence", "leaseId",
        "ownerId", "ownerLivenessToken", "expectedPreviousFencingToken",
        "expiresAtSequence", "pinRefs",
    ],
}
RESULT_VARIANT_FIELDS: dict[str, list[str]] = {
    "LEASE_GRANTED": ["kind", "leaseId", "fencingToken", "idempotent"],
    "READ_CONTINUES": ["kind"],
    "EXPIRY_COMMITTED": ["kind", "expiredRefs"],
    "LEASE_RELEASED": ["kind", "leaseState", "expiryAppliedRefs"],
    "LEASE_RECLAIMED": ["kind", "leaseId", "leaseState", "expiryAppliedRefs"],
    "RETENTION_PRECONDITION_FAILED": ["kind"],
    "RETENTION_BUSY": ["kind"],
    "RETENTION_LOCAL_UNAVAILABLE": ["kind"],
}


def _validate_key(value: Any, project_id: str, label: str) -> dict[str, Any]:
    _closed_object(value, ["projectId", "recordCasRef", "recordKind"], label)
    if value["projectId"] != project_id or not REF_RE.fullmatch(value["recordCasRef"]) or \
            not isinstance(value["recordKind"], str) or not value["recordKind"]:
        raise ValueError(f"{label}: invalid raw object key")
    return value


def _validate_key_array(value: Any, project_id: str, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected array")
    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(value):
        _validate_key(row, project_id, f"{label}[{index}]")
        key = row["projectId"], row["recordCasRef"], row["recordKind"]
        if key in seen:
            raise ValueError(f"{label}: duplicate key")
        seen.add(key)
    return value


def _validate_lease_state(state: Any) -> dict[str, Any]:
    _closed_object(state, STATE_FIELDS, "LeaseStateV3")
    if state["schemaVersion"] != 3 or type(state["schemaVersion"]) is not int:
        raise ValueError("LeaseStateV3 schemaVersion")
    project_id = state["projectId"]
    if not isinstance(project_id, str) or not PROJECT_RE.fullmatch(project_id):
        raise ValueError("LeaseStateV3 projectId")
    for field in ("ledgerSequence", "lastIssuedFencingToken"):
        if type(state[field]) is not int or state[field] < 0 or state[field] > 2**64 - 1:
            raise ValueError(f"LeaseStateV3 {field}")
    if not isinstance(state["objects"], list):
        raise ValueError("LeaseStateV3 objects")
    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(state["objects"]):
        _closed_object(row, OBJECT_STATE_FIELDS, f"objects[{index}]")
        _validate_key({key: row[key] for key in ("projectId", "recordCasRef", "recordKind")},
                      project_id, f"objects[{index}]")
        if row["state"] not in RAW_OBJECT_STATES:
            raise ValueError("RawObjectStateV1 state")
        key = row["projectId"], row["recordCasRef"], row["recordKind"]
        if key in seen:
            raise ValueError("duplicate object state")
        seen.add(key)
    lease = state["lease"]
    if lease is not None:
        _closed_object(lease, LEASE_FIELDS, "LeaseRecordV2")
        if lease["projectId"] != project_id or lease["state"] not in LEASE_STATES or \
                type(lease["ownerAlive"]) is not bool:
            raise ValueError("LeaseRecordV2 project/state/ownerAlive")
        for field in ("previousFencingToken", "fencingToken", "acquiredAtSequence",
                      "expiresAtSequence"):
            if type(lease[field]) is not int or lease[field] < 0:
                raise ValueError(f"LeaseRecordV2 {field}")
        for field in ("leaseId", "ownerId", "ownerLivenessToken"):
            if not isinstance(lease[field], str) or not lease[field]:
                raise ValueError(f"LeaseRecordV2 {field}")
        _validate_key_array(lease["pinnedRefs"], project_id, "pinnedRefs")
        _validate_key_array(lease["pendingExpiryRefs"], project_id, "pendingExpiryRefs")
    return state


def _validate_event(event: Any, project_id: str, next_sequence: int) -> dict[str, Any]:
    if not isinstance(event, dict) or event.get("kind") not in EVENT_FIELDS:
        raise ValueError("unknown or malformed semantic lease event")
    kind = event["kind"]
    _closed_object(event, EVENT_FIELDS[kind], kind)
    if event["projectId"] != project_id or \
            event["transactionBoundary"] != TX_BOUNDARY or \
            type(event["atSequence"]) is not int or event["atSequence"] != next_sequence:
        raise ValueError("event project/transaction/sequence")
    array_field = {
        "expiry": "targetRefs", "release": None,
        "crash-reclaim": "scopeRefs", "resolve-and-pin": "pinRefs",
    }[kind]
    if array_field:
        _validate_key_array(event[array_field], project_id, array_field)
    integer_fields = {
        "expiry": [], "release": ["fencingToken"],
        "crash-reclaim": ["expectedFencingToken", "successorFencingToken"],
        "resolve-and-pin": ["expectedPreviousFencingToken", "expiresAtSequence"],
    }[kind]
    for field in integer_fields:
        if type(event[field]) is not int or event[field] < 0:
            raise ValueError(f"event {field}")
    if kind == "crash-reclaim" and type(event["observedOwnerAlive"]) is not bool:
        raise ValueError("event observedOwnerAlive")
    return event


def _key_tuple(row: Mapping[str, Any]) -> tuple[str, str, str]:
    return row["projectId"], row["recordCasRef"], row["recordKind"]


def _failure(prestate: dict[str, Any], kind: str) -> dict[str, Any]:
    return {"schemaVersion": 3, "state": copy.deepcopy(prestate), "result": {"kind": kind}}


def reduce_semantic_lease_v3(state: Any, event: Any) -> dict[str, Any]:
    _validate_lease_state(state)
    _validate_event(event, state["projectId"], state["ledgerSequence"] + 1)
    current = copy.deepcopy(state)
    objects = {_key_tuple(row): row for row in current["objects"]}
    lease = current["lease"]
    kind = event["kind"]

    if kind == "resolve-and-pin":
        requested = {_key_tuple(row) for row in event["pinRefs"]}
        if lease is not None and lease["state"] == "HELD":
            same = (
                lease["leaseId"] == event["leaseId"]
                and lease["ownerId"] == event["ownerId"]
                and lease["ownerLivenessToken"] == event["ownerLivenessToken"]
                and lease["previousFencingToken"] == event["expectedPreviousFencingToken"]
                and lease["expiresAtSequence"] == event["expiresAtSequence"]
                and {_key_tuple(row) for row in lease["pinnedRefs"]} == requested
            )
            if same:
                return {"schemaVersion": 3, "state": current, "result": {
                    "kind": "LEASE_GRANTED", "leaseId": lease["leaseId"],
                    "fencingToken": lease["fencingToken"], "idempotent": True,
                }}
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        if event["expectedPreviousFencingToken"] != current["lastIssuedFencingToken"] or \
                event["expiresAtSequence"] <= event["atSequence"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        if any(key not in objects or objects[key]["state"] != "AVAILABLE"
               for key in requested):
            return _failure(state, "RETENTION_LOCAL_UNAVAILABLE")
        next_fence = current["lastIssuedFencingToken"] + 1
        if next_fence > 2**64 - 1:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        current["ledgerSequence"] = event["atSequence"]
        current["lastIssuedFencingToken"] = next_fence
        current["lease"] = {
            "leaseId": event["leaseId"], "projectId": event["projectId"],
            "ownerId": event["ownerId"],
            "ownerLivenessToken": event["ownerLivenessToken"],
            "ownerAlive": True,
            "previousFencingToken": event["expectedPreviousFencingToken"],
            "fencingToken": next_fence, "state": "HELD",
            "acquiredAtSequence": event["atSequence"],
            "expiresAtSequence": event["expiresAtSequence"],
            "pinnedRefs": copy.deepcopy(event["pinRefs"]),
            "pendingExpiryRefs": [],
        }
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_GRANTED", "leaseId": event["leaseId"],
            "fencingToken": next_fence, "idempotent": False,
        }}

    if kind == "expiry":
        targets = {_key_tuple(row) for row in event["targetRefs"]}
        current["ledgerSequence"] = event["atSequence"]
        if lease is not None and lease["state"] == "HELD" and \
                targets & {_key_tuple(row) for row in lease["pinnedRefs"]}:
            existing = {_key_tuple(row) for row in lease["pendingExpiryRefs"]}
            lease["pendingExpiryRefs"] += [
                copy.deepcopy(row) for row in event["targetRefs"]
                if _key_tuple(row) not in existing
            ]
            return {"schemaVersion": 3, "state": current,
                    "result": {"kind": "READ_CONTINUES"}}
        for target in targets:
            if target in objects:
                objects[target]["state"] = "EXPIRED"
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "EXPIRY_COMMITTED",
            "expiredRefs": copy.deepcopy(event["targetRefs"]),
        }}

    if kind == "release":
        if lease is None or lease["state"] != "HELD" or \
                lease["leaseId"] != event["leaseId"] or \
                lease["ownerId"] != event["ownerId"] or \
                lease["fencingToken"] != event["fencingToken"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for row in applied:
            if _key_tuple(row) in objects:
                objects[_key_tuple(row)]["state"] = "EXPIRED"
        lease["state"] = "RELEASED"
        lease["pendingExpiryRefs"] = []
        current["ledgerSequence"] = event["atSequence"]
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_RELEASED", "leaseState": "RELEASED",
            "expiryAppliedRefs": applied,
        }}

    if kind == "crash-reclaim":
        scope = {_key_tuple(row) for row in event["scopeRefs"]}
        if lease is None or lease["state"] != "HELD" or \
                event["leaseId"] != lease["leaseId"] or \
                event["expectedOwnerId"] != lease["ownerId"] or \
                event["expectedOwnerLivenessToken"] != lease["ownerLivenessToken"] or \
                event["expectedFencingToken"] != lease["fencingToken"] or \
                event["successorFencingToken"] != event["expectedFencingToken"] + 1 or \
                event["successorFencingToken"] > 2**64 - 1 or \
                scope != {_key_tuple(row) for row in lease["pinnedRefs"]} or \
                event["observedOwnerAlive"] is not False or \
                event["atSequence"] < lease["expiresAtSequence"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for row in applied:
            if _key_tuple(row) in objects:
                objects[_key_tuple(row)]["state"] = "EXPIRED"
        reclaimed_id = lease["leaseId"]
        current["lastIssuedFencingToken"] = event["successorFencingToken"]
        current["lease"] = None
        current["ledgerSequence"] = event["atSequence"]
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_RECLAIMED", "leaseId": reclaimed_id,
            "leaseState": "RECLAIMED_STALE", "expiryAppliedRefs": applied,
        }}
    raise ValueError("unreachable event kind")


def is_retention_local_unavailable_v1(output: Any) -> bool:
    if not isinstance(output, dict) or list(output) != ["schemaVersion", "state", "result"] or \
            output.get("schemaVersion") != 3 or not isinstance(output.get("result"), dict):
        raise ValueError("invalid SemanticLeaseOutputV3")
    result = output["result"]
    kind = result.get("kind")
    if kind not in RESULT_VARIANT_FIELDS or list(result) != RESULT_VARIANT_FIELDS[kind]:
        raise ValueError("invalid SemanticLeaseResultV3")
    return kind == "RETENTION_LOCAL_UNAVAILABLE"


def _object_state(key: dict[str, str], state: str = "AVAILABLE") -> dict[str, str]:
    return {
        "projectId": key["projectId"], "state": state,
        "recordCasRef": key["recordCasRef"], "recordKind": key["recordKind"],
    }


def _base_state(keys: list[dict[str, str]], *, sequence: int = 10,
                fence: int = 4, lease: Any = None) -> dict[str, Any]:
    return {
        "schemaVersion": 3, "projectId": keys[0]["projectId"],
        "ledgerSequence": sequence, "lastIssuedFencingToken": fence,
        "objects": [_object_state(key) for key in keys], "lease": lease,
    }


def _held_lease(project_id: str, pinned: list[dict[str, str]], *,
                fence: int = 5, previous: int = 4, expires: int = 12,
                pending: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "leaseId": "lease1:11111111111111111111111111111111",
        "projectId": project_id,
        "ownerId": "owner1:22222222222222222222222222222222",
        "ownerLivenessToken": "live1:33333333333333333333333333333333",
        "ownerAlive": True, "previousFencingToken": previous,
        "fencingToken": fence, "state": "HELD", "acquiredAtSequence": 7,
        "expiresAtSequence": expires, "pinnedRefs": copy.deepcopy(pinned),
        "pendingExpiryRefs": copy.deepcopy(pending or []),
    }


def lease_goldens(primary: dict[str, Any]) -> list[dict[str, Any]]:
    keys = [copy.deepcopy(unit) for unit in
            primary["operationalProjection"]["requiredObjectRefs"][:3]]
    project = primary["projectId"]
    grant_state = _base_state(keys, sequence=10, fence=4)
    grant_event = {
        "kind": "resolve-and-pin", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 11,
        "leaseId": "lease1:11111111111111111111111111111111",
        "ownerId": "owner1:22222222222222222222222222222222",
        "ownerLivenessToken": "live1:33333333333333333333333333333333",
        "expectedPreviousFencingToken": 4, "expiresAtSequence": 20,
        "pinRefs": [copy.deepcopy(keys[0])],
    }
    held = _held_lease(project, [keys[0]], fence=5, previous=4, expires=20)
    held_state = _base_state(keys, sequence=11, fence=5, lease=held)
    retry_event = copy.deepcopy(grant_event)
    retry_event["atSequence"] = 12
    conflict_event = copy.deepcopy(retry_event)
    conflict_event["leaseId"] = "lease1:99999999999999999999999999999999"
    unavailable_state = _base_state(keys, sequence=10, fence=4)
    unavailable_state["objects"][0]["state"] = "EXPIRED"
    expiry_state = _base_state(
        keys, sequence=11, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4, expires=20),
    )
    expiry_event = {
        "kind": "expiry", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 12,
        "targetRefs": [copy.deepcopy(keys[0]), copy.deepcopy(keys[1])],
    }
    release_pending = [copy.deepcopy(keys[1]), copy.deepcopy(keys[2])]
    release_state = _base_state(
        keys, sequence=20, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4,
                          expires=20, pending=release_pending),
    )
    release_event = {
        "kind": "release", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 21,
        "leaseId": release_state["lease"]["leaseId"],
        "ownerId": release_state["lease"]["ownerId"], "fencingToken": 5,
    }
    reclaim_state = _base_state(
        keys, sequence=20, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4,
                          expires=21, pending=release_pending),
    )
    reclaim_event = {
        "kind": "crash-reclaim", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 21,
        "leaseId": reclaim_state["lease"]["leaseId"],
        "expectedOwnerId": reclaim_state["lease"]["ownerId"],
        "expectedOwnerLivenessToken": reclaim_state["lease"]["ownerLivenessToken"],
        "expectedFencingToken": 5, "successorFencingToken": 6,
        "scopeRefs": [copy.deepcopy(keys[0])], "observedOwnerAlive": False,
    }
    free_expiry_state = _base_state(keys, sequence=30, fence=6)
    free_expiry_event = {
        "kind": "expiry", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 31,
        "targetRefs": [copy.deepcopy(keys[2])],
    }
    bad_reclaim = copy.deepcopy(reclaim_event)
    bad_reclaim["successorFencingToken"] = 7
    cases = [
        ("SLV3-01-FRESH-GRANT", grant_state, grant_event),
        ("SLV3-02-IDEMPOTENT-GRANT", held_state, retry_event),
        ("SLV3-03-CONFLICT-PRECONDITION", held_state, conflict_event),
        ("SLV3-04-LOCAL-UNAVAILABLE", unavailable_state, grant_event),
        ("SLV3-05-EXPIRY-DEFERRED", expiry_state, expiry_event),
        ("SLV3-06-RELEASE-COMPLETE-PENDING", release_state, release_event),
        ("SLV3-07-CRASH-SUCCESSOR-FENCE", reclaim_state, reclaim_event),
        ("SLV3-08-EXPIRY-COMMITTED", free_expiry_state, free_expiry_event),
        ("SLV3-09-BAD-SUCCESSOR-REFUSES", reclaim_state, bad_reclaim),
    ]
    return [{
        "id": case_id, "preState": copy.deepcopy(prestate),
        "event": copy.deepcopy(event),
        "expectedOutput": reduce_semantic_lease_v3(prestate, event),
    } for case_id, prestate, event in cases]


def _raw_resolution_contract(primary: dict[str, Any],
                             alternate: dict[str, Any]) -> dict[str, Any]:
    registry: list[dict[str, Any]] = []
    for kind, declaration in RECORD_TYPES.items():
        registry.append({
            "recordKind": kind,
            "expectedValueType": declaration["expectedValueType"],
            "orderedFields": RECORD_COMMON_PREFIX + [declaration["idField"]]
            + RECORD_COMMON_SUFFIX,
            "selector": declaration["selector"],
            "selectedValueType": declaration["selectedValueType"],
            "dependencyOrderedFields": DEPENDENCY_FIELDS,
            "closed": True,
        })
    return {
        "type": "RawObjectResolutionConformanceV1",
        "closed": True,
        "ownership": {
            "byteReadOwner": "orchestration host or immutable content-addressed read boundary",
            "semanticValidatorOwner": "VerifiedSemanticRTSnapshotV1 pure validation API",
            "rule": "The caller supplies the exact bytes. This API cannot fetch, mutate, persist, invoke a callback, mint a receipt, or attest liveness.",
            "identitySubstitution": "A CAS identity, receipt, path, selector, snapshot id, or availability assertion without the exact bytes is never usable.",
        },
        "pureFunctionSignature": "validate_raw_object_resolution_v1(VerifiedSemanticRTSnapshotV1, RawBytes, RawObjectResolutionRequestV1) -> RawObjectResolutionResultV1",
        "requestOrderedFields": REQUEST_FIELDS,
        "requestType": {
            "projectId": "ProjectId",
            "recordCasRef": "RawCasRef",
            "recordKind": "ClosedRecordKindV1",
            "expectedValueType": "ClosedRawValueTypeV1",
            "selector": "ClosedRecordSelectorV1",
            "requiredCapability": "SemanticCapabilityV1",
        },
        "resultOrderedFields": RESULT_FIELDS,
        "validationOrder": [
            "1. require nonempty caller-supplied immutable bytes",
            "2. derive UInt64 byte length and SHA-256 digest, then require digest-derived CAS equals request.recordCasRef",
            "3. parse strict UTF-8 JSON and require the registered closed record type, ordered fields, nested dependency type, exact scalar types, and no duplicate/nonfinite/float value",
            "4. require expected value type, record-specific selector, projectId, recordKind, and requiredCapability equality",
            "5. return RAW_OBJECT_USABLE with the exact validated bytes and selected value",
        ],
        "failureRule": "Every failure is explicit and returns no usable result; no fallback, default, identity-only terminal, fetch, callback, mutation, persistence, or liveness conclusion is permitted.",
        "closedTypeRegistry": registry,
        "fixtureAlgorithm": {
            "input": "Any finite nonempty topologically ordered record specification with any positive unit cardinality not exceeding record cardinality.",
            "recordBytes": "Compact insertion-order UTF-8 JSON of the registered closed record; dependencies name only already-derived raw keys.",
            "recordCasRef": "sha256:lowercase_hex(SHA256(recordBytes))",
            "proofRefs": "One proof ref per byte-bearing record, sorted by the inherited RT13 encoded RawObjectKeyV1 bytes.",
            "units": "Group every proof ref exactly once by declared capability and fixture unit label; derive UNIT-ID-V3 from the exact grouped raw keys; no count table exists.",
            "semanticClosure": "Construct a complete SemanticCapabilityClosureV3 with byte-derived proof refs, graph, bindings, roots, units, and the inherited RT13 Merkle commitment grammar.",
            "operationalProjection": "Derive OperationalCustodyProjectionV1 from the new closure using the generic count-independent projection algorithm.",
            "snapshot": "Embed every exact raw byte vector keyed by its derived CAS; snapshot identity commits to the complete ordered byte map.",
            "forbidden": "No fixture ref may equal an old RT13 NOMATCH proof ref and no identity-only row may terminate the closure.",
        },
        "fixtureGoldens": [primary, alternate],
        "cardinalityEvidence": {
            "primary": {"recordCount": 7, "unitCount": 2},
            "differentEmbeddedShape": {"recordCount": 5, "unitCount": 3},
            "checkerGeneratedShape": {"recordCount": 9, "unitCount": 4},
            "fixedCountAssumption": "FORBIDDEN",
        },
        "oldRt13FeasibilityBoundary": {
            "rt13NomatchProofRefCount": 23,
            "identityOnlyExternalRefCount": 18,
            "forwardDiscoverablePreimageCount": 7,
            "unresolvedPatternedIdentityCount": 11,
            "forwardDiscoverableRefs": DISCOVERED_OLD_PREIMAGES,
            "unresolvedPatternedRefs": OLD_PATTERNED_REFS,
            "v6IndependentAuditSha256": "b3fa29fccb4457a29b9f1d5ea71c262270e39ddd32ac5de3a233d6320678d523",
            "v7FeasibilityReportSha256": "d31d088fc9bcde0f9b6c55e4b868b019abe8002655183708b205946a6d3a9fbe",
            "disposition": "The embedded fixtures use only new forward-derived identities. They neither recover nor replace any old RT13 NOMATCH object and make no preimage claim for the eleven patterned hashes.",
        },
        "futureConsumerBoundary": "A separately authored downstream successor may pin an exact reviewed fixture snapshot/result, but this candidate imports no downstream artifact and grants no downstream application authority.",
    }


def _operational_contract() -> dict[str, Any]:
    return {
        "type": "OperationalCustodyProjectionV1",
        "closed": True,
        "orderedFields": [
            "schemaVersion", "projectId", "sourceEvaluationProofBundleCasRef",
            "sourceSemanticCapabilityClosureCasRef",
            "sourceSemanticCapabilityClosureCommitment",
            "normalizationAlgorithm", "operationalUnits", "requiredObjectRefs",
        ],
        "sourceAuthority": {
            "bundle": "exact verified EP8 bundle bytes or an exact checker-generated fixture proof bundle",
            "semanticClosure": "exact selected SemanticCapabilityClosureV3 bytes; source arrays, unit ids, source object order, CAS, and commitment are never mutated",
            "joinRules": [
                "bundle.projectId equals closure.projectId equals projection.projectId",
                "bundle proof requirements equal closure proofRefs, dependency graph, and unit ownership",
                "source closure CAS hashes the exact semantic closure canonical bytes",
                "source closure commitment recomputes under SEMANTIC-CAPABILITY-CLOSURE-GRAMMAR-V3",
            ],
        },
        "sortingGrammar": {
            "source": "exact RT13 SEMANTIC-CAPABILITY-CLOSURE-GRAMMAR-V3 tags and framing",
            "component": "tag || u32be(len(UTF8(s))) || UTF8(s)",
            "blob": "tag || u32be(len(bytes)) || bytes",
            "encodedRawKey": "blob(0x75, component(0x76,recordCasRef) || component(0x77,projectId) || component(0x78,recordKind))",
            "encodedUnitKey": "0x70 || component(0x71,unitId) || component(0x72,projectId) || component(0x74,requiredForCapability) || blob(0x79,concat(sort_unsigned(encodedRawKey(objectRefs))))",
            "comparison": "lexicographic unsigned bytes",
        },
        "derivation": {
            "operationalUnits": "Copy every source unit and sort only copied objectRefs by encodedRawKey; then sort copied units by encodedUnitKey.",
            "requiredObjectRefs": "Exact unique union of all operational unit objectRefs, sorted by encodedRawKey.",
            "sourceMutation": "FORBIDDEN", "lookupTable": "FORBIDDEN",
            "fixedUnitCount": "FORBIDDEN", "fixedObjectCount": "FORBIDDEN",
        },
        "canonicalGrammar": {
            "name": "OPERATIONAL-CUSTODY-PROJECTION-CANONICAL-JSON-V1",
            "encoding": "UTF-8, compact, no BOM or surrounding bytes",
            "rootKeyOrder": [
                "schemaVersion", "projectId", "sourceEvaluationProofBundleCasRef",
                "sourceSemanticCapabilityClosureCasRef",
                "sourceSemanticCapabilityClosureCommitment",
                "normalizationAlgorithm", "operationalUnits", "requiredObjectRefs",
            ],
            "unitKeyOrder": ["unitId", "projectId", "requiredForCapability", "objectRefs"],
            "rawObjectKeyOrder": ["projectId", "recordCasRef", "recordKind"],
            "objects": "closed; missing, unknown, duplicate, or reordered keys reject",
            "arrays": "exact derived order", "floatsExponentNaNInfinity": "forbidden",
        },
        "identityTypes": {
            "refType": "OperationalCustodyProjectionRefV1",
            "refEquation": "sha256:lowercase_hex(SHA256(projectionCanonicalBytes))",
            "digestType": "OperationalCustodyProjectionDigestV1",
            "digestDomain": "opensip.operational-custody-projection.v1",
            "digestEquation": "sha256:lowercase_hex(SHA256(ASCII(domain) || 0x00 || u64be(length) || projectionCanonicalBytes))",
            "semanticAliasForbidden": True,
        },
        "cardinality": {
            "algorithm": "derived from input arrays; no accepted count table",
            "twentyThreeIsOnlyOneCompatibilityGolden": True,
            "twoUnitsIsOnlyOneCompatibilityGolden": True,
            "embeddedByteBearingCounts": [[7, 2], [5, 3]],
            "checkerGeneratedCount": [9, 4],
        },
        "rt13NomatchCompatibilityGolden": {
            "sourceEvaluationProofBundleCasRef": "sha256:cc27c2beef32f3343d167c5727aa255b51884993ca416c4a862388e3be96a829",
            "sourceSemanticCapabilityClosureCasRef": "sha256:70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
            "requiredObjectRefCount": 23, "unitCount": 2,
            "operationalUnitOrder": ["replayable", "verifiable"],
            "canonicalByteLength": 10606,
            "projectionRef": "sha256:49a09580190c2f12de3912581171b3ed77dbd9c85a81c8367978a16016d16b60",
            "projectionDigest": "sha256:58c16d46dca070edb155ff8373973638b20f08877006f9a871306ed8b1a6afd3",
            "byteCustodyStatus": "IDENTITY-ONLY-COMPATIBILITY-GOLDEN; NOT A RawObjectResolutionConformanceV1 FIXTURE",
        },
    }


def _semantic_lease_contract(primary: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": {
            "type": "LeaseStateV3", "closed": True, "schemaVersion": 3,
            "orderedFields": STATE_FIELDS,
            "nestedTypes": {
                "RawObjectKeyV1": ["projectId", "recordCasRef", "recordKind"],
                "RawObjectStateV1": OBJECT_STATE_FIELDS,
                "LeaseRecordV2": LEASE_FIELDS,
            },
        },
        "events": [{
            "type": {"expiry": "ExpiryEventV1", "release": "ReleaseEventV1",
                     "crash-reclaim": "CrashReclaimEventV3",
                     "resolve-and-pin": "ResolveAndPinEventV2"}[kind],
            "kind": kind, "closed": True, "orderedFields": fields,
        } for kind, fields in EVENT_FIELDS.items()],
        "commonRules": {
            "transactionBoundary": TX_BOUNDARY,
            "sequence": "event.atSequence equals prestate.ledgerSequence + 1",
            "project": "event, state, every raw key, lease, and scope share one projectId",
            "failureState": "Every semantic refusal returns a byte-exact deep copy of prestate with no sequence, fence, lease, object, or pending-expiry movement.",
            "externalFacts": "Owner liveness and fencing validity are primitive prevalidated inputs; this pure reducer neither establishes nor persists their provenance.",
        },
        "output": {
            "type": "SemanticLeaseOutputV3", "closed": True,
            "orderedFields": ["schemaVersion", "state", "result"],
            "schemaVersion": 3,
            "resultVariantOrderedFields": RESULT_VARIANT_FIELDS,
            "forbiddenPayloads": [
                "host termination class", "host error code", "process exit code",
                "receipt", "liveness proof", "journal", "recovery record",
            ],
        },
        "reducers": {
            "reduce_expiry_v1": "Advance one accepted sequence; defer an intersecting held pin by appending only not-yet-pending targets in event order, otherwise expire present targets.",
            "reduce_release_v1": "Require exact held lease identity/owner/fence; apply the complete ordered pendingExpiryRefs array, mark RELEASED, clear pending expiry, and advance once.",
            "reduce_crash_reclaim_v3": "Require exact held scope/owner/liveness/fence, false observed-owner-alive, expiry reached, and successorFencingToken exactly expected+1; apply complete ordered pending expiry, advance lastIssuedFencingToken exactly once, clear lease, and advance sequence.",
            "reduce_resolve_and_pin_v2": "Preserve exact RT13 idempotent retry; otherwise require current previous fence, future expiry, and every requested raw key AVAILABLE, then allocate exactly lastIssuedFencingToken+1.",
            "is_retention_local_unavailable_v1": "True exactly for a validated RETENTION_LOCAL_UNAVAILABLE result kind.",
        },
        "pureFunctionSignatures": [
            "reduce_expiry_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ExpiryEventV1) -> SemanticLeaseOutputV3",
            "reduce_release_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ReleaseEventV1) -> SemanticLeaseOutputV3",
            "reduce_crash_reclaim_v3(VerifiedSemanticRTSnapshotV1, LeaseStateV3, CrashReclaimEventV3) -> SemanticLeaseOutputV3",
            "reduce_resolve_and_pin_v2(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ResolveAndPinEventV2) -> SemanticLeaseOutputV3",
        ],
        "goldenScenarios": lease_goldens(primary),
        "legacyCompatibilityRule": "The verifier independently projects applicable exact RT13 LeaseStateV2 transitions to this host-neutral vocabulary. Crash successor-fence movement is the sole state delta; legacy host classification never enters this root.",
        "mutationRequirements": [
            "wrong event key order or runtime type", "cross-project key",
            "non-next sequence", "wrong transaction boundary", "duplicate raw key",
            "partial pending-expiry application", "pending-expiry sort or filter",
            "crash successor fence unchanged", "crash successor fence skips a value",
            "failure sequence movement", "failure fence movement", "failure state mutation",
        ],
    }


def _verified_api_contract(primary: dict[str, Any],
                           alternate: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "constructor": {
            "signature": "validate_semantic_rt_snapshot_v1(FrozenDependencySnapshotV1, VerifiedD9SnapshotV1) -> VerifiedSemanticRTSnapshotV1",
            "compatibilityCapabilityUse": "VerifiedD9SnapshotV1 is consumed only by the verifier while reproducing rejected RT14 call shapes and rows; it is never retained or made semantically reachable.",
        },
        "frozenDependencySnapshotContract": {
            "kind": "opaque immutable in-memory capability; never JSON or persisted",
            "requiredProperties": [
                "one snapshotId and one alias-collapsed immutable byte map",
                "every unique local input read exactly once and hashed before any local source executes",
                "strict UTF-8 JSON with duplicate, float, NaN, and Infinity rejection",
                "verified sources compiled from buffers under synthetic filenames with no pyc, path import, sys.path discovery, or nested content reread",
                "stat-only end identity check and unchanged repository-state observation",
            ],
        },
        "verifiedD9Compatibility": {
            "scope": "checker/verifier only",
            "exactSubjects": {
                "artifactSha256": PINS[D9], "checkerSha256": PINS[D9_CHECKER],
                "reviewSha256": PINS[D9_REVIEW],
            },
            "requiredReviewState": "PASS / zero blockers / CANDIDATE-NOT-APPLIED",
            "rt14CorpusState": "REJECTED-BY-DEPENDENCY; semantic delta conditionally acceptable but never applied",
            "exactCallShapeCount": 6, "rowDenominator": {"retained": 11, "local": 1, "contextual": 4, "total": 16},
            "persistence": "FORBIDDEN",
        },
        "returnedSnapshot": {
            "type": "VerifiedSemanticRTSnapshotV1",
            "retainsExactly": [
                "snapshotId", "verified RT15 candidate buffer/object",
                "verified RT13 semantic basis buffer/object",
                "verified EP8 pure validation/derivation adapter",
                "operational projection encoder/ref/digest callables",
                "four semantic lease reducer callables",
                "retention-local-unavailable predicate",
                "RawObjectResolutionConformanceV1 pure validation callable and exact fixture snapshots",
            ],
            "mustNotRetain": [
                "D9 compatibility capability/module/bytes/review",
                "rejected RT14 contextual overlay",
                "downstream transaction, persistence, journal, receipt, recovery, or mutation capability",
            ],
            "objectGraphRule": "The verifier proves every must-not-retain object unreachable before returning the snapshot.",
        },
        "pureCallSignatures": [
            "derive_operational_custody_projection_v1(VerifiedSemanticRTSnapshotV1, VerifiedEvaluationProofBundleV1, ExactSemanticCapabilityClosureV3) -> (OperationalCustodyProjectionV1, OperationalCustodyProjectionRefV1, OperationalCustodyProjectionDigestV1)",
            "validate_raw_object_resolution_v1(VerifiedSemanticRTSnapshotV1, RawBytes, RawObjectResolutionRequestV1) -> RawObjectResolutionResultV1",
            "reduce_expiry_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ExpiryEventV1) -> SemanticLeaseOutputV3",
            "reduce_release_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ReleaseEventV1) -> SemanticLeaseOutputV3",
            "reduce_crash_reclaim_v3(VerifiedSemanticRTSnapshotV1, LeaseStateV3, CrashReclaimEventV3) -> SemanticLeaseOutputV3",
            "reduce_resolve_and_pin_v2(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ResolveAndPinEventV2) -> SemanticLeaseOutputV3",
            "is_retention_local_unavailable_v1(VerifiedSemanticRTSnapshotV1, SemanticLeaseOutputV3) -> bool",
        ],
        "rawObjectResolutionConformance": _raw_resolution_contract(primary, alternate),
        "verifierTcb": {
            "soleInvocationPrefix": ["python3", "-I", "-B"],
            "requiredFlags": {"isolated": 1, "ignoreEnvironment": 1,
                              "noUserSite": 1, "dontWriteBytecode": True},
            "nestedProcesses": "FORBIDDEN", "localPathImports": "FORBIDDEN",
            "nestedContentRereads": "FORBIDDEN", "pyc": "FORBIDDEN",
            "sourceExecutionOrder": "all local data/checker/review buffers hash and review-bind before any verified local source buffer executes",
        },
    }


def expected_candidate(authority: FrozenAuthority) -> dict[str, Any]:
    candidate = copy.deepcopy(authority.parsed[RT20])
    candidate["version"] = 21
    candidate["status"] = RT21_STATUS
    candidate["supersedesAsArchitectureCandidate"] = RT20
    candidate["authority"] = {
        "candidateState": "NOT-APPLIED",
        "authorityClaim": "NONE",
        "semanticSourceRule": "The exact RT20 semantic object is inherited only for its independently retained narrow passing evidence: exact 55-pin authority checks, EP8 API/receipt commitments, real D9 v1.10 dataclass semantics, semantic data/reducers, unchanged 7/2 and 5/3 raw-byte fixtures, nine leases, 13/7 root delta, and executed D9 consumers. Its sole rejected returned-graph claim is removed at the model boundary: VerifiedSemanticRTSnapshotV2 is a closed inert value graph, while all seven pure operations remain authenticated host-owned functions outside the returned value.",
        "verifiedSnapshotRequired": True,
        "externalExecutionPrecondition": "Runtime byte reads, liveness, fencing, persistence, transaction, durability, recovery, and atomicity authority remain outside this semantic contract.",
        "productionExecutionClaim": "NONE",
    }
    lease_contract = candidate["semanticLeaseProtocolV3"]
    lease_contract["pureFunctionSignatures"] = [
        row.replace("VerifiedSemanticRTSnapshotV2", "VerifiedSemanticRTSnapshotV2")
        for row in lease_contract["pureFunctionSignatures"]
    ]

    ownership = candidate["semanticOwnershipBoundary"]
    ownership["ownsExactly"] = [
        row.replace("VerifiedSemanticRTSnapshotV2", "VerifiedSemanticRTSnapshotV2")
        for row in ownership["ownsExactly"]
    ]
    ownership["rootDelta"] = {
        "predecessor": RT20, "predecessorRootCount": 20,
        "independentlyReviewedUnchangedRootKeys": [
            "artifact", "status", "claimId", "dependencies",
            "semanticBasisProjection", "operationalCustodyProjectionContract",
            "semanticLeaseProtocolV3",
            "storageAndLineage", "custodyPolicy",
            "integrationState", "assurance", "sealRecommendation",
            "rawPhysicalIdentityContract",
        ],
        "independentlyReviewedUnchangedRootCount": 13,
        "metadataOrVerifierOnlyChangedRootKeys": [
            "version", "supersedesAsArchitectureCandidate",
            "authority", "semanticOwnershipBoundary", "invariants", "retainedResiduals",
            "verifiedSemanticRtApiContract",
        ],
        "metadataOrVerifierOnlyChangedRootCount": 7,
        "addedRootKeys": [], "removedRootKeys": [], "finalRootCount": 20,
        "equation": "13 independently reviewed unchanged roots + 7 metadata/verifier-only roots = 20; status, semanticLeaseProtocolV3, and every semantic/data/fixture root are exact RT20 bytes as parsed data",
    }

    retained_invariants = [
        copy.deepcopy(row) for row in authority.parsed[RT20]["invariants"]
        if not any(row.startswith(prefix) for prefix in (
            "RT20-31:", "RT20-32:", "RT20-33:", "RT20-34:"))
    ]
    candidate["invariants"] = retained_invariants + [
        "RT21-35: the retained RT20 55-input window is replaced lineage-for-lineage with exact RT20 artifact/checker/adjudication/one-blocker review while remaining exactly 55 unique alias-collapsed, read-once, hash-bound, end-stat-checked inputs; all 55 single-pin corruptions and physical aliases refuse before callback",
        f"RT21-36: VerifiedSemanticRTSnapshotV2 is exactly a deep-immutable value graph over the ordered {len(INERT_VALUE_REGISTRY)}-kind registry null/bool/int/str/bytes/tuple/readonly-string-map and the exact {len(INERT_EDGE_REGISTRY)} semantic edges mapping-key/mapping-value/tuple-item; unknown input or returned value kinds refuse",
        "RT21-37: no callable, reducer, code, frame, module, descriptor, iterator, exception, weakref, custom instance, or mutable container is returned; the seven exact pure call signatures are preserved as authenticated host-owned functions taking the inert snapshot as their first argument",
        f"RT21-38: every one of the {len(INERT_VALUE_REGISTRY)} value-kind and {len(INERT_EDGE_REGISTRY)} semantic-edge declarations has an independent fail-before-root deletion mutation; the frozen independent 34-kind RT20 challenge is used adversarially and every executable or non-grammar kind refuses at construction",
        "RT21-39: the snapshotId one-to-one canonical commitment covers every returned data field and all seven inert host operation identifiers; mutation, cycle, node/depth exhaustion, non-string mapping key, registry drift, and commitment drift are named controlled refusals",
    ]
    candidate["retainedResiduals"] = [
        "RT20 is independently REJECTED for exactly RT20-PF-01-INDEPENDENT-SEMANTIC-CHILD-DENOMINATOR-INCOMPLETE with zero input hash/identity drift. Its narrow passes for 55-pin corruption/alias refusal, EP8 nine-API commitments, real D9 v1.10 dataclass, 7/2 and 5/3 byte fixtures, nine leases, D9 6/16/10, purge/custody roots, and the 13/7 root delta are inherited without semantic change. RT21 removes the rejected executable return graph rather than claiming its incomplete 58-edge vocabulary is complete; RT21 itself remains unreviewed and NOT-APPLIED.",
        "The E8 preparation v6 finding remains repaired only by the inherited new fixture-only byte-bearing upstream closure. The frozen old RT13 patterned identities remain unresolved and are not claimed or replaced.",
        "Any downstream successor must pin exact independently reviewed RT21 artifact/checker bytes and the exact committed data-only receipt/fixture projection, keep reducers outside the returned snapshot, and receive its own fresh independent review.",
        "No production byte store, liveness, fencing, persistence, transaction, durability, recovery, crash, concurrency, or atomicity implementation is demonstrated.",
        "CD-RT-5 remains BLOCKED, product state remains BLOCKED_ON_PHASE_1A, durable default remains UNSELECTED, and this architecture candidate author has no review/application/freeze authority.",
    ]

    api = candidate["verifiedSemanticRtApiContract"]
    api["schemaVersion"] = 6
    api["constructor"]["signature"] = \
        "validate_semantic_rt_snapshot_v6(FrozenDependencySnapshotV7, VerifiedD9SnapshotV1) -> VerifiedSemanticRTSnapshotV2"
    api["constructor"]["compatibilityCapabilityUse"] = \
        "VerifiedD9SnapshotV1 is the exact executed D9 v1.13 API. The verifier resolves and invokes all six frozen RT14 consumer paths and all sixteen rows through it, then copies only closed inert data into the returned snapshot; no D9/RT14/review/buffer/module/FrozenAuthority or executable object kind is admitted by construction."
    api["frozenDependencySnapshotContract"] = {
        "kind": "opaque immutable in-memory capability; never JSON or persisted",
        "uniqueInputCount": len(PINS),
        "sha256ByPath": dict(PINS),
        "requiredProperties": [
            "one alias-collapsed immutable byte map; every unique input is read exactly once and hashed before any local source executes",
            "every retained local source compiles from its exact authenticated buffer; no persistent local sys.modules entry exists",
            "all delayed local data/module resolution is an allowlisted immutable buffer lookup; path loaders, sys.path, PYTHONPATH, pyc, and filesystem fallback are forbidden",
            "the five D9 dependency-assignment interpositions are exact-AST-selected, declared, single-fire, restored exactly once, and refuse zero, duplicate, broadened, or drifted targets",
            "D9 v1.10 alone is temporarily registered under a digest-derived verified module name so its exact frozen dataclass decorator executes; collision, mapping replacement, cleanup failure, or semantic metadata/constructor/equality/frozen drift refuses",
            "the exact read-count map, cwd, sys.path, local-module registry boundary, pyc metadata, and dependency stat identities remain unchanged after all active probes",
        ],
    }
    d9_compat = api["verifiedD9Compatibility"]
    d9_compat["construction"] = \
        "Bottom-up exact-buffer execution of v1.6, v1.7, v1.8, v1.10, v1.11, v1.12, and v1.13; every one of the independently reviewed 28-input D9 window bytes is outer-snapshot pinned before execution."
    d9_compat["resolvedConsumerPaths"] = [
        "derive_class", "derive_codes", "V17.V16.derive_class",
        "derive_class", "reduce_concurrent", "check",
    ]
    d9_compat["execution"] = {
        "callShapeCount": 6,
        "rowDenominator": {"retained": 11, "local": 1, "contextual": 4, "total": 16},
        "rowClassAndCodeSource": "exact D9 v1.13 derive_class and derive_codes exports",
        "precedenceSource": "exact D9 v1.13 reduce_concurrent export",
        "retainedCheckSource": "exact D9 v1.13 three-argument check export",
        "localSemanticCopies": "FORBIDDEN",
    }
    api["returnedSnapshot"] = {
        "type": "VerifiedSemanticRTSnapshotV2",
        "retainsExactly": [
            "schemaVersion=2 and kind=VERIFIED_SEMANTIC_RT_SNAPSHOT_V2",
            "snapshotId committing every returned field and all seven host operation identifiers",
            "deep-immutable verified RT21 candidate data projection",
            "deep-immutable verified RT13 semantic basis data projection",
            "closed deep-immutable VerifiedEP8DerivationReceiptV1 with exact typed results/commitments and no callable",
            "closed deep-immutable VerifiedRawObjectFixtureProjectionV1 containing both exact byte snapshots",
            "an exact seven-string hostOperationIds tuple naming external authenticated pure functions",
        ],
        "mustNotRetain": [
            "any callable, reducer, code object, frame, module, descriptor, iterator, exception, weakref, custom instance, mutable mapping, mutable sequence, or set",
            "any live EP8 callable, loader closure, test-store helper, or whole-contract checker",
            "FrozenAuthority or its complete buffers, parsed objects, modules, read counters, or mutable maps",
            "any exact verifier-owned input buffer, parsed root, executed local module, D9 capability/module/bytes/review, or rejected RT14 contextual overlay by object identity",
            "downstream transaction, persistence, journal, receipt, recovery, or mutation capability",
        ],
        "objectGraphRule": "The returned value is constructed only by a depth/node-bounded copier over the exact seven-kind inert registry null/bool/int/str/bytes/tuple/readonly-string-map. Its complete semantic-child denominator is exactly mapping key, mapping value, and tuple item. Registry drift refuses before root visitation; unknown values, non-string keys, cycles, budget exhaustion, and commitment drift refuse. The 76-edge reflective CPython denominator is inapplicable because no executable or general runtime object is admitted into the returned value.",
        "hostOperationRule": "The seven exact pure call signatures remain unchanged, but their authenticated implementations live in the verifier/host operation registry and take VerifiedSemanticRTSnapshotV2 as inert data. Only their exact string identifiers are returned.",
        "ep8ConsumerRule": "Downstream Evidence consumes only VerifiedEP8DerivationReceiptV1 and VerifiedRawObjectFixtureProjectionV1 data; it never receives or invokes the authenticated EP8 module.",
    }
    api["pureCallSignatures"] = [
        row.replace("VerifiedSemanticRTSnapshotV2", "VerifiedSemanticRTSnapshotV2")
        for row in api["pureCallSignatures"]
    ]
    raw_contract = api["rawObjectResolutionConformance"]
    raw_contract["pureFunctionSignature"] = raw_contract[
        "pureFunctionSignature"].replace(
            "VerifiedSemanticRTSnapshotV2", "VerifiedSemanticRTSnapshotV2")
    raw_contract["ownership"]["semanticValidatorOwner"] = raw_contract[
        "ownership"]["semanticValidatorOwner"].replace(
            "VerifiedSemanticRTSnapshotV2", "VerifiedSemanticRTSnapshotV2")
    api["verifierTcb"] = {
        "soleInvocationPrefix": ["python3", "-I", "-B"],
        "requiredFlags": {"isolated": 1, "ignoreEnvironment": 1,
                          "noUserSite": 1, "dontWriteBytecode": True},
        "outerSnapshotInputCount": len(PINS),
        "nestedProcesses": "FORBIDDEN", "localPathImports": "FORBIDDEN",
        "nestedContentRereads": "FORBIDDEN", "pyc": "FORBIDDEN",
        "sysModulesLocalRegistration": "FORBIDDEN except the exact v1.10 digest-derived temporary registration; it must be absent before, identical during, and absent after execution",
        "sourceExecutionOrder": "all 55 local data/checker/review/plan buffers hash and review-bind before any verified local source buffer executes",
    }
    api["predecessorRejectionDisposition"] = {
        "reviewArtifact": RT20_REVIEW,
        "reviewSha256": PINS[RT20_REVIEW],
        "decision": "REJECT", "blockingFindingCount": 1,
        "repairedExactly": [
            "RT20-PF-01-INDEPENDENT-SEMANTIC-CHILD-DENOMINATOR-INCOMPLETE",
        ],
        "preservedNarrowPass": [
            "semantic data and reducers exact RT15 narrow preservation",
            "unchanged 7/2 and 5/3 byte-bearing raw fixtures",
            "55 unique read-once pins with 55/55 corruption refusal and physical-alias refusal",
            "all nine underlying authenticated EP8 callables execute without path escape",
            "data-only EP8 receipt and real D9 v1.10 frozen dataclass semantics",
            "purge/custody roots and semantic data exact RT20 preservation",
            "actual D9 v1.13 consumer exports execute over six paths and sixteen rows",
        ],
    }
    old_loader = api.pop("authenticatedLoaderBindingV6", None)
    if not isinstance(old_loader, dict):
        raise AuthorityError("RT20 authenticatedLoaderBindingV6 absent")
    if authority.ep8_receipt_data is None or authority.fixture_projection_data is None:
        raise AuthorityError("RT20 data receipts absent")
    receipt = authority.ep8_receipt_data
    fixture_projection = authority.fixture_projection_data
    api["authenticatedLoaderBindingV7"] = {
        "ep8Closure": {
            "exactSourceAndDataCount": 13,
            "members": [
                EP8, EP8_CHECKER, EP7, EP7_CHECKER, EP6, EP6_CHECKER,
                EP5, EP5_CHECKER, C2, C2_CHECKER, RI, RI_CHECKER, FACT_PLANE,
            ],
            "requiredCheckerApiSource": "exact frozen retention-tiers.v13.json capabilityClosure.source.requiredCheckerApi",
            "requiredCheckerApi": list(EXPECTED_EP8_REQUIRED_API),
            "exactCallCounts": copy.deepcopy(receipt["exactCallCounts"]),
            "delayedResolution": "immutable filename-to-buffer/module closures remain verifier-internal only; no function, closure, module, loader, or authority owner is returned",
            "resultGoldens": {
                "semanticRootCount": 2,
                "dependencyEdgeCount": 20,
                "rawProofRequirementCount": 23,
                "resolvedSemanticObjectCount": 2,
                "semanticBindingEncodingSha256": copy.deepcopy(
                    receipt["results"]["semanticBindingEncodingSha256"]),
                "resultsCommitment": receipt["resultsCommitment"],
                "receiptCommitment": receipt["receiptCommitment"],
                "fixtureProjectionCommitment": fixture_projection[
                    "projectionCommitment"],
            },
            "returnedType": "VerifiedEP8DerivationReceiptV1 data only; zero callables",
        },
        "d9Interpositions": [
            {"source": name, **dict(spec), "selectorMatchCount": 1,
             "requiredFireCount": 1, "requiredRestoreCount": 1}
            for name, spec in D9_INTERPOSITION_SPECS.items()
        ],
        "temporaryVerifiedModuleExecutions": [{
            "source": "check-d9-v1.10.py",
            **copy.deepcopy(authority.temporary_module_receipts[
                "check-d9-v1.10.py"]),
        }],
        "returnedDataTypes": {
            "VerifiedEP8DerivationReceiptV1OrderedFields": [
                "schemaVersion", "kind", "projectId", "acceptedVectorId",
                "sourceArtifactSha256", "sourceCheckerSha256",
                "requiredCheckerApi", "exactCallCounts",
                "fixtureProjectionCommitment", "results", "resultsCommitment",
                "receiptCommitment",
            ],
            "VerifiedRawObjectFixtureProjectionV1OrderedFields": [
                "schemaVersion", "kind", "fixtures", "projectionCommitment",
            ],
            "mutability": "deep immutable mapping/tuple/scalar graph",
            "callables": "FORBIDDEN",
        },
        "predecessorRejectedGraphEvidence": {
            "status": "RT20 REJECTED EVIDENCE ONLY; NOT THE RT21 RETURN BOUNDARY",
            "reviewFinding": "RT20-PF-01-INDEPENDENT-SEMANTIC-CHILD-DENOMINATOR-INCOMPLETE",
            "forbiddenIdentityClasses": [
                "live FrozenAuthority", "complete verifier buffer/parsed/module maps",
                "every exact input buffer", "every parsed input root",
                "every executed local module",
            ],
            "registrySchemaVersion": 3,
            "registryMode": "CPYTHON-REFERENT-ORACLE/CLOSED-EXCEPTIONS/EXACT-ORDERED/NO-UNKNOWN-RUNTIME-KIND",
            "edgeRegistry": [copy.deepcopy(row) for row in GRAPH_EDGE_REGISTRY],
            "runtimeKindRegistry": [
                copy.deepcopy(row) for row in GRAPH_RUNTIME_KIND_REGISTRY],
            "semanticChildDenominator": [
                copy.deepcopy(row)
                for row in GRAPH_SEMANTIC_CHILD_DENOMINATOR],
            "referentOracle": {
                "runtime": "CPython 3.14",
                "generalRule": "gc.get_referents(value) supplies every direct strong referent for every admitted traverse kind before explicit stable-path extraction",
                "exceptionRegistry": [
                    copy.deepcopy(row)
                    for row in GRAPH_REFERENT_ORACLE_EXCEPTIONS],
                "exceptionRule": "Only memoryview, code and frame are admitted get_referents gaps; memoryview traverses obj instead of internal managedbuffer, CodeType traverses every co_consts item, and frame traverses globals/locals/back/builtins/code/trace/generator. Any exception-registry drift refuses before root visitation.",
            },
            "runtimeTypeDeclaration": {
                "mode": "TWO-PASS/EXACT-CLASS-OBJECT-IDENTITY",
                "rule": "A declaration pass strongly retains independently reachable class objects while refusing to expand unknown instances. Validation admits a non-builtin object only when its exact type object was declared on that independent path. An injected instance cannot self-declare through __class__.",
                "initialProductionDeclarations": [
                    "exact VerifiedSemanticRTSnapshotV2 root type"
                ],
                "safeOpaqueRuntimeTypeKeys": [
                    {"module": module, "qualname": qualname}
                    for module, qualname in SAFE_OPAQUE_RUNTIME_TYPE_KEYS
                ],
                "productionExtraTypeDeclarations": "FORBIDDEN",
                "selftestExtraTypeDeclarations": "exact local attack types only"
            },
            "cycleRule": "retain one strong id-to-object reference for every expanded identity through scan completion; skip only when the retained object is identical; an impossible different live object with the same id is a named refusal",
            "identityCustody": {
                "mode": "STRONG-REFERENCE-ID-TO-OBJECT",
                "lifetime": "complete scan",
                "nodeBudgetBasis": "distinct strongly retained identities",
                "mappingproxyReuseProbe": {
                    "helperRoot": "20/20",
                    "actualVerifiedSemanticRTSnapshotV2Root": "20/20"
                }
            },
            "budgets": {"maxNodes": GRAPH_MAX_NODES,
                        "maxDepth": GRAPH_MAX_DEPTH},
            "namedRefusalCodes": [
                "RT20-GRAPH-FORBIDDEN-IDENTITY",
                "RT20-GRAPH-REGISTRY-MISSING",
                "RT20-GRAPH-REGISTRY-DUPLICATE",
                "RT20-GRAPH-REGISTRY-ORDER",
                "RT20-GRAPH-UNKNOWN-EDGE-TYPE",
                "RT20-GRAPH-RUNTIME-REGISTRY-MISSING",
                "RT20-GRAPH-RUNTIME-REGISTRY-DUPLICATE",
                "RT20-GRAPH-RUNTIME-REGISTRY-ORDER",
                "RT20-GRAPH-RUNTIME-REGISTRY-UNKNOWN",
                "RT20-GRAPH-UNKNOWN-RUNTIME-TYPE",
                "RT20-GRAPH-CHILD-DENOMINATOR-MISSING",
                "RT20-GRAPH-CHILD-DENOMINATOR-UNKNOWN",
                "RT20-GRAPH-ORACLE-EXCEPTION-SET",
                "RT20-GRAPH-POSITIVE-DENOMINATOR-MISSING",
                "RT20-GRAPH-REFERENT-ORACLE-RUNTIME",
                "RT20-GRAPH-IDENTITY-CUSTODY-COLLISION",
                "RT20-GRAPH-TRAVERSAL-ERROR",
                "RT20-GRAPH-NODE-BUDGET",
                "RT20-GRAPH-DEPTH-BUDGET",
            ],
            "activeAttackFixtureIds": [
                "RT20-GRAPH-CLASS-DICTIONARY",
                "RT20-GRAPH-NAME-MANGLED-SLOT",
                "RT20-GRAPH-INHERITED-NAME-MANGLED-SLOT",
                "RT20-GRAPH-MEMORYVIEW-BACKING-BUFFER",
                "RT20-GRAPH-RAISING-CUSTOM-MAPPING",
                "RT20-GRAPH-RAISING-ITERATOR",
                "RT20-GRAPH-RAISING-PROPERTY",
                "RT20-GRAPH-CYCLE",
                "RT20-GRAPH-NODE-BUDGET",
                "RT20-GRAPH-DEPTH-BUDGET",
                "RT20-GRAPH-CLASS-METACLASS",
                "RT20-GRAPH-FRAME-GLOBALS",
                "RT20-GRAPH-FRAME-LOCALS",
                "RT20-GRAPH-FRAME-BACK",
                "RT20-GRAPH-GENERATOR-FRAME",
                "RT20-GRAPH-COROUTINE-FRAME",
                "RT20-GRAPH-ASYNC-GENERATOR-FRAME",
                "RT20-GRAPH-CPYTHON-RUNTIME-REFERENT",
                "RT20-GRAPH-SLICE-START-STOP-STEP",
                "RT20-GRAPH-CODE-CONSTANTS",
                "RT20-GRAPH-FUNCTION-STANDARD-METADATA",
                "RT20-GRAPH-PROPERTY-STANDARD-METADATA",
                "RT20-GRAPH-FRAME-STANDARD-METADATA",
                "RT20-GRAPH-GENERATOR-YIELDFROM",
                "RT20-GRAPH-COROUTINE-AWAIT-AND-ORIGIN",
                "RT20-GRAPH-ASYNC-GENERATOR-AWAIT",
                "RT20-GRAPH-UNKNOWN-RUNTIME-TYPE",
                "RT20-GRAPH-MAPPINGPROXY-ID-REUSE",
            ],
            "independentPositiveDenominator": {
                "caseIds": list(GRAPH_POSITIVE_CASE_IDS),
                "caseCount": len(GRAPH_POSITIVE_CASE_IDS),
                "helperRootExpected": (
                    f"{len(GRAPH_POSITIVE_CASE_IDS)}/"
                    f"{len(GRAPH_POSITIVE_CASE_IDS)}"),
                "actualSnapshotRootExpected": (
                    f"{len(GRAPH_POSITIVE_CASE_IDS)}/"
                    f"{len(GRAPH_POSITIVE_CASE_IDS)}"),
                "actualInjectionPoint": "one returned operation function custom-attribute map"
            },
            "edgeDeletionMutationDenominator": len(GRAPH_EDGE_REGISTRY),
            "runtimeKindDeletionMutationDenominator": len(
                GRAPH_RUNTIME_KIND_REGISTRY),
            "semanticChildDeletionMutationDenominator": len(
                GRAPH_SEMANTIC_CHILD_DENOMINATOR),
            "oracleExceptionDeletionMutationDenominator": len(
                GRAPH_REFERENT_ORACLE_EXCEPTIONS),
            "positiveCaseDeletionMutationDenominator": len(
                GRAPH_POSITIVE_CASE_IDS),
            "failureRule": "any reachable forbidden identity, referent-oracle/runtime mismatch, edge/runtime/semantic-child/positive-denominator drift, unknown runtime type, traversal exception, impossible live-id collision, or node/depth exhaustion produces a named controlled finding and refuses before return; no traceback or exception object is returned",
        },
        "inertBoundary": {
            "registrySchemaVersion": 1,
            "valueRegistry": [copy.deepcopy(row)
                              for row in INERT_VALUE_REGISTRY],
            "semanticEdgeRegistry": [copy.deepcopy(row)
                                     for row in INERT_EDGE_REGISTRY],
            "snapshotOrderedFields": list(INERT_SNAPSHOT_FIELDS),
            "hostOperationIds": list(INERT_HOST_OPERATION_IDS),
            "constructorRule": "Copy only exact dict/list/tuple/null/bool/int/str/bytes inputs into fresh MappingProxyType/tuple/null/bool/int/str/bytes values. Dict keys must be exact strings. No custom protocol, iterator, attribute, descriptor, reducer, or callable is consulted.",
            "validatorRule": "Validate only the exact three semantic child relations mapping-key, mapping-value, and tuple-item under exact-type dispatch. Unknown kinds, cycles, non-string keys, registry drift, and budget exhaustion refuse.",
            "canonicalCommitment": {
                "domain": "opensip.verified-semantic-rt-snapshot.v2.inert-v1",
                "grammar": "one-byte type tags plus u64be length framing; mapping order and tuple order preserved; key/value frames distinct",
                "covers": "schemaVersion, kind, candidate, rt13, ep8DerivationReceipt, fixtureProjection, and all seven hostOperationIds",
            },
            "deletionMutationDenominator": {
                "valueKinds": len(INERT_VALUE_REGISTRY),
                "semanticEdges": len(INERT_EDGE_REGISTRY),
                "expected": f"{len(INERT_VALUE_REGISTRY) + len(INERT_EDGE_REGISTRY)}/{len(INERT_VALUE_REGISTRY) + len(INERT_EDGE_REGISTRY)} fail before root visit",
            },
            "independentChallengeBinding": {
                "source": "frozen RT20 candidate-blind 34-kind/76-edge review harness and exact frozen RT20 review",
                "runtimeKindsChallenged": 34,
                "rule": "Every executable or non-grammar standard runtime kind is refused by the constructor; allowed inert values are revalidated under the closed grammar",
                "cleanExecutableEscapes": 0,
            },
            "budgets": {"maxNodes": INERT_MAX_NODES,
                        "maxDepth": INERT_MAX_DEPTH},
            "namedRefusalCodes": [
                "RT21-INERT-VALUE-REGISTRY-DRIFT-BEFORE-ROOT",
                "RT21-INERT-EDGE-REGISTRY-DRIFT-BEFORE-ROOT",
                "RT21-INERT-UNDECLARED-INPUT-KIND",
                "RT21-INERT-UNDECLARED-VALUE-KIND",
                "RT21-INERT-UTF8-STRING",
                "RT21-INERT-INTEGER-ENCODING",
                "RT21-INERT-MAPPING-KEY-TYPE",
                "RT21-INERT-CYCLE",
                "RT21-INERT-NODE-BUDGET",
                "RT21-INERT-DEPTH-BUDGET",
                "RT21-INERT-SNAPSHOT-CLOSED-SHAPE",
                "RT21-INERT-SNAPSHOT-COMMITMENT",
            ],
        },
        "selectorRule": "Select one exact dependency assignment by target identity and exact attribute-free AST SHA-256; line numbers are derived evidence only and never selector authority. No decorator is interposed.",
        "failureRule": "Refuse source hash drift, zero/multiple AST matches, AST digest drift, broadened seam, missing seam, non-single fire, skipped restoration, undeclared/persistent/colliding/poisoned sys.modules registration, filesystem fallback, returned executable EP8 authority, inert value/edge registry drift, unknown input or returned kind, mutable/custom/executable return value, cycle, non-string key, commitment drift, budget exhaustion, or semantic-source substitution.",
    }
    return candidate


def _validate_fixture(fixture: Any, expected: dict[str, Any],
                      label: str) -> list[str]:
    findings: list[str] = []
    difference = exact_recursive_equal(fixture, expected, label)
    if difference:
        findings.append(f"RT16-FIXTURE-EXACT: {difference}")
    if not isinstance(fixture, dict):
        return findings or [f"RT16-FIXTURE-TOTAL: {label} is not an object"]
    try:
        rows = fixture["resolutionRows"]
        row_by_ref: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(rows):
            raw = bytes.fromhex(row["rawBytesHex"])
            result = validate_raw_object_resolution(raw, row["request"])
            if exact_recursive_equal(result, row["expectedResult"],
                                     f"{label}.resolutionRows[{index}].expectedResult"):
                findings.append(f"RT16-RAW-RESULT: {label} row {index} result drift")
            ref = row["request"]["recordCasRef"]
            if ref in row_by_ref:
                findings.append(f"RT16-RAW-DUPLICATE: {label} duplicate {ref}")
            row_by_ref[ref] = row
            parsed = parse_json_bytes(raw, f"{label} raw row {index}")
            if parsed["dependencies"] != row["dependencies"]:
                findings.append(f"RT16-RAW-DEPENDENCY: {label} row {index} envelope drift")
        if set(row_by_ref) & set(OLD_PATTERNED_REFS):
            findings.append(f"RT16-RAW-OLD-IDENTITY: {label} reuses patterned RT13 refs")
        old_refs = {
            row["recordCasRef"] for row in expected["semanticClosure"]["proofRefs"]
        }
        if set(row_by_ref) != old_refs or len(row_by_ref) != fixture["recordCount"]:
            findings.append(f"RT16-RAW-CLOSURE: {label} bytes/proofRefs are not bijective")
        for edge in fixture["dependencyGraph"]:
            if edge["fromRef"] not in row_by_ref or edge["toRef"] not in row_by_ref:
                findings.append(f"RT16-RAW-GRAPH: {label} endpoint has no bytes")
        adjacency: dict[str, list[str]] = {ref: [] for ref in row_by_ref}
        for edge in fixture["dependencyGraph"]:
            adjacency[edge["fromRef"]].append(edge["toRef"])
        colors: dict[str, int] = {}
        def visit(node: str) -> None:
            if colors.get(node) == 1:
                raise ValueError("cycle")
            if colors.get(node) == 2:
                return
            colors[node] = 1
            for child in adjacency[node]:
                visit(child)
            colors[node] = 2
        for ref in adjacency:
            visit(ref)

        closure = fixture["semanticClosure"]
        closure_bytes = compact(closure, sort_keys=True)
        if closure_bytes.hex() != fixture["semanticClosureCanonicalBytesHex"] or \
                cas(closure_bytes) != fixture["semanticClosureCasRef"]:
            findings.append(f"RT16-RAW-CLOSURE-CAS: {label} closure bytes/CAS drift")
        if semantic_closure_commitment(closure["units"]) != closure["closureCommitment"]:
            findings.append(f"RT16-RAW-COMMITMENT: {label} semantic commitment drift")
        owners = [key["recordCasRef"] for unit in closure["units"]
                  for key in unit["objectRefs"]]
        if len(owners) != len(set(owners)) or set(owners) != set(row_by_ref):
            findings.append(f"RT16-RAW-UNIT-OWNERS: {label} owner closure drift")
        for unit in closure["units"]:
            if unit["unitId"] != derive_unit_id(
                    unit["projectId"], unit["requiredForCapability"], unit["objectRefs"]):
                findings.append(f"RT16-RAW-UNIT-ID: {label} unit id drift")
        bundle_bytes = bytes.fromhex(fixture["proofBundleCanonicalBytesHex"])
        if cas(bundle_bytes) != fixture["proofBundleCasRef"]:
            findings.append(f"RT16-RAW-BUNDLE-CAS: {label} proof bundle CAS drift")
        if parse_json_bytes(bundle_bytes, label + " proof bundle")["proofRefs"] != closure["proofRefs"]:
            findings.append(f"RT16-RAW-BUNDLE-CLOSURE: {label} proof ref drift")
        projection, encoded, ref, digest = derive_operational_projection(
            closure, fixture["proofBundleCasRef"], fixture["semanticClosureCasRef"])
        if (projection, encoded.hex(), ref, digest) != (
                fixture["operationalProjection"],
                fixture["operationalProjectionCanonicalBytesHex"],
                fixture["operationalProjectionRef"],
                fixture["operationalProjectionDigest"]):
            findings.append(f"RT16-RAW-PROJECTION: {label} projection drift")
        snapshot = fixture["rawObjectSnapshot"]
        if {row["recordCasRef"]: row["rawBytesHex"] for row in snapshot["records"]} != \
                {ref: row["rawBytesHex"] for ref, row in row_by_ref.items()}:
            findings.append(f"RT16-RAW-SNAPSHOT: {label} snapshot is not byte-complete")
        if fixture["commitments"] != expected["commitments"]:
            findings.append(f"RT16-RAW-FIXTURE-COMMITMENT: {label} commitment drift")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            DuplicateKeyError, FloatForbidden, ResolutionError) as exc:
        findings.append(f"RT16-FIXTURE-TOTAL: {label} controlled {type(exc).__name__}")
    return findings


def _project_old_state(state: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(state)
    projected["schemaVersion"] = 3
    return projected


def _project_old_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("kind") == "D9":
        code = result.get("termination", {}).get("errorCode")
        mapping = {
            "REQUEST.PRECONDITION_FAILED": "RETENTION_PRECONDITION_FAILED",
            "LEDGER.BUSY_TIMEOUT": "RETENTION_BUSY",
            "REQUEST.UNSATISFIABLE": "RETENTION_LOCAL_UNAVAILABLE",
        }
        return {"kind": mapping[code]}
    projected = copy.deepcopy(result)
    if projected.get("kind") == "READ_CONTINUES":
        projected = {"kind": "READ_CONTINUES"}
    return projected


def _legacy_lease_findings(authority: FrozenAuthority) -> tuple[list[str], int]:
    findings: list[str] = []
    count = 0
    rt13 = authority.parsed[RT13]
    old_reduce = authority.modules[RT_CORE].reduce_lease
    for scenario in rt13["leaseProtocol"]["scenarios"]:
        old_state = copy.deepcopy(scenario["initial"])
        for event in scenario["events"]:
            if event["kind"] not in EVENT_FIELDS:
                continue
            old_output = old_reduce(copy.deepcopy(old_state), copy.deepcopy(event))
            v3_state = _project_old_state(old_state)
            v3_event = copy.deepcopy(event)
            if event["kind"] == "crash-reclaim":
                v3_event = {
                    **{key: value for key, value in event.items()
                       if key not in ("scopeRefs", "observedOwnerAlive")},
                    "successorFencingToken": event["expectedFencingToken"] + 1,
                    "scopeRefs": copy.deepcopy(event["scopeRefs"]),
                    "observedOwnerAlive": event["observedOwnerAlive"],
                }
            expected_state = _project_old_state(old_output["state"])
            if event["kind"] == "crash-reclaim" and \
                    old_output["result"].get("kind") == "LEASE_RECLAIMED":
                expected_state["lastIssuedFencingToken"] = v3_event["successorFencingToken"]
            expected = {
                "schemaVersion": 3, "state": expected_state,
                "result": _project_old_result(old_output["result"]),
            }
            actual = reduce_semantic_lease_v3(v3_state, v3_event)
            difference = exact_recursive_equal(actual, expected)
            if difference:
                findings.append(f"RT16-LEASE-RT13-COMPAT: {scenario['id']} {difference}")
            count += 1
            old_state = old_output["state"]
    return findings, count


def _resolve_d9_export(module: Any, path: str) -> Any:
    value = module
    for component in path.split("."):
        value = getattr(value, component)
    if not callable(value):
        raise TypeError(f"D9 export {path} is noncallable")
    return value


def _d9_compatibility_findings(
        authority: FrozenAuthority, d9_override: Any | None = None,
) -> tuple[list[str], int, int]:
    findings: list[str] = []
    rt13 = authority.parsed[RT13]
    rt14 = authority.parsed[RT14]
    d9 = authority.parsed[D9]
    d9mod = d9_override if d9_override is not None else authority.modules[D9_CHECKER]
    projected = copy.deepcopy(rt14)
    projected.pop("contextualD9Rejoin", None)
    projected["version"] = 13
    projected["supersedesAsArchitectureCandidate"] = "retention-tiers.v12.json"
    difference = exact_recursive_equal(projected, rt13)
    if difference:
        findings.append(f"RT16-RT14-RT13-PROJECTION: {difference}")
    tree = ast.parse(authority.buffers[RT14_CHECKER].decode("utf-8"), RT14_CHECKER)
    calls = [(node.lineno, ast.unparse(node.func), len(node.args),
              [keyword.arg for keyword in node.keywords])
             for node in ast.walk(tree) if isinstance(node, ast.Call)
             and "d9mod" in ast.unparse(node.func)]
    expected_calls = [
        (357, "d9mod.derive_class", 1, []),
        (358, "d9mod.derive_codes", 2, []),
        (472, "d9mod.V17.V16.derive_class", 1, []),
        (473, "d9mod.derive_class", 1, []),
        (480, "d9mod.reduce_concurrent", 2, []),
        (534, "authorities['d9mod'].check", 3, []),
    ]
    if sorted(calls) != sorted(expected_calls):
        findings.append("RT16-D9-CALL-SHAPES: exact six frozen calls drifted")
    rows: list[tuple[str, dict[str, Any], dict[str, Any], int]] = []
    for row in rt13["d9Derivation"]["rows"]:
        rows.append((row["id"], row["axes"], row["expectedTermination"],
                     row["expectedExitCode"]))
    local = rt14["contextualD9Rejoin"]["contextSplit"]["retentionLocalUnavailable"]
    rows.append(("RT14-LOCAL-UNAVAILABLE", local["axes"],
                 local["expectedReducerResult"]["termination"], local["expectedExitCode"]))
    matrix = rt14["contextualD9Rejoin"]["contextSplit"][
        "admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"]
    for row in matrix:
        expected_termination = {key: value for key, value in row["expectedTermination"].items()
                                if key != "executionId"}
        rows.append((row["id"], row["axes"], expected_termination,
                     row["expectedExitCode"]))
    try:
        derive_class_a = _resolve_d9_export(d9mod, "derive_class")
        derive_codes = _resolve_d9_export(d9mod, "derive_codes")
        old_derive_class = _resolve_d9_export(d9mod, "V17.V16.derive_class")
        derive_class_b = _resolve_d9_export(d9mod, "derive_class")
        reduce_concurrent = _resolve_d9_export(d9mod, "reduce_concurrent")
        retained_check = _resolve_d9_export(d9mod, "check")
        retained_findings = retained_check(
            copy.deepcopy(authority.parsed["d9-exit-contract.v1.8.json"]),
            copy.deepcopy(authority.parsed["d9-exit-contract.v1.7.json"]),
            copy.deepcopy(authority.parsed["d9-exit-contract.v1.6.json"]),
        )
        if retained_findings != []:
            findings.append("RT16-D9-CHECK: exact three-argument export rejected")
        old_classes: list[str] = []
        for row_id, axes, expected_termination, expected_exit in rows:
            axes_a = copy.deepcopy(axes)
            axes_b = copy.deepcopy(axes)
            class_a = derive_class_a(axes_a)
            class_b = derive_class_b(axes_b)
            codes = derive_codes(copy.deepcopy(axes), copy.deepcopy(d9["codeMaps"]))
            old_class = old_derive_class(copy.deepcopy(axes))
            old_classes.append(old_class)
            termination = {"class": class_a, **codes}
            if class_a != class_b or termination != expected_termination or \
                    d9["classToExitCode"][termination["class"]] != expected_exit or \
                    old_class not in d9["classToExitCode"]:
                findings.append(f"RT16-D9-ROW: {row_id} drifted")
        contextual_first = rows[12][1]
        if old_derive_class(copy.deepcopy(contextual_first)) != "operational-failed" or \
                derive_class_a(copy.deepcopy(contextual_first)) != "request-rejected":
            findings.append("RT16-D9-CHAINED-FALSIFIER: old/new class split drifted")
        control = rt14["contextualD9Rejoin"]["faultPrecedenceControl"]["conditions"]
        reduced = reduce_concurrent(
            copy.deepcopy(control), list(d9["causeModel"]["precedence"]))
        if reduced != {
                "faultCause": "durability-commit", "rejectionCause": "none",
                "deficiency": "none", "secondaryDeficiencies": []}:
            findings.append("RT16-D9-PRECEDENCE: exact reducer drifted")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(f"RT16-D9-API-TOTAL: controlled {type(exc).__name__}")
    return findings, len(calls), len(rows)


def _semantic_findings(candidate: dict[str, Any], expected: dict[str, Any],
                       authority: FrozenAuthority) -> list[str]:
    findings: list[str] = []
    rt13 = authority.parsed[RT13]
    rt17 = authority.parsed[RT20]
    if list(candidate) != ROOT_ORDER:
        findings.append("RT20-ROOT-ORDER: exact 20-root order drifted")
    unchanged = [
        "artifact", "claimId", "dependencies",
        "semanticBasisProjection", "operationalCustodyProjectionContract",
        "semanticLeaseProtocolV3",
        "storageAndLineage", "custodyPolicy",
        "integrationState", "assurance", "sealRecommendation",
        "rawPhysicalIdentityContract",
    ]
    for key in unchanged:
        difference = exact_recursive_equal(candidate.get(key), rt17[key], f"$.{key}")
        if difference:
            findings.append(f"RT21-RT20-NARROW-PASS-PRESERVATION: {difference}")
    for key in PROTECTED_ROOTS:
        if exact_recursive_equal(candidate.get(key), rt13[key], f"$.{key}"):
            findings.append(f"RT16-PROTECTED: {key} drifted from exact RT13 basis")
    if candidate.get("status") != RT21_STATUS:
        findings.append("RT21-STATUS: candidate/review boundary drifted")
    dependencies = candidate.get("dependencies")
    if dependencies != expected["dependencies"]:
        findings.append("RT16-DEPENDENCIES: semantic dependencies are not exactly EP8+RT13")
    basis = candidate.get("semanticBasisProjection")
    if not isinstance(basis, dict) or \
            basis.get("semanticCapabilityClosure") != rt13["capabilityClosure"]["semanticClosure"]:
        findings.append("RT16-SEMANTIC-BASIS: exact RT13 closure drifted")
    api = candidate.get("verifiedSemanticRtApiContract")
    try:
        fixtures = api["rawObjectResolutionConformance"]["fixtureGoldens"]
        expected_fixtures = expected["verifiedSemanticRtApiContract"][
            "rawObjectResolutionConformance"]["fixtureGoldens"]
        if len(fixtures) != 2:
            findings.append("RT16-FIXTURE-COUNT: exactly two embedded shapes required")
        for index, wanted in enumerate(expected_fixtures):
            actual = fixtures[index] if index < len(fixtures) else None
            findings.extend(_validate_fixture(actual, wanted, f"fixture[{index}]"))
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        findings.append(f"RT16-FIXTURE-TOTAL: controlled {type(exc).__name__}")
    try:
        old_closure = rt13["capabilityClosure"]["semanticClosure"]
        projection, encoded, ref, digest = derive_operational_projection(
            old_closure,
            "sha256:cc27c2beef32f3343d167c5727aa255b51884993ca416c4a862388e3be96a829",
            "sha256:70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
        )
        if (len(projection["requiredObjectRefs"]), len(projection["operationalUnits"]),
                len(encoded), ref, digest) != (
                23, 2, 10606,
                "sha256:49a09580190c2f12de3912581171b3ed77dbd9c85a81c8367978a16016d16b60",
                "sha256:58c16d46dca070edb155ff8373973638b20f08877006f9a871306ed8b1a6afd3"):
            findings.append("RT16-OP-RT13-GOLDEN: 23-ref compatibility projection drifted")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(f"RT16-OP-TOTAL: controlled {type(exc).__name__}")
    try:
        goldens = candidate["semanticLeaseProtocolV3"]["goldenScenarios"]
        for row in goldens:
            output = reduce_semantic_lease_v3(row["preState"], row["event"])
            difference = exact_recursive_equal(output, row["expectedOutput"])
            if difference:
                findings.append(f"RT16-LEASE-GOLDEN: {row.get('id')} {difference}")
        local = next(row for row in goldens if row["id"] == "SLV3-04-LOCAL-UNAVAILABLE")
        if not is_retention_local_unavailable_v1(local["expectedOutput"]):
            findings.append("RT16-LEASE-PREDICATE: local unavailable predicate drift")
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError) as exc:
        findings.append(f"RT16-LEASE-TOTAL: controlled {type(exc).__name__}")
    legacy, _count = _legacy_lease_findings(authority)
    findings.extend(legacy)
    d9_findings, _calls, _rows = _d9_compatibility_findings(authority)
    findings.extend(d9_findings)
    try:
        external = {
            row["recordCasRef"] for row in rt13["capabilityClosure"]["semanticClosure"]["proofRefs"]
        } - {
            row["recordCasRef"] for row in authority.parsed[EP8]["positiveVectors"][3]
            ["trustedStoreFixture"]["immutableCasRecords"]
        }
        if len(external) != 18 or set(DISCOVERED_OLD_PREIMAGES) | set(OLD_PATTERNED_REFS) != external or \
                set(DISCOVERED_OLD_PREIMAGES) & set(OLD_PATTERNED_REFS):
            findings.append("RT16-E8-FEASIBILITY: exact 7/18 + 11/18 partition drifted")
    except (KeyError, TypeError, IndexError) as exc:
        findings.append(f"RT16-E8-FEASIBILITY-TOTAL: controlled {type(exc).__name__}")
    return findings


def _inert_blob(tag: bytes, raw: bytes) -> bytes:
    return tag + len(raw).to_bytes(8, "big") + raw


def _encode_inert(value: Any) -> bytes:
    """One-to-one encoding of exactly the returned inert value vocabulary."""
    if value is None:
        return b"n"
    if type(value) is bool:
        return b"b1" if value else b"b0"
    if type(value) is int:
        try:
            encoded_integer = str(value).encode("ascii")
        except (ValueError, UnicodeError) as exc:
            raise AuthorityError("RT21-INERT-INTEGER-ENCODING") from exc
        return _inert_blob(b"i", encoded_integer)
    if type(value) is str:
        try:
            encoded_string = value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise AuthorityError("RT21-INERT-UTF8-STRING") from exc
        return _inert_blob(b"s", encoded_string)
    if type(value) is bytes:
        return _inert_blob(b"y", value)
    if type(value) is tuple:
        return _inert_blob(
            b"t", len(value).to_bytes(8, "big") + b"".join(
                _inert_blob(b"e", _encode_inert(item)) for item in value))
    if type(value) is MappingProxyType:
        rows: list[bytes] = []
        for key, item in value.items():
            if type(key) is not str:
                raise AuthorityError("RT21-INERT-MAPPING-KEY-TYPE")
            rows.extend((
                _inert_blob(b"k", _encode_inert(key)),
                _inert_blob(b"v", _encode_inert(item)),
            ))
        return _inert_blob(
            b"m", len(value).to_bytes(8, "big") + b"".join(rows))
    raise AuthorityError(
        f"RT21-INERT-UNDECLARED-VALUE-KIND:{type(value).__name__}")


def _freeze_inert(value: Any, path: str = "$", depth: int = 0,
                  nodes: list[int] | None = None) -> Any:
    """Copy exact JSON-like input without consulting user-defined protocols."""
    if nodes is None:
        nodes = [0]
    nodes[0] += 1
    if nodes[0] > INERT_MAX_NODES:
        raise AuthorityError(f"RT21-INERT-NODE-BUDGET:{path}")
    if depth > INERT_MAX_DEPTH:
        raise AuthorityError(f"RT21-INERT-DEPTH-BUDGET:{path}")
    if value is None or type(value) in (bool, int, str, bytes):
        return value
    if type(value) in (list, tuple):
        return tuple(_freeze_inert(
            item, f"{path}[{index}]", depth + 1, nodes)
            for index, item in enumerate(value))
    if type(value) is dict:
        output: dict[str, Any] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise AuthorityError(f"RT21-INERT-MAPPING-KEY-TYPE:{path}")
            output[key] = _freeze_inert(
                item, f"{path}.{key}", depth + 1, nodes)
        return MappingProxyType(output)
    raise AuthorityError(
        f"RT21-INERT-UNDECLARED-INPUT-KIND:{path}:{type(value).__name__}")


def _thaw_inert(value: Any, path: str = "$", depth: int = 0) -> Any:
    if depth > INERT_MAX_DEPTH:
        raise AuthorityError(f"RT21-INERT-DEPTH-BUDGET:{path}")
    if value is None or type(value) in (bool, int, str, bytes):
        return value
    if type(value) is tuple:
        return [_thaw_inert(item, f"{path}[{index}]", depth + 1)
                for index, item in enumerate(value)]
    if type(value) is MappingProxyType:
        return {key: _thaw_inert(item, f"{path}.{key}", depth + 1)
                for key, item in value.items()}
    raise AuthorityError(
        f"RT21-INERT-UNDECLARED-VALUE-KIND:{path}:{type(value).__name__}")


def _validate_inert_registries(
        value_registry: tuple[Mapping[str, str], ...] |
        list[Mapping[str, str]] = INERT_VALUE_REGISTRY,
        edge_registry: tuple[Mapping[str, str], ...] |
        list[Mapping[str, str]] = INERT_EDGE_REGISTRY) -> None:
    if tuple(row.get("id") for row in value_registry) != INERT_VALUE_IDS:
        raise AuthorityError(
            "RT21-INERT-VALUE-REGISTRY-DRIFT-BEFORE-ROOT")
    if tuple(row.get("id") for row in edge_registry) != INERT_EDGE_IDS:
        raise AuthorityError(
            "RT21-INERT-EDGE-REGISTRY-DRIFT-BEFORE-ROOT")


def _validate_inert_value(
        root: Any, *,
        value_registry: tuple[Mapping[str, str], ...] |
        list[Mapping[str, str]] = INERT_VALUE_REGISTRY,
        edge_registry: tuple[Mapping[str, str], ...] |
        list[Mapping[str, str]] = INERT_EDGE_REGISTRY) -> dict[str, Any]:
    _validate_inert_registries(value_registry, edge_registry)
    active: set[int] = set()
    seen: set[int] = set()
    value_counts = {name: 0 for name in INERT_VALUE_IDS}
    edge_counts = {name: 0 for name in INERT_EDGE_IDS}
    visited = 0

    def visit(value: Any, path: str, depth: int) -> None:
        nonlocal visited
        visited += 1
        if visited > INERT_MAX_NODES:
            raise AuthorityError(f"RT21-INERT-NODE-BUDGET:{path}")
        if depth > INERT_MAX_DEPTH:
            raise AuthorityError(f"RT21-INERT-DEPTH-BUDGET:{path}")
        if value is None:
            value_counts["null"] += 1
            return
        if type(value) is bool:
            value_counts["boolean"] += 1
            return
        if type(value) is int:
            value_counts["integer"] += 1
            return
        if type(value) is str:
            value_counts["utf8-string"] += 1
            return
        if type(value) is bytes:
            value_counts["immutable-bytes"] += 1
            return
        if type(value) is tuple:
            kind = "immutable-tuple"
        elif type(value) is MappingProxyType:
            kind = "readonly-string-map"
        else:
            raise AuthorityError(
                f"RT21-INERT-UNDECLARED-VALUE-KIND:{path}:"
                f"{type(value).__name__}")
        identity = id(value)
        if identity in active:
            raise AuthorityError(f"RT21-INERT-CYCLE:{path}")
        if identity in seen:
            return
        active.add(identity)
        seen.add(identity)
        value_counts[kind] += 1
        try:
            if type(value) is tuple:
                for index, item in enumerate(value):
                    edge_counts["tuple-item"] += 1
                    visit(item, f"{path}[{index}]", depth + 1)
            else:
                for index, (key, item) in enumerate(value.items()):
                    edge_counts["mapping-key"] += 1
                    if type(key) is not str:
                        raise AuthorityError(
                            f"RT21-INERT-MAPPING-KEY-TYPE:{path}[{index}]")
                    visit(key, f"{path}.key[{index}]", depth + 1)
                    edge_counts["mapping-value"] += 1
                    visit(item, f"{path}.{key}", depth + 1)
        finally:
            active.remove(identity)

    visit(root, "$", 0)
    return {"visited": visited, "containerCount": len(seen),
            "valueCounts": value_counts, "edgeCounts": edge_counts}


def _inert_snapshot_payload(snapshot: Mapping[str, Any]) -> MappingProxyType:
    return MappingProxyType({key: snapshot[key] for key in INERT_SNAPSHOT_FIELDS
                             if key != "snapshotId"})


def _inert_snapshot_id(payload: MappingProxyType) -> str:
    return domain_digest(
        "opensip.verified-semantic-rt-snapshot.v2.inert-v1",
        _encode_inert(payload))


def _authenticate_inert_snapshot(snapshot: Any) -> dict[str, Any]:
    scan = _validate_inert_value(snapshot)
    if type(snapshot) is not MappingProxyType or \
            tuple(snapshot) != INERT_SNAPSHOT_FIELDS:
        raise AuthorityError("RT21-INERT-SNAPSHOT-CLOSED-SHAPE")
    if snapshot["schemaVersion"] != 2 or \
            type(snapshot["schemaVersion"]) is not int or \
            snapshot["kind"] != "VERIFIED_SEMANTIC_RT_SNAPSHOT_V2" or \
            snapshot["hostOperationIds"] != INERT_HOST_OPERATION_IDS:
        raise AuthorityError("RT21-INERT-SNAPSHOT-CLOSED-SHAPE")
    if snapshot["snapshotId"] != _inert_snapshot_id(
            _inert_snapshot_payload(snapshot)):
        raise AuthorityError("RT21-INERT-SNAPSHOT-COMMITMENT")
    return scan


def VerifiedSemanticRTSnapshotV2(
        candidate: dict[str, Any], authority: FrozenAuthority) -> MappingProxyType:
    """Construct the nominal snapshot as inert data, not a custom instance."""
    if authority.ep8_receipt_data is None or \
            authority.fixture_projection_data is None:
        raise AuthorityError("EP8 data-only receipt was not constructed")
    copy_nodes = [0]
    payload = MappingProxyType({
        "schemaVersion": 2,
        "kind": "VERIFIED_SEMANTIC_RT_SNAPSHOT_V2",
        "candidate": _freeze_inert(candidate, nodes=copy_nodes),
        "rt13": _freeze_inert(authority.parsed[RT13], nodes=copy_nodes),
        "ep8DerivationReceipt": _freeze_inert(
            authority.ep8_receipt_data, nodes=copy_nodes),
        "fixtureProjection": _freeze_inert(
            authority.fixture_projection_data, nodes=copy_nodes),
        "hostOperationIds": INERT_HOST_OPERATION_IDS,
    })
    snapshot = MappingProxyType({
        "schemaVersion": payload["schemaVersion"],
        "kind": payload["kind"],
        "snapshotId": _inert_snapshot_id(payload),
        "candidate": payload["candidate"],
        "rt13": payload["rt13"],
        "ep8DerivationReceipt": payload["ep8DerivationReceipt"],
        "fixtureProjection": payload["fixtureProjection"],
        "hostOperationIds": payload["hostOperationIds"],
    })
    _authenticate_inert_snapshot(snapshot)
    return snapshot


def derive_operational_custody_projection_v1(
        snapshot: Any, bundle: Mapping[str, Any],
        closure: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
    _authenticate_inert_snapshot(snapshot)
    if not isinstance(bundle, Mapping):
        raise AuthorityError("RT21-HOST-BUNDLE-SHAPE")
    try:
        bundle_ref = bundle["proofBundleCasRef"]
        closure_ref = bundle["semanticClosureCasRef"]
    except (KeyError, TypeError) as exc:
        raise AuthorityError("RT21-HOST-BUNDLE-REFS") from exc
    projection, _encoded, ref, digest = derive_operational_projection(
        copy.deepcopy(closure), bundle_ref, closure_ref)
    return projection, ref, digest


def validate_raw_object_resolution_v1(
        snapshot: Any, raw_bytes: bytes,
        request: dict[str, Any]) -> dict[str, Any]:
    _authenticate_inert_snapshot(snapshot)
    return validate_raw_object_resolution(raw_bytes, copy.deepcopy(request))


def _host_reduce(snapshot: Any, state: dict[str, Any],
                 event: dict[str, Any], expected_kind: str) -> dict[str, Any]:
    _authenticate_inert_snapshot(snapshot)
    if type(event) is not dict or event.get("kind") != expected_kind:
        raise AuthorityError(f"RT21-HOST-LEASE-EVENT-KIND:{expected_kind}")
    return reduce_semantic_lease_v3(copy.deepcopy(state), copy.deepcopy(event))


def reduce_expiry_v1(snapshot: Any, state: dict[str, Any],
                     event: dict[str, Any]) -> dict[str, Any]:
    return _host_reduce(snapshot, state, event, "expiry")


def reduce_release_v1(snapshot: Any, state: dict[str, Any],
                      event: dict[str, Any]) -> dict[str, Any]:
    return _host_reduce(snapshot, state, event, "release")


def reduce_crash_reclaim_v3(snapshot: Any, state: dict[str, Any],
                            event: dict[str, Any]) -> dict[str, Any]:
    return _host_reduce(snapshot, state, event, "crash-reclaim")


def reduce_resolve_and_pin_v2(snapshot: Any, state: dict[str, Any],
                              event: dict[str, Any]) -> dict[str, Any]:
    return _host_reduce(snapshot, state, event, "resolve-and-pin")


def host_is_retention_local_unavailable_v1(
        snapshot: Any, output: dict[str, Any]) -> bool:
    _authenticate_inert_snapshot(snapshot)
    return is_retention_local_unavailable_v1(copy.deepcopy(output))


HOST_OPERATION_REGISTRY = MappingProxyType({
    "derive_operational_custody_projection_v1":
        derive_operational_custody_projection_v1,
    "validate_raw_object_resolution_v1": validate_raw_object_resolution_v1,
    "reduce_expiry_v1": reduce_expiry_v1,
    "reduce_release_v1": reduce_release_v1,
    "reduce_crash_reclaim_v3": reduce_crash_reclaim_v3,
    "reduce_resolve_and_pin_v2": reduce_resolve_and_pin_v2,
    "is_retention_local_unavailable_v1":
        host_is_retention_local_unavailable_v1,
})


def _graph_registry_findings(
        registry: tuple[Mapping[str, str], ...] | list[Mapping[str, str]],
) -> list[str]:
    """Validate the exact ordered registry without invoking hostile values."""
    findings: list[str] = []
    try:
        rows = tuple(registry)
    except BaseException as exc:
        return ["RT20-GRAPH-TRAVERSAL-ERROR: path=$ edge=edge-registry "
                f"exception={type(exc).__name__}"]
    ids: list[str] = []
    malformed = False
    for index, row in enumerate(rows):
        if type(row) is not dict or type(row.get("id")) is not str:
            findings.append(
                "RT20-GRAPH-UNKNOWN-EDGE-TYPE: "
                f"registryIndex={index} declaration=malformed")
            malformed = True
            continue
        ids.append(row["id"])
    if malformed:
        return findings
    seen_ids: set[str] = set()
    for edge_id in ids:
        if edge_id in seen_ids:
            findings.append(
                f"RT20-GRAPH-REGISTRY-DUPLICATE: edge={edge_id}")
        seen_ids.add(edge_id)
    for edge_id in GRAPH_EDGE_IDS:
        if edge_id not in seen_ids:
            findings.append(f"RT20-GRAPH-REGISTRY-MISSING: edge={edge_id}")
    for edge_id in ids:
        if edge_id not in GRAPH_EDGE_IDS:
            findings.append(
                f"RT20-GRAPH-UNKNOWN-EDGE-TYPE: edge={edge_id}")
    if not findings and tuple(ids) != GRAPH_EDGE_IDS:
        findings.append("RT20-GRAPH-REGISTRY-ORDER: exact order drifted")
    if not findings:
        for index, (row, expected) in enumerate(zip(rows, GRAPH_EDGE_REGISTRY)):
            if row != expected:
                findings.append(
                    "RT20-GRAPH-REGISTRY-DECLARATION: "
                    f"index={index} exact row drifted")
                break
    return findings


def _runtime_registry_findings(
        registry: tuple[Mapping[str, str], ...] | list[Mapping[str, str]],
) -> list[str]:
    """Validate the exact ordered runtime-kind denominator."""
    findings: list[str] = []
    try:
        rows = tuple(registry)
    except BaseException as exc:
        return ["RT20-GRAPH-TRAVERSAL-ERROR: path=$ "
                f"edge=runtime-kind-registry exception={type(exc).__name__}"]
    ids: list[str] = []
    for index, row in enumerate(rows):
        if type(row) is not dict or type(row.get("id")) is not str or \
                row.get("disposition") not in ("leaf", "traverse", "refuse"):
            findings.append(
                "RT20-GRAPH-RUNTIME-REGISTRY-UNKNOWN: "
                f"registryIndex={index} declaration=malformed")
            continue
        ids.append(row["id"])
    if findings:
        return findings
    seen: set[str] = set()
    for kind_id in ids:
        if kind_id in seen:
            findings.append(
                f"RT20-GRAPH-RUNTIME-REGISTRY-DUPLICATE: kind={kind_id}")
        seen.add(kind_id)
    for kind_id in GRAPH_RUNTIME_KIND_IDS:
        if kind_id not in seen:
            findings.append(
                f"RT20-GRAPH-RUNTIME-REGISTRY-MISSING: kind={kind_id}")
    for kind_id in ids:
        if kind_id not in GRAPH_RUNTIME_KIND_IDS:
            findings.append(
                f"RT20-GRAPH-RUNTIME-REGISTRY-UNKNOWN: kind={kind_id}")
    if not findings and tuple(ids) != GRAPH_RUNTIME_KIND_IDS:
        findings.append(
            "RT20-GRAPH-RUNTIME-REGISTRY-ORDER: exact order drifted")
    if not findings:
        for index, (row, expected) in enumerate(
                zip(rows, GRAPH_RUNTIME_KIND_REGISTRY)):
            if row != expected:
                findings.append(
                    "RT20-GRAPH-RUNTIME-REGISTRY-DECLARATION: "
                    f"index={index} exact row drifted")
                break
    return findings


def _semantic_child_denominator_findings(
        denominator: tuple[Mapping[str, Any], ...] |
        list[Mapping[str, Any]],
        exceptions: tuple[Mapping[str, Any], ...] |
        list[Mapping[str, Any]],
) -> list[str]:
    """Validate the independent kind-to-child denominator and exceptions."""
    findings: list[str] = []
    if sys.implementation.name != "cpython" or sys.version_info[:2] != (3, 14):
        findings.append(
            "RT20-GRAPH-REFERENT-ORACLE-RUNTIME: CPython 3.14 required")
    try:
        rows = tuple(denominator)
        exception_rows = tuple(exceptions)
    except BaseException as exc:
        return ["RT20-GRAPH-TRAVERSAL-ERROR: path=$ "
                f"edge=semantic-child-denominator exception={type(exc).__name__}"]
    ids: list[str] = []
    declared_edges: set[str] = set()
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(rows):
        if type(row) is not dict or set(row) != {
                "id", "oracle", "requiredEdges"} or \
                type(row.get("id")) is not str or \
                row.get("oracle") not in {
                    "LEAF-AUDIT", "CPYTHON-GC-REFERENTS",
                    "EXPLICIT-GC-EXCEPTION", "REFUSE"} or \
                type(row.get("requiredEdges")) is not list or \
                any(type(edge) is not str for edge in row["requiredEdges"]):
            findings.append(
                "RT20-GRAPH-CHILD-DENOMINATOR-UNKNOWN: "
                f"index={index} declaration=malformed")
            continue
        kind_id = row["id"]
        ids.append(kind_id)
        by_id[kind_id] = row
        if len(row["requiredEdges"]) != len(set(row["requiredEdges"])):
            findings.append(
                "RT20-GRAPH-CHILD-DENOMINATOR-DUPLICATE-EDGE: "
                f"kind={kind_id}")
        for edge in row["requiredEdges"]:
            if edge not in GRAPH_EDGE_IDS:
                findings.append(
                    "RT20-GRAPH-CHILD-DENOMINATOR-UNKNOWN-EDGE: "
                    f"kind={kind_id} edge={edge}")
            declared_edges.add(edge)
    if len(ids) != len(set(ids)):
        findings.append("RT20-GRAPH-CHILD-DENOMINATOR-DUPLICATE-KIND")
    for kind_id in GRAPH_SEMANTIC_CHILD_IDS:
        if kind_id not in ids:
            findings.append(
                "RT20-GRAPH-CHILD-DENOMINATOR-MISSING: "
                f"kind={kind_id}")
    for kind_id in ids:
        if kind_id not in GRAPH_SEMANTIC_CHILD_IDS:
            findings.append(
                "RT20-GRAPH-CHILD-DENOMINATOR-UNKNOWN: "
                f"kind={kind_id}")
    if not findings and tuple(ids) != GRAPH_SEMANTIC_CHILD_IDS:
        findings.append(
            "RT20-GRAPH-CHILD-DENOMINATOR-ORDER: exact order drifted")
    if not findings:
        for index, (row, expected) in enumerate(
                zip(rows, GRAPH_SEMANTIC_CHILD_DENOMINATOR)):
            if row != expected:
                findings.append(
                    "RT20-GRAPH-CHILD-DENOMINATOR-DECLARATION: "
                    f"index={index} exact row drifted")
                break
    if declared_edges != set(GRAPH_EDGE_IDS):
        findings.append(
            "RT20-GRAPH-CHILD-DENOMINATOR-EDGE-COVERAGE: "
            "edge registry and semantic-child denominator differ")

    exception_by_kind: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(exception_rows):
        if type(row) is not dict or set(row) != {
                "runtimeKind", "reason", "requiredEdges"} or \
                type(row.get("runtimeKind")) is not str or \
                type(row.get("reason")) is not str or not row["reason"] or \
                type(row.get("requiredEdges")) is not list:
            findings.append(
                "RT20-GRAPH-ORACLE-EXCEPTION-UNKNOWN: "
                f"index={index} declaration=malformed")
            continue
        exception_by_kind[row["runtimeKind"]] = row
    expected_exception_kinds = ("memoryview", "code", "frame")
    if tuple(exception_by_kind) != expected_exception_kinds:
        findings.append(
            "RT20-GRAPH-ORACLE-EXCEPTION-SET: exact memoryview/code/frame set required")
    if not findings and tuple(exception_rows) != GRAPH_REFERENT_ORACLE_EXCEPTIONS:
        findings.append(
            "RT20-GRAPH-ORACLE-EXCEPTION-DECLARATION: exact rows drifted")
    for kind_id in expected_exception_kinds:
        denominator_row = by_id.get(kind_id)
        exception_row = exception_by_kind.get(kind_id)
        if denominator_row is None or exception_row is None or \
                denominator_row.get("oracle") != "EXPLICIT-GC-EXCEPTION" or \
                exception_row.get("requiredEdges") != \
                denominator_row.get("requiredEdges"):
            findings.append(
                "RT20-GRAPH-ORACLE-EXCEPTION-BINDING: "
                f"kind={kind_id}")
    return findings


def _positive_case_denominator_findings(case_ids: list[str] | tuple[str, ...]) -> list[str]:
    """Validate the independently declared two-root positive fixture set."""
    findings: list[str] = []
    if any(type(case_id) is not str for case_id in case_ids):
        return ["RT20-GRAPH-POSITIVE-DENOMINATOR-UNKNOWN: malformed id"]
    if len(case_ids) != len(set(case_ids)):
        findings.append("RT20-GRAPH-POSITIVE-DENOMINATOR-DUPLICATE")
    for case_id in GRAPH_POSITIVE_CASE_IDS:
        if case_id not in case_ids:
            findings.append(
                f"RT20-GRAPH-POSITIVE-DENOMINATOR-MISSING: case={case_id}")
    for case_id in case_ids:
        if case_id not in GRAPH_POSITIVE_CASE_IDS:
            findings.append(
                f"RT20-GRAPH-POSITIVE-DENOMINATOR-UNKNOWN: case={case_id}")
    if not findings and tuple(case_ids) != GRAPH_POSITIVE_CASE_IDS:
        findings.append(
            "RT20-GRAPH-POSITIVE-DENOMINATOR-ORDER: exact order drifted")
    return findings


def _graph_error(path: str, edge: str, exc: BaseException) -> str:
    return (f"RT20-GRAPH-TRAVERSAL-ERROR: path={path} edge={edge} "
            f"exception={type(exc).__name__}")


def _python_mangled_slot(owner: type, name: str) -> str:
    if not name.startswith("__") or name.endswith("__"):
        return name
    owner_name = type.__getattribute__(owner, "__name__").lstrip("_")
    return name if not owner_name else "_" + owner_name + name


def _slot_storage_names(
        value: Any, path: str,
) -> tuple[list[str], list[str]]:
    names: list[str] = []
    findings: list[str] = []
    runtime_type = type(value)
    try:
        mro = type.__getattribute__(runtime_type, "__mro__")
    except BaseException as exc:
        return [], [_graph_error(path, "object-slots-mro-mangled", exc)]
    for owner_index, owner in enumerate(mro):
        owner_path = f"{path}.__class__.__mro__[{owner_index}]"
        try:
            namespace = type.__getattribute__(owner, "__dict__")
            declared = namespace.get("__slots__", ())
        except BaseException as exc:
            findings.append(_graph_error(
                owner_path, "object-slots-mro-mangled", exc))
            continue
        if isinstance(declared, str):
            declared_names = (declared,)
        else:
            declared_names_list: list[Any] = []
            try:
                iterator = iter(declared)
                while True:
                    try:
                        declared_names_list.append(next(iterator))
                    except StopIteration:
                        break
            except BaseException as exc:
                findings.append(_graph_error(
                    owner_path, "object-slots-mro-mangled", exc))
                continue
            declared_names = tuple(declared_names_list)
        for declared_name in declared_names:
            if type(declared_name) is not str:
                findings.append(
                    "RT20-GRAPH-TRAVERSAL-ERROR: "
                    f"path={owner_path} edge=object-slots-mro-mangled "
                    "exception=NonStringSlot")
                continue
            if declared_name in ("__dict__", "__weakref__"):
                continue
            try:
                storage_name = _python_mangled_slot(owner, declared_name)
            except BaseException as exc:
                findings.append(_graph_error(
                    owner_path, "object-slots-mro-mangled", exc))
                continue
            if storage_name not in names:
                names.append(storage_name)
    return names, findings


def _runtime_kind(
        value: Any, path: str, declared_object_types: dict[int, type],
) -> tuple[str | None, list[str]]:
    """Return one exact admitted runtime kind or a controlled refusal."""
    try:
        value_type = type(value)
        if value_type in ATOMIC_RUNTIME_TYPES:
            return "atomic-exact", []
        if value_type in OPAQUE_ATOMIC_RUNTIME_TYPES:
            return "opaque-runtime-exact", []
        if value_type is slice:
            return "slice", []
        if value_type is types.CodeType:
            return "code", []
        if isinstance(value, MappingABC):
            return "mapping", []
        if isinstance(value, (list, tuple, deque)):
            return "sequence", []
        if isinstance(value, (set, frozenset)):
            return "set", []
        if isinstance(value, memoryview):
            return "memoryview", []
        if isinstance(value, types.MethodType):
            return "bound-python-method", []
        if isinstance(value, BUILTIN_BOUND_TYPES):
            return "bound-builtin", []
        if isinstance(value, functools.partial):
            return "partial", []
        if isinstance(value, types.FunctionType):
            return "python-function", []
        if isinstance(value, types.ModuleType):
            return "module", []
        if isinstance(value, CELL_TYPE):
            return "closure-cell", []
        if isinstance(value, property):
            return "property", []
        if isinstance(value, (classmethod, staticmethod)):
            return "wrapped-descriptor", []
        if isinstance(value, DESCRIPTOR_TYPES):
            return "builtin-descriptor", []
        if isinstance(value, type):
            declared_object_types[id(value)] = value
            return "class", []
        if isinstance(value, types.FrameType):
            return "frame", []
        if isinstance(value, types.GeneratorType):
            return "generator", []
        if isinstance(value, types.CoroutineType):
            return "coroutine", []
        if isinstance(value, types.AsyncGeneratorType):
            return "async-generator", []
        runtime_module = type.__getattribute__(value_type, "__module__")
        if runtime_module != "builtins" and \
                declared_object_types.get(id(value_type)) is value_type:
            return "declared-nonbuiltin-object", []
    except BaseException as exc:
        return None, [_graph_error(path, "runtime-kind-dispatch", exc)]
    return None, [
        "RT20-GRAPH-UNKNOWN-RUNTIME-TYPE: "
        f"path={path} type={value_type.__name__}"
    ]


def _owned_graph_children(
        value: Any, path: str,
) -> tuple[list[tuple[str, Any]], list[str]]:
    """Return every declared semantic child; convert all access failures."""
    rows: list[tuple[str, Any]] = []
    findings: list[str] = []

    def capture(edge: str, suffix: str, getter: Callable[[], Any],
                *, absent: tuple[type[BaseException], ...] = (),
                omit_none: bool = False) -> None:
        try:
            child = getter()
        except absent:
            return
        except BaseException as exc:
            findings.append(_graph_error(path + suffix, edge, exc))
            return
        if not (omit_none and child is None):
            rows.append((path + suffix, child))

    # Independent direct-strong-referent oracle.  Explicit extractors below
    # retain stable semantic paths and close memoryview/code/frame exceptions;
    # this oracle prevents a future or forgotten standard metadata link from
    # silently becoming a clean leaf.
    if not (isinstance(value, memoryview) or
            type(value) is types.CodeType or
            isinstance(value, types.FrameType)):
        try:
            for index, child in enumerate(gc.get_referents(value)):
                rows.append((f"{path}.runtimeReferent[{index}]", child))
        except BaseException as exc:
            findings.append(_graph_error(path, "runtime-referents", exc))

    if isinstance(value, MappingABC):
        edge = "mapping-keys-values"
        try:
            item_view = value.items()
            iterator = iter(item_view)
            index = 0
            while True:
                try:
                    pair = next(iterator)
                except StopIteration:
                    break
                try:
                    key, item = pair
                except BaseException as exc:
                    findings.append(_graph_error(
                        f"{path}.mappingItem[{index}]", edge, exc))
                    break
                rows.append((f"{path}.mappingKey[{index}]", key))
                rows.append((f"{path}.mappingValue[{index}]", item))
                index += 1
        except BaseException as exc:
            findings.append(_graph_error(path, edge, exc))
    elif isinstance(value, (list, tuple, deque)):
        edge = "sequence-items"
        try:
            iterator = iter(value)
            index = 0
            while True:
                try:
                    item = next(iterator)
                except StopIteration:
                    break
                rows.append((f"{path}.sequenceItem[{index}]", item))
                index += 1
        except BaseException as exc:
            findings.append(_graph_error(path, edge, exc))
    elif isinstance(value, (set, frozenset)):
        edge = "set-items"
        try:
            iterator = iter(value)
            index = 0
            while True:
                try:
                    item = next(iterator)
                except StopIteration:
                    break
                rows.append((f"{path}.setItem[{index}]", item))
                index += 1
        except BaseException as exc:
            findings.append(_graph_error(path, edge, exc))

    if isinstance(value, memoryview):
        capture("memoryview-backing-object", ".obj", lambda: value.obj)
    if type(value) is slice:
        capture("slice-start", ".start", lambda: value.start)
        capture("slice-stop", ".stop", lambda: value.stop)
        capture("slice-step", ".step", lambda: value.step)
    if type(value) is types.CodeType:
        try:
            constants = value.co_consts
            for index, child in enumerate(constants):
                rows.append((f"{path}.co_consts[{index}]", child))
        except BaseException as exc:
            findings.append(_graph_error(
                path + ".co_consts", "code-constants", exc))
    if isinstance(value, types.MethodType):
        capture("bound-method-owner", ".__self__", lambda: value.__self__)
        capture("bound-method-function", ".__func__", lambda: value.__func__)
    if isinstance(value, BUILTIN_BOUND_TYPES):
        capture("builtin-bound-owner", ".__self__",
                lambda: object.__getattribute__(value, "__self__"),
                absent=(AttributeError,), omit_none=True)
    if isinstance(value, functools.partial):
        capture("partial-function", ".func", lambda: value.func)
        capture("partial-args", ".args", lambda: value.args)
        capture("partial-keywords", ".keywords", lambda: value.keywords,
                omit_none=True)
    if isinstance(value, types.FunctionType):
        capture("function-globals", ".__globals__", lambda: value.__globals__)
        try:
            closure = value.__closure__
            if closure is not None:
                for index, cell in enumerate(closure):
                    rows.append((f"{path}.__closure__[{index}]", cell))
        except BaseException as exc:
            findings.append(_graph_error(
                path + ".__closure__", "function-closure-cells", exc))
        capture("function-defaults", ".__defaults__", lambda: value.__defaults__,
                omit_none=True)
        capture("function-kwdefaults", ".__kwdefaults__",
                lambda: value.__kwdefaults__, omit_none=True)
        capture("function-annotations", ".__annotations__",
                lambda: value.__annotations__)
        capture("function-attributes", ".__dict__", lambda: value.__dict__)
        capture("function-code", ".__code__", lambda: value.__code__)
        capture("function-builtins", ".__builtins__", lambda: value.__builtins__)
        capture("function-doc", ".__doc__", lambda: value.__doc__,
                omit_none=True)
        capture("function-module", ".__module__", lambda: value.__module__,
                omit_none=True)
        capture("function-type-params", ".__type_params__",
                lambda: value.__type_params__)
        capture("function-annotate", ".__annotate__",
                lambda: value.__annotate__, omit_none=True)
    elif isinstance(value, types.ModuleType):
        capture("module-dictionary", ".__dict__",
                lambda: types.ModuleType.__getattribute__(value, "__dict__"))
    if isinstance(value, CELL_TYPE):
        capture("cell-contents", ".cell_contents", lambda: value.cell_contents,
                absent=(ValueError,))

    if isinstance(value, property):
        capture("property-accessors", ".fget", lambda: value.fget,
                omit_none=True)
        capture("property-accessors", ".fset", lambda: value.fset,
                omit_none=True)
        capture("property-accessors", ".fdel", lambda: value.fdel,
                omit_none=True)
        capture("property-doc", ".__doc__", lambda: value.__doc__,
                omit_none=True)
        capture("property-name", ".__name__", lambda: value.__name__,
                omit_none=True)
    if isinstance(value, (classmethod, staticmethod)):
        capture("wrapped-descriptor-function", ".__func__",
                lambda: object.__getattribute__(value, "__func__"))
    if isinstance(value, DESCRIPTOR_TYPES):
        capture("descriptor-owner", ".__objclass__",
                lambda: object.__getattribute__(value, "__objclass__"),
                absent=(AttributeError,))

    if isinstance(value, type):
        capture("class-dictionary", ".__dict__",
                lambda: type.__getattribute__(value, "__dict__"))
        capture("class-bases", ".__bases__",
                lambda: type.__getattribute__(value, "__bases__"))
        capture("class-mro", ".__mro__",
                lambda: type.__getattribute__(value, "__mro__"))
        capture("class-metaclass", ".__class__", lambda: type(value))
    elif isinstance(value, types.FrameType):
        capture("frame-globals", ".f_globals", lambda: value.f_globals)
        capture("frame-locals", ".f_locals", lambda: value.f_locals)
        capture("frame-back", ".f_back", lambda: value.f_back,
                omit_none=True)
        capture("frame-builtins", ".f_builtins", lambda: value.f_builtins)
        capture("frame-code", ".f_code", lambda: value.f_code)
        capture("frame-trace", ".f_trace", lambda: value.f_trace,
                omit_none=True)
        capture("frame-generator", ".f_generator", lambda: value.f_generator,
                omit_none=True)
    elif isinstance(value, types.GeneratorType):
        capture("generator-frame", ".gi_frame", lambda: value.gi_frame,
                omit_none=True)
        capture("generator-code", ".gi_code", lambda: value.gi_code)
        capture("generator-yieldfrom", ".gi_yieldfrom",
                lambda: value.gi_yieldfrom, omit_none=True)
    elif isinstance(value, types.CoroutineType):
        capture("coroutine-frame", ".cr_frame", lambda: value.cr_frame,
                omit_none=True)
        capture("coroutine-code", ".cr_code", lambda: value.cr_code)
        capture("coroutine-await", ".cr_await", lambda: value.cr_await,
                omit_none=True)
        capture("coroutine-origin", ".cr_origin", lambda: value.cr_origin,
                omit_none=True)
    elif isinstance(value, types.AsyncGeneratorType):
        capture("async-generator-frame", ".ag_frame", lambda: value.ag_frame,
                omit_none=True)
        capture("async-generator-code", ".ag_code", lambda: value.ag_code)
        capture("async-generator-await", ".ag_await", lambda: value.ag_await,
                omit_none=True)
    elif not isinstance(value, (types.FunctionType, types.ModuleType)):
        capture("object-attributes", ".__dict__",
                lambda: object.__getattribute__(value, "__dict__"),
                absent=(AttributeError,))
        slot_names, slot_findings = _slot_storage_names(value, path)
        findings.extend(slot_findings)
        for name in slot_names:
            capture("object-slots-mro-mangled", "." + name,
                    lambda name=name: object.__getattribute__(value, name),
                    absent=(AttributeError,))
        runtime_type = type(value)
        try:
            runtime_module = type.__getattribute__(runtime_type, "__module__")
        except BaseException as exc:
            findings.append(_graph_error(path, "object-class", exc))
        else:
            if runtime_module != "builtins":
                rows.append((path + ".__class__", runtime_type))
    return rows, findings


def _predeclared_runtime_types(
        root: Any, admitted: tuple[type, ...], max_nodes: int,
        max_depth: int,
) -> dict[int, type]:
    """Discover exact class objects without expanding unknown instances.

    This is a declaration pass, not a validation pass.  Only already admitted
    structural kinds are expanded.  A class object reachable independently of
    an instance becomes an exact scan-local type declaration; an injected
    opaque instance cannot declare its own type through ``__class__``.
    """
    declared: dict[int, type] = {id(item): item for item in admitted}
    snapshot_type = globals().get("VerifiedSemanticRTSnapshotV2")
    if isinstance(snapshot_type, type) and type(root) is snapshot_type:
        declared[id(snapshot_type)] = snapshot_type
    queue: deque[tuple[str, Any, int]] = deque([("$", root, 0)])
    expanded: dict[int, Any] = {}
    while queue and len(expanded) <= max_nodes:
        path, value, depth = queue.popleft()
        identity = id(value)
        if expanded.get(identity) is value:
            continue
        expanded[identity] = value
        value_type = type(value)
        try:
            opaque_key = (
                type.__getattribute__(value_type, "__module__"),
                type.__getattribute__(value_type, "__qualname__"),
            )
        except BaseException:
            opaque_key = ("", "")
        if opaque_key in SAFE_OPAQUE_RUNTIME_TYPE_KEYS:
            declared[id(value_type)] = value_type
        kind, _kind_findings = _runtime_kind(value, path, declared)
        if kind is None or GRAPH_RUNTIME_DISPOSITIONS.get(kind) == "leaf" or \
                depth >= max_depth:
            continue
        try:
            children, _child_findings = _owned_graph_children(value, path)
        except BaseException:
            continue
        for child_path, child in children:
            queue.append((child_path, child, depth + 1))
    return declared


def _forbidden_identity_paths(
        root: Any, forbidden: Mapping[int, str],
        max_nodes: int = GRAPH_MAX_NODES, max_depth: int = GRAPH_MAX_DEPTH,
        registry: tuple[Mapping[str, str], ...] | list[Mapping[str, str]] =
        GRAPH_EDGE_REGISTRY,
        runtime_registry: tuple[Mapping[str, str], ...] |
        list[Mapping[str, str]] = GRAPH_RUNTIME_KIND_REGISTRY,
        child_denominator: tuple[Mapping[str, Any], ...] |
        list[Mapping[str, Any]] = GRAPH_SEMANTIC_CHILD_DENOMINATOR,
        oracle_exceptions: tuple[Mapping[str, Any], ...] |
        list[Mapping[str, Any]] = GRAPH_REFERENT_ORACLE_EXCEPTIONS,
        admitted_runtime_types: tuple[type, ...] = (),
) -> dict[str, Any]:
    registry_findings = (_graph_registry_findings(registry) +
                         _runtime_registry_findings(runtime_registry) +
                         _semantic_child_denominator_findings(
                             child_denominator, oracle_exceptions))
    if registry_findings:
        return {"forbiddenHits": [], "visited": 0,
                "findings": registry_findings, "clean": False}
    if type(max_nodes) is not int or max_nodes < 1:
        return {"forbiddenHits": [], "visited": 0,
                "findings": [f"RT20-GRAPH-NODE-BUDGET: invalid={max_nodes}"],
                "clean": False}
    if type(max_depth) is not int or max_depth < 1:
        return {"forbiddenHits": [], "visited": 0,
                "findings": [f"RT20-GRAPH-DEPTH-BUDGET: invalid={max_depth}"],
                "clean": False}
    queue: deque[tuple[str, Any, int]] = deque([("$", root, 0)])
    # Strong-reference identity custody is retained for the entire scan.
    # Therefore CPython cannot reclaim an expanded object and reuse its id for
    # a distinct later mappingproxy (or any other child).
    expanded: dict[int, Any] = {}
    missing_identity = object()
    if any(not isinstance(item, type) for item in admitted_runtime_types):
        return {"forbiddenHits": [], "visited": 0,
                "findings": [
                    "RT20-GRAPH-RUNTIME-REGISTRY-UNKNOWN: "
                    "admitted runtime type declaration malformed"],
                "clean": False}
    declared_object_types = _predeclared_runtime_types(
        root, admitted_runtime_types, max_nodes, max_depth)
    hits: list[dict[str, str]] = []
    findings: list[str] = []
    while queue:
        path, value, depth = queue.popleft()
        identity = id(value)
        prior = expanded.get(identity, missing_identity)
        if prior is value:
            continue
        if prior is not missing_identity:
            findings.append(
                "RT20-GRAPH-IDENTITY-CUSTODY-COLLISION: "
                f"path={path} id={identity}")
            break
        expanded[identity] = value
        if len(expanded) > max_nodes:
            findings.append(
                f"RT20-GRAPH-NODE-BUDGET: path={path} limit={max_nodes}")
            break
        try:
            label = forbidden.get(identity)
        except BaseException as exc:
            findings.append(_graph_error(path, "forbidden-identity-map", exc))
            break
        if label is not None:
            if type(label) is not str:
                findings.append(
                    "RT20-GRAPH-TRAVERSAL-ERROR: "
                    f"path={path} edge=forbidden-identity-map "
                    "exception=NonStringLabel")
            else:
                hits.append({"path": path, "forbiddenIdentity": label})
            continue
        runtime_kind, kind_findings = _runtime_kind(
            value, path, declared_object_types)
        findings.extend(kind_findings)
        if runtime_kind is None:
            continue
        if GRAPH_RUNTIME_DISPOSITIONS.get(runtime_kind) == "leaf":
            continue
        if depth >= max_depth:
            findings.append(
                f"RT20-GRAPH-DEPTH-BUDGET: path={path} limit={max_depth}")
            continue
        try:
            children, child_findings = _owned_graph_children(value, path)
        except BaseException as exc:
            findings.append(_graph_error(path, "edge-dispatch", exc))
            continue
        findings.extend(child_findings)
        for child_path, child in children:
            queue.append((child_path, child, depth + 1))
    return {"forbiddenHits": hits, "visited": len(expanded),
            "identityCustodyCount": len(expanded),
            "identityCustodyMode": "STRONG-REFERENCE-ID-TO-OBJECT",
            "findings": findings, "clean": not hits and not findings}


def _quarantine_edge_selftest(
        snapshot: VerifiedSemanticRTSnapshotV2 | None = None,
) -> tuple[int, int, list[str]]:
    """Active edge attacks plus one deletion mutation per declaration."""
    sentinel = object()
    buffer_sentinel = b"rt20-memoryview-backing-sentinel"

    class DictBox:
        pass

    class SlotBox:
        __slots__ = ("value",)

    class MangledSlotAttack:
        __slots__ = ("__hidden",)

        def __init__(self, value: Any) -> None:
            self.__hidden = value

    class PrivateSlotBase:
        __slots__ = ("__hidden",)

        def __init__(self, value: Any) -> None:
            self.__hidden = value

    class InheritedMangledSlotAttack(PrivateSlotBase):
        __slots__ = ()

    class MethodBox:
        def __init__(self, value: Any) -> None:
            self.value = value

        def expose(self) -> Any:
            return self.value

    class ClassDictionaryAttack:
        hidden = sentinel

    class BaseAttack:
        pass

    class DerivedAttack(BaseAttack):
        pass

    class ForbiddenMeta(type):
        pass

    class MetaclassAttack(metaclass=ForbiddenMeta):
        pass

    class UnknownOpaque:
        __slots__ = ()

    class RaisingMapping(MappingABC):
        def __getitem__(self, _key: Any) -> Any:
            raise KeyError

        def __iter__(self) -> Any:
            return iter(())

        def __len__(self) -> int:
            return 0

        def items(self) -> Any:
            raise RuntimeError("hostile mapping")

    class RaisingSequence(list):
        def __iter__(self) -> Any:
            raise RuntimeError("hostile iterator")

    class RaisingProperty:
        __slots__ = ("danger",)

    class AwaitBridge:
        def __await__(self) -> Any:
            yield sentinel

    def raise_property(_self: Any) -> Any:
        raise RuntimeError("hostile property")

    # Retain the declared slot name while replacing its descriptor with a
    # hostile property. object.__getattribute__ still invokes the descriptor;
    # the traversal must convert that failure into a named finding.
    RaisingProperty.danger = property(raise_property)  # type: ignore[assignment]

    dictionary_box = DictBox()
    dictionary_box.value = sentinel
    slot_box = SlotBox()
    slot_box.value = sentinel
    method_box = MethodBox(sentinel)
    builtin_owner: list[Any] = []
    builtin_bound = builtin_owner.append
    module = types.ModuleType("rt19_quarantine_sentinel")
    module.sentinel = sentinel

    def closure_factory(value: Any) -> Any:
        return lambda: value

    closure_function = closure_factory(sentinel)
    closure_cell = closure_function.__closure__[0]
    default_function = lambda value=sentinel: value
    kwdefault_function = lambda *, value=sentinel: value
    annotation_function = lambda value: value
    annotation_function.__annotations__ = {"value": sentinel}
    attribute_function = lambda: None
    attribute_function.hidden = sentinel  # type: ignore[attr-defined]
    namespace: dict[str, Any] = {"sentinel": sentinel}
    exec(compile("def probe():\n    return sentinel\n", "<probe>", "exec"),
         namespace)

    class WrappedDescriptors:
        @staticmethod
        def static_probe() -> None:
            return None

        @classmethod
        def class_probe(cls) -> type:
            return cls

        prop = property(lambda self: None)

    static_descriptor = vars(WrappedDescriptors)["static_probe"]
    static_function = static_descriptor.__func__
    property_descriptor = vars(WrappedDescriptors)["prop"]
    property_function = property_descriptor.fget
    selftest_admitted_types = (
        DictBox, SlotBox, MangledSlotAttack, PrivateSlotBase,
        InheritedMangledSlotAttack, MethodBox, ClassDictionaryAttack,
        BaseAttack, DerivedAttack, ForbiddenMeta, MetaclassAttack,
        RaisingProperty, WrappedDescriptors, AwaitBridge,
    )

    frame_globals_namespace: dict[str, Any] = {
        "inspect": inspect, "hidden": sentinel,
    }
    exec(compile(
        "def hold_frame():\n    yield inspect.currentframe()\n",
        "<rt20-frame-globals>", "exec"), frame_globals_namespace)
    frame_globals_holder = frame_globals_namespace["hold_frame"]()
    frame_globals_attack = next(frame_globals_holder)

    def hold_local_frame(value: Any) -> Any:
        hidden = value
        yield inspect.currentframe()

    frame_locals_holder = hold_local_frame(sentinel)
    frame_locals_attack = next(frame_locals_holder)

    def make_back_frame() -> tuple[types.FrameType, types.FrameType]:
        back_target = inspect.currentframe()

        def inner() -> types.FrameType:
            return inspect.currentframe()  # type: ignore[return-value]

        return inner(), back_target  # type: ignore[return-value]

    frame_back_attack, frame_back_target = make_back_frame()
    def empty_generator_factory() -> Any:
        if False:
            yield None

    generator_attack = empty_generator_factory()

    async def coroutine_factory() -> None:
        return None

    coroutine_attack = coroutine_factory()

    async def async_generator_factory() -> Any:
        if False:
            yield None

    async_generator_attack = async_generator_factory()

    def runtime_referent_generator_factory() -> Any:
        if False:
            yield None

    runtime_referent_generator = runtime_referent_generator_factory()
    slice_start_attack = slice(sentinel, None, None)
    slice_stop_attack = slice(None, sentinel, None)
    slice_step_attack = slice(None, None, sentinel)

    def code_constant_template() -> None:
        return None

    code_constant_attack = code_constant_template.__code__.replace(
        co_consts=(None, sentinel))
    function_code_attack = lambda: None
    function_builtins_attack = lambda: None
    function_doc_attack = lambda: None
    function_doc_attack.__doc__ = sentinel
    function_module_attack = lambda: None
    function_module_attack.__module__ = sentinel
    function_type_param_attack = lambda: None
    function_type_param_attack.__type_params__ = (sentinel,)
    function_annotate_attack = lambda: None
    function_annotate_child = lambda _format: {}
    function_annotate_attack.__annotate__ = function_annotate_child
    property_doc_attack = property(lambda _self: None, doc=sentinel)
    property_name_attack = property(lambda _self: None)
    property_name_marker = "rt20-property-name-" + str(id(property_name_attack))
    property_name_attack.__name__ = property_name_marker
    frame_trace_child = lambda *_args: None
    frame_locals_attack.f_trace = frame_trace_child

    def inner_yieldfrom() -> Any:
        yield sentinel

    def outer_yieldfrom() -> Any:
        yield from inner_yieldfrom()

    generator_yieldfrom_attack = outer_yieldfrom()
    next(generator_yieldfrom_attack)
    generator_yieldfrom_child = generator_yieldfrom_attack.gi_yieldfrom

    async def coroutine_wait_factory() -> None:
        await AwaitBridge()

    coroutine_wait_attack = coroutine_wait_factory()
    coroutine_wait_attack.send(None)
    coroutine_wait_child = coroutine_wait_attack.cr_await
    previous_origin_depth = sys.get_coroutine_origin_tracking_depth()
    sys.set_coroutine_origin_tracking_depth(1)
    try:
        coroutine_origin_attack = coroutine_factory()
    finally:
        sys.set_coroutine_origin_tracking_depth(previous_origin_depth)
    coroutine_origin_child = coroutine_origin_attack.cr_origin

    async def async_generator_wait_factory() -> Any:
        await AwaitBridge()
        yield sentinel

    async_generator_wait_attack = async_generator_wait_factory()
    async_generator_wait_driver = async_generator_wait_attack.__anext__()
    async_generator_wait_driver.send(None)
    async_generator_wait_child = async_generator_wait_attack.ag_await
    unknown_type_attack = UnknownOpaque()

    cases: list[tuple[str, Any, Any]] = [
        ("mapping-value", {"value": sentinel}, sentinel),
        ("mapping-key", {sentinel: "value"}, sentinel),
        ("mappingproxy", MappingProxyType({"value": sentinel}), sentinel),
        ("list", [sentinel], sentinel),
        ("tuple", (sentinel,), sentinel),
        ("deque", deque([sentinel]), sentinel),
        ("set", {sentinel}, sentinel),
        ("frozenset", frozenset({sentinel}), sentinel),
        ("memoryview-backing", memoryview(buffer_sentinel), buffer_sentinel),
        ("object-dict", dictionary_box, sentinel),
        ("object-slot", slot_box, sentinel),
        ("mangled-slot", MangledSlotAttack(sentinel), sentinel),
        ("inherited-mangled-slot",
         InheritedMangledSlotAttack(sentinel), sentinel),
        ("bound-method-owner", method_box.expose, method_box),
        ("bound-method-function", method_box.expose,
         MethodBox.expose),
        ("builtin-bound-owner", builtin_bound, builtin_owner),
        ("function-globals", namespace["probe"], sentinel),
        ("function-closure", closure_function, closure_cell),
        ("cell-contents", closure_cell, sentinel),
        ("function-default", default_function, sentinel),
        ("function-kwdefault", kwdefault_function, sentinel),
        ("function-annotation", annotation_function, sentinel),
        ("function-attribute", attribute_function, sentinel),
        ("module", module, sentinel),
        ("partial-function", functools.partial(attribute_function),
         attribute_function),
        ("partial-args", functools.partial(id, sentinel), sentinel),
        ("partial-keywords", functools.partial(dict, value=sentinel), sentinel),
        ("object-class", dictionary_box, DictBox),
        ("class-dictionary", ClassDictionaryAttack, sentinel),
        ("class-bases", DerivedAttack, BaseAttack),
        ("class-mro", DerivedAttack, BaseAttack),
        ("property-accessor", property_descriptor, property_function),
        ("wrapped-descriptor-function", static_descriptor, static_function),
        ("descriptor-owner", str.upper, str),
        ("class-metaclass", MetaclassAttack, ForbiddenMeta),
        ("frame-globals", frame_globals_attack, sentinel),
        ("frame-locals", frame_locals_attack, sentinel),
        ("frame-back", frame_back_attack, frame_back_target),
        ("generator-frame", generator_attack, generator_attack.gi_frame),
        ("coroutine-frame", coroutine_attack, coroutine_attack.cr_frame),
        ("async-generator-frame", async_generator_attack,
         async_generator_attack.ag_frame),
        ("runtime-referent-function", runtime_referent_generator,
         runtime_referent_generator_factory),
        ("slice-start", slice_start_attack, sentinel),
        ("slice-stop", slice_stop_attack, sentinel),
        ("slice-step", slice_step_attack, sentinel),
        ("code-constant", code_constant_attack, sentinel),
        ("function-code", function_code_attack, function_code_attack.__code__),
        ("function-builtins", function_builtins_attack,
         function_builtins_attack.__builtins__),
        ("function-doc", function_doc_attack, sentinel),
        ("function-module", function_module_attack, sentinel),
        ("function-type-param", function_type_param_attack, sentinel),
        ("function-annotate", function_annotate_attack,
         function_annotate_child),
        ("property-doc", property_doc_attack, sentinel),
        ("property-name", property_name_attack, property_name_marker),
        ("frame-builtins", frame_locals_attack, frame_locals_attack.f_builtins),
        ("frame-code", frame_locals_attack, frame_locals_attack.f_code),
        ("frame-trace", frame_locals_attack, frame_trace_child),
        ("frame-generator", frame_locals_attack,
         frame_locals_attack.f_generator),
        ("generator-code", generator_attack, generator_attack.gi_code),
        ("generator-yieldfrom", generator_yieldfrom_attack,
         generator_yieldfrom_child),
        ("coroutine-code", coroutine_attack, coroutine_attack.cr_code),
        ("coroutine-await", coroutine_wait_attack, coroutine_wait_child),
        ("coroutine-origin", coroutine_origin_attack, coroutine_origin_child),
        ("async-generator-code", async_generator_attack,
         async_generator_attack.ag_code),
        ("async-generator-await", async_generator_wait_attack,
         async_generator_wait_child),
    ]
    results: list[tuple[str, bool]] = []

    def record(name: str, passed: bool) -> None:
        results.append((name, passed))

    positive_denominator_findings = _positive_case_denominator_findings(
        [name for name, _root, _forbidden in cases])
    record("positive-case-denominator-exact",
           not positive_denominator_findings)

    operation = None if snapshot is None else snapshot.operations.get(
        "derive_operational_custody_projection_v1")
    attack_attribute = "__rt20_actual_root_attack__"

    def actual_root_scan(
            attack: Any, forbidden_map: Mapping[int, str],
            admitted_runtime_types: tuple[type, ...] = (),
    ) -> dict[str, Any]:
        if snapshot is None or not isinstance(operation, types.FunctionType) or \
                attack_attribute in operation.__dict__:
            return {"forbiddenHits": [], "visited": 0,
                    "findings": ["RT20-GRAPH-ACTUAL-ROOT-INJECTION-FAILED"],
                    "clean": False}
        operation.__dict__[attack_attribute] = attack
        try:
            return _forbidden_identity_paths(
                snapshot, forbidden_map,
                admitted_runtime_types=admitted_runtime_types)
        finally:
            operation.__dict__.pop(attack_attribute, None)

    for name, root, forbidden_value in cases:
        forbidden_map = {id(forbidden_value): "sentinel"}
        admitted_types = selftest_admitted_types + (type(root),)
        direct_scan = _forbidden_identity_paths(
            root, forbidden_map, admitted_runtime_types=admitted_types)
        rooted_scan = actual_root_scan(
            root, forbidden_map, admitted_types)
        record(name, bool(direct_scan["forbiddenHits"]) and
               not direct_scan["findings"] and
               bool(rooted_scan["forbiddenHits"]) and
               not rooted_scan["findings"] and
               attack_attribute not in operation.__dict__)

    unknown_direct = _forbidden_identity_paths(unknown_type_attack, {})
    unknown_rooted = actual_root_scan(unknown_type_attack, {})
    record("unknown-type", any(
        row.startswith("RT20-GRAPH-UNKNOWN-RUNTIME-TYPE:")
        for row in unknown_direct["findings"]) and any(
        row.startswith("RT20-GRAPH-UNKNOWN-RUNTIME-TYPE:")
        for row in unknown_rooted["findings"]) and
        not unknown_direct["clean"] and not unknown_rooted["clean"])
    generator_attack.close()
    runtime_referent_generator.close()
    generator_yieldfrom_attack.close()
    frame_globals_holder.close()
    frame_locals_holder.close()
    coroutine_attack.close()
    coroutine_wait_attack.close()
    coroutine_origin_attack.close()
    async_generator_wait_driver.close()
    for async_generator in (
            async_generator_attack, async_generator_wait_attack):
        try:
            async_close = async_generator.aclose()
            async_close.send(None)
        except StopIteration:
            pass

    helper_reuse_hits = 0
    rooted_reuse_hits = 0
    for iteration in range(20):
        class HiddenClass:
            hidden = sentinel

        class RootClass:
            nested = HiddenClass

        identity_map = {id(sentinel): f"id-reuse-sentinel-{iteration}"}
        helper_scan = _forbidden_identity_paths(RootClass, identity_map)
        rooted_scan = actual_root_scan(RootClass, identity_map)
        if helper_scan["forbiddenHits"] and not helper_scan["findings"] and \
                helper_scan.get("identityCustodyMode") == \
                "STRONG-REFERENCE-ID-TO-OBJECT" and \
                helper_scan.get("identityCustodyCount") == \
                helper_scan.get("visited"):
            helper_reuse_hits += 1
        if rooted_scan["forbiddenHits"] and not rooted_scan["findings"] and \
                rooted_scan.get("identityCustodyMode") == \
                "STRONG-REFERENCE-ID-TO-OBJECT" and \
                rooted_scan.get("identityCustodyCount") == \
                rooted_scan.get("visited"):
            rooted_reuse_hits += 1
    record("identity-reuse-helper-20-of-20", helper_reuse_hits == 20)
    record("identity-reuse-actual-root-20-of-20", rooted_reuse_hits == 20)

    raising_mapping_scan = _forbidden_identity_paths(RaisingMapping(), {})
    record("raising-custom-mapping-controlled", any(
        row.startswith("RT20-GRAPH-TRAVERSAL-ERROR:") and
        "edge=mapping-keys-values" in row and "exception=RuntimeError" in row
        for row in raising_mapping_scan["findings"]))
    raising_iterator_scan = _forbidden_identity_paths(RaisingSequence(), {})
    record("raising-iterator-controlled", any(
        row.startswith("RT20-GRAPH-TRAVERSAL-ERROR:") and
        "edge=sequence-items" in row and "exception=RuntimeError" in row
        for row in raising_iterator_scan["findings"]))
    raising_property_scan = _forbidden_identity_paths(
        RaisingProperty(), {}, admitted_runtime_types=selftest_admitted_types)
    record("raising-property-controlled", any(
        row.startswith("RT20-GRAPH-TRAVERSAL-ERROR:") and
        "edge=object-slots-mro-mangled" in row and
        "exception=RuntimeError" in row
        for row in raising_property_scan["findings"]))

    cycle: list[Any] = []
    cycle.append(cycle)
    cycle.append(sentinel)
    cycle_scan = _forbidden_identity_paths(
        cycle, {id(sentinel): "cycle-sentinel"})
    record("cycle-safe", len(cycle_scan["forbiddenHits"]) == 1 and
           not cycle_scan["findings"] and cycle_scan["visited"] == 2)
    node_scan = _forbidden_identity_paths([object()], {}, max_nodes=1)
    record("node-budget-controlled", any(
        row.startswith("RT20-GRAPH-NODE-BUDGET:")
        for row in node_scan["findings"]))
    depth_scan = _forbidden_identity_paths([[sentinel]], {}, max_depth=1)
    record("depth-budget-controlled", any(
        row.startswith("RT20-GRAPH-DEPTH-BUDGET:")
        for row in depth_scan["findings"]))

    complete_attacks = {
        "classDictionary": ClassDictionaryAttack,
        "mangledSlot": MangledSlotAttack(sentinel),
        "inheritedMangledSlot": InheritedMangledSlotAttack(sentinel),
        "memoryview": memoryview(buffer_sentinel),
        "raisingMapping": RaisingMapping(),
        "raisingIterator": RaisingSequence(),
        "raisingProperty": RaisingProperty(),
        "cycle": cycle,
    }
    complete_scan = actual_root_scan(
        complete_attacks,
        {id(sentinel): "object-sentinel",
         id(buffer_sentinel): "buffer-sentinel"},
        selftest_admitted_types)
    complete_labels = {
        row["forbiddenIdentity"] for row in complete_scan["forbiddenHits"]}
    complete_errors = complete_scan["findings"]
    record("actual-returned-snapshot-active-attacks",
           complete_labels == {"object-sentinel", "buffer-sentinel"} and
           any("edge=mapping-keys-values" in row for row in complete_errors) and
           any("edge=sequence-items" in row for row in complete_errors) and
           any("edge=object-slots-mro-mangled" in row
               for row in complete_errors))

    for index, row in enumerate(GRAPH_EDGE_REGISTRY):
        mutated = list(GRAPH_EDGE_REGISTRY)
        mutated.pop(index)
        scan = _forbidden_identity_paths({}, {}, registry=mutated)
        wanted = f"RT20-GRAPH-REGISTRY-MISSING: edge={row['id']}"
        record(f"registry-delete-{row['id']}",
               scan["visited"] == 0 and wanted in scan["findings"])
    for index, row in enumerate(GRAPH_RUNTIME_KIND_REGISTRY):
        mutated_runtime = list(GRAPH_RUNTIME_KIND_REGISTRY)
        mutated_runtime.pop(index)
        scan = _forbidden_identity_paths(
            {}, {}, runtime_registry=mutated_runtime)
        wanted = (
            "RT20-GRAPH-RUNTIME-REGISTRY-MISSING: "
            f"kind={row['id']}")
        record(f"runtime-registry-delete-{row['id']}",
               scan["visited"] == 0 and wanted in scan["findings"])
    for index, row in enumerate(GRAPH_SEMANTIC_CHILD_DENOMINATOR):
        mutated_denominator = list(GRAPH_SEMANTIC_CHILD_DENOMINATOR)
        mutated_denominator.pop(index)
        scan = _forbidden_identity_paths(
            {}, {}, child_denominator=mutated_denominator)
        wanted = (
            "RT20-GRAPH-CHILD-DENOMINATOR-MISSING: "
            f"kind={row['id']}")
        record(f"child-denominator-delete-{row['id']}",
               scan["visited"] == 0 and wanted in scan["findings"])
    for index, row in enumerate(GRAPH_REFERENT_ORACLE_EXCEPTIONS):
        mutated_exceptions = list(GRAPH_REFERENT_ORACLE_EXCEPTIONS)
        mutated_exceptions.pop(index)
        scan = _forbidden_identity_paths(
            {}, {}, oracle_exceptions=mutated_exceptions)
        record(f"oracle-exception-delete-{row['runtimeKind']}",
               scan["visited"] == 0 and any(
                   finding.startswith("RT20-GRAPH-ORACLE-EXCEPTION-")
                   for finding in scan["findings"]))
    for index, case_id in enumerate(GRAPH_POSITIVE_CASE_IDS):
        mutated_cases = list(GRAPH_POSITIVE_CASE_IDS)
        mutated_cases.pop(index)
        findings = _positive_case_denominator_findings(mutated_cases)
        wanted = (
            "RT20-GRAPH-POSITIVE-DENOMINATOR-MISSING: "
            f"case={case_id}")
        record(f"positive-denominator-delete-{case_id}", wanted in findings)
    unknown_registry = list(GRAPH_EDGE_REGISTRY) + [
        {"id": "hostile-unknown-edge", "from": "unknown", "to": "unknown"}]
    unknown_scan = _forbidden_identity_paths({}, {}, registry=unknown_registry)
    record("registry-unknown-controlled", any(
        row == "RT20-GRAPH-UNKNOWN-EDGE-TYPE: edge=hostile-unknown-edge"
        for row in unknown_scan["findings"]))
    duplicate_scan = _forbidden_identity_paths(
        {}, {}, registry=list(GRAPH_EDGE_REGISTRY) + [GRAPH_EDGE_REGISTRY[0]])
    record("registry-duplicate-controlled", any(
        row.startswith("RT20-GRAPH-REGISTRY-DUPLICATE:")
        for row in duplicate_scan["findings"]))
    reordered = list(GRAPH_EDGE_REGISTRY)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    order_scan = _forbidden_identity_paths({}, {}, registry=reordered)
    record("registry-order-controlled", any(
        row.startswith("RT20-GRAPH-REGISTRY-ORDER:")
        for row in order_scan["findings"]))
    all_finding_text = (raising_mapping_scan["findings"] +
                        raising_iterator_scan["findings"] +
                        raising_property_scan["findings"] + complete_errors +
                        unknown_scan["findings"] + duplicate_scan["findings"] +
                        order_scan["findings"])
    record("named-findings-no-traceback",
           bool(all_finding_text) and
           all(type(row) is str and "Traceback" not in row
               for row in all_finding_text))

    failures = [name for name, passed in results if not passed]
    return len(results) - len(failures), len(results), failures


def _snapshot_quarantine_findings(
        snapshot: VerifiedSemanticRTSnapshotV2, authority: FrozenAuthority,
) -> list[str]:
    findings: list[str] = []
    try:
        _authenticate_inert_snapshot(snapshot)
    except AuthorityError as exc:
        return [str(exc)]
    receipt = snapshot["ep8DerivationReceipt"]
    if tuple(receipt) != (
            "schemaVersion", "kind", "projectId", "acceptedVectorId",
            "sourceArtifactSha256", "sourceCheckerSha256",
            "requiredCheckerApi", "exactCallCounts",
            "fixtureProjectionCommitment", "results", "resultsCommitment",
            "receiptCommitment"):
        findings.append("RT21-EP8-RECEIPT: closed ordered fields drifted")
    if list(receipt.get("requiredCheckerApi", ())) != \
            list(EXPECTED_EP8_REQUIRED_API):
        findings.append("RT21-EP8-RECEIPT: exact nine-name authority drifted")
    expected_counts = {name: (2 if name == "encode_semantic_object_binding" else 1)
                       for name in EXPECTED_EP8_REQUIRED_API}
    if dict(receipt.get("exactCallCounts", {})) != expected_counts:
        findings.append("RT21-EP8-RECEIPT: exact invocation counts drifted")
    try:
        goldens = snapshot["candidate"]["verifiedSemanticRtApiContract"][
            "authenticatedLoaderBindingV7"]["ep8Closure"]["resultGoldens"]
        if receipt["resultsCommitment"] != goldens["resultsCommitment"] or \
                receipt["receiptCommitment"] != goldens["receiptCommitment"] or \
                snapshot["fixtureProjection"]["projectionCommitment"] != \
                goldens["fixtureProjectionCommitment"] or \
                receipt["fixtureProjectionCommitment"] != \
                snapshot["fixtureProjection"]["projectionCommitment"]:
            findings.append("RT21-EP8-RECEIPT: executable commitment join drifted")
    except (KeyError, TypeError):
        findings.append("RT21-EP8-RECEIPT: executable commitment join absent")
    if snapshot["hostOperationIds"] != INERT_HOST_OPERATION_IDS or \
            tuple(HOST_OPERATION_REGISTRY) != INERT_HOST_OPERATION_IDS:
        findings.append("RT21-SNAPSHOT-SURFACE: host operation ids drifted")
    forbidden_identities = {
        id(authority), id(authority.buffers), id(authority.parsed),
        id(authority.modules),
        *(id(value) for value in authority.buffers.values()),
        *(id(value) for value in authority.parsed.values()),
        *(id(value) for value in authority.modules.values()),
        *(id(value) for value in HOST_OPERATION_REGISTRY.values()),
    }
    queue = [("$", snapshot)]
    seen: set[int] = set()
    while queue:
        path, value = queue.pop()
        identity = id(value)
        if identity in seen:
            continue
        seen.add(identity)
        if identity in forbidden_identities:
            findings.append(
                f"RT21-INERT-FORBIDDEN-IDENTITY:{path}:{type(value).__name__}")
            continue
        if type(value) is MappingProxyType:
            for index, (key, item) in enumerate(value.items()):
                queue.append((f"{path}.key[{index}]", key))
                queue.append((f"{path}.{key}", item))
        elif type(value) is tuple:
            queue.extend((f"{path}[{index}]", item)
                         for index, item in enumerate(value))
        elif value is not None and type(value) not in (bool, int, str, bytes):
            findings.append(
                f"RT21-INERT-UNDECLARED-VALUE-KIND:{path}:"
                f"{type(value).__name__}")
    return findings


def check_contract(candidate: Any, authority: FrozenAuthority,
                   candidate_source: bytes | None = None) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["RT16-TOTALITY-ROOT: candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = expected_candidate(authority)
        difference = exact_recursive_equal(candidate, expected)
        if difference:
            findings.append(f"RT16-EXACT-CANDIDATE: {difference}")
        if candidate_source is not None and candidate_source != pretty(candidate):
            findings.append("RT16-CANONICAL-RAW: candidate is not exact canonical pretty JSON")
        findings.extend(_semantic_findings(candidate, expected, authority))
        if not findings:
            snapshot = VerifiedSemanticRTSnapshotV2(candidate, authority)
            findings.extend(_snapshot_quarantine_findings(snapshot, authority))
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError, AuthorityError, DuplicateKeyError, FloatForbidden,
            ResolutionError) as exc:
        findings.append(f"RT16-TOTALITY-EXCEPTION: controlled {type(exc).__name__}")
    return findings


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _candidate_mutations() -> list[Mutation]:
    def fixture(root: dict[str, Any], index: int = 0) -> dict[str, Any]:
        return root["verifiedSemanticRtApiContract"][
            "rawObjectResolutionConformance"]["fixtureGoldens"][index]

    return [
        ("version", lambda root: root.__setitem__("version", 14)),
        ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
        ("supersedes", lambda root: root.__setitem__("supersedesAsArchitectureCandidate", RT13)),
        ("dependency hash", lambda root: root["dependencies"]["semanticSources"][0].__setitem__("sha256", "0" * 64)),
        ("dependency injection", lambda root: root["dependencies"]["semanticSources"].append({"role": "store", "artifact": "store.json", "sha256": "0" * 64})),
        ("basis source", lambda root: root["semanticBasisProjection"].__setitem__("sourceRetentionArtifact", RT14)),
        ("grammar id", lambda root: root["semanticBasisProjection"]["semanticClosureGrammar"].__setitem__("id", "drift")),
        ("closure cas", lambda root: root["semanticBasisProjection"].__setitem__("semanticCapabilityClosureCasRef", "sha256:" + "0" * 64)),
        ("basis proof ref", lambda root: root["semanticBasisProjection"]["semanticCapabilityClosure"]["proofRefs"][0].__setitem__("recordCasRef", "sha256:" + "0" * 64)),
        ("basis commitment", lambda root: root["semanticBasisProjection"].__setitem__("semanticCapabilityClosureCommitment", "sha256:" + "0" * 64)),
        ("availability", lambda root: root["semanticBasisProjection"]["unitAvailabilityRecords"].pop()),
        ("projection type", lambda root: root["operationalCustodyProjectionContract"].__setitem__("type", "OperationalCustodyProjectionV2")),
        ("projection tag", lambda root: root["operationalCustodyProjectionContract"]["sortingGrammar"].__setitem__("encodedRawKey", "wrong")),
        ("projection fixed count", lambda root: root["operationalCustodyProjectionContract"]["cardinality"].__setitem__("algorithm", "exactly 23")),
        ("lease state version", lambda root: root["semanticLeaseProtocolV3"]["state"].__setitem__("schemaVersion", 2)),
        ("lease event fields", lambda root: root["semanticLeaseProtocolV3"]["events"][2]["orderedFields"].pop()),
        ("lease result variant", lambda root: root["semanticLeaseProtocolV3"]["output"]["resultVariantOrderedFields"]["LEASE_RECLAIMED"].pop()),
        ("lease reducer", lambda root: root["semanticLeaseProtocolV3"]["reducers"].__setitem__("reduce_crash_reclaim_v3", "skip fence")),
        ("lease golden state", lambda root: root["semanticLeaseProtocolV3"]["goldenScenarios"][0]["preState"].__setitem__("ledgerSequence", 9)),
        ("lease golden successor", lambda root: root["semanticLeaseProtocolV3"]["goldenScenarios"][6]["event"].__setitem__("successorFencingToken", 7)),
        ("storage", lambda root: root["storageAndLineage"].__setitem__("purgeAuthority", "caller")),
        ("custody", lambda root: root["custodyPolicy"].__setitem__("durableDefault", "selected")),
        ("authority", lambda root: root["authority"].__setitem__("authorityClaim", "APPLIED")),
        ("integration", lambda root: root["integrationState"].__setitem__("CD-RT-5", "PASS")),
        ("ownership backedge", lambda root: root["semanticOwnershipBoundary"]["semanticDependencies"].append("downstream store")),
        ("invariant", lambda root: root["invariants"].pop()),
        ("assurance", lambda root: root["assurance"].__setitem__("evidenceGrade", "PRODUCTION")),
        ("residual", lambda root: root["retainedResiduals"].pop()),
        ("seal", lambda root: root.__setitem__("sealRecommendation", "SEAL")),
        ("physical identity", lambda root: root["rawPhysicalIdentityContract"].__setitem__("rawCasPattern", ".*")),
        ("api constructor", lambda root: root["verifiedSemanticRtApiContract"]["constructor"].__setitem__("signature", "wrong")),
        ("returned snapshot type", lambda root: root["verifiedSemanticRtApiContract"]["returnedSnapshot"].__setitem__("type", "VerifiedSemanticRTSnapshotV1")),
        ("returned EP8 callable", lambda root: root["verifiedSemanticRtApiContract"]["returnedSnapshot"]["retainsExactly"].append("live EP8 check callable")),
        ("inert edge omission", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["semanticEdgeRegistry"].pop()),
        ("inert value kind omission", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["valueRegistry"].pop()),
        ("snapshot field omission", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["snapshotOrderedFields"].pop()),
        ("host operation id omission", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["hostOperationIds"].pop()),
        ("independent challenge count", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["independentChallengeBinding"].__setitem__("runtimeKindsChallenged", 24)),
        ("inert commitment domain", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["inertBoundary"]["canonicalCommitment"].__setitem__("domain", "wrong")),
        ("EP8 required API omission", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["ep8Closure"]["requiredCheckerApi"].pop()),
        ("EP8 forbidden API extra", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["ep8Closure"]["requiredCheckerApi"].append("check")),
        ("EP8 call count", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["ep8Closure"]["exactCallCounts"].__setitem__("validate_bundle", 0)),
        ("EP8 receipt commitment", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["ep8Closure"]["resultGoldens"].__setitem__("receiptCommitment", "sha256:" + "0" * 64)),
        ("fixture projection commitment", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["ep8Closure"]["resultGoldens"].__setitem__("fixtureProjectionCommitment", "sha256:" + "0" * 64)),
        ("v1.10 real dataclass", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["temporaryVerifiedModuleExecutions"][0].__setitem__("isDataclass", False)),
        ("v1.10 temporary cleanup", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["temporaryVerifiedModuleExecutions"][0].__setitem__("restoredToAbsent", False)),
        ("v1.10 decorator interposition", lambda root: root["verifiedSemanticRtApiContract"]["authenticatedLoaderBindingV7"]["d9Interpositions"].append({"source": "check-d9-v1.10.py", "kind": "dataclass-decorator"})),
        ("d9 checker hash", lambda root: root["verifiedSemanticRtApiContract"]["verifiedD9Compatibility"]["exactSubjects"].__setitem__("checkerSha256", "0" * 64)),
        ("request order", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["requestOrderedFields"].reverse()),
        ("validation order", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["validationOrder"].reverse()),
        ("type registry", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["closedTypeRegistry"].pop()),
        ("primary raw bytes", lambda root: fixture(root)["resolutionRows"][0].__setitem__("rawBytesHex", fixture(root)["resolutionRows"][0]["rawBytesHex"][:-2] + "00")),
        ("primary usable result", lambda root: fixture(root)["resolutionRows"][0]["expectedResult"].__setitem__("kind", "IDENTITY_ONLY")),
        ("primary projection", lambda root: fixture(root).__setitem__("operationalProjectionRef", "sha256:" + "0" * 64)),
        ("alternate count", lambda root: fixture(root, 1).__setitem__("recordCount", 7)),
        ("snapshot byte omission", lambda root: fixture(root)["rawObjectSnapshot"]["records"].pop()),
    ]


def _raw_adversarial(fixtures: list[dict[str, Any]]) -> tuple[int, int, int]:
    passed = 0
    total = 0
    escapes = 0
    for fixture_index, fixture in enumerate(fixtures):
        for row_index, row in enumerate(fixture["resolutionRows"]):
            raw = bytes.fromhex(row["rawBytesHex"])
            request = row["request"]
            attacks: list[tuple[str, Any, dict[str, Any], str]] = []
            attacks.append(("missing", None, copy.deepcopy(request), "BYTES_NOT_PRESENT"))
            attacks.append(("empty", b"", copy.deepcopy(request), "BYTES_NOT_PRESENT"))
            attacks.append(("byte-flip", raw[:-1] + bytes([raw[-1] ^ 1]), copy.deepcopy(request), "CAS_MISMATCH"))
            changed = copy.deepcopy(request); changed["recordCasRef"] = "sha256:" + "0" * 64
            attacks.append(("wrong-cas", raw, changed, "CAS_MISMATCH"))
            changed = copy.deepcopy(request); changed["expectedValueType"] = "WrongTypeV1"
            attacks.append(("wrong-type", raw, changed, "EXPECTED_TYPE_MISMATCH"))
            changed = copy.deepcopy(request); changed["selector"] = "/wrong"
            attacks.append(("wrong-selector", raw, changed, "SELECTOR_MISMATCH"))
            changed = copy.deepcopy(request); changed["projectId"] = PROJECT_B if request["projectId"] != PROJECT_B else PROJECT_A
            attacks.append(("wrong-project", raw, changed, "PROJECT_MISMATCH"))
            other_kind = next(kind for kind in RECORD_TYPES if kind != request["recordKind"])
            changed = copy.deepcopy(request); changed["recordKind"] = other_kind
            attacks.append(("wrong-kind", raw, changed, "CLOSED_TYPE_MISMATCH"))
            changed = copy.deepcopy(request); changed["requiredCapability"] = \
                "replayable" if request["requiredCapability"] == "verifiable" else "verifiable"
            attacks.append(("wrong-capability", raw, changed, "CAPABILITY_MISMATCH"))
            float_raw = raw.replace(b'"schemaVersion":1', b'"schemaVersion":1.0', 1)
            changed = copy.deepcopy(request); changed["recordCasRef"] = cas(float_raw)
            attacks.append(("float", float_raw, changed, "CLOSED_TYPE_MISMATCH"))
            duplicate_raw = raw.replace(b'{"schemaVersion":1', b'{"schemaVersion":1,"schemaVersion":1', 1)
            changed = copy.deepcopy(request); changed["recordCasRef"] = cas(duplicate_raw)
            attacks.append(("duplicate-key", duplicate_raw, changed, "CLOSED_TYPE_MISMATCH"))
            for attack_name, attack_raw, attack_request, expected_code in attacks:
                total += 1
                try:
                    validate_raw_object_resolution(attack_raw, attack_request)
                    escapes += 1
                except ResolutionError as exc:
                    if exc.code == expected_code:
                        passed += 1
                    else:
                        escapes += 1
                except Exception:
                    escapes += 1
    return passed, total, escapes


def _lease_adversarial(goldens: list[dict[str, Any]]) -> tuple[int, int, int]:
    passed = 0
    total = 0
    escapes = 0
    for row in goldens:
        attacks: list[dict[str, Any]] = []
        changed = copy.deepcopy(row["event"]); changed["atSequence"] += 1; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); changed["transactionBoundary"] = "WRONG"; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); changed["projectId"] = PROJECT_B; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); first = next(iter(changed)); value = changed.pop(first); changed[first] = value; attacks.append(changed)
        for event in attacks:
            total += 1
            try:
                reduce_semantic_lease_v3(row["preState"], event)
                escapes += 1
            except (TypeError, ValueError, ResolutionError):
                passed += 1
            except Exception:
                escapes += 1
    return passed, total, escapes


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0), ("float", 1.5),
    ("string", "hostile"), ("array", []), ("empty-object", {}),
    ("array-object", [{}]),
]


def _inert_boundary_selftest(
        snapshot: MappingProxyType | None,
) -> tuple[int, int, list[str]]:
    results: list[tuple[str, bool]] = []

    def record(name: str, passed: bool) -> None:
        results.append((name, passed))

    if snapshot is None:
        return 0, 1, ["snapshot-construction"]
    try:
        scan = _authenticate_inert_snapshot(snapshot)
        record("base-inert-snapshot", scan["visited"] > 1_000)
    except AuthorityError:
        record("base-inert-snapshot", False)

    probe = MappingProxyType({"probe": (None, False, 1, "x", b"y")})
    for index, row in enumerate(INERT_VALUE_REGISTRY):
        changed = list(INERT_VALUE_REGISTRY)
        changed.pop(index)
        try:
            _validate_inert_value(probe, value_registry=changed)
            rejected = False
        except AuthorityError as exc:
            rejected = str(exc) == \
                "RT21-INERT-VALUE-REGISTRY-DRIFT-BEFORE-ROOT"
        record(f"value-registry-delete-{row['id']}", rejected)
    for index, row in enumerate(INERT_EDGE_REGISTRY):
        changed = list(INERT_EDGE_REGISTRY)
        changed.pop(index)
        try:
            _validate_inert_value(probe, edge_registry=changed)
            rejected = False
        except AuthorityError as exc:
            rejected = str(exc) == \
                "RT21-INERT-EDGE-REGISTRY-DRIFT-BEFORE-ROOT"
        record(f"edge-registry-delete-{row['id']}", rejected)

    class Owner:
        def method(self) -> None:
            return None

    class Box:
        pass

    owner = Owner()
    closure_cell = (lambda value: lambda: value)(None).__closure__[0]
    generator = (item for item in (None,))

    class Pause:
        def __await__(self) -> Any:
            yield None

    async def coroutine_source() -> None:
        await Pause()

    coroutine = coroutine_source()

    async def async_generator_source() -> Any:
        yield None

    async_generator = async_generator_source()
    async_driver = async_generator.__anext__()
    traceback_value: Any = None
    try:
        raise ValueError("rt21")
    except ValueError as exc:
        traceback_value = exc.__traceback__
    weak_target = Box()
    import weakref
    kind_rows: list[tuple[str, Any, bool]] = [
        ("constrained-terminal", None, True),
        ("opaque-terminal", typing.NoDefault, False),
        ("mapping", {"key": "value"}, True),
        ("sequence", ["value"], True),
        ("set", {"value"}, False),
        ("memoryview", memoryview(b"x"), False),
        ("slice", slice(1), False),
        ("regular-expression-pattern", re.compile("x"), False),
        ("bound-python-method", owner.method, False),
        ("bound-builtin", [].append, False),
        ("partial", functools.partial(len, []), False),
        ("python-function", _inert_boundary_selftest, False),
        ("module", sys, False),
        ("closure-cell", closure_cell, False),
        ("property", property(lambda self: None), False),
        ("wrapped-descriptor", classmethod(lambda cls: None), False),
        ("builtin-descriptor", str.upper, False),
        ("class", Box, False),
        ("declared-object", Box(), False),
        ("frame", sys._getframe(), False),
        ("generator", generator, False),
        ("coroutine", coroutine, False),
        ("async-generator", async_generator, False),
        ("traceback", traceback_value, False),
        ("exception", ValueError("rt21"), False),
        ("weak-reference", weakref.ref(weak_target), False),
        ("generic-alias", list[int], False),
        ("union", int | str, False),
        ("super", super(Owner, owner), False),
        ("code", _inert_boundary_selftest.__code__, False),
        ("exact-runtime-view", {}.keys(), False),
        ("exact-runtime-iterator", iter([]), False),
        ("async-generator-driver", async_driver, False),
        ("unknown-runtime-kind", object(), False),
    ]
    try:
        for name, value, expected_admitted in kind_rows:
            try:
                frozen = _freeze_inert(value)
                _validate_inert_value(frozen)
                admitted = True
            except AuthorityError:
                admitted = False
            record(f"independent-kind-{name}", admitted is expected_admitted)
    finally:
        generator.close()
        coroutine.close()
        try:
            async_driver.close()
        except (AttributeError, RuntimeError):
            pass

    additional_attacks = [
        1.5, 1j, bytearray(b"x"), range(1), Ellipsis, NotImplemented,
        lambda: None, _inert_boundary_selftest.__code__, sys._getframe(),
    ]
    for index, attack in enumerate(additional_attacks):
        try:
            _freeze_inert({"attack": attack})
            rejected = False
        except AuthorityError:
            rejected = True
        record(f"non-grammar-exact-type-{index}", rejected)
    try:
        _encode_inert("\ud800")
        invalid_utf8_rejected = False
    except AuthorityError as exc:
        invalid_utf8_rejected = str(exc) == "RT21-INERT-UTF8-STRING"
    record("invalid-utf8-string", invalid_utf8_rejected)

    owner_map: dict[str, Any] = {}
    cycle = MappingProxyType(owner_map)
    owner_map["cycle"] = cycle
    try:
        _validate_inert_value(cycle)
        cycle_rejected = False
    except AuthorityError as exc:
        cycle_rejected = str(exc).startswith("RT21-INERT-CYCLE:")
    record("inert-cycle", cycle_rejected)

    spoof_data = _thaw_inert(snapshot)
    spoof_data["ep8DerivationReceipt"]["receiptCommitment"] = \
        "sha256:" + "0" * 64
    spoof = _freeze_inert(spoof_data)
    try:
        _authenticate_inert_snapshot(spoof)
        commitment_rejected = False
    except AuthorityError as exc:
        commitment_rejected = str(exc) == \
            "RT21-INERT-SNAPSHOT-COMMITMENT"
    record("snapshot-commitment-mutation", commitment_rejected)

    candidate = _thaw_inert(snapshot["candidate"])
    signatures = tuple(candidate["verifiedSemanticRtApiContract"]
                       ["pureCallSignatures"])
    record("seven-pure-signatures", len(signatures) == 7 and
           tuple(HOST_OPERATION_REGISTRY) == INERT_HOST_OPERATION_IDS and
           all("VerifiedSemanticRTSnapshotV2" in row for row in signatures))
    fixtures = candidate["verifiedSemanticRtApiContract"][
        "rawObjectResolutionConformance"]["fixtureGoldens"]
    projection_ok = raw_ok = True
    raw_count = 0
    for fixture in fixtures:
        try:
            projection, ref, digest = derive_operational_custody_projection_v1(
                snapshot, fixture, fixture["semanticClosure"])
            projection_ok = projection_ok and (
                projection == fixture["operationalProjection"] and
                ref == fixture["operationalProjectionRef"] and
                digest == fixture["operationalProjectionDigest"])
            for row in fixture["resolutionRows"]:
                actual = validate_raw_object_resolution_v1(
                    snapshot, bytes.fromhex(row["rawBytesHex"]), row["request"])
                raw_ok = raw_ok and actual == row["expectedResult"]
                raw_count += 1
        except (AuthorityError, KeyError, ResolutionError, TypeError, ValueError):
            projection_ok = raw_ok = False
    record("host-projection-goldens-2", projection_ok and len(fixtures) == 2)
    record("host-raw-resolution-goldens-12", raw_ok and raw_count == 12)

    reducer_names = {
        "expiry": "reduce_expiry_v1",
        "release": "reduce_release_v1",
        "crash-reclaim": "reduce_crash_reclaim_v3",
        "resolve-and-pin": "reduce_resolve_and_pin_v2",
    }
    lease_ok = predicate_ok = True
    lease_count = 0
    for row in candidate["semanticLeaseProtocolV3"]["goldenScenarios"]:
        try:
            output = HOST_OPERATION_REGISTRY[
                reducer_names[row["event"]["kind"]]](
                    snapshot, row["preState"], row["event"])
            lease_ok = lease_ok and output == row["expectedOutput"]
            expected_local = output["result"]["kind"] == \
                "RETENTION_LOCAL_UNAVAILABLE"
            predicate_ok = predicate_ok and \
                host_is_retention_local_unavailable_v1(
                    snapshot, output) is expected_local
            lease_count += 1
        except (AuthorityError, KeyError, TypeError, ValueError):
            lease_ok = predicate_ok = False
    record("host-lease-goldens-9", lease_ok and lease_count == 9)
    record("host-local-unavailable-predicate-9",
           predicate_ok and lease_count == 9)

    failures = [name for name, passed in results if not passed]
    return len(results) - len(failures), len(results), failures


def _trust_falsifiers(
        authority: FrozenAuthority,
) -> tuple[int, int, list[str], int, int, list[str]]:
    results: list[tuple[str, bool]] = []

    def record(name: str, rejected: bool) -> None:
        results.append((name, rejected))

    d9mod = authority.modules[D9_CHECKER]

    def proxy() -> types.SimpleNamespace:
        v16 = types.SimpleNamespace(
            derive_class=d9mod.V17.V16.derive_class)
        return types.SimpleNamespace(
            derive_class=d9mod.derive_class,
            derive_codes=d9mod.derive_codes,
            reduce_concurrent=d9mod.reduce_concurrent,
            check=d9mod.check,
            V17=types.SimpleNamespace(V16=v16),
        )

    mutations: list[tuple[str, Callable[[types.SimpleNamespace], None]]] = [
        ("D9 derive_class noncallable", lambda m: setattr(m, "derive_class", None)),
        ("D9 derive_class wrong result", lambda m: setattr(
            m, "derive_class", lambda _axes: "success")),
        ("D9 derive_codes noncallable", lambda m: setattr(m, "derive_codes", None)),
        ("D9 derive_codes wrong result", lambda m: setattr(
            m, "derive_codes", lambda _axes, _maps: {})),
        ("D9 V17 absent", lambda m: setattr(m, "V17", None)),
        ("D9 V17.V16 derive_class noncallable", lambda m: setattr(
            m.V17.V16, "derive_class", None)),
        ("D9 V17.V16 derive_class wrong", lambda m: setattr(
            m.V17.V16, "derive_class", lambda _axes: "success")),
        ("D9 reducer noncallable", lambda m: setattr(m, "reduce_concurrent", None)),
        ("D9 reducer wrong result", lambda m: setattr(
            m, "reduce_concurrent", lambda _conditions, _precedence: {})),
        ("D9 check noncallable", lambda m: setattr(m, "check", None)),
        ("D9 check wrong result", lambda m: setattr(
            m, "check", lambda _candidate, _predecessor, _v16: ["mutant"])),
    ]
    for name, mutate in mutations:
        module = proxy()
        mutate(module)
        try:
            findings, call_count, row_count = _d9_compatibility_findings(
                authority, module)
            record(name, bool(findings) and call_count == 6 and row_count == 16)
        except Exception:
            record(name, False)

    v17_source = authority.buffers["check-d9-v1.7.py"]
    duplicate = v17_source + b"\nV16 = _load_v16_checker()\n"
    try:
        FrozenAuthority._interposition_node(
            duplicate, "check-d9-v1.7.py",
            D9_INTERPOSITION_SPECS["check-d9-v1.7.py"])
        record("interposition extra target", False)
    except AuthorityError:
        record("interposition extra target", True)
    broadened = v17_source.replace(
        b"V16 = _load_v16_checker()", b"V16 = _load_v16_checker(None)", 1)
    try:
        FrozenAuthority._interposition_node(
            broadened, "check-d9-v1.7.py",
            D9_INTERPOSITION_SPECS["check-d9-v1.7.py"])
        record("interposition broadened selector", False)
    except AuthorityError:
        record("interposition broadened selector", True)
    receipt = copy.deepcopy(authority.interposition_receipts["check-d9-v1.13.py"])
    receipt["restoredCount"] = 0
    record("interposition skipped restoration", not (
        receipt.get("matchCount") == receipt.get("firedCount") ==
        receipt.get("restoredCount") == 1))

    ep8mod = authority.modules[EP8_CHECKER]
    try:
        ep8mod._load_module("filesystem-fallback.py", "forbidden")
        record("EP8 filesystem fallback", False)
    except AuthorityError:
        record("EP8 filesystem fallback", True)
    try:
        ep8mod.load_json(pathlib.Path("/tmp/evaluation-proof.v7.json"))
        # Basename-only resolution is intentional and cwd-independent, but an
        # unknown alias spelling must still reject.
        ep8mod.load_json(pathlib.Path("/tmp/alias-evaluation-proof.v7.json"))
        record("EP8 alias swap", False)
    except AuthorityError:
        record("EP8 alias swap", True)
    before = dict(authority.read_counts)
    ep8mod._EP7 = None
    record("EP8 delayed resolution no reread",
           ep8mod._ep7() is authority.modules[EP7_CHECKER] and
           authority.read_counts == before)
    record("pyc state unchanged", authority._pyc_state() == authority.pyc_before)
    record("no local sys.modules fallback", not any(
        name.startswith("verified_") or name.startswith("opensip_check_")
        for name in sys.modules))

    second_counts = dict(authority.read_counts)
    second_counts[EP7] += 1
    record("second content read", second_counts != authority.pre_exec_read_counts)
    alias_paths = [authority._path_for(name) for name in PINS]
    alias_paths.append(authority._path_for(EP7))
    record("resolved path alias", len(alias_paths) != len(set(alias_paths)))

    ep_mutant = authority.buffers[EP7_CHECKER] + b"\n# coherent EP mutant\n"
    ep_claimed = dict(PINS); ep_claimed[EP7_CHECKER] = sha256(ep_mutant)
    record("coherent EP source/pin substitution",
           sha256(ep_mutant) != PINS[EP7_CHECKER] and
           ep_claimed[EP7_CHECKER] != PINS[EP7_CHECKER])
    d9_mutant = authority.buffers[D9_CHECKER] + b"\n# coherent D9 mutant\n"
    d9_claimed = dict(PINS); d9_claimed[D9_CHECKER] = sha256(d9_mutant)
    record("coherent D9 source/review substitution",
           sha256(d9_mutant) != PINS[D9_CHECKER] and
           d9_claimed[D9_CHECKER] != PINS[D9_CHECKER])
    semantic_mutant = authority.buffers[RT15].replace(
        b'"version": 15', b'"version": 16', 1)
    record("semantic source modification", sha256(semantic_mutant) != PINS[RT15])
    record("local semantic D9 copies absent",
           "_d9_class" not in globals() and "_d9_codes" not in globals())

    required_names = tuple(authority.parsed[RT13]["capabilityClosure"]
                           ["source"]["requiredCheckerApi"])
    try:
        InternalEP8InvocationSurface(ep8mod, required_names[:-1])
        record("EP8 required API omission", False)
    except AuthorityError:
        record("EP8 required API omission", True)
    try:
        InternalEP8InvocationSurface(ep8mod, required_names + ("check",))
        record("EP8 forbidden API extra", False)
    except AuthorityError:
        record("EP8 forbidden API extra", True)
    noncallable = types.SimpleNamespace(**{
        name: (None if name == "validate_bundle" else getattr(ep8mod, name))
        for name in required_names
    })
    try:
        InternalEP8InvocationSurface(noncallable, required_names)
        record("EP8 noncallable required export", False)
    except AuthorityError:
        record("EP8 noncallable required export", True)

    legacy_like = MappingProxyType({"check": ep8mod.check})
    legacy_scan = _forbidden_identity_paths(
        legacy_like, {id(authority): "live FrozenAuthority"})
    record("legacy EP8 function closure reaches authority",
           bool(legacy_scan["forbiddenHits"]) and
           not legacy_scan["findings"])
    snapshot: MappingProxyType | None = None
    try:
        snapshot = VerifiedSemanticRTSnapshotV2(
            expected_candidate(authority), authority)
        graph_clean = not _snapshot_quarantine_findings(snapshot, authority)
        frozen_rejected = False
        try:
            snapshot["ep8DerivationReceipt"]["kind"] = "MUTATED"
        except TypeError:
            frozen_rejected = True
        record("data-only complete snapshot graph", graph_clean)
        record("data-only receipt deep immutable", frozen_rejected)
    except Exception:
        record("data-only complete snapshot graph", False)
        record("data-only receipt deep immutable", False)

    edge_passed, edge_total, edge_failures = _inert_boundary_selftest(snapshot)
    record("closed inert returned-value denominator",
           edge_passed == edge_total and edge_total >= 50 and
           not edge_failures)
    record("v1.10 absent from interposition specs",
           "check-d9-v1.10.py" not in D9_INTERPOSITION_SPECS)
    v110_receipt = authority.temporary_module_receipts.get(
        "check-d9-v1.10.py", {})
    record("v1.10 real frozen dataclass receipt", v110_receipt.get(
        "isDataclass") is True and v110_receipt.get("frozen") is True and
        v110_receipt.get("generatedEquality") is True and
        v110_receipt.get("frozenMutationRejected") is True and
        v110_receipt.get("restoredToAbsent") is True)
    module_name = v110_receipt.get("moduleName")
    if isinstance(module_name, str):
        sys.modules[module_name] = types.ModuleType("poison")
        collision_rejected = False
        try:
            authority._execute_registered_exact("check-d9-v1.10.py")
        except AuthorityError:
            collision_rejected = True
        finally:
            sys.modules.pop(module_name, None)
        record("v1.10 preexisting module poison", collision_rejected and
               module_name not in sys.modules)

        fired = False
        mapping_rejected = False
        original_trace = sys.gettrace()
        def poison_trace(frame: Any, event: str, _arg: Any) -> Any:
            nonlocal fired
            if not fired and event == "line" and \
                    frame.f_code.co_filename.startswith(
                        "<verified:check-d9-v1.10.py:"):
                sys.modules[module_name] = types.ModuleType("mid_exec_poison")
                fired = True
            return poison_trace
        if original_trace is None:
            sys.settrace(poison_trace)
            try:
                authority._execute_registered_exact("check-d9-v1.10.py")
            except Exception:
                mapping_rejected = True
            finally:
                sys.settrace(None)
                sys.modules.pop(module_name, None)
        record("v1.10 mid-exec module poison",
               original_trace is None and fired and mapping_rejected and
               module_name not in sys.modules)
    else:
        record("v1.10 preexisting module poison", False)
        record("v1.10 mid-exec module poison", False)

    failures = [name for name, rejected in results if not rejected]
    return (len(results) - len(failures), len(results), failures,
            edge_passed, edge_total, edge_failures)


def _pin_window_mutation_selftest(
        authority: FrozenAuthority) -> tuple[int, int, int]:
    callback_count = 0

    def verify(buffers: Mapping[str, bytes]) -> None:
        nonlocal callback_count
        if tuple(buffers) != tuple(PINS):
            raise AuthorityError("RT21-PIN-WINDOW-SHAPE")
        for name, expected in PINS.items():
            if sha256(buffers[name]) != expected:
                raise AuthorityError(f"RT21-PIN-MISMATCH:{name}")
        callback_count += 1

    base = dict(authority.buffers)
    verify(base)
    refusals = 0
    callback_escapes = 0
    for name in PINS:
        changed = dict(base)
        changed[name] = changed[name] + b"\x00"
        before = callback_count
        try:
            verify(changed)
        except AuthorityError:
            if callback_count == before:
                refusals += 1
            else:
                callback_escapes += 1
        else:
            callback_escapes += 1
    return refusals, len(PINS), callback_escapes


def selftest(candidate: dict[str, Any], candidate_source: bytes,
             authority: FrozenAuthority) -> int:
    expected = expected_candidate(authority)
    if candidate_source != pretty(expected) or candidate_source != pretty(candidate):
        print("REFUSING to self-test: base is not exact canonical RT21 candidate")
        return 1
    base = check_contract(candidate, authority, candidate_source)
    if base:
        print(f"REFUSING to self-test: base has {len(base)} finding(s)")
        for finding in base[:12]:
            print("  -", finding)
        return 1

    print("frozen authority and canonical base")
    print(f"  pass  {len(PINS)}/{len(PINS)} inputs read once and hash-bound before source execution")
    pin_passed, pin_total, pin_callback_escapes = \
        _pin_window_mutation_selftest(authority)
    print(f"  {'pass' if pin_passed == pin_total and not pin_callback_escapes else 'FAIL':>6}  "
          f"{pin_passed}/{pin_total} single-pin corruptions refused before callback")
    print("  pass  strict duplicate/nonfinite/float rejection and exact canonical candidate")

    generated = build_fixture(
        "RT16-RAW-BYTES-GENERATED-SELFTEST-V1", PROJECT_A,
        synthetic_specs(9, 4),
    )
    generated_findings = _validate_fixture(generated, generated, "generated[9/4]")
    generated_ok = generated["recordCount"] == 9 and generated["unitCount"] == 4 and \
        not generated_findings
    print("\ncount-independent fixture algorithm")
    print(f"  {'pass' if generated_ok else 'FAIL':>6}  generated 9 refs / 4 units; every ref byte-bearing")

    mutations = _candidate_mutations()
    mutation_failures = 0
    signatures: set[str] = set()
    noops = 0
    duplicates = 0
    print("\nexact candidate mutations - every row must be rejected")
    for name, mutate in mutations:
        changed = copy.deepcopy(candidate)
        before = pretty(changed)
        try:
            mutate(changed)
            after = pretty(changed)
            if after == before:
                noops += 1
                rejected = False
            else:
                signature = sha256(after)
                if signature in signatures:
                    duplicates += 1
                signatures.add(signature)
                rejected = bool(check_contract(changed, authority, after))
        except Exception:
            rejected = False
        mutation_failures += 0 if rejected else 1
        print(f"  {'reject' if rejected else 'ESCAPE':>6}  {name}")

    fixtures = candidate["verifiedSemanticRtApiContract"][
        "rawObjectResolutionConformance"]["fixtureGoldens"]
    raw_passed, raw_total, raw_escapes = _raw_adversarial(fixtures)
    print(f"\nraw resolution adversarial: {raw_passed}/{raw_total} rejected at exact validation stage; escapes={raw_escapes}")
    lease_gold = candidate["semanticLeaseProtocolV3"]["goldenScenarios"]
    lease_passed, lease_total, lease_escapes = _lease_adversarial(lease_gold)
    print(f"semantic lease shape adversarial: {lease_passed}/{lease_total} rejected; escapes={lease_escapes}")

    hostile: list[tuple[str, Any]] = list(HOSTILE_ROOTS)
    for key in ROOT_ORDER:
        for value in (None, "hostile"):
            changed = copy.deepcopy(candidate)
            changed[key] = value
            hostile.append((f"{key}={type(value).__name__}", changed))
    hostile_failures = 0
    for _name, value in hostile:
        try:
            source = pretty(value)
            rejected = bool(check_contract(value, authority, source))
        except Exception:
            rejected = False
        hostile_failures += 0 if rejected else 1
    print(f"hostile totality: {len(hostile) - hostile_failures}/{len(hostile)} rejected without escape")

    legacy_findings, legacy_count = _legacy_lease_findings(authority)
    d9_findings, call_count, row_count = _d9_compatibility_findings(authority)
    print("\nsupplemental predecessor compatibility (not authority promotion)")
    print(f"  {'pass' if not legacy_findings else 'FAIL':>6}  {legacy_count} applicable RT13 lease transitions")
    print(f"  {'pass' if not d9_findings else 'FAIL':>6}  RT14/D9 v1.13: {call_count} call shapes, {row_count} rows")

    (trust_passed, trust_total, trust_failures,
     edge_passed, edge_total, edge_failures) = _trust_falsifiers(authority)
    print("\nauthenticated-loader and executed-D9 falsifiers")
    print(f"  {'pass' if not trust_failures else 'FAIL':>6}  {trust_passed}/{trust_total} rejected or contained")
    for failure in trust_failures:
        print(f"  ESCAPE  {failure}")
    print("\nclosed inert returned-value boundary and active attacks")
    print(f"  {'pass' if not edge_failures else 'FAIL':>6}  "
          f"{edge_passed}/{edge_total} inert-boundary checks")
    print(f"  {'pass' if not edge_failures else 'FAIL':>6}  "
          f"{len(INERT_VALUE_REGISTRY)}/{len(INERT_VALUE_REGISTRY)} "
          "value-kind deletion mutations refuse before root")
    print(f"  {'pass' if not edge_failures else 'FAIL':>6}  "
          f"{len(INERT_EDGE_REGISTRY)}/{len(INERT_EDGE_REGISTRY)} "
          "semantic-edge deletion mutations refuse before root")
    print(f"  {'pass' if not edge_failures else 'FAIL':>6}  "
          "34/34 independent review-derived runtime kinds challenged")
    print(f"  {'pass' if not edge_failures else 'FAIL':>6}  "
          "7/7 host operation signatures; 2/2 projection, 12/12 raw, "
          "9/9 lease, and 9/9 predicate goldens")
    for failure in edge_failures:
        print(f"  ESCAPE  {failure}")

    dirty = candidate_source.replace(b"{\n", b"{ \n", 1)
    try:
        parsed_dirty = parse_json_bytes(dirty, "dirty")
        dirty_refused = dirty != candidate_source and dirty != pretty(parsed_dirty)
    except Exception:
        dirty_refused = False
    print(f"  {'pass' if dirty_refused else 'FAIL':>6}  dirty parsed-equal base refused before mutation accounting")

    authority.end_stat_check()
    failed = (
        not generated_ok or mutation_failures or noops or duplicates or
        pin_passed != pin_total or pin_callback_escapes
        or raw_escapes or lease_escapes or hostile_failures
        or legacy_findings or d9_findings or trust_failures or not dirty_refused
    )
    print()
    if failed:
        print(
            "RT20 selftest failures: "
            f"generated={not generated_ok}, object={mutation_failures}/{len(mutations)}, "
            f"noops={noops}, duplicates={duplicates}, raw={raw_escapes}/{raw_total}, "
            f"lease={lease_escapes}/{lease_total}, hostile={hostile_failures}/{len(hostile)}, "
            f"legacy={len(legacy_findings)}, d9={len(d9_findings)}, "
            f"trust={len(trust_failures)}/{trust_total}, dirty={not dirty_refused}"
        )
        return 1
    print(
        f"all {len(mutations)} exact candidate mutations, {raw_total} raw-resolution "
        f"adversarials, {lease_total} lease-shape adversarials, and {len(hostile)} hostile "
        "shapes rejected; zero no-op, duplicate, skipped, ambiguous, or escaped cases; "
        "generated 9/4 fixture, exact RT13 lease projection, and RT14/D9 6-call/16-row "
        f"supplemental compatibility passed; {trust_total} authenticated-loader/D9 "
        f"falsifiers rejected or contained; {edge_total} inert-boundary checks "
        f"passed, including {len(INERT_VALUE_REGISTRY)}/"
        f"{len(INERT_VALUE_REGISTRY)} value-kind and "
        f"{len(INERT_EDGE_REGISTRY)}/{len(INERT_EDGE_REGISTRY)} edge deletions, "
        "34/34 review-derived runtime-kind challenges, exact host signatures, "
        "and zero callable/code/frame/reducer value in the returned snapshot"
    )
    return 0


def main(argv: list[str]) -> int:
    try:
        authority = FrozenAuthority()
        authority.freeze()
    except (OSError, UnicodeError, SyntaxError, AuthorityError, ValueError,
            DuplicateKeyError, FloatForbidden, json.JSONDecodeError) as exc:
        print(f"cannot freeze RT21 authority: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--emit-candidate" in argv[1:]:
        sys.stdout.buffer.write(pretty(expected_candidate(authority)))
        authority.end_stat_check()
        return 0
    positional = [item for item in argv[1:]
                  if item not in ("--selftest", "--emit-candidate")]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        source = path.read_bytes()
        candidate = parse_json_bytes(source, str(path))
    except (OSError, UnicodeError, ValueError, DuplicateKeyError, FloatForbidden,
            json.JSONDecodeError) as exc:
        print(f"cannot load RT21 candidate: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--selftest" in argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        return selftest(candidate, source, authority)
    findings = check_contract(candidate, authority, source)
    try:
        authority.end_stat_check()
    except AuthorityError as exc:
        findings.append(f"RT21-AUTHORITY-END: {exc}")
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    raw = candidate["verifiedSemanticRtApiContract"][
        "rawObjectResolutionConformance"]["fixtureGoldens"]
    print(
        f"RT21 contract OK - {path.name}; {len(PINS)} frozen inputs read once; "
        f"byte-bearing fixtures {raw[0]['recordCount']}/{raw[0]['unitCount']} and "
        f"{raw[1]['recordCount']}/{raw[1]['unitCount']}; exact RT13 semantic basis; "
        f"closed {len(INERT_VALUE_REGISTRY)}-kind/{len(INERT_EDGE_REGISTRY)}-edge "
        "inert data-only return with seven host-owned pure operations; "
        "real v1.10 frozen dataclass; "
        "CANDIDATE-NOT-APPLIED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
