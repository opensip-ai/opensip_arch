from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
w=Path('.')
p=w/'crates/host/tests/support/factory_ts2.rs';p.parent.mkdir(exist_ok=True);assert not p.exists();p.write_text('''//! Synthetic public A2 field projection, matching D2b's public first-party
//! descriptor fixture literals. Neither signatures nor C4 admission claimed.
use opensip_components::provider_protocol::{cbor::Value, ts2::DescriptorFields};
fn t(s: &str)->Value {Value::Text(s.into())}
pub fn provider()->DescriptorFields {
    DescriptorFields::from_iter([
        ("providerBuildId".into(),t("typescript-provider 1.0.0")),
        ("protocolMajor".into(),Value::Unsigned(2)),
        ("typescriptVersion".into(),t("5.9.2")),
        ("typescriptCompilerSha256".into(),t(&"1".repeat(64))),
        ("typescriptStdlibMerkleRoot".into(),t(&"2".repeat(64))),
        ("defaultWorkBudgetProfileId".into(),t("typescript-provider-default-work-budget-v1")),
        ("defaultWorkBudgetProfileSha256".into(),t("bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6")),
    ])
}
pub fn runtime()->DescriptorFields {
    DescriptorFields::from_iter([
        ("nodeVersion".into(),t("24.16.0")), ("v8Version".into(),t("13.6")),
        ("modulesAbi".into(),t("137")), ("platformId".into(),t("darwin-arm64")),
    ])
}
''')
send=(w/'crates/components/src/provider_protocol/ts2_send_tests.rs').read_text();recv=(w/'crates/components/src/provider_protocol/ts2_tests.rs').read_text()
universe=send[send.index('fn universe()'):send.index('/// Each file')]
plan=send[send.index('fn content('):send.index('pub(super) fn factory_fixture')]
context=recv[recv.index('fn context(tokens:'):recv.index('\nfn hello_ack')]
a=context.index('    let text =');b=context.index('    let budget =');context=context[:a]+'''    let provider = descriptors::provider();
    let runtime = descriptors::runtime();
'''+context[b:]
context_of=send[send.index('fn context_of('):send.index('\nfn wire(kind:')]
p=w/'crates/host/src/launch_recheck_ts2_fixture.rs';assert not p.exists();p.write_text('''//! Synthetic pre-C4 public wire inputs. The recipe matches D2b's public
//! sender controls; descriptor authorities are separate literal projections.
use super::*;
use opensip_components::provider_protocol::{cbor::Value, ts2::{*, send::*}};
use opensip_identity::JsonValue as J;
use std::collections::{BTreeMap,BTreeSet};
#[path = "../tests/support/factory_ts2.rs"]
mod descriptors;
const MIB:u64=1_048_576;
const BUILD:&str="typescript-provider 1.0.0";
const EXEC:&str="exec1_0123456789abcdef0123456789abcdef";
const PATH:&str="src/a.ts";
const TOKENS:[&str;4]=["coverage-v3","fact-identity-fact2","plan-identity-plan2","source-identity-snapshot2"];
fn h(c:char)->String{c.to_string().repeat(64)}
fn sha(c:char)->String{format!("sha256:{}",h(c))}
fn t(v:&str)->Value{Value::Text(v.into())}
fn get<'a>(v:&'a Value,k:&str)->&'a Value{let Value::Map(rows)=v else {panic!("map")}; &rows.iter().find(|(n,_)|n==k).unwrap().1}
fn stage(r:&Ts2Request,i:usize)->&Value{let Value::Array(rows)=get(r.analyze(),"stageRequests")else{panic!("stages")}; &rows[i]}
''' +universe+plan+context+context_of+'''
pub(super) struct Input {
    pub provider: Provider,
    pub provider_fields: DescriptorFields,
    pub runtime_fields: DescriptorFields,
    pub provider_digest: String,
    pub runtime_digest: String,
    pub capabilities: Vec<String>,
}
pub(super) fn typescript()->Input {
    let plan=plan();let request=Ts2Request::build(&plan).unwrap();let context=context_of(&plan,&request);
    Input{provider:Provider::TypeScript{sender:Ts2Sender::new(request),context},provider_fields:descriptors::provider(),runtime_fields:descriptors::runtime(),provider_digest:h('3'),runtime_digest:h('4'),capabilities:TOKENS.iter().map(|s|(*s).into()).collect()}
}
''')
p=w/'crates/host/src/launch_recheck_tests.rs';s=p.read_text();s=s.replace('mod wire_fixture;','mod wire_fixture;\n#[path = "launch_recheck_ts2_fixture.rs"]\nmod ts2_fixture;',1)
s=s.replace('''        assert!(mode.bytes().all(|b| b.is_ascii_lowercase()));''','''        Self::with_files(data, None, mode)
    }
    fn with_files(data: &[u8], node: Option<&[u8]>, mode: &str) -> Self {
        assert!(mode.bytes().all(|b| b.is_ascii_lowercase()));''',1)
s=s.replace('''        let rows = [
            ap::TreeRow {''','''        let mut rows = vec![
            ap::TreeRow {''',1)
s=s.replace('''        let archive_bytes = ap::emit(&rows, &[("provider", data)]).unwrap();''','''        let mut contents = vec![("provider", data)];
        if let Some(node) = node {
            rows.push(ap::TreeRow { path:"node", mode:0o755, kind:ap::RowKind::File { length:node.len() as u64, sha256:raw_sha256(node) } });
            rows.push(ap::TreeRow { path:"openssl.cnf", mode:0o644, kind:ap::RowKind::File { length:0, sha256:raw_sha256(b"") } });
            contents.extend([("node",node),("openssl.cnf",&b""[..])]);
        }
        rows.sort_by_key(|r|r.path);
        contents.sort_by_key(|(path,_)|*path);
        let archive_bytes = ap::emit(&rows, &contents).unwrap();''',1)
a=s.index('        object.insert("platforms"');b=s.index('        let body =',a)
s=s[:a]+'''        let entries: Vec<_> = rows.iter().map(|row| match row.kind {
            ap::RowKind::File {length,sha256} => serde_json::json!({"path":row.path,"mode":format!("{:04o}",row.mode),"type":"file","length":length,"sha256":digest_hex(&sha256)}),
            ap::RowKind::Symlink {target} => serde_json::json!({"path":row.path,"mode":format!("{:04o}",row.mode),"type":"symlink","target":target}),
            _ => unreachable!("first-party fixture uses only files and one alias"),
        }).collect();
        object.insert("platforms".into(), serde_json::json!([{"os":"macos","arch":"arm64","entrypoint":"provider","tree":{"entries":entries}}]));
''' +s[b:];p.write_text(s)
print('Added synthetic public TS2 request/independent descriptor projections and native multi-file fixture support.')
