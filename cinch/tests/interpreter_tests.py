from unittest import TestCase
from cinch.cinch_types import (Identifier, IntegerLiteral, ArgumentList,
                               Operator)
from cinch.interpreter import is_truthy, insert_in_tree, get_value


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

    def test_insert_in_tree(self):
        args = ArgumentList()
        arg0 = Identifier('a')
        arg1 = Operator('+')
        arg2 = IntegerLiteral(1)
        left = IntegerLiteral(1)
        right = IntegerLiteral(1)
        arg1.children = [left, right]
        args.children = [arg0, arg1, arg2]

        result = IntegerLiteral(2)
        insert_in_tree(args, arg1, result)
        self.assertEqual([arg0, result, arg2], args.children)

    def test_get_value(self):
        one = IntegerLiteral(1)
        a = Identifier('a')
        scope = {
            'a': 2,
        }
        self.assertEqual(get_value(a, scope), 2)
        self.assertEqual(get_value(one, scope), 1)
