from format import Section, Opcodes
class Emitter:
    WASM_BINARY_MAGIC = bytearray(b'\x00\61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.buffer = bytearray()
        return

    def encode_header(self):
        return self.WASM_BINARY_MAGIC+self.WASM_BINARY_VERSION

    def encode_section(self, section_id):
        section_buffer = bytearray([section_id.value])
        section_buffer.append(0) # section size. Need to be filled later

        return section_buffer

    def add_result_type(self, rt:list):
        buffer = bytearray()
        buffer.append(len(rt))
        for r in rt:
            buffer.append(r)

        return buffer

    def add_function_type(self, params:list, results:list ):
        buffer = bytearray()
        buffer.append(0x60)
        buffer.extend(self.add_result_type(params))
        buffer.extend(self.add_result_type(results))

        return buffer

    def encode_function(self):
        pass

    def write_to_file(self, filename):
        with open(filename+".wasm", "wb") as f:
            f.write(self.buffer)
        
        return

    def print_buffer(self):
        # Print 4 bytes per line with index
        for i in range(0, len(self.buffer), 4):
            print(f"{i:04d}: {self.buffer[i:i+4]}")

        return
    