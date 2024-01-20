DEBUG = True
UNDEFINE_VAR = "variable undefine"
ALREADY_DEFINE = "already defined at line #"
def UNEXPECTED_TOKEN(expected, unexpected):
    return f"expected {expected} but found {unexpected}"
