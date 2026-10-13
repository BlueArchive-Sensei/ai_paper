# Paper Reading Notes

本仓库保存 AI 论文原文、可检索文本、论文概要和中文精读。当前共 141 篇完整资料，阅读入口按“通用模型算法、AI Compiler、厂商定制实现”三条主线组织。

## 中文优先阅读约定

- `论文中文解读.md` 是默认入口：读完它就能学会这篇论文——背景、方法、公式推导、算法步骤、实验设置、主结果、消融、局限和常见误读都写成中文，不需要再翻英文原文。
- 每篇都嵌入论文**原图**：从原文 PDF 里按图裁出，不是整页截图；每张图配中文图题、图中文字翻译、读法和读图结论。
- 原文表格逐格转录成 Markdown 表：表头和行名译成中文，数字、模型名、数据集名保持原样，并注明原文表号和页码；表太大时只摘关键行并说明。
- 从图上读出的近似数值一律标“约”；原文自身前后矛盾或笔误的地方会在文中标注，而不是悄悄改掉。
- 专有名词第一次出现时保留英文，例如“性能缺口恢复比例（performance gap recovered, PGR）”。
- 仓库现有 1,437 张论文原图，见各论文目录下的 `rendered_figures/`；不使用整页截图或大段正文截图。

## 从这里开始：三条主线

| 主线 | 你会学到什么 | 入口 |
|---|---|---|
| 模型基础理论与最新算法 | LSTM、Transformer、Attention、Scaling、MoE、SSM、Reasoning、推测解码、扩散、多模态 | [AI 模型基础理论与算法演进索引](AI模型基础理论与算法演进索引.md) |
| AI Compiler 与运行时 | 动态图捕获、IR、lowering、fusion、autotuning、kernel DSL、分布式编译、runtime | [AI Compiler、Kernel DSL 与运行时演进索引](AI编译器与运行时演进索引.md) |
| 厂商模型与定制实现 | DeepSeek、OpenAI、Anthropic、MiniMax、Kimi、Qwen、Llama、Gemini、Ascend、NVIDIA | [AI 厂商模型、训练系统与部署实现索引](AI厂商模型与系统实现索引.md) |

## 分类边界

| 例子 | 主归类 | 原因 |
|---|---|---|
| Transformer、RoPE、Mamba、DDPM | 模型算法 | 贡献是可迁移的架构或训练方法 |
| MoE、CoT、PRM、test-time scaling | 近代高级算法 | 分别扩展条件容量或单题推理计算 |
| Speculative decoding、Medusa、EAGLE | 近代高级算法 | 是可迁移的解码算法，不是某家 serving 产品 |
| FlashAttention 1–4 | 模型/Attention 算法 | 改变 exact Attention 的 IO 和硬件算法，不是完整编译器 |
| XLA、TVM、MLIR、Triton、TensorIR | AI Compiler | 贡献是 IR、lowering、schedule 或 codegen |
| DeepSeek-V3、GPT-4、Claude 3、Qwen3 | 厂商实现 | 是具体模型族的架构、训练和发布报告 |
| CloudMatrix384、Mooncake、TensorRT-LLM | 厂商实现 | 是面向特定模型、硬件或产品的部署系统 |

跨层论文可以从多个索引找到，但只有一个主归类，避免重复时间线造成概念混淆。

## 推荐阅读方式

### 学模型算法

1. LSTM → Seq2Seq → Bahdanau Attention → Transformer。
2. GPT-1 / BERT / T5 → Scaling Laws → Chinchilla。
3. RoPE / ALiBi / MQA / GQA → FlashAttention 1–4。
4. VAE / GAN → DDPM → Latent Diffusion → DiT。
5. Mamba → Mamba-2，理解 Attention 之外的序列建模。

### 学近代高级算法

1. MoE：Sparsely-Gated MoE → Switch Transformer → MegaBlocks → DeepSeekMoE。
2. Reasoning：CoT → Self-Consistency → Tree of Thoughts → PRM → compute-optimal scaling → s1。
3. Speculative decoding：两篇基础 draft–verify → SpecInfer → Medusa → EAGLE → EAGLE-2。
4. 用 [近代高级算法专题索引](近代高级算法论文阅读索引.md) 对照三条路线的优化目标、成本和评测口径。

