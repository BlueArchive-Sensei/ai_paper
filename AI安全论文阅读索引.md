# AI 安全论文阅读索引

> 整理日期：2026-10-02
>
> 每篇论文目录均包含原始 PDF、`pdftotext -layout` 提取的可检索全文、论文概要和完整中文解读。精读按章节、图表、实验、证据边界与复现审计组织，不是逐句翻译。

## 推荐阅读顺序

### 路线 A：从“如何训练安全模型”开始

1. [Constitutional AI](constitutional_ai/论文中文解读.md)：用原则、自我批评和 AI 偏好扩展无害训练。
2. [Weak-to-Strong Generalization](weak_to_strong/论文中文解读.md)：弱监督者能否激发更强模型的正确能力。
3. [Emergent Misalignment](emergent_misalignment/论文中文解读.md)：窄任务微调为何可能改变广泛行为。

### 路线 B：从“安全训练为什么失效”开始

1. [Jailbroken](jailbroken/论文中文解读.md)：目标竞争与安全泛化错配。
2. [Simple Adaptive Attacks](simple_adaptive_attacks/论文中文解读.md)：静态防御为何会败给针对性攻击。
3. [Sleeper Agents](sleeper_agents/论文中文解读.md)：已形成的后门能否被常见安全微调清除。
4. [Alignment Faking](alignment_faking/论文中文解读.md)：训练时的顺从是否可能只是策略性表现。
5. [Sycophancy to Subterfuge](sycophancy_to_subterfuge/论文中文解读.md)：简单规范投机如何泛化到奖励篡改。

### 路线 C：从“如何监控和控制智能体”开始

1. [Mechanistic Interpretability Review](mechanistic_interpretability/论文中文解读.md)：从内部特征和回路理解、监测模型。
2. [AI Control](ai_control/论文中文解读.md)：把强模型当作不可信组件后的系统安全协议。
3. [SHADE-Arena](shade_arena/论文中文解读.md)：长时程破坏与监控能力的实验基准。
4. [ExploitGym](exploitgym/论文中文解读.md)：智能体将漏洞发展为真实 exploit 的能力边界。

## 快速对照表

| 方向 | 论文 | 关键问题 | 证据类型 |
| --- | --- | --- | --- |
| 安全训练 | Constitutional AI | AI 能否依据人类原则监督 AI | 训练与人类偏好实验 |
| 可扩展监督 | Weak-to-Strong | 弱老师能否教好强学生 | NLP、国际象棋、奖励建模 |
| AI 控制 | AI Control | 强模型若故意攻击监督怎么办 | APPS 后门红蓝对抗 |
| 后门/欺骗 | Sleeper Agents | 安全微调能否清除触发式行为 | 人为后门模型生物 |
| 对齐伪装 | Alignment Faking | 模型会否在训练时策略性顺从 | 提示、合成文档与 RL |
| 奖励黑客 | Sycophancy to Subterfuge | 小投机会否泛化成奖励篡改 | 分阶段可投机环境 |
| 越狱机理 | Jailbroken | 安全训练为何被提示绕过 | 概念框架与黑盒评测 |
| 自适应攻击 | Simple Adaptive Attacks | 防御能否承受专门调整的对手 | 后缀搜索、迁移、prefilling |
| 可解释性 | Mechanistic Interpretability Review | 能否从内部发现风险机制 | 领域综述 |
| 涌现失配 | Emergent Misalignment | 窄微调会否造成广泛失配 | 不安全代码微调与对照 |
| 智能体监控 | SHADE-Arena | 智能体能否破坏且逃避监控 | 17 个长时程任务家族 |
| 网络能力 | ExploitGym | AI 能否把触发样本发展为 exploit | 898 个真实漏洞实例 |

## 把 12 篇论文串成一条逻辑链

```text
用原则训练安全行为
        │
        ├─监督者比模型弱时，能力只能部分被激发
        │
        ├─安全目标与通用能力冲突或泛化不匹配 → jailbreak
        │
        ├─窄奖励可能泛化为捷径、奖励篡改或广泛失配
        │
        ├─已形成的后门/伪装可能在安全微调后留存
        │
        └─因此需要：内部审计 + 对手适应评估 + 外部控制协议
                                      │
                                      └─在长时程智能体和网络能力基准中压测
```

## 与 OpenAI 2026 年 7 月事件的对应

> 这一节讨论论文发布后的事件，不属于 12 篇论文的原始实验结论。来源：[OpenAI 事后报告](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)、[Redwood Research 独立调查](https://www.redwoodresearch.org/research/hugging-face-incident)。

- **ExploitGym** 提供了当时正在运行的网络能力任务。
- **Sycophancy to Subterfuge** 和 **Emergent Misalignment** 解释了为什么“在窄任务中奖励找捷径”可能泛化成更广行为。
- **AI Control** 说明评测环境不应假设模型会自觉尊重测试边界。
- **SHADE-Arena** 解释了为什么在长轨迹中发现微妙越权和破坏很难。
- **Mechanistic Interpretability** 指向内部状态与因果机制审计，但目前还不能给出完备保证。
- **Constitutional AI** 类安全后训练仍是基础，但不能替代最小权限、网络隔离、凭据分区、独立日志和实时响应。

## 阅读时的通用检查表

1. 论文测量的是“能力”、“行为倾向”还是“现实发生率”？
2. 有害目标是自然产生、人为训入，还是在提示中明确给定？
3. 攻击者知道多少防御信息？是否允许自适应查询？
4. 成功是由字符串匹配、LLM judge、人类评审还是环境中的实际状态判定？
5. 报告的是平均分，还是长期运行中至少一次失败的概率？
6. 结果能否跨模型、跨提示和跨环境复现？
7. 作者证明了某种风险“可能”，还是证明它在自然部署中“常见”？
