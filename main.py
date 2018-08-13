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
    s = dat['Top'][3]['description']
    l = textwrap.wrap(s, 40)
    return 0


def main2():
    mi = prolog_ast.ast_module_instance(
        'Mod1',
        [
            prolog_ast.ast_kv('arg1', 'value1'),
            prolog_ast.ast_kv('arg2', 'value2')
        ],
        'mod_ins_1',
        [
            prolog_ast.ast_kv('clk', 'pll_0_clk', '26M clk'),
            prolog_ast.ast_kv('switch', 'pll_switchers[2:0]')
        ],
        'some comment for mod instance'
    )
    m = prolog_ast.ast_module(
        'clk_gen_main',
        [
            prolog_ast.ast_port_decl('input', 'wire', 1, 'clk_26m', 'main input clk'),
            prolog_ast.ast_port_decl('input', 'wire', 10, 'clk_switcher')
        ],
        [
            prolog_ast.ast_local_decl('wire', 1, 'sys_src0_clk', 'temp clk 0'),
            prolog_ast.ast_local_decl('wire', 1, 'sys_src100_clk', 'temp clk 100'),
        ],
        [mi],
        [],
        'comment of clk_gen_main'
    )
    tpl = templates.default_templates.template_module(
        *m
    )

    txt = templates.default_templates.template_tostring(tpl)

    print(txt)


def main3():
    dat = load_yml('clk_gen.yml')
    prob = build_ast.ProbClkGen()
    prob.visit(dat)


if __name__ == '__main__':
    main3()