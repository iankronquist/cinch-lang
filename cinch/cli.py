import argparse
# import sys

import lexer
import parser
# import compiler


def main():
    argparser = argparse.ArgumentParser(
        description='The cinch language compiler')
    argparser.add_argument('file',
                           help='The file to be compiled or interpreted')
    argparser.add_argument('-c',  help='Produce an object file',
                           action='store_true')
    argparser.add_argument('-S',  help='Produce an assembly file',
                           action='store_true')
    argparser.add_argument('-i', '--interpret',
                           help='Interpret the file. Do not compile it',
                           action='store_true')
    argparser.add_argument('-o', help='The file which should be output to')
    argparser.add_argument('-m', help='The machine to target. May be x86',
                           choices=['x86'], default='x86')
    args = argparser.parse_args()
    with open(args.file, 'r') as f:
        source = f.read()
    tokens = lexer.lex(source)
    ast = parser.parse(tokens)  # noqa - this is a stub
    if args.i:
        # from cinch import interpreter
        # exit_code = interpreter.interpret(ast)
        # sys.exit(exit_code)
        pass
    # assembly = compiler.compile(ast, args.m)
    if args.S:
        # write out assembly
        pass
    elif args.c:
        # write out object file
        pass
    else:
        # actually link the thing
        pass


if __name__ == '__main__':
    main()
