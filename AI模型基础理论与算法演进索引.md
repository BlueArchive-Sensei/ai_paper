# AI 模型基础理论与最新算法演进索引

> 整理日期：2026-10-05
> 这条主线回答：模型为什么这样设计，训练目标、Attention、生成、MoE、Reasoning/test-time scaling 与推测解码如何演进。
> AI Compiler、Kernel DSL 与运行时请看 [AI Compiler 与运行时演进索引](AI编译器与运行时演进索引.md)；公司模型、产品报告和硬件适配请看 [AI 厂商模型与系统实现索引](AI厂商模型与系统实现索引.md)。

## 1. 本索引收什么，不收什么

| 收录 | 不作为本索引主线 |
|---|---|
| 可迁移到不同模型的基础理论、训练目标和通用架构 | 某一厂商模型的完整产品规格或模型卡 |
| Attention、位置编码、KV 表示与精确 Attention 算法 | XLA、TVM、MLIR、Triton 等编译器 |
| Scaling law、MoE、SSM、生成模型与多模态方法 | CloudMatrix、TensorRT-LLM、Mooncake 等部署实现 |
| 偏好学习、Reasoning、test-time scaling、通用解码算法 | 某个在线 API 或 coding agent 的未公开内部实现 |

一篇论文可能横跨多个层次。这里按主要知识贡献放置，并在需要时给出交叉入口。

## 2. 总体演进图

| 主线 | 起点 | 中间转折 | 当前重点 |
|---|---|---|---|
| 序列建模 | LSTM、Seq2Seq | Bahdanau Attention、Transformer | 长上下文、SSM、混合结构 |
| 预训练 | GPT-1、BERT、T5 | GPT-2/3、Scaling Laws | 数据—参数—计算配比与后训练 |
| Attention | MHA | 稀疏、低秩、线性、MQA/GQA | RoPE/ALiBi、MLA、FlashAttention 1–4 |
| 条件容量 | 稠密 FFN | Sparsely-Gated MoE、Switch | 细粒度 experts、路由稳定性 |
| Reasoning | CoT | 多路径、树搜索、PRM | 自适应 test-time compute、预算控制 |
| 推测解码 | 单链 draft–verify | token tree、multi-head、feature draft | 动态树、接受率与 kernel/serving 协同 |
| 生成模型 | VAE、GAN | DDPM、Latent Diffusion | DiT、低步数与多模态条件 |
| 多模态 | 图文表征 | CLIP、Flamingo、LLaVA | 原生多模态、视频/音频/工具 |
| 对齐 | 人类偏好奖励 | PPO/RLHF、Constitutional AI | DPO、RLAIF、可验证奖励 |

## 3. 基础理论与架构时间线

### 3.1 必要前史：1997–2015

| 时间 | 论文 | 为什么必须读 |
|---|---|---|
| 1997 | [LSTM](lstm/论文中文解读.md) | 门控记忆与近恒等误差通路；理解 Transformer 所替代的时间串行瓶颈 |
| 2013 | [VAE](vae/论文中文解读.md) | 变分下界与重参数化；后续 latent generative model 的概率基础 |
| 2014 | [GAN](gan/论文中文解读.md) | 用对抗博弈学习隐式生成分布 |
| 2014 | [Seq2Seq](seq2seq/论文中文解读.md) | encoder–decoder 条件序列建模 |
| 2014/15 | [Bahdanau Attention](bahdanau_attention/论文中文解读.md) | 每个解码步动态读取源序列，解除固定向量瓶颈 |
| 2015 | [ResNet](resnet/论文中文解读.md) | 残差参数化与直接梯度通路 |
| 2015 | [Knowledge Distillation](knowledge_distillation/论文中文解读.md) | teacher–student、软目标和部署压缩 |
| 2015 | [DQN](deep_q_network/论文中文解读.md) | 深度表征与价值学习结合 |

### 3.2 2016–2018：Transformer 与预训练范式形成

| 时间 | 论文 | 核心变化 |
|---|---|---|
| 2016/17 | [GCN](gcn/论文中文解读.md) | 从谱近似得到归一化图消息传播 |
| 2017 | [Transformer](transformer/论文中文解读.md) | self-attention、multi-head、位置编码与完全并行序列建模 |
| 2017 | [Sparsely-Gated MoE](sparsely_gated_moe/论文中文解读.md) | 每个 token 只激活部分参数的条件计算 |
| 2017 | [AlphaZero](alphazero/论文中文解读.md) | policy/value network、MCTS 与自我博弈闭环 |
| 2018 | [GPT-1](gpt1/论文中文解读.md) | 自回归预训练后监督微调 |
| 2018 | [BERT](bert/论文中文解读.md) | 双向 MLM encoder 与统一微调接口 |

