from itertools import chain, imap

# Now this is where things get complicated. The parser takes in an array of
# tokens and returns an abstract syntax tree. Parsing is perhaps the hardest
# problem in the process of compilation, but don't fear! We'll take it slowly
# and keep it simple.

Operators = ['+', '-', '=']

# First let's define the tree structure.
class TreeNode (object):
    def __init__(self, value=None, children=[]):
        self.value = value
        self.children = [] if children == [] else children

    def visit(self, callback):
        callback(self)
        for child in self.children:
            child.visit(callback)

    def __iter__(self):
        return self.pre_order()

    def pre_order(self):
        yield self
        for child in chain(*imap(lambda x: x.pre_order(), self.children)):
            print map(lambda x: (x.value, x), child.children)
            yield child

class ListMixIn(object):
    def __len__(self):
        return len(self.children)

    def __iter__(self):
        for child in self.children:
            yield child

    def __setitem__(self, index, value):
        self.children.insert(index, value)

    def __getitem__(self, index):
        self.children[index]

    def append(self, value):
        self.children.append(value)

class Statement(TreeNode):
    pass

class Expression(TreeNode):
    pass

class Argument(TreeNode):
    pass

class Operator(TreeNode):
    pass

class BinaryExpression(Expression):
    pass

class If(Statement):
    pass

class While(Statement):
    pass

class IntegerLiteral(Expression):
    pass

class FunctionCall(Expression):
    pass

class FunctionDef(Statement):
    pass

class Identifier(Expression):
    pass

class IdentifierList(Expression, ListMixIn):
    pass

class StatementList(Statement, ListMixIn):
    pass

class ExpressionList(Expression, ListMixIn):
    pass

class ArgumentList(TreeNode, ListMixIn):
    pass


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

# function_definition ::= 'function' identifier '(' identifier_list ')' '{' statement_list '}'
def parse_function_def(tokens):
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

# expression ::= integer_literal | binary_expression | identifier | function_call
def parse_expression(tokens):
    expr = parse_single_expression(tokens)
    if expr == None:
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
        expr =  parse_integer_literal(tokens)
    else:
        return None
    if len(tokens) > 1 and tokens[0] in Operators:
        return parse_binary_expression(expr, tokens)
    else:
        return expr

# expression_list ::= expression expression_list | expression
def parse_expression_list(tokens):
    expr_list = ExpressionList()
    while True:
        expr = parse_single_expression(tokens)
        if expr == None:
            break
        expr_list.append(expr)
    return expr_list

# statement_list ::= statement statement_list | statement
def parse_statement_list(tokens):
    stmt_list = StatementList()
    while True:
        stmt = parse_statement(tokens)
        if stmt == None:
            break
        stmt_list.append(stmt)
    return stmt_list

def parse_single_argument(tokens):
    # FIXME function calls should be valid arguments
    if tokens[0].isalpha() and tokens[0] != 'if' and tokens[0] != 'while' and tokens[0] != 'function':
        return parse_identifier(tokens)
    elif tokens[0].isdigit():
        return parse_integer_literal(tokens)
    else:
        return None

# argument ::= identifier | integer_literal
def parse_argument(tokens):
    arg = parse_single_argument(tokens)
    if arg == None:
        print 'Syntax error'
        print 'parse_args', tokens
        exit()
    return arg

# argument_list ::= argument | argument argument_list
def parse_argument_list(tokens):
    arg_list = ArgumentList()
    while True:
        arg = parse_single_argument(tokens)
        if arg == None:
            break
        arg_list.append(arg)
    return arg_list

# binary_expression ::= integer_literal operator expression
#                     | identifier operator expression
#                     | function_call operator expression
def parse_binary_expression(lhs, tokens):
    print tokens
    operator = Operator(tokens.pop(0), [lhs])
    print tokens
    rhs = parse_expression(tokens)
    print rhs.value
    operator.children.append(rhs)
    print map(lambda x: x.value, operator.children)
    return operator
