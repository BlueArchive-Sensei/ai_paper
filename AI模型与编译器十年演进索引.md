# 2016–2026 主流 AI 模型与 AI Compiler 十年演进索引

> 整理日期：2026-10-05
> 覆盖范围：以 2016–2026 为主，向前补入 LSTM、VAE/GAN、Seq2Seq、Bahdanau Attention、ResNet 等必要前史；时间线截至 FlashAttention-4 与 2026 年仓库已有编译器资料。
>
> “主流”采用三项标准：形成后续技术主线、进入广泛工业/开源实现、或显著改变训练与部署成本。任何“全部论文”集合都不会封闭；本索引收录的是完整主干节点和关键分叉，而不是把每个模型版本、benchmark 或微小改进都单列成论文。

## 1. 先把四个层次分开

很多技术名称都带有 Attention 或“加速”，但作用层不同：

| 层次 | 解决的问题 | 代表资料 |
|---|---|---|
| 模型架构 | 信息怎样流动、容量怎样组织 | LSTM、Transformer、ViT、Mamba、MoE |
| Attention 表示 | Q/K/V、连接图、位置如何表示 | MQA、GQA、MLA、RoPE、ALiBi、Longformer |
| Attention 算法/kernel | 数学结果不变时怎样减少 IO、安排硬件流水 | FlashAttention 1–4 |
| Compiler/runtime | 怎样捕获图、lower IR、融合、生成 kernel、管理执行 | XLA、TVM、MLIR、Triton、Inductor、TensorRT-LLM |

一个现代模型的真实性能是四层乘积，而不是论文 FLOPs 单独决定：

```text
模型质量
× attention/KV 表示
× kernel 对具体硬件的利用率
× compiler/runtime 的图捕获、融合、调度与缓存
```

## 2. 模型演进时间线

### 必要前史：1997–2015

| 时间 | 论文 | 关键变化 | 后续主线 |
|---|---|---|---|
| 1997 | [LSTM](lstm/论文中文解读.md) | 门控记忆与近线性误差通路 | Seq2Seq、语音、时间序列 |
| 2013 | [VAE](vae/论文中文解读.md) | 重参数化变分推断 | VQ-VAE、Latent Diffusion |
| 2014 | [GAN](gan/论文中文解读.md) | 生成器—判别器对抗学习 | 高保真生成、域适配 |
| 2014 | [Seq2Seq](seq2seq/论文中文解读.md) | LSTM encoder–decoder | 神经机器翻译、条件生成 |
| 2014/15 | [Bahdanau Attention](bahdanau_attention/论文中文解读.md) | 动态软对齐，解除固定向量瓶颈 | cross-attention、Transformer |
| 2015 | [ResNet](resnet/论文中文解读.md) | identity residual path | Transformer residual、扩散 U-Net |
| 2015 | [Knowledge Distillation](knowledge_distillation/论文中文解读.md) | teacher→student | LLM 蒸馏、R1 distilled models |
| 2015 | [DQN](deep_q_network/论文中文解读.md) | 深度网络+value learning | AlphaGo/MuZero、深度 RL |

LSTM 虽不在最近十年内，但用户点名且它定义了 Transformer 所替代的计算瓶颈：时间维串行、固定状态容量、长依赖逐步传递。

### 2016–2017：图网络、规划与 Transformer 起点

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2016/17 | [GCN](gcn/论文中文解读.md) | 归一化邻居聚合，建立 message-passing GNN 基线 |
| 2017 | [Attention Is All You Need](transformer/论文中文解读.md) | MHA、位置编码、完全并行的 encoder–decoder |
| 2017 | [Sparsely-Gated MoE](sparsely_gated_moe/论文中文解读.md) | 条件计算扩大总容量 |
| 2017 | [AlphaZero](alphazero/论文中文解读.md) | policy/value network + MCTS + self-play |

这一阶段的根本转变是：序列信息不必沿 RNN 时间步传递，模型可以直接建立 token-to-token 路径；容量也不必让每个 token 激活全部参数。

### 2018：预训练成为统一入口

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2018 | [GPT-1](gpt1/论文中文解读.md) | causal LM 预训练后做任务微调 |
| 2018 | [BERT](bert/论文中文解读.md) | 双向 MLM encoder + 下游微调 |

从这里分出三条经典结构路线：

- encoder-only：BERT，偏理解/表征；
- decoder-only：GPT，偏开放式自回归生成；
- encoder–decoder：T5，偏条件生成与 text-to-text。

