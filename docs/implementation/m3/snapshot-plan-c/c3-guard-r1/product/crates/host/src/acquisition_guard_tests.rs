use super::*;
use crate::archive_decoder::ProfileError;
use opensip_identity::raw_sha256;
use std::io::Read;

const BASE: &[u8] = include_bytes!("archive_decoder/fixtures/base.tar.gz");
const EMPTY: &[u8] = include_bytes!("archive_decoder/fixtures/empty.tar.gz");
// Independent one-regular-empty-file archive; unlike BASE, no preceding content.
const ZERO_FILE: &[u8] = &[
    31, 139, 8, 0, 0, 0, 0, 0, 2, 255, 43, 205, 203, 44, 209, 53, 212, 51, 208, 51, 208, 79, 205,
    45, 40, 169, 100, 160, 1, 48, 0, 2, 51, 19, 19, 48, 13, 4, 232, 52, 38, 219, 208, 192, 216,
    204, 148, 65, 193, 128, 129, 14, 160, 180, 184, 36, 177, 72, 65, 129, 97, 20, 140, 130, 81, 48,
    10, 70, 24, 0, 0, 9, 121, 90, 159, 0, 6, 0, 0,
];
// Independently authored valid GNU above-u64 announced size, actual1536-byte
// partial payload. The scalar announcement never supplies missing content.
const HUGE: &[u8] = &[
    31, 139, 8, 0, 0, 0, 0, 0, 2, 255, 43, 205, 203, 44, 209, 53, 212, 51, 208, 51, 208, 175, 96,
    160, 17, 48, 0, 2, 51, 19, 19, 48, 13, 4, 112, 186, 129, 129, 129, 17, 89, 13, 66, 222, 204,
    204, 212, 156, 65, 193, 128, 129, 14, 160, 180, 184, 36, 177, 72, 65, 129, 97, 132, 130, 10,
    134, 81, 48, 10, 70, 193, 40, 24, 5, 35, 17, 0, 0, 198, 109, 71, 252, 0, 8, 0, 0,
];

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Phase {
    Checkpoint,
    Begin,
    Content,
    End,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct OwnerFailure {
    phase: Phase,
    token: u64,
}
#[derive(Default)]
struct Receiver {
    bytes: Vec<u8>,
    began: usize,
    ended: usize,
    checkpoints: usize,
    fail: Option<Phase>,
    checkpoint_failure: Option<usize>,
    content_failure_on_file: Option<usize>,
    announced: Vec<u128>,
}
impl Receiver {
    fn failure(&self, phase: Phase) -> Result<(), OwnerFailure> {
        if self.fail == Some(phase)
            || (phase == Phase::Content && self.content_failure_on_file == Some(self.began))
            || (phase == Phase::Checkpoint && self.checkpoint_failure == Some(self.checkpoints))
        {
            Err(OwnerFailure { phase, token: 777 })
        } else {
            Ok(())
        }
    }
}
impl ArchiveConsumer for Receiver {
    type Error = OwnerFailure;
    fn checkpoint(&mut self) -> Result<(), Self::Error> {
        self.checkpoints += 1;
        self.failure(Phase::Checkpoint)
    }
    fn begin(&mut self, _: &LogicalPath, length: u128) -> Result<(), Self::Error> {
        self.began += 1;
        self.announced.push(length);
        self.failure(Phase::Begin)
    }
    fn content(&mut self, bytes: &[u8]) -> Result<(), Self::Error> {
        self.failure(Phase::Content)?;
        self.bytes.extend_from_slice(bytes);
        Ok(())
    }
    fn end(&mut self, _: &FileRecord) -> Result<(), Self::Error> {
        self.ended += 1;
        self.failure(Phase::End)
    }
}
struct Short<'a> {
    bytes: &'a [u8],
    width: usize,
    calls: usize,
    largest: usize,
    observed: usize,
    interrupted: bool,
}
impl<'a> Short<'a> {
    fn new(bytes: &'a [u8], width: usize) -> Self {
        Self {
            bytes,
            width,
            calls: 0,
            largest: 0,
            observed: 0,
            interrupted: false,
        }
    }
}
impl Read for Short<'_> {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        self.largest = self.largest.max(out.len());
        if self.interrupted {
            self.interrupted = false;
            return Err(io::Error::new(
                io::ErrorKind::Interrupted,
                "injected-interrupt",
            ));
        }
        let n = self.bytes.len().min(self.width).min(out.len());
        out[..n].copy_from_slice(&self.bytes[..n]);
        self.bytes = &self.bytes[n..];
        self.observed += n;
        Ok(n)
    }
}
fn bound(error: DecodeError<GuardError<OwnerFailure>>) -> Bound {
    match error {
        DecodeError::Consumer(GuardError::Budget(BudgetError::Bound(bound))) => bound,
        other => panic!("expected acquisition bound, got {other:?}"),
    }
}
fn seeded(totals: Totals) -> CandidateBudget {
    CandidateBudget { totals, stop: None }
}

