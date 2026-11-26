---- MODULE Counter ----
EXTENDS Naturals
CONSTANT Limit
VARIABLE x
Init == x = 0
Increment == x < Limit /\ x' = x + 1
Next == Increment
BelowLimit == x < Limit
CanIncrement == ENABLED Increment
====
