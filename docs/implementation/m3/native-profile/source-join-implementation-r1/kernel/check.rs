mod core { pub use cargo::core::SourceId; }
#[allow(dead_code)] mod source_join;
use source_join::{compare_nonpath,Refusal};
fn good(l:&str,m:&str){let d=compare_nonpath(l,Some(m)).unwrap();assert_eq!(d.original_lock_source,l);assert_eq!(d.original_metadata_source,m);assert_eq!(d.lock_source,d.metadata_source);assert!(d.lock_source.has_same_precise_as(d.metadata_source));}
fn main(){
 good("registry+https://github.com/rust-lang/crates.io-index","registry+https://github.com/rust-lang/crates.io-index");
 good("sparse+https://index.crates.io/","sparse+https://index.crates.io/");
 good("git+https://github.com/example/repo?branch=topic%2Fwork#REVISION","git+https://github.com/example/repo?branch=topic/work#REVISION");
 good("git+https://github.com/Example/Repo.git#revision","git+https://github.com/example/repo#revision");
 good("git+https://github.com/example/repo#not-a-hex-revision","git+https://github.com/example/repo#not-a-hex-revision");
 assert!(matches!(compare_nonpath("",Some("registry+https://example.com/index")),Err(Refusal::EmptyLockSource)));
 assert!(matches!(compare_nonpath("registry+https://example.com/index",None),Err(Refusal::MissingMetadataSource)));
 assert!(matches!(compare_nonpath("bad",Some("registry+https://example.com/index")),Err(Refusal::LockParse(_))));
 assert!(matches!(compare_nonpath("registry+https://example.com/index",Some("bad")),Err(Refusal::MetadataParse(_))));
 assert!(matches!(compare_nonpath("path+file:///pure-data/path",Some("path+file:///pure-data/path")),Err(Refusal::PathInNonpath)));
 assert!(matches!(compare_nonpath("git+https://example.com/repo",Some("git+https://example.com/repo")),Err(Refusal::MissingGitPrecise)));
 assert!(matches!(compare_nonpath("git+https://example.com/repo#",Some("git+https://example.com/repo#")),Err(Refusal::MissingGitPrecise)));
 let l="git+https://example.com/repo#revisionA";let m="git+https://example.com/repo#revisionB";assert_eq!(core::SourceId::from_url(l).unwrap(),core::SourceId::from_url(m).unwrap());assert!(matches!(compare_nonpath(l,Some(m)),Err(Refusal::DifferentSource)));
 assert!(matches!(compare_nonpath("registry+https://example.com/a",Some("registry+https://example.com/b")),Err(Refusal::DifferentSource)));
 assert!(matches!(compare_nonpath("registry+https://example.com/a",Some("sparse+https://example.com/a")),Err(Refusal::DifferentSource)));
 assert!(matches!(compare_nonpath("git+https://example.com/repo?branch=one#same",Some("git+https://example.com/repo?branch=two#same")),Err(Refusal::DifferentSource)));
 let l="git+https://example.com/repo?branch=topic%2Ffoo%2Bbar#same";let m="git+https://example.com/repo?branch=topic/foo+bar#same";assert!(matches!(compare_nonpath(l,Some(m)),Err(Refusal::DifferentSource)));
 // Reverse canonical spelling construction for a previously uninterned pair.
 good("git+https://github.com/example/second#same","git+https://github.com/Example/Second.git#same");
 println!("18 exact pinnedCargo nonpathcomparison controls passed; raw spellings retained; no source admission");
}
