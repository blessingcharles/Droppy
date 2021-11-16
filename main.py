from pprint import pprint
from typing import List
from DroppyAnalyzer import Token
from prettytable import PrettyTable

from utils.DroppyArgs import droopy_args
from DroppyAnalyzer.Tokenizer import Tokenizer
from utils.banner import print_seperator
from utils.colors import *
from utils.utils import recursive_dir_search

class DroppyAnalyzer:

    def __init__(self , file_name : str,directory : str , output_dir : str , thread : int ):
        self.file_name = file_name
        self.directory = directory
        self.output_dir = output_dir
        self.thread = thread
        self.file_results = {}

    def analyze_file(self):
        
        with open(self.file_name) as f:
            contents = f.read()

        lex = Tokenizer(self.file_name , contents)
        result = lex.tokenize()
        self.file_results[self.file_name] = result

        print_seperator(red , reset)
        print(self.file_name)
        print(reset)
        self.pretty_print(result)

    def analyze_dir(self):
        filenames = recursive_dir_search(self.directory ,extension = ".js")
        for f in filenames:
            self.file_name = f
            self.analyze_file()
    
    def pretty_print(self,results  : List[Token]):
        table = PrettyTable(['TokenType', 'Value' , "Line No" , "Column No"])
        for r in results:
            table.add_row([r.type , r.value , r.lin_no , r.column_no])    
        print(table)

    def __repr__(self) -> str:
        return "[thread : {self.thread} , output_dir : {self.output_dir} ]"

    def __str__(self) -> str:
        return f" Results : {len(self.file_results)}"

if __name__ == "__main__":

    (file ,directory , thread , output) = droopy_args()

    analyzer = DroppyAnalyzer(file , directory , output , thread)
    
    if file:
        analyzer.analyze_file()
    else:
        analyzer.analyze_dir()

    
