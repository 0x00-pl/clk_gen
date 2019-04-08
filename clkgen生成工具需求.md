# 1 工具需求概述

+ 根据yml格式的时钟生成配置描述文件来生成verilog格式的clock generating模块的代码；
+ 根据yml格式的时钟生成配置描述文件来生成树状形式的时钟衍生结构示意图。  

# 2 yml描述文件说明

时钟发生器模块的结构与配置是通过YAML语言进行描述的。这个YAML格式的时钟发生器描述文件可以分成四个部分，这四个部分分别是：_Top_，_Ports_，_Clock_List_，_Custom_Code_。下面就分别详细说明这四个部分的定义格式及意义。  

## 2.1 ___Top___ __段落__

Top段落用来提供对clock generator模块的全局信息的描述。这些全局信息包括了模块的名称、模块的负责人邮件地址、所属项目的名称以及关于这个模块的摘要性描述文字。

Top段落的具体格式如下所述：

```yaml
Top:  
  - module: module_name
  - owner: designer@mail.xxxx.com
  - project: project_name
  - Description: >
    Some descripting text about this module.
```

* "**module**: _module_name_" 描述了目标模块的模块名称。
* “**owner**: _designer@mail.xxxx.com_” 描述了目标模块的设计负责人的邮件地址。
* “**project**: _project_name_” 描述了目标模块所属项目的项目代号。
* “**Description**: _some_description_text_” 提供了一些关于目标模块功能和设计目标等的一些简短描述性文字。

下面就用一个具体的例子来说明Top段落的信息应当怎样映射到具体的模块RTL代码。

一个示例Yaml Top段落的描述信息如下所示：
```yaml
Top: 
  - module: cmu_clk_gen
  - owner: zhaobeihua@canaan-creative.com
  - project: MAIX-2
  - description: >
    This is the clock signals generating module for the MAIX2 SoC. 
    This module generates all the clocks required by the function 
    units, modules in MAIX-2 SoC.
```
这段Yaml Top段落描述的信息所对应的Verilog RTL代码如下所示：
```verilog
//===============================================================================
// Project    : MAIX-2
// Owner      : zhaobeihua@canaan-creative.com
// File Name  : cmu_clk_gen.v
// Module Name: cmu_clk_gen
//-------------------------------------------------------------------------------
// Description:
//       This is the clock signals generating module for the MAIX2 SoC.  This 
//   module generates all the clocks required by the function units, modules in
//   MAIX-2 SoC.
//===============================================================================
`timescale  1ns / 1ps  
```

## 2.2 ___Ports___ __段落__

Ports段落用来定义由模块设计者显示声明的输入端口信号、输出端口信号以及模块内部的节点信号。这些信号是无法由clkgen生成工具根据具体的clock cell的特性而推断出来，因此必须由模块设计者直接而明确的定义。

Ports段落是一个包含多个signal项的有序列表。而每一个signal项又是一个包含多个 ***map*** 的嵌套 ***map***。 Ports段落的具体定义格式如下所示：
```yaml
Ports:
  - signal_name: 
    comment: short description about current signal
    mode: { direction: dir_val, type: type_val, width: NUM }
  - signal_name: 
    comment: short description about current signal
    mode: { direction: dir_val, type: type_val, width: NUM }
  - signal_name: 
    comment: short description about current signal
    mode: { direction: dir_val, type: type_val, width: NUM }
                         . . . . . .