### 2019：长上下文、统一任务与解码带宽

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2019 | [GPT-2](gpt2/论文中文解读.md) | 规模化 causal LM 与 zero-shot prompting |
| 2019 | [Transformer-XL](transformer_xl/论文中文解读.md) | segment recurrence + relative position |
| 2019 | [T5](t5/论文中文解读.md) | span corruption + text-to-text 统一接口 |
| 2019 | [Multi-Query Attention](multi_query_attention/论文中文解读.md) | 多 Q heads 共享一组 K/V，降低 decode KV 带宽 |

MQA 是第一个必须从 serving memory wall 理解的主流 attention 变体：它不是让训练复杂度变成线性，而是减少自回归阶段反复读取的 K/V。

### 2020：Scaling law、高效 Attention、多模态前夜

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2020 | [Scaling Laws](scaling_laws/论文中文解读.md) | loss 与参数、数据、计算的经验幂律 |
| 2020 | [GPT-3](openai_gpt3/论文中文解读.md) | in-context learning 与大规模 few-shot |
| 2020 | [Longformer](longformer/论文中文解读.md) | sliding-window + global sparse attention |
| 2020 | [Linformer](linformer/论文中文解读.md) | K/V 序列维低秩投影 |
| 2020 | [BigBird](bigbird/论文中文解读.md) | local + random + global 稀疏图 |
| 2020 | [Performer](performer/论文中文解读.md) | FAVOR+ 随机特征线性化 softmax attention |
| 2020 | [ViT](vit/论文中文解读.md) | 图像 patch token + Transformer |
| 2020 | [DDPM](ddpm/论文中文解读.md) | 高质量逐步去噪生成 |
| 2020 | [wav2vec 2.0](wav2vec2/论文中文解读.md) | 遮盖式自监督语音表征 |
| 2020 | [MuZero](muzero/论文中文解读.md) | 学习用于规划的隐空间动力学 |

这一年以后，“高效 Attention”至少分成四类：稀疏图、低秩投影、kernel feature/recurrent state、精确 dense attention 的 IO 优化。它们不能只按大 O 复杂度混为一谈。

### 2021：视觉—语言对齐、位置外推和层次视觉

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2021 | [CLIP](clip/论文中文解读.md) | 大规模图文对比学习、zero-shot classifier |
| 2021 | [RoPE](rope/论文中文解读.md) | 旋转几何编码相对位置 |
| 2021 | [ALiBi](alibi/论文中文解读.md) | attention logit 线性距离 bias |
| 2021 | [Swin Transformer](swin_transformer/论文中文解读.md) | shifted windows + 多尺度视觉层级 |
| 2021 | [AlphaFold2](alphafold2/论文中文解读.md) | Evoformer、三角更新、IPA 与端到端蛋白结构预测 |
| 2021 | [Switch Transformer](switch_transformers/论文中文解读.md) | top-1 MoE 扩展与工程简化 |
| 2021 | [Codex](openai_codex/论文中文解读.md) | 代码预训练、HumanEval 与 pass@k |

### 2022：计算最优、扩散主流、FlashAttention

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2022 | [Latent Diffusion](latent_diffusion/论文中文解读.md) | 在压缩潜空间扩散 + cross-attention conditioning |
| 2022 | [Chinchilla](chinchilla/论文中文解读.md) | 参数与 tokens 同比扩展的 compute-optimal 配方 |
| 2022 | [PaLM](palm/论文中文解读.md) | 540B dense scaling 与 Pathways 训练 |
| 2022 | [Flamingo](flamingo/论文中文解读.md) | Perceiver Resampler + gated cross-attention 的多模态 few-shot |
| 2022 | [FlashAttention](flash_attention/论文中文解读.md) | exact attention 的 IO-aware tiling + online softmax |
| 2022 | [Whisper](whisper/论文中文解读.md) | 68 万小时弱监督多任务语音模型 |
| 2022/23 | [DiT](dit/论文中文解读.md) | Transformer diffusion backbone + adaLN-Zero |
| 2022 | [InstructGPT](openai_instructgpt/论文中文解读.md) | SFT→RM→PPO 的 RLHF 主线 |
| 2022 | [Constitutional AI](constitutional_ai/论文中文解读.md) | constitution、self-critique 与 RLAIF |

