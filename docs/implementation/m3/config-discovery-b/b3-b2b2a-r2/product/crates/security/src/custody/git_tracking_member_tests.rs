// Law X2 r9 item 6b (M3-B r9 item 21; unit B3-b1): the member observation,
// on scratch Git members built with real `git` under a scratch H, as item
// 6a's tests are. Each control of law item 21 refuses with its subject.

// r2 (Codex B3B1-R1-RF-1): a test-only queue of native capture outcomes for
// item 6b's custody judgments, in capture order; `None` lets the real capture
// through. Item 6a's judgments never consult it.
thread_local! {
    static CAPTURE_FAULTS: std::cell::RefCell<std::collections::VecDeque<Option<DescriptorAclCaptureError>>> =
        const { std::cell::RefCell::new(std::collections::VecDeque::new()) };
}
pub(super) fn injected_capture(
    captured: Result<opensip_platform::DescriptorAclCapture, DescriptorAclCaptureError>,
) -> Result<opensip_platform::DescriptorAclCapture, DescriptorAclCaptureError> {
    match CAPTURE_FAULTS.with(|q| q.borrow_mut().pop_front()) {
        Some(Some(fault)) => Err(fault),
        _ => captured,
    }
}
fn inject(faults: Vec<Option<DescriptorAclCaptureError>>) {
    CAPTURE_FAULTS.with(|q| *q.borrow_mut() = faults.into_iter().collect());
}

/// Item 6a over W, then item 6b over `members`, in one ledger.
fn observe_with_members(
    run: &Run,
    home: &Path,
    w: &Path,
    members: &[&str],
    environment: &[(OsString, OsString)],
) -> (Tracking, Result<Vec<MemberVerdict>, Failure>, usize) {
    let groups = BTreeSet::new();
    let volume = run.volume;
    let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
    let mut ledger = WorkLedger::new();
    let mut tracking = Tracking::NoRepository;
    let result = ledger.scope(|work| {
        let chain = walk_project_chain(home, w, uid(), &policy, work)
            .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
        let clean = vars(&[("HOME", home.to_str().unwrap())]);
        let inputs = TrackingInputs {
            chain: &chain,
            uid: uid(),
            policy: &policy,
            home,
            environment: &clean,
            system_sources: &[],
        };
        let observed = observe_root(&inputs, work)?;
        tracking = observed.observation().tracking();
        let root = observed
            .no_repository()
            .expect("item 6b's precondition: W is in no repository");
        let paths: Vec<MemberPath> = members
            .iter()
            .map(|m| MemberPath::new(m.as_bytes()).unwrap())
            .collect();
        let members = MemberInputs {
            uid: uid(),
            home,
            home_filesystem: &volume,
            environment,
            system_sources: &[],
            custody: MemberCustody {
                trust_groups: &groups,
                premise: Some(&run.premise),
            },
        };
        observe_members(&members, root, &paths, work)
    });
    let used = ledger.used().objects + ledger.used().edges;
    (tracking, result, used)
}
fn clean_env(home: &Path) -> Vec<(OsString, OsString)> {
    vars(&[("HOME", home.to_str().unwrap())])
}
/// A member repository at `w/<rel>` with one committed file.
fn member(githome: &Path, w: &Path, rel: &str) -> PathBuf {
    let m = w.join(rel);
    mkdir(&m);
    git(githome, &m, &["init", "-q"]);
    write(&m.join("README"), b"x\n");
    git(githome, &m, &["add", "README"]);
    git(githome, &m, &["commit", "-q", "-m", "m"]);
    m
}
fn subject(verdict: &MemberVerdict) -> String {
    match verdict {
        MemberVerdict::Refused(refusal) => refusal.subject(),
        MemberVerdict::Admitted { .. } => "admitted".to_owned(),
    }
}
/// Every regular file and directory under `root`, with its bytes.
fn tree_state(root: &Path) -> Vec<(PathBuf, Vec<u8>)> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        for entry in fs::read_dir(&d).unwrap() {
            let p = entry.unwrap().path();
            let meta = fs::symlink_metadata(&p).unwrap();
            if meta.is_dir() {
                out.push((p.clone(), Vec::new()));
                stack.push(p);
            } else {
                out.push((p.clone(), fs::read(&p).unwrap_or_default()));
            }
        }
    }
    out.sort();
    out
}

