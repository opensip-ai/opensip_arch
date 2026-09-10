"""CB4-SHOULD-1: clone payload language and body identity must use the SAME selected body
language, including a .js body under the TS engine universe and the Rust selected dialect,
and must never be inferred from the enclosing engine universe."""
import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, probe, emit

DOMS = M.DIGESTS["domainSets"]["native-semantic-universe"]
JOIN = M.RELATIONS["clones"]["bodyIdentityJoin"]
ENUM = M.SCHEMA["$defs"]["body-language-version"]["properties"]["languageId"]["enum"]

# --- 0. The registry sentence itself no longer says "the engine". --------------------------
probe("C0-languageIdSource-names-the-selected-body-language-not-the-engine", "check",
      lambda: "bodyLanguageByVariant" in JOIN["languageIdSource"]
              and "closed-suffix-table" in JOIN["languageIdSource"]
              and "NOT the domain row's own `language`" in JOIN["languageIdIsNotTheProviderLanguage"])
probe("C1-the-closed-languageId-enum-is-unchanged-and-excludes-syntax", "check",
      lambda: sorted(ENUM) == ["javascript", "rust", "typescript"] and "syntax" not in ENUM)

# --- 1. The engine reading is DEMONSTRABLY wrong for the two live cases. -------------------
def engine_language(dom): return DOMS[dom]["language"]
probe("C2-the-engine-reading-would-mint-a-non-member-under-the-syntax-universe", "check",
      lambda: engine_language("native.semantic-universe.syntax.v2") not in ENUM)
probe("C3-the-engine-reading-would-mint-typescript-for-a-js-body", "check",
      lambda: engine_language("native.semantic-universe.typescript.v2") == "typescript")

# --- 2. Every registered universe row carries the derived binding the join now names. ------
def rows_carry_binding():
    for dom, row in DOMS.items():
        b = row.get("languageVersionBinding")
        if not b: return False
        form = b.get("dialect", {}).get("form")
        if form == "closed-suffix-table":
            if not b.get("bodyLanguageByVariant"): return False
            if not set(b["bodyLanguageByVariant"].values()) <= set(ENUM): return False
        elif b.get("bodyLanguage") not in ENUM:
            return False
    return True
probe("C4-every-universe-row-carries-a-derived-body-language-binding-in-the-enum", "check",
      rows_carry_binding)

# --- 3. The DERIVED value, over real anchors, through the candidate's own selector. --------
def derived(dom, path):
    row = DOMS[dom]
    b = row["languageVersionBinding"]
    if b.get("dialect", {}).get("form") == "closed-suffix-table":
        table = b["dialect"]["suffixes"] if "suffixes" in b["dialect"] else b["dialect"].get("table", {})
        variant, best = None, -1
        for suffix, v in table.items():
            if path.endswith(suffix) and len(suffix) > best:
                variant, best = v, len(suffix)
        return b["bodyLanguageByVariant"].get(variant), variant
    return b.get("bodyLanguage"), None

CASES = [
    ("native.semantic-universe.typescript.v2", "a.ts", "typescript"),
    ("native.semantic-universe.typescript.v2", "a.js", "javascript"),
    ("native.semantic-universe.typescript.v2", "a.mjs", "javascript"),
    ("native.semantic-universe.typescript.v2", "a.tsx", "typescript"),
    ("native.semantic-universe.rust.v2", "src/lib.rs", "rust"),
]
for dom, path, want in CASES:
    probe("C5-derived-body-language-%s-under-%s-is-%s"
          % (path.replace("/", "-"), dom.split(".")[-2], want), "check",
          lambda d=dom, p=path, w=want: derived(d, p)[0] == w)

def syntax_never_yields_syntax():
    dom = "native.semantic-universe.syntax.v2"
    vals = set()
    for p in ("a.ts", "a.js", "src/lib.rs", "a.tsx"):
        v = derived(dom, p)[0]
        if v is not None: vals.add(v)
    return bool(vals) and vals <= set(ENUM)
probe("C6-under-the-syntax-universe-every-derived-body-language-is-an-enum-member", "check",
      syntax_never_yields_syntax)

# --- 4. THE JOIN ITSELF, through a complete Run: the payload language and the body identity
#        frame must agree, and a forged frame language must refuse.
probe("C7-positive-a-clones-run-closes-under-the-typescript-universe", "positive",
      lambda: M.close_run(*CI.build(relation="clones", has_match=True, resolved=True)))
probe("C8-positive-a-clones-run-closes-under-the-rust-universe", "positive",
      lambda: M.close_run(*CI.build(relation="clones", has_match=True, resolved=True,
                                    universe_language="rust")))
