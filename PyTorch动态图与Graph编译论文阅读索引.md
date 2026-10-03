# PyTorch 动态图与 Graph 编译论文阅读索引

> 整理日期：2026-10-03
>
> 本专题新增 7 篇论文与 1 份 PyTorch 官方工程资料，并复用仓库已有的 PyTorch 2 论文。每个新增目录均保存 PDF、可检索文本、论文概要、中文精读和精读引用的关键页面。

## 1. 先回答：PyTorch 里到底有哪些 Graph

“动态图”常被用来指完全不同的对象：

| 对象 | 何时产生 | 记录什么 | 主要用途 |
| --- | --- | --- | --- |
| Python 程序 | 用户编写时 | 控制流、对象、副作用 | 模型与训练逻辑 |
| Eager operator stream | 每次运行时 | 实际发出的 tensor operations | 立即执行 |
| Autograd graph | forward 运行时 | backward dependencies、saved tensors | reverse-mode 自动微分 |
| FX graph | symbolic trace/capture 时 | module/function/method calls | 分析、变换、lowering |
| Dynamo compiled region | torch.compile 运行时 | FX graph、residual bytecode、guards | JIT 优化与缓存复用 |
| AOTAutograd graphs | compile pipeline 中 | 规范化的 forward/backward | 训练编译 |
| ExportedProgram | torch.export 时 | full graph、signature、shape constraints | AOT 与部署 |

最重要的结论：

- PyTorch eager 能执行某段 Python，不代表它能被完整 capture。
- Autograd graph 能正确求导，不代表它适合 quantization、fusion 或部署。
- Dynamic shape 不代表无 specialization，也不代表 dynamic rank。
- Graph break 保留兼容性，但会减少跨区域优化机会。

## 2. 推荐阅读路线

### 路线 A：先理解动态图的原始语义

1. [Chainer](chainer_define_by_run/论文中文解读.md)：Define-by-Run 改变的是构图时机。
2. [PyTorch 2019](pytorch_imperative/论文中文解读.md)：普通 Python、eager execution 与动态 autograd。
3. [Dynamic Computation Graphs](dynamic_computation_graphs/论文中文解读.md)：输入 topology 不规则时，如何通过 dynamic batching 找回硬件并行。

读完应能区分：

- 本次运行路径产生的 backward graph；
- 每个样本本身不同的 tree/graph topology；
- tensor dimension 变化。

### 路线 B：命令式程序如何变成可优化图

1. [JANUS](janus_symbolic_graph/论文中文解读.md)：profiling、assumptions、assertions、graph cache 与 fallback。
2. [torch.fx](torch_fx/论文中文解读.md)：symbolic tracing、Proxy、GraphModule 和 transform API。
3. [PyTorch 2](pytorch_2/论文中文解读.md)：Dynamo、AOTAutograd 与 Inductor 的端到端组合。

核心演进：

    one-shot trace
        -> customizable symbolic trace
        -> bytecode capture + guards
        -> graph break / recompile
        -> forward/backward graph compilation

### 路线 C：动态 Shape 与 Runtime

1. [Nimble](nimble_dynamic_nn/论文中文解读.md)：Any dimension、shape function、dynamic memory 与 VM。
2. [DISC](disc_dynamic_shape/论文中文解读.md)：DHLO、compiled host flow、shape constraints 与动态 fusion。
3. [PyTorch Graph Programming Model](pytorch_graph_programming_model/论文中文解读.md)：SymInt/FakeTensor、backed/unbacked symbols、guards 与 export constraints。

三者关注点不同：

| 材料 | 主要动态性 | Runtime 策略 | 主要代价 |
| --- | --- | --- | --- |
| Nimble | control、structure、shape | 通用 VM 解释 bytecode | dispatch、shape function |
| DISC | static-rank dynamic dimensions | 编译生成 host flow | 通用 kernel 不及精确 specialization |
| PyTorch 现行文档 | Python capture + symbolic shapes | guards、cache、graph break/assertion | recompilation、graph fragmentation |

### 路线 D：面向实际使用

