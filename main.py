# Standard library for regular expressions (regex)
import re

# Class to define a token
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
NUM_REGEX = r'\d+\.\d+'

scanner = re.compile(NUM_REGEX)

result = scanner.match('123.456')

# The interpreter/REPL
def repl():
    print("Test REPL. Type 'exit' to quit.")
    while True:
        user_input = input (">>> ")
        if user_input.lower() == 'exit':
            break
        match = scanner.match(user_input)
        if match:
            print(f"Matched: {match.group()}")
        else:
            print("No match found.")
            
if __name__ == "__main__":
    repl()

