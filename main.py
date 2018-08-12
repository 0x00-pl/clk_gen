import yaml
import textwrap
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
        [prolog_ast.ast_kv('arg1', 'value1')],
        'mod_ins_1',
        [prolog_ast.ast_kv('clk', 'pll_0_clk', '26M clk')],
        'some comment for mod instance'
    )
    tpl = templates.default_templates.template_module_instance(
        *mi
    )

    txt = templates.default_templates.template_tostring(tpl)

    print(txt)


if __name__ == '__main__':
    main2()