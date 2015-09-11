from enum import Enum

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
Instruction = Enum('add', 'sub', 'gt', 'lt', 'eq', 'geq', 'leq', 'jmp')

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
    pass

class InstructionBlock(list):
    def __init__(label):
        self.label = label

    def __str__(self):
        return '{}: {}'.format(self.label, super(InstructionBlock, self).__str__())


def compile_to_ir(ast):
    main = InstructionBlock('main')
    for node in ast.children:
        main.extend(compile_statement(node))


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
        comparison = Code3Address(instr_type, left=variable_l, right=variable_r)
        jump = Code3Address(Instruction.jmp, left=comparison.result)
        return [left, right, comparison, jump]
    elif isinstance(ast, IntegerLiteral):
        return [Code3Address(Instruction.jmp, left=ast.value, right=Variable())]
    elif isinstance(ast, Identifier):
        assert ast.count != -1
        return [Code3Address(Instruction.jmp, left=ast.count, right=Variable())]
    else:
        assert False


def compile_while(ast):
    cond = compile_condition(ast.children[0])
    block = compile_statement_list(ast.children[1])

def compile_statement_list(parent, ast, variable_table):
    for statement in ast.children:
        #print 'isl', variable_table
        compile_statement(parent, statement, variable_table)


def compile_statement(parent, ast, variable_table):
    if isinstance(ast, If):
        return compile_if(ast)
    elif isinstance(ast, While):
        return compile_while(parent, ast, variable_table)
    elif isinstance(ast, FunctionCall):
        return compile_func_call(ast, variable_table)
    elif isinstance(ast, FunctionDef):
        return compile_func_def(ast, variable_table)
    elif isinstance(ast, Return):
        return compile_return_statement(parent, ast, variable_table)
    else:
        assert isinstance(ast, Expression)
        #print 'is', variable_table
        return compile_expression(parent, ast, variable_table)

def compile_expression(parent, statement, variable_table):
    if isinstance(statement, Operator):
        #print 'ie', variable_table
        compile_binary_expr(parent, statement, variable_table)
    elif isinstance(statement, Identifier):
        compile_identifier(parent, statement, variable_table)
    elif isinstance(statement, FunctionCall):
        compile_func_call(statement, variable_table)
    elif isinstance(statement, IntegerLiteral):
        pass
    else:
        assert 0


