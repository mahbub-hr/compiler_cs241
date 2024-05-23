def read_wasm_and_write_info(input_filename, output_filename):
    # Open the WebAssembly (WASM) file and the output text file
    with open(input_filename, 'rb') as wasm_file, open(output_filename, 'w') as info_file:
        # Read the magic number and version
        magic_number = wasm_file.read(4)
        version = wasm_file.read(4)

        # Write the magic number and version to the info file
        info_file.write(f"0000000: {magic_number.hex()}             ; WASM_BINARY_MAGIC\n")
        info_file.write(f"0000004: {version.hex()}                  ; WASM_BINARY_VERSION\n")