```

下面就具体的介绍每一个信号项的定义格式和意义。每一个信号项的定义格式如下所示：

    - signal_name:
        comment: short description about current signal
        mode: { direction: dir_val, type: type_val, width: NUM }

* ***signal_name***: 用来定义端口信号（或者模块内部结点信号）的信号名称；
* ***comment***: 用来给出该信号功能或者作用的简短描述；
* ***mode***: 用来对该信号的特征给出更具体的描述（例如，IO方向，信号线类型、信号的比特宽度）。

这里需要对 ***mode*** 项给出更详细的说明。***mode*** 项包含了3个 **map** 类型数据结构项，这三个 **map** 数据项分别提供了关于当前信号的IO方向、信号线类型和信号比特宽度的定义。  
1. **direction**: *dir_val*  
   **direction** 用来定义当前信号的IO方向，_dir_val_ 的合法值可以是：_output_、_input_ 和 _node_。_output_ 表示当前信号是一个输出端口信号；_input_ 表示当前信号是一个输入端口信号；而 _node_ 表示当前信号是一个模块的内部节点信号。
2. **type**: _type_val_  
   **type** 用来定义当前信号的信号线类型，_type_val_ 的合法值可以是：_wire_ 或者 _reg_。_wire_ 表明当前信号线是由组合逻辑或者模块内的cell instance所驱动的；而 _reg_ 表明当前信号线是由时序逻辑（也就是触发器）所驱动的。**请注意！type的默认值是wire，如果在mode定义中没有出现type项，那么当前信号的类型就是wire！**  
3. **width**: _NUM_  
   **width** 用来定义当前信号的比特宽度。_NUM_ 在这里必须是一个大于0的正整数。**请注意！width的默认值是1，如果在mode定义中没有出现width项，那么当前信号的宽度就是1！**    

下面就用一个具体的例子来说明Ports段落的信息应当怎样映射到具体的模块RTL代码。

一个示例Yaml Ports段落的描述信息如下所示：  
```yaml
Ports:
  - cmu_rst_n:
    comment: This is the global reset to CMU, LOW active
    mode: { direction: input, type: wire, width: 1 }
  - pll_0_clk:
    comment: This is the clock generated from system PLL 0
    mode: { direction: input, type: wire, width: 1 }
  - pll_1_clk:
    comment: This is the clock generated from system PLL 1
    mode: { direction: input, type: wire }
  - pll_2_clk:
    comment: This is the clock generated from system PLL 2
    mode: { direction: input, type: wire }
  - clk_26m:
    comment: This is the 26Mhz clock from off-chip oscilator
    mode: { direction: input }
  - soc_sleep_flag_i:
    comment: the flag signal that the whole SoC entering sleep mode
    mode: { direction: input }
  - sys_bus_aclk_en:
    comment: the clkin enable control for sys_bus_aclk dividor Clk Cell
    mode: { direction: node }
```  

这段Yaml Top段落描述的信息所对应的Verilog RTL代码如下所示：
```verilog
module cmu_clk_gen
(
    // in/out port signals defined by module owner
    input wire    cmu_rst_n, // This is the global reset to CMU, LOW active
    input wire    pll_0_clk, // This is the clock generated from system PLL 0
    input wire    pll_1_clk, // This is the clock generated from system PLL 1
    input wire    pll_2_clk, // This is the clock generated from system PLL 2
    input wire    clk_26m, // This is the 26Mhz clock from off-chip oscilator
    input wire    soc_sleep_flag_i, // the flag signal that SoC entering sleep mode
            . . . . . .
);

    //===========================================================================
    // declaration of internal wires and registers
    //===========================================================================
    wire   sys_bus_aclk_en; // the clkin enable for sys_bus_aclk dividor Cell
            . . . . . .

