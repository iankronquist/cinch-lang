import re

# This is the lexer. We could build a state machine which would parse
# each token character by character, but the point of this project is to
# be as simple as possible, so we will literally just split the string on
# spaces, scrub all newlines, and filter out any empty strings


def lex(source):
    """Lex the source code. Split on spaces, strip newlines, and filter out
    empty strings"""
    # Strip comments from source code.
    source = re.sub('#.*$', '', source)
    return filter(lambda s: s != '',
                  re.split('\s', source))
