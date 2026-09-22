//! Bounded caller-owned buffers and read attempts on the original work budget.
//! Requested storage accounting is not allocator/RSS, arbitrary reader internals,
//! native custody or admitted-record qualification. No incomplete prefix is returned.
//!
//! The standalone read_bounded_accounted and read_bounded_reserved functions
//! permanently close the original ledger on any returned error,
//! including ordinary I/O errors and invalid limits. They are not a drop-in reader
//! inside native brackets that must perform accounted postchecks after a read
//! error. Such owners need their own provisional-outcome/finalization sequence.
use crate::{ReservedPostchecks, WorkCost, WorkFailure, WorkScope};
use std::io::{self, Read};
const MAX_RECORD: usize = 4_194_304;
const CHUNK: usize = 4096;
#[derive(Debug)]
pub enum ReadFailure {
    InvalidLimit,
    Reserve,
    Bound,
    Io(io::Error),
}

/// Charge each requested growth and read attempt before it occurs.
/// Retained-cache copies and native observers/postchecks need separate accounting.
pub fn read_bounded_accounted(
    reader: impl Read,
    max: usize,
    work: &mut WorkScope<'_>,
) -> Result<Vec<u8>, WorkFailure<ReadFailure>> {
    work.scope(|work| read_charged(reader, max, |cost| work.charge(cost)))
}
/// Spend the same pre-reserved allowance without a new ledger or outer recharge.
/// The caller must derive sufficient allowance before its original effect.
pub fn read_bounded_reserved(
    reader: impl Read,
    max: usize,
    post: &mut ReservedPostchecks<'_>,
) -> Result<Vec<u8>, WorkFailure<ReadFailure>> {
    post.scope(|post| read_charged(reader, max, |cost| post.spend(cost)))
}
/// Read using a protected child allowance, then run the caller's required checks.
///
/// The parent must already contain the complete read allowance PLUS the allowance
/// needed by `postchecks`. For `WorkLedger::effect`, put that total in its second
/// (postchecks) argument: its first (effect) charge is not spendable here.
/// The child cannot spend the parent's remaining allowance. No work is refunded.
///
/// Ordinary I/O, allocation and record-size errors stay private until `postchecks`
/// returns; then the original read error is converted into E and closes the ledger.
/// A postcheck error takes precedence over a pending read error. Invalid limits,
/// work-budget failure and panic stop immediately without running postchecks.
/// The callback borrows the same original reader after the read has finished;
/// it receives no provisional buffer or read outcome. This permits original-file
/// inspection without conflicting with the mutable read borrow.
///
/// Successful bytes only follow successful callback completion. This orders an
/// arbitrary callback; the native owner still owes actual original-descriptor,
/// name, custody and stability checks and conservative costs. It grants no native
/// authority and does not bound arbitrary reader/callback internals.
pub fn read_bounded_reserved_with_postchecks<R: Read, E: From<ReadFailure>>(
    mut reader: R,
    max: usize,
    read_allowance: WorkCost,
    parent: &mut ReservedPostchecks<'_>,
    postchecks: impl FnOnce(&R, &mut ReservedPostchecks<'_>) -> Result<(), WorkFailure<E>>,
) -> Result<Vec<u8>, WorkFailure<E>> {
    parent.scope(|parent| {
        // Only this private local holds the ordinary read outcome. Budget refusal
        // from child.spend has already latched the original and returns at once.
        let pending = parent.with_allowance(read_allowance, |child| {
            match read_charged(&mut reader, max, |cost| child.spend(cost)) {
                Ok(bytes) => Ok(Ok(bytes)),
                Err(WorkFailure::Budget(error)) => Err(WorkFailure::Budget(error)),
                Err(WorkFailure::Operation(ReadFailure::InvalidLimit)) => {
                    Err(WorkFailure::Operation(E::from(ReadFailure::InvalidLimit)))
                }
                Err(WorkFailure::Operation(error)) => Ok(Err(error)),
            }
        })?;
        postchecks(&reader, parent)?;
        pending.map_err(|error| WorkFailure::Operation(E::from(error)))
    })
}

// Only the private algorithm receives a charge closure; public helpers always
// bind it to an original guarded WorkScope or ReservedPostchecks borrow.
fn read_charged(
    mut reader: impl Read,
    max: usize,
    mut charge: impl FnMut(WorkCost) -> Result<(), WorkFailure<ReadFailure>>,
) -> Result<Vec<u8>, WorkFailure<ReadFailure>> {
    if max == 0 || max > MAX_RECORD {
        return Err(WorkFailure::Operation(ReadFailure::InvalidLimit));
    }
    let ceiling = max + 1;
    charge(WorkCost {
        objects: 1,
        ..WorkCost::default()
    })?;
    let mut bytes = Vec::new();
    let mut used = 0;
    loop {
        if used == ceiling {
            return Err(WorkFailure::Operation(ReadFailure::Bound));
        }
        if used == bytes.len() {
            let next = if bytes.is_empty() {
                CHUNK
            } else {
                bytes.len() * 2
            }
            .min(ceiling);
            // Charge the complete requested allocation on each growth, even
            // when an allocator might reuse space. Never refund old buffers.
            charge(WorkCost {
                edges: 1,
                bytes: next,
                ..WorkCost::default()
            })?;
            bytes
                .try_reserve_exact(next - bytes.len())
                .map_err(|_| WorkFailure::Operation(ReadFailure::Reserve))?;
            bytes.resize(next, 0);
        } else {
            charge(WorkCost {
                edges: 1,
                ..WorkCost::default()
            })?;
        }
        match reader.read(&mut bytes[used..]) {
            Ok(0) => {
                bytes.truncate(used);
                return Ok(bytes);
            }
            Ok(n) if n <= bytes.len() - used => {
                used += n;
            }
            Ok(_) => {
                return Err(WorkFailure::Operation(ReadFailure::Io(io::Error::new(
                    io::ErrorKind::InvalidData,
                    "reader returned an impossible length",
                ))));
            }
            Err(e) if e.kind() == io::ErrorKind::Interrupted => {}
            Err(e) => return Err(WorkFailure::Operation(ReadFailure::Io(e))),
        }
    }
}
