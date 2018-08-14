import prolog_ast


def make_clk2_swi(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'clk2_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['src0_clki', pin.get('src0_clki', source[0])],
        ['src0_rst_n', pin.get('src0_rst_n', 'cmu_rst_n')],
        ['src1_clki', pin.get('src1_clki', source[1])],
        ['src1_rst_n', pin.get('src1_rst_n', 'cmu_rst_n')],
        ['sel', pin.get('sel', '_'.join(['para', name, 'sel_i']))]
    ]
    module_instance_name = '_'.join(['inst_cksw', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_clk3_swi(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'clk3_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['src0_clki', pin.get('src0_clki', source[0])],
        ['src0_rst_n', pin.get('src0_rst_n', 'cmu_rst_n')],
        ['src1_clki', pin.get('src1_clki', source[1])],
        ['src1_rst_n', pin.get('src1_rst_n', 'cmu_rst_n')],
        ['src2_clki', pin.get('src2_clki', source[2])],
        ['src2_rst_n', pin.get('src2_rst_n', 'cmu_rst_n')],
        ['sel', pin.get('sel', '_'.join(['para', name, 'sel_i[1:0]']))]
    ]
    module_instance_name = '_'.join(['inst_cksw', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_clk4_swi(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'clk4_swi')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
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
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_clk_div(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'clk_div')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    div_bw = int(param['DIV_BW'])
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['upd', pin.get('upd', '_'.join(['para', name, 'upd_i']))],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['high_th', pin.get('high_th', '_'.join(['para', name, 'th_i['+str(div_bw-1)+':0]']))],
        ['div', pin.get('div', '_'.join(['para', name, 'div_i['+str(div_bw-1)+':0]']))]
    ]
    module_instance_name = '_'.join(['inst_cdiv', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_gate_div(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'gate_div')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    div_bw = int(param['DIV_BW'])
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['upd', pin.get('upd', '_'.join(['para', name, 'upd_i']))],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['div_pat', pin.get('div_pat', '_'.join(['para', name, 'pat_i['+str(div_bw-1)+':0]']))]
    ]
    module_instance_name = '_'.join(['inst_gdiv', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_clk_gate(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'clk_gate')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['en', pin.get('en', '_'.join(['para', name, 'en_i']))],
        ['tmode', pin.get('tmode', 'test_mode_i')]
    ]
    module_instance_name = '_'.join(['inst_gdiv', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_baud_div(name, mode, source, cell_pack, comment):
    param = cell_pack['Param']
    pin = cell_pack.get('Pin', {})
    assert(cell_pack['Cell'] == 'baud_div')
    direction = mode.get('direction', 'node')
    name = name + '_o' if direction == 'output' else name
    sum_bw = int(param['SUM_BW'])
    step_bw = int(param['STEP_BW'])
    port_output = [
        ['clkout', pin.get('clkout', name)]
    ]
    port_input = [
        ['clkin', pin.get('clkin', source[0])],
        ['rst_n', pin.get('rst_n', 'cmu_rst_n')],
        ['sum', pin.get('sum', '_'.join(['para', name, 'sum_i['+str(sum_bw-1)+':0]']))],
        ['step', pin.get('stop', '_'.join(['para', name, 'step_i['+str(step_bw-1)+':0]']))],
        ['upd', pin.get('upd', '_'.join(['para', name, 'upd_i']))]
    ]
    module_instance_name = '_'.join(['inst_baud', name])
    return prolog_ast.ast_module_instance(cell_pack['Cell'], param.items(), module_instance_name, port_output, port_input, comment)


def make_assign(name, mode, source, cell_pack, comment):
    assert(cell_pack['Cell'] == 'assign')
    return prolog_ast.ast_extra(['assign', name, '=', source[0], ';'])


f_clk_module_dict = {
    'clk2_swi': make_clk2_swi,
    'clk3_swi': make_clk3_swi,
    'clk4_swi': make_clk4_swi,
    'clk_div': make_clk_div,
    'gate_div': make_gate_div,
    'clk_gate': make_clk_gate,
    'baud_div': make_baud_div,
    'assign': make_assign
}


def make_clk_module_instance(name, mode, source, clk_cell, comment):
    if len(clk_cell) == 1:
        cell_pack = clk_cell[0]
        f_cell_module_instance = f_clk_module_dict[cell_pack['Cell']]
        return f_cell_module_instance(name, mode, source, cell_pack, comment)
    else:
        ret = []
        for cell_pack, i in zip(clk_cell, range(len(clk_cell))):
            cell = cell_pack['Cell']

            mid_mode = dict(mode)
            if i != len(clk_cell)-1:
                mid_mode['direction'] = 'node'

            mid_source = list(source)
            if i != 0:
                mid_source = [name+'_net'+str(i-1)]

            f_cell_module_instance = f_clk_module_dict[cell]
            mi = f_cell_module_instance(name+'_net'+str(i), mid_mode, mid_source, cell_pack, comment)
            ret.append(mi)

        return ret



