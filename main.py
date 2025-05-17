# ----------------------------------------------------------
# SNOL Interpreter - CMSC 124 Final Project
# Developers: Justin Veloso, Quennie Nebria, John Andrei Manalo, Luigi Guillen
# This program interprets a simple number-only language (SNOL)
# ----------------------------------------------------------

import re  # Python Built-in module to handle regular expressions

# Global state: holds all defined variables and their values
variables = {}

# Reserved words that cannot be used as variable names
KEYWORDS = {'PRINT', 'BEG', 'EXIT!'}

# ----------------------------------------------------------
# Helper functions: the functions below check if a string is a valid token type
# ----------------------------------------------------------
def is_valid_variable(name):
    return re.fullmatch(r'[a-zA-Z][a-zA-Z0-9]*', name) and name not in KEYWORDS

def is_integer_literal(token):
    return re.fullmatch(r'-?\d+', token) is not None

def is_float_literal(token):
    return re.fullmatch(r'-?\d+\.\d+', token) is not None

def is_literal(token):
    return is_integer_literal(token) or is_float_literal(token)

def get_type(token):
    if is_integer_literal(token):
        return 'int'
    elif is_float_literal(token):
        return 'float'
    elif token in variables:
        return variables[token][1]
    return None

# ----------------------------------------------------------
# INPUT / OUTPUT HANDLERS - by Quennie Nebria
# ----------------------------------------------------------
# Handle 'BEG var': prompts the user and stores a number in a variable
def handle_input(var_name: str) -> None:
    if not is_valid_variable(var_name):
        print(f"SNOL> Unknown word [{var_name}]")
        return

    print(f"SNOL> Please enter value for [{var_name}]:")
    user_input = input("Input: ").strip()

    if is_float_literal(user_input):
        variables[var_name] = (float(user_input), 'float')
    elif is_integer_literal(user_input):
        variables[var_name] = (int(user_input), 'int')
    else:
        print("SNOL> Error! Invalid number format!")

# Handle 'PRINT x': prints the value of a literal or a variable
def handle_print(target: str) -> None:
    if is_literal(target):
        print(f"SNOL> [literal] = {float(target) if is_float_literal(target) else int(target)}")
    elif is_valid_variable(target):
        if target in variables:
            value, _type = variables[target]
            print(f"SNOL> [{target}] = {value}")
        else:
            print(f"SNOL> Error! [{target}] is not defined!")
    else:
        print(f"SNOL> Unknown word [{target}]")

# ----------------------------------------------------------
# VARIABLE & ASSIGNMENT HANDLING - by John Andrei Manalo
# ----------------------------------------------------------
# Handle 'var = expr', 'var = var', 'var = literal' and stores the result
def handle_assignment(var_name: str, expression: str) -> None:
    try:
        result, result_type = evaluate_expr(expression)
        if result is not None:
            variables[var_name] = (result, result_type)
        else:
            print(f"SNOL> Error! Could not evaluate expression for [{var_name}]")
    except Exception as e:
        print(f"SNOL> Error during assignment: {str(e)}")

# ----------------------------------------------------------
# COMMAND PARSER - by Luigi Guillen
# ----------------------------------------------------------
# Identifies what kind of command was typed
def parse_command(command_str: str) -> dict:
    command_str = command_str.strip().replace('\t', '')

    if not command_str:
        return {'type': 'error', 'message': 'Unknown command! Does not match any valid command of the language.'}
    
    # Reject if the first non-space character is an operator
    if re.match(r'^[+\-*/%]', command_str):
        return {'type': 'error', 'message': 'Unknown command! Does not match any valid command of the language.'}
    
    if command_str == 'EXIT!':
        return {'type': 'exit'}

    # Handle input: BEGvar or BEG var
    if command_str.startswith('BEG'):
        var = command_str[3:].strip()
        if not var:
            return {'type': 'error', 'message': "Missing variable name after BEG"}
        if is_literal(var):
            return {'type': 'error', 'message': "Invalid target for BEG. Literals are not allowed."}
        if is_valid_variable(var):
            return {'type': 'input', 'name': var}
        return {'type': 'error', 'message': f"Unknown word [{var}]"}

    # Handle print: PRINTvar or PRINT var
    if command_str.startswith('PRINT'):
        target = command_str[5:].strip()
        if not target:
            return {'type': 'error', 'message': "Invalid PRINT syntax. Usage: PRINT var_or_literal"}
        return {'type': 'print', 'target': target}

    # Handle assignment: var=expr (no space) or spaced variants
    if '=' in command_str:
        parts = command_str.split('=', 1)
        var_name = parts[0].strip()
        expression = parts[1].strip()

        if not is_valid_variable(var_name):
            return {'type': 'error', 'message': f"Invalid variable name [{var_name}]"}

        if not expression:
            return {'type': 'error', 'message': f"Invalid assignment. No expression provided for [{var_name}]."}

        return {'type': 'assignment', 'var_name': var_name, 'expression': expression}

    # Check if all tokens in the expression are valid
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|-?\d+\.\d+|-?\d+|[()+\-*/%]', command_str)
    reconstructed = ''.join(tokens)
    normalized = command_str.replace(' ', '')

    if reconstructed == normalized:
        return {'type': 'expression', 'expr': command_str}

    # Default case: treat it as an expression
    return {'type': 'expression', 'expr': command_str}

