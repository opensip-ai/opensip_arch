"""TSR-1 reference (interpretation evidence; the seed of the model change C2b-1b carries).

Coverage (TSR1-R2-NB-2): the positive configuration projection of §1 (effective honored options, with the refusals it
meets on the way), §2 (lib) and §4 (roots), over an in-memory snapshot {path: text}. It does NOT implement §3's P
admission or strippedOptions, §7's complete refusal order, §5, §6 or the toolchain checks. MB14a's graph is reduced to
relative `extends` specifiers. Paths are project-relative; "" is the project root.

Usage: python3 -I tsr1_ref.py <cases.json> <ts-6.0.3-lib-data.json> <option-table.json> <ts package lib dir>
"""
import json, re, sys

class Refusal(Exception):
    def __init__(self, key, path, member=None):
        super().__init__(key)
        self.key, self.path, self.member = key, path, member
    def subject(self):
        return f"{self.key}:{self.path}" + (f":{self.member}" if self.member is not None else "")

def fold(s):          # NE §2.4 fold; Python's str.lower is the full default lowercase mapping
    return s.lower()

# ---------------------------------------------------------------- JSONC (MB14a reading, reduced)
def jsonc(text):
    """MB14a JSONC: comments and trailing commas removed lexically, never inside strings (TSR1-R2-NB-1)."""
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch == '"':
            j = i + 1
            while text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1]); i = j + 1; continue
        if text.startswith("//", i):
            j = text.find("\n", i); i = n if j < 0 else j; continue
        if text.startswith("/*", i):
            i = text.index("*/", i) + 2; continue
        if ch == ",":
            j = i + 1
            while j < n and (text[j].isspace() or text.startswith("//", j) or text.startswith("/*", j)):
                if text.startswith("//", j):
                    k = text.find("\n", j); j = n if k < 0 else k
                elif text.startswith("/*", j): j = text.index("*/", j) + 2
                else: j += 1
            if j < n and text[j] in "}]": i += 1; continue
        out.append(ch); i += 1
    s = "".join(out)
    return {} if not s.strip() else json.loads(s)

def ecma_keys(obj):   # ECMAScript OrdinaryOwnPropertyKeys: array indices ascending, then insertion order
    idx = [k for k in obj if re.fullmatch(r"0|[1-9][0-9]*", k) and int(k) <= 4294967294]
    return sorted(idx, key=int) + [k for k in obj if k not in idx]

# ---------------------------------------------------------------- paths
def dirname(p): return p.rsplit("/", 1)[0] if "/" in p else ""
def join_norm(base, rest, path_for_refusal, member):
    segs = [s for s in base.split("/") if s] if base else []
    for s in rest.split("/"):
        if s in ("", "."): continue
        if s == "..":
            if not segs: raise Refusal("native.typescript-profile-path-outside-project", path_for_refusal, member)
            segs.pop(); continue
        segs.append(s)
    return "/".join(segs)

ROOTED = re.compile(r"^(/|[A-Za-z]:|[A-Za-z][A-Za-z0-9+.-]*://)")
def rebase(v, node, entry, member, base=None, spec=False):
    key = "native.typescript-profile-spec-malformed" if spec else "native.typescript-profile-option-malformed"
    if any(ord(c) < 0x20 for c in v) or "\\" in v: raise Refusal(key, node, member)
    if v.startswith("${configDir}"):                      # R-1.5 template branch
        return join_norm(dirname(entry), "./" + v[len("${configDir}"):], node, member)
    if v.lower().startswith("${configdir}"): raise Refusal(key, node, member)
    if ROOTED.match(v): raise Refusal("native.typescript-profile-path-outside-project", node, member)
    return join_norm(dirname(node) if base is None else base, v, node, member)

# ---------------------------------------------------------------- graph and inheritance
JSCONFIG_SUPPLY = {"allowJs": True, "allowSyntheticDefaultImports": True, "skipLibCheck": True, "noEmit": True,
                   "maxNodeModuleJsDepth": 2}

