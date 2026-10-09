use super::*;
use crate::raw_stream_copy::CopyCheckpoint;
const BASE: &[u8] = include_bytes!("archive_decoder/fixtures/base.tar.gz");
#[derive(Default)]
struct Check {
    calls: usize,
    fail: bool,
}
impl CopyCheckpoint for Check {
    type Error = u64;
    fn checkpoint(&mut self) -> Result<(), u64> {
        self.calls += 1;
        if self.fail { Err(419) } else { Ok(()) }
    }
}
#[derive(Default)]
struct Receiver {
    begins: usize,
    content: usize,
}
impl ArchiveConsumer for Receiver {
    type Error = u64;
    fn checkpoint(&mut self) -> Result<(), u64> {
        Ok(())
    }
    fn begin(&mut self, _: &LogicalPath, _: u128) -> Result<(), u64> {
        self.begins += 1;
        Ok(())
    }
    fn content(&mut self, b: &[u8]) -> Result<(), u64> {
        self.content += b.len();
        Ok(())
    }
    fn end(&mut self, _: &FileRecord) -> Result<(), u64> {
        Ok(())
    }
}
struct NeverRead;
impl io::Read for NeverRead {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        panic!("unexpected raw/decode read")
    }
}
#[test]
fn source_is_charged_once_before_intake_and_stays_one_through_decode() {
    let mut budget = CandidateBudget::new();
    let mut captured = Vec::new();
    let mut check = Check::default();
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    assert_eq!(attempt.budget.totals().sources, 1);
    let raw = attempt.copy_raw(BASE, &mut captured, &mut check).unwrap();
    assert_eq!(raw.byte_length, BASE.len() as u64);
    assert_eq!(attempt.budget.totals().sources, 1);
    let mut receiver = Receiver::default();
    attempt
        .decode(captured.as_slice(), "unit", "1.0.0", &mut receiver)
        .unwrap();
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 3,
            content: 17
        }
    );
    assert_eq!(receiver.begins, 3);
    assert_eq!(receiver.content, 17);
}
#[test]
fn source_limit_prevents_creating_attempt_or_invoking_raw_reader() {
    let mut budget = CandidateBudget::new();
    budget.totals.sources = SOURCES;
    let error = match begin_source_attempt(&mut budget) {
        Err(e) => e,
        Ok(_) => panic!("crossing admitted"),
    };
    assert_eq!(
        error,
        BudgetError::Bound(Bound {
            field: Field::Sources,
            observed: SOURCES + 1,
            limit: SOURCES
        })
    );
    assert_eq!(budget.totals().sources, SOURCES + 1);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Bound(_))
    ));
}
#[test]
fn raw_checkpoint_error_preserves_origin_and_stops_operation() {
    let mut budget = CandidateBudget::new();
    let mut out = Vec::new();
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    match attempt.copy_raw(
        NeverRead,
        &mut out,
        &mut Check {
            calls: 0,
            fail: true,
        },
    ) {
        Err(AttemptCopyError::Copy(crate::raw_stream_copy::CopyError::Owner(419))) => {}
        _ => panic!("original checkpoint error lost"),
    }
    drop(attempt);
    assert!(out.is_empty());
    assert_eq!(budget.totals().sources, 1);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
#[test]
fn abandoning_unread_attempt_stops_instead_of_resetting_source_charge() {
    let mut budget = CandidateBudget::new();
    drop(begin_source_attempt(&mut budget).unwrap());
    assert_eq!(budget.totals().sources, 1);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
#[test]
fn abandoning_copied_attempt_stops_without_custody_or_profile_rejection_claim() {
    let mut budget = CandidateBudget::new();
    let mut out = Vec::new();
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    attempt
        .copy_raw(BASE, &mut out, &mut Check::default())
        .unwrap();
    drop(attempt);
    assert_eq!(out, BASE);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
#[test]
fn decode_before_raw_completion_does_not_read_or_create_archive() {
    let mut budget = CandidateBudget::new();
    let mut receiver = Receiver::default();
    assert!(matches!(
        begin_source_attempt(&mut budget).unwrap().decode(
            NeverRead,
            "unit",
            "1.0.0",
            &mut receiver
        ),
        Err(DecodeError::Consumer(GuardError::Budget(
            BudgetError::Unavailable
        )))
    ));
    assert_eq!(receiver.begins, 0);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
#[test]
fn second_raw_copy_refuses_without_touching_reader_and_invalidates_attempt() {
    let mut budget = CandidateBudget::new();
    let mut out = Vec::new();
    let mut check = Check::default();
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    attempt.copy_raw(BASE, &mut out, &mut check).unwrap();
    let before = check.calls;
    assert!(matches!(
        attempt.copy_raw(NeverRead, &mut out, &mut check),
        Err(AttemptCopyError::Budget(BudgetError::Unavailable))
    ));
    assert_eq!(check.calls, before);
    drop(attempt);
    assert_eq!(budget.totals().sources, 1);
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
#[test]
fn decoder_profile_rejection_retains_charges_and_next_attempt_adds_one_source() {
    let mut corrupt = BASE.to_vec();
    let at = corrupt.len() - 8;
    corrupt[at] ^= 1;
    let mut budget = CandidateBudget::new();
    let mut out = Vec::new();
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    attempt
        .copy_raw(corrupt.as_slice(), &mut out, &mut Check::default())
        .unwrap();
    assert!(matches!(
        attempt.decode(out.as_slice(), "unit", "1.0.0", &mut Receiver::default()),
        Err(DecodeError::Profile(_))
    ));
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 3,
            content: 17
        }
    );
    let mut second = begin_source_attempt(&mut budget).unwrap();
    assert_eq!(second.budget.totals().sources, 2);
    out.clear();
    second
        .copy_raw(BASE, &mut out, &mut Check::default())
        .unwrap();
    second
        .decode(out.as_slice(), "unit", "1.0.0", &mut Receiver::default())
        .unwrap();
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 2,
            files: 6,
            content: 34
        }
    );
    // All captured bytes here are small in-memory test data, not authenticated
    // retained source observations or actual filesystem quarantine.
}

#[derive(Debug)]
struct RawFault(u64);
impl std::fmt::Display for RawFault {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "raw fault {}", self.0)
    }
}
impl std::error::Error for RawFault {}
struct PartialFault {
    calls: usize,
}
impl io::Read for PartialFault {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        if self.calls == 1 {
            out[..3].copy_from_slice(b"abc");
            Ok(3)
        } else {
            Err(io::Error::other(RawFault(321)))
        }
    }
}
#[test]
fn raw_read_failure_keeps_partial_bytes_provisional_and_exact_error_stops_budget() {
    let mut budget = CandidateBudget::new();
    let mut captured = Vec::new();
    let mut reader = PartialFault { calls: 0 };
    let mut attempt = begin_source_attempt(&mut budget).unwrap();
    match attempt.copy_raw(&mut reader, &mut captured, &mut Check::default()) {
        Err(AttemptCopyError::Copy(crate::raw_stream_copy::CopyError::Read(error))) => {
            assert_eq!(
                error
                    .get_ref()
                    .unwrap()
                    .downcast_ref::<RawFault>()
                    .unwrap()
                    .0,
                321
            );
        }
        _ => panic!("actual raw error changed"),
    }
    drop(attempt);
    assert_eq!(captured, b"abc");
    assert_eq!(reader.calls, 2);
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 0,
            content: 0
        }
    );
    assert!(matches!(
        begin_source_attempt(&mut budget),
        Err(BudgetError::Unavailable)
    ));
}