1. 用 [torch.fx](torch_fx/论文概要.md) 学 graph transformation。
2. 用 [PyTorch 2](pytorch_2/论文概要.md) 建立 compiler stack 全景。
3. 用 [官方 Programming Model](pytorch_graph_programming_model/论文中文解读.md#16-一套实用诊断顺序) 排查 graph breaks、guards、recompile 和 export。
4. 变长 sequence、检测、sparse/GNN workload 再读 [Nimble](nimble_dynamic_nn/论文概要.md) 与 [DISC](disc_dynamic_shape/论文概要.md)。
5. 树、AST、molecule 等输入 topology 动态时，读 [Dynamic Computation Graphs](dynamic_computation_graphs/论文概要.md)。

## 3. 全部资料快速对照

| 年份 | 资料 | 类型 | 核心概念 | 代表应用 |
| --- | --- | --- | --- | --- |
| 2017 | [Dynamic Computation Graphs](dynamic_computation_graphs/论文概要.md) | 论文 | dynamic batching | Tree-LSTM、molecule graph |
| 2019 | [Chainer](chainer_define_by_run/论文概要.md) | 论文 | Define-by-Run | 动态模型、CV、分布式训练 |
| 2019 | [PyTorch](pytorch_imperative/论文概要.md) | 论文 | eager + dynamic autograd | 通用研究与训练 |
| 2019 | [JANUS](janus_symbolic_graph/论文概要.md) | 论文 | speculative graph execution | CNN/RNN/TreeNN/GAN/RL |
| 2021 | [Nimble](nimble_dynamic_nn/论文概要.md) | 论文 | dynamic type + VM | LSTM、Tree-LSTM、BERT inference |
| 2021 | [DISC](disc_dynamic_shape/论文概要.md) | 论文 | dynamic HLO + shape-aware fusion | ASR、Seq2seq、BERT、推荐 |
| 2022 | [torch.fx](torch_fx/论文概要.md) | 论文 | symbolic trace + GraphModule | 量化、融合、分析、TensorRT |
| 2024 | [PyTorch 2](pytorch_2/论文概要.md) | 论文 | Dynamo + AOTAutograd + Inductor | eager program compilation |
| 2026 | [PyTorch Graph Programming Model](pytorch_graph_programming_model/论文概要.md) | 官方文档 | guards、graph breaks、export | 编译诊断与部署 |

## 4. 两条互相独立的“动态”轴

### 程序/拓扑动态

- branch path 由数据决定；
- loop count 变化；
- recursive tree topology 不同；
- Python type、callee 或 object state 改变。

对应技术：dynamic batching、control-flow op、profiling/speculation、guards、graph break。

### Shape 动态

- batch size 改变；
- sequence length 改变；
- image resolution 改变；
- output length 依赖数据；
- sparse/jagged tensor size 改变。

对应技术：symbolic dimension、shape function/meta kernel、constraints、runtime assertion、dynamic allocation、multi-version kernel。

一个模型可只在一条轴上动态，也可两条同时动态。不要仅凭“输入长度变化”断言 graph topology 也变了。

## 5. Graph 捕获方法比较

| 方法 | 观察对象 | 优点 | 主要风险 |
| --- | --- | --- | --- |
| Operator trace | 一次真实 tensor execution | 简单、贴近真实 op | 偶然路径被固化 |
| Symbolic trace | Proxy execution | 易生成高层可变换 DAG | Proxy-dependent Python control flow 失败 |
| AST/source transform | 源程序结构 | 可看 branch/loop syntax | Python 语义复杂、source 不总可得 |
| Bytecode interpretation | Python VM instructions | 覆盖调用链并生成 residual bytecode | guards、side effects 和版本兼容复杂 |
| Explicit graph API | 用户直接写 graph/control op | 语义清楚、AOT 友好 | 编程体验和 Python 互操作受限 |

现代 PyTorch 同时使用多种捕获方式，而不是只有一个 tracer。

## 6. Guards、Specialization 与 Recompile

假设捕获时观察到 shape 为 32。系统可以：

1. 生成仅接受 32 的 specialized graph；
2. 生成接受某个 range 的 symbolic graph；
3. graph break，让该段继续 eager；
4. export 失败，要求用户提供更明确的 constraint/control-flow operator。

通用 trade-off：

$$
T_{total} =
T_{capture}+T_{compile}+T_{guards}
+T_{execution}+T_{fallback/recompile}.
$$

过度 specialization：

- kernel 更容易优化；
- graph versions 增加；
- cache 与 compile latency 增加。

过度 dynamic：

- graph reuse 更高；
- symbolic reasoning 和 indexing 更复杂；
- kernel quality 可能下降。

## 7. 应用场景怎样选技术

### 普通固定结构训练

先保持 eager 正确，再用 torch.compile；重点检查 graph breaks、optimizer step 和 backward compilation。

### 变长 LLM/NLP

关注 sequence length guards、padding、automatic dynamic、kernel specialization 与 cache 命中，不只看是否“支持 dynamic”。

### Detection 与 sparse workload

data-dependent output 会产生 unbacked symbols；需要 fake/meta implementation、runtime assertion 或显式 structured control flow。

### Tree/AST/GNN

仅有 symbolic shape 可能不够；还要解决不同 topology 下的 node batching、segment operation 或 runtime scheduling。

### Quantization/硬件部署

需要显式 graph IR、functionalization、decomposition 和完整 export contract；autograd graph 不能替代。

## 8. 一套学习用的最小实验

1. 写一个带 Python shape branch 的 eager function。
2. 打印 autograd grad_fn 链，观察只包含实际分支。
3. 用 FX symbolic trace，观察 Proxy-dependent branch 为什么失败。
4. 用 torch.compile 运行多个 shape，记录 graph breaks、guards 和 recompiles。
5. 把 branch 改为显式 control-flow op，再尝试 torch.export。
6. 加一个 data-dependent output，例如 nonzero，区分 backed 与 unbacked symbol。
7. 比较 static specialization、dynamic graph 和 padding 的 compile time、steady latency 与 graph count。

## 9. 读性能结果的检查表

- compile/warmup 是否计入？
- 比较 eager、static graph、dynamic graph 还是手工 batching？
- graph construction/capture cost 是否遗漏？
- input shape/topology 分布是否真实？
- graph versions 与 guard failure 数量是多少？
- dynamic runtime 是否用了 padding 或 upper-bound allocation？
- kernel/library 版本与硬件是什么？
- 是 throughput、latency 还是 time-to-first-result？
- correctness 是否覆盖罕见路径与 mutation？

## 10. 版本提醒

- Chainer、TensorFlow Fold 和 JANUS 主要用于理解思想与历史，不是当前框架推荐。
- PyTorch 2019 解释 eager/autograd 基线；PyTorch 2 解释现代编译架构。
- 官方文档是 2026-10-03 的 main 分支快照，默认 tracing mode、dynamic shape API 和 guard 策略可能变化。
- torch.fx 论文中的 symbolic_trace 与 Dynamo 生成 FX graph 不能混为同一种捕获机制。
