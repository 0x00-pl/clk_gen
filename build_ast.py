import prolog_ast
import make_clk_module_instance


class ClkGenVisitorBase:
    def visit(self, f):
        self.visit_top(f['Top'])
        self.visit_ports(f['Ports'])
        self.visit_clock_list(f['Clock_List'].items())
        self.visit_custom_code(f['Custom_Code'])

    def visit_top(self, top):
        pass

    def visit_ports(self, ports):
        for port in ports:
            self.visit_port(port.get('Name'), port.get('Mode'), port.get('Comment'))

    def visit_port(self, name, mode, comment):
        pass

    def visit_clock_list(self, clock_list):
        for name, clock in clock_list:
            self.visit_clock(name, clock.get('Mode'), clock.get('Source'), clock.get('ClockCell'), clock.get('Comment'))

    def visit_clock(self, name, mode, source, clk_cell, comment):
        pass

    def visit_custom_code(self, custom_code):
        pass


class ProbClkGen(ClkGenVisitorBase):
    def __init__(self):
        self.name = None
        self.port_list = []
        self.local_list = []
        self.module_instance_list = []
        self.extra = []
        self.comment = None
        self.top = None

    def visit_top(self, top):
        self.name = top['Module']
        self.top = top

    def visit_port(self, name, mode, comment):
        direction = mode.get('direction', 'node')
        ty = mode.get('type', 'wire')
        bw = mode.get('width', 1)
        if direction in ('input', 'output'):
            port = prolog_ast.ast_port_decl(direction, ty, bw, name, comment)
            self.port_list.append(port)
        elif direction == 'node':
            loc = prolog_ast.ast_local_decl(ty, bw, name, comment)
            self.local_list.append(loc)

    def visit_clock(self, name, mode, source, clk_cell, comment):
        module_instances = make_clk_module_instance.make_clk_module_instance(name, mode, source, clk_cell, comment)
        if module_instances[0] == 'module_instance':
            self.module_instance_list.append(module_instances)
        elif module_instances[0] == 'extra':
            self.extra.append(module_instances)
        elif module_instances[0][0] == 'module_instance':
            self.module_instance_list.extend(module_instances)

        self.fix_module_instances_output_port(name, mode, comment)

    def fix_module_instances_output_port(self, name, mode, comment):
        direction = mode.get('direction', 'node')
        ty = mode.get('type', 'wire')
        bw = mode.get('DIV_BW', '1')
        if direction == 'output':
            port = prolog_ast.ast_port_decl(direction, ty, bw, name, comment)
            self.port_list.append(port)
        else:
            loc = prolog_ast.ast_local_decl(ty, bw, name, comment)
            self.local_list.append(loc)

    def fix_missing_ports(self):
        for modins in self.module_instance_list:
            ast, ty, params, name, ports, comment = modins
            assert(ast == 'module_instance')



