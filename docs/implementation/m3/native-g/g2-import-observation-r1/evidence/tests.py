from pathlib import Path
import hashlib,json
p=Path('/tmp/opensip-implementation/g2-import-observation-authoring/product/providers/rust/src/prepared_inputs_tests.rs');s='\n'
for kind,variant in [('dependency','Dependency'),('prepared','Prepared')]:
 raw=json.dumps({'schemaVersion':1,'kind':kind,'window':None,'population':None,'selection':None,'revisionRange':None},sort_keys=True,separators=(',',':')).encode();sha=hashlib.sha256(raw).hexdigest()
 s+=f'''\n#[test]\nfn native_import_observation_{kind}_has_exact_six_member_golden_raw_preimage() {{\n let observation=declared_native_import_observation(DeclaredNativeImportKind::{variant}).unwrap();\n assert_eq!(observation.kind(),DeclaredNativeImportKind::{variant});\n assert_eq!(observation.canonical_bytes(),br#"{raw.decode()}"#);\n assert_eq!(digest_hex(&observation.raw_sha256()),"{sha}");\n}}\n'''
s+=r'''
#[test]
fn native_import_observation_current_schema_requires_each_member_and_closed_kind() {
    let objects=BTreeMap::new();let blobs=BTreeMap::new();let inputs=RetainedInputs::new(schemas(),&objects,&blobs);
    for kind in [DeclaredNativeImportKind::Dependency,DeclaredNativeImportKind::Prepared] {
        let observation=declared_native_import_observation(kind).unwrap();
        let value=opensip_identity::parse_json(observation.canonical_bytes()).unwrap();
        inputs.check_current_value_shape(&value,"workflows/schemas/imported-evidence.schema.json","#/$defs/ImportObservationV1",WORK).unwrap();
        for key in ["schemaVersion","kind","window","population","selection","revisionRange"] {
            let mut missing=value.clone();fields(&mut missing).remove(key);
            assert!(inputs.check_current_value_shape(&missing,"workflows/schemas/imported-evidence.schema.json","#/$defs/ImportObservationV1",WORK).is_err(),"{key}");
        }
        let mut extra=value.clone();fields(&mut extra).insert("observation".into(),JsonValue::Null);
        assert!(inputs.check_current_value_shape(&extra,"workflows/schemas/imported-evidence.schema.json","#/$defs/ImportObservationV1",WORK).is_err());
        for wrong in [JsonValue::Null,text("unknown-kind")] {
            let mut invalid=value.clone();fields(&mut invalid).insert("kind".into(),wrong);
            assert!(inputs.check_current_value_shape(&invalid,"workflows/schemas/imported-evidence.schema.json","#/$defs/ImportObservationV1",WORK).is_err());
        }
    }
}
'''
p.write_text(p.read_text()+s)
