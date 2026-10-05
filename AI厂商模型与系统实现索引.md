# AI 厂商模型、训练系统与部署实现索引

> 整理日期：2026-10-05
> 这条主线按公司和产品族组织，回答“某家公司把通用算法组合成了什么模型、训练系统和部署栈”。
> 通用模型理论请看 [AI 模型基础理论与算法演进索引](AI模型基础理论与算法演进索引.md)；编译器方法请看 [AI Compiler 与运行时演进索引](AI编译器与运行时演进索引.md)。

## 1. 本索引的分类规则

| 类型 | 这里怎样处理 |
|---|---|
| 公司模型技术报告 | 按厂商放置，记录架构、数据、训练和披露边界 |
| 模型卡或系统卡 | 用于理解能力、安全和发布边界，不反推未披露架构 |
| 开放权重模型 | 单独记录许可证、权重和代码开放程度 |
| 训练/推理系统 | 记录并行、通信、KV cache、量化、scheduler 与硬件依赖 |
| 通用算法论文 | 只保留厂商路线交叉入口，主解释放在算法索引 |
| 编译器论文 | 只保留与具体产品栈相关的入口，主解释放在 Compiler 索引 |

“论文公开、权重开放、代码开放、训练可复现”是四件不同的事：

| 开放层次 | 含义 |
|---|---|
| 论文/报告公开 | 可以阅读方法和结果 |
| 权重开放 | 可以下载 checkpoint 做推理或微调 |
| 代码开放 | 有推理、训练、kernel 或系统实现 |
| 可复现训练 | 数据、配方、代码和算力信息足以重建模型 |

前沿模型很少同时满足四层。索引不把“发布了一份技术报告”写成“完整开源”。

## 2. DeepSeek：MoE、MLA、训练系统与 Reasoning

| 时间 | 资料 | 主要公开内容 | 主层次 |
|---|---|---|---|
| 2024 | [DeepSeekMoE](deepseek_moe/论文中文解读.md) | 细粒度 experts、shared experts 与路由 | 架构 |
| 2024 | [DeepSeek-V2](deepseek_v2/论文中文解读.md) | MLA、DeepSeekMoE、device-limited routing | 架构 + 推理效率 |
| 2024 | [DeepSeek-V3](deepseek_v3/论文中文解读.md) | auxiliary-loss-free balancing、MTP、DualPipe、FP8 | 训练系统 |
| 2025 | [DeepSeek-R1](deepseek_r1/论文中文解读.md) | GRPO、verifier、cold start、多阶段 RL 与蒸馏 | 后训练 |

DeepSeek-R1 是具体厂商训练系统；CoT、多路径、PRM 和 test-time scaling 的通用算法演进请先看 [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md)。

### 推荐顺序

DeepSeekMoE → V2 → V3 → R1。

- MoE 解释参数容量和 expert 路由。
- V2 引入 MLA，改变 KV cache 和 Attention kernel。
- V3 把架构推进到 FP8、流水并行与集群训练。
- R1 主要改变后训练和输出计算，不是重新发明基础网络。

## 3. Huawei Ascend × DeepSeek：硬件适配与超节点 Serving

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2025 | [CloudMatrix384 / CloudMatrix-Infer](ascend_cloudmatrix384/论文中文解读.md) | UB 超节点、EP320、P/D/C 解耦、INT8 与 DeepSeek-R1 serving |

算法到 Ascend 系统的映射：

| DeepSeek workload | Ascend/CANN/系统要解决的问题 |
|---|---|
| MLA | latent KV、特殊 Attention kernel、cache pool 与权重吸收 |
| DeepSeekMoE | token dispatch/combine、expert load、all-to-all |
| MTP | candidate generation、verification 与多 token pipeline |
| 长 CoT | decode 吞吐、KV 生命周期、TPOT 与在线 goodput |

边界：

- 模型能加载不等于吞吐和尾延迟已优化。
- CloudMatrix384 是超节点系统，结果不能直接外推到普通 8 卡 Ascend 服务器。
- CANN、MindIE、vLLM-Ascend 的版本化指南属于工程文档，不应伪装成算法论文。

## 4. OpenAI：预训练、代码、RLHF、闭源报告与开放权重

| 时间 | 资料 | 类型 | 关键公开内容 | 权重状态 |
|---|---|---|---|---|
| 2020 | [GPT-3](openai_gpt3/论文中文解读.md) | 论文 | in-context learning 与规模化 few-shot | 未开放 |
| 2021 | [Codex](openai_codex/论文中文解读.md) | 论文 | 代码预训练、HumanEval、pass@k | 未开放 |
| 2022 | [InstructGPT](openai_instructgpt/论文中文解读.md) | 论文 | SFT → reward model → PPO | 未开放 |
| 2023 | [GPT-4](openai_gpt4/论文中文解读.md) | 技术报告/系统卡 | predictable scaling、能力、安全与披露边界 | 未开放 |
| 2025 | [gpt-oss](openai_gpt_oss/论文中文解读.md) | 模型卡 | MoE、MXFP4、Harmony 与可调 reasoning effort | 开放权重 |

