from typing import List
from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import KEYWORDS_TOKEN, MODULES_TOKEN, NEWLINE_TOKEN
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

class ControlFlow:
    
    def __init__(self ,  analyzed_files : TokenizedDict) -> None:

        self.analyzed_files : dict = analyzed_files

        self.project_dead_codes = {}
        self.ifi_statements : List = ["if" , "else if"]
        
        
    def find_dead_code(self)->None:
        
        for file_name , tokens_list in self.analyzed_files.items():

            dead_codes = []

            for token in tokens_list:

                idx = tokens_list.index(token)
                
                look_ahead = None
                if idx+1 < len(tokens_list):
                     look_ahead = tokens_list[idx+1]

                if token.value == "if":
                    self._check_conditional_statement_dead(idx , tokens_list)

                elif look_ahead and str(token.value) + " " + str(look_ahead.value) == "else if":
                    self._check_conditional_statement_dead(idx+1 , tokens_list)

                elif token.value == "function":
                    result = self._check_functional_statement_dead(idx , tokens_list)

                    if result[0]:
                        #contains dead code
                        # print(result)
                        dead_codes.append(self.__build_dead_code_structure(tokens_list[idx+1].value , result[1]))


            self.project_dead_codes[file_name] = dead_codes

        

        pprint(self.project_dead_codes)


    def _check_conditional_statement_dead(self , idx : int , tokens_list : TokenizedDict):
        
        """
            parse the conditional statements and evaluate for dead code
            eg: 
                if(True || False) || if(False) ===> then the conditional statements are dead

        """
        start_idx = idx+2  #skipping if( and else if( tokens 

        conditional_tokens = self.__get_conditional_tokens(start_idx , tokens_list)
        
        print(conditional_tokens)
        

    def _check_functional_statement_dead(self , idx : int , tokens_list : TokenizedDict):
        """
            check for premature return statements not in outside of a scope block
            eg :
                function hello(msg){
                    if(msg){
                        return "hey"
                    }
                    return "bye"

                    # dead code
                    new_msg = func(msg)

                }
        """
        #skipping func name and ()
        i = idx+3
        while i < len(tokens_list):
            token = tokens_list[i]

            if token.value == "return":
                newline_idx = i + self.__move_until_newline(i , tokens_list)

                more_statements = self.__contains_more_statement(newline_idx+1 , tokens_list)
                
                if more_statements[0]:
                    
                    return [ True , {
                        "line no"  : tokens_list[newline_idx+1].lin_no ,
                        "column no": tokens_list[newline_idx+1].lin_no ,
                        "extra statements": more_statements[1]
                    }]
                i = newline_idx+1

            elif token.value in ["if" , "else"]:
                i += self.__move_untill_endcondition(i+1 ,tokens_list )

            else :
                i += 1


        return [False , {}]

    def __move_untill_endcondition(self , idx : int , tokens_list : TokenizedDict):
        
        for i in range(idx , len(tokens_list)): 
            if tokens_list[i].value == "}":
                return (i+1)-idx
        

    def __move_until_newline(self , idx : int ,  tokens_list : TokenizedDict) ->int :

        for i in range(idx , len(tokens_list)):
            if tokens_list[i].type in NEWLINE_TOKEN:
                return (i-idx)

    def __contains_more_statement(self , idx : int , tokens_list : TokenizedDict) -> list :
        
        is_statements_present = False
        extra_statements= ""

        for i in range(idx , len(tokens_list)):
            if tokens_list[i].type == NEWLINE_TOKEN:
                if is_statements_present: 
                    extra_statements += "\n"

            elif tokens_list[i].value == "}":
                break
            else:
                is_statements_present = True
                extra_statements +=  str(tokens_list[i].value) + " "

        return [is_statements_present , extra_statements ]


    def __get_conditional_tokens(self , idx : int , tokens_list : TokenizedDict):

        condition_tokens = []
        while tokens_list[idx].value != "(":
            
            condition_tokens.append(tokens_list[idx])
            idx += 1

        return condition_tokens


    def __build_dead_code_structure(self,func_name : str , details : dict):

        return {
            "function name" : func_name ,
            "details" : details
        }