### 2023：开放 LLM、偏好优化、GQA、SSM

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2023 | [LLaMA](llama/论文中文解读.md) | 公开数据、高 token/parameter 比、RMSNorm/SwiGLU/RoPE |
| 2023 | [Segment Anything](sam/论文中文解读.md) | promptable segmentation + SA-1B |
| 2023 | [DPO](dpo/论文中文解读.md) | 无显式 RM/PPO 的直接偏好优化 |
| 2023 | [GQA](grouped_query_attention/论文中文解读.md) | 多个 Q heads 共享一组 K/V heads |
| 2023 | [FlashAttention-2](flash_attention_2/论文中文解读.md) | sequence parallel 与更优 warp/block 分工 |
| 2023 | [Mamba](mamba/论文中文解读.md) | selective SSM + hardware-aware scan |
| 2023 | [GPT-4](openai_gpt4/论文中文解读.md) | predictable scaling、多模态与系统安全披露 |
| 2023 | [LLaVA](llava/论文中文解读.md) | CLIP + projector + LLM 的视觉指令微调 |
| 2023 | [Gemini](gemini/论文中文解读.md) | 原生多模态模型族与端云分层 |

### 2024：架构—系统协同加深

| 时间 | 论文 | 主贡献 |
|---|---|---|
| 2024 | [Mamba-2 / SSD](mamba_2/论文中文解读.md) | SSM 与 structured masked attention 的矩阵对偶 |
| 2024 | [FlashAttention-3](flash_attention_3/论文中文解读.md) | Hopper TMA/WGMMA、warp specialization、FP8 |
| 2024 | [Llama 3](llama_3/论文中文解读.md) | 405B dense、15T tokens、128K 与完整后训练栈 |
| 2024 | [DeepSeekMoE](deepseek_moe/论文中文解读.md) | fine-grained/shared experts |
| 2024 | [DeepSeek-V2](deepseek_v2/论文中文解读.md) | MLA + DeepSeekMoE |
| 2024 | [DeepSeek-V3](deepseek_v3/论文中文解读.md) | auxiliary-loss-free routing、MTP、DualPipe、FP8 |
| 2024 | [Claude 3 Model Card](anthropic_claude3_model_card/论文中文解读.md) | 能力、安全和发布边界 |
| 2024 | [Scaling Monosemanticity](anthropic_scaling_monosemanticity/论文中文解读.md) | Claude 3 Sonnet 上的大规模 SAE |

### 2025：Reasoning、Agentic MoE 与开放权重竞争

| 时间 | 论文/报告 | 主贡献 |
|---|---|---|
| 2025 | [DeepSeek-R1](deepseek_r1/论文中文解读.md) | GRPO、verifier、cold-start 与 reasoning distillation |
| 2025 | [Qwen3](qwen_3/论文中文解读.md) | dense/MoE、thinking/non-thinking 融合与预算控制 |
| 2025 | [gpt-oss](openai_gpt_oss/论文中文解读.md) | OpenAI 开放权重 MoE、MXFP4、Harmony |
| 2025 | [MiniMax-01](minimax_01/论文中文解读.md) | Lightning/softmax hybrid attention + MoE |
| 2025 | [MiniMax-M1](minimax_m1/论文中文解读.md) | CISPO + long-CoT |
| 2025 | [Kimi k1.5](kimi_k15/论文中文解读.md) | online mirror descent + partial rollout |
| 2025 | [Kimi K2](kimi_k2/论文中文解读.md) | 1T MoE、MuonClip、agentic data/RL |
| 2024/25 | [Mooncake](kimi_mooncake/论文中文解读.md) | KV-centric disaggregated serving |
| 2025 | [CloudMatrix384](ascend_cloudmatrix384/论文中文解读.md) | Ascend 超节点上的 R1 EP320/PDC serving |

### 2026：FlashAttention-4 与 Blackwell/CuTeDSL

| 时间 | 论文/资料 | 主贡献 |
|---|---|---|
| 2026-03 | [FlashAttention-4](flash_attention_4/论文中文解读.md) | Blackwell 非对称扩展、异步 MMA、软件 exp、TMEM、CuTe DSL |
| 2026-09 | [Hardware-Aware FP4 FlashAttention-4](fp4_flash_attention_4/论文中文解读.md) | FP4 matmul 变快后处理 softmax/量化新瓶颈 |
| 2026-09 | [Instella-MoE](instella_moe/论文中文解读.md) | AMD 全栈训练、Gated MLA、FarSkip 与完整开放流程 |
| 2026 | [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md) | layout 作为可组合代数 |
| 2026 | [CuTeDSL TorchInductor Backend](cutedsl_torchinductor/论文中文解读.md) | Python DSL 接入动态图编译 |
| 2026 | [Taming Bitwise GPU Kernels](taming_bitwise_gpu_kernels/论文中文解读.md) | tensor core 上的 bitwise kernel |
| 2026 | [Event Tensor](event_tensor/论文中文解读.md) | 事件驱动 tensor execution |
| 2026 | [Ada-MK](ada_mk/论文中文解读.md) | 自适应 mega-kernel |
| 2026 | [TensorRT-LLM Architecture](tensorrt_llm_architecture/论文中文解读.md) | LLM 专用 runtime/engine 架构 |

