# sharewhy skills

这个仓库现在承载 3 个 skill：

- `pre-code`
- `after-code`
- `html-use`

## 触发规则

- `pre-code` 和 `after-code` 是显式触发 skill
- `html-use` 是通用展示 skill，用于把内容整理成 HTML 产物

## 仓库结构

```text
skills/
  pre-code/
    SKILL.md
    preview.html
  after-code/
    SKILL.md
    preview.html
  html-use/
    SKILL.md
```

## 输出约定

- `pre-code` -> `html/precode/`
- `after-code` -> `html/aftercode/`
- `html-use` -> `html/`

如果目录不存在，skill 需要先创建。

HTML 文件命名必须和主题切题，让人一眼看出内容用途，例如：

- `payment-status-sync-precheck.html`
- `payment-status-sync-retro.html`
- `weekly-review-dashboard.html`

## Skills

- [`pre-code`](./skills/pre-code/SKILL.md)
- [`after-code`](./skills/after-code/SKILL.md)
- [`html-use`](./skills/html-use/SKILL.md)

## Previews

- [`pre-code preview`](./skills/pre-code/preview.html)
- [`after-code preview`](./skills/after-code/preview.html)

## Existing Files

仓库根目录保留原有网页/媒体文件，不影响 skill 目录结构。
