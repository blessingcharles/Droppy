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


    def analyze_file(self):
        
        with open(self.file_name) as f:
            contents = f.read()
        lex = Tokenizer(self.file_name , contents)
        results = lex.tokenize()
        print_seperator(red , reset)
        print(self.file_name)
        print(reset)
        self.pretty_print(results)

    def analyze_dir(self):
        filenames = recursive_dir_search(self.directory ,extension = ".js")
        for f in filenames:
            self.file_name = f
            self.analyze_file()
    
    def pretty_print(self,results):
        for r in results:
            print(r)

    def __repr__(self) -> str:
        return "Droppy Class with lexical analyzer"

    def __str__(self) -> str:
        return f"[thread : {self.thread} , output_dir : {self.output_dir} ]"

if __name__ == "__main__":

    (file ,directory , thread , output) = droopy_args()

    analyzer = DroppyAnalyzer(file , directory , output , thread)
    
    if file:
        analyzer.analyze_file()
    else:
        analyzer.analyze_dir()

    