class Graph:
    def __init__(self, files, entry):
        self.files, self.entry, self.docs, self.order = files, entry, {}, []
        self._read(entry)
    def _read(self, path):
        if path in self.docs: return
        doc = jsonc(self.files[path]); self.docs[path] = doc; self.order.append(path)
        ext = doc.get("extends"); ext = [] if ext is None else [ext] if isinstance(ext, str) else ext
        doc["__bases"] = []
        for s in ext:
            cand = join_norm(dirname(path), s, path, "extends")
            if not cand.endswith(".json") and cand not in self.files: cand += ".json"
            doc["__bases"].append(cand); self._read(cand)
    def kind(self, p):
        b = p.rsplit("/", 1)[-1]
        return {"tsconfig.json": "tsconfig", "jsconfig.json": "jsconfig"}.get(b, "other")
    def eff(self, path, memo=None):
        memo = {} if memo is None else memo
        if path in memo: return memo[path]
        acc = {}
        for b in self.docs[path]["__bases"]: acc.update(self.eff(b, memo))
        own = {}
        if self.kind(path) == "jsconfig":
            own.update({k: (v, path, True) for k, v in JSCONFIG_SUPPLY.items()})
        for k, v in (self.docs[path].get("compilerOptions") or {}).items():
            own[k] = (v, path, False)
        acc.update(own); memo[path] = acc
        return acc
    def spec(self, path, name):
        doc = self.docs[path]
        if name in doc: return (doc[name], path)
        found = None
        for b in doc["__bases"]:
            r = self.spec(b, name)
            if r is not None: found = r
        return found

# ---------------------------------------------------------------- tables
def load_tables(lib_data, option_table, libdir):
    d = json.load(open(lib_data))
    tlib = {k: f[4:-5] for k, f in d["libMap"]}
    tdef = {}
    for key, val, deff in d["targets"]:
        if key in ("es3", "es6"): continue
        body = re.sub(r"/\*.*?\*/", "", open(f"{libdir}/{deff}", encoding="utf-8").read(), flags=re.S)
        tdef[key] = [re.match(r'/// <reference lib="([^"]+)" />', l).group(1) for l in body.splitlines() if l.startswith("///")]
    return tlib, tdef, json.load(open(option_table))

TARGET = {"es3": None, "es5": "es5", "es6": "es2015", **{f"es{y}": f"es{y}" for y in range(2015, 2026)}, "esnext": "esnext"}
MODULE = {**{k: k for k in "none commonjs amd system umd es2015 es2020 es2022 esnext node16 node18 node20 nodenext preserve".split()}, "es6": "es2015"}
MODRES = {"node": "node10", "node10": "node10", "classic": "classic", "node16": "node16", "nodenext": "nodenext", "bundler": "bundler"}
JSXV = {k: k for k in "preserve react-native react-jsx react-jsxdev react".split()}
TORD = ["es5", "es2015", "es2016", "es2017", "es2018", "es2019", "es2020", "es2021", "es2022", "es2023", "es2024", "es2025", "esnext"]

def enum_val(table, v, node, opt):
    if not isinstance(v, str): raise Refusal("native.typescript-profile-option-malformed", node, opt)
    k = fold(v)
    if k not in table: raise Refusal("native.typescript-profile-option-value-unsupported", node, opt)
    return table[k]

