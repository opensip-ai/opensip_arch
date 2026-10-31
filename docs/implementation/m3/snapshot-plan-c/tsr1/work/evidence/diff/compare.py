"""TSR1-C27 asserting comparison (TSR1-R2-NB-2): TSR-1 reference vs TypeScript 6.0.3, exit 1 on any undeclared mismatch.

Usage: python3 -I compare.py oracle.json ref.json
Every case must succeed in both (this corpus holds positive cases only), the case sets must be identical, and the only
permitted difference is DECLARED below.
"""
import json, sys
o = json.load(open(sys.argv[1]))["cases"]; r = json.load(open(sys.argv[2]))
FIELDS = ["target", "module", "moduleResolution", "jsx", "strict", "esModuleInterop", "allowSyntheticDefaultImports",
          "resolveJsonModule", "allowJs", "checkJs", "skipLibCheck", "types", "customConditions", "lib", "baseUrl",
          "rootDirs", "paths", "programRootFiles"]
DECLARED = {("node16lib", "lib"): {"ts": ["es2015", "es2018.asynciterable", "dom", "es2015"],
                                   "ref": ["es2015", "es2018.asynciterable", "dom"]}}   # R-2.2 de-duplication
fail = []
if set(o) != set(r): fail.append(f"case sets differ: {sorted(set(o) ^ set(r))}")
for name in sorted(set(o) & set(r)):
    if "refusal" in r[name]: fail.append(f"{name}: unexpected reference refusal {r[name]['refusal']}"); continue
    for f in FIELDS:
        a, b = o[name][f], r[name][f]
        if a == b: continue
        d = DECLARED.get((name, f))
        if d and d["ts"] == a and d["ref"] == b: continue
        fail.append(f"{name}: {f}: ts={json.dumps(a, ensure_ascii=False)} ref={json.dumps(b, ensure_ascii=False)}")
for (name, f), d in DECLARED.items():
    if o.get(name, {}).get(f) != d["ts"] or r.get(name, {}).get(f) != d["ref"]: fail.append(f"declared difference {name}.{f} not observed")
print("\n".join(fail) if fail else f"PASS: {len(o)} cases, {len(FIELDS)} fields, 1 declared difference")
sys.exit(1 if fail else 0)
