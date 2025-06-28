## mkdocs

```shell
mkdocs build --clean
mkdocs build
mkdocs serve
mkdocs gh-deploy --force
git add .
git reset site/
git commit -m "Update main branch (excluding site/)"
git push -f origin main
```


| **HTMLタグ**                         | **用途**           | **使用されるCSS変数**                                         | **ライトモードの色**                          | **ダークモードの色**                          |
| ---------------------------------- | ---------------- | ------------------------------------------------------ | ------------------------------------- | ------------------------------------- |
| `h1`～`h6`                          | 見出し              | `--md-typeset-color` → `--md-default-fg-color`         | `hsla(0, 0%, 0%, 0.87)`               | `hsla(var(--md-hue), 15%, 90%, 0.82)` |
| `p`                                | 段落               | `--md-typeset-color` → `--md-default-fg-color`         | 同上                                    | 同上                                    |
| `a`                                | リンク              | `--md-typeset-a-color` → `--md-primary-fg-color`       | デフォルト：indigo系                         | テーマ指定により可変（例：teal, pinkなど）            |
| `code`（インライン）                      | コード文字色           | `--md-code-fg-color`                                   | `hsla(200, 18%, 26%, 1)`              | `hsla(var(--md-hue), 18%, 86%, 0.82)` |
| `pre` / `code`（ブロック）               | 背景色              | `--md-code-bg-color`                                   | `hsla(200, 0%, 96%, 1)`               | `hsla(var(--md-hue), 15%, 18%, 1)`    |
| `kbd`                              | キー表示（`Ctrl+C`など） | `--md-typeset-kbd-color` など                            | `hsla(0, 0%, 98%, 1)`                 | `hsla(var(--md-hue), 15%, 90%, 0.12)` |
| `mark`                             | テキストハイライト        | `--md-typeset-mark-color`                              | 黄色系（半透明）                              | 青系（半透明）                               |
| `table`, `th`, `td`                | 表の罫線など           | `--md-typeset-table-color`                             | `hsla(0, 0%, 0%, 0.12)`               | `hsla(var(--md-hue), 15%, 95%, 0.12)` |
| `footer`                           | フッター背景・文字色       | `--md-footer-bg-color`, `--md-footer-fg-color`         | 背景：黒、文字：白                             | 背景：ダークグレー、文字：白                        |
| `blockquote`                       | 引用ブロック           | `--md-typeset-color` + border                          | `--md-default-fg-color`（黒） + 薄いグレー境界線 | 明るいグレー文字 + 薄い明るい枠線                    |
| `ul`, `ol`, `li`                   | 箇条書き・リスト         | `--md-typeset-color`                                   | `--md-default-fg-color`               | 同上                                    |
| `details`, `summary`               | 折りたたみ要素          | 通常：`--md-typeset-color`／展開時：`--md-primary-fg-color`    | 黒＋強調時にテーマ色（例：青）                       | 明るいグレー＋強調時に同上                         |
| `.admonition`, `::after`           | 補足・警告ボックス        | `--md-admonition-bg-color`, `--md-admonition-fg-color` | 白背景 + 黒文字                             | ダーク背景 + 明るい文字                         |
| `.md-typeset .warning`, `.note` など | 色付きAdmonition    | 色別に強制指定（例：黄、青、緑）                                       | `--md-warning-bg-color` 等             | 同じ変数名でダーク向け指定あり（ただし暗く調整）              |
