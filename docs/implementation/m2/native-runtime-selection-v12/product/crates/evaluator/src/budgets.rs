//! Deterministic evaluator work arithmetic. Callers must independently derive
//! census and rule counts; this helper establishes neither input admission nor
//! proof truth, Run authority, or a wall-clock execution allowance.

/// Counts derived by the complete input driver, never from claimed outputs.
#[derive(Clone, Copy, Debug)]
pub struct EvaluationCensus {
    pub inventory_rows: u64,
    pub inventory_locators: u64,
    pub facts: u64,
    pub observations: u64,
    pub coverages: u64,
}
/// One rule's independently enumerated population and policy tree counts.
#[derive(Clone, Copy, Debug)]
pub struct RuleWork {
    pub enabled: bool,
    pub selected_subjects: u64,
    pub predicate_nodes: u64,
    pub atoms: u64,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EvaluationWork {
    WithinBudget {
        work_units: u64,
        predicate_bound: u64,
        finding_bound: u64,
    },
    /// The complete evaluator must emit its prescribed exhausted state and
    /// deficiencies. This is not permission to publish a truncated result.
    BudgetExceeded,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum WorkError {
    OutputBoundExceeded,
}
fn add(a: u128, b: u128, cap: u128) -> u128 {
    a.saturating_add(b).min(cap)
}
fn multiply(a: u128, b: u128, cap: u128) -> u128 {
    a.saturating_mul(b).min(cap)
}
/// Selected evaluator3 cost:
/// inventory rows + locators + sum(selected * (nodes + atoms * scan census)).
/// Disabled rules contribute zero. All intermediate operations preserve the
/// comparison against limit without wrapping; a zero population stays zero
/// even when a per-subject cost exceeds the limit. Output bounds are checked
/// only when work fits, matching budget-exhaustion-before-output-bound order.
/// This arithmetic helper does not verify the provenance of supplied counts.
pub fn estimate_evaluation_work(
    census: EvaluationCensus,
    rules: &[RuleWork],
    limit: u64,
) -> Result<EvaluationWork, WorkError> {
    // A sentinel one larger than U64::MAX fits in u128. Capped arithmetic is
    // exact for comparison with the budget; it is not a claimed exact cost
    // once the cost exceeds that budget.
    let cap = u128::from(limit) + 1;
    let mut cost = add(
        census.inventory_rows.into(),
        census.inventory_locators.into(),
        cap,
    );
    let scan = add(
        add(census.facts.into(), census.observations.into(), cap),
        census.coverages.into(),
        cap,
    );
    let mut predicates = 0;
    let mut findings = 0;
    for rule in rules.iter().filter(|rule| rule.enabled) {
        let per_subject = add(
            rule.predicate_nodes.into(),
            multiply(rule.atoms.into(), scan, cap),
            cap,
        );
        cost = add(
            cost,
            multiply(rule.selected_subjects.into(), per_subject, cap),
            cap,
        );
        predicates = add(
            predicates,
            multiply(
                rule.selected_subjects.into(),
                rule.predicate_nodes.into(),
                100001,
            ),
            100001,
        );
        findings = add(findings, rule.selected_subjects.into(), 100001);
    }
    if cost == cap {
        return Ok(EvaluationWork::BudgetExceeded);
    }
    if predicates > 100000 || findings > 100000 {
        return Err(WorkError::OutputBoundExceeded);
    }
    Ok(EvaluationWork::WithinBudget {
        work_units: cost as u64,
        predicate_bound: predicates as u64,
        finding_bound: findings as u64,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    const EMPTY: EvaluationCensus = EvaluationCensus {
        inventory_rows: 0,
        inventory_locators: 0,
        facts: 0,
        observations: 0,
        coverages: 0,
    };
    fn row(selected_subjects: u64, predicate_nodes: u64, atoms: u64) -> RuleWork {
        RuleWork {
            enabled: true,
            selected_subjects,
            predicate_nodes,
            atoms,
        }
    }
    #[test]
    fn exact_boundary_and_one_less() {
        let census = EvaluationCensus {
            inventory_rows: 3,
            inventory_locators: 5,
            facts: 7,
            observations: 11,
            coverages: 13,
        };
        let rules = [row(2, 3, 2)];
        assert_eq!(
            estimate_evaluation_work(census, &rules, 138),
            Ok(EvaluationWork::WithinBudget {
                work_units: 138,
                predicate_bound: 6,
                finding_bound: 2
            })
        );
        assert_eq!(
            estimate_evaluation_work(census, &rules, 137),
            Ok(EvaluationWork::BudgetExceeded)
        );
    }
    #[test]
    fn inventory_alone_exhausts_even_when_all_rules_disabled() {
        let mut rule = row(u64::MAX, u64::MAX, u64::MAX);
        rule.enabled = false;
        assert_eq!(
            estimate_evaluation_work(
                EvaluationCensus {
                    inventory_rows: 1,
                    ..EMPTY
                },
                &[rule],
                0
            ),
            Ok(EvaluationWork::BudgetExceeded)
        );
        assert_eq!(
            estimate_evaluation_work(EMPTY, &[rule], 0),
            Ok(EvaluationWork::WithinBudget {
                work_units: 0,
                predicate_bound: 0,
                finding_bound: 0
            })
        );
    }
    #[test]
    fn overflow_never_becomes_a_small_successful_cost() {
        assert_eq!(
            estimate_evaluation_work(
                EvaluationCensus {
                    facts: u64::MAX,
                    observations: u64::MAX,
                    coverages: u64::MAX,
                    ..EMPTY
                },
                &[row(u64::MAX, u64::MAX, u64::MAX)],
                u64::MAX
            ),
            Ok(EvaluationWork::BudgetExceeded)
        );
        assert_eq!(
            estimate_evaluation_work(
                EvaluationCensus {
                    inventory_rows: u64::MAX,
                    inventory_locators: 1,
                    ..EMPTY
                },
                &[],
                u64::MAX
            ),
            Ok(EvaluationWork::BudgetExceeded)
        );
    }
    #[test]
    fn zero_population_and_zero_atoms_preserve_zero_products() {
        let census = EvaluationCensus {
            facts: u64::MAX,
            observations: u64::MAX,
            coverages: u64::MAX,
            ..EMPTY
        };
        assert_eq!(
            estimate_evaluation_work(census, &[row(0, u64::MAX, u64::MAX)], 0),
            Ok(EvaluationWork::WithinBudget {
                work_units: 0,
                predicate_bound: 0,
                finding_bound: 0
            })
        );
        assert_eq!(
            estimate_evaluation_work(census, &[row(1, 1, 0)], 1),
            Ok(EvaluationWork::WithinBudget {
                work_units: 1,
                predicate_bound: 1,
                finding_bound: 1
            })
        );
    }
    #[test]
    fn budget_exhaustion_precedes_output_bound_refusal() {
        assert_eq!(
            estimate_evaluation_work(EMPTY, &[row(100001, 1, 0)], 100000),
            Ok(EvaluationWork::BudgetExceeded)
        );
        assert_eq!(
            estimate_evaluation_work(EMPTY, &[row(100001, 1, 0)], 100001),
            Err(WorkError::OutputBoundExceeded)
        );
        assert_eq!(
            estimate_evaluation_work(EMPTY, &[row(100000, 1, 0)], 100000),
            Ok(EvaluationWork::WithinBudget {
                work_units: 100000,
                predicate_bound: 100000,
                finding_bound: 100000
            })
        );
    }
    #[test]
    fn rule_bounds_accumulate_and_u64_max_is_inclusive() {
        assert_eq!(
            estimate_evaluation_work(EMPTY, &[row(50000, 1, 0), row(50001, 1, 0)], u64::MAX),
            Err(WorkError::OutputBoundExceeded)
        );
        assert_eq!(
            estimate_evaluation_work(
                EvaluationCensus {
                    inventory_rows: u64::MAX,
                    ..EMPTY
                },
                &[],
                u64::MAX
            ),
            Ok(EvaluationWork::WithinBudget {
                work_units: u64::MAX,
                predicate_bound: 0,
                finding_bound: 0
            })
        );
    }
}
