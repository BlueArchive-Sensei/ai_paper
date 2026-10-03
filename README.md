# Paper Reading Notes

本仓库收录人工整理的论文原文、可检索文本、论文概要、中文详细解读与关键页面截图，主题覆盖 AI 安全、强化学习与知识蒸馏、PyTorch 动态图与 Graph 编译，以及 GPU 编译、Kernel、MoE 与大模型推理系统。

## 阅读索引

- [AI 安全论文阅读索引](AI安全论文阅读索引.md)
- [强化学习与蒸馏论文阅读索引](强化学习与蒸馏论文阅读索引.md)
- [PyTorch 动态图与 Graph 编译论文阅读索引](PyTorch动态图与Graph编译论文阅读索引.md)
- [Triton 论文阅读索引](Triton论文阅读索引.md)
- [GPU 内核融合、MoE 与大模型推理论文阅读索引](GPU内核融合与大模型推理论文阅读索引.md)

## AI 安全论文

| 时间 | 目录 | 论文 |
|---|---|---|
| 2022 | [`constitutional_ai`](constitutional_ai/) | Constitutional AI: Harmlessness from AI Feedback |
| 2023 | [`jailbroken`](jailbroken/) | Jailbroken: How Does LLM Safety Training Fail? |
| 2023 | [`ai_control`](ai_control/) | AI Control: Improving Safety Despite Intentional Subversion |
| 2023 | [`weak_to_strong`](weak_to_strong/) | Weak-to-Strong Generalization |
| 2024 | [`sleeper_agents`](sleeper_agents/) | Sleeper Agents |
| 2024 | [`simple_adaptive_attacks`](simple_adaptive_attacks/) | Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks |
| 2024 | [`mechanistic_interpretability`](mechanistic_interpretability/) | Mechanistic Interpretability for AI Safety: A Review |
| 2024 | [`sycophancy_to_subterfuge`](sycophancy_to_subterfuge/) | Sycophancy to Subterfuge |
| 2024 | [`alignment_faking`](alignment_faking/) | Alignment Faking in Large Language Models |
| 2025 | [`emergent_misalignment`](emergent_misalignment/) | Emergent Misalignment |
| 2025 | [`shade_arena`](shade_arena/) | SHADE-Arena |
| 2026 | [`exploitgym`](exploitgym/) | ExploitGym |

## 强化学习与知识蒸馏论文

| 时间 | 目录 | 论文 |
|---|---|---|
| 2015 | [`deep_q_network`](deep_q_network/) | Human-level Control through Deep Reinforcement Learning |
| 2015 | [`knowledge_distillation`](knowledge_distillation/) | Distilling the Knowledge in a Neural Network |
| 2016 | [`policy_distillation`](policy_distillation/) | Policy Distillation |
| 2017 | [`proximal_policy_optimization`](proximal_policy_optimization/) | Proximal Policy Optimization Algorithms |
| 2017 | [`distral`](distral/) | Distral: Robust Multitask Reinforcement Learning |
| 2017 | [`human_preferences_rl`](human_preferences_rl/) | Deep Reinforcement Learning from Human Preferences |
| 2018 | [`soft_actor_critic`](soft_actor_critic/) | Soft Actor-Critic |
| 2020 | [`muzero`](muzero/) | Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model |

## PyTorch 动态图与 Graph 编译

| 时间 | 类型 | 目录 | 资料 |
|---|---|---|---|
| 2017 | 论文 | [`dynamic_computation_graphs`](dynamic_computation_graphs/) | Deep Learning with Dynamic Computation Graphs |
| 2019 | 论文 | [`chainer_define_by_run`](chainer_define_by_run/) | Chainer: A Deep Learning Framework for Accelerating the Research Cycle |
| 2019 | 论文 | [`pytorch_imperative`](pytorch_imperative/) | PyTorch: An Imperative Style, High-Performance Deep Learning Library |
| 2019 | 论文 | [`janus_symbolic_graph`](janus_symbolic_graph/) | JANUS |
| 2021 | 论文 | [`nimble_dynamic_nn`](nimble_dynamic_nn/) | Nimble |
| 2021 | 论文 | [`disc_dynamic_shape`](disc_dynamic_shape/) | DISC |
| 2022 | 论文 | [`torch_fx`](torch_fx/) | torch.fx |
| 2024 | 论文 | [`pytorch_2`](pytorch_2/) | PyTorch 2 |
| 2026 | 官方文档 | [`pytorch_graph_programming_model`](pytorch_graph_programming_model/) | Dynamo、torch.export 与 Dynamic Shapes Programming Model |