## 3. Attention 演进必须沿四条轴看

| 时间 | 技术 | 改变的轴 | 没有解决什么 |
|---|---|---|---|
| 2014 | Bahdanau | decoder 动态读取 encoder | RNN 串行仍在 |
| 2017 | MHA | 全局 token 交互与多子空间 | O(n²) score/IO |
| 2019 | Transformer-XL | recurrence + 相对位置 | 局部训练和 memory 上限 |
| 2019 | MQA | KV 表示/解码带宽 | prefill 二次计算 |
| 2020 | Longformer/BigBird | 稀疏连接图 | 需 sparse kernel，可能丢边 |
| 2020 | Linformer | 低秩序列投影 | 近似误差与长度绑定 |
| 2020 | Performer | kernel feature/recurrent state | 随机近似误差 |
| 2021 | RoPE/ALiBi | 位置进入 score 的方式 | 外推不等于推理可靠 |
| 2022 | FlashAttention | 精确 dense attention 的 IO | 算术仍 O(n²) |
| 2023 | GQA | KV groups | 表达与带宽 trade-off |
| 2023 | FA2 | Ampere work partition | 硬件相关性 |
| 2024 | MLA | 低秩 latent KV 表示 | 特殊 kernel 和权重吸收 |
| 2024 | FA3 | Hopper async pipeline/FP8 | 非 Hopper 可移植性 |
| 2025 | Lightning Attention | hybrid recurrent/softmax | kernel 数值一致性 |
| 2026 | FA4 | Blackwell pipeline + CuTeDSL | 端到端瓶颈仍可能在别处 |

### 一个实用判断顺序

1. 先问结果是否仍是标准 softmax attention：FlashAttention 是；Performer/Linformer 不是。
2. 再问主要优化训练 prefill、decode，还是两者：MQA/GQA 首先服务 decode；FlashAttention 两边都可用。
3. 再问减少的是 FLOPs、HBM IO、KV bytes 还是通信：四者不可互换。
4. 最后看硬件与 kernel：论文公式相同，在 A100、H100、B200、Ascend 上的最佳实现可以完全不同。

## 4. AI Compiler 十年时间线

### 2016–2017：从框架执行器到图编译

| 时间 | 资料 | 变化 |
|---|---|---|
| 2017 | [XLA/OpenXLA](xla_compiler/论文中文解读.md) | TensorFlow graph→HLO，fusion、specialization、backend codegen |
| 2017 | [Dynamic Computation Graphs](dynamic_computation_graphs/论文中文解读.md) | define-by-run 的动态图语义 |

冲突由此形成：静态图利于全局优化，动态图利于 Python 控制流和调试。后续十年大量工作都在尝试同时保留二者。

### 2018：端到端编译器与自动调优

| 时间 | 论文 | 变化 |
|---|---|---|
| 2018 | [Tensor Comprehensions](tensor_comprehensions/论文中文解读.md) | 数学 DSL + polyhedral JIT + autotuning |
| 2018 | [TVM](tvm_compiler/论文中文解读.md) | graph IR + tensor schedule + learning cost model |
| 2018 | [Glow](glow_compiler/论文中文解读.md) | high/low-level IR + progressive lowering |

### 2019：动态图框架成熟、图替换自动化、kernel DSL

| 时间 | 论文 | 变化 |
|---|---|---|
| 2019 | [PyTorch](pytorch_imperative/论文中文解读.md) | imperative eager frontend 成为主流 |
| 2019 | [Chainer](chainer_define_by_run/论文中文解读.md) | define-by-run 的工程脉络 |
| 2019 | [TASO](taso/论文中文解读.md) | 自动生成并形式验证 graph substitutions |
| 2019 | [Triton](triton_compiler/论文中文解读.md) | block-level GPU DSL，程序员控制 tile、编译器完成映射 |

