from utils.DroppyArgs import droopy_args
from DroppyAnalyzer.Tokenizer import Tokenizer

if __name__ == "__main__":

    (file ,directory , thread , output) = droopy_args()

    with open("main.js") as f:
        code = f.read()

    droppy_lex = Tokenizer("dummy" , code)
    results = droppy_lex.tokenize()

    for r in results:
        print(r)
