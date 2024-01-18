from tokenizer import Tokenizer
from symbol_table import table

tokenizer = None
_table = None

def my_SyntaxError():
    print("Syntax Error\n")
    pass

def match(token):
    return Tokenizer.cur_token == token
    
def computation():
    res = 0
    tokenizer.next_token() # compuation
    tokenizer.next_token() #
    
    while match(Tokenizer.KEYWORD_VAR):
        tokenizer.next_token() # identifier
        tokenizer.next_token() # assignment token
        tokenizer.next_token() # first number
        tokenizer.last_val = E()
        _table.insert(tokenizer.last_id, tokenizer.last_val)
        tokenizer.next_token() # semicolon
        
    res = E()
    print(res, "\n")

    while match(Tokenizer.SEMICOLON_TOKEN):
        tokenizer.next_token()
        res = E()
        print(res, "\n")

def E():
    res = 0
    res = T()
    while(True):
        if match(Tokenizer.ADDOP):
            tokenizer.next_token()
            res = res + T()
        elif match(Tokenizer.SUBOP):
            tokenizer.next_token()
            res = res - T()
        else:
            break

    return res

def T():
    res =0
    res = F()
    while(True):
        if match(Tokenizer.MULOP):
            tokenizer.next_token()
            res = res*F()
        
        elif match(Tokenizer.DIVIDEOP):
            tokenizer.next_token()
            res = res/F()

        else:
            break

    return res

def F():
    res =0
    if match(Tokenizer.LPAREN_TOKEN):
        tokenizer.next_token()
        res = E()
        # tokenizer.next_token()
        if match(Tokenizer.RPAREN_TOKEN):
            tokenizer.next_token()
        else:
            my_SyntaxError()

    elif match(Tokenizer.INTEGER):
       res = tokenizer.last_val
       tokenizer.next_token()
    
    elif Tokenizer.cur_token == Tokenizer.IDENTIFIER_TOKEN:
        res = _table.get_val(tokenizer.last_id)
        tokenizer.next_token()
    else:
        my_SyntaxError()

    return res



def main(): 
    global tokenizer, _table
    sentence = "computation var i <- 2 * 3; var abracadabra <- 7; (((abracadabra * i))); i - 5 - 1 ."
    #sentence = input("Enter your expression: ")
    tokenizer = Tokenizer(sentence)
    _table = table()
    computation()
    pass

if __name__ == "__main__":
    main()
