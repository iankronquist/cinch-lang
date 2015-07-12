import unittest
from mock import Mock, patch
# Normally I don't like to do this but we're going to be testing just about
# everything in this file
from parser import *

class TestTreeNode(unittest.TestCase):
    def test_init(self):
        from parser import *
        node1 = TreeNode()
        self.assertEqual(node1.value, None)
        self.assertEqual(node1.children, [])
        node2 = TreeNode('value', ['child1', 'child2'])
        self.assertEqual(node2.value, 'value')
        self.assertEqual(node2.children, ['child1', 'child2'])

    def test_visit(self):
        c1 = TreeNode('c1')
        c2 = TreeNode('c2')
        root = TreeNode('root', [c1, c2])
        def visitor(node):
            node.value = 'test'
        root.visit(visitor)
        assert_visitor = lambda node: self.assertEqual(node.value, 'test')
        root.visit(assert_visitor)
        self.assertEqual(c1.value, 'test')
        self.assertEqual(c2.value, 'test')
        self.assertEqual(root.value, 'test')

    def test_iter(self):
        c1 = TreeNode('test')
        c2 = TreeNode('test')
        root = TreeNode('test', [c1, c2])
        for node in root:
            print node.value
            self.assertEqual(node.value, 'test')

        c1 = TreeNode('c1')
        c2 = TreeNode('c2')
        root = TreeNode('root', [c1, c2])
        self.assertEqual([root, c1, c2], list(root))

class TestParsing(unittest.TestCase):
    @patch('__builtin__.exit')
    def test_eat(self, mock_exit):
        tokens = ['!', '@', '#']
        expected_token = '!'
        eat(expected_token, tokens)
        self.assertFalse(mock_exit.called)
        self.assertEqual(tokens, ['@', '#'])
        eat(expected_token, tokens)
        self.assertTrue(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_if_statement(self, mock_exit):
        tokens = ['if', '(', '1', ')', '{', '1', '+', '1', '}']
        ast = parse_if_statement(tokens)
        self.assertIsInstance(ast, If)
        self.assertEqual(ast.value, 'if')
        self.assertIsInstance(ast.children[0], Expression)
        self.assertIsInstance(ast.children[1], StatementList)
        self.assertEqual(len(ast.children), 2)
        self.assertFalse(mock_exit.called)
        self.assertEqual(len(tokens), 0)

    @patch('__builtin__.exit')
    def test_parse_while_loop(self, mock_exit):
        tokens = ['while', '(', '1', ')', '{', '1', '+', '1', '}']
        ast = parse_while_loop(tokens)
        self.assertIsInstance(ast, While)
        self.assertEqual(ast.value, 'while')
        self.assertIsInstance(ast.children[0], Expression)
        self.assertIsInstance(ast.children[1], StatementList)
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(len(tokens), 0)
        self.assertFalse(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_integer_literal(self, mock_exit):
        tokens = ['12345']
        ast = parse_integer_literal(tokens)
        self.assertIsInstance(ast, IntegerLiteral)
        self.assertEqual(ast.value, 12345)
        self.assertEqual(ast.children, [])
        self.assertEqual(len(tokens), 0)
        self.assertFalse(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_identifier(self, mock_exit):
        tokens = ['abcd']
        ast = parse_identifier(tokens)
        self.assertIsInstance(ast, Identifier)
        self.assertEqual(ast.value, 'abcd')
        self.assertEqual(ast.children, [])
        self.assertEqual(len(tokens), 0)
        self.assertFalse(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_operator(self, mock_exit):
        tokens = ['+']
        ast = parse_operator(tokens)
        self.assertIsInstance(ast, Operator)
        self.assertEqual(ast.value, '+')
        self.assertEqual(ast.children, [])
        self.assertEqual(len(tokens), 0)

    @patch('__builtin__.exit')
    def test_parse_function_call(self, mock_exit):
        tokens = ['somefunction', '(', 'a', 'b', '1', '2', ')']
        ast = parse_function_call(tokens)
        self.assertIsInstance(ast, FunctionCall)
        self.assertEqual(ast.value, 'somefunction')
        print ast.children
        self.assertIsInstance(ast.children[0], ArgumentList)
        self.assertEqual(len(ast.children), 1)
        self.assertEqual(len(tokens), 0)
        self.assertFalse(mock_exit.called)

        # unbalanced parens
        tokens = ['somefunction', ')', 'a', 'b', '1', '2', ')']
        ast = parse_function_call(tokens)
        self.assertTrue(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_function_def(self, mock_exit):
        tokens = ['function', 'somefunction', '(', 'a', ')', '{',
            'a', '+', '1',
            'somefunction', '(', 'a', ')',
        '}']
        ast = parse_function_def(tokens)
        self.assertIsInstance(ast, FunctionDef)
        self.assertEqual(ast.value, 'somefunction')
        self.assertIsInstance(ast.children[0], ArgumentList)
        self.assertIsInstance(ast.children[1], StatementList)
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(len(tokens), 0)
        self.assertFalse(mock_exit.called)

        # unbalanced parens
        tokens = ['function', 'somefunction', ')', 'a', ')', '{',
            'a', '+', '1',
            'somefunction', '(', 'a', ')',
        '}']
        ast = parse_function_def(tokens)
        self.assertTrue(mock_exit.called)

    @patch('__builtin__.exit')
    def test_parse_binary_expression(self, mock_exit):
        tokens = ['+', '4', '=', 'a', '-', 'b']
        lhs = Identifier('f')
        ast = parse_binary_expression(lhs, tokens)
        self.assertIsInstance(ast, Operator)
        self.assertEqual(ast.value, '+')
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(ast.children[0].value, 'f')
        self.assertIsInstance(ast.children[0], Identifier)
        self.assertEqual(ast.children[1].value, '=')
        self.assertIsInstance(ast.children[1], Operator)

        equals = ast.children[1]
        self.assertEqual(len(equals.children), 2)
        self.assertIsInstance(equals.children[0], IntegerLiteral)
        self.assertEqual(equals.children[0].value, 4)
        self.assertIsInstance(equals.children[1], Operator)
        self.assertEqual(equals.children[1].value, '-')

        minus = equals.children[1]
        self.assertEqual(len(minus.children), 2)
        self.assertIsInstance(minus.children[0], Identifier)
        self.assertIsInstance(minus.children[1], Identifier)
        self.assertEqual(minus.children[0].value, 'a')
        self.assertEqual(minus.children[1].value, 'b')
        self.assertFalse(mock_exit.called)
