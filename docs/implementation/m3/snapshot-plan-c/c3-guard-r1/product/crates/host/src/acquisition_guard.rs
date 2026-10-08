//! C3CB-1 logical acquisition guard for the existing private archive decoder.
//!
//! Actual reader/decoder callbacks establish only provisional observations.
//! The importer still owns canonical ordering, supplied non-path source and lock
//! correspondence, custody/quarantine commit, admission and final activation.
//! Fixed physical buffers and raw/inflated work keep the decoder's own counters.

use crate::archive_decoder::{self, ArchiveConsumer, DecodeError, DecodedArchive, FileRecord};
use crate::dependency_counters::{Bound, Field, Totals};
use opensip_identity::LogicalPath;
use std::io;

const SOURCES: u128 = 16_384;
const FILES: u128 = 4_000_000;
const CONTENT: u128 = 32 * (1 << 30);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Stop {
    Bound(Bound),
    Aborted,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum BudgetError {
    Bound(Bound),
    Unavailable,
}

#[derive(Debug)]
pub(crate) enum GuardError<E> {
    Budget(BudgetError),
    Delegate(E),
}

/// One accumulator per actual importing operation, not per candidate.
/// Constructor initializes quantities only; it grants no source capability.
#[derive(Debug)]
pub(crate) struct CandidateBudget {
    totals: Totals,
    stop: Option<Stop>,
}

impl CandidateBudget {
    pub(crate) fn new() -> Self {
        Self {
            totals: Totals::default(),
            stop: None,
        }
    }
    pub(crate) fn totals(&self) -> Totals {
        self.totals
    }

    fn available(&mut self) -> Result<(), BudgetError> {
        match self.stop {
            Some(Stop::Bound(bound)) => return Err(BudgetError::Bound(bound)),
            Some(Stop::Aborted) => return Err(BudgetError::Unavailable),
            None => {}
        }
        // Fields are private, initialized to zero and remain within the domain
        // on every successful charge; reject an invalid internal state as misuse.
        if self.totals.sources > SOURCES
            || self.totals.files > FILES
            || self.totals.content > CONTENT
        {
            self.stop = Some(Stop::Aborted);
            return Err(BudgetError::Unavailable);
        }
        Ok(())
    }

    fn crossing(&mut self, field: Field, observed: u128, limit: u128) -> BudgetError {
        let bound = Bound {
            field,
            observed,
            limit,
        };
        self.stop = Some(Stop::Bound(bound));
        BudgetError::Bound(bound)
    }

    fn source(&mut self) -> Result<(), BudgetError> {
        self.available()?;
        self.totals.sources += 1;
        if self.totals.sources > SOURCES {
            return Err(self.crossing(Field::Sources, self.totals.sources, SOURCES));
        }
        Ok(())
    }

    fn file(&mut self) -> Result<(), BudgetError> {
        self.available()?;
        self.totals.files += 1;
        if self.totals.files > FILES {
            return Err(self.crossing(Field::Files, self.totals.files, FILES));
        }
        Ok(())
    }

    fn abort(&mut self) {
        // Do not replace the first proven quota refusal with a placeholder.
        if self.stop.is_none() {
            self.stop = Some(Stop::Aborted);
        }
    }
}

struct Guarded<'a, C> {
    budget: &'a mut CandidateBudget,
    delegate: &'a mut C,
}

impl<C: ArchiveConsumer> ArchiveConsumer for Guarded<'_, C> {
    type Error = GuardError<C::Error>;
    fn checkpoint(&mut self) -> Result<(), Self::Error> {
        self.budget.available().map_err(GuardError::Budget)?;
        self.delegate.checkpoint().map_err(|error| {
            self.budget.abort();
            GuardError::Delegate(error)
        })
    }
    fn begin(&mut self, path: &LogicalPath, announced: u128) -> Result<(), Self::Error> {
        self.budget.file().map_err(GuardError::Budget)?;
        // The announced length is forwarded metadata, never a content charge.
        self.delegate.begin(path, announced).map_err(|error| {
            self.budget.abort();
            GuardError::Delegate(error)
        })
    }
    fn content(&mut self, bytes: &[u8]) -> Result<(), Self::Error> {
        self.budget.available().map_err(GuardError::Budget)?;
        let remaining = CONTENT - self.budget.totals.content;
        let amount = bytes.len() as u128;
        if amount <= remaining {
            self.budget.totals.content += amount;
            return self.delegate.content(bytes).map_err(|error| {
                self.budget.abort();
                GuardError::Delegate(error)
            });
        }
        // The comparison proves remaining < bytes.len(), so this narrowing is
        // exact on this actual slice even when usize is smaller than u128.
        let prefix = remaining as usize;
        if prefix != 0 {
            self.budget.totals.content += remaining;
            self.delegate.content(&bytes[..prefix]).map_err(|error| {
                self.budget.abort();
                GuardError::Delegate(error)
            })?;
        }
        // This actual byte exists, proves the first crossing, and is not written.
        // Never charge the unread logical tail of the provided fixed-size chunk.
        let _crossing_byte = bytes[prefix];
        self.budget.totals.content += 1;
        Err(GuardError::Budget(self.budget.crossing(
            Field::Content,
            self.budget.totals.content,
            CONTENT,
        )))
    }
    fn end(&mut self, file: &FileRecord) -> Result<(), Self::Error> {
        self.budget.available().map_err(GuardError::Budget)?;
        self.delegate.end(file).map_err(|error| {
            self.budget.abort();
            GuardError::Delegate(error)
        })
    }
}

/// Guard one actually supplied candidate's decoder observation sequence.
/// Caller owns the original package association and canonical candidate order.
/// Delegate writes/results remain provisional until every owning admission and
/// custody check succeeds. A successful archive report is data, not admission.
pub(crate) fn decode_with_budget<R: io::Read, C: ArchiveConsumer>(
    reader: R,
    package_name: &str,
    package_version: &str,
    budget: &mut CandidateBudget,
    delegate: &mut C,
) -> Result<DecodedArchive, DecodeError<GuardError<C::Error>>> {
    budget
        .source()
        .map_err(|error| DecodeError::Consumer(GuardError::Budget(error)))?;
    let result = {
        let mut guarded = Guarded { budget, delegate };
        archive_decoder::decode(reader, package_name, package_version, &mut guarded)
    };
    // Profile rejection retains all observed work and may continue with the
    // next canonical candidate. IO/consumer/internal failures end the operation.
    // The original first error is returned unchanged; callers retain its cause.
    if result.is_err() && !matches!(&result, Err(DecodeError::Profile(_))) {
        budget.abort();
    }
    result
}

#[cfg(test)]
#[path = "acquisition_guard_tests.rs"]
mod tests;
