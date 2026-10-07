//! Declared dependency-manifest/member retention, with no provenance admission.

use crate::universe_inputs::{
    UniverseInputChecks, UniverseInputError, UniverseInputRequest, check_declared_universe_inputs,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue, NativeFrameSet, RetainedInputError, RetainedInputs,
};
use std::collections::BTreeMap;

#[derive(Debug)]
pub enum DependencyInputError {
    Universe(UniverseInputError),
    Frame(GraphError),
    Retained(RetainedInputError),
    Representation,
    Mismatch { package: usize, field: &'static str },
    CountOverflow,
}

/// Inert byte/count observations, not an authenticated/complete dependency set.
#[derive(Debug)]
pub struct DependencyInputChecks {
    universe: UniverseInputChecks,
    dependency_digest: [u8; 32],
    package_count: usize,
    declared_files: u64,
    declared_bytes: u64,
}
impl DependencyInputChecks {
    pub fn universe_checks(&self) -> &UniverseInputChecks {
        &self.universe
    }
    pub fn dependency_digest(&self) -> [u8; 32] {
        self.dependency_digest
    }
    pub fn package_count(&self) -> usize {
        self.package_count
    }
    pub fn declared_files(&self) -> u64 {
        self.declared_files
    }
    pub fn declared_bytes(&self) -> u64 {
        self.declared_bytes
    }
}

/// Check §3.1's exact declared dependency manifest/member byte and count joins.
/// Mandatory universe/context/nested/snapshot correspondence runs first. Every
/// package names the H preimage of a current registered dependency-file-manifest,
/// whose sorted unique paths, file count, byte sum and member bytes are checked.
/// The selected snapshot's Cargo.lock raw bytes are retained at its exact length.
/// Shared member bytes may be verified once per immutable request; differing
/// declared lengths still refuse, and each file/package counts independently.
///
/// A declared checksumVerification=mismatch refuses the whole observation.
/// Other verification/provenance labels remain declarations: this does not parse
/// Cargo.lock, derive activated features/completeness, authenticate a tarball,
/// verify a vendor checksum file or git revision, admit import/source acquisition,
/// mount a dependency namespace or grant native context/Plan/provider authority.
pub fn check_declared_dependency_inputs(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    schema_work: usize,
) -> Result<DependencyInputChecks, DependencyInputError> {
    let universe = check_declared_universe_inputs(inputs, request, schema_work)
        .map_err(DependencyInputError::Universe)?;
    let universe_frame = inputs
        .frame_candidate(
            request.universe_digest,
            NativeFrameSet::SemanticUniverse,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let dependency_id = text(field(
        map(universe_frame.descriptor())?,
        "dependencySourceSetId",
    )?)?
    .strip_prefix("sha256:")
    .ok_or(DependencyInputError::Representation)?;
    let dependency_digest = digest(dependency_id)?;
    let dependency = inputs
        .frame_candidate(dependency_digest, NativeFrameSet::Nested, schema_work)
        .map_err(DependencyInputError::Frame)?;
    if dependency.domain() != "native.dependency-source-set.v1" {
        return Err(DependencyInputError::Representation);
    }
    let dependency = map(dependency.descriptor())?;
    let lock = map(field(dependency, "lockfileIdentity")?)?;
    let snapshot = inputs
        .object(request.snapshot_id, IdentityDomain::Snapshot, schema_work)
        .map_err(DependencyInputError::Retained)?;
    let mut lengths = BTreeMap::new();
    let lock_path = field(lock, "path")?;
    let mut found = false;
    for row in array(field(map(snapshot.descriptor())?, "sourceInventory")?)? {
        let row = map(row)?;
        if field(row, "path")? == lock_path {
            retain_blob(
                inputs,
                digest(text(field(lock, "contentSha256")?)?)?,
                number(field(row, "bytes")?)?,
                &mut lengths,
            )?;
            found = true;
        }
    }
    if !found {
        return Err(DependencyInputError::Representation);
    }
    let packages = array(field(dependency, "packages")?)?;
    let mut declared_files = 0u64;
    let mut declared_bytes = 0u64;
    for (index, package) in packages.iter().enumerate() {
        let package = map(package)?;
        if text(field(package, "checksumVerification")?)? == "mismatch" {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "checksumVerification",
            });
        }
        let manifest = inputs
            .frame_candidate(
                digest(text(field(package, "fileManifestSha256")?)?)?,
                NativeFrameSet::Nested,
                schema_work,
            )
            .map_err(DependencyInputError::Frame)?;
        if manifest.domain() != "native.dependency-file-manifest.v1" {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "fileManifest.domain",
            });
        }
        let files = array(manifest.descriptor())?;
        let count = u64::try_from(files.len()).map_err(|_| DependencyInputError::CountOverflow)?;
        if number(field(package, "fileCount")?)? != count {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "fileCount",
            });
        }
        let total = files.iter().try_fold(0u64, |total, row| {
            total
                .checked_add(number(field(map(row)?, "byteLength")?)?)
                .ok_or(DependencyInputError::CountOverflow)
        })?;
        if number(field(package, "totalBytes")?)? != total {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "totalBytes",
            });
        }
        for row in files {
            let row = map(row)?;
            retain_blob(
                inputs,
                digest(text(field(row, "contentSha256")?)?)?,
                number(field(row, "byteLength")?)?,
                &mut lengths,
            )?;
        }
        declared_files = declared_files
            .checked_add(count)
            .ok_or(DependencyInputError::CountOverflow)?;
        declared_bytes = declared_bytes
            .checked_add(total)
            .ok_or(DependencyInputError::CountOverflow)?;
    }
    Ok(DependencyInputChecks {
        universe,
        dependency_digest,
        package_count: packages.len(),
        declared_files,
        declared_bytes,
    })
}

