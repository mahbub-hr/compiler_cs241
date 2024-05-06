class Emitter:
    WASM_BINARY_MAGIC = bytearray(b'\x00\61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.buffer = bytearray()
        return

    def header(self):
        self.buffer = self.WASM_BINARY_MAGIC+self.WASM_BINARY_VERSION


    def print_buffer(self):
        # Print 4 bytes per line with index
        for i in range(0, len(self.buffer), 4):
            print(f"{i:04d}: {self.buffer[i:i+4]}")

        return
    