相关通用研究：

- [CLIP](clip/论文中文解读.md)：图文对比学习。
- [Whisper](whisper/论文中文解读.md)：弱监督多语语音。
- [DPO](dpo/论文中文解读.md) 不是 OpenAI 论文，但适合与 InstructGPT 的 PPO 路线对照。

不要把 GPT-3/4、Codex、InstructGPT 写成开放权重模型；它们公开的是论文或报告。

## 5. Anthropic：对齐、安全、可解释性与产品披露边界

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2022 | [Constitutional AI](constitutional_ai/论文中文解读.md) | constitution、self-critique、AI feedback 与 RLAIF |
| 2024 | [Claude 3 Model Card](anthropic_claude3_model_card/论文中文解读.md) | 能力、安全、红队与发布评估 |
| 2024 | [Scaling Monosemanticity](anthropic_scaling_monosemanticity/论文中文解读.md) | Claude 3 Sonnet 上的大规模 sparse autoencoder |

Claude Code 是 coding agent 产品，不是一家公司，也没有公开完整产品编排或底层模型架构论文。模型卡可以支持能力和安全结论，不能用来猜测未披露的参数、训练数据或 agent orchestration。

## 6. MiniMax：长上下文混合 Attention 与长 CoT

| 时间 | 资料 | 主要公开内容 | 权重 |
|---|---|---|---|
| 2025 | [MiniMax-01](minimax_01/论文中文解读.md) | Lightning/softmax hybrid Attention、MoE、长上下文 | 开放，专用许可 |
| 2025 | [MiniMax-M1](minimax_m1/论文中文解读.md) | CISPO、long-CoT 与高效推理 | 开放 |

推荐顺序：先读 MiniMax-01 理解长上下文骨干，再读 M1 理解怎样把架构效率用于长输出 RL。不要把 Lightning Attention 的理论复杂度直接当成端到端推理速度。

## 7. Kimi / Moonshot AI：Reasoning、Agentic MoE 与 KV-Centric Serving

| 时间 | 资料 | 主要公开内容 | 主层次 |
|---|---|---|---|
| 2024/25 | [Mooncake](kimi_mooncake/论文中文解读.md) | disaggregated prefill/decode 与 KV cache 调度 | Serving |
| 2025 | [Kimi k1.5](kimi_k15/论文中文解读.md) | online mirror descent、partial rollout、long2short | Reasoning RL |
| 2025 | [Kimi K2](kimi_k2/论文中文解读.md) | 1T MoE、MuonClip、agentic data/RL | 模型 + Agent |

三篇是三条互补路线，不是版本号顺序：

- k1.5：怎样训练长链推理。
- K2：怎样训练 MoE 与 agentic 能力。
- Mooncake：怎样把长上下文 KV 变成分布式资源。

## 8. Alibaba Qwen：Dense/MoE 与可控思考

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2025 | [Qwen3](qwen_3/论文中文解读.md) | dense/MoE 模型族、119 种语言、thinking/non-thinking 与预算控制 |

比较 Qwen3 时必须固定模型大小、总参数/激活参数、是否 thinking、输出预算、工具和答案解析。更长思考不是自动更正确。

## 9. Meta：开放基础模型、视觉基础模型

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2023 | [LLaMA](llama/论文中文解读.md) | 公开数据训练、RMSNorm、SwiGLU、RoPE 与推理友好规模 |
| 2023 | [Segment Anything](sam/论文中文解读.md) | promptable segmentation、SA-1B 与 data engine |
| 2024 | [Llama 3](llama_3/论文中文解读.md) | 8B/70B/405B、15.6T token、128K 与完整后训练栈 |

LLaMA/Llama 3 的 base 与 instruct 版本必须分开比较；上下文窗口上限也不等于所有距离上的可靠利用。

## 10. Google / Google DeepMind：Scaling、多模态与科学模型

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2021 | [AlphaFold2](alphafold2/论文中文解读.md) | Evoformer、IPA、recycling 与结构置信度 |
| 2022 | [PaLM](palm/论文中文解读.md) | 540B scaling、Pathways 训练与 few-shot/CoT |
| 2023 | [Gemini 1.0](gemini/论文中文解读.md) | Ultra/Pro/Nano 原生多模态模型族与 TPU 系统 |

Gemini 技术报告展示系统能力，但没有披露到可以独立复现完整架构和训练数据的程度。

## 11. NVIDIA：Kernel 基础设施与 LLM Runtime

