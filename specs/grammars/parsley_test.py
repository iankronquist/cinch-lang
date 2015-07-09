import parsley

with open('cinch.parsley', 'r') as f:
    grammar = f.read()

def if_func(e, s):
    if e:
        for stmt in s:
            machine(stmt).expression()
machine = parsley.makeGrammar(grammar, {'if_func': if_func})


print(machine("123145").number())
print(machine("1 + 1").expression())
print(machine("if ( 0 ) { 1 + 1 }").if_statement())
