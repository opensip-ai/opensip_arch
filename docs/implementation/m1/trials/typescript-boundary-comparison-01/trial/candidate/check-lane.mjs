// Trial lane checker: dependency-cruiser owns edge extraction, resolution and
// rule evaluation. supplement.mjs refuses what its documented options cannot
// express. Static declared-input graph only; no runtime purity or closure claim.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { cruise } from 'dependency-cruiser';
import extractTSConfig from 'dependency-cruiser/config-utl/extract-ts-config';
import { supplementalFindings, typescriptVersion } from './supplement.mjs';

const depcruiseRoot = path.resolve(path.dirname(fileURLToPath(import.meta.resolve('dependency-cruiser'))), '../..');
const depcruiseVersion = JSON.parse(fs.readFileSync(path.join(depcruiseRoot, 'package.json'), 'utf8')).version;
const escape = value => value.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&');

export function ruleSet(lane, localPackageNames) {
  const own = '^' + escape(lane.packageRoot) + '/';
  const rules = [
    { name: 'lane-escape', severity: 'error', from: { path: own }, to: { pathNot: `${own}|^node_modules/`, dependencyTypesNot: ['core'], couldNotResolve: false } },
    { name: 'unresolvable', severity: 'error', from: { path: own }, to: { couldNotResolve: true } },
    { name: 'undeclared-external', severity: 'error', from: { path: own }, to: { dependencyTypes: ['npm-no-pkg', 'npm-unknown', 'undetermined'], pathNot: own } },
    { name: 'external-shadows-local-package', severity: 'error', from: {}, to: { path: `^node_modules/(${localPackageNames.map(escape).join('|')})(/|$)` } },
    { name: 'external-reenters-source', severity: 'error', from: { path: '^node_modules/' }, to: { pathNot: '^node_modules/', dependencyTypesNot: ['core'], couldNotResolve: false } },
  ];
  if (lane.browserRoots.length) {
    const browser = lane.browserRoots.map(root => '^' + escape(root)).join('|');
    rules.push({ name: 'browser-imports-node-builtin', severity: 'error', from: { path: browser }, to: { dependencyTypes: ['core'] } });
    rules.push({ name: 'browser-requests-node-types', severity: 'error', from: { path: browser }, to: { path: '^node_modules/@types/node/' } });
  }
  return { forbidden: rules };
}

const RULE_CATEGORY = {
  'lane-escape': 'lane-escape', unresolvable: 'unresolved', 'undeclared-external': 'undeclared-external',
  'external-shadows-local-package': 'local-name-shadow', 'external-reenters-source': 'reentry',
  'browser-imports-node-builtin': 'browser-node', 'browser-requests-node-types': 'browser-node',
};

export async function checkLane({ root, lanes, laneId }) {
  root = fs.realpathSync(root);
  const lane = lanes.lanes[laneId];
  if (!lane) throw new Error('unknown lane ' + laneId);
  const tsconfigPath = path.join(root, lane.tsconfig);
  const own = lane.packageRoot + '/';
  // enhanced-resolve applies one condition set per cruise, so each module-format
  // group is cruised separately for both the runtime and the declaration graph.
  const groups = lane.runtimeGroups.flatMap(g => [
    { graph: 'runtime', name: g.name, files: g.files, conditions: g.conditions, mainFields: ['module', 'main'] },
    { graph: 'type', name: g.name + ':types', files: g.files, conditions: ['types', ...g.conditions], mainFields: ['types', 'typings', 'module', 'main'] },
  ]);
  const refusals = [];
  const graphs = [];
  const modules = [];
  // Without compilerOptions.baseUrl (deprecated in TypeScript 6), depcruise
  // hands tsconfig-paths-webpack-plugin baseUrl "./", which it resolves against
  // process.cwd(). Run from the tsconfig directory so paths match tsc.
  process.chdir(path.dirname(tsconfigPath));
  let tsConfig;
  try { tsConfig = extractTSConfig(tsconfigPath); } catch (error) {
    refusals.push({ source: 'depcruise', category: 'config-invalid', message: error.message.split('\n')[0] });
  }
  for (const group of tsConfig ? groups : []) {
    const options = {
      baseDir: root, validate: true, ruleSet: ruleSet(lane, lanes.localPackageNames),
      tsPreCompilationDeps: group.graph === 'runtime' ? 'specify' : true,
      detectJSDocImports: true, detectProcessBuiltinModuleCalls: true,
      exoticRequireStrings: ['require.resolve', 'module.require'],
      tsConfig: { fileName: tsconfigPath },
      // Follow own sources and materialized externals (for re-entry); never
      // read another package's sources after an escape is already recorded.
      doNotFollow: { path: `^(?!(${escape(own)}|node_modules/))` },
      combinedDependencies: false, preserveSymlinks: false,
      enhancedResolveOptions: { exportsFields: ['exports'], conditionNames: group.conditions, mainFields: group.mainFields },
    };
    let output;
    try {
      // bustTheCache: depcruise 18.3.1 memoizes followable extensions from the
      // first isFollowable call; when that is the .js->.ts retry (TS-only
      // extensions) every .js/.mjs/.cjs target becomes silently unfollowable.
      const result = await cruise(group.files, options, { bustTheCache: true }, { tsConfig });
      output = typeof result.output === 'string' ? JSON.parse(result.output) : result.output;
    } catch (error) {
      refusals.push({ source: 'depcruise', category: 'tool-error', group: group.name, message: error.message.split('\n').filter(Boolean).slice(0, 3).join(' | ') });
      continue;
    }
    const edges = [];
    for (const m of output.modules) {
      modules.push(m);
      if (!m.source.startsWith(own)) continue;
      for (const d of m.dependencies) edges.push({ from: m.source, module: d.module, resolved: d.resolved, dependencyTypes: d.dependencyTypes, couldNotResolve: d.couldNotResolve, preCompilationOnly: d.preCompilationOnly });
    }
    for (const v of output.summary.violations) {
      if (group.graph === 'runtime') {
        // Type-only edges are judged in the type graph with type conditions.
        const matches = output.modules.find(m => m.source === v.from)?.dependencies.filter(d => d.resolved === v.to) ?? [];
        if (matches.length && matches.every(d => d.preCompilationOnly === true)) continue;
      }
      refusals.push({ source: 'depcruise', category: RULE_CATEGORY[v.rule.name] ?? v.rule.name, group: group.name, rule: v.rule.name, from: v.from, to: v.to });
    }
    graphs.push({ graph: group.graph, name: group.name, conditions: group.conditions, files: group.files, edges });
  }
  for (const finding of supplementalFindings({ root, lane, modules })) refusals.push({ source: 'supplement', ...finding });
  return {
    schemaVersion: 1, lane: laneId, passed: refusals.length === 0,
    tools: { dependencyCruiser: depcruiseVersion, typescript: typescriptVersion, node: process.version },
    graphs, refusals,
    sourcePurityQualified: false, dependencyClosureQualified: false,
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const args = Object.fromEntries(process.argv.slice(2).reduce((acc, value, index, all) => (index % 2 ? acc : [...acc, [value, all[index + 1]]]), []));
  for (const key of ['--root', '--lanes', '--lane']) if (!args[key]) { process.stderr.write('missing ' + key + '\n'); process.exit(2); }
  const result = await checkLane({ root: args['--root'], lanes: JSON.parse(fs.readFileSync(args['--lanes'], 'utf8')), laneId: args['--lane'] });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  process.exitCode = result.passed ? 0 : 1;
}
