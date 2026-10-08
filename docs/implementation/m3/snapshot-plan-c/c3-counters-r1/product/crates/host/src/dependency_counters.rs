//! Pure counter arithmetic for MC8 item 12, rule 7.
//!
//! These crate-private observations do not prove source custody, completion,
//! admission, activation, canonical candidate/file order or import permission.
//! The importer owns those decisions and must enforce them before using totals.
//! Acquisition counts include acquired data even for later-rejected candidates.
//! Final counts come only from complete admitted activated non-path manifests.

const GIB: u128 = 1 << 30;
const ACQUISITION_LIMITS: Totals = Totals {
    sources: 16_384,
    files: 4_000_000,
    content: 32 * GIB,
};
const FINAL_LIMITS: Totals = Totals {
    sources: 4_096,
    files: 1_000_000,
    content: 8 * GIB,
};

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub(crate) struct Totals {
    pub(crate) sources: u128,
    pub(crate) files: u128,
    pub(crate) content: u128,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Field {
    Sources,
    Files,
    Content,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct Bound {
    pub(crate) field: Field,
    pub(crate) observed: u128,
    pub(crate) limit: u128,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum AcquisitionError {
    ArithmeticOverflow,
    Bound(Bound),
}

/// Consumed on every charge. A refused charge leaves no usable accumulator.
/// The caller owns canonical candidate order and route-specific file order.
#[derive(Debug)]
pub(crate) struct Acquisition(Totals);

impl Acquisition {
    pub(crate) fn new() -> Self {
        Self(Totals::default())
    }

    /// Charge one actually supplied non-path candidate before its file events.
    pub(crate) fn source(self) -> Result<Self, AcquisitionError> {
        self.charge(Totals {
            sources: 1,
            files: 0,
            content: 0,
        })
    }

    /// Charge one observed logical file and its actual complete content length.
    /// Never supply a tar header's announced length as an observed file.
    /// Actual streaming read bounds are a separate importer responsibility.
    pub(crate) fn file(self, content: u128) -> Result<Self, AcquisitionError> {
        self.charge(Totals {
            sources: 0,
            files: 1,
            content,
        })
    }

    fn charge(self, delta: Totals) -> Result<Self, AcquisitionError> {
        let next = self
            .0
            .checked_add(delta)
            .ok_or(AcquisitionError::ArithmeticOverflow)?;
        // The selected acquisition precedence is sources, files, content.
        if let Some(bound) = next
            .crossings(ACQUISITION_LIMITS)
            .into_iter()
            .flatten()
            .next()
        {
            return Err(AcquisitionError::Bound(bound));
        }
        Ok(Self(next))
    }

    pub(crate) fn totals(self) -> Totals {
        self.0
    }
}

/// Complete final totals that prove one or more final-set crossings.
/// Carries no source or population admission authority.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct FinalExcess(Totals);
impl FinalExcess {
    pub(crate) fn bounds(self) -> [Option<Bound>; 3] {
        self.0.crossings(FINAL_LIMITS)
    }
}

/// Exact arithmetic over supplied final-population observations only.
/// No boolean admission/activation labels are accepted as authority here.
#[derive(Debug)]
pub(crate) struct FinalPopulation(Totals);

impl FinalPopulation {
    pub(crate) fn new() -> Self {
        Self(Totals::default())
    }

    /// The owning importer must already have established actual admission,
    /// activation, non-path classification, and complete file-manifest counts.
    /// No protocol limit is applied while this final population is assembled.
    pub(crate) fn package(self, files: u128, content: u128) -> Option<Self> {
        self.0
            .checked_add(Totals {
                sources: 1,
                files,
                content,
            })
            .map(Self)
    }

    /// One final check; report all proven crossings without inventing a
    /// multi-field public failure precedence. Array slots identify fields.
    pub(crate) fn check(self) -> Result<Totals, FinalExcess> {
        let crossings = self.0.crossings(FINAL_LIMITS);
        if crossings.iter().any(Option::is_some) {
            Err(FinalExcess(self.0))
        } else {
            Ok(self.0)
        }
    }
}

impl Totals {
    fn checked_add(self, other: Self) -> Option<Self> {
        Some(Self {
            sources: self.sources.checked_add(other.sources)?,
            files: self.files.checked_add(other.files)?,
            content: self.content.checked_add(other.content)?,
        })
    }

    fn crossings(self, limits: Self) -> [Option<Bound>; 3] {
        let rows = [
            (Field::Sources, self.sources, limits.sources),
            (Field::Files, self.files, limits.files),
            (Field::Content, self.content, limits.content),
        ];
        rows.map(|(field, observed, limit)| {
            (observed > limit).then_some(Bound {
                field,
                observed,
                limit,
            })
        })
    }
}

#[cfg(test)]
#[path = "dependency_counters_tests.rs"]
mod tests;
