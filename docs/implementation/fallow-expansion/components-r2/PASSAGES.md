# FX-COMP-1 exact insertion

Parent line2777.

Before:
~~~text
they are composed in §4.5 from manifest, entry points, edges and declared consumers.
~~~
After:
~~~text
they are composed in §4.5 from manifest, entry points, edges and declared consumers.

### Shared original-source extraction model (FX-COMP-1)

The following exact source model is selected for staged Vue/Svelte/Astro/CSS adapter design. It is an extraction intermediate only; existing native capability cells, grammars, public fault routes and facts remain unchanged until their own reviewed adapter successors select a bridge. Its schema, pure reference and fixtures are the candidate members of FX-COMP-1.

## The closed record and its authority

`ComponentSourceModelV1` is the closed record in `component-source-model.schema.json`. It is an independently checkable extraction intermediate, not `fact2`, Coverage, a Run, an imported observation, a new identifier domain or a prepared-output grant. Its `source` names one admitted snapshot regular file by canonical path, raw SHA-256 and exact byte length. `snapshotId` is that admitted source snapshot. `producerClosureId` is the exact retained authenticated closure containing the extractor/parser and its complete dependency/specification bytes; an ambient parser name/version is insufficient.

The record can be constructed and validated by the syntax/adapter layer after source admission. It acquires no authority by being schema-valid. Its canonical SHA-256 may be carried by a later selected stage-input commitment only when that stage's exact successor defines the carrier, retention and admission bridge. Until then, it is design/reference evidence only and cannot enter a current closed Plan/stage/fact record as an undeclared property. The source, any derived blobs, parser closure and mapping specification must be available to reconstruct extraction when a future bridge selects it; a missing blob or closure never permits a complete claim.

The closed formats are `vue`, `svelte`, `astro`, `css`, `typescript`, `javascript`, `rust`. Whole ordinary source files use one `whole` region, with their existing dialect/grammar rules unchanged. The three component formats can carry `container`, `script`, `template`, `style` and `unmapped` regions. CSS uses a `whole` region. Template languages are distinct: `vue-template`, `svelte-template`, `astro-template`; no adapter treats one as another or treats a template as resolved TS/JS solely because expression text resembles it.

## Original byte partition

Regions are in original byte order. `regionId` equals the zero-based ordinal. For a nonempty file, regions partition `[0, byteLength)` exactly: the first starts at0, each next starts at the preceding end, all are nonempty, and the last ends at byteLength. Overlap, duplicate ownership, a gap, out-of-range position or an incorrect original content digest refuses the intermediate. An empty file has exactly zero regions. An extractor represents bytes it cannot classify as `unmapped`, with language `unknown`, state `unsupported` and blocker `unmapped-region`; it never omits them.

Offsets are original bytes, not Unicode code points or UTF-16 code units. A region or mapping endpoint used as a text span must be at a valid UTF-8 boundary. Exact text-span translation rejects a malformed UTF-8 original; its byte inventory remains available for diagnostic accounting and grants no text span. A malformed UTF-8 file is represented by a whole unmapped region with `malformed` state and `malformed-source`, rather than repairing encoding silently. Conversions from a compiler's UTF-16 offsets must be checked against the original or explicitly retained derived buffer before emission. BOMs, newline forms and non-ASCII text are preserved. Neither normalization nor decoder replacement changes source identity.

Classification of delimiters/comments/markup as `container` requires the selected component grammar's rule; it is not a way to hide unknown consumer-bearing bytes. Script language follows an explicit supported `lang` attribute or the selected format's documented default. Unsupported preprocessors stay unavailable; host analysis executes no preprocessor/config to make them complete. Grammar-specific region production is specified and independently tested in each adapter successor; this foundation supplies validation, not an invented parser for every format.

## Derived bytes and maps

A region either uses original bytes directly (`derived: null`) or names a retained derived blob by raw SHA-256/byte length and a complete sequence of mapping segments. Derived segments partition `[0, derived.byteLength)` in order, with nonempty ranges, unless the blob is empty, when the segment list is empty. Each segment is exactly one of:

