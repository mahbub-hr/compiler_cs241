from tokenizer import Tokenizer

tokenizer = None

def my_SyntaxError():
    print("Syntax Error\n")
    pass

def computation():
    res = 0
    tokenizer.next_token() # compuation
    tokenizer.next_token() #
    
    while Tokenizer.cur_token == Tokenizer.KEYWORD_VAR:
        tokenizer.next_token() # identifier
        tokenizer.next_token() # assignment token
        tokenizer.next_token() # first number
        tokenizer.last_val = E()
        tokenizer.next_token() # semicolon
        tokenizer.next_token()
        
    res = E()
    print(res, "\n")

    while Tokenizer.cur_token == Tokenizer.SEMICOLON_TOKEN:
        tokenizer.next_token()
        res = E()
        tokenizer.next_token()
        print(res, "\n")

def E():
    res = 0
    res = T()
    while(True):
        if Tokenizer.cur_token == Tokenizer.ADDOP:
            tokenizer.next_token()
            res = res + T()
        elif Tokenizer.cur_token == Tokenizer.SUBOP:
            tokenizer.next_token()
            res = res - T()
        else:
            break

    return res

def T():
    res =0
    res = F()
    while(True):
        if Tokenizer.cur_token == Tokenizer.MULOP:
            tokenizer.next_token()
            res = res*F()
        
        elif Tokenizer.cur_token == Tokenizer.DIVIDEOP:
            tokenizer.next_token()
            res = res/F()

        else:
            break

    return res

def F():
    res =0
    if(Tokenizer.cur_token == Tokenizer.LPAREN_TOKEN):
        tokenizer.next_token()
        res = E()
        # tokenizer.next_token()
        if(Tokenizer.cur_token == Tokenizer.RPAREN_TOKEN):
            tokenizer.next_token()
        else:
            my_SyntaxError()

    elif Tokenizer.cur_token == Tokenizer.INTEGER:
       res = tokenizer.last_val
       tokenizer.next_token()
    
    elif Tokenizer.cur_token == Tokenizer.IDENTIFIER_TOKEN:
        tokenizer.next_token()
    else:
        my_SyntaxError()

    return res



def main(): 
    global tokenizer
    sentence = "computation ((2*3)); 46/2."
    #sentence = input("Enter your expression: ")
    tokenizer = Tokenizer(sentence)
    computation()
    pass

if __name__ == "__main__":
    main()
