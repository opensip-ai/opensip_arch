// TSR-1 r2 interpretation evidence: does a project reference change program membership when there are no roots?
const ts = require(process.argv[2]);
const files = new Map(Object.entries({
  '/proj/main.ts': 'const root = 1;\n',
  '/proj/ref/tsconfig.json': JSON.stringify({compilerOptions: {composite: true, module: 'none', outFile: '../dist/ref.js'}, files: ['global.ts']}),
  '/proj/ref/global.ts': 'declare var g: number;\n',
  '/proj/dist/ref.d.ts': 'declare var g: number;\n',
}));
const host = {getSourceFile: (f, lv) => files.has(f) ? ts.createSourceFile(f, files.get(f), lv) : undefined,
  getDefaultLibFileName: () => '/lib/none.d.ts', writeFile: () => { throw new Error('no writes'); }, getCurrentDirectory: () => '/proj',
  getCanonicalFileName: f => f, useCaseSensitiveFileNames: () => true, getNewLine: () => '\n', fileExists: f => files.has(f),
  readFile: f => files.get(f), directoryExists: () => true, getDirectories: () => [], readDirectory: () => []};
const run = (roots, refs) => ts.createProgram({rootNames: roots, options: {noEmit: true, noLib: true, types: []}, projectReferences: refs, host})
  .getSourceFiles().map(f => f.fileName);
const R = [{path: '/proj/ref'}];
console.log(JSON.stringify({version: ts.version,
  rootsNoRef: run(['/proj/main.ts'], undefined), rootsWithRef: run(['/proj/main.ts'], R),
  noRootsNoRef: run([], undefined), noRootsWithRef: run([], R)}, null, 1));
