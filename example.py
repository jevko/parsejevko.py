from jevko import parseJevko, jevkoToString, argsToJevko, interjevkoToSchema

print(jevkoToString(parseJevko("a [b] c [d] e")))
print(jevkoToString(argsToJevko("a ", ["b"], " c", " ", ["d"], " ", "e")))
print(interjevkoToSchema(parseJevko("a [1] c [true] x [sss] y [[a][b]]")))