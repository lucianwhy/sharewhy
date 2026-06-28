---
name: html-use
description: Use when content should be delivered as a local HTML artifact instead of plain markdown, especially when it needs a collapsible left sidebar navigation, calm reading-oriented styling, and must be saved under the project's html directory
---

# HTML Use

## Overview

把内容做成可直接打开的 HTML 成品，不停留在聊天排版。

核心原则：
- 文件必须落到项目 `html/`
- 页面必须有左侧可收缩导航
- 样式要偏“安静、清晰、可长时间阅读”
- 视觉重点服务信息结构，不做花哨装饰

## When to Use

适合：
- 用户明确要 `HTML` 展示
- 内容较长，需要导航定位
- 需要交付本地文件而不是聊天临时文本
- 需要把说明、总结、方案、复盘做成可复用页面

不要用在：
- 用户只要短回答
- 用户明确要求 Markdown / 纯文本
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
<div class="app-shell" id="appShell">
  <aside class="sidebar">...</aside>
  <main class="content">...</main>
</div>
```

## Visual Direction

默认风格不是“产品后台蓝白卡片”，而是“阅读型技术说明页”：

- 背景：暖白 / 米白
- 标题：衬线字体，拉开层级
- 正文：无衬线字体，保证长文易读
- 路径 / 文件 / 代码：等宽字体
- 强调色：陶土 / 橄榄 / 深灰，少量使用
- 卡片与边框：轻，不要厚重投影堆叠

目标感觉：
- 像高质量技术备忘录
- 像架构 walkthrough
- 不像营销页
- 不像花哨仪表盘

## Recommended Information Blocks

长内容优先拆成这些块，而不是一整页散文：

- `header / summary`
- `diagram / flow`
- `step walkthrough`
- `key files`
- `gotchas / red flags`
- `acceptance / next step`

如果内容是总结类、方案类、复盘类，这套块结构优先于随意排版。

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
      --ivory: #faf9f5;
      --slate: #141413;
      --clay: #d97757;
      --oat: #e3dacc;
      --olive: #788c5d;
      --gray-150: #f0eee6;
      --gray-300: #d1cfc5;
      --gray-500: #87867f;
      --gray-700: #3d3d3a;
      --serif: ui-serif, Georgia, "Times New Roman", serif;
      --sans: system-ui, -apple-system, "Segoe UI", sans-serif;
      --mono: ui-monospace, "SF Mono", Menlo, Monaco, monospace;
      --sidebar-width: 280px;
      --sidebar-collapsed: 84px;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      background: var(--ivory);
      color: var(--gray-700);
      font-family: var(--sans);
    }

    .app-shell {
      display: grid;
      grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
      min-height: 100vh;
      transition: grid-template-columns 0.2s ease;
    }

    .app-shell.is-collapsed {
      grid-template-columns: var(--sidebar-collapsed) minmax(0, 1fr);
    }

    .sidebar {
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 18px 14px;
      background: rgba(250, 249, 245, 0.94);
      border-right: 1px solid var(--gray-300);
      overflow: auto;
    }

    .sidebar-toggle {
      width: 100%;
      margin-bottom: 14px;
      border: 1px solid var(--gray-300);
      background: #fff;
      color: var(--slate);
      border-radius: 12px;
      padding: 10px 12px;
      cursor: pointer;
    }

    .nav-link {
      display: block;
      padding: 10px 12px;
      color: var(--gray-500);
      text-decoration: none;
      border-radius: 10px;
    }

    .nav-link:hover,
    .nav-link:focus-visible {
      color: var(--clay);
      background: rgba(217, 119, 87, 0.08);
      outline: none;
    }

    .content {
      padding: 40px 28px 72px;
      max-width: 1080px;
      width: 100%;
    }

    h1, h2, h3 {
      color: var(--slate);
      font-family: var(--serif);
      font-weight: 500;
      letter-spacing: -0.02em;
    }

    .eyebrow,
    .meta,
    code,
    pre {
      font-family: var(--mono);
    }

    .panel {
      background: #fff;
      border: 1.5px solid var(--gray-300);
      border-radius: 14px;
      padding: 18px 20px;
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
      <section id="section-1" class="panel">
        <div class="eyebrow">Summary</div>
        <h1>部分 1</h1>
      </section>
      <section id="section-2" class="panel">
        <h2>部分 2</h2>
      </section>
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

1. 确认输出主题
2. 创建项目下 `html/`
3. 起一个主题明确的文件名
4. 先搭“左侧导航 + 右侧主内容”骨架
5. 再填 `summary / steps / files / risks` 等信息块
6. 加入导航收缩脚本
7. 本地检查导航、滚动、收缩、窄屏阅读

## Quick Reference

- 导航栏：左侧 `aside`
- 内容区：右侧 `main`
- 导航方式：锚点 `href="#section-id"`
- 收缩状态：给外层容器切 `is-collapsed`
- 标题：优先 serif
- 正文：优先 sans
- 路径 / 代码：优先 mono
- 输出目录：项目 `html/`

## Common Mistakes

- 只把 Markdown 搬进 HTML，不重做信息层次
- 用蓝白后台卡片味太重，阅读感太差
- 有导航栏，但不能收缩
- 把 HTML 丢到别的目录
- 文件名太泛，后续找不到
- 页面只适配桌面，不处理窄屏
- 视觉太花，盖过内容本身

## Verification

交付前至少确认：

- `html/` 目录存在
- HTML 文件能直接双击或浏览器打开
- 左侧导航点击可跳转
- 导航栏可收起、可展开
- 窄屏下内容不挤爆
- 标题 / 正文 / 代码层次清楚
- 页面整体更像“阅读型技术说明页”，不是营销页
