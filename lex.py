#!/usr/bin/env python

import sys
import string

NAME_START = string.ascii_letters
NAME_BODY = string.ascii_letters + string.digits + "_"
DIGIT = string.digits
WHITESPACE = string.whitespace
MONO_LITERAL = ['{', '}', ';', '(', ')', ',', '.', '+', '-', '*' ]
SLASH = '/'
COMP_LITERAL = ['=','<','>','!']
AND = '&'
BAR = '|'
DOUBLE_QUOTE = "\""


STATE_START = 0
STATE_NAME = 1
STATE_DIGIT = 2
STATE_COMP = 3
STATE_AND = 4
STATE_BAR = 5
STATE_STRING = 6
STATE_STRING_ESCAPE = 7
STATE_COMMENT = 8
STATE_SINGLE_SLASH = 9

class Lexer:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.tokens = []
        self.buffer = ""
        self.state = STATE_START
        self.end_of_line = False
        self.lineno = 1
        # comment_state - [is_single_line, multi_line_stack]
        self.comment_state = [False, []] 

    def flush(self):
        if self.buffer:
            self.tokens.append(str(self.buffer))
            res = self.buffer
            # print(self.buffer, end =' ')
            # sys.stdout.flush()
        self.buffer = ""
        return res
    
    def next_char(self):
        char = self.f.read(1)
        if not char:
            self.end_of_line = True
        elif char == "\n":
            self.lineno += 1
        return char

    def exit(self, code):
        print(f"Exit after line {self.lineno}")
        exit(code)

    def scan(self, f):
        self.f = f
        char = self.next_char()
        while not self.end_of_line:
            if self.state == STATE_START:
                if char in WHITESPACE:
                    char = self.next_char()
                
                elif char in MONO_LITERAL:
                    self.buffer += char
                    yield self.flush()
                    char = self.next_char()
                    
                elif char in NAME_START:
                    self.state = STATE_NAME
                    self.buffer += char
                    char = self.next_char()

                elif char in DIGIT:
                    self.state = STATE_DIGIT
                    self.buffer += char
                    char = self.next_char()

                elif char in COMP_LITERAL:
                    self.state = STATE_COMP
                    self.buffer += char
                    char = self.next_char()
                    
                elif char == BAR:
                    self.state = STATE_BAR
                    self.buffer += char
                    char = self.next_char()
                    if char != "|":
                        print(f"Lex Error: Unable to recognize token \"{self.buffer}\"")
                        self.exit(1)
                    self.buffer += char
                    yield self.flush()
                    char = self.next_char()
                    self.state = STATE_START

                elif char == AND:
                    self.state == STATE_AND
                    self.buffer += char
                    char = self.next_char()
                    if char != "&":
                        print(f"Lex Error: Unable to recognize token \"{self.buffer}\"")
                        self.exit(1)
                    self.buffer += char
                    yield self.flush()
                    char = self.next_char()
                    self.state = STATE_START

                elif char == DOUBLE_QUOTE:
                    self.state = STATE_STRING
                    self.buffer += char
                    char = self.next_char()

                elif char == SLASH:
                    self.state = STATE_SINGLE_SLASH
                    self.buffer += char
                    char = self.next_char()

                else:
                    print(f"Lex Error: character \"{char}\" is not recognised")
                    self.exit(1)

            elif self.state == STATE_NAME:
                if char in NAME_BODY:
                    self.buffer += char
                    char = self.next_char()
                else:
                    yield self.flush()
                    self.state = STATE_START

            elif self.state == STATE_DIGIT:
                if char in DIGIT:
                    self.buffer += char
                    char = self.next_char()
                elif char in NAME_BODY:
                    print(f"Lex Error: Unexpected char \"{char}\" in digit literal")
                    self.exit(1)
                else:
                    yield self.flush()
                    self.state = STATE_START
                    

            # Expects "==", ">=", "<=", "!=", "=", ">", "<", "!"
            elif self.state == STATE_COMP:
                if char == "=":
                    self.buffer += char
                    yield self.flush()
                    char = self.next_char()
                else:
                    yield self.flush()
                self.state = STATE_START

            # # Expects "||"
            # elif self.state == STATE_BAR:
            #     if char != "|":
            #         print(f"Lex Error: Unable to recognize token \"{self.buffer}\"")
            #         self.exit(1)
            #     self.buffer += char
            #     yield self.flush()
            #     char = self.next_char()
            #     self.state = STATE_START

            # # Expects "&&"
            # elif self.state == STATE_AND:
            #     if char != "&":
            #         print(f"Lex Error: Unable to recognize token \"{self.buffer}\"")
            #         self.exit(1)
            #     self.buffer += char
            #     yield self.flush()
            #     char = self.next_char()
            #     self.state = STATE_START

            elif self.state == STATE_STRING:
                if char == "\\":
                    self.buffer += char
                    char = self.next_char()
                    self.state = STATE_STRING_ESCAPE
                elif char == DOUBLE_QUOTE:
                    self.buffer += char
                    yield self.flush()
                    char = self.next_char()
                    self.state = STATE_START
                elif char in ["\n", "\r"]: # TODO: WHat is excluding backslash and double quote???
                    print(f"Lex Error: Unexpected special character in string literal: {char}")
                    self.exit(1)
                else:
                    self.buffer += char
                    char = self.next_char()
            
            elif self.state == STATE_STRING_ESCAPE:
                if char in ["\\", "n", "r", "t", "b", "\'", "\"", "x", "0"]:
                    self.buffer += char
                    char = self.next_char()
                    self.state = STATE_STRING
                else:
                    print(f"Lex Error: Unknown escape character in string \\{char}")
                    self.exit(1)

            elif self.state == STATE_SINGLE_SLASH:
                if char in ["/", "*"]:
                    # Remove the divide symbol
                    self.buffer = self.buffer[:-1] 
                    if char == "/":
                        self.comment_state[0] = True
                    elif char == "*":
                        self.comment_state[1].append("/*")
                    char = self.next_char()
                    self.state = STATE_COMMENT
                # Divide symbol - treat as mono literal
                else:
                    yield self.flush()
                    self.state = STATE_START

            elif self.state == STATE_COMMENT:
                if char == "\n" and self.comment_state[0] and not self.comment_state[1]:
                    self.comment_state[0] = False
                    char = self.next_char()
                    self.state = STATE_START

                elif char == "\n" and self.comment_state[0] and self.comment_state[1]:
                    print("Lex Error: Inappropriate paired /* */ nested within single line comment")
                    self.exit(1)
                
                elif char == "*" and self.comment_state[1]:
                    char = self.next_char()
                    if char == "/":
                        self.comment_state[1].pop()
                        char = self.next_char()
                        if not (self.comment_state[0] or self.comment_state[1]):
                            self.state = STATE_START

                else:
                    if char == "/":
                        char = self.next_char()
                        # if char == "/":
                        #     self.comment_state[0] = True
                        if char == "*":
                            self.comment_state[1].append("/*") # must be matched accordingly
                    
                    char = self.next_char()
                    


        if self.buffer:
            yield self.flush()

        if self.state != STATE_START:
            print(f"Lex Error: Unable to terminate final token \"{self.buffer}\" at state {self.state}")
            self.exit(1)

        # for t in self.tokens:
        #     print(t)




if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python lex.py filename")
        exit(1)

    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    lexer = Lexer()
    gen = lexer.scan(f)
    for token in gen:
        print(token, end=' ')
        sys.stdout.flush()
    print(len(lexer.tokens))
    f.close()