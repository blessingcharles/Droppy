from typing import List
from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import ARITHMETIC_OPERATOR_TOKEN, COMMENTS_TOKEN, MODULES_TOKEN
from DroppyAnalyzer.types.keywords import DECLARATIONS, VAR_OPERATORS
from utils.banner import print_seperator

from utils.colors import *
from pprint import pprint

class Fuzzer:

    def __init__(self , analyzed_files : TokenizedDict) -> None:
        
        self.analyzed_files : dict = analyzed_files
        
        self.var_details = {}
        self.func_details = {}

        self.var_total_count = 0
        self.var_constants_count = 0
        self.func_total_count = 0

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

    def _parse_all_variables(self):

        """
            parse all variables details from the tokenized js file
        """

        for file_name , tokens_list in self.analyzed_files.items():
            
            details = []
            total_count = 0
            constants_count = 0

            for token in tokens_list:
                if token.value in DECLARATIONS:
                    total_count += 1
                    if token.value == "const":
                        constants_count += 1
                    
                    cur_idx = tokens_list.index(token)

                    variable = tokens_list[cur_idx+1]
                    initial_value = None
                    curr_value = ""
                    braces = ["(" , ")"]

                    """
                        @if variable assignment  consists of combinatorial of other operators
                        eg : let x = (a+b)/c-d
                    """

                    if tokens_list[cur_idx+2].value == "=":
                        ele_idx = cur_idx+3
                        
                        #getting braces
                        while tokens_list[ele_idx].value in braces:
                            curr_value += tokens_list[ele_idx].value
                            ele_idx += 1
                        
                        #getting first variable 
                        curr_value += str(tokens_list[ele_idx].value)
                        ele_idx += 1

                        #getting operands and operators
                        while tokens_list[ele_idx].value in VAR_OPERATORS:
                            
                            #operators
                            curr_value += tokens_list[ele_idx].value
                            ele_idx += 1

                            #operands
                            curr_value += str(tokens_list[ele_idx].value)
                            ele_idx += 1

                            #braces
                            while tokens_list[ele_idx].value in braces:
                                curr_value += tokens_list[ele_idx].value
                                ele_idx += 1

                    
                    if curr_value:  initial_value = curr_value

                    details.append( self.__build_var_detail(token.value , variable.value ,initial_value) )
            

            self.var_total_count += total_count
            self.var_constants_count += constants_count

            self.var_details[file_name] = {"details" : details ,
                                            "total count": total_count,
                                            "constants count": constants_count
                                            }   
            

        pprint(self.var_details)
    
    def _parse_all_functions(self):

        """
            parse all functions and passed parameters
        """

        for file_name , tokens_list in self.analyzed_files.items():
            total_count = 0 
            details = []
            for token in tokens_list:

                if token.value == "function":
                    total_count += 1
                    t_idx = tokens_list.index(token)+1     # moving to function name
                    func_name = tokens_list[t_idx].value    
                    t_idx += 2 #skipping open brace also
                    
                    #loop untill closing brace encountered to get all passing parameters
                    passed_args = []
                    while tokens_list[t_idx].value is not ")":
                        param = tokens_list[t_idx].value
                        passed_args.append(param)
                        t_idx += 1
                    
                    details.append(self.__build_func_detail(func_name , passed_args))
            
            
            self.func_total_count += total_count 
            self.func_details[file_name] = {
                "total count":total_count ,
                "details":details
            }

    def brief_detail(self):
        """
            brief detail about how many variables declared and functions count in each file
        """
        self._parse_all_variables()
        self._parse_all_functions()
        pprint(self.func_details)
    
    def __build_var_detail(self , type : str , name : str , initial_value : str = None ):
        return {
                "declaration type":type ,
                "name":name , 
                "value":initial_value
                }

    def __build_func_detail(self , name : str , passed_args : List[str]):
        return {
            "function name":name ,
            "arguments count":len(passed_args) ,
            "arguments list":passed_args 
            }

    def __repr__(self) -> str:
        return "Find Comments and log in js code"