- `exact`: original source start/end are nonnull and inside this region; lengths match, both endpoint pairs are valid UTF-8 boundaries, and the two byte slices are identical.
- `anchor`: original source start/end are nonnull and inside this region; endpoints are valid UTF-8 boundaries. Bytes and lengths may differ. This is an explanatory original-source anchor only, not token identity, semantic equivalence or repair authority.
- `generated`: both source endpoints are null. It has no original-source citation and cannot become an original fact/repair span.

Source ranges in different derived segments may recur for generated copies, but never make different original regions own the same original bytes. Derived identities do not replace original snapshot identity. A proposed derived span translates to an exact original span only if all intersecting segments are `exact`, both span endpoints translate, and the corresponding original ranges are contiguous and in the same original order. Any anchor/generated segment or discontiguous source result prevents that exact translation. No bounding-box approximation, first-segment pick or guessed filename is allowed.

A source map failing structural/content validation refuses that intermediate. An adapter may emit a separately reconstructed direct-source region with `invalid-source-map` and incomplete state; it may not salvage authoritative mapped facts from a rejected map. A derived schema-valid buffer alone is not authority to call it equivalent source.

## Completeness and consumer relationships

`complete`, `partial`, `unsupported`, `malformed` describe extraction only. A complete region has no blockers. The model's state is `complete` exactly when every region is complete (the empty model is extraction-complete), otherwise `partial`. This never proves resolution-complete, closed exports, complete template consumers, class resolution, reachability non-use or repair eligibility. Only existing or later selected per-relation Coverage can prove those propositions over its full admitted population.

The blocker vocabulary is closed in the schema. Dynamic component selection/class construction, unresolved preprocessors, an unavailable grammar, unsupported syntax, unclassified bytes and config requiring evaluation remain explicit; no empty relation set proves that missing consumers do not exist. An unsupported script/template/style portion that could consume a subject blocks that subject's universal non-use and destructive repair unless a separately selected rule establishes a complete relevant population without excluding the portion.

The native provider retains separate lexical scopes for each script/template construct until its adapter law defines the cross-region binding relation. Framework-generated helper names never become public original symbols by accident. CSS selector references, CSS-in-JS and dynamic class expressions start as separately identified candidates; extraction completeness does not qualify them as resolved references or safe unused-style deletion.

## Admission checks and bounds

Validate the complete JSON shape first against this exact document; enforce unchanged canonical JSON byte/depth rules and current scalar/path/snapshot/closure rules. Then join the source to the admitted snapshot and re-hash bytes, join the producer closure, validate the original partition and format/kind/language compatibility, join/re-hash derived blobs, validate maps, and derive the model state. Bounds: at most65536 regions per file, at most65536 segments per derived region, and canonical intermediate bytes at most4 MiB. Derived/source bytes remain under the selecting stage's existing explicit byte/work bounds; this model grants none of its own file reads. Counts are checked before allocating from an untrusted declaration. A schema maximum does not override the record-byte maximum.

Validation defects are internal intermediate defects. A future producer bridge must supply exact existing/native fault projection before this record can cross an authoritative boundary; this foundation creates no public code or fallback. Reference rejection means not admissible, never a silently partial authoritative record.

## Staged implementation and acceptance

First implement the pure record validator and original/derived span translation with retained reference fixtures. Then each adapter successor selects pinned grammar/compiler closures, complete extraction algorithms and dialect/version scope, source input ownership, capability/fact/Coverage schema bridges, refusal routes, default capability effects and policy eligibility. It recomputes the full-default capacity envelope when it widens the matrix. Recognition registry changes remain separate host-owned changes.

The independently adjudicated cases must cover original-source hashing/partition, empty files, Unicode/BOM/CRLF boundaries, exact/anchor/generated maps, duplicate source copies, cross-segment/discontiguous mapping, malformed/unsupported templates, dynamic components/classes, missing grammar/preprocessor and unresolved cross-region bindings. Semantic and repair positives require adapter-specific consumer-completeness cases, including script used only from a template. This subject grants no adapter or rule qualification.
~~~
