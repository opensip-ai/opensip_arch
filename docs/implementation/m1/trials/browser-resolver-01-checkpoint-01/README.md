# Browser resolver comparison01 — policy still pending

The explicit esbuild0.28.2 browser recipe is compared with TS boundary04's
provisional enhanced-resolve adapter in23 synthetic fixtures.21 agree: relative
and extensionless JS/MJS/CJS/JSON, extension priority, import/require condition
branches, nested browser condition, main-field/browser mapping, module condition,
private exports, missing files, Node builtins, browser aliases/disabled sources
and package #imports. Two differ: esbuild accepts relative ?query and #fragment
suffixes; the old adapter refuses. This is not full resolver equivalence.

Initial compare.mjs had a computed-property syntax error, preserved separately.
The first corrected probe misclassified the adapter's {core:true,resolved:node:fs}
as a file path; compare02 handles builtin classification before a resolved file.
The Node builtin difference was a probe bug, not a candidate resolver defect.
Original result.json is preserved; result02.json is the corrected23-case result.

Final policy must either support suffixes consistently with an actual bundler
resolver or explicitly reject them as unselected OpenSIP build-input forms. Leading
# package imports already work and must not be accidentally rejected. These rules
are for OpenSIP's build lanes, not the TS/JS repositories OpenSIP analyzes. No
policy change is adopted by this experiment, and no frozen checker was modified.
The actual report bundle's source graph currently has no suffix imports.
