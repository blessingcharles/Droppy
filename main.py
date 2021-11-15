from utils.DroppyArgs import droopy_args
from DroppyAnalyzer.Tokenizer import Tokenizer

if __name__ == "__main__":

    (file , thread , output) = droopy_args()

    code = """if(true || false){
        // hello
        a = 5
        string = "hurreh"
        /* this is 
        fucking awesome */
        console.log("hi")
    }"""

    droppy_lex = Tokenizer("dummy" , code)
    results = droppy_lex.tokenize()

    for r in results:
        print(r)
