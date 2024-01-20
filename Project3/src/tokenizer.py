cur_token=None
DIGIT= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
KEYWORD = ["var", "computation"]
PERIOD = -1
ADDOP = 1
SUBOP = 2
MULOP = 3
DIVIDEOP = 4
LPAREN = 5
RPAREN = 6
COMPUTATION= 7
IDENTIFIER = 8
SEMICOLON = 9
VAR = 10
ASSIGNOP = 11
INTEGER = 12
LSQR = 13
RSQR = 14
LCURL = 15
RCURL = 16
COMMA = 17
EQOP = 18
NOTEQOP = 19
LEQOP = 20
GEQOP = 21
LTOP = 22
GTOP = 23
LET = 24
CALL = 25
IF = 26
THEN = 27
ELSE = 28
FI = 29
WHILE = 30
DO = 31
OD = 32
RETURN = 33
ARRAY = 34
VOID = 35
FUNCTION = 36
MAIN = 37
line_count = 1
char_at_line = 0

class Tokenizer:
    def __init__(self, sentence):
        global cur_token
        cur_token = -1
        self.i = -1 
        self.sentence = sentence.strip()
        self.inp = ''
        self._str = ""
        self.last_val = None 
        self.last_id = ""

    def next_token(self):
        global cur_token
        cur_token = self.parse_token()
        # print(cur_token, "\n")

    def parse_token(self):
        self.next()
        self.skip_whitespace()

        if self.is_digit():
            self.last_val = self.get_number()
            return INTEGER

        elif self.match('['):
            return LSQR
        
        elif self.match(']'):
            return RSQR

        elif self.match('{'):
            return LCURL
        
        elif self.match('}'): return RCURL

        elif self.match(','): return COMMA

        elif self.match('.'):
            return PERIOD

        elif self.match(';'):
            return SEMICOLON
            
        elif self.match('+'):
            return ADDOP

        elif self.match('-'):
            return SUBOP

        elif self.match('*'):
            return MULOP

        elif self.match('/'):
            return DIVIDEOP

        elif self.match('='):
            self.next()
            if not match('='):
                error("Expected Relational Equality sign")
            return EQOP

        elif self.match('!'):
            return NOTEQOP

        elif self.match('<'):
            self.next()
            if match('-'):
                return ASSIGNOP

            elif match('='):
                return LEQOP
            
            else:
                self.prev()
                return LTOP
        
        elif self.match('>'):
            self.next()

            if match('='):
                return GEQOP
            else:
                self.prev()
                return GTOP
        
        elif self.match('('):
            return LPAREN

        elif self.match(')'):
            return RPAREN

        elif self.is_letter():
            self._str = self.get_string()
            if self.match_str("computation"):
                return COMPUTATION

            elif self._str == "var":
                return VAR
            elif self.match_str("let"):
                return LET

            elif self.match_str("call"):
                return CALL

            elif self.match_str("if"):
                return IF

            elif self.match_str("then"):
                return THEN
            
            elif self.match_str("else"):
                return ELSE
            
            elif self.match_str("fi"):
                return FI
            
            elif self.match_str("while"):
                return WHILE
            
            elif self.match_str("do"):
                return DO
            
            elif self.match_str("od"):
                return OD
            
            elif self.match_str("return"):
                return RETURN

            elif self.match_str("var"):
                return VAR

            elif self.match_str("array"):
                return ARRAY
            
            elif self.match_str("void"):
                return VOID

            elif self.match_str("function"):
                return FUNCTION
            
            elif self.match_str("main"):
                return MAIN
            else: 
                self.last_id = self._str
                return IDENTIFIER
        else:
            return PERIOD

    def print_token(self):
        print("Token: " , cur_token, "\n")

    def next(self):
        self.i = self.i + 1
        if self.i < len(self.sentence):
            self.inp = self.sentence[self.i]
        else:
            self.inp = '$'

    def prev(self):
        if self.i > 0:
            self.i = self.i - 1
            self.inp = self.sentence[self.i]

    def skip_whitespace(self):
        global line_count

        while self.inp in [' ', '\n', '\t'] and self.inp != '$':
            if self.inp == ' ':
                self.next()
                
            elif self.inp == '\n':
                line_count  = line_count + 1
                print("<NEWLINE>: ", line_count, "\n")
                self.next()

            else:
                return
        
    def match(self, _char):
        return self.inp == _char

    def match_str(self, str2):
        return self._str == str2

    def is_digit(self):
        if self.inp in DIGIT:
            return True

    def is_letter(self):
        if self.inp in LETTER:
            return True

    def get_string(self):
        identifier = ""
        identifier = identifier+self.inp
        self.next()
        
        while self.is_letter() or self.is_digit():
            identifier = identifier + self.inp
            self.next()

        self.prev()

        return identifier
    
    def get_number(self):
        res = 0
        res = int(self.inp)
        self.next()
        while self.is_digit():
            res = 10*res + int(self.inp)
            self.next()
        
        self.prev()

        return res

    def error(msg):
        # print(msg, "\n")
        raise Exception(msg+"\n")
