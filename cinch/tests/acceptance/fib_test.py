from cinch.lexer import lex
from cinch.parser import parse
from cinch.interpreter import interpret_statement_list
from os import path
from unittest import TestCase


class TestFibonacciNumbersAlgorithm(TestCase):

    base_path = './examples/'

    def interpret_helper(self, file_name):
        file_path = path.join(self.base_path, file_name)
        with open(file_path, 'r') as f:
            source = f.read()
        tokens = lex(source)
        ast = parse(tokens)
        scope = {}
        interpret_statement_list(None, ast, scope)
        return ast, scope

    def test_recursive_fib(self):
        ast, scope = self.interpret_helper('fib.cinch')
        self.assertEqual(sorted(scope.keys()), sorted(['result', 'fib']))
        self.assertEqual(scope['result'].value, 13)

    def test_iterative_fib(self):
        ast, scope = self.interpret_helper('fib_iterative.cinch')
        self.assertEqual(sorted(scope.keys()), sorted(['result', 'fib']))
        self.assertEqual(scope['result'].value, 13)
