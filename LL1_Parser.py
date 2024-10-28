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
        node = {'type': 'program', 'statements': []}
        while self.lookahead() != 'ε':
            statement_node = self.parse_statement()
            node['statements'].append(statement_node)
        return node  

    def parse_statement(self):
        current_token = self.lookahead()
        if current_token == 'ε':  # Manejo del caso de fin de entrada
            return None

        if current_token.token_type == 'if':
            return self.parse_if_statement()
        elif current_token.token_type == 'id':
            return self.parse_assignment()
        else:
            self.error(["if", "id"])

    def parse_if_statement(self):
        self.match('if')
        self.match('(')
        self.parse_expression()
        self.match(')')
        self.match(':')
        self.parse_statement()
        
        if self.lookahead().token_type == 'else':
            self.match('else')
            self.match(':')
            self.parse_statement()

    def parse_assignment(self):
        self.match('id')
        self.match('=')
        self.match('tk_numero')
        return {'type': 'assignment'}

    def parse_expression(self):
        pass

    def lookahead(self):
        if self.current_token_index < len(self.input_tokens):
            return self.input_tokens[self.current_token_index]
        return 'ε'  

    def match(self, token_type):
        if self.lookahead() != 'ε' and self.lookahead().token_type == token_type:
            self.current_token_index += 1
        else:
            self.error([token_type])

    def error(self, expected_tokens):
        current_token = self.lookahead()
        line_number = current_token.line
        position = current_token.starting_position
        lexeme = current_token.value
        expected_tokens_str = ", ".join(expected_tokens)
        raise Exception(f"<{line_number},{position}> Error sintactico: se encontro: \"{lexeme}\"; se esperaba: \"{expected_tokens_str}\".")
