# Triton 论文阅读索引

这里的 **Triton** 指由 OpenAI 发起、现已广泛用于 PyTorch 编译栈的 GPU kernel 编程语言与编译器，不是 NVIDIA Triton Inference Server。

本文按论文首次公开时间排序，选择四篇能串起 Triton 发展主线、且在各自阶段最有代表性的论文。所谓“最出名”并非按单一引用数机械排序，而是综合了奠基性、工业影响、后续研究中的使用频率、论文/会议认可度与是否直接解释 Triton。本目录没有把 FlashAttention 纳入主线：它极其著名，也大量使用 Triton，但研究主角是注意力算法，不是 Triton 本身。

## 一、时间线

| 时间 | 论文 | 为什么读 | 本目录 |
|---|---|---|---|
| 2019-06 | *Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations*（MAPL 2019） | 奠基论文：说明 tile-level 编程模型、Triton-IR、自动并行化与 autotuning 从何而来 | [概要](triton_compiler/论文概要.md) · [中文解读](triton_compiler/论文中文解读.md) · [PDF](triton_compiler/paper.pdf) |
| 2024-04 | *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*（ASPLOS 2024） | 解释 Triton 如何成为 `torch.compile` 的 GPU 代码生成后端，并进入大规模真实模型编译链 | [概要](pytorch_2/论文概要.md) · [中文解读](pytorch_2/论文中文解读.md) · [PDF](pytorch_2/paper.pdf) |
| 2025-02 | *TritonBench: Benchmarking Large Language Model Capabilities for Generating Triton Operators*（arXiv:2502.14752） | 从基准角度回答“写对、跑通、跑快 Triton kernel 到底有多难”，也是 LLM 生成 Triton 代码的重要公开基线 | [概要](tritonbench/论文概要.md) · [中文解读](tritonbench/论文中文解读.md) · [PDF](tritonbench/paper.pdf) |
| 2025-05 / 2026-03 | *Linear Layouts: Robust Code Generation of Efficient Tensor Computation Using F2*（ASPLOS 2026） | 解释现代 Triton 后端最棘手的 tensor layout 问题，以及为何用 GF(2) 线性代数统一布局表示与转换 | [概要](linear_layouts/论文概要.md) · [中文解读](linear_layouts/论文中文解读.md) · [PDF](linear_layouts/paper.pdf) |

> Linear Layouts 于 2025 年 5 月首次上 arXiv，正式发表于 2026 年 3 月的 ASPLOS 2026；这里用“首次公开时间 / 正式发表时间”同时标注，避免时间线误导。

## 二、四篇论文分别解决什么问题

### 1. 2019：怎样把 GPU 编程从 thread-level 提升到 tile-level？

CUDA 让程序员直接处理线程、共享内存和同步，性能很强，但开发门槛高。Triton 的核心选择是：程序员表达“一个 program instance 如何处理一个 tile”，编译器负责把 tile 映射到线程、warp、共享内存和全局内存。

这篇论文确立了 Triton 的基本哲学：不是隐藏所有硬件细节，也不是让用户逐线程编程，而是选择一个足够接近算法、同时仍能生成高性能代码的抽象层。

### 2. 2024：怎样让普通 PyTorch 程序自动落到 Triton？

PyTorch 2 把问题拆成两个主要阶段：TorchDynamo 从动态 Python 中提取 FX graph，TorchInductor 再做融合、调度和代码生成；GPU 端通常生成 Triton kernel。

这篇论文说明 Triton 的影响不只来自手写 kernel。它更重要的工业角色，是承接上层编译器自动产生的大量融合算子。论文中的整体加速不能全部归功于 Triton，因为 Dynamo 捕获、AOTAutograd 分解、Inductor 融合和模板库共同贡献了结果。

### 3. 2025：LLM 能不能自动写 Triton kernel？

TritonBench 建立两个互补集合：184 个来自真实开源仓库的 Triton 算子，以及 166 个从 PyTorch 语义构造的融合任务。它同时检查代码能否调用、能否正确执行以及是否真正加速。