# ----------------------------------------------------------
# Expression Evaluation - by Justin Dominic S. Veloso
# ----------------------------------------------------------
# Evaluates expression strings
def evaluate_expr(expr: str):
    # Loop expression tokens for validation before evaluation
    def check_expression(tokens):
        expression = []
        types = set()

        for token in tokens:
            if is_valid_variable(token):
                if token not in variables:
                    raise NameError(f"Undefined variable [{token}]")
                val, val_type = variables[token]
                expression.append(str(val))
                types.add(val_type)
            elif is_integer_literal(token):
                expression.append(token)
                types.add('int')
            elif is_float_literal(token):
                expression.append(token)
                types.add('float')
            elif token in '+-*/%()':
                expression.append(token)
            else:
                raise SyntaxError(f"Unknown word [{token}]")

        # Rule: Variables should be of the same type - int and float is not allowed
        if 'int' in types and 'float' in types:
            raise TypeError("Operands must be of the same type (int or float only)")

        # Rule: Modulo only works with type int
        if '%' in expression and 'float' in types:
            raise TypeError("Modulo operator is only allowed with integers")

        return expression, list(types)[0]

    # Tokenize expression
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|-?\d+\.\d+|-?\d+|[()+\-*/%]', expr)

    try:
        expression_tokens, final_type = check_expression(tokens)
        eval_str = ' '.join(expression_tokens)
        result = eval(eval_str)

        return (int(result) if final_type == 'int' else float(result)), final_type

    except ZeroDivisionError:
        print("SNOL> Runtime error: Division by zero!")
    except TypeError as e:
        if "Operands must be of the same type" in str(e):
            print("SNOL> Error! Operands must be of the same type in an arithmetic operation!")
        elif "Modulo operator is only allowed with integers" in str(e):
            print("SNOL> Error! Modulo operator is only allowed with integers!")
        else:
            print(f"SNOL> Error! {e}")
    except NameError as e:
        # Extract variable name from the error message
        match = re.search(r'\[(\w+)\]', str(e))
        var_name = match.group(1) if match else 'unknown'
        print(f"SNOL> Error! [{var_name}] is not defined!")
    except SyntaxError as e:
        print(f"SNOL> Syntax error: {e}")
    except Exception as e:
        print(f"SNOL> Error evaluating expression: {e}")

    return None, None

# ----------------------------------------------------------
# Main Interpreter Loop
# ----------------------------------------------------------
def main():
    print("The SNOL environment is now active. Enter your commands:")

    while True:
        command_str = input('Command: ')
        command = parse_command(command_str)

        try:
            match command['type']:
                case 'exit':
                    print("Interpreter is now terminated...")
                    break
                case 'input':
                    handle_input(command['name'])  # Quennie
                case 'print':
                    handle_print(command['target'])  # Quennie
                case 'assignment':
                    handle_assignment(command['var_name'], command['expression'])  # Andrei
                case 'expression':
                    evaluate_expr(command['expr'])  # Justin
                case 'error':
                    print(f"Error: {command['message']}")
        except (NameError, TypeError, SyntaxError, ValueError) as e:
            print(f"SNOL> Runtime error: {str(e)}")
        except Exception as e:
            print(f"SNOL> Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
