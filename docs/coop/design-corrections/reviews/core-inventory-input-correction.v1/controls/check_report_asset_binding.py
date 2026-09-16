#!/usr/bin/env python3
"""Structural and join control for the PS-04 correction.

Checks the authored report-asset binding companion against frozen candidate25
and the working planning inputs, and executes the pin/manifest admission rules
over positive and negative vectors. This validates design bookkeeping and one
modelled admission path; it is not product code, a browser test, a release
build or qualification.

Usage: check_report_asset_binding.py <work-tree> <candidate25-root>
"""
import hashlib
import json
import sys
from pathlib import Path

IDENTITY = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
D9 = "docs/coop/artifacts/d9-exit-contract.v1.14.json"
COMPONENT = "docs/coop/artifacts/component-manifest-schemas.v11.json"
FAILURES = []


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def load(path):
    return json.loads(Path(path).read_text())


def check_closed_schema(schema, label):
    check(schema.get("additionalProperties") is False, label + ": not closed")
    check(set(schema.get("required", [])) == set(schema.get("properties", {})),
          label + ": required does not equal properties")


# --- modelled admission -----------------------------------------------------

HEX64 = "0123456789abcdef" * 4


def canonical_relative_path(value):
    if not isinstance(value, str) or not value or len(value) > 4096:
        return False
    if value.startswith("/") or value.endswith("/"):
        return False
    if "\\" in value or "\0" in value:
        return False
    if "//" in value:
        return False
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    if "://" in value:
        return False
    return True


def admit_manifest(document, asset_root, roles):
    """Model of ReportAssetManifestV1 admission. Returns a refusal reason or None."""
    if not isinstance(document, dict):
        return "not-an-object"
    if set(document) != {"schemaVersion", "projectionSchemaSha256s", "assets"}:
        return "member-set"
    version = document["schemaVersion"]
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        return "schema-version"
    digests = document["projectionSchemaSha256s"]
    if not isinstance(digests, list) or not digests:
        return "projection-digests-empty"
    if len(set(digests)) != len(digests):
        return "projection-digests-duplicate"
    if digests != sorted(digests):
        return "projection-digests-unsorted"
    for digest in digests:
        if not (isinstance(digest, str) and len(digest) == 64
                and all(c in "0123456789abcdef" for c in digest)):
            return "projection-digest-shape"
    assets = document["assets"]
    if not isinstance(assets, list) or not assets:
        return "assets-empty"
    seen = []
    for row in assets:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "bytes", "role"}:
            return "asset-member-set"
        if not canonical_relative_path(row["path"]):
            return "asset-path-noncanonical"
        if not row["path"].startswith(asset_root + "/"):
            return "asset-path-outside-root"
        if row["role"] not in roles:
            return "asset-role"
        if row["bytes"] is True or row["bytes"] is False:
            return "asset-bytes-boolean"
        if not isinstance(row["bytes"], int) or row["bytes"] < 0:
            return "asset-bytes"
        if not (isinstance(row["sha256"], str) and len(row["sha256"]) == 64
                and all(c in "0123456789abcdef" for c in row["sha256"])):
            return "asset-digest-shape"
        seen.append(row["path"])
    if len(set(seen)) != len(seen):
        return "asset-path-duplicate"
    if seen != sorted(seen):
        return "assets-unsorted"
    return None


def admit_pin(pin, stored_bytes):
    """Model of the load-time pin check: length first, then digest, then parse."""
    if len(stored_bytes) != pin["assetManifestBytes"]:
        return "manifest-length-mismatch"
    if hashlib.sha256(stored_bytes).hexdigest() != pin["assetManifestSha256"]:
        return "manifest-digest-mismatch"
    return None


def good_manifest():
    return {
        "schemaVersion": 1,
        "projectionSchemaSha256s": [HEX64],
        "assets": [
            {"path": "report/app.js", "sha256": HEX64, "bytes": 12, "role": "script"},
            {"path": "report/notice.txt", "sha256": HEX64, "bytes": 3, "role": "notice"},
            {"path": "report/style.css", "sha256": HEX64, "bytes": 7, "role": "style"},
        ],
    }


