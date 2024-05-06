class WASM:
    WASM_BINARY_MAGIC = bytearray(b'\x00\61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.buffer = bytearray()
        return

    def wasm_header(self):
        self.buffer = self.WASM_BINARY_MAGIC+self.WASM_BINARY_VERSION


    def print_buffer(self):
        print(self.buffer)
        return
    