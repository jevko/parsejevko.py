from jevko import parseJevko, jevkoToString, argsToJevko

print(jevkoToString(parseJevko("a [b] c [d] e")))

print(jevkoToString(argsToJevko("a ", ["b"], " c", " ", ["d"], " ", "e")))