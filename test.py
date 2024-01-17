class Parser:
    def __init__(self, input_string):
        self.tokens = input_string.split()
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def match(self, expected):
        if self.current_token == expected:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {expected}, but found {self.current_token}")

    def letter(self):
        if self.current_token.isalpha() and len(self.current_token) == 1:
            self.match(self.current_token)
        else:
            raise SyntaxError("Expected a single letter")

    def digit(self):
        if self.current_token.isdigit() and len(self.current_token) == 1:
            self.match(self.current_token)
        else:
            raise SyntaxError("Expected a single digit")

    def identifier(self):
        self.letter()
        while self.current_token and (self.current_token.isalpha() or self.current_token.isdigit()):
            self.match(self.current_token)

    def number(self):
        self.digit()
        while self.current_token and self.current_token.isdigit():
            self.match(self.current_token)

    def factor(self):
        if self.current_token.isalpha():
            self.identifier()
        elif self.current_token.isdigit():
            self.number()
        elif self.current_token == "(":
            self.match("(")
            self.expression()
            self.match(")")
        else:
            raise SyntaxError("Unexpected token in factor")

    def term(self):
        self.factor()
        while self.current_token in {"*", "/"}:
            self.match(self.current_token)
            self.factor()

    def expression(self):
        self.term()
        while self.current_token in {"+", "-"}:
            self.match(self.current_token)
            self.term()

    def computation(self):
        self.match("computation")
        while self.current_token == "var":
            self.match("var")
            self.identifier()
            self.match("<-")
            self.expression()
            self.match(";")
        while self.current_token == ";":
            self.match(";")
            self.expression()
        self.match(".")

# Example usage:
input_string = "computation var x <- 2 + 3 ; y <- x * 4 ; 3 + y ."
parser = Parser(input_string)
parser.computation()
print("Parsing successful.")
