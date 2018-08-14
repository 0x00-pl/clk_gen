import textwrap
import prolog_ast

sep1 = '//----------------------------------------------------------------------------------------------'
sep2 = '//=============================================================================================='
indentation = '    '


def template_tostring(tpl):
    return '\n'.join([
        ' '.join([str(item) for item in line])
        for line in tpl
    ])


def format_lines(lines:[list]):
    max_arr = {}
    for line in lines:
        for item,i in zip(line, range(len(line))):
            max_arr[i] = max(max_arr.get(i, float('-Inf')), len(item))

    return [[item+' '*(max_arr[i]-len(item))
             for item,i in zip(line, range(len(line)))]
            for line in lines]


def inc_indentation(lines:list):
    def indentation_aux(line):
        if isinstance(line, str):
            return indentation + line
        elif isinstance(line, list):
            return [indentation, *line]
        else:
            return line

    return [indentation_aux(line) for line in lines]


def template_header(env:dict):
    description = str(env.get('description', ''))
    description_lines = textwrap.wrap('    '+description)
    description_lines = ['//   ' + line for line in description_lines]

    ret = [sep2]
    ret.extend('''
    // Project    : {project}
    // Owner      : {owner}
    // File Name  : {module}.v
    // Module Name: {module}
    '''.format(**env).split('\n'))
    ret.append(sep1)
    ret.append('// Description:')
    ret.extend(description_lines)
    ret.append(sep2)
    ret.append('`timescale  1ns / 1ps')
    return [line.strip() for line in ret if line.strip!='']


# def template_extra(ast, text:str):
#     assert(ast == 'extra')
#     lines = ['//   ' + line for line in textwrap.wrap(text)]
#     return [sep2, *lines, sep2]


def template_port_decl(ast, direction: str, ty='wire', bw:int=1, name: str='noName', comment=None):
    assert(ast == 'port_decl')
    ty = ty+' ['+str(bw-1)+':0]' if bw > 1 else ty
    ret = [direction, ty, name+',']
    return [*ret, '// '+comment] if comment else ret


def template_local_decl(ast, ty:str='wire', bw:int=1, name: str='noName', comment=None):
    assert(ast == 'local_decl')
    ty = ty+' ['+str(bw-1)+':0]' if bw > 1 else ty
    return [ty, name+',', '// '+comment] if comment else [ty, name+',']


def template_module_instance(ast, ty, args, name, port_output_list, port_input_list, comment=None):
    assert(ast == 'module_instance')
    ret = [['// '+comment]] if comment else []
    module_instance_arguments = '#('+', '.join(template_kv_inline(args))+')'
    ret.append([ty, module_instance_arguments, name])
    ret.append(['('])
    module_instance_ports = template_kv(port_output_list)
    ret.extend(inc_indentation(format_lines(module_instance_ports)))
    module_instance_ports = template_kv(port_input_list)
    ret.extend(inc_indentation(format_lines(module_instance_ports)))
    ret.append([');'])
    return ret


def template_module(ast, name, ports, locals, module_instances, extra=[], comment=None):
    assert(ast == 'module')
    ret = []
    if comment:
        if isinstance(comment, str):
            ret.append(['// '+comment])
        else:
            ret.extend(comment)

    ret.append(['module', name])
    ret.append(['('])
    module_ports = [template_port_decl(*port) for port in ports]
    ret.extend(inc_indentation(format_lines(module_ports)))
    ret.append([');'])
    ret.append([])
    module_locals = [template_local_decl(*loc) for loc in locals]
    ret.extend(inc_indentation(format_lines(module_locals)))
    ret.append([])
    ret.extend(extra)

    module_module_instances = [template_module_instance(*modi) for modi in module_instances]
    for item in module_module_instances:
        ret.extend(inc_indentation(item))
        ret.append([])

    ret.append(['endmodule', '// '+name])
    ret.append([])
    return ret


def template_kv_inline(args):
    def kv_inline_aux(kv):
        ast, k, v, *tail = kv
        assert(ast == 'kv')
        return '.{}({})'.format(k, v)

    return [kv_inline_aux(line) for line in args]


def template_kv(args):
    def kv_aux(line):
        ast, *tail = line
        if ast == 'kv':
            k, v, comment = tail
            return ['.'+k, '(', v, '),', '// '+comment] if comment else ['.'+k, '(', v, '),']
        else:
            return tail

    return [kv_aux(line) for line in args]