#[test]
fn conventional_members_are_admitted_with_their_gitlinks_and_nothing_is_written() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        let a = member(&githome, &w, "a");
        member(&githome, &w, "group/b");
        // A submodule-style gitlink inside member a: a nested repository, a boundary.
        let head = git(&githome, &a, &["rev-parse", "HEAD"]);
        git(
            &githome,
            &a,
            &[
                "update-index",
                "--add",
                "--cacheinfo",
                &format!("160000,{},vendor/lib", head.trim()),
            ],
        );
        let before = tree_state(&w);
        let (tracking, verdicts, used) =
            observe_with_members(&Run::new(), &home, &w, &["a", "group/b"], &clean_env(&home));
        assert_eq!(tracking, Tracking::NoRepository);
        assert_eq!(
            verdicts.unwrap(),
            vec![
                MemberVerdict::Admitted {
                    gitlinks: vec![b"vendor/lib".to_vec()]
                },
                MemberVerdict::Admitted {
                    gitlinks: Vec::new()
                },
            ]
        );
        assert!(used > 0, "the pass is charged to the ledger");
        assert_eq!(tree_state(&w), before, "item 6b writes nothing");
    });
}

#[test]
fn every_member_refusal_has_its_subject() {
    churned(|| {
        let run = Run::new();
        let one = |setup: &dyn Fn(&Path, &Path) -> String| -> String {
            let (_s, home, githome) = scratch();
            let w = home.join("code/w");
            mkdir(&w);
            let rel = setup(&githome, &w);
            let (_, verdicts, _) =
                observe_with_members(&run, &home, &w, &[rel.as_str()], &clean_env(&home));
            subject(&verdicts.unwrap()[0])
        };
        // A `.git` file (a submodule checkout or a linked worktree).
        assert_eq!(
            one(&|_g, w| {
                mkdir(&w.join("m"));
                write(&w.join("m/.git"), b"gitdir: /elsewhere\n");
                "m".to_owned()
            }),
            "member-vcs-unsupported:git-not-directory"
        );
        // Another VCS marker at M, and one strictly between W and M.
        assert_eq!(
            one(&|g, w| {
                member(g, w, "m");
                mkdir(&w.join("m/.hg"));
                "m".to_owned()
            }),
            "member-vcs-unsupported:vcs-other"
        );
        assert_eq!(
            one(&|g, w| {
                mkdir(&w.join("x/.hg"));
                member(g, w, "x/m");
                "x/m".to_owned()
            }),
            "member-vcs-unsupported:vcs-other"
        );
        // Configuration refusals, written by git itself.
        for (key, value, expected) in [
            (
                "core.worktree",
                "/elsewhere",
                "member-vcs-unsupported:config-worktree",
            ),
            (
                "include.path",
                "/elsewhere",
                "member-vcs-unsupported:config-include",
            ),
            (
                "extensions.objectformat",
                "sha256",
                "member-vcs-unsupported:config-extensions",
            ),
        ] {
            assert_eq!(
                one(&|g, w| {
                    let m = member(g, w, "m");
                    git(g, &m, &["config", key, value]);
                    "m".to_owned()
                }),
                expected,
                "{key}"
            );
        }
        // `commondir` present: a linked worktree.
        assert_eq!(
            one(&|g, w| {
                let m = member(g, w, "m");
                write(&m.join(".git/commondir"), b"../..\n");
                "m".to_owned()
            }),
            "member-vcs-unsupported:linked-worktree"
        );
        // A split index, as real git writes it. Its main index holds a
        // name-less replacement entry, which item 6a's unchanged decoder
        // refuses as malformed before it reaches the `link` extension (6a's
        // own tests cover the extension itself as `index-split-or-sparse`).
        assert_eq!(
            one(&|g, w| {
                let m = member(g, w, "m");
                git(g, &m, &["update-index", "--split-index"]);
                assert!(fs::read_dir(m.join(".git")).unwrap().any(|e| {
                    e.unwrap()
                        .file_name()
                        .to_string_lossy()
                        .starts_with("sharedindex.")
                }));
                "m".to_owned()
            }),
            "member-vcs-unsupported:index-malformed"
        );
        // Group-writable Git evidence (item 6a's custody, never waived).
        assert_eq!(
            one(&|g, w| {
                let m = member(g, w, "m");
                fs::set_permissions(m.join(".git/index"), fs::Permissions::from_mode(0o664))
                    .unwrap();
                "m".to_owned()
            }),
            "member-vcs-unsupported:index-custody"
        );
        assert_eq!(
            one(&|g, w| {
                let m = member(g, w, "m");
                fs::set_permissions(m.join(".git"), fs::Permissions::from_mode(0o777)).unwrap();
                "m".to_owned()
            }),
            "member-vcs-unsupported:git-custody"
        );
        // A path component that became a symbolic link: placement no longer holds.
        assert_eq!(
            one(&|g, w| {
                let real = member(g, w, "real");
                std::os::unix::fs::symlink(&real, w.join("m")).unwrap();
                "m".to_owned()
            }),
            "member-vcs-unsupported:evidence-changed"
        );
    });
}

