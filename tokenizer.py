class Tokenizer:
    DIGIT= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    KEYWORD = ["var", "computation"]
    PERIOD = '.'
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    SEMICOLON = ';'
    PERIOD_TOKEN = 0
    ADDOP = 1
    SUBOP = 2
    MULOP = 3
    DIVIDEOP = 4
    LPAREN_TOKEN = 5
    RPAREN_TOKEN = 6
    KEYWORD_TOKEN = 7
    IDENTIFIER_TOKEN = 8
    SEMICOLON_TOKEN = 9

    def __init__(self, expression):
        self.i = 0
        self.expression = ''.join(sentence.split())
        self.inp = ''
        self.last_val = None 
        self.last_id = ""

    def next_token(self):
        next()


        if is_digit():
            return get_number()

        elif self.inp == PERIOD:
            return PERIOD_TOKEN
        elif self.inp == SEMICOLON:
            return SEMICOLON_TOKEN
            
        elif self.inp == PLUS:
            return ADDOP

        elif self.inp == MINUS:
            return SUBOP

        elif self.inp == TIMES:
            return MULOP

        elif self.inp == DIVIDE:
            return DIVIDEOP

        elif is_letter():
            _str = get_string()
            if _str in KEYWORD:
                return KEYWORD_TOKEN

            else: 
                return IDENTIFIER_TOKEN

    def next(self):

        while self.i < len(self.expression) and sentence[self.i] == ' ':
            self.i = self.i + 1

        if self.i < len(self.expression):
            self.inp = self.expression[self.i]
        else:
            self.inp = '$'

        self.i = self.i + 1

    def is_digit():
        if self.inp in DIGIT:
            return True

    def is_letter():
        if self.inp in LETTER:
            return True

    def get_string():
        identifier = ""
        identifier = identifier+self.inp
        next()
        
        while is_letter() or is_digit():
            identifier = identifier + self.inp
            next()

        return identifier
    
    def get_number(self):
        res = 0
        res = int(self.inp)
        next()
        while is_digit():
            res = 10*res + int(self.inp)
            next()
        return res