### 2020：多级 IR、自动 schedule、整体调度

| 时间 | 论文 | 变化 |
|---|---|---|
| 2020 | [MLIR](mlir/论文中文解读.md) | extensible dialect + progressive lowering |
| 2020 | [Ansor](ansor/论文中文解读.md) | 自动构造 schedule space + learned search |
| 2020 | [Rammer](rammer/论文中文解读.md) | rTask 统一 operator 内外并行调度 |
| 2020 | [FusionStitching](fusion_stitching/论文中文解读.md) | fusion 中间结果与共享内存 stitching |

### 2021：动态图编译与硬件先验回归

| 时间 | 论文 | 变化 |
|---|---|---|
| 2021 | [Nimble](nimble_dynamic_nn/论文中文解读.md) | 动态网络的编译执行 |
| 2021 | [DISC](disc_dynamic_shape/论文中文解读.md) | dynamic shape 编译 |
| 2021 | [GSPMD](gspmd/论文中文解读.md) | sharding propagation、SPMD lowering 与 collectives 插入 |
| 2021/22 | [Bolt](bolt/论文中文解读.md) | CUTLASS 等 hardware-native template search |

### 2022：可编程搜索空间、TensorIR 与轻量 runtime

| 时间 | 论文 | 变化 |
|---|---|---|
| 2022 | [torch.fx](torch_fx/论文中文解读.md) | Python-level symbolic graph transformation |
| 2022 | [Roller](roller/论文中文解读.md) | hardware-constraint-driven tile construction |
| 2022 | [TinyIREE](tinyiree/论文中文解读.md) | MLIR compiler + 小型部署 runtime |
| 2022 | [MetaSchedule](metaschedule/论文中文解读.md) | 用概率程序表达 schedule search space |
| 2022/23 | [TensorIR](tensorir/论文中文解读.md) | block/region-aware tensor program IR |
| 2022 | [Alpa](alpa/论文中文解读.md) | 自动搜索 intra-op sharding 与 inter-op pipeline |

### 2023：task mapping、tile fusion 与稀疏算子

| 时间 | 论文 | 变化 |
|---|---|---|
| 2023 | [Hidet](hidet/论文中文解读.md) | task-mapping program + post-scheduling fusion |
| 2023 | [Welder](welder/论文中文解读.md) | tile-graph 上的数据复用与 fusion |
| 2023 | [MegaBlocks](megablocks/论文中文解读.md) | block-sparse MoE kernel/system |

### 2024：动态图捕获与自动生成 kernel 进入主框架

| 时间 | 论文 | 变化 |
|---|---|---|
| 2024 | [PyTorch 2](pytorch_2/论文中文解读.md) | Dynamo guards + AOTAutograd + Inductor/Triton |
| 2024 | [Korch](korch/论文中文解读.md) | 用优化问题选择全局 kernel orchestration |

### 2025：tile DSL、mega-kernel 与编译器评测

| 时间 | 论文 | 变化 |
|---|---|---|
| 2025 | [TileLang](tilelang/论文中文解读.md) | tile dataflow 与 schedule annotation 解耦 |
| 2025 | [Mirage Persistent Kernel](mirage_persistent_kernel/论文中文解读.md) | 模型子图 mega-kernel 化 |
| 2025 | [TritonBench](tritonbench/论文中文解读.md) | 系统评测 LLM 生成/优化 Triton kernel |
| 2025/26 | [Linear Layouts](linear_layouts/论文中文解读.md) | 统一描述线程—寄存器—共享内存布局 |

### 2026：算法—kernel—DSL 同时设计

| 时间 | 资料 | 变化 |
|---|---|---|
| 2026 | [FlashAttention-4](flash_attention_4/论文中文解读.md) | CuTeDSL 内实现 Blackwell pipeline |
| 2026 | [CuTe Layout Algebra](cute_layout_algebra/论文中文解读.md) | 把 layout 变换变成可推理组合 |
| 2026 | [CuTeDSL TorchInductor](cutedsl_torchinductor/论文中文解读.md) | 高性能专家 DSL 接入 PyTorch 图编译 |
| 2026 | [TensorRT-LLM Architecture](tensorrt_llm_architecture/论文中文解读.md) | 编译 engine 与 serving runtime 深度结合 |
| 2026 | [PyTorch Graph Programming Model](pytorch_graph_programming_model/论文中文解读.md) | Dynamo、export 与 dynamic shapes 的语义边界 |

