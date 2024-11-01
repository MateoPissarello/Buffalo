from Lexer import TokenType
from Lexer import Detokenizer
import Lexer


class SyntaxAnalyzer:
    def __init__(self):
        # self.grammar = grammar
        self.input_tokens = []
        self.current_token_index = 0

    def parse(self, tokens):
        self.input_tokens = tokens
        return self.parse_statement_list()

    def parse_statement_list(self):
        flag = True
        while flag:
            lookahead = self.lookahead()
            if lookahead is not None:
                self.parse_statement(lookahead)
            else:
                flag = False

    def handle_quote(self):
        self.parse_quote_statement()

    def parse_import_statement(self):
        self.match(TokenType.IMPORT)
        self.match(TokenType.IDENTIFIER)
        opt = self.match(Lexer.SymbolsDict["."], optional=True)
        if opt:
            self.match(TokenType.IDENTIFIER)

    def parse_from_statement(self):
        self.match(TokenType.FROM)
        self.match(TokenType.IDENTIFIER)
        opt = self.match(Lexer.SymbolsDict["."], optional=True)
        if opt:
            self.match(TokenType.IDENTIFIER)
        self.match(TokenType.IMPORT)
        self.match(TokenType.IDENTIFIER)

    def parse_condition(self):
        self.parse_expression()  # Primer operando de la condición
        while True:
            current_token = self.lookahead()
            if (
                current_token
                and isinstance(current_token, Lexer.TokenSymbol)
                and Lexer.is_token_comparing_operator(current_token.value)
            ):  # Comparación
                self.match(current_token.value)
                self.parse_expression()  # Segundo operando de la comparación
            elif (
                current_token
                and isinstance(current_token, Lexer.ReservedWordToken)
                and current_token.value
                in [
                    "and",
                    "or",
                    "not",
                ]
            ):  # Lógicos
                self.match(current_token.value)
                self.parse_expression()  # Nueva expresión para el operador lógico
            else:
                break  # No hay más operadores lógicos o de comparación, termina

    def parse_print_statement(self):
        self.match(TokenType.PRINT)
        self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN)

    def parse_statement(self, lookahead=None, check_indentation=False):
        current_token = lookahead if lookahead else self.lookahead()
        if check_indentation:
            first_token_previous_row = self.lookrowback(current_token.line - 1)
            if (
                current_token.starting_position
                != first_token_previous_row.starting_position
            ):
                self.error(
                    [
                        f"Indentación incorrecta, se esperaba una columna en {first_token_previous_row.starting_position} pero se encontró en {current_token.starting_position}."
                    ]
                )
        # Cambiar de current_token.type a current_token.token_type
        if isinstance(current_token, Lexer.TokenIdentifier):
            if (
                current_token.token_type == TokenType.IDENTIFIER
            ):  # Cambia 'id' a TokenType.IDENTIFIER
                self.parse_assignment_statement()
            else:
                self.error(
                    [TokenType.IDENTIFIER, TokenType.IF]
                )  # Cambia 'id' a TokenType.IDENTIFIER
        elif isinstance(current_token, Lexer.TokenSymbol):

            if current_token.value == TokenType.COLON:
                self.match(TokenType.COLON)
            elif current_token.value == TokenType.QUOTE:
                self.parse_quote_statement()
        elif isinstance(current_token, Lexer.ReservedWordToken):
            if current_token.value == "while":
                self.parse_while_statement()
            elif current_token.value == "print":
                self.parse_print_statement()
            elif (
                current_token.value == "if"
            ):  # Asegúrate de que 'if' sea un token válido
                self.parse_if_statement(if_pos=current_token.starting_position)
            elif current_token.value == "else":
                self.parse_else_statement(else_pos=current_token.starting_position)
            elif current_token.value == "elif":
                self.parse_elif_statement(elif_pos=current_token.starting_position)
            elif current_token.value == "import":
                self.parse_import_statement()
            elif current_token.value == "from":
                self.parse_from_statement()

    def parse_assignment_statement(self):
        self.match(TokenType.IDENTIFIER)  # Cambia 'id' a TokenType.IDENTIFIER
        self.match(TokenType.ASSIGN)  # Cambia '=' a TokenType.ASSIGN
        self.parse_expression()

        """
        if condition:
            
        
        """

    def parse_quote_statement(self):
        self.match(TokenType.QUOTE)
        self.match(TokenType.STRING)
        self.match(TokenType.QUOTE)

    def parse_if_statement(self, if_pos):
        self.match(TokenType.IF)  # Cambia 'if' a TokenType.IF
        self.match(TokenType.LPAREN)  # Cambia '(' a TokenType.LPAREN
        self.parse_condition()
        self.match(TokenType.RPAREN)  # Cambia ')' a TokenType.RPAREN
        self.match(TokenType.COLON)
        self.parse_block(if_pos, method="if")
        # if self.lookahead() is not None and self.lookahead().value == "else":
        #     self.match(TokenType.ELSE)  # Cambia 'else' a TokenType.ELSE
        #     self.parse_statement()

    def parse_elif_statement(self, elif_pos):
        self.match(TokenType.ELIF)
        self.match(TokenType.LPAREN)
        self.parse_condition()
        self.match(TokenType.RPAREN)
        self.match(TokenType.COLON)
        self.parse_block(elif_pos, method="elif")

    def parse_else_statement(self, else_pos):
        self.match(TokenType.ELSE)
        self.match(TokenType.COLON)
        self.parse_block(else_pos, method="else")

    def parse_block(self, cond_pos, method: str):
        # Obtiene la posición de la columna del primer token de la fila anterior

        current_token = self.lookahead()
        if current_token is None:
            self.error(
                [
                    "Indentación incorrecta, se esperaba una identación pero se encontró en EOF."
                ]
            )
        previous_token = self.lookrowback(current_token.line - 1)
        previous_column_position = (
            previous_token.starting_position if previous_token else 0
        )

        # La nueva posición de columna debe ser al menos una unidad mayor
        expected_indent = previous_column_position + 1
        # Verifica la posición de la columna del token actual
        current_column_position = current_token.line

        # Si la columna actual es menor que la esperada, se ha salido del bloque
        if current_column_position < expected_indent:
            self.error(
                [
                    f"Indentación incorrecta, se esperaba una columna en {expected_indent} pero se encontró en {current_column_position}."
                ]
            )

        # Si la columna actual es igual a la esperada, procesamos la declaración
        if current_column_position > expected_indent:
            self.parse_statement()  # Procesa la declaración
            next_token = self.lookahead()
            first_block_index = current_token.starting_position
            if next_token:
                if next_token.starting_position == first_block_index:
                    while next_token:
                        if next_token.starting_position == first_block_index:
                            self.parse_statement(check_indentation=True)
                            self.current_token_index += 1
                            next_token = self.lookahead()

                        elif next_token.starting_position == cond_pos and method in [
                            "if",
                            "elif",
                        ]:
                            if next_token.value in ["else", "elif"]:
                                return self.parse_statement()
                            return
                        elif (
                            next_token.starting_position == cond_pos
                            and method == "else"
                        ):
                            return self.parse_statement()
                        else:
                            self.error(
                                [
                                    f"Indentación incorrecta, se esperaba una columna en {first_block_index} pero se encontró en {next_token.starting_position}."
                                ]
                            )
                else:
                    if next_token.starting_position == cond_pos and method in [
                        "if",
                        "elif",
                    ]:
                        if next_token.value in ["else", "elif"]:
                            return self.parse_statement()
                        elif next_token.starting_position == cond_pos:
                            return
                    elif next_token.starting_position == cond_pos and method == "else":
                        return
                    else:
                        self.error(
                            [
                                f"Indentación incorrecta, se esperaba una columna en {first_block_index} pero se encontró en {next_token.starting_position}."
                            ]
                        )

        else:
            # Si la columna actual es mayor que la esperada, esto es un error de indentación
            self.error(
                [
                    f"Indentación incorrecta, se esperaba una columna en {expected_indent} pero se encontró en {current_column_position}."
                ]
            )

        # Al final del bloque, se puede manejar la dedentación si es necesario

    def parse_while_statement(self):
        self.match(TokenType.WHILE)
        self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN)
        self.parse_statement()

    def parse_expression(self):
        current_token = self.lookahead()
        if current_token:
            if isinstance(current_token, Lexer.TokenIdentifier):
                token_type = current_token.token_type
                if (
                    token_type == TokenType.IDENTIFIER
                ):  # Cambia 'id' a TokenType.IDENTIFIER
                    self.match(
                        TokenType.IDENTIFIER
                    )  # Cambia 'id' a TokenType.IDENTIFIER
                    opt = self.match(Lexer.SymbolsDict["."], optional=True)
                    if opt:
                        self.match(TokenType.IDENTIFIER)
                elif (
                    token_type == TokenType.NUMBER
                ):  # Cambia 'tk_numero' a TokenType.NUMBER
                    self.match(
                        TokenType.NUMBER
                    )  # Cambia 'tk_numero' a TokenType.NUMBER
            elif isinstance(current_token, Lexer.TokenSymbol):
                token_type = current_token.value
                if token_type == TokenType.LPAREN:
                    self.match(TokenType.LPAREN)
                if token_type == TokenType.QUOTE:
                    self.handle_quote()
        else:
            self.error([TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.LPAREN])

    def lookahead(self):
        if self.current_token_index < len(self.input_tokens):
            return self.input_tokens[self.current_token_index]
        return None  # Fin de la entrada

    def lookbehind(self):
        if self.current_token_index > 0:
            return self.input_tokens[self.current_token_index - 1]
        return None

    def lookrowback(self, line_before):
        before_token = None
        for token in self.input_tokens:
            if token.line == line_before:
                before_token = token
                break
        return before_token

    def match(self, expected_token, optional=False):
        next_token = self.lookahead()

        if Lexer.is_token_identifier_cls(next_token):
            token_type = next_token.token_type
        elif Lexer.is_token_symbol_cls(next_token):
            token_type = next_token.value
        elif Lexer.is_token_reserved_word_cls(next_token):
            token_type = next_token.value
        if next_token is not None and token_type == expected_token:
            self.current_token_index += 1
            return True

        # try:
        #     token_type = next_token.token_type
        # except Exception:
        #     token_type = Lexer.obtain_key(next_token)
        # finally:
        #     if next_token is not None and token_type == expected_token:
        #         self.current_token_index += 1
        else:
            if not optional:
                self.error([expected_token])
            return False

    def error(self, expected_tokens):
        current_token = self.lookahead()
        last_tk = self.input_tokens[self.current_token_index - 1]
        last_tk_line = last_tk.line if last_tk else 0
        last_tk_end = 0
        if last_tk:
            if Lexer.is_token_symbol_cls(last_tk):
                last_tk_end = (
                    len(last_tk.symbol) + last_tk.starting_position if last_tk else 0
                )
            elif Lexer.is_token_identifier_cls(last_tk):
                last_tk_end = (
                    len(last_tk.token_type) + last_tk.starting_position
                    if last_tk
                    else 0
                )
            line_number = last_tk_line if last_tk else 0
            position = last_tk_end if last_tk else 0
            lexeme = current_token.value if current_token else "EOF"
            # expected_tokens_str = ", ".join([str(token) for token in expected_tokens])

            representation = Detokenizer(expected_tokens)
            representation.detokenize()
            detokenized_tokens = representation.detokenized
            expected_tokens_str = ", ".join(str(token) for token in detokenized_tokens)
        else:
            expected_tokens_str = ", ".join(str(token) for token in expected_tokens)
        if lexeme != "EOF":
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se encontró: "{lexeme}"; se esperaba: "{expected_tokens_str}".'
            )
        else:
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se esperaba: "{expected_tokens_str}".'
            )
