"""U-1..U-4b, U-8 and U-9 unit discovery, file membership and the unit scope descriptor (native-evidence s1.4; security S3).

Source39 (HC-18, HC-19): unit and row order, ordinals, Cargo roots, deepest-workspace folding, excluded units and the row
decision are the published U-4b law; the zero-config syntax-only fallback unit is U-9. One row-decision function serves the
synthetic host derivation and Run-closure enforcement over the RETAINED record (ENUMERATION_MEMBERSHIP_ORDER,
ENUMERATION_MEMBERSHIP_ROW_DERIVATION). The original ported file (forced orders, Cargo roots from every Cargo.toml) is preserved
in preserved/s39-original/ref/membership.py.
"""
import tomllib

import canonical as K

MARKERS = ("Cargo.toml", "package.json", "tsconfig.json", "jsconfig.json")
TSJS_MARKER_PRECEDENCE = ("tsconfig.json", "jsconfig.json", "package.json")
PRUNE_SEGMENTS = {"node_modules": "dependency-tree", ".git": "vcs-tree", ".hg": "vcs-tree", ".svn": "vcs-tree", ".jj": "vcs-tree"}
TSJS_EXT = (".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs", ".jsx")
RUST_EXT = (".rs",)
BUNDLED_GRAMMAR_EXT = RUST_EXT + TSJS_EXT + (".json", ".toml", ".md", ".yaml", ".yml")
FALLBACK_UNIT = {"rootPath": "", "languageFamily": "none", "languageMode": "syntax-only", "unitKind": "syntax-only", "markerPath": "",
                 "markerSha256": None, "recognizerId": "syntax-only-fallback", "recognizerVersion": 1, "provenance": "DEFAULTED",
                 "memberPackageRoots": []}


TSJS_UNIT_KIND = {"ts-tsconfig": "ts-program", "js-allowjs": "js-program", "js-synthesized": "js-program"}


def is_canonical_relative_dir(s):
    """native-evidence.schemas.v2.json#/$defs/CanonicalRelativeDirV1: split on "/", every segment non-empty, not "." or "..",
    no NUL and no backslash; 1..4096 characters."""
    if not isinstance(s, str) or not 1 <= len(s) <= 4096:
        return False
    return all(seg not in ("", ".", "..") and "\x00" not in seg and "\\" not in seg for seg in s.split("/"))


def unit_root_faults(units, key):
    """HC-39 (source41 native U-0 lines 626-651): rootPath is "" or a CanonicalRelativeDirV1 and every memberPackageRoots entry is a
    CanonicalRelativeDirV1; decided before membership, slicing or enumeration binding reads the root."""
    faults = []
    for i, u in enumerate(units if isinstance(units, list) else []):
        u = u if isinstance(u, dict) else {}
        ordinal = u.get("unitOrdinal", i)
        root = u.get("rootPath")
        if not (root == "" or is_canonical_relative_dir(root)):
            faults.append(f"{key}:{ordinal}:rootPath")
        members = u.get("memberPackageRoots")
        if not isinstance(members, list) or not all(is_canonical_relative_dir(m) for m in members):
            faults.append(f"{key}:{ordinal}:memberPackageRoots")
    return faults


def dirname(p):
    return p.rsplit("/", 1)[0] if "/" in p else ""


def join(d, name):
    return (d + "/" if d else "") + name


def under(path, root):
    return root == "" or path == root or path.startswith(root + "/")


def depth(d):
    return 0 if d == "" else d.count("/") + 1


def family_of(path):
    if path.endswith(RUST_EXT):
        return "rust"
    if any(path.endswith(e) for e in TSJS_EXT):
        return "tsjs"
    return "none"


def final_extension(path):
    name = path.rsplit("/", 1)[-1]
    i = name.rfind(".")
    return name[i:] if i >= 0 else ""


def pruned_anchor(path, cargo_roots):
    """Outermost pruned segment of the directory part (U-4a): dependency/VCS trees, and `target` directly under a Cargo root."""
    segs = path.split("/")
    for i, s in enumerate(segs[:-1]):
        if s in PRUNE_SEGMENTS:
            return "/".join(segs[:i + 1]), PRUNE_SEGMENTS[s]
        if s == "target" and "/".join(segs[:i]) in cargo_roots:
            return "/".join(segs[:i + 1]), "cargo-build-output"
    return None