def resolve(files, entry, tables):
    tlib, tdef, otable = tables
    g = Graph(files, entry)
    e = g.eff(entry)
    H = {r["name"] for r in otable if r["class"] == "H"}
    # §7 phase 2 is reduced here to the honored and template checks the cases exercise
    def w(opt): return e.get(opt)
    def boolean(opt, default):
        if opt not in e: return default
        v, node, _ = e[opt]
        if not isinstance(v, bool): raise Refusal("native.typescript-profile-option-malformed", node, opt)
        return v
    t = "es2025"
    if "target" in e:
        cv = enum_val(TARGET, e["target"][0], e["target"][1], "target")
        t = cv if cv is not None else "es2025"            # es3 masks inherited target, then computes as absent
    if "module" in e: m = enum_val(MODULE, e["module"][0], e["module"][1], "module")
    else:
        i = TORD.index(t)
        m = "esnext" if t == "esnext" else "es2022" if i >= TORD.index("es2022") else "es2020" if i >= TORD.index("es2020") else "es2015" if i >= TORD.index("es2015") else "commonjs"
    if "moduleResolution" in e: mr = enum_val(MODRES, e["moduleResolution"][0], e["moduleResolution"][1], "moduleResolution")
    else:
        mr = "classic" if m in ("none", "amd", "umd", "system") else "nodenext" if m == "nodenext" else "node16" if m in ("node16", "node18", "node20") else "bundler"
    jsx = enum_val(JSXV, e["jsx"][0], e["jsx"][1], "jsx") if "jsx" in e else None
    check_js = boolean("checkJs", False)
    allow_js = boolean("allowJs", check_js)
    rjm_default = True if m in ("node20", "nodenext") else (mr == "bundler")
    out = {"target": t, "module": m, "moduleResolution": mr, "jsx": jsx, "strict": boolean("strict", True),
           "esModuleInterop": boolean("esModuleInterop", True),
           "allowSyntheticDefaultImports": boolean("allowSyntheticDefaultImports", True),
           "resolveJsonModule": boolean("resolveJsonModule", rjm_default), "allowJs": allow_js, "checkJs": check_js,
           "skipLibCheck": boolean("skipLibCheck", False)}
    def strlist(opt):
        if opt not in e: return []
        v, node, _ = e[opt]
        if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
            raise Refusal("native.typescript-profile-option-malformed", node, opt)
        r = []
        for x in v:
            if x not in r: r.append(x)
        return r
    out["types"], out["customConditions"] = strlist("types"), strlist("customConditions")
    if "lib" in e:
        v, node, _ = e["lib"]
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v): raise Refusal("native.typescript-profile-option-malformed", node, "lib")
        if not v: raise Refusal("native.typescript-profile-option-value-unsupported", node, "lib")
        lib = []
        for x in v:
            if fold(x) not in tlib: raise Refusal("native.typescript-profile-option-value-unsupported", node, "lib")
            c = tlib[fold(x)]
            if c not in lib: lib.append(c)
    else:
        lib = list(tdef[t])
    out["lib"] = lib
    base_url = None
    if "baseUrl" in e:
        v, node, _ = e["baseUrl"]
        if not isinstance(v, str): raise Refusal("native.typescript-profile-option-malformed", node, "baseUrl")
        base_url = rebase(v, node, entry, "baseUrl")
    out["baseUrl"] = base_url
    rd = []
    if "rootDirs" in e:
        v, node, _ = e["rootDirs"]
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v): raise Refusal("native.typescript-profile-option-malformed", node, "rootDirs")
        for x in v:
            r = rebase(x, node, entry, "rootDirs")
            if r not in rd: rd.append(r)
    out["rootDirs"] = rd
    paths = []
    if "paths" in e:
        v, node, _ = e["paths"]
        if not isinstance(v, dict): raise Refusal("native.typescript-profile-option-malformed", node, "paths")
        base = base_url if base_url is not None else dirname(node)
        for k in ecma_keys(v):
            subs = v[k]
            if not k or k.count("*") > 1 or not isinstance(subs, list) or not subs or not all(isinstance(s, str) and s.count("*") <= 1 for s in subs):
                raise Refusal("native.typescript-profile-option-malformed", node, "paths")
            paths.append({"pattern": k, "substitutions": [rebase(s, node, entry, "paths", base=base) for s in subs]})
    out["paths"] = paths
    out["programRootFiles"] = roots(g, e, files, entry, out)
    return out

