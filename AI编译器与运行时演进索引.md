# AI Compiler、Kernel DSL 与运行时演进索引

> 整理日期：2026-10-05
> 这条主线只回答：怎样捕获模型程序、保留和降低语义、搜索调度、生成 kernel、插入通信并管理执行。
> 模型理论请看 [AI 模型基础理论与算法演进索引](AI模型基础理论与算法演进索引.md)；具体公司的模型和部署实现请看 [AI 厂商模型与系统实现索引](AI厂商模型与系统实现索引.md)。

## 1. 先把 AI Compiler 的层次分开

| 层次 | 主要问题 | 代表资料 |
|---|---|---|
| 前端与图捕获 | Python/动态图怎样变成可优化程序 | Chainer、PyTorch、torch.fx、Dynamo |
| 图 IR 与多级 lowering | 模型语义怎样逐步降到循环、GPU 和机器指令 | XLA、Glow、MLIR、TVM |
| Tensor program | tile、loop、cache、vector、tensorize 怎样表示 | TVM、TensorIR、Hidet |
| 自动调优 | 怎样在巨大 schedule space 中找高性能实现 | AutoTVM、Ansor、MetaSchedule、Roller、Bolt |
| Kernel DSL 与 layout | 专家怎样以 tile/layout/pipeline 编写 GPU kernel | Triton、TileLang、CuTe、Linear Layouts |
| 图融合与整体调度 | 怎样跨 operator 消除 HBM、launch 和 runtime 开销 | TASO、Rammer、FusionStitching、Welder、Korch、Mirage |
| 分布式编译 | tensor sharding、pipeline 与 collective 怎样生成 | GSPMD、Alpa |
| 部署 runtime | executable、buffer、KV cache 与 serving 怎样管理 | TinyIREE、TensorRT-LLM |

模型公式、编译器和厂商系统经常共同出现，但不能混成一层。FlashAttention 是 Attention kernel 算法；Triton/CuTe 是表达与生成这种 kernel 的编译技术；TensorRT-LLM 是面向 NVIDIA 的部署系统。

## 2. 十年演进时间线

### 2.1 2016–2017：图编译与动态图语义

| 时间 | 资料 | 变化 |
|---|---|---|
| 2017– | [XLA / OpenXLA](xla_compiler/论文中文解读.md) | framework graph → HLO，进行 fusion、layout、buffer assignment 与多后端 codegen |
| 2017 | [Dynamic Computation Graphs](dynamic_computation_graphs/论文中文解读.md) | define-by-run 的动态图语义与编译困难 |

这一阶段形成长期矛盾：静态图便于全局优化，动态图便于 Python 控制流和调试。后续图捕获系统一直在两者之间寻找可验证边界。

### 2.2 2018：端到端编译器与自动调优

| 时间 | 论文 | 变化 |
|---|---|---|
| 2018 | [Tensor Comprehensions](tensor_comprehensions/论文中文解读.md) | 数学 DSL、polyhedral lowering 与 autotuning |
| 2018 | [TVM](tvm_compiler/论文中文解读.md) | graph optimization、Tensor Expression、schedule 与学习成本模型 |
| 2018 | [Glow](glow_compiler/论文中文解读.md) | high/low-level IR、逐步 lowering 与显式 buffer |

三者共同确立“计算语义和执行 schedule 分离”的范式，但自动化程度不同。

### 2.3 2019：主流动态图框架、图重写与 Kernel DSL

| 时间 | 论文 | 变化 |
|---|---|---|
| 2019 | [Chainer](chainer_define_by_run/论文中文解读.md) | define-by-run 的工程化路径 |
| 2019 | [PyTorch](pytorch_imperative/论文中文解读.md) | imperative eager frontend 成为主流 |
| 2019 | [JANUS](janus_symbolic_graph/论文中文解读.md) | 从动态图运行轨迹推断并生成符号图 |
| 2019 | [TASO](taso/论文中文解读.md) | 自动生成、验证并搜索等价图替换 |
| 2019 | [Triton](triton_compiler/论文中文解读.md) | block/tile-level GPU DSL 与自动线程映射 |

Triton 的位置不是“另一个神经网络框架”，而是图编译器和专家 kernel 之间的 GPU codegen 层。

### 2.4 2020：多级 IR、自动 Schedule 与整体调度

| 时间 | 论文 | 变化 |
|---|---|---|
| 2020/21 | [MLIR](mlir/论文中文解读.md) | extensible dialect、region 与 progressive lowering |
| 2020 | [Ansor](ansor/论文中文解读.md) | 自动构造 schedule sketches 与学习型搜索 |
| 2020 | [Rammer](rammer/论文中文解读.md) | 用 rTask 统一 operator 内外并行调度 |
| 2020 | [FusionStitching](fusion_stitching/论文中文解读.md) | fusion 中间结果的共享内存 stitching |

### 2.5 2021：动态 Shape、SPMD 与硬件原生模板

