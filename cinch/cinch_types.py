from itertools import chain, imap


Operators = ['+', '-', '=', '<']


# First let's define the tree structure.
class TreeNode (object):

    def __init__(self, value=None, children=[]):
        self.value = value
        self.children = [] if children == [] else children

    def visit(self, callback):
        callback(self)
        for child in self.children:
            child.visit(callback)

    def __str__(self):
        children = ', '.join([str(child) for child in self.children])
        return '[{type}: {value}, {children}]'.format(
            type=self.__class__.__name__,
            value=self.value, children=children)

    def __iter__(self):
        return self.pre_order()

    def pre_order(self):
        yield self
        for child in chain(*imap(lambda x: x.pre_order(), self.children)):
            yield child

    def index(self, item):
        return self.children.index(item)

    def insert(self, index, item):
        return self.children.insert(index, item)

    def pop(self, index=-1):
        return self.children.pop(index)


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


# Should I put a metaclass here or is that too complicated?
class Statement(TreeNode):
    pass


class Expression(TreeNode):
    pass


class Argument(TreeNode):
    pass


class Operator(Expression):
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


class Return(Statement):
    pass


class Identifier(Expression):
    count = -1
    pass


class IdentifierList(Expression, ListMixIn):
    pass


class StatementList(Statement, ListMixIn):
    pass


class ExpressionList(Expression, ListMixIn):
    pass


class ArgumentList(TreeNode, ListMixIn):
    pass
