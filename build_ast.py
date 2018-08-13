import prolog_ast


class ClkGenVisitorBase:
    def visit(self, f):
        self.visit_top(f['Top'])

    def visit_top(self, top):
        pass

    def visit_ports(self, ports):
        for port in ports:
            self.visit_port(port.get('name'), port.get('mode'), port.get('comment'))

    def visit_port(self, name, mode, comment):
        pass

    def visit_clock_list(self, clock_list):
        for name, clock in clock_list:
            self.visit_clock(name, clock.get('mode'), clock.get('source'), clock.get('clk_cell'), clock.get('comment'))

    def visit_clock(self, name, mode, source, clk_cell, comment):
        pass

    def visit_custom_code(self, custom_code):
        pass