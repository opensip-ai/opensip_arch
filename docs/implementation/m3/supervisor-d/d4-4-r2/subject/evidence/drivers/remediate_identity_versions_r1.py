from pathlib import Path
import os,json,hashlib,datetime,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R=Path('/tmp/opensip-implementation/reviews/codex-d4-4-r1');review=json.loads((R/'review.json').read_text());assert review['verdict']=='REQUIRED-FINDINGS' and review['subjectManifestSha256']=='5d129b0f2ad4b6563b7f6f15a7403b24c54a699135a3ff135be4cd8ed2f886e4' and [x['id']for x in review['requiredFindings']]==['D4F-R1-RF-1']
p=W/'crates/components/src/provider_protocol/release_limits.rs';s=p.read_text();a=s.index('pub(crate) const RUST3:');s=s[:a]+'''/// Independent selected handshake authority for TS2 Hello and HelloAck.
/// This is protocol policy, never copied from either assembled codec output.
pub(crate) const TS2_IDENTITY_VERSIONS: [(&str, u64); 4] = [
    ("coverage", 3),
    ("fact", 2),
    ("plan", 2),
    ("snapshot", 2),
];
''' +s[a:]
s=s.replace('''        for (name, constants) in [
''','''        for name in ["TypeScriptHelloV2", "TypeScriptHelloAckV2"] {
            let J::Object(definition) = &defs[name] else { panic!() };
            let J::Object(properties) = &definition["properties"] else { panic!() };
            let J::Object(identity) = &properties["identityVersions"] else { panic!() };
            assert_eq!(identity["$ref"], J::String("#/$defs/IdentityVersionsV1".to_owned()));
            let J::Array(required)=&definition["required"] else {panic!()};
            assert!(required.contains(&J::String("identityVersions".to_owned())));
        }
        for (name, constants) in [
''',1).replace('''            ("ProtocolLimitsV3", RUST3.as_slice()),''','''            ("ProtocolLimitsV3", RUST3.as_slice()),
            ("IdentityVersionsV1", TS2_IDENTITY_VERSIONS.as_slice()),''',1);p.write_text(s)