def run_vectors(roles):
    vectors = []

    def vector(name, mutate, expected):
        document = good_manifest()
        if mutate is not None:
            mutate(document)
        actual = admit_manifest(document, "report", roles)
        ok = (actual == expected)
        vectors.append({"vector": name, "expected": expected,
                        "actual": actual, "ok": ok})
        check(ok, "manifest vector " + name + ": expected " + str(expected)
              + ", got " + str(actual))

    vector("accepts-a-well-formed-manifest", None, None)
    vector("rejects-unsorted-assets",
           lambda d: d["assets"].reverse(), "assets-unsorted")
    vector("rejects-a-duplicate-path",
           lambda d: d["assets"].append(dict(d["assets"][0])),
           "asset-path-duplicate")
    vector("rejects-a-parent-escape",
           lambda d: d["assets"][0].__setitem__("path", "report/../../etc/passwd"),
           "asset-path-noncanonical")
    vector("rejects-an-absolute-path",
           lambda d: d["assets"][0].__setitem__("path", "/report/app.js"),
           "asset-path-noncanonical")
    vector("rejects-a-url",
           lambda d: d["assets"][0].__setitem__("path", "https://cdn/app.js"),
           "asset-path-noncanonical")
    vector("rejects-a-path-outside-the-pinned-root",
           lambda d: d["assets"][0].__setitem__("path", "elsewhere/app.js"),
           "asset-path-outside-root")
    vector("rejects-an-unknown-role",
           lambda d: d["assets"][0].__setitem__("role", "wasm"), "asset-role")
    vector("rejects-an-unknown-member",
           lambda d: d.__setitem__("cdnBase", "x"), "member-set")
    vector("rejects-an-empty-asset-list",
           lambda d: d.__setitem__("assets", []), "assets-empty")
    vector("rejects-an-empty-projection-list",
           lambda d: d.__setitem__("projectionSchemaSha256s", []),
           "projection-digests-empty")
    vector("rejects-a-boolean-byte-length",
           lambda d: d["assets"][0].__setitem__("bytes", True),
           "asset-bytes-boolean")
    vector("rejects-a-short-digest",
           lambda d: d["assets"][0].__setitem__("sha256", "abc"),
           "asset-digest-shape")

    stored = json.dumps(good_manifest(), sort_keys=True).encode()
    pin = {"assetManifestBytes": len(stored),
           "assetManifestSha256": hashlib.sha256(stored).hexdigest()}
    pin_vectors = [
        ("accepts-the-pinned-bytes", stored, None),
        ("rejects-a-truncated-manifest", stored[:-1], "manifest-length-mismatch"),
        ("rejects-an-appended-byte", stored + b" ", "manifest-length-mismatch"),
        ("rejects-equal-length-substituted-bytes",
         stored[:-1] + (b"X" if stored[-1:] != b"X" else b"Y"),
         "manifest-digest-mismatch"),
    ]
    for name, payload, expected in pin_vectors:
        actual = admit_pin(pin, payload)
        ok = (actual == expected)
        vectors.append({"vector": name, "expected": expected,
                        "actual": actual, "ok": ok})
        check(ok, "pin vector " + name + ": expected " + str(expected)
              + ", got " + str(actual))
    return vectors


# --- structural joins -------------------------------------------------------

