# Owner decisions for the expansion

Status: owner selected FX-D1 A and FX-D2 A on 2026-10-05 by directing execution of the recommended design acceptance programme with Grok2 as partner/reviewer. These are programme-local decisions, not allocated coordinator numbers. Alternatives are retained as decision rationale; exact successors still require independent review and binding.

## FX-D1: whole-workspace capacity

Recommendation: choose a product target of **up to 1,024 selected program units in one coherent analysis**, with the complete selected default capability matrix and cross-unit consumers preserved. This is a design target, not a measured supported configuration. Program units are the native contract's marker/language units, not source files, npm packages or arbitrary directories.

Why this target: the existing scope descriptor already permits 1,024 selected roots. It aligns default analysis expressibility with that envelope instead of adding a second, much lower unit ceiling. The current base contract requests eleven rows per TS unit: 93 fit into 1,024 capability rows; 94 need 1,034. At 1,024 all-TS units the inherited matrix alone needs 11,264 rows. New capabilities increase that quantity, so derive the final bound from the selected matrix and target rather than adopt 11,264 as a permanent constant.

Verification at the recorded baseline: the product's selected identity schema still limits `requestedCapabilities` to 1,024, and none of the 102 selected contract records overrides native lines 4276/4278/4280. The selected `ts-tsconfig` matrix has eleven requestable capabilities. This supports the capacity calculation; it is not a measured product run.

The [serialization spike](evidence/capacity-shapes.json) measured the request-field projection alone. At 1,024 units it is 1,417,243 JSON bytes with 32-byte ASCII roots, 3,940,379 with 256-byte roots, and 47,194,139 with 4,096-byte roots. The canonical reference's 4 MiB bound is therefore independently relevant even if the row bound rises. These are synthetic serialization sizes, not admitted complete records or performance observations. Exact root/path, record, frame and resource envelopes must accompany the target; raising the row limit alone is insufficient.

| Option | Benefit | Cost and risk |
|---|---|---|
| A. Coherent bounded expansion to 1,024 units (recommended) | Preserves one source-bound analysis and existing request concepts; targets the already selected root envelope | Raises coordinated limits; needs byte/work/memory evidence and review of contexts, frames, records and retained compatibility |
| B. Compact request/Plan redesign now | Can remove repetitive unit×capability materialization and improve growth | Broader schema/identity and historical-reader changes; more potential rework during implementation; still requires bounded resources |
| C. Keep current bounds for this release | Least immediate schedule impact | Full defaults still refuse at 94 TS units; narrower requests provide a smaller analysis population |

Owner-selected: A as the goal, with a bounded representation spike deciding whether existing shapes are sufficient or B is necessary. Do not choose a serialization strategy solely from row-count arithmetic. Automatic sharding is not part of A: one scheduler may split computation only after a selected law preserves a single admitted source universe, cross-unit graph and canonical aggregate Coverage.

Before proposing exact numbers, inspect all of these together:

- Root discovery/selection and requested-capability arrays.
- Distinct native contexts, semantic closures and imported-evidence arrays.
- Per-stage keys, stages, relations, frame/response sizes and symbol-census transport.
- Snapshot/Plan/fact record bytes, canonicalization, input inventories and existing S-R/S-B work.
- Total admitted work, scratch/spool bytes, process-tree memory, cancellation and replay cost.

Other axes remain bounded independently. The unit target does not promise unlimited files, dependencies, imports, policy packs or subrepositories. Publish the exact tested multi-axis envelope and typed refusals. Raising admission limits does not constitute performance qualification.

Compatibility: keep historical schema bytes and exact accepted readers; mint new records under selected current schemas. Decide protocol negotiation and versioning from the actual shape/limit changes. Do not assume changing `maxItems` is invisible to schema identity, or mechanically rewrite existing stored digests.

## FX-D2: component languages and framework scope

Recommendation: design a **shared source model for Vue, Svelte, Astro and CSS**, then deliver adapters and recognizers in stages. Include ordinary JS/TS/JSX/TSX in the same source-correspondence model. The first implementation order is chosen from target-repository evidence, not the number of Fallow plugins.

| Option | Benefit | Cost and risk |
|---|---|---|
| A. Shared model, staged delivery (recommended) | Consistent embedded-code/template spans and completeness; avoids per-framework architectural drift | Shared model must be reviewed before adapters; complete support is not immediate |
| B. Recognizers only for this release | Improves static entry-point discovery quickly | Vue/Svelte/Astro template consumers and CSS remain incompletely analyzed |
| C. Complete all adapters before next release | Broad frontend coverage together | Highest schedule impact and largest qualification population |

Under A, first define:

1. Original file identity, embedded regions and lossless byte-span mappings; generated/intermediate bytes never substitute silently for original source.
2. Script/template/style imports, binding and consumer relations; the exact supported framework versions and syntax.
3. Coverage per region and relation, including malformed syntax, dynamic components/classes, preprocessors and config requiring execution.
4. Source-map validation, retained parser/compiler closure identity, replay and change invalidation.
5. Conservative non-use and repair eligibility: an unsupported template or consumer keeps required completeness unavailable.

Next select static recognizers in useful batches (candidate families: Astro, SvelteKit and Nuxt/Vue; Angular/Nest/Electron/React Native follow demonstrated repository need). Recognizer lists and version support remain closed and host-owned. This proposal selects no ambient plugin execution or configuration evaluation.

Parser/grammar choice, framework priorities and delivery dates are implementation/design findings to bring back with evidence. Owner selection of A does not authorize inventing those measurements or claiming full framework support.

## Recorded owner selections

- FX-D1: A (1,024-unit target with coherent bounds).
- FX-D2: A (shared model and staged adapters).

Authority is the owner's explicit direction to execute the immediately preceding recommendation: “okay, do this. you can use grok as your partner for this work and review partner. there is a herdr session named grok2 that can be utilized”. Neither a preselected UI option nor elapsed time supplied a decision.
