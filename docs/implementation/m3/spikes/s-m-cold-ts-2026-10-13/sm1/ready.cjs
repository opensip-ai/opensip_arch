'use strict';
const ts=require(process.argv[2]);
if(process.version!=='v24.16.0'||ts.version!=='6.0.3'||typeof ts.createProgram!=='function')throw Error('runtime/compiler pin or API mismatch');
const expected=Buffer.from('opensip-sm-startup-request\n','ascii');let received=Buffer.alloc(0);
process.stdin.on('data',chunk=>{received=Buffer.concat([received,chunk]);if(received.length>expected.length||!received.equals(expected.subarray(0,received.length)))throw Error('unexpected probe request');if(received.length===expected.length){process.stdout.write(JSON.stringify({event:'request-read',requestBytes:received.length,node:process.version,typescript:ts.version})+'\n');process.exit(0);}});
process.stdin.on('end',()=>{if(received.length!==expected.length)throw Error('incomplete probe request');});
process.stdout.write(JSON.stringify({event:'ready',node:process.version,typescript:ts.version,requestReaderRegistered:true})+'\n');
