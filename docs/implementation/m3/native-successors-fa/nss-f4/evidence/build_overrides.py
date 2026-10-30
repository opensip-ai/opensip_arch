"""NSS-F4: build and check the insert-only passage overrides.

Usage: python3 -I -B build_overrides.py --arch <opensip_arch checkout> --product <opensip checkout>
       [--record-root <another arch worktree>]... [--check]

Every `before` is read from its parent at pinned bytes; every override is insert-only; no selector may be bound by
the product lock or by NSS-F1's adopted (not yet bound) overrides. Writes ../overrides.json, or compares with --check.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NE = "docs/v2/contracts/product-v1/native-evidence.md"
IE = "docs/v2/contracts/product-v1/identity-and-evidence.md"
DR103 = "docs/coop/artifacts/component-manifest-schemas.v11.json"
C2PM = "docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/CONTRACT.md"
PINS = {
    NE: (329013, "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"),
    IE: (135448, "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"),
    DR103: (139492, "1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005"),
    C2PM: (13644, "58d285ca4de164465e41ade0c89400aa81a41eeb0acfed4a0de2b57de55fbc63"),
}
NSSF1_OVERRIDES = "/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/nss-f1/overrides.json"
NSSF1_PIN = "723ff2ef53fa6af3b49526770d56885cd62cdaf44e429119dfdfd565ee4cc832"

LINE = {
    (NE, 2839): (
        "the selected signed row's tokens",
        " (for `typescript-semantic` the signed row is the release's one `typescript-semantic.protocol` capability "
        "declaration in its analyzer manifest, and Hello's array is that declaration's token set in ascending UTF-8 "
        "byte order; contract successor NSS-F4)"),
    (NE, 2984): (
        None,
        " **The two descriptors in the M3 closures (contract successor NSS-F4).** `typescript-runtime/identity.json` "
        "is a member of the `kind=toolchain` closure the context's `toolClosure.closureId` names, and "
        "`typescript-provider/identity.json` and the default work-budget profile are members of the selected "
        "`kind=provider` closure; each descriptor digest is over that member's exact bytes. `runtimePayloadSha256` is "
        "`hex(SHA-256(JCS({schemaVersion: 1, files})))`, where `files` holds one `{path, sha256, bytes}` row, "
        "ascending by the UTF-8 bytes of `path`, for each member of the runtime-support inventory: the toolchain-closure "
        "members published here as support files of the runtime itself. It is an explicit selection, never derived "
        "from what the process reads, and it excludes the runtime executable (`executableSha256`), both identity "
        "descriptors, every license notice (`licenseNoticeSha256`), the compiler and standard-library members, and the "
        "worker application's inputs, each of which keeps its own commitment. For M3's only cell, `macos-aarch64` with "
        "the official Node.js build, the inventory is exactly `{etc/openssl.cnf}`, the configuration the launch passes: "
        "the build carries its ICU data and OpenSSL inside the executable. Any other inventory, for another cell or "
        "build (a shared library or an ICU data file), is a successor that names its members; `files` is never "
        "inferred from a directory listing or a trace."),
    (NE, 3175): (
        None,
        " **The artifact members (contract successor NSS-F4).** `runtimeArtifactSha256` is the 64-hex suffix of the "
        "context's `toolClosure.closureId`, the `kind=toolchain` closure that holds the runtime, and "
        "`providerArtifactSha256` is the 64-hex suffix of the `closure2` identity of the selected `kind=provider` "
        "closure, a member of the verified `plan.semanticClosures`. These are explicit successor recipes despite the "
        "retained delivery names (identity-and-evidence §3); at M3 no `ReleaseManifestV1` exists. "
        "`runtimeArtifactId` and `providerArtifactId` keep their constants. The host that mints the universe takes "
        "both values from the admitted closures and refuses, as a host invariant before spawn, a "
        "`providerArtifactSha256` that names no selected provider closure; `bind_typescript_universe` checks the "
        "runtime join against the bound context and refuses "
        "`native.universe-context-field-mismatch:runtimeArtifactSha256`. Neither member is a HelloAck join, and the "
        "worker does not check them."),
    (IE, 272): (
        "from an unverified worker claim.",
        " `TypeScriptSemanticUniverseV2.runtimeArtifactSha256` and `providerArtifactSha256` are, under the same "
        "successor-recipe rule, the 64-hex suffixes of the `closure2` identities of the selected `kind=toolchain` "
        "and `kind=provider` closures (native §9.7; contract successor NSS-F4), never a release-archive digest at "
        "M3."),
    (C2PM, 30): (
        None,
        " Contract successor NSS-F4 makes that selection for TypeScript. An analyzer whose authenticated body "
        "declares the `typescript-semantic.protocol` capability (roleSubprotocol `typescript-semantic`, "
        "subprotocolVersion 2) selects the named analyzer subprotocol `typescript-semantic`, whose only supported "
        "closure major is 2, and the projection's analyzer subprotocol is constructed from that admitted declaration "
        "and nothing else. Every other analyzer, Rust included, still has no selected subprotocol here. The "
        "TypeScript toolchain and stdlib closures declare closure major 1 under the role table above; their "
        "`compatibility.providerProtocol` has no consumer, and NSS-F4 fixes it at 1 so that equal bytes give one "
        "identity."),
}
POINTER = {
    (DR103, "/manifestSchema/fields/9/semantics"): (
        None,
        " M3 native registration (contract successor NSS-F4): for role analyzer the host-registered capabilityIds "
        "also include `typescript-semantic.protocol`, whose declarationData is `{capabilityTokens}` (the native-evidence "
        "§9.1 token set, unique, in any order), and `typescript-semantic.imports`, `.references`, `.calls`, `.types` and "
        "`.reachability`, whose declarationData is `{relation, rung}` with the native capability matrix's pairs; each "
        "carries roleSubprotocol `typescript-semantic` and subprotocolVersion 2. capabilityIds stay unique within a "
        "manifest, and `typescript-semantic.reachability` requires `typescript-semantic.calls`, exactly as the preview "
        "pair does, through the same refusal. The rows stay metadata-only at admission. A TypeScript native session's "
        "selection (SD-2) runs only after the existing parse, shape, body-semantic and closure-admission duties have "
        "admitted the release, and never replaces their refusals (for example C2PM-1's analyzer-declaration "
        "inequality, which both body validators refuse). Among admitted releases it requires exactly one protocol row, "
        "no capability row of another roleSubprotocol or version, and `compatibility.providerProtocol` and "
        "`closureProtocolMajor` both 2; an admitted release that fails this supplies no native selection, which is a "
        "session-selection failure and adds no new manifest refusal."),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pinned(arch, path):
    b = open(os.path.join(arch, path), "rb").read()
    if (len(b), sha(b)) != PINS[path]:
        sys.exit("parent not at its pin: " + path)
    return b


def insert(before, anchor, text):
    if anchor is None:
        return before + text
    if before.count(anchor) != 1:
        sys.exit("anchor not unique: " + anchor)
    i = before.index(anchor) + len(anchor)
    return before[:i] + text + before[i:]


def insert_only(before, after):
    return len(after) > len(before) and any(
        after.startswith(before[:i]) and after.endswith(before[i:]) for i in range(len(before) + 1))


def pointer_get(doc, ptr):
    cur = doc
    for part in ptr.split("/")[1:]:
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def taken(arch, product, roots):
    lock = json.load(open(os.path.join(product, "design-lock.json")))
    out = set()
    for c in lock["contractSuccessors"]:
        rec = c["record"]
        for root in (arch,) + tuple(roots):
            p = os.path.join(root, rec["path"])
            if os.path.exists(p):
                break
        else:
            sys.exit("successor record not found: " + rec["path"])
        raw = open(p, "rb").read()
        if (len(raw), sha(raw)) != (rec["bytes"], rec["sha256"]):
            sys.exit("successor record not at its locked bytes: " + p)
        for o in json.loads(raw).get("passageOverrides", []):
            out.add((o["parent"]["path"], json.dumps(o["selector"], sort_keys=True)))
    raw = open(NSSF1_OVERRIDES, "rb").read()
    if sha(raw) != NSSF1_PIN:
        sys.exit("NSS-F1 overrides not at the adopted bytes")
    for o in json.loads(raw)["passageOverrides"]:
        out.add((o["parent"]["path"], json.dumps(o["selector"], sort_keys=True)))
    return out, len(lock["contractSuccessors"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--record-root", action="append", default=[])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    bound, nlock = taken(a.arch, a.product, a.record_root)
    overrides = []
    for (path, line), (anchor, text) in sorted(LINE.items()):
        before = pinned(a.arch, path).decode("utf-8").splitlines()[line - 1]
        overrides.append({"parent": {"path": path, "bytes": PINS[path][0], "sha256": PINS[path][1]},
                          "selector": {"line": line}, "before": before, "after": insert(before, anchor, text)})
    for (path, ptr), (anchor, text) in POINTER.items():
        before = pointer_get(json.loads(pinned(a.arch, path)), ptr)
        overrides.append({"parent": {"path": path, "bytes": PINS[path][0], "sha256": PINS[path][1]},
                          "selector": {"jsonPointer": ptr}, "before": before, "after": insert(before, anchor, text)})
    for o in overrides:
        key = (o["parent"]["path"], json.dumps(o["selector"], sort_keys=True))
        if key in bound:
            sys.exit("selector already bound or adopted: " + str(key))
        if not insert_only(o["before"], o["after"]):
            sys.exit("not insert-only: " + str(key))
    out = (json.dumps({"schemaVersion": 1, "standing": "NSS-F4 r2 passage overrides (insert-only), for the "
                       "binding's successor.json. Generated by evidence/build_overrides.py.",
                       "passageOverrides": overrides}, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    target = os.path.join(ROOT, "overrides.json")
    print("lock successors:", nlock, "; checked against NSS-F1's adopted overrides too", file=sys.stderr)
    if a.check:
        same = os.path.exists(target) and open(target, "rb").read() == out
        print("MATCHES" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    open(target, "wb").write(out)
    print(json.dumps({"overrides": len(overrides), "sha256": sha(out)}))


if __name__ == "__main__":
    main()
