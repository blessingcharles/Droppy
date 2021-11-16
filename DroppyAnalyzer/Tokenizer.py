from .types.generals import *
from .types.keywords import *
from .types.operators import *
from . import Token

class Tokenizer:

    def __init__(self ,file_name : str , text : str):

        self.text : str = text
        self.text_len : int = len(text)
        self.file_name : str = file_name
        self.curr_char = self.text[0]
        self.pos : int = 0
        self.col : int = 0 
        self.lin_no :int = 1
       
    def move_forward(self):
        #move the pos to next char
        self.pos += 1
        self.col += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

        while self.curr_char == "\n":
            self.col = 0
            self.lin_no += 1
            self.pos += 1
            self.curr_char = self.text[self.pos]

    def build_operators(self):

        op : str = ""
        start_pos = self.pos

        while self.curr_char != None and self.curr_char in OPERATORS:
            op += self.curr_char
            self.move_forward()
        
        return Token(OPERATOR_TOKEN , op , self.lin_no , start_pos)

    def build_characters(self , prev_word : str = "" , nested_func : bool = False):

        word : str = prev_word 
        start_pos = self.pos

        while self.curr_char != None and self.curr_char in IDENTIFIERS_SET:
                word += self.curr_char
                self.move_forward()
        
        if word in MODULES or nested_func == True:
                #checking if a modular function call like console.log , document.innerHtml
            if self.curr_char == ".":
                word += self.curr_char
                self.move_forward()
                return self.build_characters(word , True)
            else :
                return Token(MODULES_TOKEN , word , self.lin_no , start_pos)

        elif word in KEYWORDS:
            return Token(KEYWORDS_TOKEN , word , self.lin_no , start_pos)
        else :
            return Token(IDENTIFIER_TOKEN , word , self.lin_no , start_pos)

    def build_numbers(self):

        num = ""
        start_pos = self.pos
        dot_count = 0

        while self.curr_char != None and self.curr_char in DIGITS_TOKEN + ".":
        
            if self.curr_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num += self.curr_char
            self.move_forward()

        if dot_count == 0:
            return Token(INT_TOKEN, int(num),self.lin_no , start_pos)
        else:
            return Token(FLOAT_TOKEN, float(num),self.lin_no ,start_pos)

    def parse_comments(self , starter : str):

        comment = ""
        start_pos = self.pos
        start_line_no = self.lin_no

        if starter == "//":
            # single line comment
            while  self.curr_char != None:
                comment += self.curr_char
                if self.text[self.pos+1] == "\n" : 
                    break
                self.move_forward()

        else :
            # multiline comment
            c = ""
            while self.curr_char != None:
                comment += self.curr_char
                self.move_forward()
                c = self.curr_char + self.text[self.pos+1]
                if c == "*/" :
                    comment += "*/"
                    self.move_forward()
                    break 

        self.move_forward()        
        return Token(COMMENTS_TOKEN , comment  , start_line_no ,start_pos)

    def build_strings(self):
        
        value = ""
        start_pos = self.pos
        start_line_no = self.lin_no

        while self.curr_char != None :
            value += self.curr_char
            self.move_forward()
            if self.curr_char in HARDCODED_STRINGS:
                value += self.curr_char
                self.move_forward()
                break
        
        return Token(STRING_TOKEN , value  , start_line_no ,start_pos )

    def tokenize(self):

        droppy_tokens = []
        
        while self.curr_char != None :

            if self.curr_char in SPACE_TOKEN:
                #skip tabs and spaces
                self.move_forward()
            
            elif self.pos+1 < self.text_len and self.curr_char+self.text[self.pos+1] in COMMENTS_STARTS_WITH :
                #comments
                c = self.curr_char + self.text[self.pos+1]

                droppy_tokens.append(self.parse_comments(c))
            
            elif self.curr_char in HARDCODED_STRINGS:
                droppy_tokens.append(self.build_strings())

            elif self.curr_char in ASCII_TOKEN:
                droppy_tokens.append(self.build_characters())

            elif self.curr_char in DIGITS_TOKEN:
                droppy_tokens.append(self.build_numbers())
            
            elif self.curr_char in ARITHMETIC_OPERATORS:

                ##checking if it is a single equal or double equals 
                if self.pos+1 < len(self.text) and self.text[self.pos+1] == "=" :
                    t = Token(RELATIONAL_OPERATOR_TOKEN , "==" , self.lin_no , self.col)
                    droppy_tokens.append(t)
                    self.move_forward()
                else :
                    t = Token(ARITHMETIC_OPERATOR_TOKEN , self.curr_char , self.lin_no , self.col)
                    droppy_tokens.append(t)

                self.move_forward()

            elif self.curr_char in OPERATORS:

                t = Token(OPERATOR_TOKEN , self.curr_char , self.lin_no , self.col)
                droppy_tokens.append(t)
                self.move_forward()

            elif self.curr_char in RELATIONAL_OPERATOR:

                op = self.curr_char + self.text[self.pos+1]
                if op in RELATIONAL_OPERATOR:
                    # >= , <= 
                    t = Token(RELATIONAL_OPERATOR_TOKEN , op , self.lin_no , self.col)
                    self.move_forward()
                    droppy_tokens.append(t)
                else:
                    # > , <
                    t = Token(RELATIONAL_OPERATOR_TOKEN , self.curr_char , self.lin_no , self.col)
                
                self.move_forward()

            elif self.curr_char in BITWISE_OPERATORS:

                op = self.curr_char + self.text[self.pos+1]
                if op in LOGICAL_OPERATORS:
                    # && and ||
                    t = Token(LOGICAL_OPERATORS_TOKEN , op , self.lin_no , self.col)
                    self.move_forward()
                    droppy_tokens.append(t)

                else:
                    t = Token(BITWISE_OPERATORS_TOKEN , self.curr_char , self.lin_no , self.col)
                    droppy_tokens.append(t)
                
                self.move_forward()

            else:
                self.move_forward()

        return droppy_tokens

    def __repr__(self) -> str:
        return "Tokenize Class"
    
    def __str__(self) -> str:
        return f"{Tokenizer.__dir__}"