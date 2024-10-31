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

    def parse_condition(self):
        self.parse_expression()  # Primer operando de la condición
        while True:
            current_token = self.lookahead()
            if current_token and Lexer.is_token_operator_cls(
                current_token
            ):  # Comparación
                self.match(current_token.value)
                self.parse_expression()  # Segundo operando de la comparación
            elif current_token and current_token.value in [
                TokenType.AND,
                TokenType.OR,
            ]:  # Lógicos
                self.match(current_token.value)
                self.parse_expression()  # Nueva expresión para el operador lógico
            else:
                break  # No hay más operadores lógicos o de comparación, termina

    def parse_statement(self, lookahead=None):
        current_token = lookahead if lookahead else self.lookahead()
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
            if current_token.value == TokenType.QUOTE:
                self.parse_quote_statement()
        elif isinstance(current_token, Lexer.ReservedWordToken):
            if current_token.value == "while":
                self.parse_while_statement()
            elif (
                current_token.value == "if"
            ):  # Asegúrate de que 'if' sea un token válido
                self.parse_if_statement()

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

    def parse_if_statement(self):
        self.match(TokenType.IF)  # Cambia 'if' a TokenType.IF
        self.match(TokenType.LPAREN)  # Cambia '(' a TokenType.LPAREN
        self.parse_condition()
        self.match(TokenType.RPAREN)  # Cambia ')' a TokenType.RPAREN
        self.parse_statement()
        if self.lookahead() is not None and self.lookahead().value == "else":
            self.match(TokenType.ELSE)  # Cambia 'else' a TokenType.ELSE
            self.parse_statement()

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

    def match(self, expected_token):
        next_token = self.lookahead()

        if Lexer.is_token_identifier_cls(next_token):
            token_type = next_token.token_type
        elif Lexer.is_token_symbol_cls(next_token):
            token_type = next_token.value
        elif Lexer.is_token_reserved_word_cls(next_token):
            token_type = next_token.value
        if next_token is not None and token_type == expected_token:
            self.current_token_index += 1
        # try:
        #     token_type = next_token.token_type
        # except Exception:
        #     token_type = Lexer.obtain_key(next_token)
        # finally:
        #     if next_token is not None and token_type == expected_token:
        #         self.current_token_index += 1
        else:
            self.error([expected_token])

    def error(self, expected_tokens):
        current_token = self.lookahead()
        last_tk = self.input_tokens[self.current_token_index - 1]
        last_tk_line = last_tk.line if last_tk else 0
        last_tk_end = 0
        if Lexer.is_token_symbol_cls(last_tk):
            last_tk_end = (
                len(last_tk.symbol) + last_tk.starting_position if last_tk else 0
            )
        elif Lexer.is_token_identifier_cls(last_tk):
            last_tk_end = (
                len(last_tk.token_type) + last_tk.starting_position if last_tk else 0
            )
        line_number = last_tk_line if last_tk else 0
        position = last_tk_end if last_tk else 0
        lexeme = current_token.value if current_token else "EOF"
        # expected_tokens_str = ", ".join([str(token) for token in expected_tokens])

        representation = Detokenizer(expected_tokens)
        representation.detokenize()
        detokenized_tokens = representation.detokenized
        expected_tokens_str = ", ".join(str(token) for token in detokenized_tokens)
        if lexeme != "EOF":
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se encontró: "{lexeme}"; se esperaba: "{expected_tokens_str}".'
            )
        else:
            raise Exception(
                f'<{line_number},{position}> Error sintáctico: se esperaba: "{expected_tokens_str}".'
            )
