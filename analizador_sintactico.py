KEYWORDS = {
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
    "object",
    "str",
    "bool",
    "print",
}

SYMBOLS = {
    "(": "tk_par_izq",
    ")": "tk_par_der",
    ":": "tk_dos_puntos",
    "=": "tk_asig",
    ".": "tk_punto",
    "!=": "tk_distinto",
    "+": "tk_suma",
    "-": "tk_resta",
    "*": "tk_multiplicacion",
    "/": "tk_division",
    ",": "tk_coma",
    "^": "tk_potencia",
    "[": "tk_cor_izq",
    "]": "tk_cor_der",
    "{": "tk_llave_izq",
    "}": "tk_llave_der",
    "<": "tk_menor",
    ">": "tk_mayor",
    "<=": "tk_menor_igual",
    ">=": "tk_mayor_igual",
    "==": "tk_igual",
    "%": "tk_modulo",
}


def check_indentation(line, expected_indent, line_num):
    current_indent = len(line) - len(line.lstrip())
    stripped_line = line.strip()

    # Si la línea está vacía, no hay error de indentación
    if not stripped_line:
        return expected_indent

    if stripped_line.startswith(("def ", "if ", "elif ", "for ", "while ")):
        if current_indent != expected_indent:
            return f"Error de indentación en la línea {line_num}: se esperaba {expected_indent} espacios, pero se encontraron {current_indent}."
        expected_indent += 4  # Aumenta la indentación esperada para el bloque
    elif stripped_line.startswith("else:"):
        if current_indent != expected_indent - 4:
            return f"Error de indentación en la línea {line_num}: se esperaba {expected_indent - 4} espacios para 'else', pero se encontraron {current_indent}."
    elif current_indent > expected_indent:
        return f"Error de indentación en la línea {line_num}: la indentación no puede ser mayor que {expected_indent}."
    elif current_indent < expected_indent and (
        stripped_line.startswith("return ")
        or stripped_line.startswith(("break", "continue", "pass"))
    ):
        return f"Error de indentación en la línea {line_num}: se esperaba {expected_indent} espacios para '{stripped_line}', pero se encontraron {current_indent}."

    return expected_indent


def get_token_type(token, line_num, col_num):
    if token in KEYWORDS:
        return f"<{token},{line_num},{col_num}>"
    elif token.isidentifier():
        return f"<id,{token},{line_num},{col_num}>"
    elif token.isdigit():
        return f"<tk_entero,{token},{line_num},{col_num}>"
    elif (token.startswith('"') and token.endswith('"')) or (
        token.startswith("'") and token.endswith("'")
    ):
        return f"<tk_cadena,{token},{line_num},{col_num}>"
    elif token in SYMBOLS:
        return f"<{SYMBOLS[token]},{line_num},{col_num}>"
    return f">>> Error léxico (línea: {line_num}, posición: {col_num})"


def split_line_into_tokens(line, col_num):
    tokens = []
    current_token = ""
    i = 0
    while i < len(line):
        char = line[i]
        if char.isspace():
            if current_token:
                tokens.append((current_token, col_num - len(current_token)))
                current_token = ""
            i += 1
            col_num += 1
            continue
        if i < len(line) - 1 and line[i : i + 2] in SYMBOLS:
            if current_token:
                tokens.append((current_token, col_num - len(current_token)))
                current_token = ""
            tokens.append((line[i : i + 2], col_num))
            i += 2
            col_num += 2
            continue
        if char in SYMBOLS:
            if current_token:
                tokens.append((current_token, col_num - len(current_token)))
                current_token = ""
            tokens.append((char, col_num))
            i += 1
            col_num += 1
            continue
        current_token += char
        i += 1
        col_num += 1
    if current_token:
        tokens.append((current_token, col_num - len(current_token)))
    return tokens