#[test]
fn a_device_change_is_outside_the_volume() {
    // Synthetic (law item 21 allows it where the platform cannot mount a
    // volume in a test): W's device as observed differs from the member's.
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "m");
        let run = Run::new();
        let groups = BTreeSet::new();
        let volume = run.volume;
        let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
        let mut ledger = WorkLedger::new();
        let refusal = ledger.scope(|work| {
            let chain = walk_project_chain(&home, &w, uid(), &policy, work)
                .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
            let clean = clean_env(&home);
            let inputs = TrackingInputs {
                chain: &chain,
                uid: uid(),
                policy: &policy,
                home: &home,
                environment: &clean,
                system_sources: &[],
            };
            let root = chain
                .path()
                .directory_at(chain.path().component_count())
                .unwrap();
            let device = metadata(root.as_file(), work)?.device;
            let path = MemberPath::new(b"m").unwrap();
            Ok::<_, Failure>(
                match member_layout(root, device ^ 1, &path, &inputs, Pass::Tracking, work) {
                    Err(WorkFailure::Operation(MemberFailure::Refused(refusal))) => Some(refusal),
                    _ => None,
                },
            )
        });
        assert_eq!(refusal.unwrap(), Some(MemberRefusal::OutsideVolume));
        assert_eq!(
            MemberRefusal::OutsideVolume.subject(),
            "member-outside-volume"
        );
    });
}

#[test]
fn an_environment_refusal_refuses_every_member_of_the_pass() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "a");
        member(&githome, &w, "b");
        let env = vars(&[("HOME", home.to_str().unwrap()), ("GIT_DIR", "/elsewhere")]);
        let (_, verdicts, _) = observe_with_members(&Run::new(), &home, &w, &["a", "b"], &env);
        let subjects: Vec<String> = verdicts.unwrap().iter().map(subject).collect();
        assert_eq!(subjects, vec!["member-vcs-unsupported:environment-git"; 2]);
    });
}

