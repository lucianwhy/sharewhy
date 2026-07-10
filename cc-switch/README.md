# ACTP Git 协作 Skills

> 配套 CC Switch 使用的 ACTP 团队 Git 协作 skill 集合
> 规范原文: `SourceTree团队代码拉取提交与推送规范(2).pdf` (2026-07-09)

## 包含的 Skill

| Skill | 触发场景 | 核心能力 |
|---|---|---|
| `actp-pull` | 开工 / 开始开发 / 拉取代码 | 切到个人分支 → fetch → pull → 合并 `origin/yra_dev` → 输出**本次拉取带来的变更摘要** |
| `actp-push` | 提交 / 推送 / push | 二次 fetch → 检查本地与远程分支对齐 → 落后则拉取 → 输出**本次 push 会改的代码摘要** → 无冲突则 push → 有冲突则**诊断冲突原因(双方各自实现什么功能导致冲突)** 并引导解决 |

## 设计原则

- **不替代 git**, 而是在裸 git 命令之上加"业务感知"和"团队协作规范"
- **不自动解决冲突**, 把决定权留给用户, 但提供"为什么冲突"和"双方在做什么"的人话解释
- **变更摘要必须输出**, 这是区别于普通 `git pull/push` 的核心价值
- **业务上下文自动读取**: 主动读项目根的 `AGENTS.md` 和 `docs/`, 让诊断报告带业务背景

## 安装

### 方式 1: 整组导入到 CC Switch(推荐)

```bash
# Windows PowerShell
$dest = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

# 克隆仓库后, 软链接或复制 actp-pull/actp-push 到全局 skills 目录
Copy-Item -Recurse .\cc-switch\skills\actp-pull $dest
Copy-Item -Recurse .\cc-switch\skills\actp-push $dest
```

### 方式 2: 复制到单个项目(项目级)

```bash
# 在你的 ACTP 项目根目录
$dest = ".\.claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse <sharewhy 路径>\cc-switch\skills\actp-pull $dest
Copy-Item -Recurse <sharewhy 路径>\cc-switch\skills\actp-push $dest
```

### 方式 3: CC Switch 应用商店

> 计划中: 等 CC Switch 商店支持自定义 skill 仓库后, 提交此仓库地址作为分发源。

## 配合 CC Switch 使用的效果

在 Claude Code / Cursor / Trae / Codex 中:

- 用户输入"开工" → 触发 `actp-pull` → 自动跑完整流程并给出变更摘要
- 用户输入"推送" → 触发 `actp-push` → 自动做分支对齐 + 冲突诊断 + 推送
- CC Switch 的供应商切换、MCP 路由等能力与本 skill 互不冲突

## 团队接入步骤

1. 团队成员安装 CC Switch (官网: ccswitch.io)
2. 把本目录下的 `actp-pull` 和 `actp-push` 导入到 `~/.claude/skills/`
3. 触发 `actp-pull` 完成第一次开工前同步
4. 触发 `actp-push` 完成第一次推送
5. 后续每天按"开工 actp-pull → 干活 → 推送 actp-push"循环

## 角色对照

| 角色 | 本地分支 | 推送目标 | 每日额外动作 |
|---|---|---|---|
| 普通组员 | `<个人分支>` | `origin/<个人分支>` | 通知小组负责人 |
| 小组负责人(hepengyue / why_dev / zdy) | `<负责人分支>` | `origin/<负责人分支>` | 依次合并所有组员, 通知 yra_dev 总负责人 |
| yra_dev 总负责人 | `yra_dev` | `origin/yra_dev` | 一次只合并一个负责人分支, 每合并一个测试一次 |