probe("C9-positive-a-clones-run-closes-under-the-grammar-only-syntax-universe", "positive",
      lambda: M.close_run(*CI.build(relation="clones", has_match=True, resolved=True,
                                    universe_language="syntax", pure_syntax=True)))


# --- 5. The two live cases the finding named, as COMPLETE RUNS over real bodies. -----------
def clone_run(**kw):
    return M.close_run(*CI.build(relation="clones", has_match=True, resolved=True, **kw))
probe("C10-positive-a-js-body-under-the-TYPESCRIPT-engine-universe-closes-a-run", "positive",
      lambda: clone_run(source_path="a.js"))
probe("C11-positive-a-rust-body-under-its-selected-target-edition-closes-a-run", "positive",
      lambda: clone_run(universe_language="rust", source_path="src/lib.rs"))
probe("C12-positive-a-rust-body-under-the-GRAMMAR-ONLY-syntax-universe-closes-a-run",
      "positive", lambda: clone_run(universe_language="syntax", pure_syntax=True,
                                    source_path="src/lib.rs"))

def js_body_language_is_javascript_not_typescript():
    """The decisive one: read the frame the Run actually committed and check the language the
    clone identity was minted under, rather than trusting the registry sentence."""
    run, objects, blobs = CI.build(relation="clones", has_match=True, resolved=True,
                                   source_path="a.js")
    fact = next(v for d, v in objects.values() if d == "fact")
    payload = C.parse(blobs[fact["payloadDigest"]])
    frame = blobs[payload["bodyIdentity"].split(":", 1)[1]]
    return b"javascript" in frame and b"typescript" not in frame
probe("C13-the-committed-js-clone-frame-carries-javascript-not-typescript", "check",
      js_body_language_is_javascript_not_typescript)

def syntax_frame_never_says_syntax():
    run, objects, blobs = CI.build(relation="clones", has_match=True, resolved=True,
                                   universe_language="syntax", pure_syntax=True,
                                   source_path="src/lib.rs")
    fact = next(v for d, v in objects.values() if d == "fact")
    payload = C.parse(blobs[fact["payloadDigest"]])
    frame = blobs[payload["bodyIdentity"].split(":", 1)[1]]
    return b"rust" in frame and b"syntax" not in frame
probe("C14-the-committed-syntax-universe-frame-carries-rust-never-syntax", "check",
      syntax_frame_never_says_syntax)

# --- 6. An unlisted suffix REFUSES rather than being folded into a neighbour. --------------
# ATTEMPT 1 asked for this through build(); it surfaced as FIXTURE_NO_ADMISSIBLE_PAYLOAD,
# because the fixture CATCHES the selector's refusal and degrades to a scope-only clones
# fixture. That is the fixture's documented behaviour, not the law's answer, so the selector
# is driven directly - it is the dependency interface the join actually names.
def select(dom, path, language):
    run, objects, blobs = CI.build(relation="declares", has_match=True, resolved=True,
                                   universe_language=language,
                                   pure_syntax=(language == "syntax"))
    universe = next(v for d, v in objects.values() if d == "fact")["sourceUniverse"]
    urec = next(C.parse(raw) for raw in blobs.values()
                if raw.startswith(M.FRAME_PREFIX + dom.encode() + b"\0")) \
        if False else None
    row = DOMS[dom]
    ublob = next(raw for raw in blobs.values()
                 if raw.startswith(M.FRAME_PREFIX + dom.encode() + b"\0"))
    urecord = M.parse_h_frame(ublob, "native-semantic-universe")[1]
    ctx = None
    for raw in blobs.values():
        if raw.startswith(M.FRAME_PREFIX + b"native.context."):
            ctx = M.parse_h_frame(raw, "native-context")[1]
            break
    anchor = {"path": path, "blobDigest": "0" * 64, "startByte": 0, "endByte": 1}
    return M.body_language_version(urecord, ctx, row, anchor)

probe("C15-negative-an-unlisted-suffix-refuses-rather-than-being-folded-in", "negative",
      lambda: select("native.semantic-universe.syntax.v2", "tool/main.py", "syntax"),
      "BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN")
probe("C16-negative-an-unlisted-suffix-refuses-under-the-typescript-universe-too", "negative",
      lambda: select("native.semantic-universe.typescript.v2", "tool/main.py", "typescript"),
      "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN")
probe("C17-positive-a-clones-SCOPE-still-closes-where-no-body-identity-is-admissible",
      "positive", lambda: M.close_run(*CI.build(relation="clones", has_match=False,
                                                resolved=True, universe_language="syntax",
                                                pure_syntax=True, source_path="tool/main.py")))

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-should-1.json",
     {"registeredUniverseDomains": sorted(DOMS)})
