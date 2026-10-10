from pathlib import Path
import hashlib,json
B=Path('/tmp/opensip-implementation');P=B/'sm-analysis-timing-2026-10-10';V=B/'sm-framed-analysis-2026-10-10';assert not V.exists();V.mkdir()
raw=(P/'driver.rs').read_bytes();assert hashlib.sha256(raw).hexdigest()=='6e98b5de01ff60530f3df15f557c4b2bceaaea838308b7c8fec8a01e9af45cd1';s=raw.decode()
s=s.replace('extern crate rustc_span;','extern crate rustc_span;\nextern crate opensip_identity;\nextern crate serde_json;\nuse std::io::Read;')
framed=r'''
fn frame(stream:&mut impl Read)->Vec<u8> {
 let mut length=[0u8;4];stream.read_exact(&mut length).expect("framed map truncated length");
 let length=u32::from_be_bytes(length) as usize;assert!((1..=1<<20).contains(&length),"framed map frame bound");
 let mut data=vec![0;length];stream.read_exact(&mut data).expect("framed map truncated payload");data
}
fn framed_map()->Vec<u8> {
 println!("{{\"event\":\"transfer_ready\"}}");std::io::stdout().flush().unwrap();
 let mut input=std::io::stdin().lock();let header:serde_json::Value=serde_json::from_slice(&frame(&mut input)).expect("framed map header JSON");
 let header=header.as_object().expect("framed map header object");assert_eq!(header.len(),3,"framed map header members");
 assert_eq!(header.get("format").and_then(|v|v.as_str()),Some("OPSMRUST1"));
 let expected=header.get("bytes").and_then(|v|v.as_u64()).expect("framed map bytes integer");
 // Derived wire overhead: content bound + descriptor bound + two u64 per row + magic/count.
 assert!((18..=((8u64<<30)+(4u64<<20)+16*100000+18)).contains(&expected),"framed map derived wire bound");
 let pin=header.get("sha256").and_then(|v|v.as_str()).expect("framed map hash text");
 assert!(pin.len()==64 && pin.bytes().all(|b|b.is_ascii_digit()||(b'a'..=b'f').contains(&b)),"framed map hash shape");
 let expected=usize::try_from(expected).unwrap();let mut raw=Vec::new();raw.try_reserve_exact(expected).expect("framed map allocation");let mut frames=0u64;
 while raw.len()<expected {let data=frame(&mut input);assert!(data.len()<=expected-raw.len(),"framed map extra content");raw.extend_from_slice(&data);frames=frames.checked_add(1).unwrap();}
 let mut tail=[0u8;1];assert_eq!(input.read(&mut tail).unwrap(),0,"framed map trailing input");
 let observed=opensip_identity::digest_hex(&opensip_identity::raw_sha256(&raw));assert_eq!(observed,pin,"framed map whole hash differs");
 println!("{{\"event\":\"prepared_map_wire_verified\",\"mapBytes\":{},\"mapSha256\":{},\"contentFrames\":{}}}",raw.len(),json_string(&observed),frames);raw
}
'''
s=s.replace('struct PreparedFiles',framed+'\nstruct PreparedFiles',1)
old='assert_eq!(args.get(1).map(String::as_str),Some("--prepared-map"));let raw=std::fs::read(&args[2]).unwrap();args.drain(1..3);';new='assert_eq!(args.get(1).map(String::as_str),Some("--prepared-map-framed-stdin"));args.remove(1);let raw=framed_map();';assert old in s;s=s.replace(old,new)
s=s.replace('assert!(count<=raw.len()/16);','assert!(count<=100000 && count<=raw.len()/16);')
s=s.replace('let mut files=BTreeMap::new();','let mut files=BTreeMap::new();let mut content_total=0u64;let mut descriptor_size=2usize;')
old='let n=number(&raw,&mut at);let content=bytes(&raw,&mut at,n).to_vec();let name=PathBuf::from(name);';new='''let n=number(&raw,&mut at);content_total=content_total.checked_add(u64::try_from(n).unwrap()).unwrap();assert!(content_total<=8u64<<30,"prepared content bound");let content=bytes(&raw,&mut at,n).to_vec();
 let mut row=serde_json::Map::new();row.insert("bytes".into(),serde_json::Value::from(n));row.insert("path".into(),serde_json::Value::from(name));row.insert("sha256".into(),serde_json::Value::from(opensip_identity::digest_hex(&opensip_identity::raw_sha256(&content))));let encoded=serde_json::to_vec(&serde_json::Value::Object(row)).unwrap();descriptor_size=descriptor_size.checked_add(encoded.len()).unwrap();if !files.is_empty(){descriptor_size=descriptor_size.checked_add(1).unwrap();}assert!(descriptor_size<=4<<20,"prepared descriptor bound");
 let name=PathBuf::from(name);''';assert old in s;s=s.replace(old,new)
(V/'driver.rs').write_text(s)
build=(P/'build_driver.py').read_text();old="str(B/'driver.rs'),'-o',str(exe)";new="'-L','dependency=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps','--extern','opensip_identity=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps/libopensip_identity-49c8c63d61772d58.rlib','--extern','serde_json=/Users/sb/code/opensip-ai/opensip-rsd1/target/release/deps/libserde_json-6a07d5ee01360a2d.rlib',str(B/'driver.rs'),'-o',str(exe)";assert old in build;build=build.replace(old,new);compile(build,str(V/'build_driver.py'),'exec');(V/'build_driver.py').write_text(build)
reference=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-rust-scope-2026-10-09/rust-helper/build.json');record=json.loads(reference.read_bytes())
(V/'linked-parent-reference.json').write_text(json.dumps(dict(acceptedTimingParentSource=dict(path=str(P/'driver.rs'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),linkedExistingFirstpartyArtifacts=record['linked'],buildReference=dict(path=str(reference),bytes=reference.stat().st_size,sha256=hashlib.sha256(reference.read_bytes()).hexdigest()),newVariantUnreviewed=True,actualCorpusUse=False,CargoRun=False,nativeWireProtocol=False),indent=2)+'\n')
print('Authored unbuilt separate stdin-framed Rust analysis variant; accepted source unchanged, no runtime or corpus use.')