## 5. AI Compiler 的六次主要变化

### 5.1 逐 op library → 整图编译

早期框架依次 dispatch cuDNN/cuBLAS kernels；XLA、Glow、TVM 开始跨 op 做 constant folding、layout、fusion 和 buffer planning。

### 5.2 单一 IR → 多级 IR / dialect

神经网络语义、张量循环、GPU tile 和机器指令需要不同抽象。Glow 用两层 IR，MLIR 将其泛化为 dialect 与 progressive lowering，现代 XLA/IREE/Torch 编译栈都在多级表示间移动。

### 5.3 手写 schedule → autotuning → 可编程搜索空间

```text
AutoTVM：专家写 template
Ansor：自动生成 sketches
MetaSchedule：专家用概率程序扩展搜索规则
Bolt：硬件原生模板 + 小搜索
TileLang/CuTe：专家显式表达 tile/layout/pipeline
```

趋势不是“自动化不断取代专家”，而是把专家知识放在更可组合、可验证的抽象中。

### 5.4 operator fusion → tile fusion → persistent/mega-kernel

普通 fusion 消除中间 HBM；Welder 在 tile 级分析 producer/consumer；persistent kernel 把权重/状态长期留在片上；mega-kernel 进一步把调度器和多个算子放进同一 kernel。融合越大，寄存器压力、occupancy、编译时间和动态性风险也越高。

### 5.5 静态图 → guarded dynamic capture

PyTorch 2 的关键不是“把 Python 全部静态化”，而是 Dynamo 捕获可稳定子图并生成 guards；guard 失效时重编译或 graph break。动态 shape 编译的核心是符号约束与 specialization policy。

### 5.6 通用编译器 → 模型/硬件协同

MoE 需要 dispatch/all-to-all，LLM decode 需要 KV cache 与小 batch GEMM，FlashAttention-4 针对 Blackwell 资源比例重新流水化。现代“AI compiler”已跨越传统编译边界，包含 runtime、通信、内存池、autotuning 数据库和 serving scheduler。

## 6. 推荐学习路线

### 路线 A：从 LSTM 到现代 LLM

1. LSTM
2. Seq2Seq
3. Bahdanau Attention
4. Transformer
5. GPT-1 / BERT / T5
6. GPT-2 / GPT-3
7. Scaling Laws / Chinchilla
8. LLaMA / Llama 3
9. DeepSeek-V2/V3/R1、Qwen3、Kimi K2

### 路线 B：Attention 全栈

1. Transformer MHA
2. Transformer-XL + RoPE + ALiBi
3. MQA + GQA + MLA
4. Longformer + BigBird
5. Linformer + Performer + Mamba/Mamba-2
6. FlashAttention 1 → 2 → 3 → 4
7. Mooncake / CloudMatrix384 看 KV 和 attention 如何进入系统

### 路线 C：AI Compiler

1. XLA / TVM / Glow
2. Triton / MLIR
3. Ansor / MetaSchedule / TensorIR
4. Nimble / DISC / torch.fx
5. PyTorch 2
6. Welder / Hidet / Korch
7. TileLang / Linear Layouts / CuTeDSL
8. FlashAttention-4 与 TensorRT-LLM

### 路线 D：视觉与生成

1. ResNet
2. ViT / Swin
3. CLIP / SAM
4. VAE / GAN
5. DDPM
6. Latent Diffusion
7. DiT

## 7. 如何比较论文，避免时间线误导

- 模型：统一参数 total/active、训练 tokens、数据公开度、context、后训练与推理预算。
- Attention：分清数学近似、连接稀疏、KV 压缩和 IO-aware exact kernel。
- 生成模型：统一分辨率、采样步数、guidance、FID 实现和人评协议。
- 编译器：统一 shape、batch、dtype、硬件、vendor baseline、调优预算、compile time 与 steady-state。
- 开放性：paper、weights、code、data、training recipe、kernel/runtime 分列。
- 年份：以首次公开版本为主；会议年份与 arXiv 年份可能不同。

## 8. 本专题的文件结构

本次新增的每份资料均包含：

```text
paper_name/
├── paper.pdf
├── paper.txt
├── 论文概要.md
├── 论文中文解读.md
└── rendered_figures/
```

XLA 没有与其他条目等价的单一架构论文，因此其目录明确保存 2026-10-05 官方 OpenXLA architecture/GPU architecture 文本快照并生成阅读 PDF；精读中没有把它伪装成同行评审论文。