def analyze_line(line, line_num):
    tokens = []
    col_num = 1
    token_list = split_line_into_tokens(line, col_num)
    for token, start_col in token_list:
        tokens.append(get_token_type(token, line_num, start_col))
    return tokens


def check_parentheses_balance(line, line_num):
    open_parens = line.count("(")
    close_parens = line.count(")")
    if open_parens != close_parens:
        return f"Error de sintaxis en la línea {line_num}: paréntesis desbalanceados."
    return None


def check_quotes_balance(line, line_num):
    single_quotes = line.count("'")
    double_quotes = line.count('"')
    if single_quotes % 2 != 0:
        return f"Error de sintaxis en la línea {line_num}: comillas simples desbalanceadas."
    if double_quotes % 2 != 0:
        return (
            f"Error de sintaxis en la línea {line_num}: comillas dobles desbalanceadas."
        )
    return None


def validate_expression(tokens):
    stack = []
    for token in tokens:
        if token == "tk_par_izq":
            stack.append(token)
        elif token == "tk_par_der":
            if not stack or stack.pop() != "tk_par_izq":
                return False
    return not stack


def parse_tokens(tokens, line_num):
    if len(tokens) == 0:
        return None
    if tokens[0].startswith("<def,"):
        if (
            len(tokens) < 4
            or not tokens[1].startswith("<id,")
            or tokens[-1] != "<tk_dos_puntos,"
        ):
            return f"Error sintáctico en la línea {line_num}: definición de función incorrecta."
        if not validate_expression(tokens[2:-1]):
            return f"Error sintáctico en la línea {line_num}: paréntesis no balanceados en definición de función."
    elif tokens[0].startswith("<elif,") or tokens[0].startswith("<if,"):
        if tokens[-1] != "<tk_dos_puntos,":
            return f"Error sintáctico en la línea {line_num}: falta ':' en estructura condicional."
        if not validate_expression(tokens[1:-1]):
            return f"Error sintáctico en la línea {line_num}: paréntesis no balanceados en condición."
    elif tokens[0].startswith("<while,") or tokens[0].startswith("<for,"):
        if tokens[-1] != "<tk_dos_puntos,":
            return f"Error sintáctico en la línea {line_num}: falta ':' en declaración de bucle."
        if not validate_expression(tokens[1:-1]):
            return f"Error sintáctico en la línea {line_num}: paréntesis no balanceados en condición de bucle."
    elif tokens[0].startswith("<id,") and len(tokens) > 1 and tokens[1] == "<tk_asig,":
        if len(tokens) < 3:
            return f"Error sintáctico en la línea {line_num}: asignación incompleta."
        if not validate_expression(tokens[2:]):
            return f"Error sintáctico en la línea {line_num}: paréntesis no balanceados en asignación."
    return None


def lexical_and_syntax_analyzer(input_file):
    errors = []
    expected_indent = 0  # Nivel de indentación esperado

    with open(input_file, "r") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        line = line.rstrip()  # Elimina espacios en blanco al final

        # Determinar la indentación actual
        current_indent = len(line) - len(line.lstrip())

        # Verifica la indentación
        indent_error = check_indentation(line, expected_indent, line_number)
        if isinstance(indent_error, str):
            errors.append(indent_error)
            continue
        expected_indent = indent_error

        # Verificación de paréntesis y comillas
        paren_error = check_parentheses_balance(line, line_number)
        if paren_error:
            errors.append(paren_error)

        quote_error = check_quotes_balance(line, line_number)
        if quote_error:
            errors.append(quote_error)

        # Análisis de tokens
        tokens = analyze_line(line, line_number)
        syntax_error = parse_tokens(tokens, line_number)
        if syntax_error:
            errors.append(syntax_error)

    if errors:
        for error in errors:
            print(error)
    else:
        print("No se encontraron errores en el análisis léxico y sintáctico.")


# Llama a la función con el nombre de tu archivo de entrada
lexical_and_syntax_analyzer("ejemplo3.py")
