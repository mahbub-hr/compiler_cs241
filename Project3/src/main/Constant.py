DEBUG = True
UNDEFINE = "undefine"
ALREADY_DEFINE = "already defined at line #"
UNRECOG_SYM = "unrecognize symbol"
def UNEXPECTED_TOKEN(expected, unexpected):
    return f"expected {expected} but found {unexpected}"