#[test]
fn w_inside_a_repository_gives_no_precondition() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        git(&githome, &w, &["init", "-q"]);
        let run = Run::new();
        let groups = BTreeSet::new();
        let volume = run.volume;
        let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
        let clean = clean_env(&home);
        let mut ledger = WorkLedger::new();
        let precondition = ledger.scope(|work| {
            let chain = walk_project_chain(&home, &w, uid(), &policy, work)
                .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
            let inputs = TrackingInputs {
                chain: &chain,
                uid: uid(),
                policy: &policy,
                home: &home,
                environment: &clean,
                system_sources: &[],
            };
            let observed = observe_root(&inputs, work)?;
            assert_eq!(
                observed.observation().tracking(),
                Tracking::Untracked { repositories: 1 }
            );
            Ok::<_, Failure>(observed.no_repository().is_some())
        });
        assert!(!precondition.unwrap(), "item 6b cannot run without W2");
    });
}

#[test]
fn sixty_four_members_are_observed_in_one_pass() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        let names: Vec<String> = (0..64).map(|i| format!("m{i:02}")).collect();
        for name in &names {
            let m = w.join(name);
            mkdir(&m);
            git(&githome, &m, &["init", "-q"]);
        }
        let refs: Vec<&str> = names.iter().map(String::as_str).collect();
        let (_, verdicts, _) =
            observe_with_members(&Run::new(), &home, &w, &refs, &clean_env(&home));
        let verdicts = verdicts.unwrap();
        assert_eq!(verdicts.len(), 64);
        assert!(verdicts.iter().all(|v| *v
            == MemberVerdict::Admitted {
                gitlinks: Vec::new()
            }));
    });
}

#[test]
fn member_paths_are_canonical_and_at_most_256_deep() {
    for bad in [
        &b""[..],
        b".",
        b"..",
        b"a//b",
        b"/a",
        b"a/",
        b"a/./b",
        b"a/../b",
        b"a\0b",
    ] {
        assert!(
            MemberPath::new(bad).is_none(),
            "{:?}",
            String::from_utf8_lossy(bad)
        );
    }
    let deep = vec!["d"; 256].join("/");
    assert!(MemberPath::new(deep.as_bytes()).is_some());
    let deeper = vec!["d"; 257].join("/");
    assert!(MemberPath::new(deeper.as_bytes()).is_none());
    assert_eq!(MemberPath::new(b"a/b").unwrap().spelling(), b"a/b");
}

#[test]
fn a_capture_refusal_refuses_its_member_and_the_ledger_goes_on() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "a");
        member(&githome, &w, "b");
        let run = Run::new();
        // A refused first member followed by a valid one: the first member's
        // `.git` capture reports a change, then `Malformed` on the second
        // pass's lone member; the ledger stays usable for the rest.
        inject(vec![Some(DescriptorAclCaptureError::Changed)]);
        let (_, verdicts, _) =
            observe_with_members(&run, &home, &w, &["a", "b"], &clean_env(&home));
        let subjects: Vec<String> = verdicts
            .expect("the ledger is not latched")
            .iter()
            .map(subject)
            .collect();
        assert_eq!(
            subjects,
            vec![
                "member-vcs-unsupported:git-custody".to_owned(),
                "admitted".to_owned()
            ]
        );
        inject(vec![
            None,
            Some(DescriptorAclCaptureError::Malformed("injected")),
        ]);
        let (_, verdicts, _) = observe_with_members(&run, &home, &w, &["a"], &clean_env(&home));
        let subjects: Vec<String> = verdicts
            .expect("a lone refused member returns its verdict")
            .iter()
            .map(subject)
            .collect();
        assert_eq!(
            subjects,
            vec!["member-vcs-unsupported:config-custody".to_owned()]
        );
        inject(Vec::new());
    });
}

#[test]
fn a_pass_level_capture_refusal_refuses_every_member_without_latching() {
    churned(|| {
        let (_s, home, githome) = scratch();
        write(&home.join(".gitconfig"), b"[user]\n\tname = t\n");
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "a");
        member(&githome, &w, "b");
        // The pass's first capture is the global `~/.gitconfig`.
        inject(vec![Some(DescriptorAclCaptureError::Unsupported)]);
        let (_, verdicts, _) =
            observe_with_members(&Run::new(), &home, &w, &["a", "b"], &clean_env(&home));
        let subjects: Vec<String> = verdicts.expect("not latched").iter().map(subject).collect();
        assert_eq!(subjects, vec!["member-vcs-unsupported:global-custody"; 2]);
        inject(Vec::new());
    });
}

