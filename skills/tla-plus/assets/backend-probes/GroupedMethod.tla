------------------------- MODULE GroupedMethod -------------------------
EXTENDS TLAPS
CONSTANT P
THEOREM Identity == P => P
BY IsaMT("(rule impI, assumption)", 5)
=============================================================================
