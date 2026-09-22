//! Generic reader failure and budget semantics, not native custody fixtures.
use opensip_platform::{WorkBudgetError, WorkCost, WorkFailure, WorkLedger};
use opensip_platform::{WorkReadFailure as ReadFailure, read_bounded_accounted as read_bounded};
use std::io::{self, Cursor, Read};

#[test]
fn exact_bound_and_empty_succeed_oversize_never_returns_a_prefix() {
    for max in 1..=32 {
        let input = vec![b'x'; max];
        let mut exact = Cursor::new(input.clone());
        let mut owner = WorkLedger::new();
        let got = owner
            .scope(|scope| read_bounded(&mut exact, max, scope))
            .unwrap();
        assert_eq!(got, input);
        assert!(!owner.is_failed());
        let mut excessive = Cursor::new(vec![b'x'; max + 2]);
        let mut owner = WorkLedger::new();
        assert!(matches!(
            owner.scope(|scope| read_bounded(&mut excessive, max, scope)),
            Err(WorkFailure::Operation(ReadFailure::Bound))
        ));
        assert_eq!(excessive.position(), (max + 1) as u64);
        assert!(owner.is_failed());
    }
    let mut owner = WorkLedger::new();
    assert!(
        owner
            .scope(|scope| read_bounded(Cursor::new([]), 8, scope))
            .unwrap()
            .is_empty()
    );
}
struct CountReads {
    calls: usize,
    interrupted: bool,
}
impl Read for CountReads {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        if self.interrupted {
            Err(io::ErrorKind::Interrupted.into())
        } else {
            Ok(0)
        }
    }
}
#[test]
fn budget_refusal_precedes_reader_and_interrupted_retries_are_bounded() {
    let mut reader = CountReads {
        calls: 0,
        interrupted: false,
    };
    let mut owner = WorkLedger::with_limits(WorkCost {
        objects: 1,
        edges: 2,
        bytes: 1,
    })
    .unwrap();
    assert!(matches!(
        owner.scope(|scope| read_bounded(&mut reader, 8, scope)),
        Err(WorkFailure::Budget(WorkBudgetError::Bytes))
    ));
    assert_eq!(reader.calls, 0);
    assert!(owner.is_failed());
    let mut reader = CountReads {
        calls: 0,
        interrupted: true,
    };
    let mut owner = WorkLedger::with_limits(WorkCost {
        objects: 1,
        edges: 2,
        bytes: 100,
    })
    .unwrap();
    assert!(matches!(
        owner.scope(|scope| read_bounded(&mut reader, 8, scope)),
        Err(WorkFailure::Budget(WorkBudgetError::Edges))
    ));
    assert_eq!(reader.calls, 2);
    assert_eq!(owner.used().edges, 2);
    assert!(owner.is_failed());
}
struct PartialFailure(bool);
impl Read for PartialFailure {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        if self.0 {
            Err(io::ErrorKind::PermissionDenied.into())
        } else {
            self.0 = true;
            out[0] = b'x';
            Ok(1)
        }
    }
}
#[test]
fn partial_error_keeps_original_cause_and_consumed_budget() {
    let mut owner = WorkLedger::new();
    let result = owner.scope(|scope| read_bounded(PartialFailure(false), 8, scope));
    assert!(
        matches!(result,Err(WorkFailure::Operation(ReadFailure::Io(ref e)))if e.kind()==io::ErrorKind::PermissionDenied)
    );
    assert!(owner.used().bytes > 0);
    assert_eq!(owner.used().edges, 2);
    assert!(owner.is_failed());
    assert!(matches!(
        owner.charge::<()>(WorkCost::default()),
        Err(WorkFailure::Budget(WorkBudgetError::Closed))
    ));
}
#[test]
fn largest_record_uses_bounded_growth_and_limit_refusal_precedes_io() {
    let cap = 4_194_304;
    let bytes = vec![b'x'; cap];
    let mut owner = WorkLedger::new();
    assert_eq!(
        owner
            .scope(|scope| read_bounded(Cursor::new(&bytes), cap, scope))
            .unwrap(),
        bytes
    );
    assert!(owner.used().bytes >= cap && owner.used().bytes <= 3 * (cap + 1));
    for max in [0, cap + 1, usize::MAX] {
        let mut reader = CountReads {
            calls: 0,
            interrupted: false,
        };
        let mut owner = WorkLedger::new();
        assert!(matches!(
            owner.scope(|scope| read_bounded(&mut reader, max, scope)),
            Err(WorkFailure::Operation(ReadFailure::InvalidLimit))
        ));
        assert_eq!(reader.calls, 0);
        assert!(owner.is_failed());
    }
}

