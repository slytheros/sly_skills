---- MODULE Atoms ----
CONSTANT Nodes
VARIABLES holding, active
Init == holding \in Nodes /\ active = FALSE
Next == holding' \in Nodes /\ active' = TRUE
IsInitial == ~active
IsNode == holding \in Nodes
====