/// Item 6a over `w` under one ledger scope, then item 6b with the proof of
/// `proof_root` (r3, Codex B3B1-R2-RF-1): `between` runs after `proof_root`'s
/// chain is retained and observed, and before `w`'s chain is walked.
/// Returns whether `w` itself gave a proof, and the member verdicts under
/// `proof_root`'s proof.
fn substituted(
    home: &Path,
    proof_root: &Path,
    w: &Path,
    members: &[&str],
    between: impl FnOnce(),
) -> (bool, Vec<String>) {
    let run = Run::new();
    let groups = BTreeSet::new();
    let volume = run.volume;
    let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
    let clean = clean_env(home);
    let mut ledger = WorkLedger::new();
    let outcome = ledger.scope(|work| {
        let chain_a = walk_project_chain(home, proof_root, uid(), &policy, work)
            .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
        let observed_a = observe_root(
            &TrackingInputs {
                chain: &chain_a,
                uid: uid(),
                policy: &policy,
                home,
                environment: &clean,
                system_sources: &[],
            },
            work,
        )?;
        let token = observed_a
            .no_repository()
            .expect("the proof root is in no repository");
        between();
        let chain_b = walk_project_chain(home, w, uid(), &policy, work)
            .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
        let observed_b = observe_root(
            &TrackingInputs {
                chain: &chain_b,
                uid: uid(),
                policy: &policy,
                home,
                environment: &clean,
                system_sources: &[],
            },
            work,
        )?;
        let members_b = MemberInputs {
            uid: uid(),
            home,
            home_filesystem: &volume,
            environment: &clean,
            system_sources: &[],
            custody: MemberCustody {
                trust_groups: &groups,
                premise: Some(&run.premise),
            },
        };
        let paths: Vec<MemberPath> = members
            .iter()
            .map(|m| MemberPath::new(m.as_bytes()).unwrap())
            .collect();
        let verdicts = observe_members(&members_b, token, &paths, work)?;
        Ok::<_, Failure>((
            observed_b.no_repository().is_some(),
            verdicts.iter().map(subject).collect(),
        ))
    });
    outcome.expect("the member pass completes")
}

#[test]
fn a_proof_for_one_root_never_authorizes_another() {
    // W_A outside any repository, W_B inside one under another spelling: the
    // member pass under W_A's proof walks from W_A's retained chain, never
    // W_B's, and W_B gives no proof of its own.
    churned(|| {
        let (_s, home, githome) = scratch();
        let wa = home.join("code/plain");
        mkdir(&wa);
        member(&githome, &wa, "a");
        let repo = home.join("code/repo");
        mkdir(&repo);
        git(&githome, &repo, &["init", "-q"]);
        let wb = repo.join("w");
        mkdir(&wb);
        member(&githome, &wb, "m");
        let (w_b_proof, subjects) = substituted(&home, &wa, &wb, &["a", "m"], || {});
        assert!(!w_b_proof, "W_B is inside a repository");
        assert_eq!(
            subjects,
            vec!["admitted", "member-vcs-unsupported:evidence-changed"]
        );
    });
}

#[test]
fn a_proof_never_authorizes_another_root_at_the_same_spelling() {
    // r3 (Codex B3B1-R2-RF-1): W_A is retained and observed in no
    // repository, then moved aside; a repository with a nested repository
    // `m` takes its spelling. The proof is W_A's retained chain, so the
    // member pass is over W_A: `a` is still admitted there, the replacement's
    // `m` is not reached, and the replacement gives no proof of its own.
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "a");
        let (w_b_proof, subjects) = substituted(&home, &w, &w, &["a", "m"], || {
            std::fs::rename(&w, home.join("code/w-moved")).unwrap();
            mkdir(&w);
            git(&githome, &w, &["init", "-q"]);
            member(&githome, &w, "m");
        });
        assert!(!w_b_proof, "the replacement is a repository");
        assert_eq!(
            subjects,
            vec!["admitted", "member-vcs-unsupported:evidence-changed"]
        );
    });
}

