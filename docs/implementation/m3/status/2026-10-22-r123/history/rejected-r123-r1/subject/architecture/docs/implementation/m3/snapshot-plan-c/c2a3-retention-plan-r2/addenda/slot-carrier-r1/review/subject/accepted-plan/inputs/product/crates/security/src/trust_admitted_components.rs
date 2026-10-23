// M3-C r8 item 7 (unit C2a-1; C2a plan r4, section 2's C2a-1 row and
// LD-C2A-10): the trust owner's read-only bridge to the components the
// ordinary reader verified. Each one lends its authenticated body bytes, its
// validated manifest, its catalog release row and its verified envelope, by
// reference: nothing is copied, re-verified or charged again. Only the trust
// owner constructs one, so a caller cannot assert a manifest, a body or a
// release row of its own.
use super::component_manifest::Validated;
use opensip_identity::JsonValue as V;

/// One verified component, borrowed from the ordinary reader's evidence.
/// It is not Clone, Default or serializable, and authorizes nothing: it is
/// the input of `component_closure`'s unadmitted candidate.
pub struct AuthenticatedComponent<'a> {
    path: &'a str,
    body: &'a [u8],
    envelope: &'a [u8],
    manifest: &'a Validated,
    release: &'a V,
}
impl<'a> AuthenticatedComponent<'a> {
    pub(in crate::trust) fn new(
        path: &'a str,
        body: &'a [u8],
        envelope: &'a [u8],
        manifest: &'a Validated,
        release: &'a V,
    ) -> Self {
        Self {
            path,
            body,
            envelope,
            manifest,
            release,
        }
    }
    /// The catalog member path of the manifest.
    pub fn path(&self) -> &'a str {
        self.path
    }
    /// The authenticated body bytes, excluding the signature envelope.
    pub fn body(&self) -> &'a [u8] {
        self.body
    }
    /// The verified signature envelope's raw bytes.
    pub fn envelope(&self) -> &'a [u8] {
        self.envelope
    }
    /// The validated manifest value.
    pub fn manifest(&self) -> &'a V {
        self.manifest.value()
    }
    /// CR-1's kind for the manifest's role (`component_manifest.rs`), the
    /// only source of a component closure's kind (LD-C2A-2).
    pub fn closure_kind(&self) -> &'static str {
        self.manifest.closure_kind()
    }
    /// The catalog release row the ordinary reader joined to the manifest.
    pub fn release(&self) -> &'a V {
        self.release
    }
}

/// D4-2 (M3-D r5 item 24; D4 plan r2, LD-D4-2, LD-D4-3 and LD-D4-13): what
/// R10a's excluded-form judge reads from the trust view. It holds every
/// verified component as C2a-1's bridge lends it, so a component's
/// provenance is its catalog release row, the root-authenticated
/// association the ordinary reader joined, never a caller's assertion. It
/// also borrows the reserved root-command list that reader validated every
/// manifest against. Only the trust owner builds one (and, under the joint
/// fixture predicate, a test); it is not Clone and authorizes nothing.
pub struct AdmissionView<'a> {
    components: Vec<AuthenticatedComponent<'a>>,
    reserved: &'a std::collections::BTreeSet<String>,
}
/// The view's one allocation: the component list, reserved for exactly `n`.
pub const fn admission_view_cost(n: usize) -> opensip_platform::WorkCost {
    opensip_platform::WorkCost {
        objects: 1,
        edges: 0,
        bytes: n.saturating_mul(size_of::<AuthenticatedComponent<'static>>()),
    }
}
impl<'a> AdmissionView<'a> {
    /// The list is charged before it is allocated; each component is moved
    /// in, never copied.
    pub(in crate::trust) fn collect(
        n: usize,
        components: impl Iterator<Item = AuthenticatedComponent<'a>>,
        reserved: &'a std::collections::BTreeSet<String>,
        work: &mut opensip_platform::WorkScope<'_>,
    ) -> Result<Self, opensip_platform::WorkFailure<()>> {
        work.charge::<()>(admission_view_cost(n))?;
        let mut list = Vec::with_capacity(n);
        list.extend(components.take(n));
        Ok(Self {
            components: list,
            reserved,
        })
    }
    /// The verified components, in catalog order.
    pub fn components(&self) -> &[AuthenticatedComponent<'a>] {
        &self.components
    }
    /// The reserved root-command list, ascending (a `BTreeSet`'s order).
    pub fn reserved_roots(&self) -> impl ExactSizeIterator<Item = &'a str> + 'a {
        self.reserved.iter().map(String::as_str)
    }
    /// The borrowed set itself, for D4-2's identity control.
    #[cfg(test)]
    pub(crate) fn reserved_set(&self) -> &'a std::collections::BTreeSet<String> {
        self.reserved
    }
    /// A test view over fixture components and a supplied reserved list,
    /// under the joint fixture predicate only: the host's adapter tests
    /// drive the same public view the trust owner builds.
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    pub fn fixture(
        components: Vec<AuthenticatedComponent<'a>>,
        reserved: &'a std::collections::BTreeSet<String>,
    ) -> Self {
        Self {
            components,
            reserved,
        }
    }
}

/// A test holder for one component whose body went through the real body
/// validation (`component_manifest::validate`, with the default host
/// context). It skips no check of the body; its release row and envelope are
/// the test's own, standing in for the ordinary reader's joins, which C2a-2's
/// signed fixtures exercise end to end. Shared fixture gate 7 (law CI r5
/// item 6, unit CI-2): the component installer's and the retained-tree
/// reader's fixtures in opensip-lifecycle build their evidence with it.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub struct TestComponent {
    body: Vec<u8>,
    envelope: Vec<u8>,
    manifest: Validated,
    release: V,
}
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
impl TestComponent {
    pub fn new(body: Vec<u8>, envelope: Vec<u8>, release: V) -> Option<Self> {
        let manifest = super::component_manifest::validate(
            &body,
            &super::component_manifest::Context::default(),
        )
        .ok()?;
        Some(Self {
            body,
            envelope,
            manifest,
            release,
        })
    }
    pub fn authenticated(&self) -> AuthenticatedComponent<'_> {
        AuthenticatedComponent::new(
            "components/test/payload.json",
            &self.body,
            &self.envelope,
            &self.manifest,
            &self.release,
        )
    }
}

/// Unit D4-2's fixture components (under the joint fixture predicate only):
/// `admission_fixture_bodies`' six role-valid bodies, each through the real
/// body validation, with a release row of exactly the fields R10a's judge
/// reads, taken from the body itself: `manifestDigest` (its raw SHA-256),
/// `publisher` and `sourceClass`. The envelope is empty: these stand in for
/// the ordinary reader's joins, which the security owner's own D4-2 control
/// runs end to end.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub fn admission_fixture_components() -> Vec<TestComponent> {
    super::root_payload::admission_fixture_bodies()
        .into_iter()
        .map(|body| {
            let value = opensip_identity::parse_json(&body).unwrap();
            let V::Object(m) = &value else { unreachable!() };
            let V::Object(provenance) = &m["provenance"] else {
                unreachable!()
            };
            let digest =
                opensip_identity::digest_hex(&opensip_identity::raw_sha256(&body)).to_owned();
            let release = V::Object(
                [
                    ("manifestDigest".to_owned(), V::String(digest)),
                    ("publisher".to_owned(), provenance["publisher"].clone()),
                    ("sourceClass".to_owned(), provenance["sourceClass"].clone()),
                ]
                .into_iter()
                .collect(),
            );
            TestComponent::new(body, Vec::new(), release).unwrap()
        })
        .collect()
}
