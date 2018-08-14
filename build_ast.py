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
            for mi in module_instances:
                ast, ty, args, name, ports_output, ports_input, comment = mi
                for port_kv in ports_output:
                    ast, k, v, p_comment = port_kv
                    bw = 1
                    if v.find('[') == -1:
                        name = v
                    else:
                        name, bw_ref_1 = v.split('[')
                        shi, slo = bw_ref_1[:-1].split(':')
                        bw = int(shi) - int(slo) + 1

                    if not self.exist_in_ports_and_locals(v):
                        loc = prolog_ast.ast_local_decl('wire', bw, name, p_comment)
                        self.local_list.append(loc)

        self.fix_module_instances_output_port(name, mode, comment)

    def fix_module_instances_output_port(self, name, mode, comment):
        direction = mode.get('direction', 'node')
        name = name+'_o' if direction == 'output' else name
        ty = mode.get('type', 'wire')
        bw = mode.get('DIV_BW', '1')
        if direction == 'output':
            port = prolog_ast.ast_port_decl(direction, ty, bw, name, comment)
            self.port_list.append(port)
        else:
            loc = prolog_ast.ast_local_decl(ty, bw, name, comment)
            self.local_list.append(loc)

    def exist_in_ports_and_locals(self, target_name):
        for item in self.port_list:
            ast, direction, ty, bw, name, comment = item
            if name == target_name:
                return True

        for item in self.local_list:
            ast, ty, bw, name, comment = item
            if name == target_name:
                return True

        return False

    def fix_missing_ports(self):
        for modins in self.module_instance_list:
            ast, ty, params, name, port_output, port_input, m_comment = modins
            assert(ast == 'module_instance')
            for port_i in port_input:
                ast, k, v, p_comment = port_i
                bw = 1
                if v.find('[') == -1:
                    name = v
                else:
                    name, bw_ref_1 = v.split('[')
                    shi, slo = bw_ref_1[:-1].split(':')
                    bw = int(shi) - int(slo) + 1

                if not self.exist_in_ports_and_locals(v):
                    port = prolog_ast.ast_port_decl('input', 'wire', bw, name, p_comment)
                    self.port_list.append(port)

    def get_module_ast(self):
        return prolog_ast.ast_module(self.name, self.port_list, self.local_list, self.module_instance_list, self.extra, self.comment)

