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
                return {'type': 'input', 'name': var}
            elif is_literal(var):
                return {'type': 'error', 'messsage': f"Unknwon command"}
            else:
                return {'type': 'error', 'message': f"Unknown word [{var}]"}
        return {'type': 'error', 'message': 'Invalid BEG syntax. Usage: BEG var'}
    
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
                    print(f"Command parsed: {command}")
                case 'print':
                    print(f"Command parsed: {command}")
                case 'assignment':
                    print(f"Command parsed: {command}")
                case 'expression':
                    # result, _ = evaluate_expression(command['expr'])
                    # Per spec, no output here
                    print(f"Command parsed: {command}")
                case 'error':
                    print(f"Error: {command['message']}")
                case 'empty':
                    continue
        except NameError as e:
            print(str(e))
        except TypeError as e:
            print(str(e))
        except SyntaxError as e:
            print(str(e))
        except ValueError as e:
            print(str(e))
            
if __name__ == "__main__":
    main()
    