// ------------------------------------------------ unit B3-b2b2a: the binding

/// Item 6a over each of `roots` in one ledger scope, each walked as its own
/// retained chain; `between` runs after the first. The observations and,
/// for every (chain, observation) pair, whether `NoRepository::retained`
/// gives a proof.
fn retained_pairs(
    home: &Path,
    roots: &[&Path],
    between: impl FnOnce(),
) -> (Vec<TrackingObservation>, Vec<Vec<bool>>) {
    let run = Run::new();
    let groups = BTreeSet::new();
    let volume = run.volume;
    let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
    let clean = clean_env(home);
    let mut ledger = WorkLedger::new();
    let mut between = Some(between);
    ledger
        .scope(|work| {
            let mut chains = Vec::new();
            let mut observed = Vec::new();
            for root in roots {
                let chain = walk_project_chain(home, root, uid(), &policy, work).map_err(|_| {
                    WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain"))
                })?;
                let inputs = TrackingInputs {
                    chain: &chain,
                    uid: uid(),
                    policy: &policy,
                    home,
                    environment: &clean,
                    system_sources: &[],
                };
                observed.push(observe_tracking(&inputs, work)?);
                chains.push(chain);
                if let Some(between) = between.take() {
                    between();
                }
            }
            let proofs = chains
                .iter()
                .map(|chain| {
                    observed
                        .iter()
                        .map(|o| NoRepository::retained(chain, o).is_some())
                        .collect()
                })
                .collect();
            Ok::<_, Failure>((observed, proofs))
        })
        .expect("the observations complete")
}

