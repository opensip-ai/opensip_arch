"""Shared vocabulary for the native wire-carrier author candidate 05 (TS2 + Rust3).

AUTHOR candidate for independent review. Not approval, not a production wire decoder, not product code.
Every integer literal in emitted documents is a decimal string so a TypeScript consumer never loses precision.
"""
import os
from pathlib import Path

SUBJECT = Path(__file__).resolve().parent.parent
ARCH_DEFAULT = "/Users/sb/code/opensip-ai/opensip_arch"


def arch_root():
    return Path(os.environ.get("OPENSIP_ARCH", ARCH_DEFAULT))


# Architecture snapshot pins: (repository-relative path, sha256, bytes). This is the COMPLETE set of architecture files
# the checker and builder read or execute (observed with an open audit hook; check.py fails on any unpinned read).
ARCH_PINS = {
    "c2v3": ("docs/coop/artifacts/c2-plan-stage-schema.v3.json", "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285", 112128),
    "checkFactPlane": ("docs/coop/artifacts/check-fact-plane.py", "c7ebcd3ee2c206ae8cdd6dfd1750236e465bdab7e9a104b105fe8e85330e29ac", 64066),
    "checkRust2": ("docs/coop/artifacts/check-rust-provider-protocol-v2.py", "7b967b888fc172b27268fae2f59273e5cf10b58b97db7c1f19a15657826a48e4", 105962),
    "checkRust1": ("docs/coop/artifacts/check-rust-provider-protocol.py", "c190ee7f62552ec342f5da1f66ba2b840cdffd5cd5cddb25e5987c315ee1502e", 125802),
    "delivery2": ("docs/coop/artifacts/delivery.v2.json", "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3", 143995),
    "factPlane": ("docs/coop/artifacts/fact-plane.v1.json", "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d", 59168),
    "resolvedInputs2": ("docs/coop/artifacts/resolved-inputs.v2.json", "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43", 107615),
    "rust2": ("docs/coop/artifacts/rust-provider-protocol.v2.json", "6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b", 61698),
    "discoveryDefaults": ("docs/coop/design-corrections/discovery-defaults.py", "f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c", 22344),
    "canonical": ("docs/coop/design-corrections/foundation/canonical.py", "d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442", 6465),
    "identityModel2": ("docs/coop/design-corrections/foundation/identity-model.py", "12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6", 135671),
    "identityModel3": ("docs/coop/design-corrections/foundation/identity-model.v3.py", "a6dc5f997b5b9502d185d1b68a61765516ccf5f64f1c33a4282682ebee2803dc", 157684),
    "identitySchemas2": ("docs/coop/design-corrections/foundation/identity-schemas.v2.json", "c56679857b83e0ff71f8eca9345e29433617030945429d524bb5645669d267d5", 148414),
    "identitySchemas3": ("docs/coop/design-corrections/foundation/identity-schemas.v3.json", "a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21", 196987),
    "relationRegistry2": ("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json", "53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a", 57623),
    "capabilityDomains": ("docs/coop/design-corrections/native/capability-manifest-domains.v2.json", "1456ae1476dfe1b0f3b1134c9d7a36e35890e45e20f57e7bbc2b7ada2144aef6", 16522),
    "dispatch": ("docs/coop/design-corrections/native/dispatch-binding.schema.v1.json", "868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938", 4568),
    "factBatch3": ("docs/coop/design-corrections/native/fact-batch.schema.v3.json", "b0ebc133df8763f6cd5f3716542321eba21c69714fca368fbe31ba57677a24e0", 10028),
    "capabilityMatrix": ("docs/coop/design-corrections/native/native-capability-matrix.v2.json", "4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14", 36595),
    "nativeCases": ("docs/coop/design-corrections/native/native-cases.v2.json", "a08b8cc380a2d332a752405fde11df1d5d63b050c7297ec21820516702367ddc", 952644),
    "evidence": ("docs/coop/design-corrections/native/native-evidence.schemas.v2.json", "2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043", 277967),
    "nativeModel": ("docs/coop/design-corrections/native/native_evidence_model.v2.py", "7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be", 319376),
    "occupancy": ("docs/coop/design-corrections/native/occupancy-companion.schema.v1.json", "d2bbbcc49adbb130d0bb010fee0b4cf25af7727f730fc329725fa62cd46ae14f", 8821),
    "p3": ("docs/coop/design-corrections/native/protocol3-transitions.v1.json", "b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b", 14845),
    "handshake": ("docs/coop/design-corrections/native/provider-handshake.schemas.v1.json", "9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84", 32009),
    "startup": ("docs/coop/design-corrections/native/provider-startup.schemas.v1.json", "1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c", 33341),
    "startupModel": ("docs/coop/design-corrections/native/provider_startup_model.v1.py", "3f75b859b45c4fc6d5e5c8ede642a981d8d83bdf55d8e19ef7c9ffe7d5e8d494", 16245),
    "wireModel": ("docs/coop/design-corrections/native/provider_wire_model.v1.py", "a2a8b9d116552856412e4257069f8c75debd6d8b2fe165407477fb7b28e46295", 19099),
    "ts2order": ("docs/coop/design-corrections/native/typescript-protocol2-order.v1.json", "007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb", 11341),
    "workflowCommon": ("docs/coop/design-corrections/workflows/schemas/common.schema.json", "b7b25d5e7c2bf2c8d3496a2f222c31bcc87360f3e2541fbdb551136358f7d39c", 55042),
    "workflowImported": ("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json", "edce21a3c7905f215c019eddc5776e08e6cff59a6ceea4b4e422275ead594b9e", 46315),
    "workflowTest": ("docs/coop/design-corrections/workflows/schemas/test-execution.schema.json", "a6f7c2d85cdc4c4bb018288d962f7d30384fd8924162a0cb5c95582de043d54b", 13672),
    "publicDetailRegistry": ("docs/coop/design-corrections/public-detail-registry.v1.json", "2702e6ca97b6d8095cbcef0b0a219048b1ffdc434e0d8bb8c4bff247cda70e68", 59547),
    "controlRoute": ("docs/implementation/m1/control-source-route.v1.json", "3965745fd1413e35a9913ed394e7d81075ed5d64c4e21f07533c52eb656c2c02", 1826),
    "importSourceContext": ("docs/coop/design-corrections/foundation/import-source-context.schema.json", "51cdca8bd3c9212d11982416b9101be96bdcf47db22efb0098b39c7850ae6518", 842),
    "enumerationPlan": ("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json", "10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c", 19975),
    "subjectInventory": ("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json", "6ab46925853d26c1a5f7ae1fbd69db5dcc9052fdefdb1b265e53481b4e1cee33", 16861),
    "evaluatorEmissionPlan": ("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json", "ac9ae438ca3e1a94e257209c460cd7beed5047e0d9d0a7bf49a94b637dd3198e", 3055),
    "targetAttribution1": ("docs/coop/design-corrections/foundation/target-attribution.schema.v1.json", "788bd9d000fb1da830ef368d14c119f441f7b60e8a56f8da3467ef0fbf0ed90e", 13480),
    "targetAttribution2": ("docs/coop/design-corrections/foundation/target-attribution.schema.v2.json", "bd938f11c584be65e914bc1446193fdf3dd4a15f7b78630cc3eb628c5bca1d53", 23086),
    "incomingSearch": ("docs/coop/design-corrections/foundation/incoming-search.schema.v1.json", "accb597a95969109fc88cf40eada296231afe510093d6fb56449f6cbf465b8a1", 13724),
    "executionInputs": ("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json", "604bd94175584128adbeb241fdba2f48e2220de74d6505a671eae2ce892700e9", 39910),
    "identityMd": ("docs/v2/contracts/product-v1/identity-and-evidence.md", "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f", 135448),
    "nativeMd": ("docs/v2/contracts/product-v1/native-evidence.md", "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0", 329013),
}

