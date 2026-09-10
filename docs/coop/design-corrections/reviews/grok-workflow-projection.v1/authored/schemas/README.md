# Isolated evaluator3 workflow schemas

Closed self-contained version-dispatch copies. Unique `$id` namespace
`urn:opensip:product-v1:workflows:evaluator3:*`. Internal refs rewritten to that
namespace. Foreign unchanged owners remain:

- `urn:opensip:product-v1:workflows:policy-document` — ScopeDocumentV1, WaiverSetV1, EvidenceUse, Rung
- `urn:opensip:product-v1:policy-document:2` — PolicyDocumentV2 embed in baseline
- `urn:opensip:product-v1:workflows:imported-evidence` — import kinds/payloads

Output prefixes are exact `run3` / `evidence3` / `finding3`. Fingerprint remains
`finding-key2`. Mixed output-major patterns are refused. Historical baseline/comparison
schemaMajor 1 is not admitted by empty-array coercion.

Standing: isolated successor. Not frozen/live/product. Root retains workflow1 checks.
