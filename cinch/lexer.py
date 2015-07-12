
# This is the lexer. We could build a state machine which would parse
# each token character by character, but the point of this project is to
# be as simple as possible, so we will literally just call string.split
# source is the source code as a string
# returns an array of string tokens.
def lex(source):
    return map(lambda x: x.strip(), source.split(' '))
