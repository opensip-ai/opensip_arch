# Design binding v4 correction candidate02

The live product has accepted candidate01, selecting one inventory3/metadata-v2
unit and no inherited passages. This candidate addresses its review advisories
before selecting further inventory successors. It does not approve new contracts.

Ordered additive inventory and contract histories, exact source/review/assent
joins, immutable parents and stable file-path description inheritance remain.
For v4 only, any parent content that parses as JSON requires JSON Pointer
selectors. Text line selectors remain valid for non-JSON documents. This removes
line/pointer aliasing of a single JSON value, including misleading file suffixes.
Versions1–3 keep their existing reviewed selector behavior.

Inheritance order is lexicographic by parent path then selector JSON. Thus
/files/10/description sorts before /files/2/description. Malformed candidate
paths are refused with a controlled DesignError before hash-map lookup.

Tests retain all38 prior groups and add fully rebound overlay reuse, cycle,
unsupported selectors, ancestor/direct conflicts, competing ancestors, direct
identical suppression, lexicographic ordering, selector alias and compatibility
cases. Independent reviewer fixture construction is explicitly attributed.
This candidate has not yet received independent review. No new product paths,
base approval changes, commits or pushes; no product/release qualification.

The optional --implementation ROOT preflight executes no generator code. After
full design verification, it joins every mapped architecture source to accepted
base/contract candidates, checks exact architecture and implementation bytes,
registry digest/ID and source-map coverage/owner fields. Rebinding a local source
map/registry cannot select unaccepted architecture bytes. It is an explicit
contributor preflight, not an OS execution guard or remote attestation; callers
start from the reviewed developer checkout. Generator closure/options/outputs
still have their separate checks. Six source-binding test groups are included.