use opensip_platform::read_bounded_reserved;
#[test]
fn scope_and_reserved_readers_agree_at_every_small_bound() {
    for cap in 1..=32 {
        let bytes = vec![b'x'; cap];
        let mut regular = WorkLedger::new();
        let expected = regular
            .scope(|work| read_bounded(Cursor::new(&bytes), cap, work))
            .unwrap();
        let mut owner = WorkLedger::new();
        let allowance = WorkCost {
            objects: 1,
            edges: cap + 2,
            bytes: 3 * (cap + 1),
        };
        let got = owner
            .effect(WorkCost::default(), allowance, |post| {
                read_bounded_reserved(Cursor::new(&bytes), cap, post)
            })
            .unwrap();
        assert_eq!(got, expected);
        assert_eq!(owner.used(), allowance);
        assert!(!owner.is_failed());
    }
}
struct Counting {
    calls: usize,
    interrupted: bool,
}
impl Read for Counting {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        if self.interrupted {
            Err(io::ErrorKind::Interrupted.into())
        } else {
            Ok(0)
        }
    }
}
#[test]
fn reservation_refusal_precedes_reads_and_interrupted_retries_are_finite() {
    for (bytes, interrupted, expected_calls) in [(1, false, 0), (100, true, 2)] {
        let allowance = WorkCost {
            objects: 1,
            edges: 2,
            bytes,
        };
        let mut owner = WorkLedger::new();
        let mut reader = Counting {
            calls: 0,
            interrupted,
        };
        let result = owner.effect::<(), ReadFailure>(WorkCost::default(), allowance, |post| {
            assert!(matches!(
                read_bounded_reserved(&mut reader, 8, post),
                Err(WorkFailure::Budget(WorkBudgetError::ReservedPostcheck))
            ));
            Ok(())
        });
        assert!(matches!(
            result,
            Err(WorkFailure::Budget(WorkBudgetError::Closed))
        ));
        assert_eq!(reader.calls, expected_calls);
        assert_eq!(owner.used(), allowance);
        assert!(owner.is_failed());
    }
}
struct Partial(bool);
impl Read for Partial {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        if self.0 {
            Err(io::ErrorKind::PermissionDenied.into())
        } else {
            self.0 = true;
            out[0] = 1;
            Ok(1)
        }
    }
}
#[test]
fn caught_reserved_read_error_closes_original_owner_and_returns_no_prefix() {
    let allowance = WorkCost {
        objects: 1,
        edges: 4,
        bytes: 32,
    };
    let mut owner = WorkLedger::new();
    let result=owner.effect::<(),ReadFailure>(WorkCost::default(),allowance,|post|{
        let read=read_bounded_reserved(Partial(false),8,post);
        assert!(matches!(read,Err(WorkFailure::Operation(ReadFailure::Io(ref e)))if e.kind()==io::ErrorKind::PermissionDenied));
        assert!(matches!(post.spend::<ReadFailure>(WorkCost::default()),Err(WorkFailure::Budget(WorkBudgetError::Closed))));Ok(())
    });
    assert!(matches!(
        result,
        Err(WorkFailure::Budget(WorkBudgetError::Closed))
    ));
    assert_eq!(owner.used(), allowance);
}
#[test]
fn reserved_empty_oversize_and_invalid_limits_keep_honest_results() {
    let allowance = WorkCost {
        objects: 1,
        edges: 8,
        bytes: 32,
    };
    let mut owner = WorkLedger::new();
    assert!(
        owner
            .effect(
                WorkCost::default(),
                allowance,
                |post| read_bounded_reserved(Cursor::new([]), 8, post)
            )
            .unwrap()
            .is_empty()
    );
    let mut owner = WorkLedger::new();
    let mut oversized = Cursor::new([0; 10]);
    assert!(matches!(
        owner.effect(
            WorkCost::default(),
            allowance,
            |post| read_bounded_reserved(&mut oversized, 8, post)
        ),
        Err(WorkFailure::Operation(ReadFailure::Bound))
    ));
    assert_eq!(oversized.position(), 9);
    for cap in [0, 4_194_305, usize::MAX] {
        let mut owner = WorkLedger::new();
        let mut reader = Counting {
            calls: 0,
            interrupted: false,
        };
        assert!(matches!(
            owner.effect(
                WorkCost::default(),
                allowance,
                |post| read_bounded_reserved(&mut reader, cap, post)
            ),
            Err(WorkFailure::Operation(ReadFailure::InvalidLimit))
        ));
        assert_eq!(reader.calls, 0);
        assert_eq!(owner.used(), allowance);
        assert!(owner.is_failed());
    }
}