_KIND_LAW = []


def config_node_kind(path):
    """native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law (the exact basename law of TypeScriptConfigGraphV1)."""
    if not _KIND_LAW:
        import schemas
        _KIND_LAW.append(schemas.kit().doc("native/native-evidence.schemas.v2.json")["x-opensip-config-node-kind-law"])
    return _KIND_LAW[0]["basenames"].get(path.split("/")[-1], _KIND_LAW[0]["otherwise"])


def _inherited_js_options(inv_bytes, cfg_path, stack):
    """HC-39 (source41 native s1.2 lines 516-531): a jsconfig-kind node supplies allowJs=true unless it writes allowJs itself; a node's
    own options take precedence over its bases and later extends entries over earlier ones. Returns the inherited {allowJs, checkJs}
    subset; an unresolvable or cyclic base contributes nothing."""
    if cfg_path in stack or cfg_path not in inv_bytes:
        return {}
    data = K.parse_raw(inv_bytes[cfg_path])
    eff = {}
    ext = data.get("extends")
    for b in ([ext] if isinstance(ext, str) else (ext or [])):
        target = b if not b.startswith("./") else (dirname(cfg_path) + "/" + b[2:] if dirname(cfg_path) else b[2:])
        eff.update(_inherited_js_options(inv_bytes, target, stack | {cfg_path}))
    own = {k: v for k, v in data.get("compilerOptions", {}).items() if k in ("allowJs", "checkJs")}
    if config_node_kind(cfg_path) == "jsconfig" and "allowJs" not in own:
        own["allowJs"] = True
    eff.update(own)
    return eff


def effective_allow_js(inv_bytes, cfg_path):
    """After inheritance an allowJs value wins, including false; otherwise allowJs follows the effective checkJs (default false)."""
    eff = _inherited_js_options(inv_bytes, cfg_path, frozenset())
    if "allowJs" in eff:
        return eff["allowJs"] is True
    return eff.get("checkJs") is True


def retained_cargo_roots(units):
    """U-4b.4(b): every rust unit root and every member package root."""
    return {u["rootPath"] for u in units if u["languageFamily"] == "rust"} | {m for u in units for m in u["memberPackageRoots"]}


