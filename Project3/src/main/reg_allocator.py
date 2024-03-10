import Constant

class register_allocator:

    def __init__(self, cfg_list):
        self.cfg_list = cfg_list
        self.live_variable_analysis()
        self.gpr = Constant.NO_OF_GPR
        self.build_interference_graph_cfg_list()

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
        
    def live_variable_analysis(self):
        for cfg in self.cfg_list:
            cfg.live_variable_analysis()

    def build_interference_graph_cfg_list(self):
        for cfg in self.cfg_list:
            self.build_interference_graph_cfg(cfg)
    
    def build_interference_graph_cfg(self, cfg):

        for id in cfg.tree:
            self.build_interference_graph(cfg.tree[id])

    def build_interference_graph(self, bb):
        '''
        For single block
        live_var_set = {ins_id: {ins_id1, ins_id2, ..}}
        '''
        live_var_set = bb.live_var_set
        graph = Graph()

        for i in live_var_set:
            for x in live_var_set[i]:
                graph.add_edge(i, x)

        bb.interference_graph = graph

        return



class Graph:
    '''Used to represent interference of live variables'''
    def __init__(self):
        # {ins_id: set(ins_ids)}
        self.graph = {}

    def add_edge(self, node1, node2):
        if node1 == node2:
            return
        
        self.add_edge_to_graph(node1, node2)
        self.add_edge_to_graph(node2, node1)
    
    def add_edge_to_graph(self, node1, node2):
        if node1 in self.graph:
            self.graph[node1].add(node2)
        
        else:
            self.graph[node1] = {node2}