// Provisional outcomes stay inside the helper until the callback finishes. These
// tests check ordering/failure boundaries, not native custody qualification.
#[derive(Debug)]
enum CheckedReadError {
    Read(ReadFailure),
    Check(&'static str),
}
impl From<ReadFailure> for CheckedReadError {
    fn from(error: ReadFailure) -> Self {
        Self::Read(error)
    }
}
fn read_allowance438() -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 2,
        bytes: 9,
    }
}
fn whole_allowance438() -> WorkCost {
    WorkCost {
        edges: 4,
        ..read_allowance438()
    }
}
#[test]
fn postchecked_read_success_preserves_parent_share_and_no_double_charge() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let got = owner
        .effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                Cursor::new(b"good"),
                8,
                read_allowance438(),
                parent,
                |_, post| {
                    post.spend(WorkCost {
                        edges: 2,
                        ..WorkCost::default()
                    })?;
                    checked = true;
                    Ok(())
                },
            )
        })
        .unwrap();
    assert_eq!(got, b"good");
    assert!(checked);
    assert!(!owner.is_failed());
    assert_eq!(owner.used(), whole_allowance438());
}
#[test]
fn postchecked_read_io_failure_runs_checks_then_preserves_cause() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                PartialFailure(false),
                8,
                read_allowance438(),
                parent,
                |_, post| {
                    post.spend(WorkCost {
                        edges: 2,
                        ..WorkCost::default()
                    })?;
                    checked = true;
                    Ok(())
                },
            )
        });
    assert!(
        matches!(result, Err(WorkFailure::Operation(CheckedReadError::Read(ReadFailure::Io(ref e)))) if e.kind() == io::ErrorKind::PermissionDenied)
    );
    assert!(checked);
    assert!(owner.is_failed());
    assert_eq!(owner.used(), whole_allowance438());
}
#[test]
fn postchecked_read_semantic_oversize_runs_checks_and_returns_no_prefix() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                Cursor::new([0; 10]),
                8,
                read_allowance438(),
                parent,
                |_, post| {
                    post.spend(WorkCost {
                        edges: 2,
                        ..WorkCost::default()
                    })?;
                    checked = true;
                    Ok(())
                },
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Operation(CheckedReadError::Read(
            ReadFailure::Bound
        )))
    ));
    assert!(checked);
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_work_exhaustion_stops_without_postchecks_or_parent_spend() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let mut reader = CountReads {
        calls: 0,
        interrupted: true,
    };
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                &mut reader,
                8,
                read_allowance438(),
                parent,
                |_, _| {
                    checked = true;
                    Ok(())
                },
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Budget(WorkBudgetError::ReservedPostcheck))
    ));
    assert_eq!(reader.calls, 2);
    assert!(!checked);
    assert!(owner.is_failed());
    assert_eq!(owner.used(), whole_allowance438());
}
#[test]
fn postchecked_read_postcheck_error_takes_precedence_over_read_error() {
    let mut owner = WorkLedger::new();
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                PartialFailure(false),
                8,
                read_allowance438(),
                parent,
                |_, _| Err(WorkFailure::Operation(CheckedReadError::Check("changed"))),
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Operation(CheckedReadError::Check("changed")))
    ));
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_invalid_limit_stops_before_reader_and_postchecks() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let mut reader = CountReads {
        calls: 0,
        interrupted: false,
    };
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                &mut reader,
                0,
                read_allowance438(),
                parent,
                |_, _| {
                    checked = true;
                    Ok(())
                },
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Operation(CheckedReadError::Read(
            ReadFailure::InvalidLimit
        )))
    ));
    assert_eq!(reader.calls, 0);
    assert!(!checked);
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_caught_read_error_cannot_reopen_outer_operation() {
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            let failed = opensip_platform::read_bounded_reserved_with_postchecks(
                PartialFailure(false),
                8,
                read_allowance438(),
                parent,
                |_, _| {
                    checked = true;
                    Ok::<(), WorkFailure<CheckedReadError>>(())
                },
            );
            assert!(failed.is_err());
            Ok(())
        });
    assert!(checked);
    assert!(matches!(
        result,
        Err(WorkFailure::Budget(WorkBudgetError::Closed))
    ));
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_caught_postcheck_budget_error_cannot_release_bytes() {
    let mut owner = WorkLedger::new();
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                Cursor::new(b"good"),
                8,
                read_allowance438(),
                parent,
                |_, post| {
                    let failed = post.spend::<CheckedReadError>(WorkCost {
                        edges: 3,
                        ..WorkCost::default()
                    });
                    assert!(failed.is_err());
                    Ok(())
                },
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Budget(WorkBudgetError::Closed))
    ));
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_reservation_refusal_precedes_reader_and_checks() {
    let mut owner = WorkLedger::new();
    let mut reader = CountReads {
        calls: 0,
        interrupted: false,
    };
    let mut checked = false;
    let result =
        owner.effect::<_, CheckedReadError>(WorkCost::default(), WorkCost::default(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                &mut reader,
                8,
                read_allowance438(),
                parent,
                |_, _| {
                    checked = true;
                    Ok(())
                },
            )
        });
    assert!(matches!(
        result,
        Err(WorkFailure::Budget(WorkBudgetError::ReservedPostcheck))
    ));
    assert_eq!(reader.calls, 0);
    assert!(!checked);
    assert!(owner.is_failed());
}
#[test]
fn postchecked_read_panic_is_terminal_without_postchecks() {
    struct Panics;
    impl Read for Panics {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            panic!("read panic")
        }
    }
    let mut owner = WorkLedger::new();
    let mut checked = false;
    let panic = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let _ = owner.effect::<_, CheckedReadError>(
            WorkCost::default(),
            whole_allowance438(),
            |parent| {
                opensip_platform::read_bounded_reserved_with_postchecks(
                    Panics,
                    8,
                    read_allowance438(),
                    parent,
                    |_, _| {
                        checked = true;
                        Ok(())
                    },
                )
            },
        );
    }));
    assert!(panic.is_err());
    assert!(!checked);
    assert!(owner.is_failed());
    assert_eq!(owner.used(), whole_allowance438());
}

