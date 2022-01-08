from os import write
from typing import List
import csv

from DroppyAnalyzer import Token, TokenizedDict
from DroppyAnalyzer.types.generals import ARITHMETIC_OPERATOR_TOKEN, COMMENTS_TOKEN, MODULES_TOKEN
from DroppyAnalyzer.types.keywords import DECLARATIONS, VAR_OPERATORS
from utils.banner import print_seperator

from utils.colors import *
from pprint import pprint

class Fuzzer:

    def __init__(self , analyzed_files : TokenizedDict ,output_dir : str ,csv_dir : str ,verbose : bool = False) -> None:
        
        self.analyzed_files : dict = analyzed_files
        self.verbose = verbose
        self.output_dir = output_dir
        self.csv_dir = csv_dir

        self.output_variable_file = f"{self.csv_dir}/fuzzer_variables.csv"
        self.output_func_file_name = f"{self.csv_dir}/fuzzer_func.csv"
        self.output_fuzz_file_name = f"{self.csv_dir}/fuzzer.csv"
        self.output_fuzztotal_file_name = f"{self.csv_dir}/total_fuzz.csv"

        self.func_details = {}
        self.var_details = {}
        self.comments_details = {}
        self.log_details = {}

        self.var_total_count = 0
        self.var_constants_count = 0
        self.func_total_count = 0

    def fuzz(self):
        #find comments token
        for file_name , tokens_list in self.analyzed_files.items():
            print_seperator(blue,reset)
            print(f"{green}[+]Fuzzing file for comments : {file_name}{reset}\n")
            flag = False
            details = []

            #iterating through each lexically analyzed tokens for comments
            for token in tokens_list:
                if token.type == COMMENTS_TOKEN :
                    flag = True
                    print(f"{red}[-] comments in [lin:col {token.lin_no}:{token.column_no}] {reset} : {token.value}")
                
                    details.append(self.__build_fuzz_details("Comments present" , token.value , token.lin_no))

            self.comments_details[file_name] = {
                "details":details
            }

            if not flag :
                print(f"{grey}[*] No Comments found {reset}")


        #find log tokens
        for file_name , tokens_list in self.analyzed_files.items():
            print_seperator(blue,reset)
            print(f"{green}[+]Fuzzing file for logs: {file_name}{reset}\n")
            flag = False
            details = []

            #iterating through each lexically analyzed tokens for comments
            for token in tokens_list:

                idx = tokens_list.index(token)

                log_token = None

                if idx+2 < len(tokens_list):
                     log_token = tokens_list[idx+2]

                if token.value == "console.log" :
                    flag = True
                    print(f"{red}[-] log in [lin:col {token.lin_no}:{token.column_no}] {reset} : {log_token.value}")
            
                    details.append(self.__build_fuzz_details("log statement present" , log_token.value , token.lin_no))

            self.log_details[file_name] = {
                "details":details
            }

            if not flag :
                print(f"{grey}[*] No Comments found {reset}")

    
    def brief_detail(self):
        """
            brief detail about how many variables declared and functions count in each file
        """
        self._parse_all_variables()
        self._parse_all_functions()
    
    def save_to_file(self):

        #saving fuzzed details
        headers = ["path" , "line_number" , "error_type" , "value"]
        with open(self.output_fuzz_file_name , "w") as f:
            writer = csv.writer(f)

            writer.writerow(headers)

            # comments details
            for file_name , results in self.comments_details.items():
                for detail in results["details"]:
                    writer.writerow([file_name , detail["line no"] , detail["type"] , detail["value"]])

            #console log details
            for file_name , results in self.log_details.items():
                for detail in results["details"]:
                    writer.writerow([file_name , detail["line no"] , detail["type"] , detail["value"]])

        #saving parsed variables declaration with init values

        headers = ["path" ,"line_number" , "declaration_type" , "variable_name" , "initial_value"]

        with open(self.output_variable_file , "w") as f :
            writer = csv.writer(f)

            writer.writerow(headers)
            for file_name , results in self.var_details.items():
                for detail in results["details"]:
                    writer.writerow([file_name, detail["line no"] ,detail["declaration type"] , detail["name"] , detail["value"]])

    
        #saving parsed function details 
        headers = ["path" , "line_number" ,"function_name" , "arguments_list" ,"arguments_count"]

        with open(self.output_func_file_name , "w") as f:
            writer = csv.writer(f)

            writer.writerow(headers)

            for file_name , results in self.func_details.items():
                for detail in results["details"]:
                    args = list(filter(lambda a: a != ",", detail["arguments list"]))

                    writer.writerow([file_name , detail["line no"] , detail["function name"] ,args, detail["arguments count"] ])

    def generate_total_results(self):

        headers = ["path" , "variables_count" , "constants_count" , "functions_count" 
                                                        , "comments_count" , "log_count"]

        with open(self.output_fuzztotal_file_name , "w") as f:
            writer = csv.writer(f)
            
            writer.writerow(headers)

            for file_name , results in self.var_details.items():
                constants_count = results["constants count"]
                variables_count = results["total count"]
                functions_count = self.func_details[file_name]["total count"]
                comments_count = len(self.comments_details[file_name]["details"])
                log_count = len(self.log_details[file_name]["details"])
                
                writer.writerow([file_name , variables_count , constants_count , functions_count , comments_count , log_count])


    def _parse_arrays(self, tokens_list:TokenizedDict , idx : int = 0):
        
        cur_arr = "["

        while tokens_list[idx].value != "]":
            cur_arr += str(tokens_list[idx].value)
            idx += 1

        cur_arr += "]"
        return cur_arr

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
                    square_brackets = ["[" , "]"]

                    """
                        @if variable assignment  consists of combinatorial of other operators
                        eg : let x = (a+b)/c-d
                    """

                    if tokens_list[cur_idx+2].value == "=":
                        ele_idx = cur_idx+3
                        
                        # array initialisation parsing
                        if tokens_list[ele_idx].value in square_brackets:
                            curr_value = self._parse_arrays(tokens_list , ele_idx+1)

                        #normal expression parsing
                        else :
                            #getting braces
                            while tokens_list[ele_idx].value in braces:
                                curr_value += tokens_list[ele_idx].value
                                ele_idx += 1
                            #getting first variable 
                            curr_value += str(tokens_list[ele_idx].value)
                            ele_idx += 1

                            #getting operands and operators
                            while tokens_list[ele_idx].value in VAR_OPERATORS + [","]:
                                
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

                        details.append( self.__build_var_detail(token.value , variable.value , token.lin_no  ,initial_value) )
            

            self.var_total_count += total_count
            self.var_constants_count += constants_count

            self.var_details[file_name] = {"details" : details ,
                                            "total count": total_count,
                                            "constants count": constants_count
                                            }   
            

    def _parse_all_functions(self):

        """
            parse all functions and passed parameters
        """

        for file_name , tokens_list in self.analyzed_files.items():
            total_count = 0 
            details = []
            for token in tokens_list:

                if token.value == "function":
                    lin_no = token.lin_no
                    total_count += 1
                    t_idx = tokens_list.index(token)+1     # moving to function name
                    func_name = tokens_list[t_idx].value    
                    t_idx += 2 #skipping open brace also
                    
                    #loop untill closing brace encountered to get all passing parameters
                    passed_args = []
                    while tokens_list[t_idx].value != ")":
                        param = tokens_list[t_idx].value
                        passed_args.append(param)
                        t_idx += 1
                    
                    details.append(self.__build_func_detail(func_name , passed_args , lin_no))
            
            
            self.func_total_count += total_count 
            self.func_details[file_name] = {
                "total count":total_count ,
                "details":details
            }

    def __build_var_detail(self , type : str , name : str ,line_no : int, initial_value : str = None ):
        return {
                "declaration type":type ,
                "name":name , 
                "value":initial_value ,
                "line no": line_no
                }

    def __build_func_detail(self , name : str , passed_args : List[str] , line_no : int):
        return {
            "line no": line_no ,
            "function name":name ,
            "arguments count":len(passed_args) ,
            "arguments list":passed_args 
            }

    def __build_fuzz_details(self ,type : str ,value : str , line_no : int):

        return {
            "type" : type ,
            "value" : value ,
            "line no":line_no
        }

    def __repr__(self) -> str:
        return "Find Comments and log in js code"
