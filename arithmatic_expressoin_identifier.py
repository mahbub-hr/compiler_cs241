inp = ''
PLUS = '+'
MINUS = '-'
TIMES = '*'
DIVIDE = '/'
OPEN_PAREN = '('
CLOSE_PAREN = ')'
TERMINATING_SYM = '$'
sentence = ""
KEYWORD_VAR = "var"
KEYWORD_COMPUTATION = "computation"

import Tokenizer

def my_SyntaxError():
    print("Syntax Error\n")
    pass

def computation():
    string = get_string()
    print(string, "\n")
    if string != KEYWORD_COMPUTATION:
        my_SyntaxError()
        return 

    res = 0
    res = E()

    if inp == '.':
        print(res, "\n")
        next()
        if inp == TERMINATING_SYM:
            return
        computation()
    else:
        my_SyntaxError()

def E():
    global inp
    res = 0
    res = T()
    while(True):
        if inp == PLUS:
            next()
            res = res + T()
        elif inp == MINUS:
            next()
            res = res - T()
        else:
            break

    return res

def T():
    res =0
    res = F()
    while(True):
        if inp == TIMES:
            next()
            res = res*F()
        
        elif inp == DIVIDE:
            next()
            res = res/F()

        else:
            break

    return res

def F():
    res =0
    if(inp == OPEN_PAREN):
        next()
        res = E()
        if(inp == CLOSE_PAREN):
            next()
        else:
            my_SyntaxError()

    elif is_digit()== True:
       res = get_number()
    else:
        my_SyntaxError()

    return res



def main(): 
    sentence = "computation 10 -2 *(3+4) . 7 * 60 .  (63/3)*2-20."
    #sentence = input("Enter your expression: ")
    tokenizer = Tokenizer(sentence)
    next()
    computation()
    pass

if __name__ == "__main__":
    main()