/// Declared package tuple/checksum joins to exact retained lock bytes only.
#[derive(Debug)]
pub struct DependencyLockChecks {
    dependency: DependencyInputChecks,
    lockfile_version: u8,
    lock_package_rows: usize,
}
impl DependencyLockChecks {
    pub fn dependency_checks(&self) -> &DependencyInputChecks {
        &self.dependency
    }
    pub fn lockfile_version(&self) -> u8 {
        self.lockfile_version
    }
    pub fn lock_package_rows(&self) -> usize {
        self.lock_package_rows
    }
}
#[derive(Debug)]
pub enum DependencyLockError {
    Inputs(DependencyInputError),
    Parse(opensip_identity::TomlError),
    Shape(&'static str),
    Version,
    MissingTuple(usize),
    AmbiguousTuple(usize),
    Checksum(usize),
}
impl From<DependencyInputError> for DependencyLockError {
    fn from(error: DependencyInputError) -> Self {
        Self::Inputs(error)
    }
}

/// Observe exact Cargo.lock version/package tuple/checksum correspondence.
/// Mandatory retained universe/context/snapshot/dependency-manifest/member joins
/// run first. All exact inventoried lock bytes are parsed as one TOML document,
/// without recovery. The parsed version is 3 or 4 and equals the descriptor.
/// Every declared package joins by the exact (name, version, sourceId) tuple;
/// absent source means the path-package empty string. Missing or ambiguous joins
/// never choose a first/last/nearest row. Declared lockChecksum equals the
/// matching lock row's optional checksum, with absence remaining null.
///
/// This is not activated-feature membership/completeness, Cargo metadata or
/// Cargo's full lock-format validation. Other lock rows/fields are not an
/// activation list, and sourceKind/provenance/acquisition/tarball/vendor/git
/// admission remain separate. No packageKey codec, delimiter or mount spelling
/// is invented. The selected pure parser's local bounds remain local parse
/// errors, not a widened product scope bound or new wire refusal cause.
pub fn check_declared_lockfile_joins(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    schema_work: usize,
) -> Result<DependencyLockChecks, DependencyLockError> {
    let dependency = check_declared_dependency_inputs(inputs, request, schema_work)?;
    let frame = inputs
        .frame_candidate(
            dependency.dependency_digest(),
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let descriptor = map(frame.descriptor())?;
    let lock = map(field(descriptor, "lockfileIdentity")?)?;
    let raw = inputs
        .blob(digest(text(field(lock, "contentSha256")?)?)?)
        .map_err(DependencyInputError::Retained)?;
    let document = opensip_identity::parse_toml(raw.bytes()).map_err(DependencyLockError::Parse)?;
    let root = document.table();
    let parsed = root
        .get("version")
        .and_then(|v| v.as_integer())
        .ok_or(DependencyLockError::Shape("version"))?;
    let version = u8::from_str_radix(parsed.digits(), parsed.radix())
        .map_err(|_| DependencyLockError::Version)?;
    if !matches!(version, 3 | 4) || u64::from(version) != number(field(lock, "lockfileVersion")?)? {
        return Err(DependencyLockError::Version);
    }
    let mut by_tuple: BTreeMap<(&str, &str, &str), Vec<Option<&str>>> = BTreeMap::new();
    let mut lock_package_rows = 0;
    if let Some(value) = root.get("package") {
        let rows = value
            .as_array()
            .ok_or(DependencyLockError::Shape("package"))?;
        lock_package_rows = rows.len();
        for row in rows.iter() {
            let row = row
                .as_table()
                .ok_or(DependencyLockError::Shape("package.row"))?;
            let name = row
                .get("name")
                .and_then(|v| v.as_str())
                .ok_or(DependencyLockError::Shape("package.name"))?;
            let version = row
                .get("version")
                .and_then(|v| v.as_str())
                .ok_or(DependencyLockError::Shape("package.version"))?;
            let source = optional_lock_text(row, "source")?.unwrap_or("");
            let checksum = optional_lock_text(row, "checksum")?;
            by_tuple
                .entry((name, version, source))
                .or_default()
                .push(checksum);
        }
    }
    for (index, package) in array(field(descriptor, "packages")?)?.iter().enumerate() {
        let package = map(package)?;
        let key = (
            text(field(package, "name")?)?,
            text(field(package, "version")?)?,
            text(field(package, "sourceId")?)?,
        );
        let matches = by_tuple
            .get(&key)
            .ok_or(DependencyLockError::MissingTuple(index))?;
        if matches.len() != 1 {
            return Err(DependencyLockError::AmbiguousTuple(index));
        }
        let checksum = match field(package, "lockChecksum")? {
            JsonValue::Null => None,
            value => Some(text(value)?),
        };
        if matches[0] != checksum {
            return Err(DependencyLockError::Checksum(index));
        }
    }
    Ok(DependencyLockChecks {
        dependency,
        lockfile_version: version,
        lock_package_rows,
    })
}
#[derive(Debug)]
pub enum VendorChecksumError {
    Lock(DependencyLockError),
    Inputs(DependencyInputError),
    Json(opensip_identity::CanonicalError),
    SelectedPackage,
    VerificationDeclaration,
    PackageChecksum,
    FileMap,
}
impl From<DependencyInputError> for VendorChecksumError {
    fn from(value: DependencyInputError) -> Self {
        Self::Inputs(value)
    }
}
/// Declared DS-1 equality observations only; never an authentication token.
#[derive(Debug)]
pub struct VendorChecksumChecks {
    lock: DependencyLockChecks,
    package_index: usize,
    file_count: usize,
}
impl VendorChecksumChecks {
    pub fn lock_checks(&self) -> &DependencyLockChecks {
        &self.lock
    }
    pub fn package_index(&self) -> usize {
        self.package_index
    }
    pub fn file_count(&self) -> usize {
        self.file_count
    }
}

/// Compare one caller-selected retained checksum JSON blob to the exact selected
/// package lock checksum and complete retained file-manifest map (DS-1).
/// Mandatory universe/context/snapshot/dependency/member/lock joins run first.
/// The package must declare self-consistent and declared; this comparison never
/// promotes a rewritten tree to registry-authenticated, even when package agrees.
/// The JSON package field equals the non-null lockChecksum; files has exactly
/// the same path keys and content hashes as the retained H file manifest.
///
/// Caller owns selection of the .cargo-checksum.json source, acquisition/root
/// mapping, file inventory capture/completeness, and admission of all owners.
/// No metadata-file exclusion, packageKey codec, import/archive mapping or host
/// path read is inferred. The selected strict JSON parser's local bounds remain
/// parse errors, not product scope limits or wire causes. No DS-2 tarball/registry
/// authentication, DS-3 revision, DS-4 snapshot root, DS-6 activation completeness,
/// materialization, NativeContextVerified, provider, Plan/Run or qualification.
pub fn check_declared_vendor_checksum(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    package_index: usize,
    checksum_blob_sha256: [u8; 32],
    schema_work: usize,
) -> Result<VendorChecksumChecks, VendorChecksumError> {
    let lock = check_declared_lockfile_joins(inputs, request, schema_work)
        .map_err(VendorChecksumError::Lock)?;
    let frame = inputs
        .frame_candidate(
            lock.dependency_checks().dependency_digest(),
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let package = array(field(map(frame.descriptor())?, "packages")?)?
        .get(package_index)
        .ok_or(VendorChecksumError::SelectedPackage)?;
    let package = map(package)?;
    if text(field(package, "checksumVerification")?)? != "self-consistent"
        || text(field(package, "provenanceAssurance")?)? != "declared"
    {
        return Err(VendorChecksumError::VerificationDeclaration);
    }
    let JsonValue::String(checksum) = field(package, "lockChecksum")? else {
        return Err(VendorChecksumError::PackageChecksum);
    };
    let raw = inputs
        .blob(checksum_blob_sha256)
        .map_err(DependencyInputError::Retained)?;
    let json = opensip_identity::parse_json(raw.bytes()).map_err(VendorChecksumError::Json)?;
    let json = map(&json)?;
    if json.get("package") != Some(&JsonValue::String(checksum.clone())) {
        return Err(VendorChecksumError::PackageChecksum);
    }
    let JsonValue::Object(checksums) = json.get("files").ok_or(VendorChecksumError::FileMap)?
    else {
        return Err(VendorChecksumError::FileMap);
    };
    let manifest = inputs
        .frame_candidate(
            digest(text(field(package, "fileManifestSha256")?)?)?,
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let files = array(manifest.descriptor())?;
    if checksums.len() != files.len() {
        return Err(VendorChecksumError::FileMap);
    }
    for file in files {
        let file = map(file)?;
        if checksums.get(text(field(file, "path")?)?) != Some(field(file, "contentSha256")?) {
            return Err(VendorChecksumError::FileMap);
        }
    }
    Ok(VendorChecksumChecks {
        lock,
        package_index,
        file_count: files.len(),
    })
}

/// Locked raw bytes only, not an extracted or authenticated package tree.
#[derive(Debug)]
pub struct DeclaredCratePreimage {
    lock: DependencyLockChecks,
    package_index: usize,
    raw_bytes: std::sync::Arc<[u8]>,
}
impl DeclaredCratePreimage {
    pub fn lock_checks(&self) -> &DependencyLockChecks {
        &self.lock
    }
    pub fn package_index(&self) -> usize {
        self.package_index
    }
    pub fn raw_bytes(&self) -> &[u8] {
        &self.raw_bytes
    }
}
#[derive(Debug)]
pub enum CratePreimageError {
    Lock(DependencyLockError),
    Inputs(DependencyInputError),
    SelectedPackage,
    VerificationDeclaration,
    Checksum,
}
impl From<DependencyInputError> for CratePreimageError {
    fn from(value: DependencyInputError) -> Self {
        Self::Inputs(value)
    }
}

/// Retain a caller-selected raw .crate preimage whose SHA256 equals the actual
/// selected package lock checksum, after the mandatory declared lock/member
/// joins. Require tarball-matched/registry-authenticated declarations, but never
/// use those labels as proof. A hash match supplies immutable raw bytes only.
/// Caller owns actual source acquisition, registry authority, archive parsing,
/// deterministic extraction and equality of the extracted tree/file manifest.
/// No tar/header/compression/root/member policy or limit is invented here; even
/// hash-matched arbitrary bytes are only a declared preimage, not a .crate tree,
/// full DS-2 admission, NativeContextVerified, Plan/Run or provider authority.
pub fn retain_declared_crate_preimage(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    package_index: usize,
    crate_blob_sha256: [u8; 32],
    schema_work: usize,
) -> Result<DeclaredCratePreimage, CratePreimageError> {
    let lock = check_declared_lockfile_joins(inputs, request, schema_work)
        .map_err(CratePreimageError::Lock)?;
    let frame = inputs
        .frame_candidate(
            lock.dependency_checks().dependency_digest(),
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let package = array(field(map(frame.descriptor())?, "packages")?)?
        .get(package_index)
        .ok_or(CratePreimageError::SelectedPackage)?;
    let package = map(package)?;
    if text(field(package, "checksumVerification")?)? != "tarball-matched"
        || text(field(package, "provenanceAssurance")?)? != "registry-authenticated"
    {
        return Err(CratePreimageError::VerificationDeclaration);
    }
    let JsonValue::String(checksum) = field(package, "lockChecksum")? else {
        return Err(CratePreimageError::Checksum);
    };
    if digest(checksum)? != crate_blob_sha256 {
        return Err(CratePreimageError::Checksum);
    }
    let raw_bytes = std::sync::Arc::from(
        inputs
            .blob(crate_blob_sha256)
            .map_err(DependencyInputError::Retained)?
            .bytes(),
    );
    Ok(DeclaredCratePreimage {
        lock,
        package_index,
        raw_bytes,
    })
}

/// A regular member of caller-declared, already-inflated GNU tar bytes.
/// The content borrows those bytes; no extraction or filesystem path is made.
#[derive(Debug)]
pub struct DeclaredTarMember<'a> {
    path: opensip_identity::LogicalPath,
    content: &'a [u8],
}
impl DeclaredTarMember<'_> {
    pub fn path(&self) -> &str {
        self.path.as_str()
    }
    pub fn content(&self) -> &[u8] {
        self.content
    }
}
/// Local parser errors, never checksum-mismatch labels or public refusal codes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DeclaredTarError {
    Truncated,
    Header,
    Checksum,
    Size,
    EntryType,
    LongName,
    Path,
    Duplicate,
    EndRegion,
}

/// Observe profile CRATE-ARCHIVE-1's GNU tar members (C r7 item 12, rules
/// 2-6 and D2) in explicitly supplied inflated bytes. Results become available
/// only after the whole tar stream passes. Paths are sorted and unique; every
/// content slice retains its exact archive bytes. Ignored header metadata and
/// padding never enter this observation.
///
/// This does not prove these are the inflation of a locked .crate preimage.
/// It performs no gzip/header/trailer/CRC/ISIZE/D3 validation, streaming D1
/// guard, acquisition or admitted-set counter check, manifest identity/hash
/// join, materialization, activation, registry/provenance/import admission,
/// or NativeContextVerified/Plan/provider authorization. Those remain the
/// importer and full decoder's duties; M3-L's in-effect gate is unchanged.
pub fn observe_declared_tar_members<'a>(
    name: &str,
    version: &str,
    inflated: &'a [u8],
) -> Result<Vec<DeclaredTarMember<'a>>, DeclaredTarError> {
    use DeclaredTarError as E;
    // Caller supplies the exact lock tuple; it is not a directory or a path.
    let root = format!("{name}-{version}/");
    let mut offset = 0usize;
    let mut pending: Option<&[u8]> = None;
    let mut files = BTreeMap::new();
    loop {
        let header_end = offset.checked_add(512).ok_or(E::Truncated)?;
        let header = inflated.get(offset..header_end).ok_or(E::Truncated)?;
        if header.iter().all(|b| *b == 0) {
            let end = &inflated[offset..];
            if pending.is_some()
                || !(1024..=10240).contains(&end.len())
                || !end.len().is_multiple_of(512)
                || end.iter().any(|b| *b != 0)
            {
                return Err(E::EndRegion);
            }
            return Ok(files.into_values().collect());
        }
        if &header[257..263] != b"ustar " || &header[263..265] != b" \0" {
            return Err(E::Header);
        }
        let checksum = tar_octal(&header[148..156]).ok_or(E::Checksum)?;
        let sum: u64 = header
            .iter()
            .enumerate()
            .map(|(i, b)| u64::from(if (148..156).contains(&i) { b' ' } else { *b }))
            .sum();
        if checksum != sum {
            return Err(E::Checksum);
        }
        let size = tar_size(&header[124..136]).ok_or(E::Size)?;
        let size = usize::try_from(size).map_err(|_| E::Size)?;
        let kind = header[156];
        if pending.is_some() && kind != b'0' {
            return Err(E::LongName);
        }
        if kind != b'0' && kind != b'L' {
            return Err(E::EntryType);
        }
        // D2 is checked before touching or slicing a long-name payload.
        if kind == b'L' && !(2..=16385).contains(&size) {
            return Err(E::LongName);
        }
        let content_end = header_end.checked_add(size).ok_or(E::Size)?;
        let content = inflated.get(header_end..content_end).ok_or(E::Truncated)?;
        let padding = (512 - size % 512) % 512;
        offset = content_end.checked_add(padding).ok_or(E::Size)?;
        if offset > inflated.len() {
            return Err(E::Truncated);
        }
        let header_name = tar_name(&header[..100]);
        if kind == b'L' {
            if header_name != b"././@LongLink"
                || content.last() != Some(&0)
                || content[..size - 1].contains(&0)
            {
                return Err(E::LongName);
            }
            let path = &content[..size - 1];
            let path_text = std::str::from_utf8(path).map_err(|_| E::Path)?;
            if path_text.chars().take(4097).count() > 4096 {
                return Err(E::LongName);
            }
            pending = Some(path);
            continue;
        }
        let effective = match pending.take() {
            Some(long) => {
                if !long.starts_with(header_name) {
                    return Err(E::LongName);
                }
                long
            }
            None => header_name,
        };
        let effective = std::str::from_utf8(effective).map_err(|_| E::Path)?;
        let relative = effective.strip_prefix(&root).ok_or(E::Path)?;
        let path = opensip_identity::LogicalPath::parse(relative).map_err(|_| E::Path)?;
        let key = path.as_str().to_owned();
        if files
            .insert(key, DeclaredTarMember { path, content })
            .is_some()
        {
            return Err(E::Duplicate);
        }
    }
}
fn tar_name(field: &[u8]) -> &[u8] {
    &field[..field.iter().rposition(|b| *b != 0).map_or(0, |i| i + 1)]
}
fn tar_octal(field: &[u8]) -> Option<u64> {
    let first = field.iter().position(|b| *b != 0 && *b != b' ')?;
    let last = field.iter().rposition(|b| *b != 0 && *b != b' ')?;
    field[first..=last].iter().try_fold(0u64, |n, b| {
        if !(b'0'..=b'7').contains(b) {
            return None;
        }
        n.checked_mul(8)?.checked_add(u64::from(*b - b'0'))
    })
}
fn tar_size(field: &[u8]) -> Option<u64> {
    if field.first()? & 0x80 == 0 {
        return tar_octal(field);
    }
    // GNU positive base-256 only above the 11-octal-digit size range.
    // Negative or out-of-u64 values cannot describe a borrowed content slice.
    if field[0] & 0x40 != 0 {
        return None;
    }
    let value = field.iter().enumerate().try_fold(0u64, |n, (i, b)| {
        n.checked_mul(256)?
            .checked_add(u64::from(if i == 0 { *b & 0x7f } else { *b }))
    })?;
    (value > 0o77777777777).then_some(value)
}

