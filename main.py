from pprint import pprint
from typing import List
from DroppyAnalyzer import Token
from prettytable import PrettyTable
from DroppyAnalyzer.Scanner import VulnScanner

from utils.DroppyArgs import droopy_args
from DroppyAnalyzer.Tokenizer import Tokenizer
from utils.banner import print_seperator
from utils.colors import *
from utils.utils import dir_create, recursive_dir_search

class DroppyAnalyzer:

    def __init__(self , file_name : str,directory : str , output_dir : str , thread : int , verbose : bool = False):
        self.file_name = file_name
        self.directory = directory
        self.output_dir = output_dir
        self.thread = thread
        self.verbose = verbose
        self.file_results = {}
        self.analyzed_files = {}

    def analyze_file(self) -> None:
        
        with open(self.file_name) as f:
            contents = f.read()

        #tokenize each file
        lex = Tokenizer(self.file_name , contents)
        result = lex.tokenize()
        
        self.analyzed_files[self.file_name] = result
        self.file_results[self.file_name] = self.pretty_print(result)

        print_seperator(red , reset)
        print(self.file_name)
        print(reset)

        if self.verbose : print(self.pretty_print(result))

    def analyze_dir(self) -> None:

        filenames = recursive_dir_search(self.directory ,extension = ".js")
        for f in filenames:
            self.file_name = f
            self.analyze_file()
    
    def save_to_file(self) -> None:
        
        with open(f"{self.output_dir}/tokenized.log" , "w") as f:
            for key , value in self.file_results.items():
                f.write("\n\n\t\t"+"-"*50+"\n")
                f.write("\t\t\t"+key)
                f.write("\n\t\t"+"-"*50+"\n\n\n")
                f.write(str(value))

    def pretty_print(self,results  : List[Token]) -> PrettyTable :

        table = PrettyTable(['TokenType', 'Value' , "Line No" , "Column No"])
        for r in results:
            table.add_row([r.type , r.value , r.lin_no , r.column_no])
        return table

    def __repr__(self) -> str:
        return "[thread : {self.thread} , output_dir : {self.output_dir} ]"

    def __str__(self) -> str:
        return f" Results : {len(self.file_results)}"

if __name__ == "__main__":

    (file ,directory , thread , output , verbose , is_logoutput) = droopy_args()
    dir_create(output)

    analyzer = DroppyAnalyzer(file , directory , output , thread , verbose)
    
    # tokenize both file or recursively in directory
    if file:
        analyzer.analyze_file()
    else:
        analyzer.analyze_dir()

    #log to output file
    if is_logoutput : analyzer.save_to_file()

    v_scanner = VulnScanner(analyzer.analyzed_files)
    v_scanner.scan()
    
