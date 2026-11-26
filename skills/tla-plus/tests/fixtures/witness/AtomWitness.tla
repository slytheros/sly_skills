---- MODULE AtomWitness ----
LOCAL INSTANCE TLC

CounterExample ==
	[action |-> {<<<<1, [active |-> FALSE, holding |-> a]>>, [name |-> "Next", location |-> [beginLine |-> 5, beginColumn |-> 9, endLine |-> 5, endColumn |-> 44, module |-> "Atoms"]], <<2, [active |-> TRUE, holding |-> a]>>>>}, state |-> {<<1, [active |-> FALSE, holding |-> a]>>, <<2, [active |-> TRUE, holding |-> a]>>}]

====
