# Selected runtime profile, candidate 2

This is an implementation trial and a proposed finite pattern compatibility
mapping. It is not generator selection, general JSON Schema support, public API
acceptance, Rust dependency approval or product qualification.

R1 selects the **existing reference pattern behavior** for the exact 66 patterns
in the pinned 28 documents. The owner is the selected foundation `canonical.py`
ExactValidator and its Python `re.search` pattern behavior, consistently with the
explicit historical bare-dollar/end-anchor distinction in product
`identity-and-evidence.md` section 2. We do not silently replace this with native
JavaScript regex semantics. `pattern-profile.json` binds the exact finite source
set and mapping. The root author proposes this scoped implementation choice;
actual Claude review and root assent must select it before product integration.

All engines use Unicode scalar strings. In this profile an unescaped dot outside
a character class excludes LF only. Bare dollar matches at the end or just before
one final LF. The existing absolute `(?![\s\S])` guard remains an exact end guard.
The mapped patterns express those distinctions explicitly for ECMA-262 engines.
Other selected constructs already share the required behavior. No standalone
Unicode shorthand class is selected; `[\s\S]` is the union of complementary sets.
Escaped dots, dollars and character-class members remain literal. The runtime
looks up exact patterns in the generated finite table and refuses new patterns;
this is **not** a general Python regex translator. A changed source/pattern requires
a new table, independent differential and reviewed generator profile.

Python uses original pinned patterns. JS and the Rust conformance probe use the
mapped patterns with Unicode mode. The probe does not select Rust regress as a
production pure-layer dependency. Pattern cases cover every selected pattern and
LF, CR, CRLF, U+2028, U+2029, U+0085, other Unicode and path/identity boundaries.
The raw schemas and accepted historical evidence stay unchanged.

Shape validation does not establish filesystem path safety. Retained path patterns
are not interchangeable with full canonical-path/custody admission: for example,
the historical lookahead using dot still cannot inspect past LF. Host path
admission must independently check every component and selected semantic owner;
these pattern carriers must never authorize opening or following paths. R1's CR,
U+2028 and final-LF cases now agree with the reference, without claiming stronger
historical pattern coverage. Regex wall-clock limits are not established here.

R2 makes `matches` evaluate a private parsed snapshot of canonical bytes. Canonical
arrays must have the ordinary Array prototype; subclasses/custom prototypes refuse.
Objects may have ordinary or null prototype and enumerable data properties only.
The byte API requires this realm's Uint8Array and rejects SharedArrayBuffer-backed
views. The inert-value API assumes trusted builtins and excludes native Proxies and
concurrent mutation. Proxy traps can run during serialization; no effect-free claim
applies to those inputs. A Proxy changing ordinary Get cannot change the subsequent
owned value. Parse repository/provider bytes first instead of accepting native
objects from untrusted code. This matches the existing trusted-native-code boundary.

A1 now returns invalid shape for malformed ordering keys, with exact string/integer
types per annotation, including under `not` and applicators. A2 adds selected
keyword operand validation; unsupported number types and patterns refuse. A4 has
an executable metadata differential against the accepted v2 reference adapter.
A3's nonproductive cycles still yield ShapeLimit; A5's unmetered canonical/regex
work remains bounded by data/profile size but not a hard time budget. These are
carried limitations, not claims of complete schema or resource-policy validation.
