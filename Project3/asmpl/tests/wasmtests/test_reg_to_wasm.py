import unittest
import os

from asmpl.wasm import reg_to_wasm
from asmpl.wasm import format

def get_simple_register_allocation(ssa_value):
        reg_start = 0
        reg_allocation = {}

        for ssa in ssa_value:
            reg_allocation[ssa] = reg_start
            reg_start = reg_start + 1
        return reg_allocation

def get_cwd():
    path = os.path.realpath(__file__)
    dir_name = os.path.dirname(path)

    return dir_name

def compare_bytearray(arr1, arr2):
    l = min(len(arr1), len(arr2))

    for i in range(0, l):
        if arr1[i] != arr2[i]:
            print(f"Byte mismatch found at position {i}: {arr1[i]} != {arr2[i]}")
            return
 
def get_add_1_2_wasm():
    dir_name = get_cwd()
    path = os.path.join(dir_name, "add.wasm")
    with open(path, 'rb') as wasm_file:
        wasm_bytes = bytearray(wasm_file.read())

    return wasm_bytes

class TestRegToWasm(unittest.TestCase):
    def setUp(self):
        self.regtowasm = reg_to_wasm.get_reg_to_stack()

    def test_add_local_fun(self):
        foo = self.regtowasm.add_local_func(["a"], True)
        self.assertEqual(foo.params, [format.Types.i32.value])
        self.assertEqual(foo.results, [format.Types.i32.value])
        self.assertEqual(self.regtowasm.reg_to_var, {})
        self.assertEqual(self.regtowasm.cur_var_idx, 0)

        return 

    def test_add_print_instruction(self):
        self.regtowasm.add_local_func([], False)
        buffer = self.regtowasm.add_print_instruction()
        buffer1 = bytearray([format.Opcodes.call.value, 0])
        self.assertEqual(buffer, buffer1)

    def test_if_else(self):
        self.regtowasm.add_local_func("main", [], False)
        self.regtowasm.push_constant(1)
        self.regtowasm.push_constant(3)
        self.regtowasm.add_instruction("bgt")
        self.regtowasm.add_instruction("_if")
        self.regtowasm.add_instruction("void")
        self.regtowasm.add_instruction("")
        self.regtowasm.add_instruction()

    def test_add_smpl(self):
        # 1: assign(a)(#1)
        # 2. add(#1)(#2)
        # 3. assign(a)(2)
        # 4. write(2)
        # 5. end

        self.regtowasm.add_local_func("main", [], False)
        reg_alloacation = get_simple_register_allocation([2])
        self.regtowasm.push_constant(1)
        self.regtowasm.push_constant(2)
        self.regtowasm.add_instruction("add")
        self.regtowasm.save_to_reg(reg_alloacation[2])
        self.regtowasm.push_variable(reg_alloacation[2])
        self.regtowasm.add_print_instruction()
        self.regtowasm.append_func_to_module()
        buffer = self.regtowasm.emitter.encode_module()
        buffer1 = get_add_1_2_wasm()
        self.regtowasm.emitter.write_to_file(get_cwd()+"/new_add", buffer)

        compare_bytearray(buffer, buffer1)
        self.assertEqual(len(buffer), len(buffer1))
        self.assertEqual(buffer, buffer1)

if __name__== '__main__':

    unittest.main()