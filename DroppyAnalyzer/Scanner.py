from typing import List
from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import COMMENTS_TOKEN, MODULES_TOKEN
from utils.banner import print_seperator

from utils.colors import *

class Fuzzer:
    def __init__(self , analyzed_files : TokenizedDict) -> None:
        self.analyzed_files : dict = analyzed_files
    
    def fuzz(self):
        #find comments token
        for file_name , tokens_list in self.analyzed_files.items():
            print_seperator(blue,reset)
            print(f"{green}[+]Fuzzing file for comments : {file_name}{reset}\n")
            flag = False

            #iterating through each lexically analyzed tokens for comments
            for token in tokens_list:
                if token.type == COMMENTS_TOKEN :
                    flag = True
                    print(f"{red}[-] comments in [lin:col {token.lin_no}:{token.column_no}] {reset} : {token.value}")
            if not flag :
                print(f"{grey}[*] No Comments found {reset}")


        #find log tokens
        for file_name , tokens_list in self.analyzed_files.items():
            print_seperator(blue,reset)
            print(f"{green}[+]Fuzzing file for logs: {file_name}{reset}\n")
            flag = False

            #iterating through each lexically analyzed tokens for comments
            for token in tokens_list:
                if token.value == "console.log" :
                    flag = True
                    print(f"{red}[-] log in [lin:col {token.lin_no}:{token.column_no}] {reset} : {token.value}")
            if not flag :
                print(f"{grey}[*] No Comments found {reset}")

    
    def __repr__(self) -> str:
        return "Find Comments and log in js code"

class VulnScanner:
    def __init__(self , analyzed_files : TokenizedDict) -> None:
        
        self.analyzed_files : dict = analyzed_files
        self.js_sources = []
        self.js_sinks = []
        self.get_details_from_brain()

    def scan(self):
        for file_name , tokens_list in self.analyzed_files.items():
            print_seperator(blue,reset)
            print(f"{green}[+]Analyzing file : {file_name}{reset}\n")
            flag = False

            #iterating through each lexically analyzed tokens
            for token in tokens_list:
                if token.type == MODULES_TOKEN :
                    if token.value in self.js_sources:
                        flag = True
                        print(f"{red}[-] possible source [lin:col {token.lin_no}:{token.column_no}] {reset} : {token.value}")
                    if token.value in self.js_sinks:
                        flag = True
                        print(f"{red}[-] possible sinks [lin:col {token.lin_no}:{token.column_no}] {reset} : {token.value}")
            if not flag :
                print(f"{grey}[*] No Source or Sink found {reset}")

            
    
    def get_details_from_brain(self) -> None:
        
        with open("DroopyBrain/domxss_sinks.txt") as f :
            for line in f.readlines():
                self.js_sinks.append(line.strip())
        
        with open("DroopyBrain/domxss_sources.txt") as f :
            for line in f.readlines():
                self.js_sources.append(line.strip())


    def __repr__(self) -> str:
        return "Find Sources and Sinks in tokenized js files"

    def __str__(self) -> str:
        return self.analyzed_files