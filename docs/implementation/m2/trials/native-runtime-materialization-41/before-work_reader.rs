//! Bounded caller-owned buffers and read attempts on the original work budget.
//! Requested storage accounting is not allocator/RSS, arbitrary reader internals,
//! native custody or admitted-record qualification. No incomplete prefix is returned.
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