# Pinned ECMA-262 execution tool for RF-3 (the declared pattern dialect). The binary bytes are verified before every exec;
# its dynamic libraries are operating-system frameworks recorded here, not pinned (honest execution-closure record).
NODE = {
    "path": "/Users/sb/.nvm/versions/node/v24.16.0/bin/node",
    "sha256": "1ee75375e33b94fc34b3b19aede049e11dae90efb63b374dc96d6bdace70c4b8",
    "bytes": 120573328,
    "versions": {"node": "24.16.0", "v8": "13.6.233.17-node.49", "icu": "78.3", "unicode": "17.0"},
    "dynamicLibraries": ["/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation",
                         "/System/Library/Frameworks/Security.framework/Versions/A/Security",
                         "/usr/lib/libc++.1.dylib", "/usr/lib/libSystem.B.dylib"],
}

# Subject-local frozen inputs (byte copies; build-time method inputs, also cross-checked by check.py).
SUBJECT_INPUTS = {
    "tsFields": ("inputs/ts2-fields.json", "4c211bb5fd28115b9fad3384d978b3911dd8f1f63cbd6fcf2e633430a27efe6a",
                 "/tmp/opensip-implementation/m1-typescript-wire-translation-01/fields.json"),
    "rustFields": ("inputs/rust3-fields.json", "26cc2b9b2ad07287ed59afdd455b79c684a033078fd562684a27f417512af41b",
                   "/tmp/opensip-implementation/m1-rust-wire-translation-01/fields.json"),
    "generatorOptions": ("inputs/generator-candidate03-options.json", "1719ef1860624e390af57f58c9670b60c68aa9d599eba3a4cee18d43343d7902",
                         "/tmp/opensip-implementation/m1-generator-integration-candidate-03/tools/contracts/options.json"),
}
# Unexecuted provenance only (never opened by build or check).
PROVENANCE_ONLY = [
    {"path": "/tmp/opensip-implementation/m1-protocol-gap-resolution-01/resolutions.md", "sha256": "c60af837f526b2de5982c7abdb94f4400687a61d04aae0c516c1fe692ea90781", "use": "method reading of proposals P-1..P-4"},
    {"path": "/tmp/opensip-implementation/m1-native-wire-owner-review-01/review.json", "sha256": None, "use": "required findings RF-1..RF-6 and advisories"},
    {"path": "/tmp/opensip-implementation/m1-native-wire-owner-review-02/review.json", "sha256": None, "use": "required findings RF-1..RF-3 and advisories A-1..A-7 (the review-02 ECMA engine output is a byte copy under prior/review-02/ and IS a check input)"},
    {"path": "/tmp/opensip-implementation/m1-native-wire-owner-review-03/review.json", "sha256": None, "use": "required findings RF-1..RF-4 and advisories A-1..A-9 (the review-03 ECMA engine probe output is a byte copy under prior/review-03/ and IS a check input)"},
]

