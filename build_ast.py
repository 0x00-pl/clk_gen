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
            self.visit_port(port.get('name'), port.get('mode'), port.get('comment'))

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
        self.module_instance_list = []

    def visit_clock(self, name, mode, source, clk_cell, comment):
        module_instances = make_clk_module_instance.make_clk_module_instance(name, mode, source, clk_cell, comment)
        if not isinstance(module_instances, list):
            self.module_instance_list.append(module_instances)
        else:
            self.module_instance_list.extend(module_instances)