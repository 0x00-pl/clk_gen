def ast_extra(*content):
    return ['extra', *content]


def ast_port_decl(direction, ty='wire', bw=1, name='noName', comment=None):
    return ['port_decl', direction, ty, bw, name, comment]


def ast_local_decl(ty='wire', bw=1, name='noName', comment=None):
    return ['local_decl', ty, bw, name, comment]


def ast_module_instance(ty, args, name, ports_output, ports_input, comment=None):
    return [
        'module_instance',
        ty, [ast_kv(k, v) for k, v in args], name,
        [ast_kv(*item) for item in ports_output],
        [ast_kv(*item) for item in ports_input],
        comment
    ]


def ast_kv(name, value, comment=None):
    return ['kv', name, value, comment]


def ast_module(name, ports, locs, module_instances, extra=None, comment=None):
    return ['module', name, ports, locs, module_instances, extra if extra else [], comment]












