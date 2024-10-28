class Grammar:
    def __init__(self):
        self.grammar = {
            'program': [['statement_list']],
            'statement_list': [['statement', 'statement_list'],
                              ['']],
            'statement': [['simple_statement'],
                          ['compound_statement']],
            'simple_statement': [['expression_statement'],
                                ['assignment_statement'],
                                ['print_statement']],
            'compound_statement': [['if_statement'],
                                  ['while_statement'],
                                  ['for_statement'],
                                  ['function_definition']],
            'expression_statement': [['expression']],
            'assignment_statement': [['identifier', '=', 'expression']],
            'print_statement': [['print', '(', 'expression', ')']],
            
            'if_statement': [['if', '(', 'expression', ')', 'statement', 'else_statement']],
            'else_statement': [['else', 'statement'],
                               ['']],
            'while_statement': [['while', '(', 'expression', ')', 'statement']],
            'for_statement': [['for', 'identifier', 'in', 'expression', 'statement']],
            'function_definition': [['def', 'identifier', '(', 'parameter_list', ')', 'statement']],
            
            'parameter_list': [['identifier', 'parameter_list_tail']],
            'parameter_list_tail': [[',', 'identifier', 'parameter_list_tail'],
                                    ['']],
            
            'expression': [['term', 'expression_tail']],
            'expression_tail': [['+', 'term', 'expression_tail'],
                                ['-', 'term', 'expression_tail'],
                                ['']],
            
            'term': [['factor', 'term_tail']],
            'term_tail': [['*', 'factor', 'term_tail'],
                          ['/','factor', 'term_tail'],
                          ['']],
            
            'factor': [['(', 'expression', ')'],
                       ['number'],
                       ['string'],
                       ['identifier']],
            
            'identifier': [['IDENTIFIER']],  # Token para identificadores
            'number': [['NUMBER']],  # Token para números
            'string': [['STRING']],  # Token para cadenas
        }
        self.first_sets = {}  # Para almacenar los conjuntos FIRST
        self.follow_sets = {}  # Para almacenar los conjuntos FOLLOW

    def add_rule(self, non_terminal, production):
        """Agrega una nueva regla a la gramática."""
        if non_terminal in self.grammar:
            self.grammar[non_terminal].append(production)
        else:
            self.grammar[non_terminal] = [production]

    def get_productions(self, non_terminal):
        """Obtiene las producciones de un no terminal."""
        return self.grammar.get(non_terminal, [])

    def compute_first_sets(self):
        """Método para calcular los conjuntos FIRST (implementar según sea necesario)."""
        pass

    def compute_follow_sets(self):
        """Método para calcular los conjuntos FOLLOW (implementar según sea necesario)."""
        pass

    def __str__(self):
        """Representación en cadena de la gramática."""
        return str(self.grammar)
