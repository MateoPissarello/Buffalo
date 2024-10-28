class Grammar:
    def __init__(self):
        self.grammar = {
            'program': [['statement_list']],
            'statement_list': [['statement', 'statement_list'], ['']],
            'statement': [['assignment_statement'], ['if_statement']],
            'assignment_statement': [['identifier', '=', 'expression']],
            'if_statement': [['if', '(', 'expression', ')', 'statement', 'else_statement']],
            'else_statement': [['else', 'statement'], ['']],
            'expression': [['identifier'], ['number']],
            'identifier': [['id']],
            'number': [['tk_numero']],
        }