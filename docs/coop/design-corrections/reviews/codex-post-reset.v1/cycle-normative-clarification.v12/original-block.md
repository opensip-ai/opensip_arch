these occurrences. An annotation on the occurrence, its enclosing schema path,
or an intermediate alias applies to that occurrence. An annotation on the
terminal governed scalar definition does **not** provide a blanket default for
all references to that type. Directly annotated top-level selector properties remain subject to retention
and join checks even when their scalar form is not one of these three.
