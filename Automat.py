#!/usr/bin/env python3
from typing import List, Dict
import sys
from utils import KEYWORDS, SYMBOLS
from tokens import ReservedWordToken, TokenIdentifier, TokenType, SymbolsDict


class AFD:
    """
    Clase que representa un Autómata Finito Determinista (AFD).
    Args:
        estados (list): Lista de estados del AFD.
        alfabeto (list): Lista de símbolos del alfabeto del AFD.
        transiciones (dict): Diccionario que representa las transiciones del AFD.
        estadoInicial (str): Estado inicial del AFD.
        estadosFinales (list): Lista de estados finales del AFD.
    Methods:
        transicion(estado, simbolo): Realiza una transición en el AFD dado un estado y un símbolo.
        checkIsDigit(digit): Verifica si un dígito es un número entero.
        evaluarCadena(cadena): Evalúa una cadena en el AFD y devuelve la clasificación correspondiente.
    """

    def __init__(
        self,
        estados: List[str],
        alfabeto: List[str],
        transiciones: Dict[str, Dict[str, str]],
        estadoInicial: str,
        estadosFinales: List[str],
    ):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estadoInicial = estadoInicial
        self.estadosFinales = estadosFinales

    def transicion(self, estado: str, simbolo: str) -> str:
        """
        Realiza la transición del autómata a partir del estado y el símbolo dados.
        Parámetros:
        - estado: El estado actual del autómata.
        - simbolo: El símbolo de entrada.
        Retorna:
        - El estado resultante después de realizar la transición.
        """
        return self.transiciones[estado][simbolo]

    def checkIsDigit(self, digit: str) -> str:
        """
        Comprueba si el dígito dado es un número decimal.
        Args:
            digit (str): El dígito a comprobar.
        Returns:
            str: Si el dígito es un número decimal, devuelve "d". En caso contrario, devuelve False.
        """
        if digit.isdigit():
            return True

    def checkIsSymbol(self, symbol: str) -> str:
        if symbol in SYMBOLS:
            return True

    def checkisChar(self, c: str) -> str:
        if c.isalpha():
            return True

    def isHash(self, c: str) -> str:
        if c == "#":
            return True

    def handle_token(self, value, line, start):
        if value in KEYWORDS:
            token = ReservedWordToken(
                value=value,
                line=line + 1,
                starting_position=start + 1,
            )
        elif value in SYMBOLS:
            token = TokenIdentifier(
                token_type=SymbolsDict[value],
                value=value,
                line=line + 1,
                starting_position=start + 1,
            )
        else:
            token = TokenIdentifier(
                token_type=TokenType.IDENTIFIER,
                value=value,
                line=line + 1,
                starting_position=start + 1,
            )
        return token

    def evaluarCadena(self, cadena: str) -> str:
        """
        Evalúa una cadena de entrada utilizando el autómata finito determinista (AFD) actual.
        Parámetros:
        - cadena: Cadena de entrada a evaluar.
        Retorna:
        - Si la cadena es válida según el AFD, retorna una cadena que indica la clasificación de la cadena.
        - Si la cadena no es válida según el AFD, retorna "Cadena no válida".
        """
        estadoActual = self.estadoInicial

        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                if self.checkIsDigit(simbolo):
                    simbolo = "d"
                elif self.checkisChar(simbolo):
                    simbolo = "c"
                elif self.isHash(simbolo):
                    simbolo = "#"
                else:
                    return "Cadena no valida"

            try:
                estadoActual = self.transicion(estadoActual, simbolo)
            except KeyError:
                return "Cadena no valida"

        if estadoActual in self.estadosFinales:
            return f"Cadena valida, clasificacion: {estadoActual}"

    def read_lines(self, lines):
        estadoActual = self.estadoInicial
        tokens = []
        position = 0
        value = ""
        for line_index, line in enumerate(lines):
            while len(line) > 0:
                char = line[0]
                line = line[1:]
                if char == '"':
                    value += char
                    char = '"'
                elif char == "'":
                    value += char
                    char = "'"
                if char not in self.alfabeto:
                    if self.checkIsDigit(char):
                        value += char
                        char = "%d"
                    elif self.checkisChar(char):
                        value += char
                        char = "%c"
                    elif self.isHash(char):
                        value += char
                        char = "#"
                    elif char == " ":
                        value += char
                        char = "whitespace"
                    elif char in SYMBOLS:
                        value += char
                        char = "%s"

                try:
                    estadoActual = self.transicion(estadoActual, char)
                except KeyError:
                    line = value[-1] + line
                    value = value[:-1]
                    token = self.handle_token(value, line_index, position)
                    tokens.append(token)
                    print(token)
                    value = ""
                    estadoActual = self.estadoInicial
                    position -= 1
                position += 1
            # for char_index, char in enumerate(line):
            #     if char not in self.alfabeto:

            #         # if char_index == len(line) - 1:
            #         #     token = self.handle_token(line[position:], line_index, position)
            #         #     print(token)
            #         if self.checkIsDigit(char):
            #             char = "%d"
            #         elif self.checkisChar(char):
            #             char = "%c"
            #         elif char == " ":
            #             char = "whitespace"
            #         elif char in SYMBOLS:
            #             char = "%s"
            #     try:
            #         estadoActual = self.transicion(estadoActual, char)
            #     except KeyError:
            #         token = self.handle_token(
            #             line[position:char_index], line_index, position
            #         )
            #         tokens.append(token)
            #         position = char_index - 1
            #         char_index = position
            #         print(token)
            #         estadoActual = self.estadoInicial
            # estado_final = estadoActual
            # if estado_final in self.estadosFinales:
            #     print(
            #         f"Linea {line_index + 1}: Cadena valida, clasificacion: {estado_final}"
            #     )

        # for line in self.lines:
        #     length = len(line)
        #     position = 0
        #     while position < length:
        #         char = line[position]
        #         if char.isalpha() or char == "_":
        #             start = position
        #             while position < length and is_identifier_char(line[position]):
        #                 position += 1
        #             value = line[start:position]
        #             if value in self.keywords:
        #                 self.tokens.append(
        #                     ReservedWordToken(
        #                         value=value,
        #                         line=self.lines.index(line) + 1,
        #                         starting_position=start + 1,
        #                     )
        #                 )

        #             else:
        #                 self.tokens.append(
        #                     TokenIdentifier(
        #                         token_type=TokenType.IDENTIFIER,
        #                         value=line[start:position],
        #                         line=self.lines.index(line) + 1,
        #                         starting_position=start + 1,
        #                     )
        #                 )

        #         elif is_quote(char):
        #             # State: Identifying a string literal
        #             start = position
        #             position += 1
        #             while position < length and not is_quote(line[position]):
        #                 position += 1
        #             if position < length:
        #                 position += 1  # Skip the closing quote
        #                 self.tokens.append(
        #                     TokenIdentifier(
        #                         token_type=TokenType.STRING,
        #                         value=line[start:position],
        #                         line=self.lines.index(line) + 1,
        #                         starting_position=start,
        #                     )
        #                 )
        #             else:
        #                 raise RuntimeError("Unterminated string literal")

        #         elif is_paren(char):
        #             if char == "(":
        #                 self.tokens.append(
        #                     TokenSymbol(
        #                         value=TokenType.LPAREN,
        #                         line=self.lines.index(line) + 1,
        #                         starting_position=position + 1,
        #                     )
        #                 )
        #             else:
        #                 self.tokens.append(
        #                     TokenSymbol(
        #                         value=TokenType.RPAREN,
        #                         line=self.lines.index(line) + 1,
        #                         starting_position=position,
        #                     )
        #                 )
        #             position += 1

        #         elif is_whitespace(char):
        #             start = position
        #             while position < length and is_whitespace(line[position]):
        #                 position += 1
        #             # self.tokens.append(
        #             #     TokenIdentifier(
        #             #         TokenType.WHITESPACE,
        #             #         line[start:position],
        #             #         self.lines.index(line) + 1,
        #             #         start,
        #             #     )
        #             # )
        #         elif is_colon(char):
        #             self.tokens.append(
        #                 TokenSymbol(
        #                     value=TokenType.COLON,
        #                     line=self.lines.index(line) + 1,
        #                     starting_position=position + 1,
        #                 )
        #             )
        #             position += 1

        #         else:
        #             self.tokens.append(
        #                 TokenIdentifier(
        #                     TokenType.UNKNOWN,
        #                     char,
        #                     self.lines.index(line) + 1,
        #                     position,
        #                 )
        #             )
        #             position += 1

        # return self.tokens

    def __str__(self) -> str:
        return f"AFD({self.estados}, {self.alfabeto}, {self.transiciones}, {self.estadoInicial}, {self.estadosFinales})"


hola = 8  # esto es un 8

if __name__ == "__main__":
    estados = ["Inicio", "Num", "Letter", "Comment", "q1", "ID"]
    alfabeto = ["%d", "%c", "#"]
    transiciones = {
        "Inicio": {"%d": "Num", "%c": "Letter", "#": "Comment"},
        "Num": {".": "q1"},
        "q1": {"%d": "Num"},
        "Letter": {
            "%c": "ID",
            "%d": "ID",
        },
        "ID": {"%c": "ID"},
        "Comment": {"%c": "Comment", "%d": "Comment"},
    }
    estadoInicial = "Inicio"
    estadosFinales = ["Num", "ID", "Comment"]

    afd = AFD(estados, alfabeto, transiciones, estadoInicial, estadosFinales)

    if len(sys.argv) != 2:
        print("Uso: python AFD.py <expresion>")
        sys.exit(1)

    cadena = sys.argv[1]
    print(afd.evaluarCadena(cadena))
