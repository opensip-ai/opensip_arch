// Native OS measurements composed with an already verified profile, under a
// borrowed supplied installation fence. Still conditional on the profile's root,
// core pin and revocation inputs, selected installation/actor and launch TCB.
use super::{
    PlatformDecision, PlatformError, ProfileSetEvidence, platform_decision, platform_profile,
};
use crate::custody::installation_fence::{self, SuppliedInstallationFence};
use opensip_identity::JsonValue as V;
use opensip_platform::{
    DescriptorFilesystem, MacosBootError, MacosBootObservation, MacosLoaderError,
    MacosLoaderObservation, MacosProcessError, MacosProcessObservation, capture_system_loader,
    observe_macos_boot, observe_macos_process,
};
use std::{collections::BTreeMap, io};
#[derive(Debug)]
pub(super) enum Error {
    Fence(installation_fence::Error),
    Boot(MacosBootError),
    Loader(MacosLoaderError),
    Process(MacosProcessError),
    Native(io::Error),
    Decision(PlatformError),
    UnsupportedPopulation,
    UnsupportedFilesystem,
    Changed,
}
pub(super) struct NativePlatformEvidence<'f> {
    fence: &'f SuppliedInstallationFence,
    profile: ProfileSetEvidence,
    boot: MacosBootObservation,
    process: MacosProcessObservation,
    loader: MacosLoaderObservation,
    install_fs: DescriptorFilesystem,
    loader_fs: DescriptorFilesystem,
    observed: V,
    decision: PlatformDecision,
}
fn machine(process: MacosProcessObservation, cpu: u32) -> Result<&'static str, Error> {
    if process == MacosProcessObservation::Translated {
        return Err(Error::UnsupportedPopulation);
    }
    // CPU comes from the independently parsed fixed loader slice, and must match
    // the native process family. No display aliases or caller platform labels.
    match (std::env::consts::ARCH, cpu) {
        ("aarch64", 0x0100000c) => Ok("macos-aarch64"),
        ("x86_64", 0x01000007) => Ok("macos-x86_64"),
        _ => Err(Error::UnsupportedPopulation),
    }
}
fn filesystems(install: &DescriptorFilesystem, loader: &DescriptorFilesystem) -> Result<(), Error> {
    if !install.is_local()
        || install.is_union()
        || !loader.is_local()
        || loader.is_union()
        || !loader.is_read_only()
        || loader.name() != b"apfs"
    {
        return Err(Error::UnsupportedFilesystem);
    }
    Ok(())
}
// Undefined/unspecified IDs cannot establish a shared mounted filesystem.
fn usable_filesystem_id(id: [i32; 2]) -> bool {
    id != [0, 0] && id != [-1, -1]
}
impl NativePlatformEvidence<'_> {
    pub(super) fn qualifies_installation_filesystem(&self, fs: &DescriptorFilesystem) -> bool {
        if !self.decision.refusals.is_empty()
            || !fs.is_local()
            || fs.is_union()
            || fs.device() != self.install_fs.device()
            || !usable_filesystem_id(fs.native_id())
            || fs.native_id() != self.install_fs.native_id()
        {
            return false;
        }
        let Some(id) = self.decision.platform.as_deref() else {
            return false;
        };
        let Some(name) = std::str::from_utf8(fs.name()).ok() else {
            return false;
        };
        super::object(self.profile.envelope().payload())
            .and_then(|p| p.get("platforms"))
            .and_then(super::object)
            .and_then(|p| p.get(id))
            .and_then(super::object)
            .and_then(|p| p.get("installRootFilesystems"))
            .and_then(super::array)
            .is_some_and(|filesystems| filesystems.iter().any(|v| super::string(v) == Some(name)))
    }
    pub(super) fn observed(&self) -> &V {
        &self.observed
    }
    pub(super) fn decision(&self) -> &PlatformDecision {
        &self.decision
    }
    pub(super) fn profile(&self) -> &ProfileSetEvidence {
        &self.profile
    }
    pub(super) fn process(&self) -> MacosProcessObservation {
        self.process
    }
    pub(super) fn loader(&self) -> &MacosLoaderObservation {
        &self.loader
    }
    pub(super) fn install_filesystem(&self) -> &DescriptorFilesystem {
        &self.install_fs
    }
    pub(super) fn standing(&self) -> &'static str {
        "Native sequential OS samples under supplied installation fence; profile root/core/revocation provenance and launch TCB remain conditional; not current authority or a write grant. Sealed-volume loaded-image equivalence is a platform premise, not independently proved. Full versus Reduced Security is not distinguished."
    }
    /// Re-sample before consuming; retained handles plus cooperative exclusion
    /// do not create an atomic OS snapshot or defeat hostile trusted code/ABA.
    pub(super) fn recheck(&self) -> Result<(), Error> {
        self.fence.recheck().map_err(Error::Fence)?;
        self.loader.recheck().map_err(Error::Loader)?;
        let process = observe_macos_process().map_err(Error::Process)?;
        let boot = observe_macos_boot().map_err(Error::Boot)?;
        let install = self
            .fence
            .root()
            .directory()
            .observe_filesystem()
            .map_err(Error::Native)?;
        let loader = self.loader.filesystem().map_err(Error::Native)?;
        machine(process, self.loader.cpu())?;
        filesystems(&install, &loader)?;
        if process != self.process
            || boot != self.boot
            || install != self.install_fs
            || loader != self.loader_fs
        {
            return Err(Error::Changed);
        }
        self.loader.recheck().map_err(Error::Loader)?;
        self.fence.recheck().map_err(Error::Fence)
    }
}
pub(super) fn capture<'f>(
    profile: ProfileSetEvidence,
    fence: &'f SuppliedInstallationFence,
) -> Result<NativePlatformEvidence<'f>, Error> {
    capture_with(profile, fence, || {})
}
fn capture_with<'f>(
    profile: ProfileSetEvidence,
    fence: &'f SuppliedInstallationFence,
    after_sample: impl FnOnce(),
) -> Result<NativePlatformEvidence<'f>, Error> {
    fence.recheck().map_err(Error::Fence)?;
    let process = observe_macos_process().map_err(Error::Process)?;
    if process == MacosProcessObservation::Translated {
        return Err(Error::UnsupportedPopulation);
    }
    let boot = observe_macos_boot().map_err(Error::Boot)?;
    let loader = capture_system_loader().map_err(Error::Loader)?;
    let platform = machine(process, loader.cpu())?;
    let install_fs = fence
        .root()
        .directory()
        .observe_filesystem()
        .map_err(Error::Native)?;
    let loader_fs = loader.filesystem().map_err(Error::Native)?;
    filesystems(&install_fs, &loader_fs)?;
    let fs_type =
        std::str::from_utf8(install_fs.name()).map_err(|_| Error::UnsupportedFilesystem)?;
    let observed = V::Object(BTreeMap::from([
        ("platform".into(), V::String(platform.into())),
        ("fsType".into(), V::String(fs_type.into())),
        (
            "authenticatedRoot".into(),
            V::String(
                if boot.unauthenticated_root_allowed() {
                    "disabled"
                } else {
                    "enabled"
                }
                .into(),
            ),
        ),
        (
            "sip".into(),
            V::Bool(!boot.unrestricted_filesystem_allowed()),
        ),
        ("osversion".into(), V::String(boot.os_build().into())),
        ("kernUuid".into(), V::String(boot.kernel_uuid().into())),
        (
            "dyldCdhash".into(),
            V::String(loader.cdhash().iter().map(|b| format!("{b:02x}")).collect()),
        ),
    ]));
    let decision = platform_decision(
        platform_profile::AdmittedProfile::from_verified(&profile),
        &observed,
    )
    .map_err(Error::Decision)?;
    let result = NativePlatformEvidence {
        fence,
        profile,
        boot,
        process,
        loader,
        install_fs,
        loader_fs,
        observed,
        decision,
    };
    after_sample();
    result.recheck()?;
    Ok(result)
}
#[cfg(test)]
mod tests {
    use super::super::{
        PlatformTier, admit, admitted_profiles, array, decode_hex32, object, string,
    };
    use super::*;
    use opensip_identity::{digest_hex, parse_json, raw_sha256};
    use opensip_platform::RetainedDirectoryPath;
    use std::{
        collections::BTreeSet,
        fs::{self, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt},
        path::PathBuf,
        sync::Arc,
    };
    fn bytes(v: &V) -> Vec<u8> {
        string(v)
            .unwrap()
            .as_bytes()
            .chunks_exact(2)
            .map(|b| u8::from_str_radix(std::str::from_utf8(b).unwrap(), 16).unwrap())
            .collect()
    }
    fn profile() -> ProfileSetEvidence {
        let q = include_bytes!("../../tests/fixtures/profile-signature-cases.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
            .map(|b| parse_json(b).unwrap())
            .find(|v| {
                object(&object(v).unwrap()["expected"])
                    .unwrap()
                    .contains_key("admit")
            })
            .unwrap();
        let q = object(&q).unwrap();
        let roots = parse_json(include_bytes!("../../tests/fixtures/profile-roots.json")).unwrap();
        let root = admit(
            &object(&roots).unwrap()[string(&q["root"]).unwrap()],
            [true, true],
        )
        .unwrap();
        let revoked = array(&q["revoked"])
            .unwrap()
            .iter()
            .map(|v| decode_hex32(string(v).unwrap()).unwrap())
            .collect();
        admitted_profiles::verify_profile_set(
            &root,
            &bytes(&q["stored"]),
            &q["envelope"],
            Some(decode_hex32(string(&q["corePin"]).unwrap()).unwrap()),
            &revoked,
        )
        .unwrap()
    }
    struct Fixture {
        root: PathBuf,
        path: Arc<RetainedDirectoryPath>,
        uid: u32,
    }
    impl Fixture {
        fn new() -> Self {
            let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
            let root = std::env::temp_dir().join(format!("opensip-native-platform-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let root = fs::canonicalize(root).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            fs::write(root.join("lifecycle.fence"), b"").unwrap();
            fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600))
                .unwrap();
            let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
            Self { root, path, uid }
        }
        fn fence(&self) -> SuppliedInstallationFence {
            SuppliedInstallationFence::try_acquire(
                Arc::clone(&self.path),
                self.uid,
                &BTreeSet::new(),
            )
            .unwrap()
            .unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn native_platform_actual_observations_join_existing_signed_synthetic_profile() {
        let f = Fixture::new();
        let fence = f.fence();
        let evidence = capture(profile(), &fence).unwrap();
        let o = object(evidence.observed()).unwrap();
        assert_eq!(o.len(), 7);
        let boot = observe_macos_boot().unwrap();
        assert_eq!(o["kernUuid"], V::String(boot.kernel_uuid().into()));
        assert_eq!(o["osversion"], V::String(boot.os_build().into()));
        assert_eq!(o["sip"], V::Bool(!boot.unrestricted_filesystem_allowed()));
        assert_eq!(
            o["authenticatedRoot"],
            V::String(
                if boot.unauthenticated_root_allowed() {
                    "disabled"
                } else {
                    "enabled"
                }
                .into()
            )
        );
        assert_eq!(
            o["dyldCdhash"],
            V::String(
                evidence
                    .loader()
                    .cdhash()
                    .iter()
                    .map(|b| format!("{b:02x}"))
                    .collect()
            )
        );
        assert_eq!(
            o["fsType"],
            V::String(
                std::str::from_utf8(evidence.install_filesystem().name())
                    .unwrap()
                    .into()
            )
        );
        assert_eq!(evidence.process(), observe_macos_process().unwrap());
        assert_eq!(
            object(evidence.profile().envelope().payload()).unwrap()["standing"],
            V::String("SYNTHETIC".into())
        );
        assert!(evidence.standing().contains("not current authority"));
        let pure = platform_decision(
            platform_profile::AdmittedProfile::from_verified(evidence.profile()),
            evidence.observed(),
        )
        .unwrap();
        assert_eq!(evidence.decision().tier, pure.tier);
        assert_eq!(evidence.decision().refusals, pure.refusals);
        assert_eq!(evidence.decision().drift, pure.drift);
        println!(
            "native profile observation={:?}; decision={:?}; synthetic fixture only",
            evidence.observed(),
            evidence.decision()
        );
        evidence.recheck().unwrap();
    }
    #[test]
    fn native_platform_translation_and_wrong_cpu_never_name_native_lane() {
        for cpu in [0, 0x01000007, 0x0100000c] {
            assert!(machine(MacosProcessObservation::Translated, cpu).is_err());
        }
        assert!(machine(MacosProcessObservation::NativeReported, 0).is_err());
        let (cpu, other, id) = if cfg!(target_arch = "aarch64") {
            (0x0100000c, 0x01000007, "macos-aarch64")
        } else {
            (0x01000007, 0x0100000c, "macos-x86_64")
        };
        for process in [
            MacosProcessObservation::NativeReported,
            MacosProcessObservation::NativeSelectorAbsent,
        ] {
            assert_eq!(machine(process, cpu).unwrap(), id);
            assert!(machine(process, other).is_err());
        }
    }
    #[test]
    fn native_platform_fence_changes_during_sample_refuse_before_return() {
        for mode in [0o666, 0o600] {
            let f = Fixture::new();
            let fence = f.fence();
            let r = capture_with(profile(), &fence, || {
                if mode == 0o600 {
                    fs::rename(f.root.join("lifecycle.fence"), f.root.join("old-fence")).unwrap();
                    fs::write(f.root.join("lifecycle.fence"), b"").unwrap();
                }
                fs::set_permissions(f.root.join("lifecycle.fence"), Permissions::from_mode(mode))
                    .unwrap();
            });
            assert!(r.is_err());
        }
    }
    #[test]
    fn native_platform_later_root_or_carrier_changes_invalidate_evidence() {
        for root in [false, true] {
            let f = Fixture::new();
            let fence = f.fence();
            let evidence = capture(profile(), &fence).unwrap();
            let path = if root {
                f.root.clone()
            } else {
                f.root.join("lifecycle.fence")
            };
            fs::set_permissions(&path, Permissions::from_mode(0o777)).unwrap();
            assert!(evidence.recheck().is_err());
        }
    }
    #[test]
    fn native_platform_existing_profile_refusals_are_not_tier_grants() {
        let f = Fixture::new();
        let fence = f.fence();
        let evidence = capture(profile(), &fence).unwrap();
        // Pure decision exercise only. These altered observations cannot enter
        // capture(), whose sole inputs are verified profile and retained fence.
        for (field, value, refusal) in [
            (
                "fsType",
                V::String("devfs".into()),
                "NT-TCB-BOOT:INSTALL_ROOT_FS",
            ),
            ("sip", V::Bool(false), "NT-TCB-BOOT:SIP_DISABLED"),
            (
                "authenticatedRoot",
                V::String("disabled".into()),
                "NT-TCB-BOOT:AUTHENTICATED_ROOT_DISABLED",
            ),
            (
                "dyldCdhash",
                V::String("0".repeat(40)),
                "NT-TCB-IDENTITY:dyldCdhash",
            ),
        ] {
            let mut o = object(evidence.observed()).unwrap().clone();
            o.insert(field.into(), value);
            // Fix exact-build fixture values so host upgrades do not make this
            // pure semantic test accidentally select BASELINE-ATTESTED.
            let platforms =
                object(&object(evidence.profile().envelope().payload()).unwrap()["platforms"])
                    .unwrap();
            let selected = object(&platforms[string(&o["platform"]).unwrap()]).unwrap();
            let measured = object(&array(&selected["measuredProfiles"]).unwrap()[0]).unwrap();
            o.insert("osversion".into(), measured["build"].clone());
            if field != "dyldCdhash" {
                o.insert("dyldCdhash".into(), measured["dyldCdhash"].clone());
            }
            o.insert("kernUuid".into(), measured["kernUuid"].clone());
            let d = platform_decision(
                platform_profile::AdmittedProfile::from_verified(evidence.profile()),
                &V::Object(o),
            )
            .unwrap();
            assert!(d.refusals.iter().any(|s| s == refusal), "{field}: {d:?}");
            if field == "dyldCdhash" {
                assert_eq!(d.tier, Some(PlatformTier::ExactMeasured));
                assert!(d.lane.is_none());
            }
        }
    }
    #[test]
    fn native_platform_loader_requires_readonly_apfs_and_saved_samples_are_checked() {
        let f = Fixture::new();
        let fence = f.fence();
        let mut evidence = capture(profile(), &fence).unwrap();
        let dev = RetainedDirectoryPath::open(std::path::Path::new("/dev"), 128)
            .unwrap()
            .directory()
            .observe_filesystem()
            .unwrap();
        assert_ne!(dev.name(), b"apfs");
        assert!(filesystems(&evidence.install_fs, &dev).is_err());
        assert!(!evidence.install_fs.is_read_only());
        assert!(filesystems(&evidence.install_fs, &evidence.install_fs).is_err());
        let old = evidence.install_fs.clone();
        evidence.install_fs = dev;
        assert!(matches!(evidence.recheck(), Err(Error::Changed)));
        evidence.install_fs = old;
        evidence.recheck().unwrap();
        evidence.process = match evidence.process {
            MacosProcessObservation::NativeReported => {
                MacosProcessObservation::NativeSelectorAbsent
            }
            _ => MacosProcessObservation::NativeReported,
        };
        assert!(matches!(evidence.recheck(), Err(Error::Changed)));
    }
    #[test]
    fn native_platform_filesystem_id_refuses_unspecified_without_restricting_signed_words() {
        assert!(!usable_filesystem_id([0, 0]));
        assert!(!usable_filesystem_id([-1, -1]));
        for id in [[16777232, 26], [i32::MIN, 26], [-1, 26], [0, 26], [1, -1]] {
            assert!(usable_filesystem_id(id));
        }
    }
}
