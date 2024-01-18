

class symbol_info:
    def __init__(self, kind, val, addr, regno):
        self.kind = kind
        self.val = val
        self.addr = addr
        self.regno = regno

class table:
    def __init__(self):
        self.table = {}
        pass

    def error(self, msg):
        print(msg, "\n")
        raise Exception("Error")

    def insert(self, identifier, value):
        if identifier in self.table:
            error("Already defined")

        self.table[identifier] = value

    def update(self, identifier, value):
        if identifier in self.table:
            self.table[identifier] = value

        else:
            error(identifier + " Not Found")

    def remove(self, identifier):
        if identifier in self.table:
            del self.table[identifier]
        
    def get_val(self, identifier):
        return self.table[identifier]