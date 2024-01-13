i=0
inp = ''
PLUS = '+'
MINUS = '-'
TIMES = '*'
DIVIDE = '/'
OPEN_PAREN = '('
CLOSE_PAREN = ')'
TERMINATING_SYM = '$'
sentence = ""
DIGIT= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_digit():
    if inp in DIGIT:
        return True

def get_number():
    global inp
    res = 0
    res = int(inp)
    next()
    while is_digit():
        res = 10*res + int(inp)
        next()
    return res

def my_SyntaxError():
    print("Syntax Error\n")
    pass

def computation():
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

def next():
    global i, inp

    while i < len(sentence) and sentence[i] == ' ':
        i = i + 1

    if i < len(sentence):
        inp = sentence[i]
    else:
        inp = '$'

    i = i + 1

def main(): 
    global sentence
    sentence = "10 -2 *(3+4) . 7 * 60 .  (63/3)*2-20."
    #sentence = input("Enter your expression: ")
    sentence =''.join(sentence.split())
    next()
    computation()
    pass

if __name__ == "__main__":
    main()
