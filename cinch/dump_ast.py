#!/usr/bin/python2
import sys
from lexer import lex
from parser import parse


USAGE = """{name} file
    Parses and prints the ast to stdout."""


def main():
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        source = f.read()
    tokens = lex(source)
    ast = parse(tokens)
    print(ast)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print USAGE.format(name=sys.argv[0])
    else:
        main()
