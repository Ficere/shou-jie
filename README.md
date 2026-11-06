# 守界 · FounderGuard

融资可以让渡股权，个人责任不能稀里糊涂。面向创始人及融资公司的投资协议审查 Agent Skill：输入协议与关联文件，输出风险定位、责任边界、情景测算、修改草案和谈判顺序。

Founder-side financing agreement review: trace liability, test downside scenarios, and prepare actionable negotiation drafts.

按 [Agent Skills 开放标准](https://agentskills.io) 组织，可供支持该标准的 Agent 加载；各宿主的文件读取、联网和脚本能力不同，本项目未逐一完成跨平台实测。

## 安装 / Install

```bash
npx skills add Ficere/shou-jie
```

安装器需要 Node.js。核心审查无需 Python；实时法律核验需要联网，可选经济测算脚本需要 Python 3.10+。

<details>
<summary>手动安装与 Perplexity Computer / Alternative methods</summary>

```bash
git clone https://github.com/Ficere/shou-jie.git
```

将仓库完整目录放入宿主支持的 skills 路径，例如 `~/.claude/skills/shou-jie/` 或 `~/.codex/skills/shou-jie/`，以宿主说明为准。

Perplexity Computer 可将完整技能目录打成 ZIP，在 [Skills 管理页面](https://www.perplexity.ai/computer/skills) 导入。保留 `SKILL.md`、`references/`、`templates/`，需要测算时也保留 `scripts/`。

</details>

## 使用 / Usage

附上协议后，直接提出需求。可先提供脱敏文本，原始文件只在你授权的工作环境中处理。

```text
我是创始人，帮我审这份 A 轮 Term Sheet，先看个人回购和连带责任，
给出签署阻断项、首选改法与可以退让的方案。
```

```text
把增资协议、股东协议、章程和配偶同意函一起看，
检查“以所持股权价值为限”是否被赔偿或担保条款架空。
```

```text
投资人分三期打款，却要求我在技术指标失败时回购全部投资。
请核对出资、持股取得、里程碑和救济是否匹配，并给出替换条款。
```

```text
这份协议已经签了，我今天收到了回购通知。
请先整理触发、送达、行权和付款期限，再列出需要律师立即核验的问题。
```

```text
比较这两份融资方案。不要只看估值，
请推演失败、IPO 延迟、降价融资和低价退出时，公司与我各承担什么。
```

## 功能 / Features

| 模块 | 交付内容 |
|---|---|
| 主体与责任 | 区分公司、创始人、平台、配偶、关联方及回购/保证/赔偿 |
| 个人边界 | 分别核查金额上限、责任财产、变现机制及例外 |
| 文件群联动 | 发现主协议、章程、担保、配偶函和侧函的冲突与绕行 |
| 回购与对赌 | 触发可控性、里程碑、行权与付款期限、利息和重复受偿 |
| 经济收益 | 清算优先、反稀释、最惠国与退出权叠加 |
| 出资与治理 | 付款确定性、分期断档、否决权、董事、信息和资源承诺 |
| 情景推演 | 失败、IPO 延迟、降价融资、低价退出、投资人迟付 |
| 修改与谈判 | P0/P1/P2、首选/退让/底线、草案和待律师核验清单 |
| 法律证据 | 区分法律、纪要、参考答问、个案、政策和媒体转述 |
| 可选计算 | 单利回购、单轮清算分配、加权平均与完全棘轮价格对比 |

<details>
<summary>审查逻辑与输出 / Review logic and output</summary>

不预设“投资人不承担风险”，也不把严苛条款直接判为无效。逐项还原“权利人→触发→义务人→金额→上限→财产→期限→例外→救济”，看普通经营失败是否被转成个人不封顶债务。

- **P0：** 签署前必须处理的重大责任或结构冲突，不表示当然违法。
- **P1：** 重点谈判项，给出具体边界、程序和替代保护。
- **P2：** 清晰度、通知、协作等优化项。
- **待核验：** 证据状态，可与 P0 并列，不等于低风险。

不默认给总分，也不让其他低风险项抵消 P0。输出包含结论摘要、文件清单、责任图、逐条审查表、情景、修改草案、谈判顺序和律师复核事项；没有全文时，只做局部审查。

本项目没有把固定年利率、清算倍数、行权窗口或“以股权为限”等措辞视为普遍有效的安全港。参考入口见 [法律证据基线](references/legal-baseline.md)，每次实际审查仍须重新核验现行规则。

</details>

## 独立脚本 / Standalone script

Python 标准库即可运行；利率和持股比例用小数，金额使用同一币种。输出是合同假设下的算术，不是法律意见。

```bash
python scripts/economics.py --help
python scripts/economics.py redemption --principal 10000000 --rate 0.08 --days 730 --dividends 500000
python scripts/economics.py liquidation --investment 10000000 --share 0.2 --proceeds 15000000
python scripts/economics.py liquidation --investment 10000000 --share 0.2 --proceeds 15000000 --participating
python scripts/economics.py antidilution --old-price 10 --existing-diluted-shares 1000000 --new-money 1000000 --new-price 5
```

上述回购结果为 1110 万；同一退出额下非参与型投资人分配为 1000 万，参与型为 1100 万。清算输入必须是已扣债务、税费与交易费用后可分配给股东的金额；其他股东合计不等于创始人个人所得。

脚本不支持多轮优先级、参与封顶、分批本金、复利、分红时点调整或法律约束。复杂情况应另建可复核模型，不能强套单轮结果。

## 验证 / Validation

```bash
python -m unittest discover -s tests -v
agentskills validate "$PWD"
```

第一项验证经济算术，第二项需另行安装 `agentskills` 验证器。`tests/behavior-cases.md` 是独立的 Agent 行为回归规范，不会被单元测试自动执行；不能把算术通过等同法律推理正确。

## 目录结构 / Structure

```text
shou-jie/
├── SKILL.md                      # 技能入口与审查流程
├── references/
│   ├── review-checklist.md       # 逐条与跨文件检查
│   ├── legal-baseline.md         # 法律入口、层级与易错边界
│   └── clause-design.md          # 有限追索及谈判草案骨架
├── templates/
│   └── review-report.md          # 可独立交付的审查报告
├── scripts/
│   └── economics.py              # 单轮经济算术
├── tests/
│   ├── test_economics.py         # 自动算术测试
│   └── behavior-cases.md         # 合成行为回归案例
├── LICENSE                       # MIT
└── README.md                     # 安装与使用
```

## 免责声明 / Disclaimer

本项目用于融资协议风险识别和谈判准备，不构成律师意见、投资建议或效力保证。默认关注中国内地非上市公司股权融资；跨境、国资审批、已发生争议、重大个人责任等应由独立律师结合完整文件处理，法律和政策必须按使用当日重新核验。

This project supports issue spotting and negotiation preparation. It is not legal advice, an investment recommendation, or a guarantee of enforceability; obtain independent jurisdiction-specific counsel before signing or responding to a dispute.

## License

[MIT](LICENSE)。外链法律资料及第三方文章的权利归原权利人，本仓库许可不覆盖这些外部内容。