/// An exact declared inflated-member / retained-manifest byte join only.
#[derive(Debug)]
pub struct DeclaredTarManifest<'a> {
    lock: DependencyLockChecks,
    package_index: usize,
    members: Vec<DeclaredTarMember<'a>>,
}
impl DeclaredTarManifest<'_> {
    pub fn lock_checks(&self) -> &DependencyLockChecks {
        &self.lock
    }
    pub fn package_index(&self) -> usize {
        self.package_index
    }
    pub fn members(&self) -> &[DeclaredTarMember<'_>] {
        &self.members
    }
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
    fn from(value: DependencyInputError) -> Self {
        Self::Inputs(value)
    }
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
    let frame = inputs
        .frame_candidate(
            lock.dependency_checks().dependency_digest(),
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let package = array(field(map(frame.descriptor())?, "packages")?)?
        .get(package_index)
        .ok_or(E::SelectedPackage)?;
    let package = map(package)?;
    let members = observe_declared_tar_members(
        text(field(package, "name")?)?,
        text(field(package, "version")?)?,
        inflated,
    )
    .map_err(E::Tar)?;
    let manifest = inputs
        .frame_candidate(
            digest(text(field(package, "fileManifestSha256")?)?)?,
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    // The mandatory dependency check has already checked the exact domain,
    // registered shape, ordering, count/sum and all retained raw member bytes.
    let rows = array(manifest.descriptor())?;
    if rows.len() != members.len() {
        return Err(E::Mismatch { field: "fileCount" });
    }
    for (row, member) in rows.iter().zip(&members) {
        let row = map(row)?;
        if text(field(row, "path")?)? != member.path() {
            return Err(E::Mismatch { field: "path" });
        }
        let length = u64::try_from(member.content().len())
            .map_err(|_| DependencyInputError::CountOverflow)?;
        if number(field(row, "byteLength")?)? != length {
            return Err(E::Mismatch {
                field: "byteLength",
            });
        }
        if digest(text(field(row, "contentSha256")?)?)?
            != opensip_identity::raw_sha256(member.content())
        {
            return Err(E::Mismatch {
                field: "contentSha256",
            });
        }
    }
    Ok(DeclaredTarManifest {
        lock,
        package_index,
        members,
    })
}

fn optional_lock_text<'a>(
    row: opensip_identity::TomlTableView<'a>,
    name: &'static str,
) -> Result<Option<&'a str>, DependencyLockError> {
    row.get(name)
        .map(|v| v.as_str().ok_or(DependencyLockError::Shape(name)))
        .transpose()
}

