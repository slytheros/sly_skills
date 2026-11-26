---- MODULE Witness ----
LOCAL INSTANCE TLC

CounterExample ==
	[action |-> {<<<<1, [x |-> 0]>>, [name |-> "Increment", location |-> [beginLine |-> 6, beginColumn |-> 14, endLine |-> 6, endColumn |-> 36, module |-> "Counter"]], <<2, [x |-> 1]>>>>, <<<<2, [x |-> 1]>>, [name |-> "Increment", location |-> [beginLine |-> 6, beginColumn |-> 14, endLine |-> 6, endColumn |-> 36, module |-> "Counter"]], <<3, [x |-> 2]>>>>}, state |-> {<<1, [x |-> 0]>>, <<2, [x |-> 1]>>, <<3, [x |-> 2]>>}]

====
