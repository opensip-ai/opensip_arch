# TypeScript build bootstrap01 — trial, not selected product scaffold

This trial proposes npm11.13.0 with independent package-lock.json v3 locks for
apps/report, providers/typescript and tools/contracts. The root coordinates lanes;
it does not install a hoisted workspace tree. Root package metadata/membership
wording and final inventory4 need an explicit successor before product scaffolding.
All packages pin Node24.16.0. TypeScript6.0.3 is a provider runtime dependency and
a report/generator development dependency. Browser source uses native DOM modules.
The report build proposes esbuild0.28.2, with platform/browser, module condition,
browser/module/main fields and fixed .js/.mjs/.cjs/.json resolution after tsc emit.
The boundary checker must be qualified against this concrete bundler policy;
its provisional enhanced-resolve policy is not automatically accepted here.

Provisioning used npm install with ignore-scripts, audit=false and fund=false into
three separate packages and an explicit local cache. Fresh isolated01/<lane>
copies contain only that lane's source/configuration/lock. npm ci runs offline,
with scripts disabled and explicit empty user/global configs. Report compiles and
bundles its actual implemented reader/overview/evidence/catalog/history/navigation;
provider compiles a clearly labelled compiler-API fixture; generator loads its
compiler fixture. All commands pass, all locks stay unchanged, and every generated
file matches the initial build byte-for-byte. Report realizes TypeScript/esbuild/
its current darwin-arm64 binary; provider and generator each realize only TypeScript.
All three installations match140 previously pinned TypeScript package members.

The actual1,739,279-byte IIFE bundle passes18 private Chrome checks across32 current
report fixtures plus labelled pagination/hostile-text controls. No external imports
remain in bundle metadata. This is a bundle fixture exposing implemented modules,
not the final report index, complete app, CSP/HTML delivery or source custody. No
product files are written. The provider fixture is not protocol or native analysis.

bootstrap-observed-toolchain.json records Node/npm files and registry metadata;
materialized-closures.json records every realized member/mode/symlink. The exact
esbuild package integrity matches the registry observation and lock. Platform
binary/system loader, offline cache materialization, signed component packaging,
confinement and supported-platform/release qualification are separate. Skipping
install scripts does not sandbox build tools; these are declared trusted build
inputs. The report's Cargo consumer will consume explicit verified assets, not
invoke npm/esbuild or the TS compiler during an ordinary host build.

Independent review is pending. Before selecting this setup: assess TS04's runtime/
dev/tooling policy; compare actual esbuild resolution against the boundary adapter;
bind product tooling exceptions, source inventory, lock paths and bootstrap recipes;
replace build-only fixture entries with final reviewed owners as they are implemented.
Do not copy synthetic fixture paths into the canonical product file inventory.

Documentation consulted: [npm11 ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
for frozen/offline installation controls and [esbuild API](https://esbuild.github.io/api/)
for bundling, explicit resolution settings and build metadata. Observed runs, not
these documents, establish the local results above.
