from copy import deepcopy
from cinch_types import (Operator, If, While, IntegerLiteral, FunctionCall,
                         FunctionDef, Identifier, StatementList, Return,
                         Expression)


def interpret(ast):
    assert isinstance(ast, StatementList)
    variable_table = {}
    interpret_statement_list(None, ast, variable_table)


def interpret_statement_list(parent, ast, variable_table):
    for statement in ast.children:
        interpret_statement(parent, statement, variable_table)


def interpret_statement(parent, ast, variable_table):
    if isinstance(ast, If):
        interpret_expression(ast, ast.children[0], variable_table)
        if is_truthy(ast.children[0], variable_table):
            interpret_statement_list(ast.children[1], ast.children[1],
                                     variable_table)
    elif isinstance(ast, While):
        interpret_while(parent, ast, variable_table)
    elif isinstance(ast, FunctionCall):
        interpret_func_call(ast, variable_table)
    elif isinstance(ast, FunctionDef):
        interpret_func_def(ast, variable_table)
    elif isinstance(ast, Return):
        interpret_return_statement(parent, ast, variable_table)
    else:
        assert isinstance(ast, Expression)
        interpret_expression(parent, ast, variable_table)


def interpret_expression(parent, statement, variable_table):
    if isinstance(statement, Operator):
        interpret_binary_expr(parent, statement, variable_table)
    elif isinstance(statement, Identifier):
        interpret_identifier(parent, statement, variable_table)
    elif isinstance(statement, FunctionCall):
        interpret_func_call(statement, variable_table)
    elif isinstance(statement, IntegerLiteral):
        pass
    else:
        assert 0


def interpret_identifier(parent, statement, variable_table):
    val = variable_table[statement.value]
    assert isinstance(val, IntegerLiteral)
    insert_in_tree(parent, statement, val)


def interpret_return_statement(parent, statement, variable_table):
    interpret_expression(statement, statement.children[0],
                         variable_table)
    insert_in_tree(parent, statement, statement.children[0])


def is_truthy(node, variable_table):
    assert isinstance(node, (Identifier, IntegerLiteral))
    if isinstance(node, Identifier):
        val = variable_table[node.value]
        if val == 0:
            return False
        else:
            return True
    else:
        if node.value == 0:
            return False
        else:
            return True


def interpret_func_def(statement, variable_table):
    variable_table[statement.value] = statement


def interpret_while(parent, statement, variable_table):
    interpret_expression(statement, statement.children[0], variable_table)
    while is_truthy(statement.children[0], variable_table):
        interpret_statement_list(parent, statement.children[1], {})
        interpret_expression(statement, statement.children[0], variable_table)


def get_value(node, variable_table):
    if isinstance(node, IntegerLiteral):
        value = node.value
    elif isinstance(node, Identifier):
        value = variable_table[node.value]
    else:
        assert False
    return value


def interpret_func_call(node, variable_table):
    function = variable_table[node.value]
    # Really we want a copy on write data structure, but that's an optimization
    arguments = deepcopy(node.children[0])
    parent = deepcopy(function)
    local = deepcopy(variable_table)
    # FIXME: This is way too complicated
    resolve_values(arguments, local)
    for child, argument in zip(parent.children[0].children, arguments.children):
        local[child.value] = argument
    interpret_statement_list(parent.children[1], parent.children[1], local)


def resolve_values(expression_list, variable_table):
    for expr in expression_list.children:
        interpret_expression(expression_list, expr, variable_table)
    return expression_list


def interpret_binary_expr(parent, statement, variable_table):
    # TODO: Implement <, <=, >, >=, !=
    lvalue = get_value(statement.children[0], variable_table).value
    rvalue = get_value(statement.children[1], variable_table).value
    if statement.value == '=':
        assert isinstance(statement.children[0], Identifier)
        assert isinstance(statement.children[1],
                          (Identifier, IntegerLiteral, Operator))
        variable_table[lvalue] = rvalue
    elif statement.value == '-':
        result = IntegerLiteral(lvalue-rvalue)
        insert_in_tree(statement, result)
    elif statement.value == '+':
        result = IntegerLiteral(lvalue+rvalue)
        insert_in_tree(parent, statement, result)
    elif statement.value == '<':
        if lvalue < rvalue:
            result = IntegerLiteral(1)
        else:
            result = IntegerLiteral(0)
        insert_in_tree(parent, statement, result)
    else:
        assert 0


def insert_in_tree(parent, old, new):
    index = parent.index(old)
    parent.pop(index)
    parent.insert(index, new)
