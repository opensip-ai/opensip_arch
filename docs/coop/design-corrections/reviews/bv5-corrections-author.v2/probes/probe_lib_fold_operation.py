"""CX-BV5-01 control: the published `fold` is the operation the admission actually performs.

The correction names `fold` as Unicode Default Case Conversion `toLowercase(X)` - full,
non-tailored, context-sensitive - bound to a declared case-data version. This probe measures the
three discriminators that separate it from the two operations it is NOT, checks that the published
table matches the measurement, and re-runs the MUST-2 join through the host admission so the rename
to `lib_name_fold` is shown to change no admitted outcome.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_lib_fold_operation.py <work-root>
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
NATIVE = ROOT / "docs/coop/design-corrections/native"
spec = importlib.util.spec_from_file_location("nm", NATIVE / "native_evidence_model.v2.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
FX = json.loads((NATIVE / "native-cases.v2.json").read_text(encoding="utf-8"))["fixtures"]
SCHEMAS = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
MD = (ROOT / "docs/v2/contracts/product-v1/native-evidence.md").read_text(encoding="utf-8")

out = {"probe": "lib-name-fold-operation",
       "runtime": {"python": sys.version.split()[0], "unicodedata": unicodedata.unidata_version},
       "declaredCaseDataVersion": N.UNICODE_CASE_DATA_VERSION,
       "agreement": N.unicode_case_data_agreement(),
       "measurements": [], "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


def cps(s):
    return " ".join("U+%04X" % ord(c) for c in s)


# `unicodedata` exposes no simple-lowercase table, so the simple mapping is stated from UnicodeData
# field 13 for the exact characters under test and cited as such, rather than silently synthesised.
SIMPLE_LOWERCASE = {"İ": "i",      # UnicodeData.txt 0130 field 13 -> 0069
                    "Σ": "σ",      # sigma has ONE simple mapping, position-independent
                    "ß": "ß"}


def simple(s):
    return "".join(SIMPLE_LOWERCASE.get(c, c.lower() if len(c.lower()) == 1 else c) for c in s)


for label, src in [("U+0130 LATIN CAPITAL LETTER I WITH DOT ABOVE", "İ"),
                   ("GREEK sigma in FINAL position", "ΟΣ"),
                   ("GREEK sigma NOT final", "ΣΟ"),
                   ("U+00DF LATIN SMALL LETTER SHARP S", "ß"),
                   ("ASCII ES2022 (the live vocabulary shape)", "ES2022")]:
    out["measurements"].append({"name": label, "input": cps(src),
                                "fold (published operation)": cps(N.lib_name_fold(src)),
                                "foldCodePoints": len(N.lib_name_fold(src)),
                                "simple lowercase": cps(simple(src)),
                                "case folding": cps(src.casefold())})

# --- the three discriminators, each asserted against the measurement -------------------------
check("fold is FULL, not simple: U+0130 folds to TWO code points via SpecialCasing",
      N.lib_name_fold("İ") == "i̇" and simple("İ") == "i",
      fold=cps(N.lib_name_fold("İ")), simple=cps(simple("İ")))
check("fold is CONTEXT-SENSITIVE: sigma folds differently in final and non-final position",
      N.lib_name_fold("ΟΣ")[-1] == "ς" and N.lib_name_fold("ΣΟ")[0] == "σ",
      final=cps(N.lib_name_fold("ΟΣ")), nonFinal=cps(N.lib_name_fold("ΣΟ")))
check("fold is NOT case folding: sharp s is unchanged where casefold gives ss",
      N.lib_name_fold("ß") == "ß" and "ß".casefold() == "ss",
      fold=cps(N.lib_name_fold("ß")), casefold=cps("ß".casefold()))
check("all three operations coincide on the live ASCII vocabulary",
      N.lib_name_fold("ES2022") == simple("ES2022").lower() == "ES2022".casefold() == "es2022")

# --- the published prose matches the measurement ---------------------------------------------
check("native section 2.4 no longer calls the fold 'simple lowercase'",
      "Unicode simple lowercase mapping" not in MD)
check("native section 2.4 publishes the operation by name",
      "Default Case Conversion `toLowercase(X)`" in MD and "non-tailored" in MD
      and "context-sensitive" in MD)
for token in ["`U+0069 U+0307`", "`U+03BF U+03C2`", "`U+0073 U+0073`"]:
    check("the published discriminator table carries " + token, token in MD)
check("the published table's U+0130 row matches the measured fold",
      cps(N.lib_name_fold("İ")) == "U+0069 U+0307")
check("version custody is published, with the declared version named",
      "UNICODE_CASE_DATA_VERSION" in MD and N.UNICODE_CASE_DATA_VERSION in MD)
check("the portability consequence is stated, not claimed away",
      "does **not** claim the fold is invariant across every runtime" in MD)
check("no ASCII narrowing was introduced: libSelection items are still unrestricted strings",
      "pattern" not in SCHEMAS["$defs"]["TypeScriptToolchainIdentityV1"]["properties"]["libSelection"]["items"]
      and SCHEMAS["$defs"]["TypeScriptToolchainIdentityV1"]["properties"]["libSelection"]["items"]["type"]
      == "string")
check("no locale delegation: the fold takes no locale argument",
      N.lib_name_fold.__code__.co_argcount == 1)

# --- MUST-2 still holds through the host admission, unchanged by the rename -------------------
base = copy.deepcopy(FX["tsNativeContext"])
a = N.admit_native_context("typescript", base, FX["tsClosureTrees"])
check("the accepted TypeScript context still admits after the fold was named",
      a["refusals"] == [], refusals=a["refusals"], nativeContextId=a["nativeContextId"])
check("its identity is unchanged from the accepted case expectation",
      a["nativeContextId"] == "sha256:8ddb79348a7511abcd457553f20f7e9d446088b1375da32d06eecf1b69875f61",
      nativeContextId=a["nativeContextId"])
components = [r["component"] for r in base["toolchain"]["standardLibraryComponentDigests"]]
check("every selected name still maps into the retained component set under the named fold",
      all("lib." + N.lib_name_fold(n) + ".d.ts" in components
          for n in base["toolchain"]["libSelection"]),
      libSelection=base["toolchain"]["libSelection"], components=components)
missing = copy.deepcopy(base)
missing["toolchain"]["libSelection"] = sorted(base["toolchain"]["libSelection"] + ["es2023"],
                                              key=lambda x: x.encode())
missing["configProjection"]["honoredOptions"]["lib"] = list(missing["toolchain"]["libSelection"])
r = N.admit_native_context("typescript", missing, FX["tsClosureTrees"])
check("an unretained selected lib still refuses through the named fold",
      r["refusals"] == ["native.native-context-lib-not-retained:es2023"], refusals=r["refusals"])

# --- the declared version binding is EFFECTIVE, not merely reported -------------------------
check("a distinct reference-environment error type exists and is NOT an AdmissionError",
      issubclass(N.ReferenceEnvironmentError, Exception)
      and not issubclass(N.ReferenceEnvironmentError, N.AdmissionError),
      mro=[c.__name__ for c in N.ReferenceEnvironmentError.__mro__])
check("the fold itself gates on the declared case data, rather than only reporting it",
      "UNICODE_CASE_DATA_VERSION" in N.lib_name_fold.__code__.co_names
      or "ReferenceEnvironmentError" in N.lib_name_fold.__code__.co_names,
      names=list(N.lib_name_fold.__code__.co_names))
saved = N.unicodedata.unidata_version
try:
    class _Shim:
        unidata_version = "14.0.0"
        def __getattr__(self, item):
            import unicodedata as u
            return getattr(u, item)
    N.unicodedata = _Shim()
    try:
        N.lib_name_fold("ES2022")
        raised = None
    except Exception as exc:
        raised = exc
    check("under different case data the fold REFUSES to produce a result",
          isinstance(raised, N.ReferenceEnvironmentError),
          raisedType=type(raised).__name__ if raised else None,
          message=str(raised)[:160] if raised else None)
    check("that refusal is an environment fault, NOT an ordinary lib-selection AdmissionError",
          raised is not None and not isinstance(raised, N.AdmissionError))
finally:
    import unicodedata as _u
    N.unicodedata = _u
check("the fold works again once the declared case data is restored",
      N.lib_name_fold("ES2022") == "es2022" and N.unicodedata.unidata_version == saved)

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1, ensure_ascii=False))
sys.exit(0 if out["ok"] else 1)
