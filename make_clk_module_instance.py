import prolog_ast


def make_clk2_swi(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'clk2_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['src0_clki', pin.get('src0_clki', source[0])],
        ['src0_rst_n', pin.get('src0_rst_n', 'cmu_rst_n')],
        ['src1_clki', pin.get('src1_clki', source[1])],
        ['src1_rst_n', pin.get('src1_rst_n', 'cmu_rst_n')],
        ['sel', pin.get('sel', '_'.join(['para', name, 'sel_i']))]
    ]
    module_instance_name = '_'.join(['inst_cksw', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_clk3_swi(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'clk3_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['src0_clki', pin.get('src0_clki', source[0])],
        ['src0_rst_n', pin.get('src0_rst_n', 'cmu_rst_n')],
        ['src1_clki', pin.get('src1_clki', source[1])],
        ['src1_rst_n', pin.get('src1_rst_n', 'cmu_rst_n')],
        ['src2_clki', pin.get('src2_clki', source[2])],
        ['src2_rst_n', pin.get('src2_rst_n', 'cmu_rst_n')],
        ['sel', pin.get('sel', '_'.join(['para', name, 'sel_i[1:0]']))]
    ]
    module_instance_name = '_'.join(['inst_cksw', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_clk4_swi(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'clk4_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['src0_clki', pin.get('src0_clki', source[0])],
        ['src0_rst_n', pin.get('src0_rst_n', 'cmu_rst_n')],
        ['src1_clki', pin.get('src1_clki', source[1])],
        ['src1_rst_n', pin.get('src1_rst_n', 'cmu_rst_n')],
        ['src2_clki', pin.get('src2_clki', source[2])],
        ['src2_rst_n', pin.get('src2_rst_n', 'cmu_rst_n')],
        ['src3_clki', pin.get('src3_clki', source[3])],
        ['src3_rst_n', pin.get('src3_rst_n', 'cmu_rst_n')],
        ['sel', pin.get('sel', '_'.join(['para', name, 'sel_i[1:0]']))]
    ]
    module_instance_name = '_'.join(['inst_cksw', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_clk_div(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'clk_div')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    div_bw = int(param['DIV_BW'])
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['upd', pin.get('upd', '_'.join(['para', name, 'upd_i']))],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['high_th', pin.get('high_th', '_'.join(['para', name, 'th_i['+str(div_bw-1)+':0]']))],
        ['div', pin.get('div', '_'.join(['para', name, 'div_i['+str(div_bw-1)+':0]']))]
    ]
    module_instance_name = '_'.join(['inst_cdiv', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_gate_div(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'gate_div')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    div_bw = int(param['DIV_BW'])
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['upd', pin.get('upd', '_'.join(['para', name, 'upd_i']))],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['div_pat', pin.get('div_pat', '_'.join(['para', name, 'pat_i['+str(div_bw-1)+':0]']))]
    ]
    module_instance_name = '_'.join(['inst_gdiv', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_clk_gate(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    param = cell['Param']
    pin = cell.get('Pin', {})
    assert(cell['Cell'] == 'clk_gate')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    ports = [
        '// outputs',
        ['clkout', pin.get('clkout', name)],
        '// inputs',
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['tmode', pin.get('tmode', 'test_mode_i')]
    ]
    module_instance_name = '_'.join(['inst_gdiv', name])
    return prolog_ast.ast_module_instance(cell['Cell'], param.items(), module_instance_name, ports, comment)


def make_assign(name, mode, source, clk_cell, comment):
    cell = clk_cell[0]
    assert(cell['Cell'] == 'assign')
    return prolog_ast.ast_extra(['assign', name, '=', source[0], ';'])


f_clk_module_dict = {
    'clk2_swi': make_clk2_swi,
    'clk3_swi': make_clk3_swi,
    'clk4_swi': make_clk4_swi,
    'clk_div': make_clk_div,
    'gate_div': make_gate_div,
    'clk_gate': make_clk_gate,
    'assign': make_assign
}


def make_clk_module_instance(name, mode, source, clk_cell, comment):
    if len(clk_cell) == 1:
        f_cell_module_instance = f_clk_module_dict[clk_cell[0]['Cell']]
        return f_cell_module_instance(name, mode, source, clk_cell, comment)
    else:
        pass
