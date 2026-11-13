# 教师回传审核短表（合成示例）

> **这张表不是脚本输出。** 它是照合并版 `references/teacher-review.md` 的规则，由 Claude 读完两份稿子以后手写的。初稿和教师改稿都是为演示新写的合成文字；“教师”不是真人，也不是哪个真实模型的回传。表里引用的脚本结果都在 [tool-outputs/](tool-outputs/) 里，是真跑出来的，一个字没动。

对照的两份稿：

- 初稿 [draft.md](draft.md)，sha256 `b3cc483cce58…`，章节门里展示并确认的那一版（`demo-10-present-draft`）。
- 教师改稿 [teacher-revision.md](teacher-revision.md)，sha256 `64120d6b0317…`，回传事件 `demo-14-teacher-return`，绑定在上面那一版初稿上。

## 一句话

教师主要想把话说完整、把没交代的地方补上（这是推断：教师没有写理由）。一共动了四处：错别字 1 处，台词口气 1 处，添了事实 1 处，删了台词 1 处。

## 逐处对照

| # | 位置 | 原句 | 教师改句 | 多了什么 | 丢了什么 | 拟处置和依据 | 谁来定 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 初稿第 21 行 | 丁穗把硬币拢进铁盒，**在**把两张票从窗口底下推出去。 | ……**再**把两张票从窗口底下推出去。 | 句子通了：“再”是接着做下一个动作。 | 没有。 | **拟采纳。** 错别字，“在”应为“再”；意思和事实都没变。 | 工坊核过，你只点例外 |
| 2 | 初稿第 11 行，老郝的台词 | “活的算行李，两块。” | “按规定，活禽属于行李，要收两块钱。” | 一个完整的句子；“按规定”这个出处。 | 老郝惜字的口气：这句台词从 7 个字变成 14 个字；口头的“活的”换成了书面的“活禽”；看一眼就报价的随手劲儿。 | **拟拒绝，保留原句。** 写前准备里记的声音是“老郝惜字”。另外“按规定”在台词里带出了一条规矩，而本章范围里写的是价目表上一块，查不到“两块”的规定。读感是工坊的看法，不是结论。 | 你 |
| 3 | 初稿第 17 行 | 老郝把笔帽咬在嘴里，没接话。 | 老郝在这个窗口卖了二十三年票，头一回被新来的当面纠正。他把笔帽咬在嘴里，没接话。 | 两件稿子里原来没有的事：老郝的工龄（二十三年），“头一回被当面纠正”；他为什么不接话有了解释。 | 这一处的留白：原稿只写咬笔帽、不接话，原因留给读的人。 | **拟暂缓（待核）。** 本章范围、章纲和初稿里都查不到老郝在这个窗口干了多少年；演示项目没有设定档，也没有前章。有依据再谈这句留不留，没有依据不进正文。 | 你（等你给依据或裁决） |
| 4 | 初稿第 13 行 | “上回还不要钱呢。” | （整句删去） | 没有。 | 一句顶回去的话。原稿里这句后面紧接着丁穗翻价目表；删掉以后，她翻价目表直接接在老郝报价后面。 | **拟拒绝，保留这句。** 台词的增删工坊不动。教师可能是嫌这句没写是谁说的（推断；分栏里它在“没写明是谁说的”一栏）。要解决这个，补“某某说”三个字就够；是谁说的要你来认，工坊不猜。 | 只有你 |

每处动的是哪一类：1 是纯表达（错别字）；2 拆成两类记，措辞口气是纯表达，“按规定”是台词里添的话（补信息）；3 是补信息；4 是台词的删改。

## 工坊核过的

1 处，拟采纳：第 1 处，“在”改“再”。

## 可改可不改的

0 处。

## 跟着走的一处小改

第 3 处里，教师把后一句的“老郝”换成了“他”，是跟着新加的那句走的。新加的那句不留，这里也不动。

## 待核的、没查的、查不了的

- **待核**：老郝的工龄（第 3 处）。
- **工具没报、靠读看出来的**：`prose_lint.py --hint deai` 在初稿和改稿上都是“没有命中”，`detail_check.py compare` 的“新出现的判断句”也是 0 处。第 3 处新加的那句把留白说破，是读出来的，工具列不出来。
- **标点**：`punctuation_lint.py --baseline` 报 `NO_NEW_FLAGS`，改稿没有新带进来的标点问题。
- **没查**：没有跑 `fact_guard.py`（演示项目没有事实账；教师添的事实只有一条，直接列了待核）；没有用 `--keep`（这个演示没有锁定句）。
- **教师没动、工坊分栏时自己看到的**：初稿第 15 行，丁穗的“然而价目表上写的是一块。”，书面词“然而”进了台词。这不在教师回传里，不算进上面四处，另记在审稿意见里。
- **没做的**：这张表到这里为止，没有人确认过。真实流程里，下一步是把整份方案作为 `review` 阶段的成果交给你确认，你确认以后才动稿子；修订以后要对新稿重新复查。这个演示没有做修订，也没有做复查。

## 引用的脚本结果

| 文件 | 命令（在本目录下运行，`$NW_SCRIPTS` 是包里的 `skills/novel-workshop/scripts`） |
| --- | --- |
| [tool-outputs/changes.txt](tool-outputs/changes.txt) | `python3 -I -B "$NW_SCRIPTS/detail_check.py" changes draft.md teacher-revision.md` |
| [tool-outputs/compare.txt](tool-outputs/compare.txt) | `python3 -I -B "$NW_SCRIPTS/detail_check.py" compare draft.md teacher-revision.md` |
| [tool-outputs/dialogue-lines.draft.txt](tool-outputs/dialogue-lines.draft.txt) | `python3 -I -B "$NW_SCRIPTS/dialogue_lines.py" draft.md --names 老郝,丁穗,冯姐` |
| [tool-outputs/dialogue-lines.teacher.txt](tool-outputs/dialogue-lines.teacher.txt) | `python3 -I -B "$NW_SCRIPTS/dialogue_lines.py" teacher-revision.md --names 老郝,丁穗,冯姐` |
| [tool-outputs/deai.draft.txt](tool-outputs/deai.draft.txt) | `python3 -I -B "$NW_SCRIPTS/prose_lint.py" draft.md --hint deai --format text` |
| [tool-outputs/deai.teacher.txt](tool-outputs/deai.teacher.txt) | `python3 -I -B "$NW_SCRIPTS/prose_lint.py" teacher-revision.md --hint deai --format text` |
| [tool-outputs/punctuation.baseline.txt](tool-outputs/punctuation.baseline.txt) | `python3 -I -B "$NW_SCRIPTS/punctuation_lint.py" teacher-revision.md --baseline draft.md --format text` |

台词字数（7 和 14）取自 `dialogue_lines.py --format json` 里那两句的 `han` 字段。
