from LL1_ParserV2 import LL1Parser

parsing_table = {
    "program": {"print": "statement_list", "id": "statement_list"},
    "statement_list": {
        "print": "statement statement_list",
        "id": "statement statement_list",
        "ε": "ε",
    },
    "statement": {"id": "assignment_statement", "print": "print_statement"},
    "assignment_statement": {"id": "identifier = expression"},
    "print_statement": {"print": "print ( expression )"},
    "expression": {"id": "identifier", "tk_cadena": "string", "tk_numero": "number"},
}

# Clase del pa
tokens = [
    ("print", 1, 1),
    ("tk_paren_izq", 1, 6),
    ("tk_cadena", "Hola mundo", 1, 6),
    ("tk_paren_der", 1, 18),
]

parser = LL1Parser(parsing_table, tokens)
parser.parse()
