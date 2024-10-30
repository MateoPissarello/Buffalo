#!/usr/bin/env python3

import argparse
from FileHandler import FileHandler, LineByLineReadStrategy
from Lexer import Lexer
from LL1_Parser import LL1_Parser
from grammar import Grammar


def main():
    parser = argparse.ArgumentParser(
        description="Buffalo: tokenizador de archivos de texto conteniendo código de Python"
    )

    parser.add_argument("-f", "--file", type=str, help="El nombre del archivo")
    parser.add_argument("-o", "--output", type=str, help="El archivo de salida")

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit(0)

    if args.file:
        path = args.file.strip()
        line_by_line_handler = FileHandler(path, LineByLineReadStrategy())
        lines = line_by_line_handler.read()

        lexer = Lexer(lines=lines)
        tokens = lexer.tokenize()

        if args.output:
            path = "output/" + args.output
            with open(path, "w") as f:
                for token in tokens:
                    f.write(f"{token}\n")
        else:
            for token in tokens:
                print(token)

        grammar = Grammar()
        parser = LL1_Parser(grammar)
        try:
            parser.parse(tokens)
            print("El análisis sintáctico ha finalizado exitosamente.")
        except Exception as e:
            print(str(e))
    else:
        print("No se proporcionó ningún archivo.")

    lexer = Lexer(lines=lines)
    tokens = lexer.tokenize()

    # Inicializa el analizador LL1


if __name__ == "__main__":
    main()