def structural_checks(companion, identity, d9, component, inventory):
    pin = companion["privateSchemas"]["HostAssetPinV1"]["schema"]
    manifest = companion["privateSchemas"]["ReportAssetManifestV1"]["schema"]
    check_closed_schema(pin, "HostAssetPinV1")
    check_closed_schema(manifest, "ReportAssetManifestV1")
    check(manifest["properties"]["assets"]["items"]
          .get("additionalProperties") is False, "asset row not closed")

    # The withdrawn anchor's facts, re-verified against frozen bytes.
    kinds = identity["$defs"]["closure"]["properties"]["kind"]["enum"]
    check(len(kinds) == 8, "closure2 kind enum is no longer eight members")
    check(not any(k in kinds for k in ("host", "core", "asset", "report")),
          "closure2 kind enum gained a host/asset member")
    check("platform-independent" not in json.dumps(identity),
          "platform-independent vocabulary appeared in identity schemas")
    kind_field = [f for f in component["manifestSchema"]["fields"]
                  if f["name"] == "kind"]
    check(kind_field and "'component'" in kind_field[0]["type"],
          "component manifest kind vocabulary changed")

    # Only existing closed D9 members may be used.
    vocabulary = set(d9["codeVocabulary"]["errorCodes"]) | set(
        d9["codeVocabulary"]["reasonCodes"])
    check(d9["codeVocabulary"]["closed"] is True, "D9 vocabulary is not closed")
    for case in companion["failureBehavior"]["cases"]:
        code = case.get("code")
        if code is not None:
            check(code in vocabulary, "minted D9 code: " + str(code))

    # Named owning modules exist in the planning inventory.
    paths = {row["path"] for row in inventory["files"]}
    named = [companion["privateSchemas"]["HostAssetPinV1"]["owningModule"],
             companion["privateSchemas"]["ReportAssetManifestV1"]["owningModule"],
             companion["loadTimeValidation"]["owner"]]
    for text in named:
        for token in text.replace(";", " ").replace(",", " ").split():
            if token.startswith(("crates/", "apps/", "providers/")):
                check(token in paths, "owning module not in inventory: " + token)

    # The optional-surface row must preserve the underlying aggregate, not reset it.
    optional = [c for c in companion["failureBehavior"]["cases"]
                if c.get("preservesUnderlyingOutcome") is True]
    check(len(optional) == 1, "exactly one optional-surface row must be marked")
    if optional:
        row = optional[0]
        check(row["class"] != "success" and row["exit"] != 0,
              "the optional-surface row must not hard-code success/exit 0")
        check("aggregate" in str(row["class"]).lower(),
              "the optional-surface row must defer to the aggregate termination")
    check(any(a["id"] == "B11" for a in companion["frozenSourceAnchors"]),
          "the aggregate-termination anchor B11 must be cited")
    check("Architecture and release engineering" in companion["anchorSelection"]["whatItDoesNotCover"]["dependencyOwner"] and "DR-101" in companion["anchorSelection"]["whatItDoesNotCover"]["dependencyOwner"],
          "the restored signed CORE inventory must retain its DR-101 architecture/release owner")
    check("not grant-journal carrier work" in companion["anchorSelection"]["whatItDoesNotCover"]["dependencyOwner"],
          "the correction must state the dependency is not the carrier author's work")

    # Manifest self-reference must be resolved by excluding exactly the pinned path.
    self_ref = companion.get("manifestSelfReference")
    check(self_ref is not None, "manifestSelfReference section missing")
    if self_ref:
        rules = json.dumps(self_ref["exactRules"])
        check("MANIFEST_SELF_LISTED" in rules, "self-listing refusal not named")
        check("EXTRA_UNLISTED_FILE" in rules, "completeness refusal not named")
        check("exact path equality" in rules or "exact path" in rules,
              "the exclusion must be by exact path equality")
    check(any("MANIFEST_SELF_LISTED" in r for r in
              companion["privateSchemas"]["ReportAssetManifestV1"]["extraAdmissionRules"]),
          "the manifest schema rules must forbid self-listing")

    # The correction must not reintroduce what it withdrew.
    text = json.dumps(companion)
    check("TreeCommitment" not in companion["anchorSelection"]["statement"],
          "the selected anchor must not depend on a TreeCommitment")
    check("TR-CORE" in text, "the CORE/host owner must be named")
    check("prospective" in json.dumps(
        companion["anchorSelection"]["whatItDoesNotCover"]),
        "the prospective core-release-manifest dependency must be stated")
    prohibited = json.dumps(companion["buildTimeValidation"]["prohibited"]).lower()
    check("package-manager" in prohibited or "package manager" in prohibited,
          "build prohibition missing: ambient package manager")
    check("network" in prohibited, "build prohibition missing: network fetch")
    check("closure2" in prohibited or "producer" in prohibited,
          "build prohibition missing: no producer identity or closure2 kind")