### 3.3 2019–2020：长依赖、统一任务与 Scaling

| 时间 | 论文 | 核心变化 |
|---|---|---|
| 2019 | [GPT-2](gpt2/论文中文解读.md) | 规模化 causal LM 与 zero-shot task formatting |
| 2019 | [Transformer-XL](transformer_xl/论文中文解读.md) | segment recurrence 与相对位置 |
| 2019 | [T5](t5/论文中文解读.md) | span corruption 与 text-to-text 接口 |
| 2019 | [Multi-Query Attention](multi_query_attention/论文中文解读.md) | 多个 Q heads 共享单组 K/V，降低自回归解码带宽 |
| 2020 | [Scaling Laws](scaling_laws/论文中文解读.md) | loss 与参数、数据、计算之间的经验幂律 |
| 2020 | [Longformer](longformer/论文中文解读.md) | local window 与 global token 的稀疏 Attention |
| 2020 | [Linformer](linformer/论文中文解读.md) | 沿序列维做低秩 K/V 投影 |
| 2020 | [BigBird](bigbird/论文中文解读.md) | local、random、global 稀疏连接图 |
| 2020 | [Performer](performer/论文中文解读.md) | FAVOR+ 随机特征近似 softmax kernel |
| 2020 | [ViT](vit/论文中文解读.md) | 图像 patch token 与纯 Transformer encoder |
| 2020 | [DDPM](ddpm/论文中文解读.md) | 逐步高斯加噪与学习反向去噪 |
| 2020 | [wav2vec 2.0](wav2vec2/论文中文解读.md) | 遮盖式语音表征、量化目标与对比学习 |
| 2020 | [MuZero](muzero/论文中文解读.md) | 在只保留规划相关信息的隐空间中搜索 |

### 3.4 2021–2022：多模态、计算最优与推理轨迹

| 时间 | 论文 | 核心变化 |
|---|---|---|
| 2021 | [CLIP](clip/论文中文解读.md) | 图文对比预训练与开放词汇零样本分类 |
| 2021 | [RoPE](rope/论文中文解读.md) | 用旋转使 Q/K 内积自然依赖相对位移 |
| 2021 | [ALiBi](alibi/论文中文解读.md) | 在 Attention logit 上加入线性距离偏置 |
| 2021 | [Swin Transformer](swin_transformer/论文中文解读.md) | shifted window 与层次化视觉特征 |
| 2021 | [AlphaFold2](alphafold2/论文中文解读.md) | Evoformer、三角更新、IPA 与端到端结构预测 |
| 2021 | [Switch Transformer](switch_transformers/论文中文解读.md) | top-1 MoE 与大规模稀疏训练简化 |
| 2022 | [Latent Diffusion](latent_diffusion/论文中文解读.md) | 在压缩 latent 空间中做条件扩散 |
| 2022 | [Chinchilla](chinchilla/论文中文解读.md) | 固定计算下重新平衡模型参数与训练 token |
| 2022 | [Flamingo](flamingo/论文中文解读.md) | Perceiver Resampler 与 gated cross-attention |
| 2022 | [FlashAttention](flash_attention/论文中文解读.md) | exact Attention 的 IO-aware tiling 与 online softmax |
| 2022 | [Whisper](whisper/论文中文解读.md) | 大规模弱监督、多语言、多任务语音建模 |
| 2022 | [Chain-of-Thought Prompting](chain_of_thought/论文中文解读.md) | 把中间推理步骤写成可条件化的生成 token |
| 2022/23 | [Self-Consistency](self_consistency/论文中文解读.md) | 多路径采样并在答案层近似边缘化 |
| 2022/23 | [Speculative Decoding](speculative_decoding/论文中文解读.md) | draft–verify 与保持目标分布的修正拒绝采样 |
| 2022/23 | [DiT](dit/论文中文解读.md) | Transformer 作为扩散去噪骨干 |

### 3.5 2023–2026：Reasoning、SSM 与硬件感知生成

