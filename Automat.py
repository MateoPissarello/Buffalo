#!/usr/bin/env python3
from typing import List, Dict
import sys


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

    def checkisChar(self, c: str) -> str:
        if c.isalpha():
            return True

    def isHash(self, c: str) -> str:
        if c == "#":
            return True

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

    def __str__(self) -> str:
        return f"AFD({self.estados}, {self.alfabeto}, {self.transiciones}, {self.estadoInicial}, {self.estadosFinales})"


hola = 8  # esto es un 8

if __name__ == "__main__":
    estados = ["Inicio", "Num", "Letter", "Comment", "q1", "ID"]
    alfabeto = ["d", "c", "#"]
    transiciones = {
        "Inicio": {"d": "Num", "c": "Letter", "#": "Comment"},
        "Num": {".": "q1"},
        "q1": {"d": "Num"},
        "Letter": {
            "c": "ID",
            "d": "ID",
        },
        "ID": {"c": "ID"},
        "Comment": {"c": "Comment", "d": "Comment"},
    }
    estadoInicial = "Inicio"
    estadosFinales = ["Num", "Id", "Comment"]

    afd = AFD(estados, alfabeto, transiciones, estadoInicial, estadosFinales)

    if len(sys.argv) != 2:
        print("Uso: python AFD.py <expresion>")
        sys.exit(1)

    cadena = sys.argv[1]
    print(afd.evaluarCadena(cadena))