#[test]
fn postchecked_read_callback_borrows_same_original_mutable_reader() {
    let mut reader = Cursor::new(b"good".to_vec());
    let original = std::ptr::from_ref(&reader);
    let mut owner = WorkLedger::new();
    let got = owner
        .effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                &mut reader,
                8,
                read_allowance438(),
                parent,
                |retained, post| {
                    assert_eq!(std::ptr::from_ref(&**retained), original);
                    assert_eq!(retained.position(), 4);
                    post.spend(WorkCost {
                        edges: 2,
                        ..WorkCost::default()
                    })?;
                    Ok(())
                },
            )
        })
        .unwrap();
    assert_eq!(got, b"good");
    assert_eq!(reader.position(), 4);
    assert!(!owner.is_failed());
}

#[cfg(unix)]
#[test]
fn postchecked_read_actual_file_is_retained_for_callback_inspection() {
    use std::io::{Seek, SeekFrom, Write};
    use std::os::unix::fs::MetadataExt;
    struct Fixture {
        path: std::path::PathBuf,
        file: std::fs::File,
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_file(&self.path);
        }
    }
    let nonce = opensip_platform::request_entropy().unwrap();
    let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
    let path = std::env::temp_dir().join(format!("opensip-postchecked438-{name}"));
    let file = std::fs::OpenOptions::new()
        .read(true)
        .write(true)
        .create_new(true)
        .open(&path)
        .unwrap();
    let mut fixture = Fixture { path, file };
    fixture.file.write_all(b"good").unwrap();
    fixture.file.seek(SeekFrom::Start(0)).unwrap();
    let before = fixture.file.metadata().unwrap();
    let original = std::ptr::from_ref(&fixture.file);
    let mut owner = WorkLedger::new();
    let got = owner
        .effect::<_, CheckedReadError>(WorkCost::default(), whole_allowance438(), |parent| {
            opensip_platform::read_bounded_reserved_with_postchecks(
                &mut fixture.file,
                8,
                read_allowance438(),
                parent,
                |retained, post| {
                    post.spend(WorkCost {
                        edges: 2,
                        ..WorkCost::default()
                    })?;
                    assert_eq!(std::ptr::from_ref(&**retained), original);
                    let after = retained.metadata().unwrap();
                    assert_eq!(
                        (after.dev(), after.ino(), after.len()),
                        (before.dev(), before.ino(), before.len())
                    );
                    Ok(())
                },
            )
        })
        .unwrap();
    assert_eq!(got, b"good");
    assert!(!owner.is_failed());
    // This proves the callback can inspect the retained File, not native custody.
}