| 时间 | 论文 | 核心变化 |
|---|---|---|
| 2023 | [LLaMA](llama/论文中文解读.md) | 更充分训练的小模型、RMSNorm、SwiGLU、RoPE |
| 2023 | [Segment Anything](sam/论文中文解读.md) | promptable segmentation 与 data engine |
| 2023 | [DPO](dpo/论文中文解读.md) | 将 KL 约束偏好优化化为直接分类损失 |
| 2023 | [Grouped-Query Attention](grouped_query_attention/论文中文解读.md) | 在 MHA 与 MQA 之间调节 K/V 组数 |
| 2023 | [FlashAttention-2](flash_attention_2/论文中文解读.md) | 减少非矩阵乘工作并改进序列/warp 并行 |
| 2023 | [Mamba](mamba/论文中文解读.md) | 输入相关 selective SSM 与硬件感知 scan |
| 2023 | [LLaVA](llava/论文中文解读.md) | 视觉编码器、投影器与 LLM 的指令微调 |
| 2023 | [Tree of Thoughts](tree_of_thoughts/论文中文解读.md) | thought 级分支、评价、剪枝与回溯 |
| 2023 | [Let’s Verify Step by Step](lets_verify_step_by_step/论文中文解读.md) | PRM800K 与步骤级过程监督 |
| 2023 | [Speculative Sampling](speculative_sampling/论文中文解读.md) | Chinchilla 70B 上验证 exact speculative sampling |
| 2023/24 | [SpecInfer](specinfer/论文中文解读.md) | token tree 与 topology-aware 并行验证 |
| 2024 | [Mamba-2 / SSD](mamba_2/论文中文解读.md) | SSM 与半可分矩阵的对偶及 GEMM 友好算法 |
| 2024 | [FlashAttention-3](flash_attention_3/论文中文解读.md) | Hopper 上 TMA/WGMMA、异步流水与 FP8 |
| 2024 | [Compute-Optimal Test-Time Scaling](scaling_test_time_compute/论文中文解读.md) | 按题目难度分配 parallel、sequential 与 PRM search |
| 2024 | [Medusa](medusa/论文中文解读.md) | multiple decoding heads 与 tree attention |
| 2024 | [EAGLE](eagle_speculative/论文中文解读.md) | feature-level draft 与 shifted-token conditioning |
| 2024 | [EAGLE-2](eagle_2/论文中文解读.md) | context-aware dynamic draft tree |
| 2025 | [s1](s1_test_time_scaling/论文中文解读.md) | 1K reasoning SFT 与 budget forcing |
| 2025 | [Qwen3](qwen_3/论文中文解读.md) | dense/MoE 与 thinking/non-thinking 统一接口 |
| 2026 | [FlashAttention-4](flash_attention_4/论文中文解读.md) | 面向 Blackwell 的持久化异步流水 |
| 2026 | [FP4 FlashAttention-4](fp4_flash_attention_4/论文中文解读.md) | block-scaled FP4 与 Attention 数值/流水协同 |

Qwen3、LLaMA、LLaVA 等也属于具体厂商模型。这里仅把它们作为通用方法演进节点；完整公司路线放在厂商索引。

## 4. Attention 应沿五条轴学习

| 轴 | 代表论文 | 真正改变的对象 |
|---|---|---|
| 语义与连接 | Bahdanau、Transformer | 谁查询谁、如何形成上下文 |
| 位置与记忆 | Transformer-XL、RoPE、ALiBi | 位置信息怎样进入 score，历史怎样复用 |
| 稀疏或近似 | Longformer、BigBird、Linformer、Performer | 减少连接、降低秩或近似 softmax kernel |
| KV 表示 | MQA、GQA | 自回归阶段缓存多少组 K/V |
| 精确 kernel | FlashAttention 1–4 | 数学结果不变，减少 HBM IO 并适配不同 GPU |

### Attention 推荐顺序

1. [Bahdanau Attention](bahdanau_attention/论文中文解读.md)
2. [Transformer](transformer/论文中文解读.md)
3. [Transformer-XL](transformer_xl/论文中文解读.md)、[RoPE](rope/论文中文解读.md)、[ALiBi](alibi/论文中文解读.md)
4. [MQA](multi_query_attention/论文中文解读.md) 与 [GQA](grouped_query_attention/论文中文解读.md)
5. Longformer、BigBird、Linformer、Performer 四种高效 Attention 路线
6. [FlashAttention 1](flash_attention/论文中文解读.md) → [2](flash_attention_2/论文中文解读.md) → [3](flash_attention_3/论文中文解读.md) → [4](flash_attention_4/论文中文解读.md)

判断顺序：结果是否仍是标准 softmax Attention；改变的是连接数、近似误差、KV 字节、HBM IO 还是硬件流水；收益发生在训练、prefill 还是 decode；复杂度降低是否有真实 kernel 支持。

