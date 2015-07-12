from unittest import TestCase
from cinch.lexer import lex


class TestLexer(TestCase):

    def test_lex(self):
        # noqa -- this is formatted like real code
        source = """
            if ( 4 ) {
                avariable = 1 + 1
                anothervariable = a - 314
            }
        """
        # noqa -- this is formatted like real code
        expected_lexing = ['if', '(', '4', ')', '{',     # noqa
            'avariable', '=', '1', '+', '1',             # noqa
            'anothervariable', '=', 'a', '-', '314',     # noqa
        '}']
        result = lex(source)
        self.assertEqual(result, expected_lexing)

        # noqa -- this is formatted like real code
        source = """
            function afunction ( a b c ) {
                avariable = 1 + 1
                anothervariable = a - 314
            }
        """

        # noqa -- this is formatted like real code
        expected_lexing = ['function', 'afunction', '(', 'a', 'b', 'c', ')',
        '{',                                                          # noqa
            'avariable', '=', '1', '+', '1',                          # noqa
            'anothervariable', '=', 'a', '-', '314',                  # noqa
        '}']
        result = lex(source)
        self.assertEqual(result, expected_lexing)
