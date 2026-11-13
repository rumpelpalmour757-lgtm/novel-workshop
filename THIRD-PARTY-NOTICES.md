# 第三方组件与许可范围

本仓库按 MIT 许可发布，全文见 [LICENSE](LICENSE)，版权人 Celeste。这份文件说明两件事：仓库里早先写下的许可说明现在以哪一份为准；哪些东西是别人的，继续按它们自己的许可。

## 许可范围

- 从 2026-11-13 起，根目录的 `LICENSE` 适用于本仓库里版权人自己的全部内容，包括各个版本的压缩包、便携单文件和单独放的风格卡文件。
- 各压缩包里的 `LICENSE-NOTICES.md`、`SOURCE-NOTES.md`，单文件末尾的来源记录，以及旧风格卡文件里的 `SOURCE-NOTICE.md`，都写在这个日期以前。里面“整体尚未指定许可”“不将整包统一声明为 MIT”“使用条件还没有确认”这类话说的是当时的情况，现在以根目录 `LICENSE` 和本文件为准。这些文件留在包里没有改，下一个版本的包会更新。
- 版权人在 2026-11-13 确认：83 张风格卡、两套风格包、分场模块和节拍卡里照录的规范文字、`prose_lint.py` 里照录的词表，以及依据课程和教程材料改写的方法，由版权人本人所写或有权公开，按 MIT 一并发布。
- 下面列出的第三方组件不算进版权人的版权声明，各按自己的许可，版权归各自的权利人。

## 包里带的第三方组件

三样都是 MIT 许可。它们的版权行和许可全文原样留在包里；再分发这些文件时，请把对应的版权行和许可声明一起带上。下表的路径相对于完整包解压后的根目录。

| 组件 | 版权行 | 包里的哪些文件 | 包内的许可文件 |
|:-----|:-------|:---------------|:---------------|
| [Oh Story](https://github.com/zenstory-ai/oh-story-claudecode) | Copyright (c) 2025-2026 oh-story-claudecode | **取自上游**：`skills/novel-workshop/scripts/oh-story/` 下的 `inspect_existing_assets.py`、`render_relation_chart.py`、`build_chapter_index.py`（只加了一行导入路径）。**在上游文件上改编**：同目录的 `dashboard-server.mjs`，以及 `skills/novel-workshop/assets/dashboard/` 的 `index.html`、`app.js`、`styles.css`、`tokens.css`。**参考后重写**：11 篇方法参考，各篇末尾记了参照的上游文件 | `skills/novel-workshop/assets/third-party/oh-story-LICENSE.txt`、`oh-story-0.8.4-LICENSE.txt`；便携单文件里也附了全文 |
| [darwin-skill](https://github.com/alchaincyf/darwin-skill) | Copyright (c) 2026 alchaincyf (花叔) | `skills/darwin-novel-workshop/`：用了它候选迭代和配对比较的思路，目录里的文件是面向小说工坊重写的 | `skills/darwin-novel-workshop/LICENSE` |
| TypeSafe AI | Copyright (c) 2026 TypeSafe AI | `optional/typesafe-ai/SKILL.md`：可选的开发技能，正文保持原样，默认不安装 | `optional/typesafe-ai/LICENSE` |

`tokens.css` 文件头里的 ZenStory 是上游文件自带的说明，本项目不使用这个名字和它的标记。

`skills/novel-workshop/scripts/oh-story/` 目录里其余的文件（启动器、`workbench.mjs`、`gemini-*.mjs`、`acp-*.mjs`）是本项目自己写的，按根目录的 `LICENSE`。

这三样组件的许可声明原文如下，分别配上表里各自的版权行：

```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 不在仓库里、要使用者自己安装的外部项目

可选的找图链路会调用下面这些项目。包里只有调用它们的适配器（本项目自己写的），没有它们的代码、模型权重或浏览器。它们各有各的许可，下面的许可名称照包内记录填写，以各项目自己的说明为准。

| 项目 | 许可 |
|:-----|:-----|
| SearXNG | AGPL-3.0 |
| Crawl4AI | Apache-2.0 |
| ImageHash | BSD-2-Clause |
| OpenCLIP | MIT；模型权重的许可看所选模型的模型卡 |
| Openverse | 调它的公开接口；返回的每张图按它来源页的授权 |

## 名字和引用

- 风格卡的卡名和说明里提到的作家、作品和品牌，只用来描述腔调。MIT 许可不涉及这些名字和作品本身的任何权利；卡里当作反例引用的口头禅、书名和流行语也一样。
- 本地工作台的界面布局参考过 InkOS（AGPL-3.0）的写作台思路；按包内记录，没有使用它的代码、标志或图片。
- AI 平台、模型和外部服务不随本仓库提供，它们的账户、费用和使用条款由各自的提供方决定。
