import argparse
import sys

def droopy_args() -> tuple:

    parser = argparse.ArgumentParser(description="Droopy Automated Static Code Analysis")
    parser.add_argument('-f' , '--file' , dest="file" , help="provide a javascript filename")
    parser.add_argument('-t','--thread',dest="thread" , help="provide number of threads [default 2]" , type=int , default=2)
    parser.add_argument('-o' , '--output' , dest="output" , help="provide a output folder name [default droppy_output]" , default="droppy_output")
    parser.add_argument('-d' , '--directory' , dest="directory" , help="provide a directory containing javascript files")
    args = parser.parse_args()

    if args.directory is None and args.file is None :
        parser.print_help(sys.stderr)
        exit(-1)

    return (args.file , args.directory , args.thread , args.output )