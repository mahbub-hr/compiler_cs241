class DLX:
    @staticmethod
    def code_F1(opcode, a, b, c):
        ins = (opcode << 26)|(a<<21)|(b<<16)| (c&0x000FFFF)
        return

    @staticmethod
    def code_F2(opcode, a, b, c):
        ins = (opcode << 26)|(a<<21)|(b<<16)| (c&0x00001F)
        return