# 论文精读 GitHub Markdown 审核报告

- 审核日期：2026-10-05
- 审核范围：仓库内全部 129 个 `论文中文解读.md`，并联查 README、索引和 129 个 `论文概要.md`
- 总体结论：**129/129 篇论文的 PDF、文本、概要、精读和证据导航已经配齐**
- 精读统计：count=129 min=2451 median=3048 max=34534 h2=1723 images=990 cites=268
- 全部作者撰写 Markdown 终检：267 个文件、1,789 个本地链接，错误 0

## 本轮实际改动

1. 对 67 篇原先偏短的模型、Attention、生成模型、多模态与 AI Compiler 笔记进行了正文级加深。
2. 每篇加深稿新增“原文论证链、机制/公式、实验阅读、复现检查、常见误读”。
3. 67 篇加深稿分别在论证、机制、实验、结论段加入 4 个原文页定位，共 268 个逐段定位。
4. 全部 129 篇精读新增“原文证据导航”，链接本地 PDF、可检索文本和已引用截图。
5. 数学分隔符统一为 GitHub 支持的 `$...$` 与 `$$...$$`。
6. 补齐 `taming_bitwise_gpu_kernels/论文概要.md`，现在 129 篇全部具有“概要 + 精读”。
7. 保留原来已经较长的详细精读正文；本轮对它们补齐证据入口，并完成结构与链接复核。

## 审核规则与结果

| 检查项 | 通过标准 | 结果 |
|---|---|---|
| 资料配对 | 每篇均有 PDF、可检索文本、概要、精读 | 129/129 |
| 标题结构 | 每篇恰好一个 H1，标题层级不跳级 | 129/129 |
| 代码围栏 | Markdown 围栏成对闭合 | 129/129 |
| 数学公式 | 无旧式圆括号或方括号数学分隔符残留；美元分隔符成对 | 129/129 |
| 本地链接 | PDF、文本、截图和 Markdown 相对链接目标存在 | 1,789/1,789 |
| 图片可访问性 | 每篇至少一张原文截图，且 alt 文本非空 | 129/129 |
| 原文入口 | 同时提供 `paper.pdf` 与 `paper.txt` | 129/129 |
| 证据导航 | 提供 PDF 文件页码与对应截图 | 129/129 |
| 异常字符 | 不含会破坏渲染的控制字符 | 129/129 |
| 最低完整度 | 不存在少于 1,800 个中文/公式字符的精读 | 129/129 |

## 审核边界

- `source_*.md`、`source_*.html` 等是为了留存上游页面而保存的原始快照，不属于作者撰写的精读 Markdown；其中的相对链接可能依赖原项目目录结构。
- 表中的“逐段原文定位”为 4，表示该篇是本轮正文级加深的 67 篇之一；为 0 表示原稿本身已是详细精读，本轮保留正文并补齐统一证据导航。0 不是审核失败。
- PDF 页码使用仓库文件的物理页序号，可能与论文正文印刷页码不同。
- PASS 表示 Markdown 结构、本地资源和证据入口通过。对开放问题、复现实验和闭源技术报告未披露信息，正文仍按论文自身证据边界表述，不把缺失细节推断为事实。

## 逐篇追踪表