endmodule
```   

## 2.3 ___Clock_List___ __段落__

Clock_List段落是整个描述文件的核心内容之所在。Clock_List段落定义了 _clkgen_ 模块所需要生成的所有时钟信号，利用什么类型的clock cell来产生这些时钟信号。同时也隐含定义了表达整个时钟网络中时钟对象派生关系的是时钟树结构图。  

Clock_List段落是由多个clock object define项构成的。Clock_List段落的具体定义格式如下所示：  
```yaml
Clock_List:
  clk_obj_name: 
    comment: short description about clk_obj_name's function or purpose
    mode: { direction: dir_val }
    Source: [ src_clk_obj_0, src_clk_obj_1, ... ]
    Clk_Cell:
      - clk_cell_0_name:
        Param: { PARA0: NUM, PARA1: NUM, PARA2: NUM, ... }
        Pins: { pin0_name: signal_name, pin1_name: signal_name, ... }
      - clk_cell_1_name:
        Param: { PARA0: NUM, PARA1: NUM, PARA2: NUM, ... }
        Pins: { pin0_name: signal_name, pin1_name: signal_name, ... }

  clk_obj_name2:
    . . . . . .

  clk_obj_name3:
    . . . . . .
```

下面再具体的介绍每一个时钟对象项的定义格式和意义。   

1. **clk_obj_name**: 定义了当前时钟对象的名称。
2. **comment**: 用来提供关于当前时钟对象的简短注释性描述；
3. **mode**: 用来定义当前时钟对象的IO方向及信号线类型，具体定义方式可以参考端口信号的定义说明；
4. **Source**: 一个父时钟对象的列表。当前时钟对象是通过clock cell根据父时钟对象而派生出来的。父时钟对象列表可以包含一个或者多个父时钟对象；
5. **Clk_Cell**: 用来定义时钟发生器cell列表。时钟发生器是一类 _verilog_ module，时钟发生器根据父时钟对象来生成一个新的派生时钟对象。**Clk_Cell** 下可以包含多个时钟发生器cells；
6. **clk_cell_name**: 用来定义具体的一个时钟发生器cell。目前在构建时钟发生器网络时使用到了下列几种时钟发生器cells：  
    * `clk2_swi`: 两时钟源切换器，从两个时钟源中选择一个作为新的输出时钟；
    * `clk3_swi`: 三时钟源切换器，从三个时钟源中选择一个作为新的输出时钟；
    * `clk4_swi`: 四时钟源切换器，从四个时钟源中选择一个作为新的输出时钟；
    * `clk_div`: 基于 _edge_ 的时钟分频器，利用一个源时钟经分频产生一个新的输出时钟；
    * `gate_div`: 基于 _clock gate_ 的时钟分频器，利用一个源时钟并通过控制clock gate信号而产生一个新的输出时钟；
    * `clk_gate`: clock gating控制cell；
    * `baud_div`: 参照UART波特率发生器的工作原理而对源时钟进行分频而产生新的输出时钟；
    * `assign`: verilog中的 **assign** 语句，可直接将输入源时钟重命名后输出。   
7. **Param**: _Param_ 是 **clk_cell_name** 下的一个属性项。每一种时钟发生器cell都有数个配置参数，不同的配置参数可以使时钟发生器具有不同的特性，从而适应于多种场景的时钟生成。而 _Param_ 就是用来定义时钟发生器的配置参数的；
8. **Pins**: _Pins_ 是 **clk_cell_name** 下的另一个属性项。每一种时钟发生器cell都具有多个输入pins和一个输出pins。在一般情况下，输入pins的控制信号可由clkgen生成工具根据默认的信号推断规则定义出来，而无需设计者特别指定，但是在一些特殊的场景下，设计者需要对某个pin做特殊的控制，在这种情况下就可以利用 _Pins_ 来指定设计者自定义控制信号。  

### 2.3.1 普通Clock Cell信号名推断规则

Clock Cell信号名推断指的是依照一定的规则由代码生成工具来自动的为每个clock发生器cell产生输入pin和输出pin的信号，并自动的将这些信号声明在模块的端口或者内部节点信号声明列表中。  

对于不同的clock发生器cell，其相关的信号名推断规则也是不同的，下面就根据不同clock发生器cell来说明这些推断规则。

#### 2.3.1.1 _clk2_swi_
* 如果 _clk2_swi_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _clk2_swi_ 的 _sel_ pin的关联信号应当声明为 para\_***clk_obj_name***\_sel\_i（增加前缀 para_ 和后缀 _sel_i），而且这个信号必须是输入端口信号，1-bit宽度；
* _clk2_swi_ 的两个源时钟信号来自于 **Source** 属性中定义的父时钟对象的列表，并且这个列表只允许含有两个父时钟对象;
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _clk2_swi_ 来说，instance的名称应当声明为 inst_cksw_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  sys_src0_clk:
    comment: The SoC system source 0 clock, from clk_26m or pll_0_clk
    mode: { direction: node }
    Source: [ clk_26m, pll_0_clk ]
    Clk_Cell:
      - clk2_swi:
        Param: { INIT_SEL: 1 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    clk2_swi #(.INIT_SEL(1)) inst_cksw_sys_src0_clk
    (
        // Outputs
        .clkout                        ( sys_src0_clk                      ),
        // Inputs
        .src0_clki                     ( clk_26m                           ),
        .src0_rst_n                    ( cmu_rst_n                         ),
        .src1_clki                     ( pll_0_clk                         ),
        .src1_rst_n                    ( cmu_rst_n                         ),
        .sel                           ( para_sys_src0_clk_sel_i           )
    );

```

