# Standard library for regular expressions (regex)
import re

# VARIABLE STORE
variables = {}

# List of keywords that are not allowed as variable names
KEYWORDS = {'PRINT', 'BEG', 'EXIT!'}

# Functions to check if a variable, integer-literal, float-literal, or literal is valid
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

#----------------------------------------------------------------------------
# Input/Output Handlers- Quennie Nebria

# Handles BEG var: Reads value from user and stores in variable store
def handle_input(var_name: str) -> None:
    # Validate variable name
    if not is_valid_variable(var_name):
        print(f"SNOL> Unknown word [{var_name}]")
        return

    # Prompt the user
    print(f"SNOL> Please enter value for [{var_name}]:")
    user_input = input("Input: ").strip()

    # Check if input is float or int and store appropriately
    if is_float_literal(user_input):
        value = float(user_input)
        variables[var_name] = (value, 'float')  # Store float
    elif is_integer_literal(user_input):
        value = int(user_input)
        variables[var_name] = (value, 'int')    # Store int
    else:
        # Invalid input format
        print("SNOL> Error! Invalid number format!")

# Handles PRINT x: Prints value of variable or literal
def handle_print(target: str) -> None:
    # If it's a literal, print directly
    if is_literal(target):
        if is_integer_literal(target):
            print(f"SNOL> [literal] = {int(target)}")
        else:
            print(f"SNOL> [literal] = {float(target)}")
    
    # If it's a valid variable, print stored value
    elif is_valid_variable(target):
        if target in variables:
            value, _type = variables[target]
            print(f"SNOL> [{target}] = {value}")
        else:
            print(f"SNOL> Error! [{target}] is not defined!")
    
    # Unknown target
    else:
        print(f"SNOL> Unknown word [{target}]")
        
#----------------------------------------------------------------------------
# VARIABLE & ASSIGNMENT STORAGE HANDLING - John Andrei Manalo

# A function that retrieves the value and type of a variable from the variable store
def get_variable_value(var_name: str, variables: dict):
    if var_name in variables:
        return variables[var_name]
    return None, None

# A function that handles assignment statements which supports assignment from literals or existing variables
def handle_assignment(var_name: str, expression: str) -> None:
    try:
        # Evaluate the right-hand side expression
        result, result_type = evaluate_expr(expression)
        
        if result is not None:
            variables[var_name] = (result, result_type)
        else:
            print(f"SNOL> Error! Could not evaluate expression for [{var_name}]")
    except Exception as e:
        print(f"SNOL> Error during assignment: {str(e)}")


#----------------------------------------------------------------------------
# Main core function that parses the commands
def parse_command(command_str: str) -> dict:
    command_str = command_str.strip()

## LIST OF IF-ELSE STATEMENTS FOR THE INDIVIDUAL COMMANDS OF SNOL
    if not command_str:
        return {'type': 'error', 'message': 'Unknown command! Does not match any valid command of the language.'}
    
    tokens = command_str.split()
    
    if command_str == 'EXIT!':
        return {'type': 'exit'}
    
    if command_str.startswith('BEG'):
        var = command_str[3:].strip()
        if is_valid_variable(var):
            return {'type': 'input', 'name': var}
        elif is_literal(var):
            return {'type': 'error', 'message': "Invalid target for BEG. Literals are not allowed."}
        return {'type': 'error', 'message': f"Unknown word [{var}]"}

    if command_str.startswith('PRINT'):
        target = command_str[5:].strip()
        if target:
            return {'type': 'print', 'target': target}
        return {'type': 'error', 'message': "Invalid PRINT syntax. Usage: PRINT var_or_literal"}

    # Handle assignment statement
    if '=' in command_str:
        parts = command_str.split('=', 1)
        var_name = parts[0].strip()
        expression = parts[1].strip()
        
        if not is_valid_variable(var_name):
            return {'type': 'error', 'message': f"Invalid variable name [{var_name}]"}
        if expression == '':
            return {'type': 'error', 'message': f"Invalid assignment. No expression provided for [{var_name}]."}
        
        return {'type': 'assignment', 'var_name': var_name, 'expression': expression}
       
    if re.fullmatch(r'[-+*/()%.\d\s]+', command_str):
        return {'type': 'expression', 'expr': command_str}

    # All the otherwise, assume it's an arithmetic expression
    return {'type': 'expression', 'expr': command_str}

# EVALUATING EXPRESSIONS - Justin Dominic S. Veloso

def evaluate_expr(expr: str):
    # Replace all variables with their values and check type consistency
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

        # Rule: All operands must be of the same type
        if 'int' in types and 'float' in types:
            raise TypeError("Operands must be of the same type (int or float only)")

        # Rule: Modulo is only valid with integers
        if '%' in expression and ('float' in types):
            raise TypeError("Modulo operator is only allowed with integers")

        return expression, list(types)[0]

    # Tokenize expression
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|-?\d+\.\d+|-?\d+|[()+\-*/%]', expr)

    try:
        expression_tokens, final_type = check_expression(tokens)
        eval_str = ' '.join(expression_tokens)
        result = eval(eval_str)

        # Coerce to correct type
        if final_type == 'int':
            result = int(result)
        else:
            result = float(result)

        return result, final_type

    except ZeroDivisionError:
        print("SNOL> Runtime error: Division by zero!")
    except TypeError as e:
        print(f"SNOL> Type error: {e}")
    except NameError as e:
        print(f"SNOL> Name error: {e}")
    except SyntaxError as e:
        print(f"SNOL> Syntax error: {e}")
    except Exception as e:
        print(f"SNOL> Error evaluating expression: {e}")

    return None, None

def main():
    print("The SNOL environment is now active, you may proceed with giving your commands.")
    
    # Eternal while loop to act as a REPL/Interpreter until the user executes "EXIT!"
    while True:
        command_str = input('Command: ')
        command = parse_command(command_str)
        
        try:
            match command['type']:
                case 'exit':
                    print("Interpreter is now terminated...")
                    break
                case 'input':
                    handle_input(command['name']) #--> changed by Quennie
                case 'print':
                    handle_print(command['target']) #--> changed by Quennie
                case 'assignment':
                    handle_assignment(command['var_name'], command['expression']) # --> implemented by Andrei
                case 'expression':
                    result, result_type = evaluate_expr(command['expr']) # --> done by Justin
                    if result is not None:
                        print(f"SNOL> [result] = {result}")
                case 'error':
                    print(f"Error: {command['message']}")
                case 'empty':
                    continue
        except (NameError, TypeError, SyntaxError, ValueError) as e:
            print(f"SNOL> Runtime error: {str(e)}")
        except Exception as e:
            print(f"SNOL> Unexpected error: {str(e)}")
            
if __name__ == "__main__":
    main()
