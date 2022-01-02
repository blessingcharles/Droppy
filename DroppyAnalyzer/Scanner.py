from typing import List
from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import KEYWORDS_TOKEN, MODULES_TOKEN
from utils.banner import print_seperator
from DroopyBrain.deprecated import DEPRECATED_FEATURES

from utils.colors import *
from pprint import pprint

class VulnScanner:
    def __init__(self , analyzed_files : TokenizedDict) -> None:
        
        self.analyzed_files : dict = analyzed_files
        self.js_sources = []
        self.js_sinks = []

        self.deprecated_features_details = {}
        self.deprecated_features_count = 0

        self.get_details_from_brain()

    def scan(self):

        self.scan_xss()
        self.scan_deprecated_features()

    def scan_deprecated_features(self):

        print_seperator(blue,print_seperator)
        print(f"{green}[+]Scanning for deprecated features {reset}")

        for file_name , tokens_list in self.analyzed_files.items():
            
            details = []
            count = 0

            for token in tokens_list:
                if token.type in [MODULES_TOKEN , KEYWORDS_TOKEN] and token.value in DEPRECATED_FEATURES:
                    details.append(self.__build_deprecated_feature(token.value , DEPRECATED_FEATURES[token.value]))                    
                    count += 1

            self.deprecated_features_count += count
            self.deprecated_features_details[file_name] = {
                                "count" : count ,
                                "deprecated features list":details    
            } 

        pprint(self.deprecated_features_details)

    def scan_xss(self):

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
    

    def __build_deprecated_feature(self , name : str , reference : str) -> None:
        
        return {
            "name":name ,
            "reference":reference
        }

    def __repr__(self) -> str:
        return "Find Sources and Sinks in tokenized js files"

    def __str__(self) -> str:
        return self.analyzed_files