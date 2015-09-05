import sys

from cinch_types import (Operator, If, While, IntegerLiteral, FunctionCall,
                         FunctionDef, Identifier, IdentifierList,
                         StatementList, ExpressionList, ArgumentList,
                         Operators)


# Now this is where things get complicated. The parser takes in an array of
# tokens and returns an abstract syntax tree. Parsing is perhaps the hardest
# problem in the process of compilation, but don't fear! We'll take it slowly
# and keep it simple.

def eat(expected_token, tokens):
    if tokens[0] != expected_token:
        print 'Syntax error'
        print 'eat', expected_token, tokens
        exit()
    tokens.pop(0)


# Parse takes a list of tokens and returns an abstract syntax tree.
def parse(tokens):
    return parse_statement_list(tokens)


# statement ::= expression | while_loop | if_statment
def parse_statement(tokens):
    # Gobble empty tokens
    if tokens[0] == '':
        tokens.pop(0)
        return parse_statement(tokens)
    elif tokens[0] == 'if':
        return parse_if_statement(tokens)
    elif tokens[0] == 'while':
        return parse_while_loop(tokens)
    else:
        return parse_single_expression(tokens)


# if_statement ::= 'if' '(' expression ')' '{' statement_list '}'
def parse_if_statement(tokens):
    tokens.pop(0)
    if_stmt = If('if')
    eat('(', tokens)
    condition = parse_expression(tokens)
    eat(')', tokens)
    eat('{', tokens)
    stmt_list = parse_statement_list(tokens)
    eat('}', tokens)
    if_stmt.children = [condition, stmt_list]
    return if_stmt


# while_loop ::= 'while' '(' expression ')' '{' statement_list '}'
def parse_while_loop(tokens):
    tokens.pop(0)
    while_loop = While('while')
    eat('(', tokens)
    condition = parse_expression(tokens)
    eat(')', tokens)
    eat('{', tokens)
    stmt_list = parse_statement_list(tokens)
    eat('}', tokens)
    while_loop.children = [condition, stmt_list]
    return while_loop


# integer_literal ::= [0-9]
def parse_integer_literal(tokens):
    if not tokens[0].isdigit():
        print("Syntax error")
        print 'int lit', tokens
        exit()
    i = int(tokens[0])
    tokens.pop(0)
    return IntegerLiteral(i)


# identifier ::= [a-zA-Z]
def parse_identifier(tokens):
    ident = tokens.pop(0)
    return Identifier(ident)


# identifier ::= [a-zA-Z]
def parse_identifier_list(tokens):
    id_list = IdentifierList()
    while tokens[0].isalpha():
        id_list.append(tokens.pop(0))
    return id_list


# operator ::= '=' | '+' | '-'
def parse_operator(tokens):
    op = tokens.pop(0)
    return Operator(op)


# function_call ::= identifier '(' argument_list ')'
def parse_function_call(tokens):
    func_call = FunctionCall(tokens[0])
    tokens.pop(0)
    eat('(', tokens)
    args = parse_argument_list(tokens)
    eat(')', tokens)
    func_call.children = [args]
    return func_call


def parse_function_def(tokens):
    """
    ```
    function_definition ::= 'function' identifier '(' identifier_list ')' '{'
                                statement_list
                            '}'
    ```
    """
    tokens.pop(0)
    func_def = FunctionDef(tokens[0])
    tokens.pop(0)
    eat('(', tokens)
    args = parse_argument_list(tokens)
    eat(')', tokens)
    eat('{', tokens)
    body = parse_statement_list(tokens)
    eat('}', tokens)
    func_def.children = [args, body]
    return func_def


def parse_expression(tokens):
    """
    expression ::= integer_literal
                 | binary_expression
                 | identifier
                 | function_call
    """
    expr = parse_single_expression(tokens)
    if expr is None:
        print 'Syntax error'
        print 'parse expr', tokens
        exit()
    return expr


def parse_single_expression(tokens):
    if len(tokens) >= 2 and tokens[1] == '(':
        expr = parse_function_call(tokens)
    elif tokens[0].isalpha():
        expr = parse_identifier(tokens)
    elif tokens[0].isdigit():
        expr = parse_integer_literal(tokens)
    else:
        return None
    if len(tokens) > 1 and tokens[0] in Operators:
        return parse_binary_expression(expr, tokens)
    else:
        return expr


def parse_expression_list(tokens):
    """Parse a list of expressions. Will return a ExpressionList object. The
    production for an expression list is:
    ```
    expression_list ::= expression expression_list | expression | epsilon
    ```"""
    expr_list = ExpressionList()
    while True:
        expr = parse_single_expression(tokens)
        if expr is None:
            break
        expr_list.append(expr)
    return expr_list


def parse_statement_list(tokens):
    """Parse a list of statements. Will return a StatementList object. The
    production for a statement list is:
    ```
    statement_list ::= statement statement_list | statement | epsilon
    ```"""
    stmt_list = StatementList()
    while True:
        stmt = parse_statement(tokens)
        if stmt is None:
            break
        stmt_list.append(stmt)
    return stmt_list


def parse_single_argument(tokens):
    """Parse a single argument. Will return None if the next token is not
    a valid argument.
    FIXME: all arguments list functions should be replaced with expression
    lists.
    """
    if len(tokens) > 1 and tokens[1] == '(':
        return parse_function_call(tokens)
    elif (tokens[0].isalpha() and tokens[0] != 'if' and
          tokens[0] != 'while' and tokens[0] != 'function'):
        return parse_identifier(tokens)
    elif tokens[0].isdigit():
        return parse_integer_literal(tokens)
    else:
        return None


def parse_argument(tokens):
    """Parse a single argument. May raise SystemExit if the next token is not
    a valid argument.
    The production for an argument is:
    ```
    argument ::= identifier | integer_literal | function_call
    ```
    """
    arg = parse_single_argument(tokens)
    if arg is None:
        print 'Syntax error'
        print 'parse_args', tokens
        sys.exit()
    return arg


def parse_argument_list(tokens):
    """Parse a list of arguments. `tokens` is the list of tokens.
    A list of arguments is zero or more arguments. An argument is an identifier
    or an integer literal.
    The production for a list of arguments is:
    ```
    argument_list ::= argument
                    | argument argument_list
                    | epsilon
    ```
    """
    arg_list = ArgumentList()
    while True:
        arg = parse_single_argument(tokens)
        if arg is None:
            break
        arg_list.append(arg)
    return arg_list


def parse_binary_expression(lhs, tokens):
    """Parse a binary expression. `lhs` is an expression representing the left
    hand side of the binary expression. `tokens` is a list of tokens.
    May raise SystemExit.
    The production for binary expressions is:
    ```
    binary_expression ::= integer_literal operator expression
                        | identifier operator expression
                        | function_call operator expression
    ```
    """
    operator = Operator(tokens.pop(0), [lhs])
    rhs = parse_expression(tokens)
    operator.children.append(rhs)
    return operator
