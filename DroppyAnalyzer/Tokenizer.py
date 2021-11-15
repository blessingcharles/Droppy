from .types.generals import *
from .types.keywords import *
from .types.operators import *
from . import Token

class Tokenizer:

    def __init__(self ,file_name : str , text : str):

        self.text : str = text
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

    def build_characters(self , prev_word : str = ""):
        word : str = prev_word 
        start_pos = self.pos

        while self.curr_char != None and self.curr_char in IDENTIFIERS_SET:
                word += self.curr_char
                self.move_forward()
        
        if word in KEYWORDS:
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

    def tokenize(self):

        droppy_tokens = []
        
        while self.curr_char != None :

            if self.curr_char in SPACE_TOKEN:
                self.move_forward()
            
            elif self.curr_char in ASCII_TOKEN:
                droppy_tokens.append(self.build_characters())

            elif self.curr_char in DIGITS_TOKEN:
                droppy_tokens.append(self.build_numbers())
            
            elif self.curr_char in OPERATORS:
                droppy_tokens.append(self.build_operators())
            else:
                self.move_forward()

        return droppy_tokens

    def __repr__(self) -> str:
        return "Tokenize Class"