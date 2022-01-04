from pprint import pp, pprint
from typing import List
from rich.traceback import install

install(show_locals=True)

from DroppyAnalyzer import Token
from prettytable import PrettyTable
from DroppyAnalyzer.Scanner import ControlFlow, VulnScanner
from DroppyAnalyzer.Fuzzer import Fuzzer
from DroppyAnalyzer.Analyzer import DroppyAnalyzer

from utils.DroppyArgs import droopy_args
from DroppyAnalyzer.Tokenizer import Tokenizer
from utils.banner import print_seperator
from utils.colors import *
from utils.utils import dir_create, recursive_dir_search

if __name__ == "__main__":

    (file ,directory , thread , output , verbose , is_logoutput) = droopy_args()
    csv_dir = f"{output}/csv_output"
    dir_create(output)
    dir_create(csv_dir)

    analyzer = DroppyAnalyzer(file , directory , output , thread , verbose)
    
    # tokenize both file or recursively in directory
    if file:
        analyzer.analyze_file()
    else:
        analyzer.analyze_dir()

    #log to output file
    if is_logoutput : analyzer.save_to_file()

    v_scanner = VulnScanner(analyzer.analyzed_files , output , verbose)
    v_scanner.scan()

    fuzzer = Fuzzer(analyzer.analyzed_files , output ,csv_dir, verbose)
    fuzzer.fuzz()
    fuzzer.brief_detail()
    fuzzer.save_to_file()
    fuzzer.generate_total_results()

    # pp(analyzer.analyzed_files)
    cfa = ControlFlow(analyzer.analyzed_files)

    cfa.find_dead_code()
    