# ---------------------------------------------------------------- §4 roots
PKG = "(?!(?:node_modules|bower_components|jspm_packages)(?:/|$))"
FILES = {"single": "(?:[^./]|(?:\\.(?!min\\.js$))?)*", "double": f"(?:/{PKG}[^/.][^/]*)*?"}
EXCL = {"single": "[^/]*", "double": "(?:/.+?)?"}
def u16(s):           # match over UTF-16 code units, as TypeScript's non-Unicode RegExp does
    b = s.encode("utf-16-be")
    return "".join(chr(int.from_bytes(b[i:i + 2], "big")) for i in range(0, len(b), 2))

def subpattern(spec_abs_components, usage):
    comps = list(spec_abs_components)
    last = comps[-1]
    if usage != "exclude" and last == "**": return None
    if not re.search(r"[.*?]", last): comps += ["**", "*"]
    frag = FILES if usage == "files" else EXCL
    sp, written = "", False
    for c in comps:
        if c == "**": sp += frag["double"]
        else:
            if written: sp += "/"
            if usage != "exclude":
                cp = ""
                if c.startswith("*"): cp += "(?:[^./]" + frag["single"] + ")?"; c = c[1:]
                elif c.startswith("?"): cp += "[^./]"; c = c[1:]
                cp += re.sub(r"[^\w\s/]", lambda mm: frag["single"] if mm.group(0) == "*" else "[^/]" if mm.group(0) == "?" else "\\" + mm.group(0), c, flags=re.ASCII)
                if cp != c: sp += PKG
                sp += cp
            else:
                sp += re.sub(r"[^\w\s/]", lambda mm: frag["single"] if mm.group(0) == "*" else "[^/]" if mm.group(0) == "?" else "\\" + mm.group(0), c, flags=re.ASCII)
        written = True
    return sp

def abs_components(p):  # project-relative path -> components under a virtual "/" root
    return [""] + [s for s in p.split("/") if s] if p else [""]

def ext_is(p, e):     # R-4.4: on the rooted subject "/" + path (TSR1-R2-RF-2)
    q = "/" + p
    return len(q) > len(e) and q.endswith(e)
def change_ext(p, e):  # R-4.8 change(), on the rooted subject, mapped back by dropping the leading "/"
    q = "/" + p
    for x in [".d.ts", ".d.mts", ".d.cts", ".mjs", ".mts", ".cjs", ".cts", ".ts", ".js", ".tsx", ".jsx", ".json"]:
        if len(q) >= len(x) and q[len(q) - len(x)] == "." and q.endswith(x): return (q[:-len(x)] + e)[1:]
    return p

