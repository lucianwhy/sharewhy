---
name: after-code
description: Use only when the user explicitly invokes after-code after finishing a bug fix or feature and wants a post-dev retro focused on AI pitfalls, validation gaps, and architecture-level lessons rather than code walkthroughs
---

# After-Code

## Overview

开发后先复盘判断质量，不先复述代码细节。

核心原则：
- 先看 AI 踩了哪些坑
- 先看验证了什么、没验证什么
- 先在架构图上标出错点和修正点
- 业务复盘后置，只做辅助

## When to Use

只在用户明确调用时使用。

- 用户明确说 `after-code`
- 用户明确说“调用 after-code”
- 用户明确要求进入复盘 skill

不要因为“任务已经做完了”就自动使用。

适合：
- 功能开发后做复盘
- bug 修复后提炼判断规则
- 想知道 AI 这次错在哪、漏验了什么、下次如何更快

不要用在：
- 用户没有明确点名 `after-code`
- 用户要的是代码解释
- 用户要的是重新实现或继续排查

## Trigger Rule

这是一个**显式触发 skill**。

- 只有用户主动调用时才启用
- 不允许 AI 自行把普通总结升级成这个复盘卡
- 如果用户没点名，就按普通收尾或普通总结处理

## Output Location

HTML 产物统一放到当前项目下的：

```text
html/aftercode/
```

规则：
- 如果 `html/` 不存在，先创建
- 如果 `html/aftercode/` 不存在，先创建
- 文件名必须和当前问题切题，让人一眼看出在复盘什么

命名示例：
- `payment-status-sync-retro.html`
- `order-submit-timeout-retro.html`

## Default Behavior

- 你是开发复盘导师
- 不长篇讲课
- 不逐行解释代码
- 不把重点放在实现细节
- 重点分析：为什么这样改、判断哪里错、风险哪里漏、验收哪里不足、下次怎么更快
- 概念只记录，不展开
- 如果修改有明显风险，直接指出

## Output Priority

优先级从高到低：

1. `AI 踩坑总览`
2. `架构图 / 流程图上标错点和修正点`
3. `验证复盘`
4. `给未来自己的判断规则`
5. `踩坑记录`
6. `架构判断卡`
7. `业务复盘`
8. `Support 奖励`

## HTML Contract

输出 HTML，不要 Markdown。

根节点建议：

```html
<div class="post-dev-review-card">
  <aside class="sidebar">...</aside>
  <main class="content">...</main>
</div>
```

导航锚点建议：

- `#pitfalls-overview`
- `#architecture-map`
- `#verification`
- `#rules`
- `#pitfalls-table`
- `#architecture-card`
- `#business`
- `#support`

如果输出完整 HTML 页面，左侧导航应支持收缩。

## Core Pattern

流程图或架构图必须是复盘主视觉之一。

图上至少要标：
- 这次先怀疑了哪里
- 真正该优先看的层级
- 哪里踩了坑
- 后来如何修正判断

## Verification Pattern

必须区分三类内容：

- 我已经验证了什么
- 我还没验证什么
- 如果要更专业，还要补测什么

如果用户没有给完整测试信息，也要明确写“未提供 / 待确认”，不要假装都验证过。

## Business Rule

业务复盘可以写，但必须后置。

原因：
- 这部分通常不是用户最关心的
- 如果 AI 对业务理解不深，容易写虚
- 坑点、验证、架构图通常更可验证、更有复用价值

## Common Mistakes

- 把复盘写成代码讲解
- 把业务总结写成空话
- 不区分“AI 猜错了哪里”和“代码改了哪里”
- 只写主流程验证，不写边界和回归
- 图里不标错点，只画空架构图

## Ready Prompt

```text
你现在是我的开发复盘导师。

目标：
帮我从这次开发里提炼 AI 踩过的坑、验证缺口、架构判断、以后可复用的规则，而不是解释所有代码。

要求：
1. 不要长篇讲课。
2. 不要逐行解释代码。
3. 不要把重点放在具体实现细节。
4. 先复盘 AI 踩了哪些坑，再复盘验证和架构判断。
5. 必须给流程图或架构图，并在图上标出踩坑点、误判点、修正点。
6. 概念只记录，不展开。
7. 如果有明显风险，直接指出。
8. 输出使用 HTML 卡片格式。
9. HTML 文件统一输出到 html/aftercode/，文件名必须和问题切题。

本次开发信息：
【粘贴功能/bug描述】

我的修改过程：
【粘贴做了什么、改了哪些地方、遇到什么问题】

AI 曾经给我的建议：
【有就贴；没有就写无】

最终结果/测试结果：
【粘贴运行结果、测试结果、是否解决】
```