def discover_units(inv_bytes, boundaries=None, explicit_roots=None):
    boundaries = boundaries or {"nestedRepositories": [], "nestedProjects": [], "custodyExcludedUnits": []}
    anchors = [(a, "nested-repository") for a in boundaries["nestedRepositories"]] + \
              [(a, "nested-project") for a in boundaries["nestedProjects"]] + \
              [(a["path"], "custody-excluded") for a in boundaries["custodyExcludedUnits"]]
    selected = None if explicit_roots is None else set(explicit_roots)
    provenance = "DISCOVERED" if selected is None else "EXPLICIT"
    excluded_units, candidates = [], []
    for p in sorted((p for p in inv_bytes if p.split("/")[-1] in MARKERS), key=lambda s: s.encode()):
        d, marker = dirname(p), p.split("/")[-1]
        if pruned_anchor(p, set()) is not None:  # dependency and VCS trees; Cargo output is decided once roots are known
            continue
        boundary = next(((a, r) for a, r in anchors if under(d, a)), None)
        if boundary is not None:
            excluded_units.append({"path": d, "marker": marker, "reason": boundary[1], "anchor": boundary[0]})
            continue
        candidates.append((d, marker))
    rust_units, cargo_roots = [], set()
    for d in sorted({d for d, m in candidates if m == "Cargo.toml"}, key=lambda s: (depth(s), s.encode())):
        mp = join(d, "Cargo.toml")
        if pruned_anchor(mp, cargo_roots) is not None:
            continue
        enclosing = [u for u in rust_units if u["unitKind"] == "cargo-workspace" and d != u["rootPath"] and under(d, u["rootPath"])]
        if enclosing:
            max(enclosing, key=lambda u: len(u["rootPath"]))["memberPackageRoots"].append(d)
            cargo_roots.add(d)
            continue
        if selected is not None and d not in selected:
            continue
        kind = "cargo-workspace" if "workspace" in tomllib.loads(inv_bytes[mp].decode("utf-8")) else "cargo-package"
        rust_units.append({"rootPath": d, "languageFamily": "rust", "languageMode": "rust-cargo", "unitKind": kind, "markerPath": mp,
                           "markerSha256": K.sha256_hex(inv_bytes[mp]), "recognizerId": kind, "recognizerVersion": 1,
                           "provenance": provenance, "memberPackageRoots": []})
        cargo_roots.add(d)
    tsjs_markers = {}
    for d, m in candidates:
        if m != "Cargo.toml" and pruned_anchor(join(d, m), cargo_roots) is None:
            tsjs_markers.setdefault(d, set()).add(m)
    tsjs_units = []
    for d in sorted(tsjs_markers, key=lambda s: s.encode()):
        if selected is not None and d not in selected:
            continue
        marker = next(m for m in TSJS_MARKER_PRECEDENCE if m in tsjs_markers[d])
        mp = join(d, marker)
        if marker in ("tsconfig.json", "jsconfig.json"):
            # HC-39 (source41 native U-1 lines 654-659): both configuration markers select the mode by the effective s1.2 allowJs
            mode, rid = ("js-allowjs" if effective_allow_js(inv_bytes, mp) else "ts-tsconfig"), "typescript-config"
        else:
            mode, rid = "js-synthesized", "node-package"
        tsjs_units.append({"rootPath": d, "languageFamily": "tsjs", "languageMode": mode,
                           "unitKind": TSJS_UNIT_KIND[mode], "markerPath": mp,
                           "markerSha256": K.sha256_hex(inv_bytes[mp]), "recognizerId": rid, "recognizerVersion": 1,
                           "provenance": provenance, "memberPackageRoots": []})
    units = rust_units + tsjs_units
    if selected is not None:
        for r in sorted(selected, key=lambda s: s.encode()):
            if not any(u["rootPath"] == r for u in units):
                raise K.AdmissionError("native.explicit-root-without-marker", r)
    fallback = selected is None and not units
    if fallback:
        units = [dict(FALLBACK_UNIT)]
    units.sort(key=lambda u: (u["rootPath"].encode(), u["languageFamily"].encode()))
    numbered = []
    for i, u in enumerate(units):
        u = dict(u, memberPackageRoots=sorted(u["memberPackageRoots"], key=lambda s: s.encode()))
        numbered.append(dict({"unitOrdinal": i}, **u))
    pruned = {}
    for p in inv_bytes:
        pa = pruned_anchor(p, cargo_roots)
        if pa:
            pruned[pa] = True
    return {"units": numbered, "fallback": fallback,
            "prunedTrees": [{"path": a, "reason": r, "markerCount": None, "markerCountBasis": "not-enumerated"}
                            for a, r in sorted(pruned, key=lambda t: (t[0].encode(), t[1]))],
            "boundaries": dict(boundaries, excludedUnits=sorted(excluded_units, key=lambda e: (e["path"].encode(), e["marker"]))),
            "cargoDirs": sorted(cargo_roots, key=lambda s: s.encode()), "anchors": anchors}


def derive_row(path, units, cargo_roots):
    """U-4b.4 (b)-(e): (languageFamily, unitOrdinal, membership, reason) for a row not at or below an admitted boundary."""
    fam = family_of(path)
    if pruned_anchor(path, cargo_roots) is not None:
        return fam, None, "syntax-only", "host-ignore-convention"
    if fam == "none":
        if final_extension(path) in BUNDLED_GRAMMAR_EXT:
            return fam, None, "syntax-only", "grammar-only"
        return fam, None, "unsupported-file", "no-bundled-grammar"
    owners = [u for u in units if u["languageFamily"] == fam and (u["rootPath"] == "" or path.startswith(u["rootPath"] + "/"))]
    if not owners:
        return fam, None, "syntax-only", "no-program-unit-for-language"
    return fam, max(owners, key=lambda u: len(u["rootPath"]))["unitOrdinal"], "program-member", "deepest-unit-in-language"


