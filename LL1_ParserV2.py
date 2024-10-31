from Lexer import TokenType


# Clase del parser LL(1)
class LL1Parser:
    def __init__(self, parsing_table, tokens):
        self.parsing_table = parsing_table
        self.tokens = tokens
        self.stack = ["program"]  # Inicializa la pila con el símbolo inicial

    def parse(self):
        i = 0
        while self.stack:
            top = self.stack.pop()
            token_type = self.tokens[i][0]  # Extraer solo el tipo de token

            if top in TokenType.__dict__.values():  # Si top es un terminal
                if i < len(self.tokens) and token_type == top:
                    i += 1  # Avanza al siguiente token
                else:
                    print(f"Error: Se esperaba {top} pero se encontró {token_type}")
                    return False
            else:  # Si top es un no terminal
                if token_type in self.parsing_table[top]:
                    production = self.parsing_table[top][token_type]
                    if production != "ε":
                        self.stack.extend(
                            production.split()[::-1]
                        )  # Agrega la producción a la pila en orden inverso
                else:
                    print(
                        f"Error: No hay una regla para {top} con el token {token_type}"
                    )
                    return False
        if i < len(self.tokens):
            print("Error: Tokens sobrantes después de la evaluación")
            return False
        print("Análisis sintáctico exitoso")
        return True
