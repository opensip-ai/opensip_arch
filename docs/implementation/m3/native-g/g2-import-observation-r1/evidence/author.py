from pathlib import Path
p=Path('/tmp/opensip-implementation/g2-import-observation-authoring/product/providers/rust/src/prepared_inputs.rs');s=p.read_text();assert 'pub fn declared_native_import_observation' not in s
addition=r'''
/// The two native-input wrapper kinds named by C r7 item13, not the complete
/// ImportKind vocabulary and not a token that admits an import.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DeclaredNativeImportKind {
    Dependency,
    Prepared,
}
/// Pure exact canonical preimage and raw digest; caller retains these bytes in
/// the wrapper's observation blob. This does not mint an ImportId or wrapper.
#[derive(Debug)]
pub struct DeclaredNativeImportObservation {
    kind: DeclaredNativeImportKind,
    canonical_bytes: Vec<u8>,
    raw_sha256: [u8; 32],
}
impl DeclaredNativeImportObservation {
    pub fn kind(&self) -> DeclaredNativeImportKind { self.kind }
    pub fn canonical_bytes(&self) -> &[u8] { &self.canonical_bytes }
    pub fn raw_sha256(&self) -> [u8; 32] { self.raw_sha256 }
}

/// C r7 item13's exact ImportObservationV1 record: version1, wrapper kind,
/// and null window/population/selection/revisionRange. Use the shared canonical
/// encoder and raw SHA256, never an H domain prefix or an import identity.
/// This constructor performs no wrapper/payload/source/context/retention/Plan
/// join or admission. The host still owns wrapper-kind equality, retained blob
/// custody, source correspondence, scope/build digests, closure selection,
/// native input imports and their NIJ-1/C/L/owner gates. No provider/input use,
/// execution, full importer or NativeContextVerified authority is granted.
pub fn declared_native_import_observation(
    kind: DeclaredNativeImportKind,
) -> Result<DeclaredNativeImportObservation, CanonicalError> {
    let name = match kind {
        DeclaredNativeImportKind::Dependency => "dependency",
        DeclaredNativeImportKind::Prepared => "prepared",
    };
    let value = JsonValue::Object(BTreeMap::from([
        ("schemaVersion".into(), JsonValue::Integer(opensip_identity::JsonInteger::new(1)?)),
        ("kind".into(), JsonValue::String(name.into())),
        ("window".into(), JsonValue::Null),
        ("population".into(), JsonValue::Null),
        ("selection".into(), JsonValue::Null),
        ("revisionRange".into(), JsonValue::Null),
    ]));
    let canonical_bytes = canonical_bytes(&value)?;
    let raw_sha256 = raw_sha256(&canonical_bytes);
    Ok(DeclaredNativeImportObservation { kind, canonical_bytes, raw_sha256 })
}
'''
pos=s.index('\nfn inert_media');p.write_text(s[:pos]+addition+s[pos:])
