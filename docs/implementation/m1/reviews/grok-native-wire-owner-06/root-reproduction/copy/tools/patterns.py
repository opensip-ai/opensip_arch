"""Reachable pattern closure and ECMA construct inventory (candidate 03, RF-3).

closure(wire, docs) walks (a) every `pattern` in wire-carriers.v1.json scalars, records and protocols and (b) every
`pattern` reachable from any extern schemaRef the carriers name, following $ref transitively through the pinned
registered schema documents. It skips x-opensip* annotations and literal-valued keywords, and marks a pattern that sits
under an odd number of `not` keywords as negated. A site is {location, pattern, negated, constructs, lower}.

constructs(pattern) lexes with the same grammar as wirecodec.ecma_to_python. `lower` is true when a construct has no
same-meaning spelling in the Rust `regex` crate: lookahead or lookbehind (unsupported there), `.` (Rust excludes only
U+000A, ECMA all four line terminators) and a bare `\\s`/`\\S` (Rust uses Unicode White_Space, which includes U+0085 and
excludes U+FEFF). `[\\s\\S]`, `^` and `$` (no multiline flag in either engine: start/end of input) keep their meaning.
"""
import re


def _esc(s):
    return s.replace("~", "~0").replace("/", "~1")


def constructs(pattern):
    found, i, n = set(), 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "\\":
            e = pattern[i + 1:i + 2]
            if e in ("s", "S"):
                found.add("whitespace-class")
            elif e == "u":
                found.add("unicode-escape")
                i += 6
                continue
            else:
                found.add("escape")
            i += 2
            continue
        if c == "[":
            j = pattern.index("]", i + 1)
            while pattern[j - 1] == "\\" and pattern[j - 2] != "\\":
                j = pattern.index("]", j + 1)
            body = pattern[i + 1:j]
            found.add("any-class" if body == "\\s\\S" else "negated-class" if body.startswith("^") else "class")
            if "\\u" in body:
                found.add("unicode-escape")
            i = j + 1
            continue
        if pattern.startswith("(?=", i) or pattern.startswith("(?!", i):
            found.add("lookahead")
            i += 3
            continue
        if pattern.startswith("(?<=", i) or pattern.startswith("(?<!", i):
            found.add("lookbehind")
            i += 4
            continue
        if pattern.startswith("(?:", i):
            found.add("group")
            i += 3
            continue
        token = {"(": "group", ".": "dot", "$": "end-anchor", "^": "start-anchor", "|": "alternation",
                 "*": "quantifier", "+": "quantifier", "?": "quantifier", "{": "quantifier"}.get(c)
        if token:
            found.add(token)
        i += 1
    return sorted(found)


RUST_LOWERING = {"lookahead", "lookbehind", "dot", "whitespace-class"}


def site(location, pattern, negated=False):
    cs = constructs(pattern)
    return {"location": location, "pattern": pattern, "negated": negated, "constructs": cs, "lower": bool(set(cs) & RUST_LOWERING)}


