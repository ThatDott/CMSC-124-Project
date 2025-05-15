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

def determine_type(value):
    return 'float' if isinstance(value, float) else 'int'

# Command parsing function
def parse_command(command_str: str) -> dict:
    command_str = command_str.strip()

## LIST OF IF-ELSE STATEMENTS FOR THE INDIVIDUAL COMMANDS OF SNOL
    if not command_str:
        return {'type': 'empty'}
    
    # EXIT!
    if command_str == 'EXIT!':
        return {'type': 'exit'}
    
    if command_str.startswith('BEG'):
        parts = command_str.split()
        if len(parts) == 2 and is_valid_variable(parts[1]):
            return {'type': 'input', 'name': parts[1]}
        return {'type': 'error', 'message': 'Invalid BEG syntax. Usage: BEG var'}
    
    # If it looks like a variable, literal, or operation
    return {'type': 'expression', 'expr': command_str}

def main():
    print("The SNOL environment is now active, you may proceed with giving your commands.")
    
    # Eternal while loop to act as a REPL/Interpreter until the user executes "EXIT!"
    while True:
        try:
            command_str = input('Command: ')
        except (EOFError, KeyboardInterrupt):
            print("\nUnknown command!")
            
        command = parse_command(command_str)
        
        match command['type']:
            case 'exit':
                print("Interpreter is now terminated...")
                break
            case 'input':
                print(f"Command parsed: {command}")
            case 'print':
                print(f"Command parsed: {command}")
            case 'assignment':
                print(f"Command parsed: {command}")
            case 'expression':
                print(f"Command parsed: {command}")
            case 'error':
                print(f"Error: {command['message']}")
            case 'empty':
                continue
            case _:
                print("Unknown command!")
            
if __name__ == "__main__":
    main()
    
