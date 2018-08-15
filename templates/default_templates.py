import textwrap

sep1 = '//----------------------------------------------------------------------------------------------'
sep2 = '//=============================================================================================='
indentation = '    '


def template_tostring(tpl):
    return '\n'.join([
        ' '.join([str(item) for item in line])
        for line in tpl
    ])


def format_lines(lines):
    max_arr = {}
    for line in lines:
        for item,i in zip(line, range(len(line))):
            max_arr[i] = max(max_arr.get(i, float('-Inf')), len(item))

    return [[item+' '*(max_arr[i]-len(item))
             for item,i in zip(line, range(len(line)))]
            for line in lines]


def inc_indentation(lines):
    def indentation_aux(line):
        if isinstance(line, str):
            return indentation + line
        elif isinstance(line, list):
            return [indentation, *line]
        else:
            return line

    return [indentation_aux(line) for line in lines]


def template_header(env):
    description = str(env.get('Description', ''))
    description_lines = textwrap.wrap('    '+description)
    description_lines = [['//   ' + line] for line in description_lines]

    ret = [[sep2]]
    ret.extend(format_lines([
        ['// Project', ':', env['Project']],
        ['// Owner', ':', env['Owner']],
        ['// File Name', ':', env['Module']+'.v'],
        ['// Module Name', ':', env['Module']]
    ]))
    ret.append([sep1])
    ret.append(['// Description:'])
    ret.extend(description_lines)
    ret.append([sep2])
    ret.append(['`timescale  1ns / 1ps'])
    ret.append([])
    return ret


def template_extra(ast, *content):
    assert(ast == 'extra')
    return list(content)


def template_port_decl(ast, direction, ty='wire', bw=1, name='noName', comment=None):
    assert(ast == 'port_decl')
    ty = ty+' ['+str(bw-1)+':0]' if int(bw) > 1 else ty
    ret = [direction, ty, name+',']
    return [*ret, '// '+comment] if comment else ret


def template_local_decl(ast, ty='wire', bw=1, name='noName', comment=None):
    assert(ast == 'local_decl')
    ty = ty+' ['+str(bw-1)+':0]' if int(bw) > 1 else ty
    return [ty, name+',', '// '+comment] if comment else [ty, name+',']


def template_module_instance(ast, ty, args, name, port_output_list, port_input_list, comment=None):
    assert(ast == 'module_instance')
    ret = [['// '+comment]] if comment else []
    module_instance_arguments = '#('+', '.join(template_kv_inline(args))+')'
    ret.append([ty, module_instance_arguments, name])
    ret.append(['('])

    # format
    module_instance_port_output = template_kv(port_output_list)
    module_instance_port_input = template_kv(port_input_list)
    output_len = len(module_instance_port_output)
    input_len = len(module_instance_port_input)
    ports = []
    ports.extend(module_instance_port_output)
    ports.extend(module_instance_port_input)
    ports.append(['x'*40, '(', 'x'*40, '),'])
    ports = format_lines(ports)
    # remove last ','
    if ports[-1][-1].endswith(','):
        ports[-1][-1] = ports[-1][-1][:-1]
    elif ports[-1][-2].endswith(','):
        ports[-1][-2] = ports[-1][-2][:-1]
    module_instance_port_output = ports[:output_len]
    module_instance_port_input = ports[output_len:output_len+input_len]

    ret.extend(inc_indentation([['// Outputs']]))
    ret.extend(inc_indentation(format_lines(module_instance_port_output)))
    ret.extend(inc_indentation([['// Inputs']]))
    ret.extend(inc_indentation(format_lines(module_instance_port_input)))
    ret.append([');'])
    return ret


def template_module(ast, name, ports, locs, module_instances, extra=None, comment=None):
    extra = extra or []
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
    ret.extend(inc_indentation([
        [sep2],
        ['// declaration of internal wires and registers'],
        [sep2]
    ]))
    module_locals = [template_local_decl(*loc) for loc in locs]
    ret.extend(inc_indentation(format_lines(module_locals)))
    ret.append([])
    if len(extra) != 0:
        ret.extend(inc_indentation([
            [sep2],
            ['// module main RTL code starts here!'],
            [sep2]
        ]))
        ret.extend(inc_indentation([template_extra(*line) for line in extra]))
        ret.append([])

    module_module_instances = [template_module_instance(*modi) for modi in module_instances]
    for item in module_module_instances:
        ret.extend(inc_indentation(item))
        ret.append([])

    ret.append(['endmodule', '// '+name])
    ret.append([])
    return ret


def template_file(top, module):
    ret = []
    ret.extend(template_header(top))
    ret.extend(template_module(*module))
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