p=W/'crates/components/src/session_factory/spec.rs';s=p.read_text();a=s.index('            let versions = field(hello, "identityVersions", work)?;');b=s.index('\n        }\n        (Provider::Rust',a)
s=s[:a]+'''            // Both assembled outputs are judged against the independent
            // selected protocol map. Agreement between outputs alone is not
            // evidence: both could carry the same missing/wrong version.
            let expected_versions = &release_limits::TS2_IDENTITY_VERSIONS;
            let versions = field(hello, "identityVersions", work)?;
            check(work, "hello-identity-version-count", || {
                matches!(versions, Value::Map(rows) if rows.len() == expected_versions.len())
            })?;
            for (key, version) in expected_versions {
                let actual = field(versions, key, work)?;
                check(work, "hello-identity-version", || {
                    actual == &Value::Unsigned(*version)
                })?;
            }
            check(work, "context-identity-version-count", || {
                context.identity_versions.len() == expected_versions.len()
            })?;
            // Ordered views avoid an assumed BTreeMap lookup price; each
            // actual key and value comparison is charged before evaluation.
            for ((key, version), (expected_key, expected_version)) in
                context.identity_versions.iter().zip(expected_versions)
            {
                check(work, "context-identity-version-key", || key == expected_key)?;
                check(work, "context-identity-version", || version == expected_version)?;
            }
''' +s[b:];p.write_text(s)
p=W/'crates/components/src/provider_protocol/ts2/send.rs';s=p.read_text();a=s.index('    pub fn request(&self) -> &Ts2Request {');b=s.index('\n    }',a)+6
s=s[:b]+'''

    /// Inject assembled-output drift for D4's independent-authority controls.
    /// No production API can mutate the immutable request after building it.
    #[cfg(test)]
    pub(crate) fn factory_identity_versions_mut_for_test(&mut self) -> &mut Value {
        let Value::Map(fields) = &mut self.request.hello else { unreachable!() };
        &mut fields.iter_mut().find(|(key, _)|key == "identityVersions").unwrap().1
    }
''' +s[b:];p.write_text(s)
p=W/'crates/components/src/session_factory/tests.rs';s=p.read_text();a=s.index('        let expected = selection(2);',s.index('fn typescript_checks_verified_descriptor'));b=s.index('        if corrupt == 0 {',a);block=s[a:b]
s+='''
#[test]
fn typescript_identity_versions_use_pinned_authority_even_when_both_outputs_agree_wrong() {
    // Wrong value in sender only / receiver only, then agreed-wrong value,
    // missing key, substituted key, extra key and empty maps. The independent
    // selected schema projection remains unchanged in every case.
    for case in 0..7 {
        let (mut sender, mut context)=crate::provider_protocol::ts2::factory_fixture_for_test();
        let (_, authority)=crate::provider_protocol::ts2::factory_fixture_for_test();
        let mut wrong=context.identity_versions.clone();
        match case {
            0..=2 => {wrong.insert("fact".to_owned(),99);}
            3 => {wrong.remove("fact");}
            4 => {let value=wrong.remove("fact").unwrap();wrong.insert("unexpected".to_owned(),value);}
            5 => {wrong.insert("unexpected".to_owned(),2);}
            6 => wrong.clear(),
            _ => unreachable!(),
        }
        if case != 1 {
            *sender.factory_identity_versions_mut_for_test()=Value::Map(wrong.iter().map(|(key,value)|(key.clone(),Value::Unsigned(*value))).collect());
        }
        if case != 0 {context.identity_versions=wrong;}
        if case >= 2 {
            let output=sender.factory_identity_versions_mut_for_test();
            let receiver=Value::Map(context.identity_versions.iter().map(|(key,value)|(key.clone(),Value::Unsigned(*value))).collect());
            assert_eq!(output,&receiver,"both assembled outputs deliberately agree on the same wrong map");
        }
''' +block+'''
        assert!(matches!(result,Err(WorkFailure::Operation(FactoryRefusal::SpecInconsistent(_)))),"case {case}");
        assert!(fake.calls.is_empty(),"case {case}: version drift must refuse before any native recheck");
    }
}
''';p.write_text(s)
record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),standing='R1 remediation implemented but UNVERIFIED and UNACCEPTED; R1 archive remains immutable.',independentReview=review,requiredFinding='D4F-R1-RF-1',chosenAuthority='Independent sorted constant projection pinned to selected IdentityVersionsV1 and actual TS2 Hello/HelloAck required refs; no caller/codec output supplies expected values.',checks='Both actual Hello and actual DispatchContext exact count/keys/values checked separately before recheck; no new allocation or profile.',newControl='Seven unilateral/agreed-wrong value/key/count/empty projections, with agreed outputs explicitly asserted; no recheck on refusal.',additionalRootCorrection='LEAD-D4F-R1-OFFSET-1; constructor-pin-r3 has explicit character/UTF8-byte units and raw-byte validation.',codeUnitAccepted=False,inventoryBound=False,productQualification=False)
(F/'r1-review-disposition.json').write_text(json.dumps(record,indent=2)+'\n')
C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/CURRENT-STATE.json');c=json.loads(C.read_text());j=json.loads((F/'CONTINUATION.json').read_text());j.update(utc=record['utc'],standing='R1 REQUIRED-FINDINGS: independent TS2 identity-version authority gap; remediation implemented, verification/successor review pending. Inventory mechanics separately ACCEPTed; not bound. Root also requires byte-offset evidence correction.',nextAction='Verify pinned version map and agreed-wrong control, compile affected mutations and restore, refresh public census if needed, freeze corrected complete R2 subject with preserved R1 review/history and offset correction; fresh CODEX2 review and separate inventory record assessment required. No R1 integration.',implementationAccepted=False,productQualification=False,entirePlanComplete=False)
j['review'].update(agentStatus='done',stateChangeSeq=2304,verdictRecorded=True,verdict='REQUIRED-FINDINGS',requiredFindings=['D4F-R1-RF-1'],inventoryVerdict='ACCEPT',worktreeMustRemainFrozen=False)
j['pendingSuccessor']='codex-d4-4-r2';j['rootRequiredCorrections']=['LEAD-D4F-R1-OFFSET-1'];paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());j['sourcePins']=[dict(path=q,bytes=(W/q).stat().st_size,sha256=hashlib.sha256((W/q).read_bytes()).hexdigest())for q in paths]
for name in ['CURRENT.json','CONTINUATION.json']:(F/name).write_text(json.dumps(j,indent=2)+'\n')
c['currentExecution']=j;c['D4FactoryTakeover']=j;C.write_text(json.dumps(c,indent=2)+'\n')
print('Implemented independent schema-pinned TS2 identity-version checks and seven output-drift controls; R1 preserved, no integration.')
