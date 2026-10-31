// TSR-1 r2 interpretation evidence (RF-6): declaration files a 6.0.3 program loads with `lib` omitted vs T-DEF,
// over a confined in-memory host: one non-empty root plus only the pinned package's lib.*.d.ts files.
const ts = require(process.argv[2]); const tdef = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const fs = require('fs'), path = require('path'); const LIB = process.argv[4];
const libFiles = new Map(fs.readdirSync(LIB).filter(f => /^lib\..*\.d\.ts$/.test(f) || f === 'lib.d.ts').map(f => ['/lib/' + f, fs.readFileSync(LIB + '/' + f, 'utf8')]));
const ROOT = '/proj/main.ts', SRC = 'export const x: Array<number> = [1];\n';
const out = {version: ts.version, root: SRC, targets: {}};
for (const [target, libs] of Object.entries(tdef)) {
  const t = ts.targetOptionDeclaration.type.get(target);
  const load = opts => {
    const host = {getSourceFile: (f, lv) => { const text = f === ROOT ? SRC : libFiles.get(f); return text === undefined ? undefined : ts.createSourceFile(f, text, lv); },
      getDefaultLibFileName: o => '/lib/' + ts.getDefaultLibFileName(o), getDefaultLibLocation: () => '/lib', writeFile: () => { throw new Error('no writes'); },
      getCurrentDirectory: () => '/proj', getCanonicalFileName: f => f, useCaseSensitiveFileNames: () => true, getNewLine: () => '\n',
      fileExists: f => f === ROOT || libFiles.has(f), readFile: f => f === ROOT ? SRC : libFiles.get(f), directoryExists: d => d === '/proj' || d === '/lib', getDirectories: () => []};
    return ts.createProgram({rootNames: [ROOT], options: {target: t, noEmit: true, types: [], ...opts}, host}).getSourceFiles().map(f => f.fileName);
  };
  const def = load({}), exp = load({lib: libs.map(n => 'lib.' + n + '.d.ts')});
  const agg = '/lib/' + ts.getDefaultLibFileName({target: t});
  const defRest = def.filter(f => f !== agg);
  out.targets[target] = {aggregator: agg, aggregatorInDefault: def.includes(agg), aggregatorInExpanded: exp.includes(agg),
    defaultCount: def.length, expandedCount: exp.length, rootInBoth: def.includes(ROOT) && exp.includes(ROOT),
    equalInOrderExceptAggregator: JSON.stringify(defRest) === JSON.stringify(exp), defaultFiles: def, expandedFiles: exp};
}
console.log(JSON.stringify(out, null, 1));
