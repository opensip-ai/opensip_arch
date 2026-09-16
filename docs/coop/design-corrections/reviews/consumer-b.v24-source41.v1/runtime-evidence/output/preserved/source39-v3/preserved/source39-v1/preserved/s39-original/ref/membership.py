"""U-0..U-8 unit discovery, file membership and the unit scope descriptor (native-evidence s1.4, security S3).

Forced choices (reported in notes/02): unit order = (rootPath UTF-8 bytes, languageFamily), unitOrdinal = index;
rows ordered by path UTF-8 bytes; unsupportedFiles/outsideBoundaryFiles ascending. The kit publishes the
record shape (sequence order) but not these orders, although the canonical record feeds membershipDigest.
"""
import json
import tomllib

import canonical as K

PRUNE_SEGMENTS = {"node_modules": "dependency-tree", ".git": "vcs-tree", ".hg": "vcs-tree", ".svn": "vcs-tree", ".jj": "vcs-tree"}
TSJS_EXT = (".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs", ".jsx")
RUST_EXT = (".rs",)
GRAMMAR_ONLY_EXT = (".json", ".toml", ".md", ".yaml", ".yml")  # data-document bundled grammars (registry)
CODE_GRAMMAR_EXT = TSJS_EXT + RUST_EXT


def dirname(p):
    return p.rsplit("/", 1)[0] if "/" in p else ""


def under(path, root):
    return root == "" or path == root or path.startswith(root + "/")


def family_of(path):
    if path.endswith(RUST_EXT):
        return "rust"
    if any(path.endswith(e) for e in TSJS_EXT):
        return "tsjs"
    return "none"


def cargo_roots_and_units(inv_bytes):
    tomls = sorted(p for p in inv_bytes if p.split("/")[-1] == "Cargo.toml")
    workspaces = []
    for p in tomls:
        data = tomllib.loads(inv_bytes[p].decode("utf-8"))
        if "workspace" in data:
            workspaces.append(dirname(p))
    return tomls, workspaces


def pruned_anchor(path, cargo_dirs):
    segs = path.split("/")
    for i, s in enumerate(segs[:-1]):
        if s in PRUNE_SEGMENTS:
            return "/".join(segs[:i + 1]), PRUNE_SEGMENTS[s]
        if s == "target" and "/".join(segs[:i]) in cargo_dirs:
            return "/".join(segs[:i + 1]), "cargo-build-output"
    return None


def effective_allow_js(inv_bytes, cfg_path, seen=None):
    seen = seen or set()
    if cfg_path in seen or cfg_path not in inv_bytes:
        return None
    seen.add(cfg_path)
    data = K.parse_raw(inv_bytes[cfg_path])
    val = None
    ext = data.get("extends")
    bases = [ext] if isinstance(ext, str) else (ext or [])
    for b in bases:
        target = b if not b.startswith("./") else (dirname(cfg_path) + "/" + b[2:] if dirname(cfg_path) else b[2:])
        v = effective_allow_js(inv_bytes, target, seen)
        if v is not None:
            val = v
    co = data.get("compilerOptions", {})
    if "allowJs" in co:
        val = co["allowJs"]
    return val


def discover_units(inv_bytes, boundaries=None, explicit_roots=None):
    boundaries = boundaries or {"nestedRepositories": [], "nestedProjects": [], "custodyExcludedUnits": []}
    anchors = [(a, "nested-repository") for a in boundaries["nestedRepositories"]] + \
              [(a, "nested-project") for a in boundaries["nestedProjects"]] + \
              [(a["path"], "custody-excluded") for a in boundaries["custodyExcludedUnits"]]
    tomls, workspaces = cargo_roots_and_units(inv_bytes)
    cargo_dirs = {dirname(p) for p in tomls}

    def excluded(p):
        for a, r in anchors:
            if under(p, a):
                return r
        return None

    markers = {}
    pruned = {}
    for p in sorted(inv_bytes):
        pa = pruned_anchor(p, cargo_dirs)
        if pa:
            pruned[pa[0]] = pa[1]
            continue
        if excluded(p):
            continue
        base = p.split("/")[-1]
        if base in ("Cargo.toml", "tsconfig.json", "jsconfig.json", "package.json"):
            markers.setdefault(dirname(p), set()).add(base)
    units = []
    for d in sorted(markers):
        if explicit_roots is not None and d not in explicit_roots:
            continue
        ms = markers[d]
        if "Cargo.toml" in ms:
            ws_parent = [w for w in workspaces if w != d and under(d, w)]
            if not ws_parent:
                is_ws = d in workspaces
                members = sorted(m for m in cargo_dirs if m != d and under(m, d)) if is_ws else []
                units.append({"rootPath": d, "languageFamily": "rust", "languageMode": "rust-cargo",
                              "unitKind": "cargo-workspace" if is_ws else "cargo-package",
                              "markerPath": (d + "/" if d else "") + "Cargo.toml",
                              "markerSha256": K.sha256_hex(inv_bytes[(d + "/" if d else "") + "Cargo.toml"]),
                              "recognizerId": "cargo-workspace" if is_ws else "cargo-package", "recognizerVersion": 1,
                              "provenance": "EXPLICIT" if explicit_roots is not None else "DISCOVERED",
                              "memberPackageRoots": members})
        for marker, mode_fn in (("tsconfig.json", None), ("jsconfig.json", None), ("package.json", None)):
            if marker in ms:
                mp = (d + "/" if d else "") + marker
                if marker == "tsconfig.json":
                    mode = "js-allowjs" if effective_allow_js(inv_bytes, mp) else "ts-tsconfig"
                    kind, rid = ("ts-program", "typescript-config") if mode == "ts-tsconfig" else ("js-program", "typescript-config")
                elif marker == "jsconfig.json":
                    mode, kind, rid = "js-allowjs", "js-program", "typescript-config"
                else:
                    mode, kind, rid = "js-synthesized", "js-program", "node-package"
                units.append({"rootPath": d, "languageFamily": "tsjs", "languageMode": mode, "unitKind": kind,
                              "markerPath": mp, "markerSha256": K.sha256_hex(inv_bytes[mp]), "recognizerId": rid,
                              "recognizerVersion": 1, "provenance": "EXPLICIT" if explicit_roots is not None else "DISCOVERED",
                              "memberPackageRoots": []})
                break
    units.sort(key=lambda u: (u["rootPath"].encode(), u["languageFamily"]))
    for i, u in enumerate(units):
        u_ord = {"unitOrdinal": i}
        u_ord.update(u)
        units[i] = u_ord
    if explicit_roots is not None:
        for r in explicit_roots:
            if not any(u["rootPath"] == r for u in units):
                raise K.AdmissionError("native.explicit-root-without-marker", r)
    return {"units": units, "prunedTrees": [{"path": a, "reason": r, "markerCount": None, "markerCountBasis": "not-enumerated"}
                                            for a, r in sorted(pruned.items())],
            "boundaries": boundaries, "cargoDirs": sorted(cargo_dirs), "anchors": anchors}