#[test]
fn complete_actual_archives_preserve_data_and_fixed_read_buffers() {
    for width in [1, 7, 4096] {
        let mut budget = CandidateBudget::new();
        let mut sink = Receiver::default();
        let mut input = Short::new(BASE, width);
        let result =
            decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
        assert_eq!(
            budget.totals(),
            Totals {
                sources: 1,
                files: 3,
                content: 17
            }
        );
        assert_eq!(sink.bytes.len(), 17);
        assert_eq!((sink.began, sink.ended), (3, 3));
        assert_eq!(result.compressed_sha256, raw_sha256(BASE));
        assert_eq!(result.compressed_bytes, 141);
        assert_eq!(result.inflated_bytes, 3584);
        assert_eq!(result.content_bytes, 17);
        assert_eq!(result.files.len(), 3);
        assert_eq!(input.observed, BASE.len());
        assert!(input.largest <= 4096);
        assert!(sink.checkpoints > 0);
    }
}
#[test]
fn inclusive_content_quota_accepts_under_every_read_partition() {
    for width in [1, 7, 4096] {
        let mut budget = seeded(Totals {
            sources: 0,
            files: 0,
            content: CONTENT - 17,
        });
        let mut sink = Receiver::default();
        let mut input = Short::new(BASE, width);
        decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
        assert_eq!(budget.totals().content, CONTENT);
        assert_eq!(sink.bytes.len(), 17);
    }
}
#[test]
fn first_content_crossing_is_chunk_independent_and_never_written() {
    for width in [1, 7, 4096] {
        let mut budget = seeded(Totals {
            sources: 0,
            files: 0,
            content: CONTENT - 10,
        });
        let mut sink = Receiver::default();
        let mut input = Short::new(BASE, width);
        let rejected = bound(
            decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err(),
        );
        assert_eq!(
            rejected,
            Bound {
                field: Field::Content,
                observed: CONTENT + 1,
                limit: CONTENT
            }
        );
        assert_eq!(sink.bytes.len(), 10);
        assert_eq!(
            budget.totals(),
            Totals {
                sources: 1,
                files: 2,
                content: CONTENT + 1
            }
        );
        assert_eq!(sink.ended, 1);
        assert!(input.largest <= 4096);
        assert!(input.observed <= BASE.len());
    }
}
#[test]
fn file_crossing_precedes_any_of_its_payload_or_delegate_begin() {
    let mut budget = seeded(Totals {
        sources: 0,
        files: FILES - 1,
        content: 0,
    });
    let mut sink = Receiver::default();
    let rejected =
        bound(decode_with_budget(BASE, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err());
    assert_eq!(
        rejected,
        Bound {
            field: Field::Files,
            observed: FILES + 1,
            limit: FILES
        }
    );
    assert_eq!((sink.began, sink.ended, sink.bytes.len()), (1, 1, 6));
    assert_eq!(budget.totals().content, 6);
}
#[test]
fn source_crossing_precedes_physical_reads_and_other_at_limit_fields() {
    let mut budget = seeded(Totals {
        sources: SOURCES,
        files: FILES,
        content: CONTENT,
    });
    let mut sink = Receiver::default();
    let mut input = Short::new(BASE, 4096);
    let rejected =
        bound(decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err());
    assert_eq!(
        rejected,
        Bound {
            field: Field::Sources,
            observed: SOURCES + 1,
            limit: SOURCES
        }
    );
    assert_eq!(input.calls, 0);
    assert_eq!((sink.checkpoints, sink.began), (0, 0));
}
#[test]
fn framing_and_empty_files_do_not_charge_content_at_ceiling() {
    let mut budget = seeded(Totals {
        sources: 0,
        files: 0,
        content: CONTENT,
    });
    let mut sink = Receiver::default();
    let empty = decode_with_budget(EMPTY, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
    assert!(empty.files.is_empty());
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 0,
            content: CONTENT
        }
    );
    let zero = decode_with_budget(ZERO_FILE, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
    assert_eq!(zero.files.len(), 1);
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 2,
            files: 1,
            content: CONTENT
        }
    );
    let rejected =
        bound(decode_with_budget(BASE, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err());
    assert_eq!(rejected.field, Field::Content);
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 3,
            files: 2,
            content: CONTENT + 1
        }
    );
    assert_eq!((sink.began, sink.ended, sink.bytes.len()), (2, 1, 0));
}
#[test]
fn late_crc_rejection_retains_actual_work_and_allows_next_profile_candidate() {
    let mut bad = BASE.to_vec();
    let trailer = bad.len() - 8;
    bad[trailer] ^= 1;
    let mut budget = CandidateBudget::new();
    let mut sink = Receiver::default();
    assert!(matches!(
        decode_with_budget(bad.as_slice(), "unit", "1.0.0", &mut budget, &mut sink),
        Err(DecodeError::Profile(ProfileError::GzipTrailer))
    ));
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 3,
            content: 17
        }
    );
    assert_eq!(sink.bytes.len(), 17);
    assert_eq!(sink.ended, 3);
    decode_with_budget(EMPTY, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 2,
            files: 3,
            content: 17
        }
    );
}
#[test]
fn every_delegate_error_keeps_its_exact_value_and_stops_reuse() {
    for phase in [Phase::Checkpoint, Phase::Begin, Phase::Content, Phase::End] {
        let mut budget = CandidateBudget::new();
        let mut sink = Receiver {
            fail: Some(phase),
            ..Receiver::default()
        };
        let error = decode_with_budget(BASE, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err();
        match error {
            DecodeError::Consumer(GuardError::Delegate(actual)) => {
                assert_eq!(actual, OwnerFailure { phase, token: 777 })
            }
            other => panic!("lost delegate origin {other:?}"),
        }
        let before = budget.totals();
        let mut next = Short::new(EMPTY, 4096);
        sink.fail = None;
        assert!(matches!(
            decode_with_budget(&mut next, "unit", "1.0.0", &mut budget, &mut sink),
            Err(DecodeError::Consumer(GuardError::Budget(
                BudgetError::Unavailable
            )))
        ));
        assert_eq!(next.calls, 0);
        assert_eq!(budget.totals(), before);
    }
}
#[derive(Debug)]
struct PhysicalFault(u64);
impl std::fmt::Display for PhysicalFault {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "physical-{}", self.0)
    }
}
impl std::error::Error for PhysicalFault {}
struct Broken;
impl Read for Broken {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::other(PhysicalFault(99)))
    }
}
#[test]
fn physical_io_origin_is_not_relabelled_as_quota_or_profile() {
    let mut budget = CandidateBudget::new();
    let mut sink = Receiver::default();
    match decode_with_budget(Broken, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err() {
        DecodeError::Io(error) => assert_eq!(
            error
                .get_ref()
                .unwrap()
                .downcast_ref::<PhysicalFault>()
                .unwrap()
                .0,
            99
        ),
        other => panic!("lost physical IO {other:?}"),
    }
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 0,
            content: 0
        }
    );
    let mut next = Short::new(EMPTY, 4096);
    assert!(matches!(
        decode_with_budget(&mut next, "unit", "1.0.0", &mut budget, &mut sink),
        Err(DecodeError::Consumer(GuardError::Budget(
            BudgetError::Unavailable
        )))
    ));
    assert_eq!(next.calls, 0);
}
#[test]
fn interrupted_retry_runs_owning_checkpoint_and_preserves_cancel_origin() {
    let mut budget = CandidateBudget::new();
    let mut sink = Receiver {
        checkpoint_failure: Some(2),
        ..Receiver::default()
    };
    let mut input = Short::new(BASE, 1);
    input.interrupted = true;
    match decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err() {
        DecodeError::Consumer(GuardError::Delegate(actual)) => assert_eq!(
            actual,
            OwnerFailure {
                phase: Phase::Checkpoint,
                token: 777
            }
        ),
        other => panic!("lost checkpoint {other:?}"),
    }
    assert_eq!(input.calls, 1);
    assert_eq!(input.observed, 0);
    assert_eq!(sink.checkpoints, 2);
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 0,
            content: 0
        }
    );
}
#[test]
fn wrong_effective_path_never_creates_a_file_charge() {
    let mut budget = CandidateBudget::new();
    let mut sink = Receiver::default();
    assert!(matches!(
        decode_with_budget(BASE, "wrong", "1.0.0", &mut budget, &mut sink),
        Err(DecodeError::Profile(ProfileError::Path))
    ));
    assert_eq!(
        budget.totals(),
        Totals {
            sources: 1,
            files: 0,
            content: 0
        }
    );
    assert_eq!(sink.began, 0);
    decode_with_budget(EMPTY, "unit", "1.0.0", &mut budget, &mut sink).unwrap();
    assert_eq!(budget.totals().sources, 2);
}
#[test]
fn first_bound_stays_exact_and_never_runs_another_reader() {
    let mut budget = seeded(Totals {
        sources: 0,
        files: 0,
        content: CONTENT,
    });
    let mut sink = Receiver::default();
    let first =
        bound(decode_with_budget(BASE, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err());
    let before = budget.totals();
    let calls = sink.checkpoints;
    let mut next = Short::new(EMPTY, 1);
    let second =
        bound(decode_with_budget(&mut next, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err());
    assert_eq!(first, second);
    assert_eq!(budget.totals(), before);
    assert_eq!(next.calls, 0);
    assert_eq!(sink.checkpoints, calls);
}
#[test]
fn above_u64_announcement_charges_only_actual_partial_payload() {
    for width in [1, 7, 4096] {
        let mut budget = CandidateBudget::new();
        let mut sink = Receiver::default();
        let mut input = Short::new(HUGE, width);
        assert!(matches!(
            decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink),
            Err(DecodeError::Profile(ProfileError::TruncatedTar))
        ));
        assert_eq!(sink.announced, vec![1u128 << 64]);
        assert_eq!(sink.bytes.len(), 1536);
        assert_eq!(
            budget.totals(),
            Totals {
                sources: 1,
                files: 1,
                content: 1536
            }
        );
        assert_eq!(sink.ended, 0);
        assert_eq!(input.observed, HUGE.len());
        assert!(input.largest <= 4096);
    }
}
#[test]
fn earlier_prefix_delegate_failure_is_preserved_before_possible_quota_crossing() {
    for width in [1, 7, 4096] {
        let mut budget = seeded(Totals {
            sources: 0,
            files: 0,
            content: CONTENT - 10,
        });
        let mut sink = Receiver {
            content_failure_on_file: Some(2),
            ..Receiver::default()
        };
        let mut input = Short::new(BASE, width);
        match decode_with_budget(&mut input, "unit", "1.0.0", &mut budget, &mut sink).unwrap_err() {
            DecodeError::Consumer(GuardError::Delegate(actual)) => assert_eq!(
                actual,
                OwnerFailure {
                    phase: Phase::Content,
                    token: 777
                }
            ),
            other => panic!("invented later quota cause {other:?}"),
        }
        assert!(budget.totals().content <= CONTENT);
        assert_eq!(budget.stop, Some(Stop::Aborted));
        assert_eq!(sink.bytes.len(), 6);
    }
}
