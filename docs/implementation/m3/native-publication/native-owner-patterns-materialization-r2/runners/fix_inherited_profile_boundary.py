from pathlib import Path
import os,json,re,hashlib,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip';B=F/'inherited-boundary-fix-r1';assert not B.exists();B.mkdir()
Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-materialization-r1');review=json.loads((Q/'review.json').read_text());assert review['verdict']=='REQUIRED-FINDINGS' and [r['id'] for r in review['requiredFindings']]==['OWNPAT-UNIT-R1-RF-1']
M=W/'crates/identity/src/schema_patterns.rs';T=W/'crates/identity/src/schema_tests.rs';before={str(p.relative_to(W)):p.read_bytes() for p in [M,T]}
s=M.read_text();s=s.replace('    CompleteRelativePath(bool),\n','')
start=s.index('    (\n',s.index('const TABLE:'));end=s.index('    (r##"^.+$"##',start);removed=s[start:end];assert removed.count('Kind::CompleteRelativePath')==2;s=s[:start]+s[end:]
line=next(x for x in s.splitlines(True) if 'Kind::CompleteRelativePath(empty) =>' in x);s=s.replace(line,'')
needle='    // ECMA-u without m: `$` is the actual end of input, not a position\n'
assert s.count(needle)==1
forms=[r'^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]*(?![\s\S])',r'^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])']
branch='''    // The two corrected complete-input forms are native keyword forms only.
    // Inherited patterns, including every patternProperties key, must refuse
    // them rather than silently expanding the 72-form legacy interpreter.
    let allows_empty = match pattern {
'''+''.join('        r##"'+p+'"## => Some('+('true' if i==0 else 'false')+'),\n' for i,p in enumerate(forms))+'''        _ => None,
    };
    if let Some(empty) = allows_empty {
        return Ok((empty || !value.is_empty())
            && !value.starts_with('/')
            && !value.contains(['\\0', '\\\\'])
            && !value.split('/').any(|part| matches!(part, "." | "..")));
    }
'''
s=s.replace(needle,branch+needle)
old=(P/'crates/identity/src/schema_patterns.rs').read_text()
def table(raw):return raw[raw.index('const TABLE:'):raw.index('\npub fn matches')]
assert table(s)==table(old)
patterns=re.findall(r'r(#+)"(.*?)"\1',table(old),re.S);assert len(patterns)==72
expected='''
#[cfg(test)]
#[test]
fn native_owner_inherited_pattern_set_is_exactly_the_selected_predecessor_72_forms() {
    // Exact accepted predecessor profile, independently enumerated; checking
    // only old-pattern behavior would miss new shared-table admissions.
    const EXPECTED: &[&str] = &[
'''+''.join('        r##"'+p+'"##,\n' for _,p in patterns)+'''    ];
    let actual: alloc::vec::Vec<_> = TABLE.iter().map(|row| row.0).collect();
    assert_eq!(actual.len(), 72);
    assert_eq!(actual.as_slice(), EXPECTED);
}
'''
s+=expected
M.write_text(s)
control='''
#[test]
fn native_owner_corrected_forms_refuse_foreign_patterns_and_all_pattern_property_keys() {
    let forms = [
'''+''.join('        r##"'+p+'"##,\n' for p in forms)+'''    ];
    let owners = [
        "urn:opensip:product-v1:native:evidence-schemas:v2",
        "opensip.product.occupancy-companion.1",
        "opensip.product.relation-payload.2",
    ];
    for (index, pattern) in forms.into_iter().enumerate() {
        let raw = crate::canonical_bytes(&crate::JsonValue::String(pattern.into())).unwrap();
        let quoted = core::str::from_utf8(&raw).unwrap();
        let body = format!(r#""type":"string","pattern":{quoted}"#);
        for owner in owners {
            let entry = format!("{owner}#");
            let document = native_owner_document(owner, &body);
            let scoped = Program::compile_registered_native_owners(
                vec![document.clone()], &[&entry], 100_000,
            ).unwrap();
            for (value, expected) in [
                ("", index == 0), ("a/..\\n", true), ("a/..\\r", true),
                ("a/..\\u{2028}", true), ("a/..\\u{2029}", true),
                ("a/..", false), ("x\\n/../y", false), ("/a", false),
                ("a\\0", false), ("a\\\\b", false),
            ] {
                let input = crate::canonical_bytes(&crate::JsonValue::String(value.into())).unwrap();
                assert_eq!(scoped.matches_json(&entry, &input, 100_000), Ok(expected), "{owner} {pattern} {value:?}");
            }
            // The inert/generic Program keeps the inherited closed profile,
            // even when a document uses a native spelling for its identity.
            assert!(matches!(Program::compile(vec![document], &[&entry], 100_000), Err(Error::Pattern)));
        }
        assert!(matches!(
            Program::compile_registered_native_owners(vec![doc(&body)], &["urn:probe#"], 100_000),
            Err(Error::Pattern)
        ));
        // Native-to-foreign references must refuse the foreign pattern at
        // construction, as direct foreign documents do.
        let foreign = doc(&body);
        let native = native_owner_document(owners[0], r##""$ref":"urn:probe#""##);
        let entry = format!("{}#", owners[0]);
        assert!(matches!(
            Program::compile_registered_native_owners(vec![native, foreign], &[&entry], 100_000),
            Err(Error::Pattern)
        ));
        let property_body = format!(r#""type":"object","patternProperties":{{{quoted}:{{"type":"integer"}}}}"#);
        for owner in owners.into_iter().chain(["urn:probe"]) {
            let entry = format!("{owner}#");
            let document = native_owner_document(owner, &property_body);
            assert!(matches!(
                Program::compile_registered_native_owners(vec![document.clone()], &[&entry], 100_000),
                Err(Error::Pattern)
            ), "patternProperties leaked: {owner} {pattern}");
            assert!(matches!(Program::compile(vec![document], &[&entry], 100_000), Err(Error::Pattern)));
        }
    }
}
'''
# Format only new test items; preserve all base-dirty historical source bytes.
for name,raw in [('pattern-profile-control.rs',expected),('owner-boundary-control.rs',control)]:
 proc=subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--emit','stdout'],input=raw.encode(),capture_output=True);assert proc.returncode==0,proc.stderr
 (B/name).write_bytes(proc.stdout)
 if name.startswith('pattern'):M.write_text(s[:-len(expected)]+'\n'+proc.stdout.decode())
 else:T.write_bytes(before[str(T.relative_to(W))]+b'\n'+proc.stdout)
for rel,raw in before.items():
 p=B/'parents'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
report=dict(requiredFinding='OWNPAT-UNIT-R1-RF-1',sharedTableExactPredecessor=True,inheritedForms=72,newSharedForms=0,nativeFormCount=26,changedPaths=[dict(path=p,beforeSha256=hashlib.sha256(raw).hexdigest(),afterSha256=hashlib.sha256((W/p).read_bytes()).hexdigest()) for p,raw in before.items()],unitAccepted=False,blindModesRun=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