| 时间 | 论文 | 变化 |
|---|---|---|
| 2021 | [Nimble](nimble_dynamic_nn/论文中文解读.md) | 动态神经网络的编译执行 |
| 2021 | [DISC](disc_dynamic_shape/论文中文解读.md) | dynamic shape 的 MLIR 编译路径 |
| 2021 | [GSPMD](gspmd/论文中文解读.md) | sharding propagation、SPMD lowering 和 collective 插入 |
| 2021/22 | [Bolt](bolt/论文中文解读.md) | 在 CUTLASS 等 hardware-native template 上做小空间搜索 |

### 2.6 2022：可编程搜索空间、TensorIR 与分布式自动并行

| 时间 | 论文 | 变化 |
|---|---|---|
| 2022 | [torch.fx](torch_fx/论文中文解读.md) | Python 层可检查、可变换的符号图 |
| 2022 | [Roller](roller/论文中文解读.md) | 用硬件约束构造 tile，减少海量黑盒测量 |
| 2022 | [TinyIREE](tinyiree/论文中文解读.md) | MLIR 编译器、HAL、VM 与小型部署 runtime |
| 2022 | [MetaSchedule](metaschedule/论文中文解读.md) | 用可组合概率程序表达 schedule search space |
| 2022/23 | [TensorIR](tensorir/论文中文解读.md) | 以 block/read-write region 连接循环调度和 tensor intrinsic |
| 2022 | [Alpa](alpa/论文中文解读.md) | 联合搜索 intra-op sharding 与 inter-op pipeline |

### 2.7 2023：Task Mapping、Tile Fusion 与稀疏 Kernel

| 时间 | 论文 | 变化 |
|---|---|---|
| 2023 | [Hidet](hidet/论文中文解读.md) | task-mapping program 与 post-scheduling fusion |
| 2023 | [Welder](welder/论文中文解读.md) | tile graph 上联合分析 fusion 与数据复用 |
| 2023 | [MegaBlocks](megablocks/论文中文解读.md) | 面向 MoE 的 block-sparse kernel 与系统 |

### 2.8 2024：动态图捕获进入主框架

| 时间 | 论文 | 变化 |
|---|---|---|
| 2024 | [PyTorch 2](pytorch_2/论文中文解读.md) | Dynamo guards、AOTAutograd、Inductor 与 Triton codegen |
| 2024 | [Korch](korch/论文中文解读.md) | 以全局优化问题选择 kernel orchestration |

### 2.9 2025：Tile DSL、Persistent Kernel 与编译器评测

| 时间 | 论文 | 变化 |
|---|---|---|
| 2025 | [TileLang](tilelang/论文中文解读.md) | tile dataflow 与 schedule annotation 的可组合 DSL |
| 2025 | [Mirage Persistent Kernel](mirage_persistent_kernel/论文中文解读.md) | 把模型子图编译为 persistent mega-kernel |
| 2025 | [TritonBench](tritonbench/论文中文解读.md) | 分离 LLM 生成 kernel 的可调用性、正确性与性能 |
| 2025/26 | [Linear Layouts](linear_layouts/论文中文解读.md) | 用统一代数描述线程、寄存器与 shared-memory layout |

### 2.10 2026：布局代数、动态图后端与数值契约

| 时间 | 资料 | 变化 |
|---|---|---|
| 2026 | [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md) | layout 变换成为可组合、可推理的代数 |
| 2026 | [CuTeDSL TorchInductor Backend](cutedsl_torchinductor/论文中文解读.md) | 专家 GPU DSL 接入 PyTorch 图编译 |
| 2026 | [PyTorch Graph Programming Model](pytorch_graph_programming_model/论文中文解读.md) | Dynamo、export 与 dynamic shape 的语义边界 |
| 2026 | [Event Tensor](event_tensor/论文中文解读.md) | 事件驱动 tensor execution |
| 2026 | [Ada-MK](ada_mk/论文中文解读.md) | 自适应 mega-kernel |
| 2026 | [Taming Bitwise GPU Kernels](taming_bitwise_gpu_kernels/论文中文解读.md) | 将浮点依赖树变成可编译和静态验证的逐位契约 |

## 3. 编译器演进的七次主要变化

### 3.1 逐 Operator Runtime → 整图编译

XLA、Glow、TVM 开始跨 operator 做常量折叠、layout、fusion 和 buffer planning，减少 launch 与中间 HBM 流量。

### 3.2 单一 IR → 多级 IR 与 Dialect

模型算子、张量循环、GPU tile 和机器指令需要不同抽象。Glow 的高低两层 IR 是早期实例，MLIR 将其基础设施化。

### 3.3 手写 Schedule → Autotuning → 可编程搜索空间

