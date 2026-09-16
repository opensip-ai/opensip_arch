"""Native evidence reference checker v2.

Design evidence only: validates fixtures against the closed v2 schema bundle after exact typed
admission, verifies every consumed source pin, runs hand-authored cases against
native_evidence_model.v2.py and writes native-evidence-report.v2.json. It executes no compiler,
provider, Cargo, or repository code and qualifies no platform.

  python -I -B check_native_evidence.v2.py                 # verify pins, run cases, write report
  python -I -B check_native_evidence.v2.py --regenerate-pins   # rewrite source-pins.v2.json from current bytes
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PINS_PATH = HERE / "source-pins.v2.json"
CASES_PATH = HERE / "native-cases.v2.json"
REPORT_PATH = HERE / "native-evidence-report.v2.json"
FOUNDATION_DIR = HERE.parent / "foundation"
MATRIX_PATH = HERE / "native-capability-matrix.v2.json"

CONSUMED_SOURCES = [
    # (repo-relative path, why it is consumed)
    ("docs/coop/design-corrections/foundation/canonical.py", "imported: exact parse/canonical/identity/validate"),
    ("docs/coop/design-corrections/foundation/identity-model.py", "imported: import2 identifier and ordered-array admission"),
    ("docs/coop/design-corrections/foundation/identity-schemas.v2.json", "import2 wrapper, fact2, coverage2, snapshot2, plan2 closed schemas"),
    ("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json", "the single relation ladder authority: LADDERS is read from it and every mirror is drift-checked against it in order"),
    ("docs/coop/design-corrections/JOINT-INTERFACES.md", "shared choices; ownership; identity join"),
    ("docs/v2/contracts/product-v1/identity-and-evidence.md", "canonical encoding, domain table, predicate semantics"),
    ("docs/coop/design-corrections/reviews/native-author-feedback.v1.md", "the twelve corrections this unit answers"),
    ("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json", "workflow canonical RuntimePayloadV1/HistoryPayloadV1 schema document and ImportWrapperV2 digest recipes; payloadSchemaDigest = raw SHA-256 of these bytes (§7)"),
    ("docs/coop/design-corrections/workflows/schemas/common.schema.json", "workflow shared SourceCorrespondence and primitives; validated directly by the model (§7)"),
    ("docs/coop/design-corrections/workflows/schemas/test-execution.schema.json", "workflow canonical TestPayloadV1 schema document; payloadSchemaDigest = raw SHA-256 of these bytes (§7)"),
    ("docs/coop/design-corrections/foundation/product-configuration.schema.v2.json", "Config2 discovery section consumed by unit discovery (§1.4)"),
    ("docs/v2/contracts/product-v1/workflows-and-surfaces.md", "workflow §4 import registry and §7 P-TRUSTED-REPO spelling joined in §5/§7"),
    ("docs/v2/contracts/product-v1/security-and-lifecycle.md", "S10 principal class repository-code and RepoExecutionGrantV1 joined in §5.1"),
    ("docs/coop/design-corrections/security/security_lifecycle_model_v1.py", "repository-code principal, revocation/cancellation boundaries (H-2)"),
    ("docs/coop/artifacts/rust-provider-protocol.v2.json", "superseded selectors: repositoryExecution, RepositoryResolutionV2, CoverageResultV2, UnavailableV2, limits, phases"),
    ("docs/coop/artifacts/resolved-inputs.v2.json", "superseded selectors: rust-v1/typescript-v1 resolvedInputs, ifIncomplete"),
    ("docs/coop/artifacts/delivery.v2.json", "superseded selectors: repositoryExecution.withGrant, offlineAssets, CoverageResultV1.completenessRule; platform inventory"),
    ("docs/coop/artifacts/fact-plane.v1.json", "superseded selectors: sufficiency, deficiencyVocabulary, requirementSchema; relation registry extended"),
    ("docs/coop/artifacts/check-fact-plane.py", "v1 sufficiency mirrored as the AR-12 counterexample oracle"),
    ("docs/coop/artifacts/c2-plan-stage-schema.v4.json", "retained: subjectScopeCommitment"),
    ("docs/coop/artifacts/permission-truth-tables.v9.json", "copied enforcement values for AuthorizedExecutionV2.effects"),
    ("docs/coop/artifacts/d9-exit-contract.v1.14.json", "existing D9 classes/codes used by interim mappings"),
    ("docs/coop/artifacts/fact-identity-policy.v2.json", "retained clone normalisation ladder"),
    ("docs/coop/completion/language-quality-matrix.completed.v2.json", "TypeScript cells retained by the v2 matrix"),
    ("docs/v2/architecture/10-mvp-and-future-scope.md", "one product design: native language depth, platforms, exclusions"),
    ("docs/v2/architecture/03-configuration-and-security.md", "preserved confinement honesty and execution default"),
    ("docs/coop/architecture-depth-review/REVIEW.md", "AR-07/12/13/16 findings"),
    ("docs/coop/design-corrections/native/native-evidence.schemas.v2.json", "owned: closed schema bundle under test"),
    ("docs/coop/design-corrections/native/native_evidence_model.v2.py", "owned: model under test"),
    ("docs/coop/design-corrections/native/native-cases.v2.json", "owned: hand-authored cases"),
    ("docs/coop/design-corrections/native/native-capability-matrix.v2.json", "owned: matrix validated here"),
    ("docs/v2/contracts/product-v1/native-evidence.md", "owned: contract these checks evidence"),
]
PRIMARY_REFERENCES = [
    {"url": "https://doc.rust-lang.org/cargo/reference/config.html", "readOn": "2026-09-06", "claim": "Cargo reads .cargo/config.toml (and legacy .cargo/config) in all ancestors of CWD and in CARGO_HOME; arrays merge; executable/linker/runner/credential knobs and environment overrides exist"},
    {"url": "https://doc.rust-lang.org/rustc/command-line-arguments.html", "readOn": "2026-09-06", "claim": "rustc accepts -C linker/link-arg/link-args/link-self-contained, -L, --sysroot, --extern, --remap-path-prefix and @path response files"},
    {"url": "https://www.typescriptlang.org/tsconfig/allowJs.html", "readOn": "2026-09-06", "claim": "allowJs admits JavaScript files into the program alongside TypeScript"},
    {"url": "https://www.typescriptlang.org/tsconfig/checkJs.html", "readOn": "2026-09-06", "claim": "checkJs enables error reporting in JavaScript files; it does not change what is resolved"},
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regenerate_pins() -> None:
    pins = [{"path": p, "sha256": sha256_file(REPO / p), "consumedFor": why} for p, why in CONSUMED_SOURCES]
    doc = {"artifact": "opensip.native-evidence.source-pins", "version": 2, "status": "PROPOSED",
           "purpose": "Exact SHA-256 pins of every source consumed by the native unit (contract, schemas, model, cases, foundation canonical/identity, joint interfaces, superseded artifacts). The checker refuses to run cases if any pin differs.",
           "primaryReferences": PRIMARY_REFERENCES, "pins": pins}
    PINS_PATH.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {PINS_PATH.name} with {len(pins)} pins")


def verify_pins() -> list[dict]:
    if not PINS_PATH.exists():
        return [{"path": str(PINS_PATH), "fault": "pin file missing; run --regenerate-pins"}]
    pins = json.loads(PINS_PATH.read_text(encoding="utf-8"))["pins"]
    faults = []
    pinned = {p["path"] for p in pins}
    for p, _ in CONSUMED_SOURCES:
        if p not in pinned:
            faults.append({"path": p, "fault": "consumed source not pinned"})
    for p in pins:
        target = REPO / p["path"]
        if not target.exists():
            faults.append({"path": p["path"], "fault": "missing"}); continue
        actual = sha256_file(target)
        if actual != p["sha256"]:
            faults.append({"path": p["path"], "fault": "sha256 mismatch", "expected": p["sha256"], "actual": actual})
    return faults


def load_model():
    spec = importlib.util.spec_from_file_location("native_evidence_model_v2", HERE / "native_evidence_model.v2.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------
# Step interpreter
# ---------------------------------------------------------------------------

def expand_tokens(spec: str) -> list[dict]:
    """'kind:value kind:value ...' shorthand for token lists; '|' separates value with spaces."""
    out = []
    for item in spec.split():
        kind, _, value = item.partition(":")
        out.append({"kind": kind, "value": value.replace("|", " ")})
    return out


def resolve(value, env):
    if isinstance(value, str) and value.startswith("$"):
        head, *rest = value[1:].split(".")
        cur = env[head]
        for part in rest:
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        return copy.deepcopy(cur)
    if isinstance(value, dict):
        if set(value) == {"$tokens"}:
            return expand_tokens(value["$tokens"])
        if set(value) == {"$set"}:
            return set(resolve(value["$set"], env))
        if set(value) == {"$merge", "$with"}:
            base = resolve(value["$merge"], env)
            for path, v in value["$with"].items():
                cur = base; keys = json.loads(path) if path.startswith("[") else path.split(".")
                for k in keys[:-1]:
                    cur = cur[int(k)] if isinstance(cur, list) else cur[k]
                last = keys[-1]
                if isinstance(cur, list):
                    cur[int(last)] = resolve(v, env)
                else:
                    cur[last] = resolve(v, env)
            return base
        return {k: resolve(v, env) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(v, env) for v in value]
    return value


def get_path(obj, path: str):
    cur = obj
    for part in path.split("."):
        if part == "":
            continue
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            cur = getattr(cur, part)
    return cur


def same(a, b) -> bool:
    if isinstance(a, set):
        a = sorted(a)
    if isinstance(b, set):
        b = sorted(b)
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def run_case(case: dict, model, fixtures: dict) -> dict:
    env: dict = {"fixtures": fixtures}
    faults: list[str] = []
    for step in case.get("steps", []):
        fn = step["fn"]; args = resolve(step.get("args", {}), env); bind = step.get("bind")
        expect_error = step.get("expectError")
        try:
            if fn == "parse":
                result = model.C.parse(args["raw"].encode("utf-8"))
            elif fn == "validate":
                result = model.validate_native(args["def"], args["value"])
            elif fn == "canonical":
                result = model.C.canonical(args["value"]).decode("utf-8")
            elif fn == "identityVector":
                canonical = model.C.canonical(args["descriptor"])
                if canonical != args["canonicalUtf8"].encode("utf-8"):
                    faults.append(f"canonical bytes differ from hand-spelled: {canonical!r}")
                preimage = b"opensip.product.v1\0" + args["domain"].encode("ascii") + b"\0" + len(canonical).to_bytes(8, "big") + canonical
                oracle = "sha256:" + hashlib.sha256(preimage).hexdigest()
                result = {"model": model.native_identity(args["domain"], args["def"], args["descriptor"]), "oracle": oracle,
                          "rawSha256": hashlib.sha256(canonical).hexdigest()}
            elif fn == "foundationIdentityVector":
                # Independent hashlib oracle for a FOUNDATION-domain identity (subject-scope / closure /
                # coverage), the counterpart of identityVector for native domains. The native `sha256:`
                # text form of the same digest is returned so a case can pin both spellings at once.
                canonical = model.C.canonical(args["descriptor"])
                if "canonicalUtf8" in args and canonical != args["canonicalUtf8"].encode("utf-8"):
                    faults.append(f"canonical bytes differ from hand-spelled: {canonical!r}")
                preimage = b"opensip.product.v1\0" + args["domain"].encode("ascii") + b"\0" + len(canonical).to_bytes(8, "big") + canonical
                oracle_hex = hashlib.sha256(preimage).hexdigest()
                result = {"oracle": model.IM.PREFIX[args["domain"]] + ":" + oracle_hex,
                          "model": model.IM.identifier(args["domain"], args["descriptor"]),
                          "sha256Text": "sha256:" + oracle_hex, "rawSha256": hashlib.sha256(canonical).hexdigest()}
            elif fn == "concat":
                # join resolved parts into one string, so a case can assert an exact typed refusal whose
                # subject is a value the step above computed rather than a frozen literal
                result = "".join(args["parts"])
            elif fn == "sha256Utf8":
                result = hashlib.sha256(args["text"].encode("utf-8")).hexdigest()
            elif fn == "schemaDocumentDigest":
                result = hashlib.sha256((REPO / args["path"]).read_bytes()).hexdigest()
            elif fn == "rawSha256Canonical":
                result = hashlib.sha256(model.C.canonical(args["value"])).hexdigest()
            else:
                result = getattr(model, fn)(**args)
            if expect_error:
                faults.append(f"step {fn}: expected error containing {expect_error!r} but got result")
        except Exception as exc:  # noqa: BLE001 — every refusal is a typed exception here
            text = getattr(exc, "message", None) or str(exc)
            if expect_error and expect_error in text:
                result = {"error": text}
            else:
                faults.append(f"step {fn}: {type(exc).__name__}: {text}")
                result = None
        if bind:
            env[bind] = result
    for path, expected in case.get("expect", {}).items():
        try:
            actual = get_path(env, path.lstrip("$"))
        except Exception as exc:  # noqa: BLE001
            faults.append(f"expect {path}: unreachable ({exc})"); continue
        if isinstance(expected, dict) and set(expected) == {"$not"}:
            forbidden = resolve(expected["$not"], env)
            if same(actual, forbidden):
                faults.append(f"expect {path}: must differ from {json.dumps(forbidden, default=sorted)[:200]}")
            continue
        expected_r = resolve(expected, env)
        if not same(actual if not isinstance(actual, set) else sorted(actual), expected_r if not isinstance(expected_r, set) else sorted(expected_r)):
            faults.append(f"expect {path}: got {json.dumps(actual, default=sorted)[:400]} want {json.dumps(expected_r, default=sorted)[:400]}")
    return {"id": case["id"], "feedback": case.get("feedback", []), "kind": case.get("kind", "positive"), "passed": not faults, "faults": faults}


def main(argv: list[str]) -> int:
    if "--regenerate-pins" in argv:
        regenerate_pins(); return 0
    report = {"artifact": "opensip.native-evidence-report", "version": 2, "status": "PROPOSED",
              "standing": "design reference evidence; not product measurement; no compiler, provider, Cargo or repository code executed; no platform qualified",
              "python": sys.version.split()[0], "jsonschema": __import__("importlib.metadata").metadata.version("jsonschema"),
              "trustedObservationInputs": "every fixture's provider/adapter observations are assumed inputs marked in native-cases.v2.json; the model decides host behavior only"}
    pin_faults = verify_pins()
    report["pins"] = {"verified": not pin_faults, "faults": pin_faults}
    if pin_faults:
        report["result"] = "PIN-MISMATCH"; REPORT_PATH.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(pin_faults, indent=1)); return 2
    model = load_model()
    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(model.SCHEMAS)

    # ---- relation ladder: one authority, every mirror drift-checked exactly AND IN ORDER.
    # The kit carried four independent ladder copies and they had already drifted: the capability
    # domain registry's arrays were alphabetised while declaring the inherited ladder as their
    # source, reversing calls/imports/references. Order is load-bearing (_rung_index compares
    # positions), so set equality is not a sufficient check.
    authority = model.C.parse(
        (FOUNDATION_DIR / "relation-payload-schemas.v2.json").read_bytes()
    )["x-opensip-relation-registry"]["relations"]
    # Plain json: the inherited artifact is a historical design document, not a product payload
    # under C (it carries float lexemes elsewhere, which C correctly refuses). Only its ladders
    # are read here, and they are compared as exact string arrays.
    inherited = json.loads(
        (REPO / "docs/coop/artifacts/fact-plane.v1.json").read_text(encoding="utf-8")
    )["relationRegistry"]["relations"]
    domain_ladders = model.CAPABILITY_DOMAINS["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    rung_vocabulary = set(model.SCHEMAS["$defs"]["Rung"]["enum"])
    ladder_faults: list[str] = []
    for name, row in sorted(authority.items()):
        ladder = row.get("ladder")
        if not ladder:
            ladder_faults.append(f"{name}: authority publishes no ladder")
            continue
        if len(set(ladder)) != len(ladder):
            ladder_faults.append(f"{name}: ladder repeats a rung")
        # unresolved-edge is the successor's own relation and has no inherited row.
        if name in inherited and inherited[name]["ladder"] != ladder:
            ladder_faults.append(
                f"{name}: inherited fact-plane ladder {inherited[name]['ladder']} != authority {ladder}")
        if model.LADDERS.get(name) != ladder:
            ladder_faults.append(f"{name}: model LADDERS {model.LADDERS.get(name)} != authority {ladder}")
        if domain_ladders.get(name) != ladder:
            ladder_faults.append(
                f"{name}: RELATION-LADDER-DOMAIN-V2 {domain_ladders.get(name)} != authority {ladder}")
        for rung in ladder:
            if rung not in rung_vocabulary:
                ladder_faults.append(f"{name}: rung {rung} is outside the Rung vocabulary")
        # A rung table entry that is not a ladder rung is a field rule for a rung that cannot occur.
        for rung in row["rungs"]:
            if rung not in ladder:
                ladder_faults.append(f"{name}: rungs table names {rung}, which is not on its ladder")
    for name in sorted(set(inherited) - set(authority)):
        ladder_faults.append(f"{name}: inherited relation absent from the authority")
    for name in sorted(set(domain_ladders) - set(authority)):
        ladder_faults.append(f"{name}: capability registry names a relation the authority does not")
    # Every vocabulary member must belong to exactly one relation's ladder: a rung nobody can carry
    # is a live token with no owner, which is how cross-relation rungs get accepted.
    owners: dict[str, list[str]] = {}
    for name, row in authority.items():
        for rung in row.get("ladder", []):
            owners.setdefault(rung, []).append(name)
    for rung in sorted(rung_vocabulary - set(owners)):
        ladder_faults.append(f"vocabulary rung {rung} belongs to no relation ladder")
    # ---- syntax-only universe: the advertised grammar set and the identity vocabulary agree.
    # native-evidence 1.2 advertises syntax-only over "any file whose extension maps to a bundled
    # grammar". A bundled grammar whose languageId the body-language-version record cannot express
    # would make that advertisement outrun what a clone identity can say, so the two are held equal
    # here rather than by convention.
    foundation_schemas = model.C.parse(
        (FOUNDATION_DIR / "identity-schemas.v2.json").read_bytes())
    body_language_ids = set(
        foundation_schemas["$defs"]["body-language-version"]["properties"]["languageId"]["enum"])
    grammar_language_ids = set(
        model.SCHEMAS["$defs"]["SyntaxGrammarBundleV1"]["properties"]["grammars"]["items"]
        ["properties"]["languageId"]["enum"])
    universe_sets = foundation_schemas["x-opensip-digest-domains"]["domainSets"]
    syntax_binding = universe_sets["native-semantic-universe"][
        "native.semantic-universe.syntax.v2"]["languageVersionBinding"]
    syntax_faults: list[str] = []
    # The descriptor vocabulary must cover EXACTLY what the host bundles. An earlier revision
    # required it to equal the body-language-version enum, which silently excluded the four
    # data/document grammars the host has always bundled and made native-evidence 1.2's
    # "any file whose extension maps to a bundled grammar" unrepresentable for them.
    bundled_language_ids = set(model.BUNDLED_GRAMMARS.values())
    if grammar_language_ids != bundled_language_ids:
        syntax_faults.append(
            f"grammar descriptor languageId enum {sorted(grammar_language_ids)} != "
            f"host BUNDLED_GRAMMARS languages {sorted(bundled_language_ids)}")
    # What IS held equal to the body-language enum is the clone-capable subset. section 6.3 gives
    # body spans and an L1-L3 normalisation table to the code languages only, so a data/document
    # grammar must never be able to enter a clone preimage, and a code language must never be
    # missing from it.
    if not body_language_ids <= bundled_language_ids:
        syntax_faults.append("a clone body language is not a bundled grammar language")
    data_languages = bundled_language_ids - body_language_ids
    if not data_languages:
        syntax_faults.append("no data/document grammar class remains; the distinction was lost")
    # Every bundled suffix belongs to exactly one language, and only code suffixes carry a dialect.
    dialect_suffixes = set(syntax_binding["dialect"]["table"])
    code_suffixes = {s for s, l in model.BUNDLED_GRAMMARS.items() if l in body_language_ids}
    data_suffixes = {s for s, l in model.BUNDLED_GRAMMARS.items() if l in data_languages}
    # Not naive set equality: the dialect table may carry LONGEST-MATCH sub-variants of a bundled
    # suffix (`.d.ts` is ts-declaration and is reached through the bundled `.ts`). So every bundled
    # code suffix must appear, and every dialect entry must resolve to a bundled code suffix.
    for suffix in sorted(code_suffixes - dialect_suffixes):
        syntax_faults.append("bundled code suffix has no grammar dialect variant: " + suffix)
    for suffix in sorted(dialect_suffixes):
        base = max((b for b in model.BUNDLED_GRAMMARS if suffix.endswith(b)), key=len, default=None)
        if base is None or model.BUNDLED_GRAMMARS[base] not in body_language_ids:
            syntax_faults.append("dialect variant resolves to no bundled code grammar: " + suffix)
    if data_suffixes & dialect_suffixes:
        syntax_faults.append(
            "a data/document suffix has a grammar dialect variant, so it could mint a body identity: "
            + ",".join(sorted(data_suffixes & dialect_suffixes)))
    if not set(syntax_binding["bodyLanguages"]) <= body_language_ids:
        syntax_faults.append("syntax universe bodyLanguages outside the languageId enum")
    variants = set(syntax_binding["dialect"]["table"].values())
    if set(syntax_binding["bodyLanguageByVariant"]) != variants:
        syntax_faults.append("bodyLanguageByVariant does not cover exactly the dialect variants")
    if set(syntax_binding["bodyLanguageByVariant"].values()) != set(syntax_binding["bodyLanguages"]):
        syntax_faults.append("bodyLanguageByVariant values are not exactly bodyLanguages")
    # The grammar dialect axis must stay distinct from the compiler ones, or a grammar-parsed body
    # could mint the same identity as a compiler-parsed one.
    compiler_keys = {universe_sets["native-semantic-universe"][d]["languageVersionBinding"]["dialect"]["key"]
                     for d in ("native.semantic-universe.typescript.v2", "native.semantic-universe.rust.v2")}
    if syntax_binding["dialect"]["key"] in compiler_keys:
        syntax_faults.append("syntax dialect key collides with a compiler dialect key")
    if universe_sets["native-context"]["native.context.syntax.v2"]["language"] != "syntax":
        syntax_faults.append("syntax context row language is not `syntax`")
    report["syntaxOnlyUniverse"] = {
        "contextDomain": "native.context.syntax.v2",
        "universeDomain": "native.semantic-universe.syntax.v2",
        "dialectKey": syntax_binding["dialect"]["key"],
        "bundledGrammarLanguages": sorted(bundled_language_ids),
        "cloneBodyIdentityLanguages": sorted(body_language_ids),
        "dataDocumentLanguages": sorted(data_languages),
        "faults": syntax_faults,
    }
    ladder_faults.extend("syntax-only: " + f for f in syntax_faults)

    report["ladderAuthority"] = {
        "authority": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations[].ladder",
        "mirrorsChecked": ["fact-plane.v1 relationRegistry", "native_evidence_model.v2.LADDERS",
                           "capability-manifest-domains.v2 RELATION-LADDER-DOMAIN-V2"],
        "relations": len(authority), "faults": ladder_faults,
        "sharedRungsAcrossRelations": {r: sorted(o) for r, o in sorted(owners.items()) if len(o) > 1},
    }
    open_objects = []
    digest_sites = []
    def walk(x, p):
        if isinstance(x, dict):
            if "x-opensip-digest" in x:
                digest_sites.append({"path": p, **x["x-opensip-digest"]})
            if x.get("type") == "object" and "additionalProperties" not in x:
                open_objects.append(p)
            for k, v in x.items():
                walk(v, p + "/" + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, p + "/" + str(i))
    walk(model.SCHEMAS, "")
    report["schemas"] = {"defs": len(model.SCHEMAS["$defs"]), "openObjects": open_objects}
    digest_law = model.SCHEMAS["x-opensip-digest-law"]
    undeclared_retention = [s["path"] for s in digest_sites if s.get("retention") not in digest_law["retention"]]
    undeclared_representation = [s["path"] for s in digest_sites if s.get("representation") not in digest_law["representations"]]
    report["digestLaw"] = {"annotationSites": len(digest_sites),
                          "undeclaredRetentionSites": undeclared_retention,
                          "undeclaredRepresentationSites": undeclared_representation}

    matrix = model.C.parse(MATRIX_PATH.read_bytes())
    model.validate_native("NativeCapabilityMatrixV2", matrix)
    cells = matrix["cells"]
    modes = {m for m in matrix["languageModes"]}; caps = {c["id"] for c in matrix["capabilities"]}
    covered = {(c["capability"], c["mode"]) for c in cells}
    missing_cells = sorted(f"{c}×{m}" for c in caps for m in modes if (c, m) not in covered)
    # The cell count is DERIVED and held to the exact product, in both directions. A prose count of
    # 60 stood against 66 actual cells; a second hand-maintained counter would only go stale again,
    # so what is maintained is the invariant and the number is reported from it (CB4-ADV-1).
    extra_cells = sorted(f"{c}×{m}" for (c, m) in covered if c not in caps or m not in modes)
    duplicate_cells = sorted(f"{c}×{m}" for (c, m) in covered if
                             sum(1 for x in cells if (x["capability"], x["mode"]) == (c, m)) > 1)
    cell_count_is_the_product = len(cells) == len(caps) * len(modes)
    # The published vocabulary law must not drift from the table it governs.
    law = matrix["capabilityIdLaw"]
    vocabulary_drift = law["members"] != [c["id"] for c in matrix["capabilities"]]
    report["matrix"] = {"cells": len(cells), "capabilities": len(caps), "modes": len(modes), "missingCells": missing_cells,
                        "extraCells": extra_cells, "duplicateCells": duplicate_cells,
                        "cellCountIsTheProduct": cell_count_is_the_product,
                        "capabilityVocabularyDrift": vocabulary_drift,
                        "qualifiedCells": sum(1 for c in cells if c["state"] not in ("SUPPORTED-DESIGN", "UNSUPPORTED-TYPED", "NOT-SELECTED"))}
    cases_doc = model.C.parse(CASES_PATH.read_bytes())
    fixtures = cases_doc.get("fixtures", {})
    results = [run_case(c, model, fixtures) for c in cases_doc["cases"]]
    ids = [r["id"] for r in results]
    if len(ids) != len(set(ids)):
        results.append({"id": "__unique-ids", "passed": False, "faults": ["duplicate case ids"], "kind": "meta", "feedback": []})
    feedback_cov = {}
    for r in results:
        for f in r["feedback"]:
            feedback_cov.setdefault(f, []).append(r["id"])
    passed = sum(1 for r in results if r["passed"])
    report["cases"] = {"total": len(results), "passed": passed, "failed": len(results) - passed,
                       "positive": sum(1 for r in results if r["kind"] == "positive"),
                       "negative": sum(1 for r in results if r["kind"] == "negative"),
                       "feedbackCoverage": {k: sorted(v) for k, v in sorted(feedback_cov.items())},
                       "uncoveredFeedback": sorted((set(f"F{i}" for i in range(1, 13)) | set(f"R{i}" for i in range(1, 8))) - set(feedback_cov)),
                       "results": results}
    ok = (passed == len(results) and not missing_cells and not extra_cells and not duplicate_cells
          and cell_count_is_the_product and not vocabulary_drift and not open_objects
          and not report["cases"]["uncoveredFeedback"] and not ladder_faults
          and not undeclared_retention and not undeclared_representation)
    report["result"] = "PASS" if ok else "FAIL"
    report["limitations"] = [
        "Observation inputs (edges, tokens, vendored file digests, stage terminals) are fixture-asserted, not measured from a compiler or Cargo.",
        "Protocol transitions are a host-side abstract machine; framing, byte limits, OS process death and EOF are not exercised.",
        "Cargo config discovery and rustc flag semantics are pinned to primary documentation read on 2026-09-06; the ancestor-carrier verification is a design rule, not a demonstrated switch.",
        "The tsjs-erasure-v1 projection operates on token kinds supplied by fixtures; a real tokenizer is qualification work.",
        "No cell is QUALIFIED; the four platform families are asserted design-invariant only.",
    ]
    REPORT_PATH.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    for r in results:
        if not r["passed"]:
            print("FAIL", r["id"]); [print("   ", f) for f in r["faults"]]
    for fault in ladder_faults:
        print("FAIL ladder-drift:", fault)
    for path in undeclared_retention + undeclared_representation:
        print("FAIL digest-law vocabulary:", path)
    print(f"{report['result']}: {passed}/{len(results)} cases; matrix cells {len(cells)}; open objects {len(open_objects)}; uncovered feedback {report['cases']['uncoveredFeedback']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# altered
