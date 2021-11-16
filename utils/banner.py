

def banner(blue,reset):
    print(blue,end="")
    print('''
                    
                             ^_^                      
                            {=.=}   
                        (   /  (           
                        (  /   )    
                        \(_)__))    
                      DROPPY SCANNER
''',end="")
    print(reset,end="")

def print_seperator(color,reset,count:int = 100):
    print(color,end="")
    print("-"*count)
    print(reset,end="")

#banner()