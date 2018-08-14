import yaml
import textwrap

import build_ast
import prolog_ast
import templates.default_templates


def load_yml(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)


def main():
    dat = load_yml('clk_gen.yml')
    prob = build_ast.ProbClkGen()
    prob.visit(dat)
    prob.fix_missing_ports()

    tpl = templates.default_templates.template_file(prob.top, prob.get_module_ast())
    txt = templates.default_templates.template_tostring(tpl)
    print(txt)


if __name__ == '__main__':
    main()