| 阶段 | 代表 | 专家知识放在哪里 |
|---|---|---|
| 模板搜索 | AutoTVM | 人工 schedule template |
| 自动 sketch | Ansor | sketch rule 与 cost model |
| 可编程搜索 | MetaSchedule | 概率程序、rule、mutator、postprocessor |
| 约束构造 | Roller | 硬件资源和 tile 约束 |
| 原生模板 | Bolt | CUTLASS/tensor-core pipeline |
| 专家 DSL | Triton、TileLang、CuTe | tile、layout 与 pipeline 程序 |

趋势不是“自动化最终替代专家”，而是把专家知识放进更可组合、更容易验证的抽象。

### 3.4 Operator Fusion → Tile Fusion → Persistent/Mega-Kernel

普通 fusion 消除中间 tensor；Welder 在 tile 级考虑 producer/consumer；persistent kernel 让状态长期留在片上；mega-kernel 将多个操作和部分调度合并。融合越大，寄存器压力、occupancy、编译时间和动态性风险越高。

### 3.5 静态图 → Guarded Dynamic Capture

Dynamo 并非把任意 Python 永久静态化，而是捕获满足 guards 的稳定子图。guard 失效会重编译或 graph break；dynamic shape 的关键是符号约束和 specialization policy。

### 3.6 单设备 Codegen → 分布式编译

GSPMD 把 tensor sharding 降成每设备局部程序和 collectives；Alpa 在更高层搜索算子内分片和 pipeline stage。通信、拓扑和 microbatch 已成为编译计划的一部分。

### 3.7 近似数值一致 → 显式数值契约

传统编译器常允许浮点重排。逐位 GPU kernel 工作进一步要求 compiler、autotuner 和汇编检查器理解依赖树，使“最快”变成“在指定数值等价类中最快”。

## 4. 推荐阅读路线

### 路线 A：端到端编译器

[XLA](xla_compiler/论文中文解读.md) → [TVM](tvm_compiler/论文中文解读.md) → [Glow](glow_compiler/论文中文解读.md) → [MLIR](mlir/论文中文解读.md) → [TinyIREE](tinyiree/论文中文解读.md)。

### 路线 B：动态图到图编译

Chainer / PyTorch → JANUS → torch.fx → Nimble / DISC → PyTorch 2 → PyTorch Graph Programming Model。

### 路线 C：Tensor Schedule 与自动调优

Tensor Comprehensions / TVM → Ansor → Roller / Bolt → TensorIR + MetaSchedule。

### 路线 D：GPU Kernel DSL

[Triton](triton_compiler/论文中文解读.md) → [Hidet](hidet/论文中文解读.md) → [TileLang](tilelang/论文中文解读.md) → [Linear Layouts](linear_layouts/论文中文解读.md) → [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md)。

### 路线 E：融合与整体调度

TASO → Rammer / FusionStitching → Welder → Korch → Mirage / Ada-MK / Event Tensor。

### 路线 F：分布式训练编译

GSPMD → Alpa → 再去厂商索引看 DeepSeek DualPipe、Ascend CloudMatrix 等生产约束。

## 5. 与 Kernel 算法和厂商 Runtime 的边界

| 资料 | 主归类 | 原因 |
|---|---|---|
| FlashAttention 1–4 | 模型/Attention 算法 | 主要贡献是 exact Attention 的 IO 与硬件算法 |
| Triton、TileLang、CuTe | AI Compiler | 主要贡献是 kernel 表达、分析和 codegen |
| TensorRT-LLM | 厂商系统实现 | NVIDIA 专用模型编译、engine 与 serving runtime |
| CloudMatrix384 | 厂商系统实现 | Ascend 超节点与 DeepSeek workload 的联合设计 |
| Mooncake | 厂商系统实现 | Kimi 的 KV-centric disaggregated serving |
| MegaBlocks | AI Compiler/系统 | 通用 block-sparse MoE kernel 与执行方法 |

跨层资料可以在两个索引出现，但只有一个主归类，另一个只保留交叉入口。

## 6. 编译器论文统一比较口径

- 语义覆盖：静态 shape、dynamic shape、控制流、副作用和自定义算子。
- 编译成本：capture、search、device measurement、codegen 与首次执行分开。
- 运行成本：kernel、图级、端到端训练/推理分开。
- 调优预算：候选数、设备测量次数、历史数据库和失败率。
- 硬件：GPU 型号、dtype、layout、vendor library 与软件版本。
- 内存：峰值显存、HBM 字节、寄存器、shared memory 和 KV cache。
- 分布式：拓扑、collective 字节、通信重叠和负载均衡。
- 正确性：误差容忍、浮点重排、逐位要求和动态 guard。

## 7. 相关专题索引

- [PyTorch 动态图与 Graph 编译论文阅读索引](PyTorch动态图与Graph编译论文阅读索引.md)
- [Triton 论文阅读索引](Triton论文阅读索引.md)
- [GPU 内核融合、MoE 与大模型推理论文阅读索引](GPU内核融合与大模型推理论文阅读索引.md)
