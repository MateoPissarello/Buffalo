#!/usr/bin/env python3

import argparse
from FileHandler import FileHandler, LineByLineReadStrategy
from Lexer import Lexer
from LL1_Parser import LL1_Parser
from grammar import Grammar

class TokenSymbol:
    def __init__(self, token_type, value, line, starting_position):
        self.token_type = token_type  # Tipo de token
        self.value = value  # Valor del token
        self.line = line  # Línea donde se encuentra el token
        self.starting_position = starting_position  # Posición inicial del token

    def __str__(self):
        return f"<{self.token_type}, {self.value}, {self.line}, {self.starting_position}>"

class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.current_line = 0

    def tokenize(self):
        tokens = []
        # Lógica para generar tokens
        for line in self.lines:
            # Procesar cada línea y agregar tokens
            # Asegúrate de crear objetos TokenSymbol aquí
            token = TokenSymbol(token_type='tk_numero', value='10', line=self.current_line, starting_position=5)
            tokens.append(token)

        return tokens


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

        # Inicializa el analizador LL1 y analiza los tokens
        grammar = Grammar()
        parser = LL1_Parser(grammar)  # Cambié 'tokens' por 'grammar'

        try:
            parse_tree = parser.parse(tokens)  # Aquí pasamos los tokens al método parse
            print("El análisis sintáctico ha finalizado exitosamente.")
            # Imprime el árbol de análisis
            print("Árbol de análisis:")
            print(parse_tree)
        except Exception as e:
            # Aquí se captura el error y se puede imprimir en el formato requerido
            print(str(e))
    else:
        print("No se proporcionó ningún archivo.")


if __name__ == "__main__":
    main()

    