use std::{collections::BTreeMap, sync::Arc};

/// A host-owned request capability. It exposes no identifier or mint authority.
/// It is neither deserializable nor independently constructible.
pub struct RequestContext {
    _private: u8,
}

#[derive(Debug, PartialEq, Eq)]
pub enum RequestAllocationError {
    EntropyUnavailable,
    CollisionExhausted,
}

/// Process-custody registry for the explicitly nonpersistent metadata host.
/// Durable host audit custody uses the separately implemented durable ingress.
#[derive(Default)]
pub(crate) struct RequestAuthority {
    reservations: BTreeMap<[u8; 16], Arc<RequestContext>>,
}
impl RequestAuthority {
    pub(crate) fn begin(&mut self) -> Result<Arc<RequestContext>, RequestAllocationError> {
        self.allocate(|| {
            opensip_platform::request_entropy()
                .map_err(|_| RequestAllocationError::EntropyUnavailable)
        })
    }
    fn allocate(
        &mut self,
        mut draw: impl FnMut() -> Result<[u8; 16], RequestAllocationError>,
    ) -> Result<Arc<RequestContext>, RequestAllocationError> {
        for _ in 0..8 {
            let id = draw()?;
            if let std::collections::btree_map::Entry::Vacant(entry) = self.reservations.entry(id) {
                let context = Arc::new(RequestContext { _private: 1 });
                entry.insert(Arc::clone(&context));
                return Ok(context);
            }
        }
        Err(RequestAllocationError::CollisionExhausted)
    }
    pub(crate) fn project(&self, context: &RequestContext) -> Option<String> {
        self.reservations.iter().find_map(|(id, reserved)| {
            if !std::ptr::eq(Arc::as_ptr(reserved), context) {
                return None;
            }
            let mut text = String::from("req1_");
            use std::fmt::Write;
            for byte in id {
                write!(&mut text, "{byte:02x}").expect("String writes cannot fail");
            }
            Some(text)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn foreign_and_unreserved_contexts_cannot_project() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.allocate(|| Ok([1; 16])).unwrap();
        let y = b.allocate(|| Ok([1; 16])).unwrap();
        assert!(a.project(&y).is_none());
        assert!(b.project(&x).is_none());
        assert!(a.project(&RequestContext { _private: 1 }).is_none());
        assert_eq!(
            a.project(&x).unwrap(),
            "req1_01010101010101010101010101010101"
        );
        assert_eq!(a.reservations.len(), 1);
    }
    #[test]
    fn collision_budget_and_error_do_not_publish_or_replace() {
        let mut a = RequestAuthority::default();
        let first = a.allocate(|| Ok([0; 16])).unwrap();
        let mut draws = 0;
        assert!(matches!(
            a.allocate(|| {
                draws += 1;
                Ok([0; 16])
            }),
            Err(RequestAllocationError::CollisionExhausted)
        ));
        assert_eq!(draws, 8);
        assert_eq!(a.reservations.len(), 1);
        assert!(a.project(&first).is_some());
        assert!(matches!(
            a.allocate(|| Err(RequestAllocationError::EntropyUnavailable)),
            Err(RequestAllocationError::EntropyUnavailable)
        ));
        assert_eq!(a.reservations.len(), 1);
        let mut calls = 0;
        let second = a
            .allocate(|| {
                calls += 1;
                Ok([if calls < 3 { 0 } else { 2 }; 16])
            })
            .unwrap();
        assert_eq!(calls, 3);
        assert_ne!(a.project(&first), a.project(&second));
    }
}