EXTERN_NS = {
    "opensip.product.provider-handshake.1": "Handshake1",
    "opensip.product.provider-startup.1": "Startup1",
    "urn:opensip:product-v1:native:evidence-schemas:v2": "Native2",
    "opensip.product.occupancy-companion.1": "Occupancy1",
    "opensip.product.fact-batch.3": "FactBatch3",
    "opensip.product.dispatch-binding.1": "Dispatch1",
}
HS, ST, NE, OC = ("opensip.product.provider-handshake.1", "opensip.product.provider-startup.1",
                  "urn:opensip:product-v1:native:evidence-schemas:v2", "opensip.product.occupancy-companion.1")

U64_MAX = 18446744073709551615
I63_MAX = 9223372036854775807


def s(n):
    return None if n is None else str(n)


def _clean(d):
    return {k: v for k, v in d.items() if v is not None}


# ----- closed type-expression grammar (see wire-carriers.meta.schema.json) -----
def U(min=None, max=None, const=None):
    return _clean({"t": "uint64", "min": s(min), "max": s(max), "const": s(const)})


def T(min_scalars=None, max_scalars=None, max_utf8=None, pattern=None, enum=None, const=None, controls=None, lexical=None):
    return _clean({"t": "text", "nfc": True, "minScalars": s(min_scalars), "maxScalars": s(max_scalars),
                   "maxUtf8Bytes": s(max_utf8), "pattern": pattern,
                   "enum": sorted(enum, key=lambda x: x.encode()) if enum else None, "const": const,
                   "forbidC0C1": controls, "lexical": lexical})


def B(min_bytes, max_bytes):
    return {"t": "bytes", "minBytes": s(min_bytes), "maxBytes": s(max_bytes)}


def BOOL(const=None):
    return _clean({"t": "bool", "const": const})


NULL = {"t": "null"}


def A(items, min_items, max_items, order="sequence"):
    return _clean({"t": "array", "items": items, "minItems": s(min_items), "maxItems": s(max_items), "order": order})


def REF(name):
    return {"t": "ref", "ref": name}


def EXT(schema_id, pointer):
    name = pointer.rsplit("/", 1)[-1] if pointer != "#" else "Root"
    return {"t": "extern", "schemaRef": schema_id + pointer, "generatedType": EXTERN_NS[schema_id] + name}


def NULLABLE(x):
    return {"t": "nullable", "of": x}


def M(name, type_, presence="required", note=None):
    return _clean({"name": name, "type": type_, "presence": presence, "note": note})


def REC(members, source, admission=(), note=None):
    return _clean({"kind": "record", "members": members, "source": source, "admission": list(admission), "note": note})


def VREC(discriminator, member_order, variants, source, admission=(), note=None):
    return _clean({"kind": "variant-record", "discriminator": discriminator, "memberOrder": member_order,
                   "variants": variants, "source": source, "admission": list(admission), "note": note})


def ALIAS(target, source, note=None):
    return _clean({"kind": "alias", "target": target, "source": source, "note": note})


def SRC(key, selector):
    return {"pin": key, "selector": selector}


ORDERS = {
    "sequence": "declared order preserved; no sort law beyond the member's admission rules",
    "utf8-strict": "strictly ascending by UTF-8 bytes of the text item; duplicates refuse",
    "path-utf8-strict": "strictly ascending by UTF-8 bytes of item.path; duplicates refuse",
    "cbor-bytes-strict": "strictly ascending by deterministic-CBOR bytes of the item under the language profile; duplicates refuse",
    "cve1-bytes-strict": "strictly ascending by CVE1(item) bytes (resolved-inputs.v2 planIdContract.canonicalValueEncoding); duplicates refuse",
    "candidateOrdinal-contiguous": "candidateOrdinal contiguous, starting at DispatchBindingV1.expectedFirstCandidateOrdinal",
    "candidateOrdinal-increasing": "candidateOrdinal unique strictly increasing (occupancy vocabulary); each names a candidate of this batch",
    "package-tuple-then-path": "strictly ascending by the UTF-8 byte tuple (name, version, sourceId, path) of the exactly joined DependencySourceSetV1 package row; equals packages x-opensip-order then DependencyFileManifestV1 path order",
    "nested-loop-relation-rung-target": "rust2 coverageDomainAlgorithm canonical nested-loop order; duplicates refuse",
    "request-order": "exactly one item per requested stage, in Analyze request order",
    "outputOrdinal-contiguous": "outputOrdinal equals array index; PreparedOutputSetV3.rows order",
}
