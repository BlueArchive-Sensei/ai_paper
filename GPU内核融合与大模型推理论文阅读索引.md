# GPU 内核融合、MoE 与大模型推理论文阅读索引

> 整理日期：2026-10-05
>
> 本专题新增 10 篇论文与 2 份官方工程资料。每个目录均保存 PDF、可检索文本、论文概要、中文精读和原文证据导航；不保存论文正文截图。TensorRT-LLM 与 PyTorch CuTeDSL 两项没有被包装成学术论文，目录中已明确标注资料性质与快照日期。

Speculative decoding、Medusa 与 EAGLE 属于通用解码算法，主归类在 [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md)；本索引只在讨论 target verification kernel、batch、KV 与 serving runtime 时与它们交叉。

## 1. 五条推荐阅读路线

### 路线 A：Kernel Fusion 从规则走向全局 orchestration

1. [FusionStitching](fusion_stitching/论文中文解读.md)：不同并行度算子如何在一个 kernel 中用 register、shuffle、shared memory 交换中间值。
2. [Welder](welder/论文中文解读.md)：把融合单位从 operator 降到 tile，用多级 memory traffic 统一 intra/inter-operator 优化。
3. [Korch](korch/论文中文解读.md)：先 fission operator，再用候选 profiling 与二元线性规划决定 kernel 边界。
4. [MPK](mirage_persistent_kernel/论文中文解读.md)：跨越静态 fusion，进入带设备侧 scheduler 的模型级 persistent megakernel。
5. [Event Tensor](event_tensor/论文中文解读.md)：让动态 shape 和 data-dependent dependency 成为 megakernel compiler 的一等对象。

核心演进：

    pattern fusion
        → heterogeneous stitching
        → tile/memory-level planning
        → operator fission + global orchestration
        → persistent megakernel + device scheduling

### 路线 B：从 MoE 算法到 MoE kernel

