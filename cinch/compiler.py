from enum import Enum
from cinch_types import (If, While, FunctionCall, FunctionDef, Operator,
                         Identifier, IntegerLiteral, Return, Expression)

# instructions
#
# add left, right, result
# sub left, right, result
# gt  left, right, result
# lt  left, right, result
# eq  left, right, result
# geq left, right, result
# leq left, right, result
# jmp left, right
# label:
Instruction = Enum('Instruction', 'add sub gt lt eq geq leq jmp')


class Code3Address(object):

    def __init__(self, instr_type, left=None, right=None, result=None):
        self.instr_type = instr_type
        self.result = result if result is not None else Variable()
        self.left = left
        self.right = right


class Variable(object):
    count = 0

    def __init__(self):
        Variable.count += 1


def compile(ast):
    compile_to_ir(ast)


class InstructionBlock(list):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return '{}: {}'.format(self.label,
                               super(InstructionBlock, self).__str__())


def compile_to_ir(ast):
    main = InstructionBlock('main')
    for node in ast.children:
        main.extend(compile_statement(node))
    return main


def compile_if(ast):
    first = compile_condition(ast.children[0])
    block = compile_statement_list(ast.children[1])
    return [first, block]


def compile_condition(ast):
    if isinstance(ast, Operator):
        symbol_to_mnemonic = {
            '==': Instruction.eq,
            '>=': Instruction.geq,
            '<=': Instruction.leq,
            '>':  Instruction.gt,
            '<':  Instruction.lt,
        }
        variable_l, left = compile_expression(ast.children[0])
        variable_r, right = compile_expression(ast.children[1])
        instr_type = symbol_to_mnemonic[ast.value]
        comparison = Code3Address(instr_type, left=variable_l,
                                  right=variable_r)
        jump = Code3Address(Instruction.jmp, left=comparison.result)
        return [left, right, comparison, jump]
    elif isinstance(ast, IntegerLiteral):
        return [Code3Address(Instruction.jmp, left=ast.value,
                right=Variable())]
    elif isinstance(ast, Identifier):
        assert ast.count != -1
        return [Code3Address(Instruction.jmp, left=ast.count,
                             right=Variable())]
    else:
        assert False


def compile_while(ast):
    cond = compile_condition(ast.children[0])
    block = compile_statement_list(ast.children[1])
    block.append(cond)
    return [cond, block]


def compile_statement_list(ast):
    statements = []
    for statement in ast.children:
        statements.append(compile_statement(statement))
    return statements


def compile_statement(ast):
    if isinstance(ast, If):
        return compile_if(ast)
    elif isinstance(ast, While):
        return compile_while(ast)
    elif isinstance(ast, FunctionCall):
        return compile_func_call(ast)
    elif isinstance(ast, FunctionDef):
        return compile_func_def(ast)
    elif isinstance(ast, Return):
        return compile_return_statement(ast)
    else:
        assert isinstance(ast, Expression)
        return compile_expression(ast)


def compile_expression(ast):
    if isinstance(ast, Operator):
        return compile_binary_expr(ast)
    elif isinstance(ast, Identifier):
        return compile_identifier(ast)
    elif isinstance(ast, FunctionCall):
        return compile_func_call(ast)
    elif isinstance(ast, IntegerLiteral):
        return []
    else:
        assert 0


def compile_func_call(ast):
    function = ast.value
    return Code3Address(Instruction.jmp, left=function)


def compile_func_def(ast):
    body = compile_statement_list(ast.children[1])
    return InstructionBlock(ast.value).extend(body)


def compile_identifier(ast):
    return []


def compile_return_statement(ast):
    return []


def compile_binary_expr(ast):
    symbol_to_mnemonic = {
        '+': Instruction.add,
        '-': Instruction.sub,
    }
    variable_l, left = compile_expression(ast.children[0])
    variable_r, right = compile_expression(ast.children[1])
    instr_type = symbol_to_mnemonic[ast.value]
    expression = Code3Address(instr_type, left=variable_l,
                              right=variable_r)
    return [left, right, expression]
