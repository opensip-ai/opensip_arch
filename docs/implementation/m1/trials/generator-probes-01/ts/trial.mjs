import fs from "node:fs/promises";
import { compile } from "json-schema-to-typescript";
import Ajv2020 from "ajv/dist/2020.js";
import standaloneCode from "ajv/dist/standalone/index.js";
const rows=[];
for (const name of ["u64", "closure-id"]) {
 const raw=await fs.readFile(`../inputs/${name}.json`, "utf8");
 const schema=JSON.parse(raw);
 const declaration=await compile(schema,name,{bannerComment:"",$refOptions:{resolve:{file:false,http:false}}});
 await fs.writeFile(`${name}.ts`,declaration);
 const ajv=new Ajv2020({strict:true,allErrors:true,coerceTypes:false,useDefaults:false,removeAdditional:false,code:{source:true,esm:true}});
 const validate=ajv.compile(schema);
 await fs.writeFile(`${name}.validator.mjs`,standaloneCode(ajv,validate));
 const tokens=name==="u64"?["9007199254740991","9007199254740992","9007199254740993","18446744073709551615","18446744073709551616","-9223372036854775808","1e2","1.0","-0",'"7"']:[];
 const cases=tokens.map(token=>{const native=JSON.parse(token);const accepted=validate(native);const errors=structuredClone(validate.errors);const integer=/^-?(0|[1-9][0-9]*)$/.test(token)?BigInt(token):undefined;const bigAccepted=integer===undefined?null:validate(integer);return {token,native:String(native),nativeAccepted:accepted,nativeErrors:errors,bigintAccepted:bigAccepted,bigintErrors:integer===undefined?null:structuredClone(validate.errors)};});
 const patternCases=name==="closure-id"?["closure2:"+"a".repeat(64),"closure2:"+"a".repeat(64)+"\n"].map(value=>({value,accepted:validate(value)})):[];
 rows.push({name,declaration,cases,patternCases});
}
const report={standing:"Preliminary bounded compatibility trial; no complete generation recipe selected",tools:{node:process.version,typescript:"7.0.2",jsonSchemaToTypescript:"16.0.0",ajv:"8.20.0"},rows};
await fs.writeFile("trial-results.json",JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify(report,null,2));
