// (F) Selected report-ref facade on the frozen report.ts, transpiled into reviewer scratch.
const fs = require('node:fs'); const path = require('node:path');
const WORK = __dirname; const SUBJECT = '/tmp/opensip-implementation/m1-generator-adapter-subject-03';
const ts = require(path.join(WORK, 'base/tools/contracts/node_modules/typescript'));
const scratch = path.join(WORK, 'facade-scratch'); fs.mkdirSync(scratch, {recursive: true});
const src = fs.readFileSync(path.join(SUBJECT, 'apps/report/src/generated/report.ts'), 'utf8');
const out = ts.transpileModule(src, {compilerOptions: {target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS}});
fs.writeFileSync(path.join(scratch, 'report.cjs'), out.outputText);
const m = require(path.join(scratch, 'report.cjs'));
const options = JSON.parse(fs.readFileSync(path.join(SUBJECT, 'tools/contracts/options.json'), 'utf8'));
const selected = options.entryPoints.map(e => e.ref); const sel = new Set(selected);
const r = {runtimeExports: Object.keys(m).sort(), selectedCount: selected.length};
const reg = m.createReportShapeRegistry();
r.facadeFrozen = Object.isFrozen(reg); r.facadeKeys = Object.keys(reg);
const attempt = (ref) => { try { return 'returned:' + reg.matches(ref, null); } catch (e) { return 'refused:' + e.constructor.name + ':' + e.message; } };
const probes = [...options.deniedRefs, options.deniedRefs[0] + '/properties/protocolMajor', options.deniedRefs[0] + '/'];
// Unselected definitions present in embedded raw schemas.
const reg2 = JSON.parse(fs.readFileSync(path.join(SUBJECT, 'schemas/registry.json'), 'utf8'));
let unselected = [];
for (const row of reg2.sources) {
  const doc = JSON.parse(fs.readFileSync(path.join(SUBJECT, row.sourcePath), 'utf8'));
  for (const k of Object.keys(doc.$defs || {})) { const ref = doc.$id + '#/$defs/' + k; if (!sel.has(ref)) unselected.push(ref); }
  if (!sel.has(doc.$id + '#')) probes.push(doc.$id + '#');
}
r.unselectedDefinitionCount = unselected.length;
probes.push(...unselected.slice(0, 5), 'urn:unregistered#', selected[0] + '/properties', selected[0].replace('#', '#/'));
r.probes = Object.fromEntries(probes.map(p => [p, attempt(p)]));
r.probeAccepted = Object.values(r.probes).filter(v => v.startsWith('returned')).length;
r.allUnselectedRefused = unselected.every(ref => attempt(ref).startsWith('refused'));
r.selectedFirst = attempt(selected[0]);
try { reg.checkEntryPoints(selected); r.checkAllSelected = 'ok'; } catch (e) { r.checkAllSelected = 'refused:' + e.message; }
try { reg.matches = () => true; r.facadeMutation = 'assigned'; } catch (e) { r.facadeMutation = 'threw:' + e.constructor.name; }
r.facadeMutationEffective = reg.matches.toString().includes('=> true');
console.log(JSON.stringify(r, null, 1));
