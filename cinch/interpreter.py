from copy import deepcopy
from cinch_types import (Operator, If, While, IntegerLiteral, FunctionCall,
                         FunctionDef, Identifier, StatementList, Return,
                         Expression)


def interpret(ast):
    assert isinstance(ast, StatementList)
    variable_table = {}
    interpret_statement_list(None, ast, variable_table)


def interpret_statement_list(parent, ast, variable_table):
    ret = None
    for statement in ast.children:
        ret = interpret_statement(parent, statement, variable_table)
    return ret


def interpret_statement(parent, ast, variable_table):
    if isinstance(ast, If):
        ret = interpret_expression(ast, ast.children[0], variable_table)
        if is_truthy(ret, variable_table):
            interpret_statement_list(ast.children[1], ast.children[1],
                                     variable_table)
    elif isinstance(ast, While):
        interpret_while(parent, ast, variable_table)
    elif isinstance(ast, FunctionCall):
        interpret_func_call(ast, variable_table)
    elif isinstance(ast, FunctionDef):
        interpret_func_def(ast, variable_table)
    elif isinstance(ast, Return):
        return interpret_return_statement(parent, ast, variable_table)
    else:
        assert isinstance(ast, Expression)
        interpret_expression(parent, ast, variable_table)


def interpret_expression(parent, statement, variable_table):
    if isinstance(statement, Operator):
        return interpret_binary_expr(parent, statement, variable_table)
    elif isinstance(statement, Identifier):
        return interpret_identifier(parent, statement, variable_table)
    elif isinstance(statement, FunctionCall):
        return interpret_func_call(statement, variable_table)
    elif isinstance(statement, IntegerLiteral):
        return statement
    else:
        print statement
        assert False


def interpret_identifier(parent, statement, variable_table):
    val = variable_table[statement.value]
    assert isinstance(val, IntegerLiteral)
    return val


def interpret_return_statement(parent, statement, variable_table):
    return interpret_expression(statement, statement.children[0],
                                variable_table)


def is_truthy(node, variable_table):
    assert isinstance(node, IntegerLiteral)
    if node.value == 0:
        return False
    else:
        return True


def interpret_func_def(statement, variable_table):
    variable_table[statement.value] = statement


def interpret_while(parent, statement, variable_table):
    value = interpret_expression(statement, statement.children[0],
                                 variable_table)
    while is_truthy(value, variable_table):
        interpret_statement_list(parent, statement.children[1], variable_table)
        value = interpret_expression(statement, statement.children[0],
                                     variable_table)


def get_value(node, variable_table):
    if isinstance(node, IntegerLiteral):
        value = node.value
    elif isinstance(node, Identifier):
        value = variable_table[node.value].value
    else:
        print node
        assert False
    return value


def interpret_func_call(node, variable_table):
    function = variable_table[node.value]
    # Really we want a copy on write data structure, but that's an optimization
    values = node.children[0].children
    names = function.children[0].children
    local = deepcopy(variable_table)
    for argument, expression in zip(names, values):
        value = interpret_expression(None, expression, variable_table)
        local[argument.value] = value
    return interpret_statement_list(function.children[1], function.children[1],
                                    local)


def interpret_binary_expr(parent, statement, variable_table):
    # TODO: Implement <, <=, >, >=, !=
    rvalue = interpret_expression(statement, statement.children[1],
                                  variable_table)
    if statement.value == '=':
        assert isinstance(statement.children[0], Identifier)
        assert isinstance(statement.children[1], Expression)
        lvalue = statement.children[0]
        variable_table[lvalue.value] = rvalue
        return None
    elif statement.value == '-':
        rvalue = rvalue.value
        lvalue = interpret_expression(statement, statement.children[0],
                                      variable_table).value
        result = IntegerLiteral(lvalue-rvalue)
        return result
    elif statement.value == '+':
        rvalue = rvalue.value
        lvalue = interpret_expression(statement, statement.children[0],
                                      variable_table).value
        result = IntegerLiteral(lvalue+rvalue)
        return result
    elif statement.value == '<':
        rvalue = rvalue.value
        lvalue = interpret_expression(statement, statement.children[0],
                                      variable_table).value
        if lvalue < rvalue:
            result = IntegerLiteral(1)
        else:
            result = IntegerLiteral(0)
        return result
    else:
        print statement
        assert False
