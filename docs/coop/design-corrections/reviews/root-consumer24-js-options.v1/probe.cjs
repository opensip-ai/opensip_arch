// Bounded compiler observation, using memory files only. No repository code executes.
const fs = require('node:fs');
const path = require('node:path');
const ts = require('./compiler/lib/typescript.js');
const choices = [{}, {checkJs:true}, {allowJs:false,checkJs:true}, {allowJs:true,checkJs:false}, {allowJs:true,checkJs:true}, {allowJs:false,checkJs:false}, {allowJs:true}, {allowJs:false}];
const rows=[];
for (const origin of ['tsconfig','jsconfig']) for (const jsFilePresent of [false,true]) for (const options of choices) {
  const files={'/review/main.ts':'export const x = 1;'};
  if(jsFilePresent) files['/review/helper.js']='export const y = 1;';
  const config={compilerOptions:{noLib:true,noEmit:true,...options},include:['**/*']};
  const configName='/review/'+origin+'.json';
  files[configName]=JSON.stringify(config);
  const readFile=name=>files[name];
  const parsed=ts.parseJsonConfigFileContent(config, {
    useCaseSensitiveFileNames:true, readFile, fileExists:name=>name in files,
    readDirectory:(_root,extensions)=>Object.keys(files).filter(name=>extensions.some(ext=>name.endsWith(ext))),
  }, '/review',undefined,configName);
  const host={
    getSourceFile:(name,languageVersion)=>files[name]===undefined?undefined:ts.createSourceFile(name,files[name],languageVersion,true),
    getDefaultLibFileName:()=>'/lib.d.ts',writeFile:()=>{},getCurrentDirectory:()=>'/review',getDirectories:()=>[],
    fileExists:name=>name in files,readFile,getCanonicalFileName:name=>name,useCaseSensitiveFileNames:()=>true,getNewLine:()=> '\n',
  };
  const program=ts.createProgram(parsed.fileNames,parsed.options,host);
  const jsRoots=program.getRootFileNames().filter(name=>/\.(?:js|mjs|cjs|jsx)$/.test(name));
  rows.push({origin,jsFilePresent,options,parsedAllowJs:parsed.options.allowJs??null,parsedCheckJs:parsed.options.checkJs??null,
    effectiveAllowJs:ts.getAllowJSCompilerOption(parsed.options),checkJs:!!parsed.options.checkJs,
    rootFiles:program.getRootFileNames(),jsRootFiles:jsRoots,
    configDiagnostics:parsed.errors.map(x=>({code:x.code,message:ts.flattenDiagnosticMessageText(x.messageText,'\n')})),
    optionDiagnostics:program.getOptionsDiagnostics().map(x=>({code:x.code,message:ts.flattenDiagnosticMessageText(x.messageText,'\n')})),
  });
}
const result={standing:'Bounded official compiler5.6.3 observations, not whole compiler/provider/product qualification or a required OpenSIP compiler pin.',compilerVersion:ts.version,rows};
fs.writeFileSync(path.join(__dirname,'compiler-observations.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({version:ts.version,cases:rows.length,samples:rows.filter(x=>x.jsFilePresent&&x.options.checkJs&&x.options.allowJs!==true)},null,2));
