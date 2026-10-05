# 论文精读与 GitHub Markdown 审核报告

- 审核日期：2026-10-05
- 审核范围：仓库内全部 295 个 Markdown 文件，包括 141 个精读、141 个概要、11 个根目录入口/索引和 2 份上游资料
- 总体结论：**295/295 个 Markdown 文件通过 GitHub 渲染结构、表格、数学、链接和本地解析检查**
- 精读统计：count=141，字符总数=533404，min=1664，median=2456，max=36003，H2=1842
- 图像资源：整页截图 0；独立图表 7；图表中文翻译块 7
- 全仓库本地链接：1,439 个，错误 0

## GitHub Markdown 全仓库整改

首轮检查发现 201 个文件至少存在一项格式问题，现已全部修复：

- 67 个文件的文件尾换行不规范；
- 644 处连续空行、23 处尾随空格；
- 20 处标题前后缺少空行，9 处列表前缺少空行；
- 1 个数学代码围栏未正确关闭，6 处围栏前后缺少空行；
- 84 个星号列表标记已统一为短横线；
- 2 份 TensorRT-LLM 文档存在多 H1、Setext 标题、Sphinx 锚点、MyST 指令或无效 HTML；
- 13 个依赖上游仓库结构的失效相对链接已改为有效的 GitHub 链接。

## GitHub Markdown 终检结果

| 检查项 | 通过标准 | 结果 |
|---|---|---|
| 文件范围 | 所有 `.md` 均参与审核 | 295/295 |
| 一级标题 | 每个文件首个非空行是 H1，且全文只有一个 H1 | 295/295 |
| 标题结构 | ATX 标题、层级不跳级、标题前后有空行、无重复标题 | 295/295 |
| 空白字符 | 无尾随空格、Tab、CRLF、连续空行；文件尾恰好一个换行 | 295/295 |
| 代码围栏 | 全部成对闭合、带语言标识、前后留空行，统一使用反引号 | 62 个代码块入口，错误 0 |
| 数学公式 | 无旧式分隔符；`$$` 和行内 `$...$` 成对闭合 | 错误 0 |
| 表格 | 表头、分隔行、列数及表格前后空行符合 GFM | 147 张表，错误 0 |
| 列表 | 统一短横线标记，编号格式和嵌套缩进可被 GFM 正确解析 | 错误 0 |
| HTML 扩展 | `details/summary` 成对；删除不平衡 `div`；保留有效显式锚点 | 错误 0 |
| 非 GFM 语法 | Sphinx 锚点和 MyST note 已转为 HTML 锚点与 GitHub Alert | 残留 0 |
| 图片 | 图片 alt 非空；无论文整页文字截图 | 7/7 独立图表通过 |
| 本地链接 | PDF、文本、图表和 Markdown 相对链接目标存在 | 1,439/1,439 |
| 实际解析 | 使用本地 Markdown 解析器逐文件渲染 | 295/295 |

说明：GitHub Flavored Markdown 允许原生 HTML、自动链接和长表格行，因此没有强制 80 字符换行，也没有删除用于 `details`、`summary`、`br` 和显式锚点的有效 HTML。

## 图片与中文解释整改

1. 删除 823 个 `page-*` 整页渲染文件，共约 238 MB。
2. 删除全部 1,434 处整页截图 Markdown 引用。
3. 141 篇精读的证据导航统一只提供本地 PDF 与可检索文本。
4. 仓库目前只保留 7 张从论文源码导出的独立架构图、流程图和性能图。
5. 7 张图全部具有中文图题、英文标签翻译、坐标或流程含义和证据边界。
6. 图表密集或术语困难的 12 篇论文保留“图表英文术语与坐标轴翻译”章节。

## 本轮新增专题审核

