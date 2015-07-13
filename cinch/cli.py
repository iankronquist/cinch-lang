import argparse
import sys

from cinch import lexer
from cinch import parser
from cinch import compiler

def main():
    parser = argparse.ArgumentParser(description='The cinch language compiler')
    parser.add_argument('file', help='The file to be compiled or interpreted')
    parser.add_argument('-c',  help='Produce an object file',
                        action='store_true')
    parser.add_argument('-S',  help='Produce an assembly file',
                        action='store_true')
    parser.add_argument('-i', '--interpret',
                        help='Interpret the file. Do not compile it',
                        action='store_true')
    parser.add_argument('-o', help='The file which should be output to')
    parser.add_argument('-m', help='The machine to target. May be x86',
                        choices=['x86'], default='x86')
    args = parser.parse_args()
    with open(args.file, 'r') as f:
        source = f.read()
    tokens = lexer.lex(source)
    ast = parser.parse(tokens)
    if args.i:
        from cinch import interpreter
        exit_code = interpreter.interpret(ast)
        sys.exit(exit_code)
    assembly = compiler.compile(ast, args.m)
    if args.S:
        # write out assembly
    elif args.c:
        # write out object file
    else:
        # actually link the thing


if __name__ == '__main__':
    main()
