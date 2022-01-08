import argparse
import sys

from utils.banner import banner
from utils.colors import *

def droopy_args() -> tuple:

    parser = argparse.ArgumentParser(description="Droopy Automated Static Code Analysis")
    parser.add_argument('-f' , '--file' , dest="file" , help="provide a javascript filename")
    parser.add_argument('-t','--thread',dest="thread" , help="provide number of threads [default 2]" , type=int , default=2)
    parser.add_argument('-o' , '--output' , dest="output" , help="provide a output folder name [default droppy_output]" , default="droppy_output")
    parser.add_argument('-d' , '--directory' , dest="directory" , help="provide a directory containing javascript files")
    parser.add_argument("-v","--verbose",action="store_true",default=False,dest="verbose",help="set for verbose output")
    parser.add_argument("-gj","--generate_json",action="store_true",default=False,dest="generate_json",help="set for generating output in json format")
    parser.add_argument("-gxml","--generate_xml",action="store_true",default=False,dest="generate_xml",help="set for generating output in xml format") 
    parser.add_argument("-dso","--donot_save_output",action="store_false",default=True,dest="is_logoutput",help="to log output[default true]")

    args = parser.parse_args()

    if args.directory is None and args.file is None :
        banner(blue,reset)
        print(reset)
        parser.print_help(sys.stderr)
        exit(-1)
   
    return (args.file , args.directory , args.thread , args.output 
                    ,args.verbose , args.is_logoutput , args.generate_json , 
                    args.generate_xml)