def assign_membership(inv_bytes, discovery):
    units = discovery["units"]
    root_faults = unit_root_faults(units, "NATIVE_UNIT_ROOT_REPRESENTATION")
    if root_faults:
        raise K.AdmissionError(root_faults[0].split(":", 1)[0], root_faults[0].split(":", 1)[1])
    cargo_roots = retained_cargo_roots(units)
    rows = []
    for p in sorted(inv_bytes, key=lambda s: s.encode()):
        boundary = next((r for a, r in discovery["anchors"] if under(p, a)), None)
        if boundary:
            rows.append({"path": p, "languageFamily": family_of(p), "unitOrdinal": None, "membership": "outside-project-boundary", "reason": boundary})
            continue
        fam, ordinal, membership, reason = derive_row(p, units, cargo_roots)
        rows.append({"path": p, "languageFamily": fam, "unitOrdinal": ordinal, "membership": membership, "reason": reason})
    return {"schemaVersion": 1, "units": units, "rows": rows,
            "unsupportedFiles": [r["path"] for r in rows if r["membership"] == "unsupported-file"],
            "outsideBoundaryFiles": [r["path"] for r in rows if r["membership"] == "outside-project-boundary"], "erasedFiles": []}


def membership_order_faults(record, inventory_paths):
    """U-4b.3/U-4b.5 over the retained record: ENUMERATION_MEMBERSHIP_ORDER."""
    faults = []
    units = record["units"]
    keys = [(u["rootPath"].encode(), u["languageFamily"].encode()) for u in units]
    if any(a >= b for a, b in zip(keys, keys[1:])):
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:units")
    if [u["unitOrdinal"] for u in units] != list(range(len(units))):
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:unitOrdinal")
    for u in units:
        roots = [m.encode() for m in u["memberPackageRoots"]]
        if any(a >= b for a, b in zip(roots, roots[1:])):
            faults.append(f"ENUMERATION_MEMBERSHIP_ORDER:memberPackageRoots:{u['unitOrdinal']}")
    # HC-39 (source41 native U-4b.2 lines 755-760, U-4b.5 lines 797-799): a tsjs unitKind is the projection of its mode, and a
    # ts-program/js-program kind on a unit of another family refuses.
    for u in units:
        if u["languageFamily"] == "tsjs":
            if u["unitKind"] != TSJS_UNIT_KIND.get(u["languageMode"]):
                faults.append(f"ENUMERATION_MEMBERSHIP_ORDER:unitKind:{u['unitOrdinal']}")
        elif u["unitKind"] in ("ts-program", "js-program"):
            faults.append(f"ENUMERATION_MEMBERSHIP_ORDER:unitKind-family:{u['unitOrdinal']}")
    paths = [r["path"].encode() for r in record["rows"]]
    if any(a >= b for a, b in zip(paths, paths[1:])):
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:rows")
    if sorted(paths) != sorted(p.encode() for p in inventory_paths):
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:rows-not-one-per-inventory-path")
    if record["unsupportedFiles"] != [r["path"] for r in record["rows"] if r["membership"] == "unsupported-file"]:
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:unsupportedFiles")
    if record["outsideBoundaryFiles"] != [r["path"] for r in record["rows"] if r["membership"] == "outside-project-boundary"]:
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:outsideBoundaryFiles")
    if record["erasedFiles"]:
        faults.append("ENUMERATION_MEMBERSHIP_ORDER:erasedFiles")
    return faults


def membership_row_faults(record):
    """U-4b.4/U-4b.5 over the retained units: ENUMERATION_MEMBERSHIP_ROW_DERIVATION. An outside-project-boundary row is judged on
    its family and null ordinal only (the boundary inventory is security-owned and not retained by the Plan)."""
    units = record["units"]
    cargo_roots = retained_cargo_roots(units)
    faults = []
    for row in record["rows"]:
        p = row["path"]
        if row["membership"] == "outside-project-boundary":
            if row["languageFamily"] != family_of(p) or row["unitOrdinal"] is not None:
                faults.append(f"ENUMERATION_MEMBERSHIP_ROW_DERIVATION:{p}")
            continue
        if (row["languageFamily"], row["unitOrdinal"], row["membership"], row["reason"]) != derive_row(p, units, cargo_roots):
            faults.append(f"ENUMERATION_MEMBERSHIP_ROW_DERIVATION:{p}")
    return faults


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
