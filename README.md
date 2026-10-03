# Paper Reading Notes

本仓库收录人工整理的论文原文、可检索文本、论文概要、中文详细解读与关键页面截图，主题主要覆盖 AI 安全和 Triton/GPU 编译。

## 阅读索引

- [AI 安全论文阅读索引](AI安全论文阅读索引.md)
- [AI 安全论文详细解读索引](AI安全论文详细解读索引.md)
- [Triton 论文阅读索引](Triton论文阅读索引.md)

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

## Triton 与 GPU 编译论文

| 时间 | 目录 | 论文 |
|---|---|---|
| 2019 | [`triton_compiler`](triton_compiler/) | Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations |
| 2024 | [`pytorch_2`](pytorch_2/) | PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation |
| 2025 | [`tritonbench`](tritonbench/) | TritonBench |
| 2025/2026 | [`linear_layouts`](linear_layouts/) | Linear Layouts: Robust Code Generation of Efficient Tensor Computation Using F2 |
| 2026 | [`taming_bitwise_gpu_kernels`](taming_bitwise_gpu_kernels/) | Taming Bitwise Behavior in GPU Kernels with Tensor Core |

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

## 新增论文检查表

1. 使用唯一、可读的英文短标题作为目录名。
2. 保存原始 PDF，并记录论文链接、作者、公开时间和版本。
3. 从 PDF 提取可检索文本。
4. 分别编写概要与中文详细解读，不把两者混为同一文档。
5. 只渲染解读实际引用的关键页面。
6. 把论文加入相应主题索引，并检查所有相对链接。

## 文件规模

仓库包含 PDF 和论文截图。当前单文件均低于 GitHub 的 100 MB 限制，因此暂不要求 Git LFS；后续若加入超大附件，应在提交前检查文件大小并单独决定是否使用 LFS。
