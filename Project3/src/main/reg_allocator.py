import Constant
import file
import sys

class register_allocator:

    def __init__(self):
        self.no_gpr = Constant.NO_OF_GPR
        self.phy_reg_start = Constant.PHY_REG_START
        self.vir_reg_start = Constant.NO_OF_GPR
        self.vir_reg_end = Constant.VIR_REG_END
        self.reg_alloacation = {}

    def next_phy_reg(self):
        # No more physical reg
        if self.phy_reg_start >= self.no_gpr:
            return -1

        reg_no = self.phy_reg_start
        self.phy_reg_start = self.phy_reg_start + 1

        return reg_no

    def next_vir_reg(self):
        # Unlimited Virtual Register
        reg_no = self.vir_reg_start
        self.vir_reg_start = self.vir_reg_start + 1

        return reg_no

    def get_phy_reg(self, excluded_registers: set):
        for i in range (self.phy_reg_start, self.no_gpr):
            if i not in excluded_registers:
                return i
            
        return NO_PHY_REG_AVAILABLE

    def get_vir_reg(self, excluded_registers: set):
        for i in range (self.vir_reg_start, self.vir_reg_end):
            if i not in excluded_registers:
                return i
    
        return NO_VIR_REG_AVAILABLE

    def allocate_reg(self, degree, excluded_registers: set):
        if degree > self.no_gpr:
            return self.get_vir_reg(excluded_registers)
        
        return self.get_phy_reg(excluded_registers)

    def deallocate_reg(self, reg_no):
        self.reg_array[reg_no] = 0
        return
        

class Graph:
    '''Used to represent interference of live variables'''
    def __init__(self, name):
        self.name = name
        # {ins_id: set(ins_ids)}
        self.graph = {}
        # {ins_id: Reg_no}
        self.color = {}
        self.color_name = ['red', 'green', 'blue', 'yellow', 'orange', "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", 
    "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown", 
    "burlywood", "cadetblue", "chartreuse"]

        self.dot_str = ""

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

    def sort_vertices_by_degree(self):
        # Calculate the degree of each node
        degrees = {node: len(neighbors) for node, neighbors in self.graph.items()}

        # Sort the nodes based on their degrees in descending order
        soreted_tuple = sorted(degrees.items(), key= lambda x: x[1], reverse=True)

        return soreted_tuple

    def color_graph(self, reg_allocator:register_allocator):
        stack = []
        sorted_nodes = self.sort_vertices_by_degree()
        
        for node, degree in sorted_nodes:
            # Initialize a set of colors used by neighboring nodes
            neighbor_colors = set()
            
            # Iterate over neighboring nodes and collect their colors
            for neighbor in self.graph[node]:
                if neighbor in self.color:
                    neighbor_colors.add(self.color[neighbor])

            color = reg_allocator.allocate_reg(degree, neighbor_colors)

            if color == (Constant.NO_PHY_REG_AVAILABLE or Constant.NO_VIR_REG_AVAILABLE):
                panic()
            
            self.color[node] = color

        return
    # def reduce_graph(self):

    def dot_node_style(self, node):
        style =f"{node}[label = {node}, fillcolor=\"{self.color_name[self.color[node]]}\", style=filled];\n"

        return style

    def dot(self):
        self.dot_str= ""
        self.node_style = ""
        printed_edge = set()

        for node in self.graph:
            self.node_style = self.node_style + self.dot_node_style(node)

            printed_edge.add(node)

            for i in self.graph[node]:
                if i in printed_edge: continue
                self.dot_str = self.dot_str + f"{node} -- {i};\n"
        
        self.dot_str= self. node_style + self.dot_str

        self.dot_str = "subgraph cluster_" + self.name + "{\n\tlabel="+ self.name+"\n"+ self.dot_str +"\n}"

        return self.dot_str

def panic():
    Constant.info("**Resource Exhausted\n")
    sys.exit(-1)

def build_interference_graph_cfg_list(cfg_list):
    dot_str = ""

    for cfg in cfg_list:
        graph = Graph(cfg.name)

        for id in cfg.tree:
            build_interference_graph(cfg.tree[id], graph)
        
        cfg.interference_graph = graph


def build_interference_graph(bb, graph):
    '''
    For single block
    live_var_set = {ins_id: {ins_id1, ins_id2, ..}}
    '''
    live_var_set = bb.live_var_set

    for i in live_var_set:
        for x in live_var_set[i]:
            graph.add_edge(i, x)

    return

def render_dot(cfg_list):
    dot_str = ""

    for cfg in cfg_list:
        dot_str = dot_str + cfg.interference_graph.dot()

    with open(file.get_file_path_without_extension()+"_inference.dot", "w") as f:
        graph_str = "graph G{\n"+ dot_str + "\n}"
        f.write(graph_str)
    
    return

def live_variable_analysis(cfg_list):
    for cfg in cfg_list:
        cfg.live_variable_analysis()

    build_interference_graph_cfg_list(cfg_list)
    allocate_register(cfg_list)


def allocate_register(cfg_list):
    reg_allocator = register_allocator()

    for cfg in cfg_list:
        interference_graph = cfg.interference_graph
        interference_graph.color_graph(reg_allocator)

    render_dot(cfg_list)