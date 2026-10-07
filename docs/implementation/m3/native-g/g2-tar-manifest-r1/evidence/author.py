from pathlib import Path
p=Path('/tmp/opensip-implementation/g2-tar-manifest-authoring/product/providers/rust/src/dependency_inputs.rs');s=p.read_text();assert 'pub fn check_declared_tar_manifest' not in s
addition=r'''
/// An exact declared inflated-member / retained-manifest byte join only.
#[derive(Debug)]
pub struct DeclaredTarManifest<'a> {
    lock: DependencyLockChecks,
    package_index: usize,
    members: Vec<DeclaredTarMember<'a>>,
}
impl DeclaredTarManifest<'_> {
    pub fn lock_checks(&self) -> &DependencyLockChecks { &self.lock }
    pub fn package_index(&self) -> usize { self.package_index }
    pub fn members(&self) -> &[DeclaredTarMember<'_>] { &self.members }
}
#[derive(Debug)]
pub enum DeclaredTarManifestError {
    Lock(DependencyLockError),
    Inputs(DependencyInputError),
    SelectedPackage,
    Tar(DeclaredTarError),
    Mismatch { field: &'static str },
}
impl From<DependencyInputError> for DeclaredTarManifestError {
    fn from(value: DependencyInputError) -> Self { Self::Inputs(value) }
}

/// Compare caller-declared inflated tar members with the selected retained
/// dependency file manifest after all accepted declared lock/context/universe/
/// snapshot/member checks. The exact checked package tuple supplies the root;
/// no caller root, package-key spelling, source priority or mount is inferred.
/// Every path, byte length and raw SHA256 must match, with no extra/missing
/// members. Return no partial observation on a mismatch or malformed tar.
///
/// Even matching bytes do not prove that this inflated stream came from the
/// locked compressed .crate preimage. This grants no gzip/CRC/inflation proof,
/// acquisition/provenance/manifest admission, filesystem extraction, activation,
/// full decoder/importer, NativeContextVerified/Plan/provider or qualification.
pub fn check_declared_tar_manifest<'a>(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    package_index: usize,
    inflated: &'a [u8],
    schema_work: usize,
) -> Result<DeclaredTarManifest<'a>, DeclaredTarManifestError> {
    use DeclaredTarManifestError as E;
    let lock = check_declared_lockfile_joins(inputs, request, schema_work).map_err(E::Lock)?;
    let frame = inputs.frame_candidate(
        lock.dependency_checks().dependency_digest(), NativeFrameSet::Nested, schema_work,
    ).map_err(DependencyInputError::Frame)?;
    let package = array(field(map(frame.descriptor())?, "packages")?)?
        .get(package_index).ok_or(E::SelectedPackage)?;
    let package = map(package)?;
    let members = observe_declared_tar_members(
        text(field(package, "name")?)?, text(field(package, "version")?)?, inflated,
    ).map_err(E::Tar)?;
    let manifest = inputs.frame_candidate(
        digest(text(field(package, "fileManifestSha256")?)?)?, NativeFrameSet::Nested, schema_work,
    ).map_err(DependencyInputError::Frame)?;
    // The mandatory dependency check has already checked the exact domain,
    // registered shape, ordering, count/sum and all retained raw member bytes.
    let rows = array(manifest.descriptor())?;
    if rows.len() != members.len() { return Err(E::Mismatch { field: "fileCount" }); }
    for (row, member) in rows.iter().zip(&members) {
        let row = map(row)?;
        if text(field(row, "path")?)? != member.path() {
            return Err(E::Mismatch { field: "path" });
        }
        let length = u64::try_from(member.content().len()).map_err(|_| DependencyInputError::CountOverflow)?;
        if number(field(row, "byteLength")?)? != length {
            return Err(E::Mismatch { field: "byteLength" });
        }
        if digest(text(field(row, "contentSha256")?)?)? != opensip_identity::raw_sha256(member.content()) {
            return Err(E::Mismatch { field: "contentSha256" });
        }
    }
    Ok(DeclaredTarManifest { lock, package_index, members })
}
'''
pos=s.index('\nfn optional_lock_text');p.write_text(s[:pos]+addition+s[pos:])
