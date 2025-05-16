# Standard library for regular expressions (regex)
import re

# VARIABLE STORE
variables = {}

# List of keywords that are not allowed as variable names (see line 12)
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
    # Case 1: Assigned expression is a literal
    if is_integer_literal(expression):
        variables[var_name] = (int(expression), 'int')
    elif is_float_literal(expression):
        variables[var_name] = (float(expression), 'float')
    
    # Case 2: Assigned expression is a variable
    elif is_valid_variable(expression):
        if expression in variables:
            value, val_type = variables[expression]
            variables[var_name] = (value, val_type)
        else:
            print(f"SNOL> Error! [{expression}] is not defined!")
            
    # Case 3: Invalid assignment (neither literal nor variable)
    else:
        print(f"SNOL> Unknown word[{expression}]")


#----------------------------------------------------------------------------

# Main core function that parses the commands
def parse_command(command_str: str) -> dict:
    command_str = command_str.strip()

## LIST OF IF-ELSE STATEMENTS FOR THE INDIVIDUAL COMMANDS OF SNOL
# Format: if command_str == 'COMMAND':
    if not command_str:
        return {'type': 'error', 'message': 'Unknown command! Does not match any valid command of the language.'}
    
    tokens = command_str.split()
    
    # EXIT!
    if command_str == 'EXIT!':
        return {'type': 'exit'}
    
    if tokens[0] == 'BEG':
        if len(tokens) == 2:
            var = tokens[1]
            if is_valid_variable(var):
                return {'type': 'input', 'name': var} #--> will trigger handle_input()
            elif is_literal(var):
                return {'type': 'error', 'message': f"Invalid target for BEG. Literals are not allowed."}
            else:
                return {'type': 'error', 'message': f"Unknown word [{var}]"}
        return {'type': 'error', 'message': 'Invalid BEG syntax. Usage: BEG var'}
    
    # Handle PRINT x
    if tokens [0] == 'PRINT':
        if len(tokens) == 2:
            return {'type': 'print', 'target': tokens[1]} #--> will trigger handle_print()
        return {'type': 'error', 'message': 'Invalid PRINT syntax. Usage: PRINT var_or_literal'}
    
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
    
    # Unknown Tokens
    for token in tokens:
        if not (is_valid_variable(token) or is_literal(token) or token in '+-*/%()'):
            return {'type': 'error', 'message': f"Unknown word [{token}]"}
        if is_valid_variable(token) and token not in variables:
            return {'type': 'error', 'message': f"Undefined variable [{token}]"}
        
    # All the otherwise, assume it's an arithmetic expression
    return {'type': 'expression', 'expr': command_str}


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
                    ## ROLES TO BE FILLED BY OTHERS
                    handle_input(command['name']) #--> changed by Quennie
                case 'print':
                    handle_print(command['target']) #--> changed by Quennie
                case 'assignment':
                    handle_assignment(command['var'], command['expr']) # --> implemented by Andrei
                case 'expression':
                    # result, _ = evaluate_expression(command['expr']) placeholder for expression evaluation only
                    # Per spec, no output here
                    print(f"Command parsed: {command}")
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
    