| 目录 | 字符数 | H2 数 | 原文截图数 | 逐段原文定位 | 结果 |
|---|---:|---:|---:|---:|---|
| `ada_mk` | 3552 | 12 | 5 | 0 | PASS |
| `ai_control` | 10895 | 17 | 28 | 0 | PASS |
| `alibi` | 2724 | 13 | 4 | 4 | PASS |
| `alignment_faking` | 17862 | 19 | 102 | 0 | PASS |
| `alpa` | 3043 | 13 | 4 | 4 | PASS |
| `alphafold2` | 2938 | 13 | 4 | 4 | PASS |
| `alphazero` | 2451 | 13 | 4 | 4 | PASS |
| `ansor` | 2819 | 13 | 4 | 4 | PASS |
| `anthropic_claude3_model_card` | 3596 | 11 | 6 | 0 | PASS |
| `anthropic_scaling_monosemanticity` | 3415 | 11 | 5 | 0 | PASS |
| `ascend_cloudmatrix384` | 5191 | 12 | 5 | 0 | PASS |
| `bahdanau_attention` | 2662 | 13 | 4 | 4 | PASS |
| `bert` | 2869 | 13 | 4 | 4 | PASS |
| `bigbird` | 2652 | 13 | 4 | 4 | PASS |
| `bolt` | 2915 | 13 | 4 | 4 | PASS |
| `chainer_define_by_run` | 4185 | 11 | 5 | 0 | PASS |
| `chinchilla` | 2816 | 13 | 4 | 4 | PASS |
| `clip` | 2807 | 13 | 4 | 4 | PASS |
| `constitutional_ai` | 10919 | 20 | 12 | 0 | PASS |
| `cute_layout_algebra` | 3803 | 13 | 8 | 0 | PASS |
| `cutedsl_torchinductor` | 4079 | 14 | 4 | 0 | PASS |
| `ddpm` | 2843 | 13 | 4 | 4 | PASS |
| `deep_q_network` | 5024 | 13 | 6 | 0 | PASS |
| `deepseek_moe` | 3421 | 10 | 4 | 0 | PASS |
| `deepseek_r1` | 4324 | 12 | 5 | 0 | PASS |
| `deepseek_v2` | 3963 | 11 | 5 | 0 | PASS |
| `deepseek_v3` | 4533 | 13 | 6 | 0 | PASS |
| `disc_dynamic_shape` | 4926 | 13 | 4 | 0 | PASS |
| `distral` | 5099 | 13 | 6 | 0 | PASS |
| `dit` | 2944 | 13 | 4 | 4 | PASS |
| `dpo` | 3012 | 13 | 4 | 4 | PASS |
| `dynamic_computation_graphs` | 4736 | 11 | 5 | 0 | PASS |
| `emergent_misalignment` | 12149 | 14 | 29 | 0 | PASS |
| `event_tensor` | 3519 | 13 | 7 | 0 | PASS |
| `exploitgym` | 10362 | 17 | 8 | 0 | PASS |
| `flamingo` | 2883 | 13 | 4 | 4 | PASS |
| `flash_attention` | 3042 | 13 | 4 | 4 | PASS |
| `flash_attention_2` | 2877 | 13 | 4 | 4 | PASS |
| `flash_attention_3` | 3004 | 13 | 4 | 4 | PASS |
| `flash_attention_4` | 3119 | 13 | 4 | 4 | PASS |
| `fp4_flash_attention_4` | 2974 | 13 | 4 | 4 | PASS |
| `fusion_stitching` | 3828 | 12 | 6 | 0 | PASS |
| `gan` | 2700 | 13 | 4 | 4 | PASS |
| `gcn` | 2587 | 13 | 4 | 4 | PASS |
| `gemini` | 2704 | 13 | 4 | 4 | PASS |
| `glow_compiler` | 2884 | 13 | 4 | 4 | PASS |
| `gpt1` | 2869 | 13 | 4 | 4 | PASS |
| `gpt2` | 2793 | 13 | 4 | 4 | PASS |
| `grouped_query_attention` | 2887 | 13 | 4 | 4 | PASS |
| `gspmd` | 2908 | 13 | 4 | 4 | PASS |
| `hidet` | 2838 | 13 | 4 | 4 | PASS |
| `human_preferences_rl` | 5410 | 15 | 6 | 0 | PASS |
| `instella_moe` | 2909 | 13 | 4 | 4 | PASS |
| `jailbroken` | 6319 | 14 | 10 | 0 | PASS |
| `janus_symbolic_graph` | 5031 | 13 | 7 | 0 | PASS |
| `kimi_k15` | 3488 | 11 | 5 | 0 | PASS |
| `kimi_k2` | 3787 | 11 | 5 | 0 | PASS |
| `kimi_mooncake` | 3644 | 10 | 5 | 0 | PASS |
| `knowledge_distillation` | 5251 | 14 | 5 | 0 | PASS |
| `korch` | 3807 | 13 | 6 | 0 | PASS |
| `latent_diffusion` | 2805 | 13 | 4 | 4 | PASS |
| `linear_layouts` | 15615 | 23 | 8 | 0 | PASS |
| `linformer` | 2826 | 13 | 4 | 4 | PASS |
| `llama` | 2853 | 13 | 4 | 4 | PASS |
| `llama_3` | 2820 | 13 | 4 | 4 | PASS |
| `llava` | 2775 | 13 | 4 | 4 | PASS |
| `longformer` | 2833 | 13 | 4 | 4 | PASS |
| `lstm` | 2728 | 13 | 4 | 4 | PASS |
| `mamba` | 2916 | 13 | 4 | 4 | PASS |
| `mamba_2` | 2954 | 13 | 4 | 4 | PASS |
| `mechanistic_interpretability` | 8371 | 17 | 25 | 0 | PASS |
| `megablocks` | 4097 | 13 | 9 | 0 | PASS |
| `metaschedule` | 2737 | 13 | 4 | 4 | PASS |
| `minimax_01` | 4003 | 11 | 6 | 0 | PASS |
| `minimax_m1` | 3683 | 11 | 5 | 0 | PASS |
| `mirage_persistent_kernel` | 4117 | 14 | 8 | 0 | PASS |
| `mlir` | 3074 | 13 | 4 | 4 | PASS |
| `multi_query_attention` | 2950 | 13 | 4 | 4 | PASS |
| `muzero` | 7163 | 16 | 8 | 0 | PASS |
| `nimble_dynamic_nn` | 5673 | 13 | 6 | 0 | PASS |
| `openai_codex` | 3038 | 11 | 5 | 0 | PASS |
| `openai_gpt3` | 3263 | 11 | 5 | 0 | PASS |
| `openai_gpt4` | 2931 | 10 | 5 | 0 | PASS |
| `openai_gpt_oss` | 3764 | 11 | 5 | 0 | PASS |
| `openai_instructgpt` | 3240 | 10 | 5 | 0 | PASS |
| `palm` | 2814 | 13 | 4 | 4 | PASS |
| `performer` | 2841 | 13 | 4 | 4 | PASS |
| `policy_distillation` | 5304 | 13 | 7 | 0 | PASS |
| `proximal_policy_optimization` | 5494 | 13 | 6 | 0 | PASS |
| `pytorch_2` | 10809 | 20 | 5 | 0 | PASS |
| `pytorch_graph_programming_model` | 9308 | 19 | 13 | 0 | PASS |
| `pytorch_imperative` | 4900 | 11 | 5 | 0 | PASS |
| `qwen_3` | 2845 | 13 | 4 | 4 | PASS |
| `rammer` | 2934 | 13 | 4 | 4 | PASS |
| `resnet` | 2646 | 13 | 4 | 4 | PASS |
| `roller` | 2614 | 13 | 4 | 4 | PASS |
| `rope` | 2763 | 13 | 4 | 4 | PASS |
| `sam` | 2858 | 13 | 4 | 4 | PASS |
| `scaling_laws` | 2834 | 13 | 4 | 4 | PASS |
| `seq2seq` | 2500 | 13 | 4 | 4 | PASS |
| `shade_arena` | 10076 | 14 | 17 | 0 | PASS |
| `simple_adaptive_attacks` | 11154 | 17 | 32 | 0 | PASS |
| `sleeper_agents` | 13672 | 18 | 82 | 0 | PASS |
| `soft_actor_critic` | 5258 | 13 | 6 | 0 | PASS |
| `sparsely_gated_moe` | 3644 | 12 | 7 | 0 | PASS |
| `swin_transformer` | 2733 | 13 | 4 | 4 | PASS |
| `switch_transformers` | 3462 | 12 | 8 | 0 | PASS |
| `sycophancy_to_subterfuge` | 8579 | 17 | 25 | 0 | PASS |
| `t5` | 2922 | 13 | 4 | 4 | PASS |
| `taming_bitwise_gpu_kernels` | 34534 | 19 | 7 | 0 | PASS |
| `taso` | 2851 | 13 | 4 | 4 | PASS |
| `tensor_comprehensions` | 3080 | 13 | 4 | 4 | PASS |
| `tensorir` | 2956 | 13 | 4 | 4 | PASS |
| `tensorrt_llm_architecture` | 4322 | 13 | 3 | 0 | PASS |
| `tilelang` | 2919 | 13 | 4 | 4 | PASS |
| `tinyiree` | 2829 | 13 | 4 | 4 | PASS |
| `torch_fx` | 5323 | 13 | 6 | 0 | PASS |
| `transformer` | 3048 | 13 | 4 | 4 | PASS |
| `transformer_xl` | 2815 | 13 | 4 | 4 | PASS |
| `triton_compiler` | 10022 | 17 | 5 | 0 | PASS |
| `tritonbench` | 10600 | 19 | 5 | 0 | PASS |
| `tvm_compiler` | 3012 | 13 | 4 | 4 | PASS |
| `vae` | 2930 | 13 | 4 | 4 | PASS |
| `vit` | 2803 | 13 | 4 | 4 | PASS |
| `wav2vec2` | 2758 | 13 | 4 | 4 | PASS |
| `weak_to_strong` | 10889 | 16 | 56 | 0 | PASS |
| `welder` | 3810 | 12 | 7 | 0 | PASS |
| `whisper` | 2799 | 13 | 4 | 4 | PASS |
| `xla_compiler` | 3298 | 13 | 4 | 4 | PASS |