## 5. 近代高级算法：MoE、Reasoning 与推测解码

这三条线的完整时间线、公式、横向比较和组合方式见 [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md)。

### 5.1 MoE：扩展模型容量

[Sparsely-Gated MoE](sparsely_gated_moe/论文中文解读.md) → [Switch Transformer](switch_transformers/论文中文解读.md) → [MegaBlocks](megablocks/论文中文解读.md) → [DeepSeekMoE](deepseek_moe/论文中文解读.md)。

核心问题是：怎样让每个 token 只激活少量 experts，同时保持路由均衡、减少丢 token 和 all-to-all 开销。

### 5.2 Reasoning / test-time scaling：扩展单题计算

[CoT](chain_of_thought/论文中文解读.md) → [Self-Consistency](self_consistency/论文中文解读.md) → [Tree of Thoughts](tree_of_thoughts/论文中文解读.md) → [PRM](lets_verify_step_by_step/论文中文解读.md) → [Compute-Optimal Scaling](scaling_test_time_compute/论文中文解读.md) → [s1](s1_test_time_scaling/论文中文解读.md)。

核心问题是：额外预算应放在并行探索、顺序修订、步骤搜索还是停止决策上。最难问题未必随“想更久”改善。

### 5.3 Speculative decoding：降低串行生成延迟

[Speculative Decoding](speculative_decoding/论文中文解读.md) / [Speculative Sampling](speculative_sampling/论文中文解读.md) → [SpecInfer](specinfer/论文中文解读.md) → [Medusa](medusa/论文中文解读.md) → [EAGLE](eagle_speculative/论文中文解读.md) → [EAGLE-2](eagle_2/论文中文解读.md)。

核心问题是：怎样用低成本 draft 提高每次 target forward 接受的 token 数，并在 exact 模式下保持目标分布。它可加速 reasoning 产生的长输出，但不自动提高答案正确率。

## 6. 七条专题阅读路线

### 路线 A：从 RNN 到现代序列模型

LSTM → Seq2Seq → Bahdanau Attention → Transformer → Transformer-XL → Mamba → Mamba-2。

### 路线 B：从预训练到计算最优

GPT-1 / BERT / T5 → GPT-2 → Scaling Laws → Chinchilla → LLaMA。

### 路线 C：条件容量与 MoE

Sparsely-Gated MoE → Switch Transformer → MegaBlocks → DeepSeekMoE。

### 路线 D：Reasoning 与 test-time scaling

CoT → Self-Consistency → Tree of Thoughts → PRM → Compute-Optimal Scaling → s1。

### 路线 E：Speculative decoding

两篇基础 draft–verify → SpecInfer → Medusa → EAGLE → EAGLE-2。

### 路线 F：生成模型

VAE / GAN → DDPM → Latent Diffusion → DiT。

### 路线 G：视觉、多模态与对齐

ResNet → ViT / Swin → CLIP → Flamingo / LLaVA → SAM；Human Preferences → PPO → Constitutional AI → DPO。

具体厂商的大规模训练和 reasoning recipe 继续看 [厂商实现索引](AI厂商模型与系统实现索引.md)。

## 7. 阅读模型论文时统一的比较口径

- 参数：区分 total、active、shared experts 与 top-$k$。
- 数据：区分训练 token、唯一 token、重复 epoch、数据质量和去重。
- 上下文：区分训练长度、声明输入上限、可靠检索距离与输出预算。
- Attention：区分数学近似、KV 压缩和 exact IO 优化。
- Reasoning：分开 parallel samples、sequential revisions、搜索节点、verifier FLOPs 与 thinking token。
- 推测解码：分开 acceptance length、draft overhead、target verification、latency、throughput 与分布保证。
- 生成：统一分辨率、采样步数、guidance、FID 实现与样本数。
- 后训练：区分 SFT、奖励模型、在线/离线偏好优化和 test-time compute。
- 开放性：论文、权重、代码、数据和训练 recipe 分开陈述。

## 8. 与另外两条主线的边界

- [AI Compiler 与运行时演进索引](AI编译器与运行时演进索引.md)：研究图捕获、IR、lowering、fusion、schedule、kernel DSL、分布式编译与 runtime。
- [AI 厂商模型与系统实现索引](AI厂商模型与系统实现索引.md)：研究 DeepSeek、OpenAI、Anthropic、MiniMax、Kimi、Qwen、Llama、Gemini、Ascend、NVIDIA 等具体实现与公开边界。