def assign_membership(inv_bytes, discovery):
    units = discovery["units"]
    cargo_dirs = set(discovery["cargoDirs"])
    rows, unsupported, outside = [], [], []
    for p in sorted(inv_bytes, key=lambda s: s.encode()):
        fam = family_of(p)
        ex = next((r for a, r in discovery["anchors"] if under(p, a)), None)
        if ex:
            rows.append({"path": p, "languageFamily": fam, "unitOrdinal": None, "membership": "outside-project-boundary", "reason": ex})
            outside.append(p)
            continue
        if pruned_anchor(p, cargo_dirs):
            rows.append({"path": p, "languageFamily": fam, "unitOrdinal": None, "membership": "syntax-only", "reason": "host-ignore-convention"})
            continue
        if fam in ("rust", "tsjs"):
            cands = [u for u in units if u["languageFamily"] == fam and under(p, u["rootPath"])]
            if cands:
                deepest = max(cands, key=lambda u: len(u["rootPath"]))
                rows.append({"path": p, "languageFamily": fam, "unitOrdinal": deepest["unitOrdinal"], "membership": "program-member", "reason": "deepest-unit-in-language"})
            else:
                rows.append({"path": p, "languageFamily": fam, "unitOrdinal": None, "membership": "syntax-only", "reason": "no-program-unit-for-language"})
            continue
        if any(p.endswith(e) for e in GRAMMAR_ONLY_EXT):
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only", "reason": "grammar-only"})
            continue
        rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None, "membership": "unsupported-file", "reason": "no-bundled-grammar"})
        unsupported.append(p)
    return {"schemaVersion": 1, "units": units, "rows": rows, "unsupportedFiles": unsupported,
            "outsideBoundaryFiles": outside, "erasedFiles": []}


def spell_root(r):
    return "." if r == "" else r


def unit_scope_descriptor(discovery, ignore_paths=(), root_selection=None):
    roots = sorted({spell_root(u["rootPath"]) for u in discovery["units"]}) if root_selection is None else sorted(root_selection)
    excl = set(ignore_paths)
    excl |= {t["path"] for t in discovery["prunedTrees"]}
    for u in discovery["units"]:
        pre = (u["rootPath"] + "/") if u["rootPath"] else ""
        excl.add(pre + ".git")
        excl.add(pre + "node_modules")
    for c in discovery["cargoDirs"]:
        excl.add(((c + "/") if c else "") + "target")
    excl |= {a for a, _ in discovery["anchors"]}
    return {"schemaVersion": 2, "workspaceRoots": sorted(roots, key=lambda s: K.C(s)),
            "pathPrefixes": [], "excludedPathPrefixes": sorted(excl, key=lambda s: K.C(s))}


def in_foundation_scope(path, scope):
    """Import/scope-descriptor membership (atom s6): under a workspaceRoots member AND under a pathPrefixes member
    (empty admits all) AND not under excludedPathPrefixes. '.' denotes the project root."""
    roots = ["" if r == "." else r for r in scope["workspaceRoots"]]
    if not any(under(path, r) for r in roots):
        return False
    if scope["pathPrefixes"] and not any(under(path, pp) for pp in scope["pathPrefixes"]):
        return False
    return not any(under(path, e) for e in scope["excludedPathPrefixes"])
