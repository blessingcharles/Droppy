
from typing import List, TypedDict


class Token:

    def __init__(self, type : str, value :str ,lin_no , column_no : int , info : dict = {}):

        self.type : str = type
        self.value : str  = value
        self.lin_no : int = lin_no
        self.column_no : int = column_no 
        self.info : dict = info

    def __repr__(self) -> str:

        return f"[type : {self.type} , value : {self.value}] \
                INFO : {self.info}"

    def __str__(self) -> str:

        return f"[type : {self.type} , value : {self.value}]"


class TokenizedDict(TypedDict):
    filename : List[Token]