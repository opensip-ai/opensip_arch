# D4-2 control repair

The prior d4-2-checks-r1b lane retained two surviving mutations: allocation-before-its-charge and parent-dropped. This continuation changes the existing test file only; it does not alter the production adapter or trust implementation.

The allocation-order guard now inventories `::with_capacity(` calls, including explicitly typed `Vec::<T>::with_capacity`, so an extra unfunded allocation cannot evade the site count. The new behavioral control admits a validated analyzer with a root command and a child with an explicit parent; the child name is in the reserved root set. It requires admission of the original digest. Losing the parent would create two apparent roots and incorrectly refuse this valid component. The control exercises body validation, the view, host projection and real excluded-form judge; it does not mock the projection.

The full lane uses the existing thirteen mutations unchanged and expects one additional host test (nine above base). Original test bytes are retained as component_admission_tests.before.rs. Raw failed prior lanes are preserved. Results remain pending until the new lane and independent review finish.
