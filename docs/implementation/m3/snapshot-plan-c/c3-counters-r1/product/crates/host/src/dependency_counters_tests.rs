use super::*;

#[test]
fn inclusive_limits_and_each_first_crossing() {
    for (field, at, delta, observed, limit) in [
        (
            Field::Sources,
            Totals {
                sources: 16_384,
                files: 0,
                content: 0,
            },
            Totals {
                sources: 1,
                files: 0,
                content: 0,
            },
            16_385,
            16_384,
        ),
        (
            Field::Files,
            Totals {
                sources: 1,
                files: 4_000_000,
                content: 0,
            },
            Totals {
                sources: 0,
                files: 1,
                content: 0,
            },
            4_000_001,
            4_000_000,
        ),
        (
            Field::Content,
            Totals {
                sources: 1,
                files: 1,
                content: 32 * GIB,
            },
            Totals {
                sources: 0,
                files: 0,
                content: 1,
            },
            32 * GIB + 1,
            32 * GIB,
        ),
    ] {
        assert_eq!(
            Acquisition(at).charge(Totals::default()).unwrap().totals(),
            at
        );
        assert_eq!(
            Acquisition(at).charge(delta).unwrap_err(),
            AcquisitionError::Bound(Bound {
                field,
                observed,
                limit
            })
        );
    }
}

#[test]
fn simultaneous_acquisition_crossings_use_selected_precedence() {
    assert_eq!(
        Acquisition(ACQUISITION_LIMITS)
            .charge(Totals {
                sources: 1,
                files: 1,
                content: 1
            })
            .unwrap_err(),
        AcquisitionError::Bound(Bound {
            field: Field::Sources,
            observed: 16_385,
            limit: 16_384
        })
    );
    assert_eq!(
        Acquisition(ACQUISITION_LIMITS).file(1).unwrap_err(),
        AcquisitionError::Bound(Bound {
            field: Field::Files,
            observed: 4_000_001,
            limit: 4_000_000
        })
    );
}

#[test]
fn final_check_returns_all_proven_crossings() {
    let at = FinalPopulation(FINAL_LIMITS).check().unwrap();
    assert_eq!(at, FINAL_LIMITS);
    let rejected = FinalPopulation(FINAL_LIMITS)
        .package(1, 1)
        .unwrap()
        .check()
        .unwrap_err()
        .bounds();
    assert_eq!(
        rejected,
        [
            Some(Bound {
                field: Field::Sources,
                observed: 4_097,
                limit: 4_096
            }),
            Some(Bound {
                field: Field::Files,
                observed: 1_000_001,
                limit: 1_000_000
            }),
            Some(Bound {
                field: Field::Content,
                observed: 8 * GIB + 1,
                limit: 8 * GIB
            }),
        ]
    );
}

#[test]
fn oversized_single_candidate_is_acquired_without_protocol_shortcut() {
    let observed = Acquisition::new()
        .source()
        .unwrap()
        .file(8 * GIB + 1)
        .unwrap()
        .totals();
    assert_eq!(
        observed,
        Totals {
            sources: 1,
            files: 1,
            content: 8 * GIB + 1
        }
    );
    // Selection is performed outside this kernel: an unselected candidate
    // contributes no call to package, while a selected one contributes all.
    assert_eq!(FinalPopulation::new().check().unwrap(), Totals::default());
    let selected = FinalPopulation::new()
        .package(1, 8 * GIB + 1)
        .unwrap()
        .check()
        .unwrap_err()
        .bounds();
    assert_eq!(selected[0], None);
    assert_eq!(selected[1], None);
    assert_eq!(selected[2].unwrap().observed, 8 * GIB + 1);
}

#[test]
fn candidate_source_and_zero_content_file_events_count() {
    let state = Acquisition::new()
        .source()
        .unwrap()
        .file(0)
        .unwrap()
        .source()
        .unwrap()
        .file(7)
        .unwrap()
        .totals();
    assert_eq!(
        state,
        Totals {
            sources: 2,
            files: 2,
            content: 7
        }
    );
    let final_counts = FinalPopulation::new()
        .package(1, 0)
        .unwrap()
        .package(1, 7)
        .unwrap()
        .check()
        .unwrap();
    assert_eq!(final_counts, state);
}

#[test]
fn actual_source_count_limit_uses_event_loop() {
    let mut state = Acquisition::new();
    for _ in 0..16_384 {
        state = state.source().unwrap();
    }
    assert_eq!(
        state.source().unwrap_err(),
        AcquisitionError::Bound(Bound {
            field: Field::Sources,
            observed: 16_385,
            limit: 16_384
        })
    );
}

#[test]
fn arithmetic_overflow_refuses_without_wrap_or_saturation() {
    assert_eq!(
        Acquisition(Totals {
            sources: u128::MAX,
            files: 0,
            content: 0
        })
        .source()
        .unwrap_err(),
        AcquisitionError::ArithmeticOverflow
    );
    assert!(
        FinalPopulation::new()
            .package(u128::MAX, 0)
            .unwrap()
            .package(1, 0)
            .is_none()
    );
    assert!(
        FinalPopulation::new()
            .package(0, u128::MAX)
            .unwrap()
            .package(0, 1)
            .is_none()
    );
}