def roots(g, e, files, entry, opts):
    E = dirname(entry)
    def get_spec(name):
        r = g.spec(entry, name)
        if r is None: return None
        v, node = r
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v): raise Refusal("native.typescript-profile-spec-malformed", node, name)
        return [(x, node) for x in v]
    fs, inc, exc = get_spec("files"), get_spec("include"), get_spec("exclude")
    if fs is None and inc is None: inc = [("**/*", entry)]
    if exc is None:
        exc = []
        for o in ("outDir", "declarationDir"):
            if o in e and isinstance(e[o][0], str):
                try: exc.append((rebase(e[o][0], e[o][1], entry, o), None))
                except Refusal: pass
    def spec_path(x, node):
        if x.startswith("${configDir}"): return rebase(x, node, entry, "spec", spec=True)
        return rebase(x, node, entry, "spec", spec=True)
    groups = [[".ts", ".tsx", ".d.ts", ".js", ".jsx"], [".cts", ".d.cts", ".cjs"], [".mts", ".d.mts", ".mjs"]] if opts["allowJs"] else [[".ts", ".tsx", ".d.ts"], [".cts", ".d.cts"], [".mts", ".d.mts"]]
    flat = [x for gg in groups for x in gg] + ([".json"] if opts["resolveJsonModule"] else [])
    cand = sorted(p for p in files if not re.search(r"(^|/)(node_modules|\.git)(/|$)", p))
    literal = []
    for x, node in fs or []:
        p = spec_path(x, node)
        if p not in files or not any(ext_is(p, ee) for ee in flat): raise Refusal("native.typescript-profile-root-unsupported", node, x)
        if p not in literal: literal.append(p)
    W, J = [], []
    if inc:
        specs = []
        for x, node in inc:
            if x == "": continue                                  # RF-5: an empty spec contributes nothing
            if re.search(r"(^|/)\*\*/?$", x): raise Refusal("native.typescript-profile-spec-malformed", node, "include")
            specs.append((x, spec_path(x, node)))
        exs = [spec_path(x, node) if node else x for x, node in exc if x != ""]
        inc_re = [re.compile("^" + subpattern(abs_components(p), "files") + "$") for _, p in specs]
        json_re = [re.compile("^" + subpattern(abs_components(p), "files") + "$") for x, p in specs if x.endswith(".json")]
        ex_pats = [subpattern(abs_components(p), "exclude") for p in exs]
        ex_re = re.compile("^(?:" + "|".join(f"(?:{q})" for q in ex_pats) + ")(?:$|/)") if ex_pats else None
        # bases: D(E), then include bases outside it, sorted by UTF-16 code units
        def inc_base(p):
            m = re.search(r"[*?]", p)
            if m: return p[:p.rfind("/", 0, m.start())] if "/" in p[:m.start()] else ""
            last = p.rsplit("/", 1)[-1]
            return p if "." not in last else dirname(p)
        def contains(a, b): return a == "" or b == a or b.startswith(a + "/")
        bases = [E]
        for b in sorted({inc_base(p) for _, p in specs}, key=u16):
            if all(not contains(a, b) for a in bases): bases.append(b)
        visited = set()     # TSR1-R2-RF-1: shared across bases, by canonical snapshot directory
        def dfs(base):
            under = [p for p in cand if contains(base, p) and p != base]
            def walk(d):
                if d in visited: return
                visited.add(d)
                pre = d + "/" if d else ""
                kids = {p[len(pre):].split("/")[0] for p in under if p.startswith(pre)}
                fl = sorted((k for k in kids if pre + k in files), key=u16)
                ds = sorted((k for k in kids if pre + k not in files), key=u16)
                for f in fl: yield pre + f
                for dd in ds: yield from walk(pre + dd)
            yield from walk(base)
        buckets = [[] for _ in specs]
        for b in bases:
            for p in dfs(b):
                a = "/" + p
                if not any(ext_is(p, ee) for ee in flat): continue
                if ex_re and ex_re.match(u16(a)): continue
                for i, r in enumerate(inc_re):
                    if r.match(u16(a)): buckets[i].append(p); break
        for p in [q for bk in buckets for q in bk]:
            if p.endswith(".json"):
                if any(r.match(u16("/" + p)) for r in json_re) and p not in literal and p not in J: J.append(p)
                continue
            gr = next((gg for gg in groups if any(ext_is(p, x) for x in gg)), None)
            if gr is not None:
                higher = False
                for x in gr:
                    if ext_is(p, x) and (x != ".ts" or not ext_is(p, ".d.ts")): break
                    h = change_ext(p, x)
                    if h in literal or h in W:
                        if x == ".d.ts" and (ext_is(p, ".js") or ext_is(p, ".jsx")): continue
                        higher = True; break
                if higher: continue
                for x in reversed(gr):
                    if ext_is(p, x): break
                    lo = change_ext(p, x)
                    if lo in W: W.remove(lo)
            if p not in literal and p not in W: W.append(p)
    return literal + W + J

def main(cases_path, lib_data, option_table, libdir):
    tables = load_tables(lib_data, option_table, libdir)
    out = {}
    for c in json.load(open(cases_path)):
        try: out[c["name"]] = resolve(c["files"], c["entry"], tables)
        except Refusal as r: out[c["name"]] = {"refusal": r.subject()}
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(*sys.argv[1:5])
