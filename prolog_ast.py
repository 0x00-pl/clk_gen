
def ast_extra(text):
    return ['extra', text]


def ast_port_decl(direction: str, ty='wire', bw:int=1, name: str='noName', comment=None):
    return ['port_decl', direction, ty, bw, name, comment]


def ast_local_decl(ty='wire', bw:int=1, name: str='noName', comment=None):
    return ['local_decl', ty, bw, name, comment]


def ast_module_instance(ty, args, name, ports, comment=None):
    return ['module_instance', ty, args, name, ports, comment]


def ast_kv(name, value, comment=None):
    return ['kv', name, value, comment]


def ast_module(name, ports, locals, module_instances, extra=[], comment=None):
    return ['module', name, ports, locals, module_instances, extra, comment]