PRECEDENCE = ["success", "indeterminate", "policy-failed",
              "request-rejected", "operational-failed"]
EXIT_OF = {"success": 0, "policy-failed": 1, "request-rejected": 2,
           "indeterminate": 3, "operational-failed": 4, "interrupted": 130}


def aggregate(steps):
    """Frozen law: over REQUIRED steps only; an optional step never changes it."""
    required = [s["class"] for s in steps if s["required"]]
    if not required:
        return "success"
    return max(required, key=PRECEDENCE.index)


def optional_failure_property(d9):
    """An optional asset/surface failure must not reset a nonzero aggregate."""
    rows = []
    for underlying in ("success", "indeterminate", "policy-failed", "operational-failed"):
        before = aggregate([{"class": underlying, "required": True}])
        after = aggregate([{"class": underlying, "required": True},
                           {"class": "operational-failed", "required": False}])
        rows.append({
            "underlyingRequiredClass": underlying,
            "aggregateBefore": before, "exitBefore": EXIT_OF[before],
            "aggregateAfterOptionalAssetFailure": after, "exitAfter": EXIT_OF[after],
            "unchanged": before == after,
            "nonzeroStayedNonzero": (EXIT_OF[before] != 0) == (EXIT_OF[after] != 0),
        })
        check(before == after,
              "optional failure changed the aggregate for " + underlying)
    # The v1 wording would have reset every one of these to success/0.
    would_have_reset = [r["underlyingRequiredClass"] for r in rows if r["exitBefore"] != 0]
    # A REQUIRED asset failure does dominate, by the same precedence.
    required_before = aggregate([{"class": "policy-failed", "required": True}])
    required_after = aggregate([{"class": "policy-failed", "required": True},
                                {"class": "operational-failed", "required": True}])
    check(required_after == "operational-failed",
          "a required delivery fault must dominate policy-failed")
    check(EXIT_OF[required_after] == 4, "required delivery fault must exit 4")
    check(set(EXIT_OF) >= set(PRECEDENCE), "exit table does not cover the precedence set")
    return {"optionalRows": rows,
            "v1WordingWouldHaveResetTheseToZero": would_have_reset,
            "requiredFaultStillDominates": {
                "before": required_before, "exitBefore": EXIT_OF[required_before],
                "after": required_after, "exitAfter": EXIT_OF[required_after]}}


def main():
    work = Path(sys.argv[1])
    c25 = Path(sys.argv[2])
    arch = work / "docs/v2/architecture"
    companion = load(arch / "report-asset-binding.v1.json")
    identity = load(c25 / IDENTITY)
    d9 = load(c25 / D9)
    component = load(c25 / COMPONENT)
    inventory = load(arch / "repository-file-inventory.v1.json")

    structural_checks(companion, identity, d9, component, inventory)
    roles = set(companion["privateSchemas"]["ReportAssetManifestV1"]["schema"]
                ["properties"]["assets"]["items"]["properties"]["role"]["enum"])
    vectors = run_vectors(roles)
    optional_property = optional_failure_property(d9)

    result = {
        "control": "check_report_asset_binding",
        "structuralFailures": FAILURES,
        "vectors": {"count": len(vectors),
                    "passed": sum(1 for v in vectors if v["ok"]),
                    "failed": [v for v in vectors if not v["ok"]]},
        "optionalFailureProperty": optional_property,
        "status": "PASS" if not FAILURES else "FAIL",
        "limits": "Models manifest admission and the pin check only. Establishes no "
                  "browser behaviour, no release build, no signing and no qualification.",
    }
    print(json.dumps(result, indent=1))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
