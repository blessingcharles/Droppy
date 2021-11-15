import argparse

def droopy_args() -> tuple:

    parser = argparse.ArgumentParser(description="Droopy Automated Static Code Analysis")
    parser.add_argument('-f' , '--file' , dest="file")
    parser.add_argument('-t','--thread',dest="thread")
    parser.add_argument('-o' , '--output' , dest="output")

    args = parser.parse_args()

    return (args.file , args.thread , args.output)