## GPU 编译、Kernel 与大模型推理

| 时间 | 类型 | 目录 | 资料 |
|---|---|---|---|
| 2017 | 论文 | [`sparsely_gated_moe`](sparsely_gated_moe/) | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer |
| 2019 | 论文 | [`triton_compiler`](triton_compiler/) | Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations |
| 2020 | 论文 | [`fusion_stitching`](fusion_stitching/) | FusionStitching |
| 2022 | 论文 | [`switch_transformers`](switch_transformers/) | Switch Transformers |
| 2023 | 论文 | [`welder`](welder/) | Welder: Scheduling Deep Learning Memory Access via Tile-graph |
| 2023 | 论文 | [`megablocks`](megablocks/) | MegaBlocks: Efficient Sparse Training with Mixture-of-Experts |
| 2024 | 论文 | [`pytorch_2`](pytorch_2/) | PyTorch 2 |
| 2024 | 论文 | [`korch`](korch/) | Optimal Kernel Orchestration for Tensor Programs with Korch |
| 2025 | 论文 | [`tritonbench`](tritonbench/) | TritonBench |
| 2025/2026 | 论文 | [`linear_layouts`](linear_layouts/) | Linear Layouts |
| 2025 | 预印本 | [`mirage_persistent_kernel`](mirage_persistent_kernel/) | MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs |
| 2026 | 论文 | [`taming_bitwise_gpu_kernels`](taming_bitwise_gpu_kernels/) | Taming Bitwise Behavior in GPU Kernels with Tensor Core |
| 2026 | 预印本 | [`event_tensor`](event_tensor/) | Event Tensor |
| 2026 | 预印本 | [`ada_mk`](ada_mk/) | Ada-MK |
| 2026 | 预印本 | [`cute_layout_algebra`](cute_layout_algebra/) | CuTe Layout Representation and Algebra |
| 2026 | 官方文档 | [`tensorrt_llm_architecture`](tensorrt_llm_architecture/) | TensorRT LLM Architecture Overview |
| 2026 | 官方报告 | [`cutedsl_torchinductor`](cutedsl_torchinductor/) | TorchInductor CuTeDSL Backend |

## 目录命名约定

论文目录使用可读的英文短标题和 `lowercase_snake_case`：

```text
paper_short_title/
├── paper.pdf
├── paper.txt
├── 论文概要.md
├── 论文中文解读.md
└── rendered_figures/
```

- 目录名表达论文内容，不再使用只有编号的 `arxiv_YYMM.NNNNN`。
- `论文概要.md` 用于快速浏览；`论文中文解读.md` 是详细版本。
- `paper.txt` 由 PDF 提取，便于全文搜索，不替代排版后的原文。
- `rendered_figures/` 保存解读实际引用的原论文页面。
- 个别论文可能包含额外的源码归档或实验材料。
- 官方工程资料会明确标注来源性质、快照日期，并保留原始 Markdown/HTML。

## 新增论文检查表

1. 使用唯一、可读的英文短标题作为目录名。
2. 保存原始 PDF，并记录论文链接、作者、公开时间和版本。
3. 从 PDF 提取可检索文本。
4. 分别编写概要与中文详细解读，不把两者混为同一文档。
5. 只渲染解读实际引用的关键页面。
6. 把论文加入相应主题索引，并检查所有相对链接。
7. 非论文资料必须标明类型、来源与快照时间。

## 文件规模

仓库包含 PDF 和论文截图。当前单文件均低于 GitHub 的 100 MB 限制，因此暂不要求 Git LFS；后续若加入超大附件，应在提交前检查文件大小并单独决定是否使用 LFS。