fn retain_blob(
    inputs: &RetainedInputs<'_>,
    sha: [u8; 32],
    bytes: u64,
    checked: &mut BTreeMap<[u8; 32], u64>,
) -> Result<(), DependencyInputError> {
    if let Some(previous) = checked.get(&sha) {
        if *previous != bytes {
            return Err(DependencyInputError::Retained(
                RetainedInputError::BlobLength,
            ));
        }
    } else {
        inputs
            .blob(sha)
            .map_err(DependencyInputError::Retained)?
            .require_length(bytes)
            .map_err(DependencyInputError::Retained)?;
        checked.insert(sha, bytes);
    }
    Ok(())
}
fn map(value: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, DependencyInputError> {
    match value {
        JsonValue::Object(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn field<'a>(
    value: &'a BTreeMap<String, JsonValue>,
    name: &str,
) -> Result<&'a JsonValue, DependencyInputError> {
    value.get(name).ok_or(DependencyInputError::Representation)
}
fn text(value: &JsonValue) -> Result<&str, DependencyInputError> {
    match value {
        JsonValue::String(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn array(value: &JsonValue) -> Result<&[JsonValue], DependencyInputError> {
    match value {
        JsonValue::Array(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn number(value: &JsonValue) -> Result<u64, DependencyInputError> {
    match value {
        JsonValue::Integer(value) => {
            u64::try_from(value.get()).map_err(|_| DependencyInputError::Representation)
        }
        _ => Err(DependencyInputError::Representation),
    }
}
fn digest(value: &str) -> Result<[u8; 32], DependencyInputError> {
    if value.len() != 64 {
        return Err(DependencyInputError::Representation);
    }
    let mut result = [0; 32];
    for (index, pair) in value.as_bytes().chunks_exact(2).enumerate() {
        let digit = |value| match value {
            b'0'..=b'9' => Ok(value - b'0'),
            b'a'..=b'f' => Ok(value - b'a' + 10),
            _ => Err(DependencyInputError::Representation),
        };
        result[index] = digit(pair[0])? << 4 | digit(pair[1])?;
    }
    Ok(result)
}

#[cfg(test)]
#[path = "dependency_inputs_tests.rs"]
mod tests;