- 新增 12 篇、24 份中文 Markdown，覆盖 CoT、Self-Consistency、ToT、PRM、test-time scaling 与六篇推测解码论文。
- 12/12 篇均具备 PDF、可检索文本、概要和精读；没有新增任何图片或文字截图。
- 每篇精读均单列原文方法与公式、主实验、消融或失败模式、证据边界和复现检查。
- 新增 [近代高级算法论文阅读索引](近代高级算法论文阅读索引.md)，将 MoE、Reasoning/test-time scaling 与 Speculative decoding 设为同级算法分支。

## 当前强制写作标准

- 摘要、定义、实验设置、结论、表格说明和附录论证必须写成可独立阅读的中文。
- 图片只允许真正的架构图、流程图、曲线图、柱状图、热力图或其他数据图表。
- 每张图必须紧邻中文图题、图例/标签翻译、坐标轴解释、主要趋势和证据边界。
- 专有名词第一次出现时保留英文。
- 每个 Markdown 文件必须只有一个 H1，并通过结构、表格、数学、链接和解析检查。

## 审核边界

- “中文精读”是忠实重建论证，不是逐词机械直译；目标是让中文读者不看英文页面也能理解论文。
- 当前只有一篇论文的源码包提供了可直接复用的 7 张独立图表。其他论文暂不展示图片，避免把整页渲染冒充图表。
- 后续若增加 Markdown 或裁切新图表，应按本报告同一规则重新审核。

## 逐篇精读追踪表

