class Tokenizer:
    cur_token = 0
    DIGIT= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    KEYWORD = ["var", "computation"]
    PERIOD = '.'
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    LPAREN = '('
    RPAREN = ')'
    SEMICOLON = ';'
    ASSIGNMENT = '<'
    PERIOD_TOKEN = -1
    ADDOP = 1
    SUBOP = 2
    MULOP = 3
    DIVIDEOP = 4
    LPAREN_TOKEN = 5
    RPAREN_TOKEN = 6
    KEYWORD_COMPUTATION= 7
    IDENTIFIER_TOKEN = 8
    SEMICOLON_TOKEN = 9
    KEYWORD_VAR = 10
    ASSIGNOP = 11
    INTEGER = 12

    def __init__(self, sentence):
        self.i = 0
        self.sentence = sentence.strip()
        self.inp = ''
        self.last_val = None 
        self.last_id = ""

    def next_token(self):
        Tokenizer.cur_token = self.parse_token()
        self.skip_whitespace()

    def parse_token(self):
        self.next()


        if self.is_digit():
            self.last_val = self.get_number()
            return Tokenizer.INTEGER

        elif self.inp == Tokenizer.PERIOD:
            return Tokenizer.PERIOD_TOKEN
        elif self.inp == Tokenizer.SEMICOLON:
            return Tokenizer.SEMICOLON_TOKEN
            
        elif self.inp == Tokenizer.PLUS:
            return Tokenizer.ADDOP

        elif self.inp == Tokenizer.MINUS:
            return Tokenizer.SUBOP

        elif self.inp == Tokenizer.TIMES:
            return Tokenizer.MULOP

        elif self.inp == Tokenizer.DIVIDE:
            return Tokenizer.DIVIDEOP

        elif self.inp == Tokenizer.ASSIGNMENT:
            self.next() # <hyphen>
            return Tokenizer.ASSIGNOP

        elif self.inp == Tokenizer.LPAREN:
            return Tokenizer.LPAREN_TOKEN

        elif self.inp == Tokenizer.RPAREN:
            return Tokenizer.RPAREN_TOKEN

        elif self.is_letter():
            _str = self.get_string()
            if _str == "computation":
                return Tokenizer.KEYWORD_COMPUTATION

            elif _str == "var":
                return Tokenizer.KEYWORD_VAR

            else: 
                self.last_id = _str
                return Tokenizer.IDENTIFIER_TOKEN
        else:
            return Tokenizer.PERIOD_TOKEN

    def print_token(self):
        print("Token: " , Tokenizer.cur_token, "\n")

    def next(self):

        if self.i < len(self.sentence):
            self.inp = self.sentence[self.i]
        else:
            self.inp = '$'

        self.i = self.i + 1

    def skip_whitespace(self):
        while self.i < len(self.sentence) and self.sentence[self.i] == ' ':
            self.i = self.i + 1


    def is_digit(self):
        if self.inp in Tokenizer.DIGIT:
            return True

    def is_letter(self):
        if self.inp in Tokenizer.LETTER:
            return True

    def get_string(self):
        identifier = ""
        identifier = identifier+self.inp
        self.next()
        
        while self.is_letter() or self.is_digit():
            identifier = identifier + self.inp
            self.next()

        return identifier
    
    def get_number(self):
        res = 0
        res = int(self.inp)
        self.next()
        while self.is_digit():
            res = 10*res + int(self.inp)
            self.next()
        
        self.i = self.i-1
        return res