def closure(wire, docs):
    sites = []

    def walk_wire(o, ptr):
        if isinstance(o, dict):
            if o.get("t") == "text" and "pattern" in o:
                sites.append(site({"document": "wire-carriers.v1.json", "pointer": ptr}, o["pattern"]))
            for k, v in o.items():
                walk_wire(v, ptr + "/" + _esc(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk_wire(v, ptr + "/" + str(i))

    for top in ("scalars", "records", "protocols"):
        walk_wire(wire[top], "#/" + top)
    roots = []

    def collect(o):
        if isinstance(o, dict):
            if o.get("t") == "extern":
                roots.append(o["schemaRef"])
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    collect([wire["records"], wire["protocols"]])
    seen, stack, ext = set(), [], {}
    for r in roots:
        if r not in seen:
            seen.add(r)
            stack.append(r)
    skip = {"description", "examples", "enum", "const", "default", "$comment", "title"}
    while stack:
        ref = stack.pop()
        sid, ptr = ref.split("#", 1)
        node = docs[sid]
        for part in [p for p in ptr.split("/") if p]:
            node = node[part.replace("~1", "/").replace("~0", "~")]

        def scan(o, p, negated):
            if isinstance(o, dict):
                if isinstance(o.get("pattern"), str):
                    ext[(sid, "#" + p if not p.startswith("#") else p, negated)] = o["pattern"]
                for k, v in o.items():
                    if k.startswith("x-opensip") or k in skip:
                        continue
                    if k == "$ref":
                        target = (sid + v) if v.startswith("#") else v
                        if target not in seen:
                            seen.add(target)
                            stack.append(target)
                        continue
                    if k == "properties" and isinstance(v, dict):
                        for pk, pv in v.items():
                            scan(pv, p + "/properties/" + _esc(pk), negated)
                        continue
                    scan(v, p + "/" + _esc(k), negated ^ (k == "not"))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    scan(v, p + "/" + str(i), negated)

        scan(node, ptr, False)
    for (sid, ptr, negated), pat in ext.items():
        sites.append(site({"document": sid, "pointer": ptr}, pat, negated))
    sites.sort(key=lambda s: (s["location"]["document"], s["location"]["pointer"], s["negated"]))
    return {"sites": sites, "externRootsReached": len(seen)}


def path_sites(wire, docs, flags):
    """Closed path-site set (review-03 RF-1): (a) every wire scalar whose text type carries a segment lexical rule;
    (b) every string schema node reachable from the carriers through $ref whose EFFECTIVE ECMA-262 constraint (its
    pattern and a sibling `not` pattern) admits 'a/b' and refuses 'a/../b'. A fixed-form template such as the prepared
    logicalPath does not admit 'a/b' and is therefore not a path site."""
    import wirecodec as W
    sites = []
    for name, sc in wire["scalars"].items():
        lex = sc["type"].get("lexical")
        if lex in ("logical-path-segments", "canonical-path-segments"):
            sites.append({"location": {"document": "wire-carriers.v1.json", "pointer": "#/scalars/" + name + "/type"}, "kind": "wire-lexical-scalar", "lexical": lex})
    roots = []

    def collect(o):
        if isinstance(o, dict):
            if o.get("t") == "extern":
                roots.append(o["schemaRef"])
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    collect([wire["records"], wire["protocols"]])
    seen, stack, found = set(), [], set()
    for r in roots:
        if r not in seen:
            seen.add(r)
            stack.append(r)
    skip = {"description", "examples", "enum", "const", "default", "$comment", "title"}
    while stack:
        ref = stack.pop()
        sid, ptr = ref.split("#", 1)
        node = docs[sid]
        for part in [p for p in ptr.split("/") if p]:
            node = node[part.replace("~1", "/").replace("~0", "~")]

        def scan(o, p):
            if isinstance(o, dict):
                if isinstance(o.get("pattern"), str):
                    neg = o["not"].get("pattern") if isinstance(o.get("not"), dict) else None

                    def ok(s, o=o, neg=neg):
                        return W.ecma_test(o["pattern"], flags, s) and not (neg is not None and W.ecma_test(neg, flags, s))
                    if ok("a/b") and not ok("a/../b"):
                        found.add((sid, p if p.startswith("#") else "#" + p))
                for k, v in o.items():
                    if k.startswith("x-opensip") or k in skip:
                        continue
                    if k == "$ref":
                        target = (sid + v) if v.startswith("#") else v
                        if target not in seen:
                            seen.add(target)
                            stack.append(target)
                        continue
                    if k == "properties" and isinstance(v, dict):
                        for pk, pv in v.items():
                            scan(pv, p + "/properties/" + _esc(pk))
                        continue
                    scan(v, p + "/" + _esc(k))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    scan(v, p + "/" + str(i))

        scan(node, ptr)
    for sid, ptr in sorted(found):
        sites.append({"location": {"document": sid, "pointer": ptr}, "kind": "schema-string"})
    return sites


def site_key(s):
    return (s["location"]["document"], s["location"]["pointer"], s["pattern"], s["negated"])


def pattern_ok_for_translation(pattern, translate):
    try:
        translate(pattern, "u")
        return True
    except Exception:  # noqa: BLE001
        return False


LINE_TERMINATOR_RE = re.compile("[\n\r\u2028\u2029]")