| 目录 | 字符数 | H2 | 独立图表 | 图中文字翻译 | 专项术语表 | 文字页引用 | 结果 |
|---|---:|---:|---:|---:|---:|---:|---|
| `ada_mk` | 3352 | 12 | 0 | 0 | 否 | 0 | PASS |
| `ai_control` | 9584 | 17 | 0 | 0 | 是 | 0 | PASS |
| `alibi` | 1942 | 13 | 0 | 0 | 否 | 0 | PASS |
| `alignment_faking` | 11543 | 19 | 0 | 0 | 是 | 0 | PASS |
| `alpa` | 2256 | 13 | 0 | 0 | 否 | 0 | PASS |
| `alphafold2` | 2156 | 13 | 0 | 0 | 否 | 0 | PASS |
| `alphazero` | 1664 | 13 | 0 | 0 | 否 | 0 | PASS |
| `ansor` | 2031 | 13 | 0 | 0 | 否 | 0 | PASS |
| `anthropic_claude3_model_card` | 2599 | 11 | 0 | 0 | 否 | 0 | PASS |
| `anthropic_scaling_monosemanticity` | 2456 | 11 | 0 | 0 | 否 | 0 | PASS |
| `ascend_cloudmatrix384` | 4228 | 12 | 0 | 0 | 否 | 0 | PASS |
| `bahdanau_attention` | 1880 | 13 | 0 | 0 | 否 | 0 | PASS |
| `bert` | 2087 | 13 | 0 | 0 | 否 | 0 | PASS |
| `bigbird` | 1870 | 13 | 0 | 0 | 否 | 0 | PASS |
| `bolt` | 2127 | 13 | 0 | 0 | 否 | 0 | PASS |
| `chainer_define_by_run` | 3314 | 11 | 0 | 0 | 否 | 0 | PASS |
| `chinchilla` | 2024 | 13 | 0 | 0 | 否 | 0 | PASS |
| `clip` | 2020 | 13 | 0 | 0 | 否 | 0 | PASS |
| `constitutional_ai` | 10805 | 21 | 0 | 0 | 是 | 0 | PASS |
| `cute_layout_algebra` | 3397 | 13 | 0 | 0 | 否 | 0 | PASS |
| `cutedsl_torchinductor` | 3916 | 14 | 0 | 0 | 否 | 0 | PASS |
| `ddpm` | 2061 | 13 | 0 | 0 | 否 | 0 | PASS |
| `deep_q_network` | 4692 | 13 | 0 | 0 | 否 | 0 | PASS |
| `deepseek_moe` | 2746 | 10 | 0 | 0 | 否 | 0 | PASS |
| `deepseek_r1` | 3427 | 12 | 0 | 0 | 否 | 0 | PASS |
| `deepseek_v2` | 3030 | 11 | 0 | 0 | 否 | 0 | PASS |
| `deepseek_v3` | 4375 | 14 | 0 | 0 | 是 | 0 | PASS |
| `disc_dynamic_shape` | 4149 | 13 | 0 | 0 | 否 | 0 | PASS |
| `distral` | 4751 | 13 | 0 | 0 | 否 | 0 | PASS |
| `dit` | 2162 | 13 | 0 | 0 | 否 | 0 | PASS |
| `dpo` | 2225 | 13 | 0 | 0 | 否 | 0 | PASS |
| `dynamic_computation_graphs` | 3747 | 11 | 0 | 0 | 否 | 0 | PASS |
| `emergent_misalignment` | 11113 | 15 | 0 | 0 | 是 | 0 | PASS |
| `event_tensor` | 3152 | 13 | 0 | 0 | 否 | 0 | PASS |
| `exploitgym` | 9927 | 17 | 0 | 0 | 否 | 0 | PASS |
| `flamingo` | 2096 | 13 | 0 | 0 | 否 | 0 | PASS |
| `flash_attention` | 2255 | 13 | 0 | 0 | 否 | 0 | PASS |
| `flash_attention_2` | 2090 | 13 | 0 | 0 | 否 | 0 | PASS |
| `flash_attention_3` | 2217 | 13 | 0 | 0 | 否 | 0 | PASS |
| `flash_attention_4` | 2332 | 13 | 0 | 0 | 否 | 0 | PASS |
| `fp4_flash_attention_4` | 2209 | 13 | 0 | 0 | 否 | 0 | PASS |
| `fusion_stitching` | 3576 | 12 | 0 | 0 | 否 | 0 | PASS |
| `gan` | 1918 | 13 | 0 | 0 | 否 | 0 | PASS |
| `gcn` | 1805 | 13 | 0 | 0 | 否 | 0 | PASS |
| `gemini` | 1917 | 13 | 0 | 0 | 否 | 0 | PASS |
| `glow_compiler` | 2091 | 13 | 0 | 0 | 否 | 0 | PASS |
| `gpt1` | 2087 | 13 | 0 | 0 | 否 | 0 | PASS |
| `gpt2` | 2011 | 13 | 0 | 0 | 否 | 0 | PASS |
| `grouped_query_attention` | 2105 | 13 | 0 | 0 | 否 | 0 | PASS |
| `gspmd` | 2121 | 13 | 0 | 0 | 否 | 0 | PASS |
| `hidet` | 2040 | 13 | 0 | 0 | 否 | 0 | PASS |
| `human_preferences_rl` | 5076 | 15 | 0 | 0 | 否 | 0 | PASS |
| `instella_moe` | 2117 | 13 | 0 | 0 | 否 | 0 | PASS |
| `jailbroken` | 6191 | 15 | 0 | 0 | 是 | 0 | PASS |
| `janus_symbolic_graph` | 3830 | 13 | 0 | 0 | 否 | 0 | PASS |
| `kimi_k15` | 2467 | 11 | 0 | 0 | 否 | 0 | PASS |
| `kimi_k2` | 2842 | 11 | 0 | 0 | 否 | 0 | PASS |
| `kimi_mooncake` | 2651 | 10 | 0 | 0 | 否 | 0 | PASS |
| `knowledge_distillation` | 4962 | 14 | 0 | 0 | 否 | 0 | PASS |
| `korch` | 3501 | 13 | 0 | 0 | 否 | 0 | PASS |
| `latent_diffusion` | 2023 | 13 | 0 | 0 | 否 | 0 | PASS |
| `linear_layouts` | 13828 | 23 | 0 | 0 | 否 | 0 | PASS |
| `linformer` | 2044 | 13 | 0 | 0 | 否 | 0 | PASS |
| `llama` | 2071 | 13 | 0 | 0 | 否 | 0 | PASS |
| `llama_3` | 2033 | 13 | 0 | 0 | 否 | 0 | PASS |
| `llava` | 1993 | 13 | 0 | 0 | 否 | 0 | PASS |
| `longformer` | 2046 | 13 | 0 | 0 | 否 | 0 | PASS |
| `lstm` | 1941 | 13 | 0 | 0 | 否 | 0 | PASS |
| `mamba` | 2124 | 13 | 0 | 0 | 否 | 0 | PASS |
| `mamba_2` | 2162 | 13 | 0 | 0 | 否 | 0 | PASS |
| `mechanistic_interpretability` | 7303 | 17 | 0 | 0 | 是 | 0 | PASS |
| `megablocks` | 3598 | 13 | 0 | 0 | 否 | 0 | PASS |
| `metaschedule` | 1949 | 13 | 0 | 0 | 否 | 0 | PASS |
| `minimax_01` | 2804 | 11 | 0 | 0 | 否 | 0 | PASS |
| `minimax_m1` | 2800 | 11 | 0 | 0 | 否 | 0 | PASS |
| `mirage_persistent_kernel` | 3721 | 14 | 0 | 0 | 否 | 0 | PASS |
| `mlir` | 2281 | 13 | 0 | 0 | 否 | 0 | PASS |
| `multi_query_attention` | 2168 | 13 | 0 | 0 | 否 | 0 | PASS |
| `muzero` | 6599 | 16 | 0 | 0 | 否 | 0 | PASS |
| `nimble_dynamic_nn` | 4504 | 13 | 0 | 0 | 否 | 0 | PASS |
| `openai_codex` | 2181 | 11 | 0 | 0 | 否 | 0 | PASS |
| `openai_gpt3` | 2402 | 11 | 0 | 0 | 否 | 0 | PASS |
| `openai_gpt4` | 2078 | 10 | 0 | 0 | 否 | 0 | PASS |
| `openai_gpt_oss` | 2805 | 11 | 0 | 0 | 否 | 0 | PASS |
| `openai_instructgpt` | 2313 | 10 | 0 | 0 | 否 | 0 | PASS |
| `palm` | 2027 | 13 | 0 | 0 | 否 | 0 | PASS |
| `performer` | 2059 | 13 | 0 | 0 | 否 | 0 | PASS |
| `policy_distillation` | 4910 | 13 | 0 | 0 | 否 | 0 | PASS |
| `proximal_policy_optimization` | 5112 | 13 | 0 | 0 | 否 | 0 | PASS |
| `pytorch_2` | 9746 | 20 | 0 | 0 | 否 | 0 | PASS |
| `pytorch_graph_programming_model` | 6579 | 19 | 0 | 0 | 否 | 0 | PASS |
| `pytorch_imperative` | 4013 | 11 | 0 | 0 | 否 | 0 | PASS |
| `qwen_3` | 2063 | 13 | 0 | 0 | 否 | 0 | PASS |
| `rammer` | 2141 | 13 | 0 | 0 | 否 | 0 | PASS |
| `resnet` | 1859 | 13 | 0 | 0 | 否 | 0 | PASS |
| `roller` | 1826 | 13 | 0 | 0 | 否 | 0 | PASS |
| `rope` | 1976 | 13 | 0 | 0 | 否 | 0 | PASS |
| `sam` | 2076 | 13 | 0 | 0 | 否 | 0 | PASS |
| `scaling_laws` | 2047 | 13 | 0 | 0 | 否 | 0 | PASS |
| `seq2seq` | 1718 | 13 | 0 | 0 | 否 | 0 | PASS |
| `shade_arena` | 9680 | 15 | 0 | 0 | 是 | 0 | PASS |
| `simple_adaptive_attacks` | 9556 | 17 | 0 | 0 | 是 | 0 | PASS |
| `sleeper_agents` | 8625 | 18 | 0 | 0 | 是 | 0 | PASS |
| `soft_actor_critic` | 4900 | 13 | 0 | 0 | 否 | 0 | PASS |
| `sparsely_gated_moe` | 3340 | 12 | 0 | 0 | 否 | 0 | PASS |
| `swin_transformer` | 1951 | 13 | 0 | 0 | 否 | 0 | PASS |
| `switch_transformers` | 3092 | 12 | 0 | 0 | 否 | 0 | PASS |
| `sycophancy_to_subterfuge` | 7529 | 17 | 0 | 0 | 是 | 0 | PASS |
| `t5` | 2135 | 13 | 0 | 0 | 否 | 0 | PASS |
| `taming_bitwise_gpu_kernels` | 36003 | 19 | 7 | 7 | 否 | 0 | PASS |
| `taso` | 2063 | 13 | 0 | 0 | 否 | 0 | PASS |
| `tensor_comprehensions` | 2282 | 13 | 0 | 0 | 否 | 0 | PASS |
| `tensorir` | 2158 | 13 | 0 | 0 | 否 | 0 | PASS |
| `tensorrt_llm_architecture` | 4208 | 13 | 0 | 0 | 否 | 0 | PASS |
| `tilelang` | 2126 | 13 | 0 | 0 | 否 | 0 | PASS |
| `tinyiree` | 2041 | 13 | 0 | 0 | 否 | 0 | PASS |
| `torch_fx` | 4112 | 13 | 0 | 0 | 否 | 0 | PASS |
| `transformer` | 2261 | 13 | 0 | 0 | 否 | 0 | PASS |
| `transformer_xl` | 2033 | 13 | 0 | 0 | 否 | 0 | PASS |
| `triton_compiler` | 8937 | 17 | 0 | 0 | 否 | 0 | PASS |
| `tritonbench` | 9543 | 19 | 0 | 0 | 否 | 0 | PASS |
| `tvm_compiler` | 2214 | 13 | 0 | 0 | 否 | 0 | PASS |
| `vae` | 2148 | 13 | 0 | 0 | 否 | 0 | PASS |
| `vit` | 2021 | 13 | 0 | 0 | 否 | 0 | PASS |
| `wav2vec2` | 1976 | 13 | 0 | 0 | 否 | 0 | PASS |
| `weak_to_strong` | 7686 | 16 | 0 | 0 | 是 | 0 | PASS |
| `welder` | 3476 | 12 | 0 | 0 | 否 | 0 | PASS |
| `whisper` | 2012 | 13 | 0 | 0 | 否 | 0 | PASS |
| `xla_compiler` | 2510 | 13 | 0 | 0 | 否 | 0 | PASS |
| `chain_of_thought` | 3097 | 7 | 0 | 0 | 是 | 0 | PASS |
| `self_consistency` | 3387 | 9 | 0 | 0 | 是 | 0 | PASS |
| `tree_of_thoughts` | 3402 | 8 | 0 | 0 | 是 | 0 | PASS |
| `lets_verify_step_by_step` | 3181 | 10 | 0 | 0 | 是 | 0 | PASS |
| `scaling_test_time_compute` | 3837 | 10 | 0 | 0 | 是 | 0 | PASS |
| `s1_test_time_scaling` | 3668 | 10 | 0 | 0 | 是 | 0 | PASS |
| `speculative_decoding` | 3322 | 10 | 0 | 0 | 是 | 0 | PASS |
| `speculative_sampling` | 3526 | 10 | 0 | 0 | 是 | 0 | PASS |
| `specinfer` | 3381 | 10 | 0 | 0 | 是 | 0 | PASS |
| `medusa` | 3598 | 10 | 0 | 0 | 是 | 0 | PASS |
| `eagle_speculative` | 3575 | 10 | 0 | 0 | 是 | 0 | PASS |
| `eagle_2` | 3574 | 10 | 0 | 0 | 是 | 0 | PASS |
