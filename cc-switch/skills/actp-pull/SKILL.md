---
name: "actp-pull"
# 手动触发: 在 Claude Code / Cursor / Trae 中输入 /actp-pull 调用
---

# actp-pull · ACTP 团队开工前同步

按 ACTP 项目组规范执行每日开工前代码同步: 拉取当前分支最新代码, 合并 `origin/yra_dev` 主干, 并**以人能读懂的方式输出本次拉取带来的变更**。

## 适用角色

- 普通组员(在自己个人分支上工作)
- 小组负责人(在 `hepengyue` / `why_dev` / `zdy` 负责人分支上工作)
- yra_dev 总负责人(在 `yra_dev` 上工作,本 skill 仅做"只拉取 yra_dev 自己"的同步)

**注意**: 本 skill 只处理"拉取 + 合并 yra_dev + 变更摘要", 不负责"合并多个组员分支"——那是 `actp-push` 或更上层的合并流程负责。

## 触发词(任一即可)

- "开工"、"开始开发"、"拉取代码"、"拉最新代码"、"同步代码"
- "pull"、"fetch"、"merge yra_dev"
- 用户在 SourceTree/Cursor 上下文里说"我今天要开始干活了"
- 用户主动问"今天 yra_dev 上有没有新东西"

## 执行步骤(严格顺序)

### 1. 确认当前分支(安全前置)

```bash
git branch --show-current
git status --short
```

- 如果 `git status` 显示有未提交修改 → **停止**, 提示用户: "当前有未提交修改, 请先提交或 `git stash` 再开工"(`stash` 命令参考下方)
- 记下当前分支名, 后续所有操作都基于这个分支

### 2. Fetch 远程

```bash
git fetch origin --prune
```

刷新所有远程分支和 tag, 同时清理已删除的远程引用。

### 3. Pull 当前分支(与远程同名的分支)

```bash
git pull --ff-only origin <当前分支>
```

- **必须** `--ff-only`: 拒绝非快进合并, 避免无意中引入合并提交
- 如果 pull 失败(可能有未推送的本地提交 + 远程有新提交), 停下来提示用户处理, 不要自动 rebase 或 merge

### 4. 合并 `origin/yra_dev`(开工前强制动作)

```bash
git merge origin/yra_dev --no-ff -m "merge: 同步 yra_dev 主干 $(date +%Y-%m-%d)"
```

- 普通组员 / 负责人: **必须** 合并 `origin/yra_dev` 到当前分支
- yra_dev 总负责人: 跳过此步(已经在主干上)

### 5. 如果发生冲突

立刻停下来, **不要尝试自动解决**, 输出:

```
冲突文件: <列出所有 unmerged 文件>
yra_dev 最新提交: <hash + 标题>
建议: 联系相关组员确认业务逻辑, 详见 actp-push 的冲突处理段。
```

### 6. 输出变更摘要(本 skill 的核心交付)

这一步是**用户最在意的**, 不能只输出"已拉取成功"。

执行:

```bash
# 本次合并 origin/yra_dev 引入的提交列表
git log --oneline origin/yra_dev~1..origin/yra_dev 2>/dev/null
# 或更稳: HEAD@{1} 拿到 merge 前的位置
git log --oneline -1 HEAD@{1} 2>/dev/null
# 实际合并进来的文件统计
git diff --stat HEAD@{1} HEAD
```

按以下格式输出(中文, 简洁, 适合给组员 / 负责人发群消息):

```
【开工同步摘要】 <当前分支>
时间: <今天日期>
来源: origin/yra_dev

改动文件数: <N>
涉及模块: <按目录聚类, 如 actp-mnzb / actp-ui / docs>

核心变更(按 commit 倒序, 最多 5 条):
  - <hash 短>  <提交类型: feat/fix/refactor/chore>  <一句话功能说明>
  - <hash 短>  <类型>  <说明>
  ...

风险提示(如有):
  - <涉及数据库变更 / 配置文件 / 接口契约 的 commit>

下一步: 本地运行 <启动命令> 确认能跑起来, 即可开始今天的开发。
```

**变更摘要的数据源**:
1. `git log --oneline <merge-base>..origin/yra_dev` — 列出 yra_dev 新增的提交
2. `git diff --stat HEAD@{1} HEAD` — 列出实际合并进来的文件统计
3. 提交信息里的 `feat/fix/refactor/chore` 类型前缀(ACTP 团队规范)

如果项目根有 `AGENTS.md` 或 `docs/` 目录, **主动读取** 来补充业务上下文(比如这个模块是干什么的、某个 API 改了影响哪些下游), 让摘要更可读。

### 7. 自测(轻量)

提示用户: "建议先跑一遍相关模块的启动命令 / 单测, 确认 yra_dev 合并没破坏本地环境, 再开始新功能开发。"

## 禁止事项(踩坑警示)

- 禁止在有未提交修改时直接 pull(会冲突或丢失改动)
- 禁止用 `git pull`(默认行为, 可能在错误分支上产生 merge commit)—— 永远用 `git pull --ff-only origin <当前分支>`
- 禁止把 yra_dev 直接 `git pull`(双击 yra_dev 会切到 yra_dev 分支, 普通组员应在自己分支上)
- 禁止自动 `--rebase`(会改写本地未推送的提交历史, 团队协作风险)
- 禁止跳过"输出变更摘要"步骤——这是本 skill 区别于裸 `git pull` 的核心价值

## 备用: 工作区有未提交修改怎么办

```bash
# 方案 A: 提交(推荐)
git add <本次相关文件>
git commit -m "work: 保存当前开发进度"

# 方案 B: 临时保存
git stash push -u -m "临时保存: <功能说明>"
# 恢复时:
git stash list
git stash pop
# 恢复后必须 git status 检查(可能产生冲突)
```

## 关联

- `actp-push`: 推送前的代码审查 + 冲突诊断 + 推送
- ACTP 团队规范原文: `SourceTree团队代码拉取提交与推送规范(2).pdf` §4.1 §5