1. [Sparsely-Gated MoE](sparsely_gated_moe/论文中文解读.md)：noisy top-k、专家并行、importance/load balancing。
2. [Switch Transformer](switch_transformers/论文中文解读.md)：top-1、capacity factor、token dropping 与稳定训练。
3. [MegaBlocks](megablocks/论文中文解读.md)：把动态 expert batches 表示成 block sparsity，去掉 dropping/padding 二选一。
4. [MPK 的 MoE case](mirage_persistent_kernel/论文中文解读.md#9-moe-与多-gpu)：在同一 tGraph 融合 routing、dispatch、expert compute、combine。
5. [Event Tensor 的 MoE case](event_tensor/论文中文解读.md#6-moe-与通信融合)：用 runtime-computed event indices 表达 top-k 路由。

这条路线要始终同时看四个量：

- 模型质量：是否 drop token，router 是否塌缩；
- kernel：expert GEMM shape 与 block utilization；
- 通信：all-to-all/collective；
- runtime：动态 batch、KV 与设备侧调度。

### 路线 C：MegaKernel 专题

1. [MPK](mirage_persistent_kernel/论文概要.md)：通用 SM-level graph、event runtime、AOT/JIT hybrid dispatch。
2. [Event Tensor](event_tensor/论文概要.md)：统一 static/dynamic schedule 和 shape/data dynamism。
3. [Ada-MK](ada_mk/论文概要.md)：资源受限 Ada GPU 上的 offline DAG search 与 TensorRT-LLM plugin。

三篇不是简单迭代：

| 论文 | 主要假设 | 调度重点 | 典型甜点区 |
| --- | --- | --- | --- |
| MPK | 模型可降成 SM tasks | 通用 event-driven runtime | 小 batch、跨 operator pipeline、多 GPU |
| Event Tensor | dependency 可表示成 tensor | static/dynamic 同 IR 切换 | dynamic shape、MoE、AOT serving |
| Ada-MK | 部署配置大体固定 | 离线搜索并固化路径 | L20、小模型、W4A16、低延迟 decode |

### 路线 D：理解 TensorRT-LLM

1. [TensorRT-LLM Architecture](tensorrt_llm_architecture/论文中文解读.md)：先建立 API、Scheduler、KVCacheManager、ModelEngine、Sampler 的系统地图。
2. [FusionStitching](fusion_stitching/论文概要.md) 与 [Welder](welder/论文概要.md)：理解 kernel fusion 不是无限合并。
3. [Switch Transformer](switch_transformers/论文概要.md) 与 [MegaBlocks](megablocks/论文概要.md)：理解 MoE 的算法与 grouped/block-sparse kernel 约束。
4. [Ada-MK](ada_mk/论文中文解读.md)：看 MegaKernel 如何作为 plugin 嵌入成熟 runtime，而不是替换整套系统。
5. [PyTorch CuTeDSL Backend](cutedsl_torchinductor/论文中文解读.md)：理解现代推理栈为何同时使用库 kernel、Triton、CUTLASS/CuTeDSL。

注意三个不同项目：

| 名称 | 含义 |
| --- | --- |
| TensorRT-LLM | NVIDIA 的 LLM kernel、KV、scheduler 与 execution runtime |
| Triton Inference Server | 模型服务端，可加载 TensorRT-LLM backend |
| OpenAI Triton | GPU kernel 编程语言与编译器 |

### 路线 E：CuTe DSL 与 Triton 对比

1. [Triton 论文](triton_compiler/论文中文解读.md)：理解 block-level tiled programming。
2. [Linear Layouts](linear_layouts/论文中文解读.md)：理解现代 Triton 用 $\mathbb{F}_2$ 线性映射统一 layout codegen。
3. [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md)：理解 hierarchy、shape/stride、composition、inverse 与 thread-value mapping。
4. [TorchInductor CuTeDSL Backend](cutedsl_torchinductor/论文中文解读.md)：在 B200 的真实 autotuning pipeline 中看 ATen、Triton 与 CuTeDSL 如何竞争。

简表：

| 维度 | Triton | CuTe DSL |
| --- | --- | --- |
| 主要编程层次 | block/tile program | thread、warp、CTA、cluster 与硬件 atom |
| Layout 控制 | 编译器主导，现代实现用 Linear Layouts | 显式 CuTe hierarchy/layout algebra |
| 开发体验 | 较高层，适合快速自定义 kernel | 更低层，常从优化模板/config 出发 |
| 常见强项 | pointwise、reduction、通用融合 | 最新 NVIDIA GEMM/attention、FP8/FP4、特殊 MMA/TMA/TMEM |
| 可移植性目标 | 编译器可支持多类 GPU backend | NVIDIA CUDA/CUTLASS 生态 |
| 风险 | 新硬件细节可能暴露较晚 | 学习、配置和维护复杂度更高 |

不存在脱离具体 kernel、shape、GPU 和版本的“谁总是更快”。PyTorch 报告给出的合理答案是：生成多个 backend candidates，在目标设备上 autotune。

## 2. 全部资料快速对照

| 年份 | 资料 | 类型 | 核心抽象 | 代表证据 |
| --- | --- | --- | --- | --- |
| 2017 | [Sparsely-Gated MoE](sparsely_gated_moe/论文概要.md) | 论文 | noisy top-k gate | 固定计算、4096 experts 时 perplexity 改善 |
| 2020 | [FusionStitching](fusion_stitching/论文概要.md) | 论文 | stitching schemes | 相对 XLA 平均 1.45× |
| 2022 | [Switch Transformer](switch_transformers/论文概要.md) | 论文 | top-1 + capacity | 扩展到 1.6T 总参数 |
| 2023 | [Welder](welder/论文概要.md) | 论文 | tile-graph | V100 多模型相对 TensorRT 平均约 1.47× |
| 2023 | [MegaBlocks](megablocks/论文概要.md) | 论文 | block-sparse MoE | dropless training 最高 4.35× vs padding |
| 2024 | [Korch](korch/论文概要.md) | 论文 | fission + BLP | V100/A100 平均 1.39×/1.30× |
| 2025 | [MPK](mirage_persistent_kernel/论文概要.md) | 预印本 | SM-level tGraph | 相对 vLLM/SGLang 约 1.0×–1.7× |
| 2026 | [Event Tensor](event_tensor/论文概要.md) | 预印本 | dependency tensor | dynamic megakernel + AOT warmup |
| 2026 | [Ada-MK](ada_mk/论文概要.md) | 预印本 | offline DAG search | L20/TRT-LLM batch 1 最高 +23.6% |
| 2026 | [CuTe Layout Algebra](cute_layout_algebra/论文概要.md) | 预印本 | layout algebra | 表示、验证与推导，不以 benchmark 为主 |
| 2026 | [TensorRT-LLM Architecture](tensorrt_llm_architecture/论文概要.md) | 官方文档 | executor/KV/scheduler | 版本化架构快照 |
| 2026 | [TorchInductor CuTeDSL](cutedsl_torchinductor/论文概要.md) | 官方报告 | backend portfolio | B200 GEMM 最高 1.78×，E2E 最高 6.5% |

## 3. Fusion、CUDA Graph 与 MegaKernel 的区别

| 机制 | 主要减少什么 | kernel 边界 | 动态性 | 新代价 |
| --- | --- | --- | --- | --- |
| Operator fusion | HBM 中间值、部分 launch | 局部消失 | 通常静态 | register/SMEM、occupancy、codegen |
| CUDA Graph | host launch/API overhead | 仍存在 | shape 受限，多图/填充 | capture、graph cache、padding |
| Persistent/MegaKernel | launch、边界同步、HBM，并开放跨算子 pipeline | 大范围消失 | 需设备侧 runtime/抽象 | scheduler、queue、barrier、调试 |

因此“一次 launch”本身不保证快。若 MegaKernel 内仍全局串行，只省 launch；真正额外收益来自 tile-level overlap、prefetch、通信重叠和动态负载均衡。

## 4. 读性能图时必须锁定的口径

### Kernel Fusion

- 端到端还是只测 memory-intensive 子图？
- 对比 eager、XLA、TensorRT、TVM 的哪个版本？
- 是否包含 compile/autotune？
- bytes、launch 数、occupancy 是否同时报告？

### MoE

- total/active parameters；
- top-k、expert 数、capacity factor、drop rate；
- tokens/expert 与 micro-batch；
- permutation 与 all-to-all 是否计时；
- 达到相同 loss，还是只比 steps/s？

### MegaKernel/LLM serving

- offline batch 还是 online arrival；
- TTFT、TPOT、throughput、P99 哪个目标；
- input/output length 与 quantization；
- CUDA Graph、continuous batching、paged attention 是否开启；
- compile/warmup 是否移到离线而非真正消失。

### CuTe/Triton

- 具体 GPU generation；
- dtype 与 shape，尤其 GEMM 的 M/N/K；
- winner baseline 是 ATen/cuBLAS 还是 Triton；
- cold compile 与 warm cache；
- 数值精度和量化 scale layout。

## 5. 一个统一的成本模型

这些论文可以放在同一式子下理解：

$$
T_{e2e}=
T_{compute}+T_{memory}+T_{launch}
+T_{sync}+T_{communication}+T_{scheduling}
+T_{padding/imbalance}.
$$

- FusionStitching/Welder/Korch 主要减少 memory 与 launch，但可能增加 compute/sync。
- MegaBlocks 主要减少 padding/imbalance，同时保持 GEMM throughput。
- MPK/Event Tensor/Ada-MK 减少 launch 与 coarse sync，但增加 device scheduling。
- TensorRT-LLM 在请求、KV、kernel 与 distributed runtime 间做系统级权衡。
- CuTeDSL/Triton 改变单 kernel 的 compute/memory/codegen 点，但端到端收益受其时间占比限制。

## 6. 推荐实践顺序

若目标是优化一个真实 LLM/MoE workload：

1. 先 profile：区分 prefill/decode、compute/memory/launch/communication。
2. 先用库 kernel 或 Triton 建正确 baseline。
3. 对局部 memory-bound chain 做 fusion，观察 HBM bytes 与 occupancy。
4. MoE 先看 routing/load/padding，再决定 grouped GEMM 或 block sparse。
5. 只有 kernel launch/coarse boundary 成为显著瓶颈时，再考虑 MegaKernel。
6. CuTeDSL 用于确有硬件控制收益的 shapes，并让 autotuner 与 ATen/Triton 竞争。
7. 最终用真实 arrival、长度分布和 SLO 复验，不以 microbenchmark 替代系统结果。

## 7. 版本提醒

- MPK、Event Tensor、Ada-MK、CuTe Layout Algebra 均为快速演进的预印本。
- TensorRT-LLM 文档与 PyTorch 报告是 2026-10-03 保存的工程快照，未来 API/版本会变化。
- 仓库中的 Triton 2019 论文解释原始语言设计；现代 Triton layout 与后端能力应结合 Linear Layouts 和当前实现。
- CuTe Layout Algebra 明确区分 PyCuTe、C++ CuTe 与 CuTe DSL，不应把三者混称为同一个编译器。
