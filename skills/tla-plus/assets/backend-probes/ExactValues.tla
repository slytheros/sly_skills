------------------------- MODULE ExactValues -------------------------
EXTENDS TLAPS
Keys == {"alpha", "beta", "gamma", "delta"}
GroupedKeys == {"alpha", "beta"} \cup {"gamma", "delta"}
THEOREM SameKeys == GroupedKeys = Keys
BY IsaMT("auto", 5) DEF GroupedKeys, Keys
THEOREM SameRecord ==
  [alpha |-> TRUE, beta |-> FALSE] =
  [k \in {"alpha", "beta"} |-> IF k = "alpha" THEN TRUE ELSE FALSE]
BY IsaMT("auto", 5)
=============================================================================