### 学 AI Compiler

1. XLA / TVM / Glow：为什么需要整图与多层 IR。
2. MLIR / TensorIR：怎样保存不同抽象层的语义。
3. Ansor / MetaSchedule / Roller / Bolt：怎样搜索 schedule。
4. Triton / Hidet / TileLang / CuTe：怎样表达 GPU tile、layout 和 pipeline。
5. GSPMD / Alpa：怎样把分片和通信纳入编译计划。

### 看厂商工程落地

1. DeepSeekMoE → V2 → V3 → R1。
2. Mooncake / CloudMatrix384 / TensorRT-LLM：模型怎样进入 serving。
3. InstructGPT / DeepSeek-R1 / Kimi k1.5 / MiniMax-M1：reasoning RL 横向对照。
4. OpenAI / Anthropic / Qwen / Llama / Gemini：比较公开内容与未披露边界。

## 专题索引

| 专题 | 入口 |
|---|---|
| MoE、Reasoning/test-time scaling 与 Speculative decoding | [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md) |
| AI 安全、对齐欺骗、越狱与控制 | [AI 安全论文阅读索引](AI安全论文阅读索引.md) |
| 强化学习与知识蒸馏 | [强化学习与蒸馏论文阅读索引](强化学习与蒸馏论文阅读索引.md) |
| PyTorch 动态图与 Graph 编译 | [PyTorch 动态图与 Graph 编译论文阅读索引](PyTorch动态图与Graph编译论文阅读索引.md) |
| Triton 与 GPU layout | [Triton 论文阅读索引](Triton论文阅读索引.md) |
| GPU 融合、MoE Kernel 与推理系统 | [GPU 内核融合与大模型推理论文阅读索引](GPU内核融合与大模型推理论文阅读索引.md) |
| 全量 Markdown 审核 | [论文精读 GitHub Markdown 审核报告](论文精读Markdown审核报告.md) |

## 每篇论文的目录结构

每篇资料通常包含：

- `paper.pdf`：论文或官方资料原文；
- `paper.txt`：可全文检索的文本；
- `论文概要.md`：快速理解问题、方法、证据与局限；
- `论文中文解读.md`：公式、论证链、实验、复现和证据边界；
- `rendered_figures/`：中文解读里引用的论文原图（按图裁剪的 PNG/JPG），文件名为 `fig<编号>-<英文短词>`；不存放整页或正文段落截图。

XLA、TensorRT-LLM、CuTeDSL、Anthropic 的网页型报告等少数资料来自官方页面快照，目录中会明确说明它们不是同行评审论文；这类资料的图取自页面里的原图。

## 精读质量与审核

- 141/141 篇均有 PDF、可检索文本、概要、中文解读和证据导航。
- 2026-10-12 对 141 篇逐篇对照原文重新核对并重写：共嵌入 1,437 张原图，转录 1,700 张 Markdown 表（含少量整理汇总表），解读合计约 531 万字符。
- 核对中纠出并改正了大量旧稿错误（数字、公式、术语、结论方向、页码定位），其中事实性错误同步改在对应的 `论文概要.md` 和各索引文件里；每篇解读都在文中列出原文自身的矛盾与未解决项。
- 发现并更正一处资料错放：`roller/` 里原来的 `paper.pdf` / `paper.txt` 是一篇天文学论文，现已换成 OSDI '22 的 Roller 官方 PDF。
- 全部 Markdown 文件通过 `tools/mdlint.py`（GitHub 渲染检查：中文加粗、行内与行间公式、表格列数、尖括号标签、锚点与相对链接等），0 个错误。
- 逐篇统计和审核过程见 [论文精读 GitHub Markdown 审核报告](论文精读Markdown审核报告.md)。

## 工具

[tools/](tools/README.md) 里有裁图脚本（`fig.py`）、Markdown 检查脚本（`mdlint.py`）、统计脚本（`audit.py`）和中文解读的写作规范。新增或修改解读后运行 `tools/mdlint.py <目录>`，应输出 0 errors。
