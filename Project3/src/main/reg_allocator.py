class register_allocator:

    def __init__(self):
        self.reg_array= [0]*30

    '''
        Find and return the register number of 
        an emtpy register
    '''
    def walk(self):
        for i in range(1, 30):
            if self.reg_array[i] == 0:
                return i

    def allocate_reg(self):
        reg_no = self.walk()
        self.reg_array[reg_no] = 1
        return reg_no

    def deallocate_reg(self, reg_no):
        self.reg_array[reg_no] = 0
        return
        

def live_variable_analysis(cfg_list):
    for cfg in cfg_list:
        cfg.live_variable_analysis()