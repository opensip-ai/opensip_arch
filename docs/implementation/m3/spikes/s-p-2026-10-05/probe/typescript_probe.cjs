const fs = require('node:fs');
const ts = require(process.argv[2]);
const file = process.argv[3];
const options = { noEmit: true, strict: true, types: [], target: ts.ScriptTarget.ES2022 };
const readPaths = new Set();
const host = ts.createCompilerHost(options);
const read = host.readFile.bind(host);
host.readFile = name => { readPaths.add(name); return read(name); };
const program = ts.createProgram([file], options, host);
const diagnostics = ts.getPreEmitDiagnostics(program);
console.log(JSON.stringify({ compilerVersion: ts.version, createProgramAvailable: true,
    diagnostics: diagnostics.map(d => ({code: d.code, message: ts.flattenDiagnosticMessageText(d.messageText, '\n')})),
    sourceFiles: program.getSourceFiles().map(s => s.fileName), readPaths: [...readPaths].sort() }));
if (diagnostics.length) process.exitCode = 1;
