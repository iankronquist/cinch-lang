from cinch_types import (Operator, If, While, IntegerLiteral, FunctionCall,
                         FunctionDef, Identifier, IdentifierList,
                         StatementList, ExpressionList, ArgumentList,
                         Operators, BinaryExpression)


def interpret(ast):
    assert isinstance(ast, StatementList)
    variable_table = {}
    interpret_statement_list(ast, variable_table)

def interpret_statement_list(ast, variable_table):
    for statement in ast:
        if isinstance(statement, BinaryExpression):
            interpret_binary_expr(statement, variable_table)
        elif isinstance(statement, If):
            if is_truthy(statement[0]):
                interpret_statement_list(statement[1], variable_table)
        elif isinstance(statement, While):
            interpret_while(statement, variable_table)
        elif isinstance(statement, FunctionCall):
            interpret_func_call(statement, variable_table)
        elif isinstance(statement, FunctionDef):
            interpret_func_def(statement, variable_table)

def is_truthy(node):
    assert isinstance(node, (Identifier, IntegerLiteral))
    if isinstance(node, Identifier):
        val = variable_table.get(node.value, None)
        # This isn't idiomatic python because it's meant to be obvious to
        # those not familiar with the language
        if val is None:
            print('{0} is undefined!'.format(node.value))
            sys.exit(1)
        elif val == 0:
            return False
        else:
            return True
    else:
        if node.value == 0:
            return False
        else:
            return True

def interpret_func_def(statement, variable_table):
    variable_table[statement[0]] = statement[1]

def interpret_while(statement, variable_table):
    while is_truthy(statement[0]):
        interpret_statement_list(statement[1])

def get_value(node, variable_table):
    if isinstance(statement[1], IntegerLiteral):
        value = statement[1].value
    else:
        value = variable_table.get[statement[1]]
    return value

def interpret_func_call(node, variable_table):
    function = variable_table[node.value]
    local = variable_table.copy()
    local.update(zip(function[0], node[0]))
    interpret_statement_list(statement[1], local)

def interpret_binary_expr(parent, statement, variable_table):
    if statement.value == '=':
        assert isinstance(statement[0], Identifier)
        assert isinstance(statement[1], (Identifier, IntegerLiteral, Operator))
        lvalue = statement[0].value
        rvalue = get_value(statement[1], variable_table)
        variable_table[lvalue] = rvalue
    elif statement.value == '-':
        lvalue = get_value(statement[0], variable_table)
        rvalue = get_value(statement[1], variable_table)
        result = IntegerLiteral(lvalue-rvalue)
        insert_in_tree(statement, result)
    elif statement.value == '+':
        lvalue = get_value(statement[0], variable_table)
        rvalue = get_value(statement[1], variable_table)
        result = IntegerLiteral(lvalue+rvalue)
        insert_in_tree(parent, statement, result)

def insert_in_tree(parent, old, new):
    index = parent.index(old)
    parent.pop(index)
    parent.insert(new)
