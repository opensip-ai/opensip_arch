# Browser resolver02 — actual bundler resolver experiment

Proposes sharing explicit browser-options.mjs with the real esbuild0.28.2 build. The first build.resolve API-only experiment matched22/23cases: it did not expose the disabled-module result for browser:false, although the actual build did. Preserved resolve-api-only.mjs/result-api-only.json document this failed assumption.

Current resolve.mjs resolves one request through esbuild's actual scanner and metadata. A tool-owned onLoad supplies the entry request and inert target placeholders; target module bodies are not parsed or executed. Physical file, disabled, external and refusal results are explicit. Query/fragment suffixes remain separate from the resolved physical path; leading#package imports keep normal package-import semantics. Self-imports and same-file suffix instances have separate controls. No dependency/source-tree plugin or JavaScript config is loaded.

All31scoped fixture cases match the real bundle recipe, including8additional package-directory/conditional/wildcard/scoped/null-export/builtin-disable/import-map/suffix cases. Seven controls cover invalid target bodies, self-edge/suffix, remote/inline refusal, invalid mode and disposal. A joint import+require legacy main/module probe selects module.mjs in both independent modes and the actual combined bundle under the explicit mainFields recipe. These measurements are not a proof of all multi-module, alias, loader or parser behavior.

The target body placeholder is intentionally only a resolution probe: invalid source may resolve here and later fail the real build or checker. No full-checker substitution, selected product policy, concurrency/filesystem confinement, arbitrary-import support or host release claim. Esbuild package/lock/materialized closure pins are recorded in external-input-pins.json. Actual network/syscall tracing is not claimed. Full TypeScript checker, bootstrap, isolated npm closure and inventory/source integration plus independent review remain required. The frozen TS05 checker is unchanged and still uses its provisional enhanced-resolve adapter.

Primary API reference: https://esbuild.github.io/plugins/#resolve .
