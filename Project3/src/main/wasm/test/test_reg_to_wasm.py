import unittest
import reg_to_wasm

def get_simple_register_allocation(ssa_value):
        reg_start = 0
        reg_allocation = {}

        for ssa in ssa_value:
            reg_allocation[ssa] = reg_start
            reg_start = reg_start + 1
        return reg_allocation

class TestRegToWasm(unittest.TestCase):
    def setUp(self):
        self.regtowasm = reg_to_wasm.get_reg_to_stack()

    def test_hello_smpl(self):
        # 1: assign(a)(#1)
        # 2. add(a)(#2)
        # 3. assign(a)(2)
        # 4. write(2)
        # 5. end

        reg_alloacation = get_simple_register_allocation([2])
        self.regtowasm.push_constant(1)
        self.regtowasm.push_constant(2)
        self.regtowasm.push_variable(reg_alloacation[2])
        self.regtowasm.add_print_instruction()

if __name__== '__main__':

    unittest.main()