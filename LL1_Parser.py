from Lexer import TokenType
from Lexer import Detokenizer


class LL1_Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.input_tokens = []
        self.current_token_index = 0

    def parse(self, tokens):
        self.input_tokens = tokens
        self.current_token_index = 0
        return self.parse_program()

    def parse_program(self):
        self.parse_statement_list()

    def parse_statement_list(self):
        while self.lookahead() is not None:
            self.parse_statement()

    def parse_statement(self):
        current_token = self.lookahead()
        # Cambiar de current_token.type a current_token.token_type
        if (
            current_token.token_type == TokenType.IDENTIFIER
        ):  # Cambia 'id' a TokenType.IDENTIFIER
            self.parse_assignment_statement()

        elif: (
            current_token.token_type == TokenType.
        )
        elif (
            current_token.token_type == TokenType.IF
        ):  # Asegúrate de que 'if' sea un token válido
            self.parse_if_statement()
        else:
            self.error(
                [TokenType.IDENTIFIER, TokenType.IF]
            )  # Cambia 'id' a TokenType.IDENTIFIER

    def parse_assignment_statement(self):
        self.match(TokenType.IDENTIFIER)  # Cambia 'id' a TokenType.IDENTIFIER
        self.match(TokenType.ASSIGN)  # Cambia '=' a TokenType.ASSIGN
        self.parse_expression()

    def parse_if_statement(self):
        self.match(TokenType.IF)  # Cambia 'if' a TokenType.IF
        self.match(TokenType.LPAREN)  # Cambia '(' a TokenType.LPAREN
        self.parse_expression()
        self.match(TokenType.RPAREN)  # Cambia ')' a TokenType.RPAREN
        self.parse_statement()
        if self.lookahead() is not None and self.lookahead().value == "else":
            self.match(TokenType.ELSE)  # Cambia 'else' a TokenType.ELSE
            self.parse_statement()

    def parse_expression(self):
        current_token = self.lookahead()
        if (
            current_token.token_type == TokenType.IDENTIFIER
        ):  # Cambia 'id' a TokenType.IDENTIFIER
            self.match(TokenType.IDENTIFIER)  # Cambia 'id' a TokenType.IDENTIFIER
        elif (
            current_token.token_type == TokenType.NUMBER
        ):  # Cambia 'tk_numero' a TokenType.NUMBER
            self.match(TokenType.NUMBER)  # Cambia 'tk_numero' a TokenType.NUMBER
        else:
            self.error(
                [TokenType.IDENTIFIER, TokenType.NUMBER]
            )  # Cambia 'id' a TokenType.IDENTIFIER

    def lookahead(self):
        if self.current_token_index < len(self.input_tokens):
            return self.input_tokens[self.current_token_index]
        return None  # Fin de la entrada

    def match(self, expected_token):
        if (
            self.lookahead() is not None
            and self.lookahead().token_type == expected_token
        ):  # Cambia .value a .token_type
            self.current_token_index += 1
        else:
            self.error([expected_token])

    def error(self, expected_tokens):
        current_token = self.lookahead()
        last_tk = self.input_tokens[self.current_token_index - 1]
        last_tk_line = last_tk.line if last_tk else 0
        last_tk_end = len(last_tk.value) + last_tk.starting_position if last_tk else 0
        line_number = last_tk_line if last_tk else 0
        position = last_tk_end if last_tk else 0
        lexeme = current_token.value if current_token else "EOF"
        # expected_tokens_str = ", ".join([str(token) for token in expected_tokens])
        expected_tokens = [TokenType.get_token_name(token) for token in expected_tokens]
        representation = Detokenizer(expected_tokens).detokenize()
        expected_tokens_str = ", ".join(str(token) for token in representation)
        if lexeme != "EOF":
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se encontró: "{lexeme}"; se esperaba: "{expected_tokens_str}".'
            )
        else:
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se esperaba: "{expected_tokens_str}".'
            )
