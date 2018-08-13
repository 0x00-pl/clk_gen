
def ast_extra(text):
    return ['extra', text]


def ast_port_decl(direction: str, ty='wire', bw:int=1, name: str='noName', comment=None):
    return ['port_decl', direction, ty, bw, name, comment]


def ast_local_decl(ty='wire', bw:int=1, name: str='noName', comment=None):
    return ['local_decl', ty, bw, name, comment]


def ast_module_instance(ty, args, name, ports, comment=None):
    def kv_or_comment(line):
        if len(line) >= 3:
            return ast_kv(line[0], line[1], (line[2] if len(line)>2 else None))
        else:
            return [line]

    return ['module_instance', ty, [ast_kv(k, v) for k, v in args], name, [kv_or_comment(line) for line in ports], comment]


def ast_kv(name, value, comment=None):
    return ['kv', name, value, comment]


def ast_module(name, ports, locs, module_instances, extra=None, comment=None):
    return ['module', name, ports, locs, module_instances, extra if extra else [], comment]












