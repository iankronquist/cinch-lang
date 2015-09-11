from unittest import TestCase
from mock import patch, call
from cinch.cinch_types import (Identifier, IntegerLiteral, ArgumentList,
                               Operator, FunctionDef, StatementList, If, While,
                               Return, ExpressionList)
from cinch.interpreter import (is_truthy, interpret_func_def,
                               interpret_statement, interpret_while,
                               interpret_return_statement,
                               interpret_statement_list, interpret_identifier)


class TestInterpreter(TestCase):

    def test_is_truthy(self):
        zero = IntegerLiteral(0)
        self.assertEqual(is_truthy(zero, {}), False)

        one = IntegerLiteral(1)
        self.assertEqual(is_truthy(one, {}), True)

        negone = IntegerLiteral(-1)
        self.assertEqual(is_truthy(negone, {}), True)

        scope = {
            'a': 0,
            'b': 1,
            'c': -1,
        }
        a = Identifier('a')
        self.assertEqual(is_truthy(a, scope), False)

        b = Identifier('b')

        self.assertEqual(is_truthy(b, scope), True)

        c = Identifier('c')
        self.assertEqual(is_truthy(c, scope), True)

    def test_def_func(self):
        func = FunctionDef('name')
        args = ArgumentList()
        body = StatementList()
        func.children = [args, body]
        scope = {}
        interpret_func_def(func, scope)
        self.assertEqual(scope['name'], func)

    @patch('cinch.interpreter.interpret_func_def')
    def test_func_def_statement_list_machine(self, interpret_func_def):
        func = FunctionDef('name')
        args = ArgumentList()
        body = StatementList()
        func.children = [args, body]
        scope = {}
        interpret_statement(None, func, scope)
        interpret_func_def.assert_called_with(func, scope)

    @patch('cinch.interpreter.interpret_expression')
    @patch('cinch.interpreter.interpret_statement_list')
    def test_if(self, interpret_statement_list, interpret_expression):
        args = IntegerLiteral(1)
        body = StatementList()
        fi = If(None, children=[args, body])
        interpret_statement(None, fi, {})
        interpret_expression.assert_called_with(fi, args, {})
        interpret_statement_list.assert_called_with(body, body, {})

    @patch('cinch.interpreter.is_truthy')
    @patch('cinch.interpreter.interpret_statement_list')
    def test_while(self, interpret_statement_list, is_truthy):
        cond = IntegerLiteral(1)
        body = StatementList()

        elihw = While(None, children=[cond, body])

        # While loop executes 0 times
        is_truthy.side_effect = [False]
        interpret_while(None, elihw, {})
        is_truthy.assert_called_with(cond, {})
        self.assertFalse(interpret_statement_list.called)

        # While loop executes 1 time
        is_truthy.side_effect = [True, False]
        interpret_while(None, elihw, {})
        is_truthy.assert_called_with(cond, {})
        interpret_statement_list.assert_called_once_with(None, body, {})

        # While loop executes 2 times
        is_truthy.side_effect = [True, True, False]
        interpret_while(None, elihw, {})
        is_truthy.assert_called_with(cond, {})
        interpret_statement_list.assert_has_calls([call(None, body, {})]*2)

        # While loop executes 3 times
        is_truthy.side_effect = [True, True, True, False]
        interpret_while(None, elihw, {})
        is_truthy.assert_called_with(cond, {})
        interpret_statement_list.assert_has_calls([call(None, body, {})]*3)

    @patch('cinch.interpreter.is_truthy')
    @patch('cinch.interpreter.interpret_statement_list')
    def test_while_statement_machine(self, interpret_statement_list,
                                     is_truthy):
        cond = IntegerLiteral(1)
        body = StatementList()

        elihw = While(None, children=[cond, body])

        # While loop executes 3 times
        is_truthy.side_effect = [True, True, True, False]
        interpret_statement(None, elihw, {})
        is_truthy.assert_called_with(cond, {})

    @patch('cinch.interpreter.interpret_expression')
    def test_expression_statement_machine(self, interpret_expression):
        expr = IntegerLiteral(1)
        interpret_statement(None, expr, {})
        interpret_expression.assert_called_with(None, expr, {})

    def test_interpret_return_statement(self):
        expr = IntegerLiteral(1)
        ret = Return(children=[expr])
        sl = StatementList(children=[ret])
        self.assertEqual(sl.children, [ret])
        interpret_return_statement(sl, ret, {})
        self.assertEqual(sl.children, [expr])

    @patch('cinch.interpreter.interpret_return_statement')
    def test_return_statement_machine(self, interpret_return_statement):
        ret = Return(children=[IntegerLiteral(1)])
        interpret_statement(None, ret, {})
        interpret_return_statement.assert_called_with(None, ret, {})

    @patch('cinch.interpreter.interpret_statement')
    def test_interpret_statement_list(self, interpret_statement):
        sl = StatementList(children=[1, 2, 3])
        interpret_statement_list(None, sl, {})
        interpret_statement.assert_has_calls([call(None, 1, {}),
                                              call(None, 2, {}),
                                              call(None, 3, {})])

    def test_interpret_identifier(self):
        ident = Identifier('a')
        parent = StatementList(children=[ident])
        scope = {
            'a': IntegerLiteral(42),
        }
        interpret_identifier(parent, ident, scope)
        self.assertIsInstance(parent.children[0], IntegerLiteral)
        self.assertEqual(parent.children[0].value, 42)
