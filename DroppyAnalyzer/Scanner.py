from typing import List
from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import IDENTIFIER_TOKEN, KEYWORDS_TOKEN, MODULES_TOKEN, NEWLINE_TOKEN
from utils.banner import print_seperator
from DroopyBrain.deprecated import DEPRECATED_FEATURES

from utils.colors import *
from pprint import pprint

class VulnScanner:
    def __init__(self , analyzed_files : TokenizedDict , output_dir : str , verbose : bool = False) -> None:
        
        self.analyzed_files : dict = analyzed_files
        self.verbose = verbose
        
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
                    
                    result = self._check_conditional_statement_dead(idx , tokens_list)

                    if result[0]:
                        dead_codes.append(self.__build_conditonal_dead_code_structure(result[1]))

                elif look_ahead and str(token.value) + " " + str(look_ahead.value) == "else if":
                    
                    result = self._check_conditional_statement_dead(idx+1 , tokens_list)
                    
                    if result[0]:
                        dead_codes.append(self.__build_conditonal_dead_code_structure(result[1]))

                elif token.value == "function":
                    result = self._check_functional_statement_dead(idx , tokens_list)

                    if result[0]:
                        #contains dead code
                        dead_codes.append(self.__build_func_dead_code_structure(tokens_list[idx+1].value , result[1]))


            self.project_dead_codes[file_name] = dead_codes

        

        pprint(self.project_dead_codes)


    def _check_conditional_statement_dead(self , idx : int , tokens_list : TokenizedDict):
        
        """
            parse the conditional statements and evaluate for dead code
            eg: 
                if(True || False) || if(1+2 < 10) ===> then the conditional statements are dead

        """
        start_idx = idx+2  #skipping if( and else if( tokens 

        conditional_tokens = self.__get_conditional_tokens(start_idx , tokens_list)
        
        if self.__check_for_dynamic_variables(conditional_tokens):
            #contains dynamic variables if present skip it
            return [False , {}]

        cond_str = ""

        for token in conditional_tokens:
            cond_str += str(token.value)



        #replacing boolean with 0 and 1
        fixed_cond_str = self.__fix_string(cond_str)

        result = eval(fixed_cond_str)

        return [True ,  {
            "condition": cond_str ,
            "parsed result":result ,
            "line no": tokens_list[idx].lin_no
        }] 


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
        while tokens_list[idx].value != ")":
            
            condition_tokens.append(tokens_list[idx])
            idx += 1

        return condition_tokens


    def __build_func_dead_code_structure(self,func_name : str , details : dict):

        return {
            "type" : "Function",
            "issue":"dead code after return" ,
            "function name" : func_name ,
            "details" : details
        }

    def __build_conditonal_dead_code_structure(self ,details : dict ):

        return {
            "type" : "Conditional Statements",
            "issue" : "static evaluation of conditions" ,
            "details" : details
        }

    def __check_for_dynamic_variables(self , condition_tokens : TokenizedDict) -> bool:
        """
            check if a dynamic variabes present in a given token list

            return True if present else False
        """
    
        boolean_statements = ["true" , "false"]

        for token in condition_tokens:
            if token.type == IDENTIFIER_TOKEN and token.value not in boolean_statements:
                return True

        return False


    def __fix_string(self , cond_str : str) -> str :
        fixed_cond_str = ""

        for word in cond_str.split():
            if word == "true":
                fixed_cond_str += f" 1 "
            elif word == "false":
                fixed_cond_str += f" 0 "
            else :
                fixed_cond_str += word

        return fixed_cond_str
