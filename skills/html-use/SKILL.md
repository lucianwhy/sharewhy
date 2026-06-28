---
name: html-use
description: Use when content should be delivered as a local HTML artifact instead of plain markdown, especially when it needs a collapsible left sidebar navigation and must be saved under the project's html directory
---

# HTML Use

## Overview

把信息整理成可直接打开的 HTML 成品，不停留在 Markdown。

核心原则：
- 产物必须能本地直接打开
- 左侧必须有可收缩导航栏
- 文件统一落到项目目录下的 `html/`

## When to Use

适合：
- 用户明确要 `HTML` 展示
- 输出内容较长，需要导航定位
- 需要交付本地文件，而不是聊天里的临时排版
- 需要给后续 skill 或项目沉淀一个可复用页面

不要用在：
- 用户只要一段短回答
- 用户明确要求 Markdown、纯文本、表格文本
- 只是内部草稿，还不需要 HTML 成品

## Output Location

HTML 文件统一放到当前项目下的：

```text
html/
```

规则：
- 如果 `html/` 不存在，先创建
- 文件名必须和主题切题
- 默认使用 `.html` 后缀

命名示例：
- `payment-architecture-map.html`
- `bug-retro-summary.html`
- `feature-scope-review.html`

## Required Layout

每个 HTML 产物都必须满足：

- 页面含左侧侧边栏
- 侧边栏用于导航锚点跳转
- 侧边栏支持收缩 / 展开
- 主内容区滚动阅读

根结构建议：

```html
<div class="app-shell">
  <aside class="sidebar">...</aside>
  <main class="content">...</main>
</div>
```

## Minimal Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>页面标题</title>
  <style>
    :root {
      --bg: #f7f8fc;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --line: #d9e1ec;
      --accent: #2563eb;
      --sidebar-width: 260px;
      --sidebar-collapsed: 76px;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .app-shell {
      display: grid;
      grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
      min-height: 100vh;
    }

    .app-shell.is-collapsed {
      grid-template-columns: var(--sidebar-collapsed) minmax(0, 1fr);
    }

    .sidebar {
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 20px 14px;
      background: var(--panel);
      border-right: 1px solid var(--line);
      overflow: auto;
    }

    .sidebar-toggle {
      width: 100%;
      margin-bottom: 16px;
    }

    .nav-link {
      display: block;
      padding: 10px 12px;
      color: var(--muted);
      text-decoration: none;
      border-radius: 10px;
    }

    .nav-link:hover,
    .nav-link:focus-visible {
      background: #eef4ff;
      color: var(--accent);
    }

    .content {
      padding: 32px;
    }

    @media (max-width: 900px) {
      .app-shell,
      .app-shell.is-collapsed {
        grid-template-columns: 1fr;
      }

      .sidebar {
        position: relative;
        height: auto;
      }
    }
  </style>
</head>
<body>
  <div class="app-shell" id="appShell">
    <aside class="sidebar">
      <button class="sidebar-toggle" type="button" id="sidebarToggle">收起导航</button>
      <nav>
        <a class="nav-link" href="#section-1">部分 1</a>
        <a class="nav-link" href="#section-2">部分 2</a>
      </nav>
    </aside>
    <main class="content">
      <section id="section-1"><h1>部分 1</h1></section>
      <section id="section-2"><h2>部分 2</h2></section>
    </main>
  </div>
  <script>
    const shell = document.getElementById("appShell");
    const toggle = document.getElementById("sidebarToggle");

    toggle.addEventListener("click", () => {
      const collapsed = shell.classList.toggle("is-collapsed");
      toggle.textContent = collapsed ? "展开导航" : "收起导航";
    });
  </script>
</body>
</html>
```

## Workflow

1. 先确认输出主题
2. 创建项目下的 `html/` 目录
3. 生成主题明确的 HTML 文件名
4. 按“左侧导航 + 右侧内容”结构组织页面
5. 为每个导航项绑定锚点
6. 加入收缩脚本
7. 本地打开检查导航、滚动、收缩是否正常

## Quick Reference

- 导航栏：左侧 `aside`
- 内容区：右侧 `main`
- 导航方式：锚点 `href="#section-id"`
- 收缩状态：给外层容器切 `is-collapsed`
- 输出目录：项目 `html/`

## Common Mistakes

- 只写内容，不做左侧导航
- 有导航栏，但不能收缩
- 把 HTML 丢到别的目录
- 文件名太泛，后续找不到
- 页面只适配桌面，不处理窄屏

## Verification

交付前至少确认：

- `html/` 目录存在
- HTML 文件能直接双击或浏览器打开
- 左侧导航点击可跳转
- 导航栏可收起、可展开
- 窄屏下内容不挤爆