| 时间 | 资料 | 主要公开内容 | 主归类 |
|---|---|---|---|
| 2026 | [TensorRT-LLM Architecture](tensorrt_llm_architecture/论文中文解读.md) | model definition、compiler、engine、KV cache 与 serving runtime | 厂商系统 |
| 2026 | [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md) | layout 的可组合代数 | Compiler 交叉入口 |
| 2026 | [CuTeDSL TorchInductor Backend](cutedsl_torchinductor/论文中文解读.md) | CuTe DSL 接入动态图编译 | Compiler 交叉入口 |
| 2024–26 | [FlashAttention 3](flash_attention_3/论文中文解读.md) / [4](flash_attention_4/论文中文解读.md) | Hopper/Blackwell 硬件感知 Attention | 算法交叉入口 |

TensorRT-LLM 属于厂商定制实现；CuTe 和 FlashAttention 仍有可迁移的方法贡献，因此主解释分别放在 Compiler 和算法索引。

## 12. AMD 与开放训练栈

| 时间 | 资料 | 主要公开内容 |
|---|---|---|
| 2026 | [Instella-MoE](instella_moe/论文中文解读.md) | AMD 全栈训练、Gated MLA、FarSkip、16B 总参数/约 2.8B 激活参数 |

阅读时同时记录总参数、激活参数、expert 通信、KV cache 和具体硬件，不能只用“2.8B 激活”与 dense 2.8B 直接等价。

## 13. 横向比较表：不同厂商主要公开了哪一层

| 厂商 | 预训练架构 | 后训练/Reasoning | 训练系统 | Serving/硬件 | 典型公开缺口 |
|---|---|---|---|---|---|
| DeepSeek | 强 | 强 | 强 | 部分公开 | 完整数据、训练代码、生产 kernel |
| OpenAI | 历史论文强 | RLHF 与 gpt-oss 部分公开 | GPT-4 细节有限 | 产品系统有限 | frontier 权重、数据、完整架构 |
| Anthropic | 架构披露少 | 对齐研究强 | 有限 | Claude Code 编排未公开 | 网络结构、数据、产品 agent 栈 |
| MiniMax | hybrid Attention + MoE | CISPO | 部分 | 部分 | 完整数据和生产系统 |
| Kimi | MoE | reasoning/agentic RL | 部分 | Mooncake 较强 | 完整训练 recipe |
| Qwen | dense/MoE | 混合思考 | 部分 | 部分 | 数据与完整训练代码 |
| Meta | Llama 系列较强 | instruct/safety 部分 | 大规模训练经验 | 部分 | 完整数据与端到端复现 |
| Google | scaling/多模态/科学模型 | 部分 | TPU 系统 | 产品细节有限 | frontier 复现细节 |

## 14. 三条跨厂商阅读路线

### 路线 A：Reasoning 后训练

先用 [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md) 建立 CoT、Self-Consistency、Tree search、PRM 与 test-time scaling 的通用框架，再读厂商 recipe。

InstructGPT → DeepSeek-R1 → Kimi k1.5 → MiniMax-M1 → Qwen3。
比较 PPO、GRPO、mirror descent、CISPO 与混合思考时，统一 verifier、rollout budget、reference/KL 和输出长度。

### 路线 B：MoE 与长上下文

DeepSeekMoE/V2/V3 → MiniMax-01 → Kimi K2 → Qwen3 → Instella-MoE。
统一 total/active 参数、top-k、shared experts、KV 表示与通信拓扑。

### 路线 C：模型怎样进入部署系统

DeepSeek-V2/V3 → Mooncake → CloudMatrix384 → TensorRT-LLM。
依次观察 KV 表示、prefill/decode 解耦、expert parallel、cache pool、量化和硬件互联。

## 15. 厂商报告统一比较口径

- 权重、代码、数据和训练 recipe 分栏，不使用模糊的“开源”。
- base、instruct、reasoning、agent 版本分开。
- total parameters 与 active parameters 分开。
- 训练 context、API context、输出 budget 和可靠长程利用分开。
- prefill、decode、TTFT、TPOT、throughput、P99 和 goodput 分开。
- 同一 benchmark 固定 prompt、CoT、工具、pass@k、judge 与答案解析。
- 闭源报告只陈述公开证据，不由性能表反推未披露结构。

## 16. 与另外两条主线的边界

- [AI 模型基础理论与算法演进索引](AI模型基础理论与算法演进索引.md)：学习 Transformer、Attention、MoE、SSM、Reasoning、test-time scaling、推测解码、扩散和偏好学习等可迁移方法。
- [AI Compiler、Kernel DSL 与运行时演进索引](AI编译器与运行时演进索引.md)：学习图捕获、IR、schedule、kernel codegen、分布式编译与通用 runtime。