#### 2.3.1.2 _clk3_swi_
* 如果 _clk3_swi_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _clk3_swi_ 的 _sel_ pin的关联信号应当声明为 para\_***clk_obj_name***\_sel\_i（增加前缀 para_ 和后缀 _sel_i），而且这个信号必须是输入端口信号，2-bit宽度；
* _clk3_swi_ 的两个源时钟信号来自于 **Source** 属性中定义的父时钟对象的列表，并且这个列表只允许含有三个父时钟对象；
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _clk3_swi_ 来说，instance的名称应当声明为 inst_cksw_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  sys_src1_clk:
    comment: The SoC system source 1 clock, from clk_26m, pll_1_clk, or pll_2_clk
    mode: { direction: node }
    Source: [clk_26m, pll_1_clk, pll_2_clk]
    Clk_Cell:
      - clk3_swi:
        Param: { INIT_SEL: 2 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    clk3_swi #(.INIT_SEL(2)) inst_cksw_sys_src1_clk
    (
        // Outputs
        .clkout                        ( sys_src1_clk                      ),
        // Inputs
        .src0_clki                     ( clk_26m                           ),
        .src0_rst_n                    ( cmu_rst_n                         ),
        .src1_clki                     ( pll_1_clk                         ),
        .src1_rst_n                    ( cmu_rst_n                         ),
        .src2_clki                     ( pll_2_clk                         ),
        .src2_rst_n                    ( cmu_rst_n                         ),
        .sel                           ( para_sys_src1_clk_sel_i[1:0]      )
    );
```

#### 2.3.1.3 _clk4_swi_
* 如果 _clk4_swi_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _clk4_swi_ 的 _sel_ pin的关联信号应当声明为 para\_***clk_obj_name***\_sel\_i（增加前缀 para_ 和后缀 _sel_i），而且这个信号必须是输入端口信号，2-bit宽度；
* _clk4_swi_ 的两个源时钟信号来自于 **Source** 属性中定义的父时钟对象的列表，并且这个列表只允许含有四个父时钟对象；
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _clk4_swi_ 来说，instance的名称应当声明为 inst_cksw_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  sys_src2_clk:
    comment: The SoC system source 2 clock, from clk_26m, pll_0_clk, pll_1_clk, or pll_2_clk
    mode: { direction: node }
    Source: [clk_26m, pll_0_clk, pll_1_clk, pll_2_clk, pll_3_clk]
    Clk_Cell:
      - clk4_swi:
        Param: { INIT_SEL: 3 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    clk4_swi #(.INIT_SEL(3)) inst_cksw_sys_src2_clk
    (
        // Outputs
        .clkout                         ( sys_src2_clk                     ),
        // Inputs
        .src0_clki                      ( clk_26m                          ),
        .src0_rst_n                     ( cmu_rst_n                        ),
        .src1_clki                      ( pll_0_clk                        ),
        .src1_rst_n                     ( cmu_rst_n                        ),
        .src2_clki                      ( pll_1_clk                        ),
        .src2_rst_n                     ( cmu_rst_n                        ),
        .src3_clki                      ( pll_2_clk                        ),
        .src3_rst_n                     ( cmu_rst_n                        ),
        .sel                            ( para_sys_src2_clk_sel_i[1:0]     )
    );
```

#### 2.3.1.4 _clk_div_
* 如果 _clk_div_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _clk_div_ cell的 _upd_ pin的关联信号应当声明为 para\_***clk_obj_name***\_upd\_i（增加前缀 para_ 和后缀 _upd_i），而且这个信号必须是输入端口信号，1-bit宽度；
* 如果CKEN参数的值是0，_en_ pin的关联信号应当声明为 1'b1，如果CKEN参数的值是1，_en_ pin的关联信号应当声明为 para\_***clk_obj_name***\_en\_i（增加前缀 para_ 和后缀 _en_i），而且这个信号必须是输入端口信号，1-bit宽度；
* _clk_div_ cell的 _div_ pin的关联信号应当声明为 para\_***clk_obj_name***\_div\_i（增加前缀 para_ 和后缀 _div_i），而且这个信号必须是输入端口信号，宽度等于 **DIV_BW** 的定义值；
* _clk_div_ cell的 _high_th_ pin的关联信号应当声明为 para\_***clk_obj_name***\_th\_i（增加前缀 para_ 和后缀 _th_i），而且这个信号必须是输入端口信号，宽度等于 **DIV_BW** 的定义值；
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _clk_div_ 来说，instance的名称应当声明为 inst_cdiv_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  peri_mclk_src:
    comment: the source clock for peripheral device module clock
    mode: { direction: node }
    Source: [sys_src2_clk]
    Clk_Cell:
      - clk_div:
        Param: { STATIC: 0, CKEN: 1, DIV_BW: 4, INI_DIV: 7 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    clk_div #(.STATIC(0), CKEN(1), .DIV_BW(4), .INI_DIV(7)) inst_cdiv_peri_mclk_src
    (
        // Outputs
        .clkout                         ( peri_mclk_src                    ),
        // Inputs
        .clkin                          ( sys_src2_clk                     ),
        .rst_n                          ( cmu_rst_n                        ),
        .upd                            ( para_peri_mclk_src_upd_i         ),
        .en                             ( para_peri_mclk_src_en_i          ),
        .high_th                        ( para_peri_mclk_src_th_i[3:0]     ),
        .div                            ( para_peri_mclk_src_div_i[3:0]    )
    );
```

#### 2.3.1.5 _gate_div_
* 如果 _gate_div_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _gate_div_ cell的 _upd_ pin的关联信号应当声明为 para\_***clk_obj_name***\_upd\_i（增加前缀 para_ 和后缀 _upd_i），而且这个信号必须是输入端口信号，1-bit宽度；
* 如果CKEN参数的值是0，_en_ pin的关联信号应当声明为 1'b1，如果CKEN参数的值是1，_en_ pin的关联信号应当声明为 para\_***clk_obj_name***\_en\_i（增加前缀 para_ 和后缀 _en_i），而且这个信号必须是输入端口信号，1-bit宽度；
* _gate_div_ cell的 _div_pat_ pin的关联信号应当声明为 para\_***clk_obj_name***\_pat\_i（增加前缀 para_ 和后缀 _pat_i），而且这个信号必须是输入端口信号，宽度等于 **DIV_BW** 的定义值；
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _gate_div_ 来说，instance的名称应当声明为 inst_gdiv_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  sys_dma_aclk:
    comment: the system DMAC master AXI interface aclk
    mode: { direction: output }
    Source: [sys_bus_aclk]
    Clk_Cell:
      - gate_div:
        Param: { STATIC: 0, CKEN: 1, DIV_BW: 10, INI_DIV: 0x155 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    gate_div #(.STATIC(0), CKEN(1), .DIV_BW(10), .INI_DIV(10'h155)) inst_gdiv_sys_dma_aclk
    (
        // Outputs
        .clkout                         ( sys_dma_aclk_o                   ),
        // Inputs
        .clkin                          ( sys_bus_aclk                     ),
        .rst_n                          ( cmu_rst_n                        ),
        .upd                            ( para_sys_dma_aclk_upd_i          ),
        .en                             ( para_sys_dma_aclk_en_i           ),
        .div_pat                        ( para_sys_dma_aclk_pat_i[9:0]     )
    );
```

#### 2.3.1.6 _clk_gate_

* 如果 _clk_gate_ 产生的输出时钟被定义为输出端口，那么其输出信号就需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其输出信号就是 ***clk_obj_name***；
* _clk_gate_ cell的 _en_ pin的关联信号应当声明为 para\_***clk_obj_name***\_en\_i（增加前缀 para_ 和后缀 _en_i），而且这个信号必须是输入端口信号，1-bit宽度；
* 在实例化一个 _module_ cell时，需要为这个cell指定一个instance名称，对于 _clk_gate_ 来说，instance的名称应当声明为 inst_cg_***clk_obj_name***。

下面给出一个具体的例子：
```yaml
  sys_dma_pclk:
    comment: the system DMAC slave APB interface pclk
    mode: { direction: output }
    Source: [sys_pclk_src]
    Clk_Cell:
      - clk_gate:
        Param: { ASYNC: 1 }
```
根据上面的yaml描述信息，可产生下面相对应的verilog代码片段：
```verilog
    clk_gate #(.ASYNC(1)) inst_cg_sys_dma_pclk
    (
        // Outputs
        .clkout                         ( sys_dma_pclk_o                   ),
        // Inputs
        .clkin                          ( sys_pclk_src                     ),
        .rst_n                          ( cmu_rst_n                        ),
        .en                             ( para_sys_dma_pclk_en_i           ),
        .tmode                          ( test_mode_i                      )
    );
```

### 2.3.2 复合Clock Cell信号名推断规则

在某些场景下，需要利用多个clock发生器cell通过直接级联而产生新的派生时钟，在这种情况下，cell的信号名及示例名的推断规则就不同于一般情况下的规则，这里就详细说明一下具体的推断规则。

* 当一个时钟是通过多级clock发生器级联而产生时，如果这个是时钟对象声明为输出端口，那么其信号名需要声明为 ***clk_obj_name***_o（增加一个 _o 的后缀），如果定义为节点，那么其信号就是 ***clk_obj_name***；
* 对于第一级clock发生器cell，其instance名字应当声明为 inst\_**ID**0\_***clk_obj_name***。这里的 ___ID___ 与clock发生器的类型有关，对于 _clk2_swi_、_clk3_swi_和_clk4_swi_，___ID___ 的值为`cksw`；对于 _clk_div_，___ID___ 的值为`cdiv`；对于 _gate_div_，___ID___ 的值为`gdiv`；对于 _baud_div_，___ID___ 的值为`baud`；
* 对于第一级clock发生器cell，其产生的中间输出时钟的信号名字应当为 ***clk_obj_name***_net0；
* 对于第二级clock发生器cell，其instance名字应当声明为 inst\_**ID**1\_***clk_obj_name***。这里就不再重复的 ___ID___ 的定义方法了；
* 对于第二级clock发生器cell，如果其产生的就是最后的输出时钟，名字就直接用***clk_obj_name***_o；如果是中间输出时钟，信号名应当为 ***clk_obj_name***_net1；
* 对于可能出现的第三级，第四级等的clock发生器cell，可按照类似的规则递推；

下面就用几个例子来说明复合clock发生器的定义及对应的生成。

#### 例-1
sys_pclk_src的时钟定义信息如下所示：
```yaml
  sys_pclk_src:
    comment: the source clock for function modules APB I/F pclk
    mode: { direction: node }
    Source: [sys_src0_clk]
    Clk_Cell:
      - clk_div:
        Param: { STATIC: 0, CKEN: 1, DIV_BW: 4, INI_DIV: 7 }
      - gate_div:
        Param: { STATIC: 0, CKEN: 0, DIV_BW: 12, INI_DIV: 0x111 }
```
这个配置可对应到如下的Verilog RTL代码片段：
```verilog
    clk_div #(.STATIC(0), CKEN(1), .DIV_BW(4), .INI_DIV(7)) inst_cdiv0_sys_pclk_src
    (
        // Outputs
        .clkout                         ( sys_pclk_src_net0                ),
        // Inputs
        .clkin                          ( sys_src0_clk                     ),
        .rst_n                          ( cmu_rst_n                        ),
        .upd                            ( para_sys_pclk_src_upd0_i         ),
        .en                             ( para_sys_pclk_src_en0_i          ),
        .high_th                        ( para_sys_pclk_src_th0_i[3:0]     ),
        .div                            ( para_sys_pclk_src_div0_i[3:0]    )
    );

    gate_div #(.STATIC(0), CKEN(0), .DIV_BW(12), .INI_DIV(12'h111)) inst_gdiv1_sys_pclk_src
    (
        // Outputs
        .clkout                         ( sys_pclk_src                     ),
        // Inputs
        .clkin                          ( sys_pclk_src_net0                ),
        .rst_n                          ( cmu_rst_n                        ),
        .upd                            ( para_sys_pclk_src_upd1_i         ),
        .en                             ( 1'b1                             ),
        .div_pat                        ( para_sys_pclk_src_pat1_i[11:0]   )
    );
```

#### 例-2
uart_0_sclk的时钟定义信息如下所示：
```yaml
  uart_0_sclk:
    comment: the UART 0 host interface module serial clock
    mode: { direction: output }
    Source: [peri_mclk_src]
    Clk_Cell:
      - clk_div:
        Param: { STATIC: 0, CKEN: 1, DIV_BW: 4, INI_DIV: 7 }
        Pins: { high_th: 1 }
      - baud_div:
        Param: { SUM_BW: 12, STEP_BW: 8, INI_SUM: 230, INI_STEP: 33 }
```
这个配置可对应到如下的Verilog RTL代码片段：
```verilog
    clk_div #(.STATIC(0), CKEN(1), .DIV_BW(4), .INI_DIV(7)) inst_cdiv0_uart_0_sclk
    (
        // Outputs
        .clkout                         ( uart_0_sclk_net0                 ),
        // Inputs
        .clkin                          ( peri_mclk_src                    ),
        .rst_n                          ( cmu_rst_n                        ),
        .upd                            ( para_uart_0_sclk_upd0_i          ),
        .en                             ( para_uart_0_sclk_en0_i           ),
        .high_th                        ( 4'h1                             ),
        .div                            ( para_uart_0_sclk_div0_i[3:0]     )
    );

    baud_div #(.SUM_BW(12), .STEP_BW(8), .INI_SUM(12'd230), .INI_STEP(8'd33)) inst_baud1_uart_0_sclk
    (
        // Outputs
        .clkout                         ( uart_0_sclk_o                    ),
        // Inputs                                                          
        .clkin                          ( uart_0_sclk_net0                 ),
        .rst_n                          ( cmu_rst_n                        ),
        .sum                            ( para_uart_0_sclk_sum1_i[11:0]    ),
        .step                           ( para_uart_0_sclk_step1_i[7:0]    ),
        .upd                            ( para_uart_0_sclk_upd1_i          )
    );
```