结果的重点不是“某模型会不会补全语法”，而是：在真实算子集合上，即使强模型的执行正确率仍只有约四分之一；性能正确性比文本相似度难得多。这个基准也提醒我们，能运行、数值正确和比基线快是三个不同门槛。

### 4. 2025/2026：怎样统一不断膨胀的 GPU layout 规则？

随着 NVIDIA、AMD 等架构加入更多矩阵指令、warp 组织和共享内存访问模式，旧式“每种 layout 单独写规则”的办法会产生组合爆炸。Linear Layouts 把硬件资源位到逻辑张量坐标位的映射表示为 GF(2) 上的线性变换，用统一代数处理 reshape、broadcast、layout conversion、shuffle 与 shared-memory swizzle。

它的最大意义是编译器工程的正确性与可扩展性。真实 benchmark 的平均提升是 1.07×、最高 1.40×；不能只摘最高值，把它宣传成普遍 40% 加速。

## 三、推荐阅读顺序

如果目标是理解 Triton：

1. 先读 2019 论文的概要，建立 tile、program instance、layout 和自动并行化的直觉。
2. 再读 PyTorch 2，明确 Triton 在端到端系统中的位置：它是 GPU backend 的关键一层，不等于整个 `torch.compile`。
3. 读 TritonBench，理解“写一个 kernel”中语义、边界、正确性和性能调优的实际难度。
4. 最后读 Linear Layouts；它偏编译器内部，适合在已经理解 warp、shared memory、layout conversion 后阅读。

如果目标是实际写 kernel，可以采用 `2019 概要 → TritonBench 详细解读 → Linear Layouts 概要` 的短路线；如果目标是研究编译器，则建议四篇详细解读全部按时间顺序读。

## 四、概念演化图

```text
PyTorch / 上层模型
        │
        │ TorchDynamo 捕获 + AOTAutograd 分解
        ▼
TorchInductor：融合、调度、索引化简
        │
        │ 生成 Triton kernel
        ▼
Triton tile-level 程序
        │
        │ layout 推导、转换、硬件 intrinsic lowering
        ▼
GPU 线程 / warp / 寄存器 / shared memory

TritonBench 横向检查：生成的 kernel 是否可调用、正确、且有性能收益？
Linear Layouts 纵向改造：tile 到硬件资源的映射怎样统一、正确、高效？
```

## 五、读数时最容易犯的四个错误

1. **把 2019 原型等同于当前 Triton。** 奠基论文使用 C 风格前端、GTX 1070 和当年的编译流程；今天常见的是 Python DSL、MLIR 后端和新一代 GPU。
2. **把 PyTorch 2 的端到端加速全部归于 Triton。** 图捕获、算子分解、融合、调度、模板与 Triton codegen 缺一不可。
3. **把 TritonBench 的 speedup 与正确率分开看。** 速度通常只对成功且正确的样本统计，不能用少数幸存 kernel 的高加速掩盖低成功率。
4. **把 Linear Layouts 的局部 14.20× 当成整体收益。** 该数字来自特定 gather 微基准；265 个真实用例的平均值是 1.07×。

## 六、文件约定

每篇目录均包含：

- `paper.pdf`：论文原文；
- `paper.txt`：由 PDF 提取、保留大致版面的文本，便于全文检索；
- `论文概要.md`：快速了解贡献、关键结果和边界；
- `论文中文解读.md`：按章节、图表、方法、实验和局限展开的长篇解读；
- `rendered_figures/`：从论文源码导出的独立图表；不保存整页文字截图。

在线原文入口：[Triton 2019](https://www.eecs.harvard.edu/~htk/publication/2019-mapl-tillet-kung-cox.pdf) · [PyTorch 2](https://docs.pytorch.org/assets/pytorch2-2.pdf) · [TritonBench](https://arxiv.org/abs/2502.14752) · [Linear Layouts](https://arxiv.org/abs/2505.23819)