#[test]
fn a_retained_proof_needs_the_very_chain_item_6a_walked() {
    // The same directory walked twice is two retained chains: each gets the
    // proof only from its own observation. The observations still compare
    // equal, so item 6a's recheck is unchanged by the identity.
    churned(|| {
        let (_s, home, _githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        let (observed, proofs) = retained_pairs(&home, &[&w, &w], || {});
        assert_eq!(proofs, vec![vec![true, false], vec![false, true]]);
        assert_eq!(
            observed[0], observed[1],
            "the recheck compares the decision and evidence only"
        );
    });
}

#[test]
fn no_retained_proof_for_a_repository_or_a_replacement_at_the_same_spelling() {
    churned(|| {
        let (_s, home, githome) = scratch();
        // W inside a repository: no proof, for its own chain or any other.
        let repo = home.join("code/repo");
        mkdir(&repo);
        git(&githome, &repo, &["init", "-q"]);
        let (observed, proofs) = retained_pairs(&home, &[&repo], || {});
        assert_eq!(
            observed[0].tracking(),
            Tracking::Untracked { repositories: 1 }
        );
        assert_eq!(proofs, vec![vec![false]]);
        // W observed in no repository, then moved aside; a repository takes
        // its spelling. The replacement's chain never gets W's proof.
        let w = home.join("code/w");
        mkdir(&w);
        let (observed, proofs) = retained_pairs(&home, &[&w, &w], || {
            fs::rename(&w, home.join("code/w-moved")).unwrap();
            mkdir(&w);
            git(&githome, &w, &["init", "-q"]);
        });
        assert_eq!(observed[0].tracking(), Tracking::NoRepository);
        assert_eq!(
            observed[1].tracking(),
            Tracking::Untracked { repositories: 1 }
        );
        assert_eq!(proofs, vec![vec![true, false], vec![false, false]]);
    });
}

/// `observe_members` and the session over the same members, each in its own
/// ledger: their subjects and their charges.
fn both_ways(
    home: &Path,
    w: &Path,
    members: &[&str],
    environment: &[(OsString, OsString)],
) -> [(Vec<String>, WorkCost); 2] {
    let run = Run::new();
    let groups = BTreeSet::new();
    let volume = run.volume;
    let policy = ProjectChainPolicy::new(Some(&run.premise), &volume, &groups);
    let clean = clean_env(home);
    let paths: Vec<MemberPath> = members
        .iter()
        .map(|m| MemberPath::new(m.as_bytes()).unwrap())
        .collect();
    let member_inputs = MemberInputs {
        uid: uid(),
        home,
        home_filesystem: &volume,
        environment,
        system_sources: &[],
        custody: MemberCustody {
            trust_groups: &groups,
            premise: Some(&run.premise),
        },
    };
    [false, true].map(|session| {
        let mut ledger = WorkLedger::new();
        let subjects = ledger
            .scope(|work| {
                let chain = walk_project_chain(home, w, uid(), &policy, work).map_err(|_| {
                    WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain"))
                })?;
                let inputs = TrackingInputs {
                    chain: &chain,
                    uid: uid(),
                    policy: &policy,
                    home,
                    environment: &clean,
                    system_sources: &[],
                };
                let observed = observe_tracking(&inputs, work)?;
                let proof =
                    NoRepository::retained(&chain, &observed).expect("W is in no repository");
                let verdicts = if session {
                    let session = MemberSession::begin(&member_inputs, proof, work)?;
                    paths
                        .iter()
                        .map(|m| session.observe(m, work))
                        .collect::<Result<Vec<_>, _>>()?
                } else {
                    observe_members(&member_inputs, proof, &paths, work)?
                };
                Ok::<_, Failure>(verdicts.iter().map(subject).collect::<Vec<_>>())
            })
            .expect("the pass completes");
        (subjects, ledger.used())
    })
}

#[test]
fn the_session_gives_observe_members_verdicts_and_charges_one_member_at_a_time() {
    churned(|| {
        let (_s, home, githome) = scratch();
        let w = home.join("code/w");
        mkdir(&w);
        member(&githome, &w, "a");
        member(&githome, &w, "b");
        mkdir(&w.join("b/.hg"));
        member(&githome, &w, "c");
        let [batch, session] = both_ways(&home, &w, &["a", "b", "c"], &clean_env(&home));
        assert_eq!(
            batch.0,
            vec!["admitted", "member-vcs-unsupported:vcs-other", "admitted"]
        );
        assert_eq!(batch, session);
        // A pass-level refusal at `begin` is every member's verdict, and no
        // member is observed: the charges still equal the batch's.
        let env = vars(&[("HOME", home.to_str().unwrap()), ("GIT_DIR", "/elsewhere")]);
        let [batch, session] = both_ways(&home, &w, &["a", "b"], &env);
        assert_eq!(batch.0, vec!["member-vcs-unsupported:environment-git"; 2]);
        assert_eq!(batch, session);
    });
}

#[test]
fn the_chain_identity_allocator_never_reuses_an_identity_at_its_end() {
    // r2 (Codex B3B2B2A-R1-RF-1): a local counter near the end of the space
    // (the live global one is untouched). It issues its last identities, then
    // nothing, and never wraps to an identity already issued.
    use std::sync::atomic::{AtomicU64, Ordering};
    let counter = AtomicU64::new(u64::MAX - 2);
    let first = super::super::project_chain::draw_identity(&counter).unwrap();
    let second = super::super::project_chain::draw_identity(&counter).unwrap();
    assert_ne!(first, second);
    assert_eq!(super::super::project_chain::draw_identity(&counter), None);
    assert_eq!(super::super::project_chain::draw_identity(&counter), None);
    assert_eq!(
        counter.load(Ordering::Relaxed),
        u64::MAX,
        "the counter never wraps"
    );
}
