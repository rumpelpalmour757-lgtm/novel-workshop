# 四个可选模块

[← 返回首页](../README.md) · 适用版本 `2026-11-14-r5.55`

r5.54-merged 起多带四个模块：章节门、学习循环、示范记忆、对白声纹与反模式检查。**四个都默认不开**，你说了才用；不开，工坊照原来的办法写和改。r5.55 另加了一页默认不开的“从改稿记录里学编辑判断”（`references/editorial-judgment.md`），只有说明页和模板，没有脚本，不算在这四个里，见首页的[模块](../README.md#模块)表。

它们是记录和核对用的：把你的确认、别人的意见、实际改了什么、新稿查没查，一条一条对上号。它们不写小说，不调用模型，也认证不了一句话是不是你说的。

这一页写的是让 AI 和脚本照着做的方法，不是效果保证。工坊只和不用工坊的 AI 比过一次（r5.46，规模小，执行和评审都是同一类模型）：改 AI 腔重的稿子，排第一的都是不用工坊的；从头起草，工坊多数在前。之后没有再比过。对白是不是更像人、更有感情，没有验证；好不好由你读了定。

本页提到的 `references/…`、`assets/…`、`scripts/…` 都在完整包的 `skills/novel-workshop/` 下。便携单文件里有这四个模块的说明和两个模板，没有脚本。

- [一览](#一览)
- [章节门](#章节门)
- [学习循环](#学习循环)
- [示范记忆](#示范记忆)
- [对白声纹与反模式检查](#对白声纹与反模式检查)
- [只能聊天时](#只能聊天时)
- [本页的命令是怎么核的](#本页的命令是怎么核的)

## 一览

| 模块 | 管什么 | 默认 |
| --- | --- | --- |
| 章节门 | 写新的一章分七个阶段交成果，每一步等你确认；开了以后写前看图、初稿由你交教师两项默认开着；登记你带回来的教师意见或改稿 | 不开 |
| 学习循环 | 一轮改稿里的意见、每条怎么取舍、实际改动、新稿复查，连成一条记录 | 不开 |
| 示范记忆 | 存下认可过的“改前、改后、为什么”，下次相似任务最多取三条参考 | 不开 |
| 对白声纹与反模式检查 | 按本书登记的人物扫对白，角色一栏只给数字；文风提示要另开，命中只标“复核”；要候选改句时先校验、再写进新文件 | 不开，你要求时才跑 |

脚本入口和包里的说明各在哪里：

- 章节门：`scripts/chapter_gate.py`（读进度）和 `scripts/learning_loop.py apply`（写入）；说明在 `references/chapter-confirmation.md` 和 `references/teacher-review.md`。
- 学习循环：`scripts/learning_loop.py`；说明在 `references/learning-loop.md`。
- 示范记忆：`scripts/demonstration_memory.py`（只读）；说明在 `references/demonstration-learning.md`。
- 对白声纹与反模式检查：`scripts/dialogue_lint/run_lint.py`；说明在 `references/dialogue-lint.md`。

四个怎么搭：章节门管“这一章走到哪一步、你确认了没有”。教师（你选来改稿的人，或另一个 AI）的意见回来以后，学习循环记“每条意见怎么取舍、改了什么、新稿查了没有”。这一轮里值得留的对照登记成示范，下次由示范记忆取出来。对白检查是单独的一项扫描，哪一步想用都行。章节门不看学习循环的开关，可以单开。

平时对 AI 说话就行，不用记命令。每个模块下面的“最短步骤”，是给想自己动手核一遍、或者想知道 AI 在背后记了什么的人看的。命令都在 `skills/novel-workshop` 目录下运行，路径换成你自己的。

## 章节门

**是什么。** 开启以后，写新的一章分七步交成果：材料与目标（`scope`）→ 章节方案（`outline`）→ 写前准备（`preparation`）→ 初稿（`draft`）→ 审稿与修订计划（`review`）→ 修订稿（`revision`）→ 定稿记录（`final`）。把一章重写出新的一版、接着写一章只写了一半的稿子算不算，它先问你一句，不默认走。每一步交出来就停下等你，不能跳步。你回“继续”只放行正在等的那一步；“你决定”只授权这一阶段里可撤回的选择，不算确认。最后一步要你对当前这一版明确说采纳，比如“定稿。”“采纳当前稿。”。初稿、修订稿和定稿交出来时都绑定稿件的 SHA-256：审稿对着已确认的初稿，定稿对着已确认的修订稿。你改了方案或正文，可以重开某一步，这一步和它后面的旧确认全部作废，历史留着。

开了以后还有两项策略：**写前必须看图，初稿由你自己交给教师**。你和作品档案都没另说的，两项都按开着办（r5.55 起；r5.54-merged 是默认关着）。写前准备要带看图记录；初稿确认后工坊停下，等你把教师的意见或改稿带回来，工坊不自己扮教师；回传登记时绑定这一版初稿的展示实例（哪一次交出来的）、版本和哈希，绑错的拒收；初稿换了版，旧回传留在记录里，不能套到新稿上。登记回传不算任何一步的确认，也不算你采纳了教师的改法。

教师结果回来以后工坊怎样对照、怎样给你短表，见[详细用法](usage.md#别人改过的稿子怎么审)。

**什么时候用。** 你想每一步都自己把关的新章；你有固定的教师改稿，想让每份回传对得上它改的是哪一版。只做分析、逐字保真排版、改几处标点、在已有稿子上精修这类任务不走七步，开了也不扩大成全流程。

**默认开不开，怎么开。** 不开。分两层：

1. 逐阶段确认：对 AI 说一句，比如“以后每写新的一章都走完整流程，一步一步给我看，我确认了再往下”。它记在你自己的档案里（包里叫“作者档案”，是你的私有记录，包里不带）；只管这本书的，记在作品档案里。
2. 看图和教师交接：开了第 1 层以后，这两项默认开着（r5.55 起）。不要的另说一句。整本书都不要的，比如“这本书写前不用看图”，有脚本的环境里记成一条 `configure` 事件，带你的原话和出处，只对之后才开始的章节生效，已经开始的章节保持它开始时的做法；只这一章不要的，当章说，记成一条 `chapter_policy` 事件，只管这一章（这一章还没开始也能先记）。两项可以只关一样。

这一章实际按什么走，看 `chapter_gate.py status` 里的 `workflow_policy`：`basis` 是 `default`（项目里没有任何策略记录，两项都开）、`project`（整本书的 `configure`）、`chapter`（你对这一章说的）或 `earlier_version`（在 r5.54-merged 下开始、当时没记策略的章，照两项都关走，工坊见到会问你一句）。

第 1 层没开时，装上这个包不会生成任何章节确认记录。想关，说一声。

**聊天里能不能用。** 能，人工记，见[只能聊天时](#只能聊天时)。

**最短步骤。** 读进度用 `chapter_gate.py status`（它只有这一个子命令，只读）；写入走 `learning_loop.py apply`，一次交一个事件文件。

第 0 步，准备一份记录。已有项目 JSON 状态文件的沿用原文件；没有的，在项目里放一份带固定标记的 Markdown 学习记录，最小的样子是这样（标记块外面可以写别的字，写入时原样保留）：

````text
<!-- NOVEL_WORKSHOP_LEARNING_START -->
```json
{"schema_version":1,"project_id":"demo-bike-stall","revision":0,"data":{}}
```
<!-- NOVEL_WORKSHOP_LEARNING_END -->
````

第 1 步，读这份记录现在的版本：

```bash
python3 scripts/learning_loop.py status 项目/learning-record.md
```

返回里的 `"version": "sha256:…"` 是整份记录的版本。每次写入都要带上最新的这个值；记录被别人改过，写入就被拒绝。

第 2 步，交出第一步的成果。事件文件 `events/01-present-scope.json`：

```json
{
  "event_id": "ch01-01-present-scope",
  "op": "chapter_gate",
  "action": "present",
  "chapter_id": "ch01",
  "stage": "scope",
  "content": "【合成演示】本章范围：一场，巷口修车摊，傍晚收摊前。人物：老秦（修车的，话少）、阿梨（来补胎的学生）。篇幅：两百字以内。不改的事实：补两处三块。材料缺口：没有前章，没有口吻表。",
  "source_ref": "合成演示：为这一页新写的本章范围"
}
```

```bash
python3 scripts/learning_loop.py apply 项目/learning-record.md 项目/events/01-present-scope.json \
    --project-id demo-bike-stall --if-version '第 1 步返回的 version'
```

返回（节选）：

```text
  "status": "saved",
  "chapter_status": "awaiting_confirmation",
  "current_stage": "scope",
  "presentation_id": "ch01-01-present-scope",
  "presentation_version": "cff9d4e8dc0c403584e1c3f2bd966646fcb218c17776ee75bb3f4b67304c32c4",
  "next_action": "confirm",
  "workflow_policy": {
    "visual_required": true,
    "teacher_handoff": "user_return",
    "basis": "default",
    "frozen": true
  },
  "version": "sha256:a9f7c6db848b150114fffa98687268518a256beb1d3f1daa035349642e488467",
```

这份记录里没有任何策略事件，所以 `basis` 是 `default`：这一章在第一次展示时，就按看图和教师交接两项都开定了下来。

第 3 步，随时读进度：

```bash
python3 scripts/chapter_gate.py status 项目/learning-record.md --chapter-id ch01
```

这时它报 `"status": "awaiting_confirmation"`、`"current_stage": "scope"`，就是停在第一步等你。

第 4 步，记下你的确认。事件里写明确认的是哪一次展示（上面返回的 `presentation_id` 和 `presentation_version`）、你的原话和出处：

```json
{
  "event_id": "ch01-02-confirm-scope",
  "op": "chapter_gate",
  "action": "confirm",
  "chapter_id": "ch01",
  "stage": "scope",
  "presentation_id": "ch01-01-present-scope",
  "presentation_version": "cff9d4e8dc0c403584e1c3f2bd966646fcb218c17776ee75bb3f4b67304c32c4",
  "actor_role": "author",
  "mode": "human",
  "author_quote": "（合成演示）继续。",
  "source_ref": "合成演示：这句不是真人作者说的，只用来让脚本走到下一步"
}
```

用同样的 `apply` 命令交上去（`--if-version` 换成第 2 步返回的值），返回（节选）：

```text
  "status": "saved",
  "chapter_status": "awaiting_presentation",
  "current_stage": "outline",
  "next_action": "present",
```

**“继续”只放行了材料与目标这一步**——下一步章节方案还没交。往后每一步都是这两条：`present` 交成果，`confirm` 记确认。初稿、修订稿、定稿的 `present` 多一个 `artifact_sha256`（稿件文件的 SHA-256）；这一章看图开着，写前准备的 `present` 要带 `visual_evidence`；初稿由你交教师，审稿的 `present` 要带 `teacher_return_id`。最后一步的 `confirm` 多一个 `"decision": "accept_final_version"`，你的原话整句要是对当前稿的明确采纳。教师回传用 `"action": "teacher_return"` 登记，只管一章的策略用 `"action": "chapter_policy"`，字段见 `references/chapter-confirmation.md`。

同一份合成材料上接着一路走到了最终采纳，中间试了这些，结果照录（这一章没记策略，看图和教师交接都是默认开着的）：

| 做了什么 | 脚本怎么答 |
| --- | --- |
| 章节方案还没交，直接交初稿 | 拒绝：`Only the current stage may be presented or confirmed` |
| 拿旧的 `version` 来写 | 拒绝，退出码 3：`Store changed since your read; no write performed` |
| 同一个事件原样再交一次 | `"status": "unchanged"`，不重复记 |
| 写前准备不带看图记录 | 拒绝：`This chapter follows visual_required:true: preparation must carry visual_evidence for images actually looked at …`；报错里写着另一条路：你说了这一章不看图的，先用 `chapter_policy` 记你的原话 |
| 初稿确认以后读进度 | `"status": "await_teacher_return"` |
| 回传还没登记，就交审稿 | 拒绝：`Review must name a teacher_return_id bound to the current confirmed draft. …`，后面同样写着 `chapter_policy` 这条路 |
| 回传绑的不是这一版初稿的哈希 | 拒绝：`Teacher return must bind this chapter's current confirmed draft instance, version and hash` |
| 重开初稿、换了一版，再拿旧回传来审 | 拒绝，报错同“回传还没登记”那一行；旧回传仍在记录里，但不在有效回传之列 |
| 定稿绑的不是已确认的修订稿 | 拒绝：`Final must bind the confirmed revision artifact; reopen revision to change it` |
| 最后一步说“继续”“先不采纳，我再看看”“就这版吧”“下午再定稿”，或者话对了却没带 `decision` | 都留在等待：`Final stays pending. It needs decision:accept_final_version and author words that are, as a whole, a plain acceptance of the current version. …`，报错末尾说别替作者改写原话，问一句，回“定稿。”或“采纳当前稿。”就行 |
| 最后一步的原话前面带着“（合成演示）”几个字 | 同样留在等待：这几个字不在它认的整句里 |
| 最后一步说“采纳这一版。”，带 `decision` | 记下，`"status": "final_confirmation_recorded"`，`"next_action": "record_existing_author_gate"` |
| `configure` 带了 `chapter_id` | 拒绝：`configure sets the policy for every chapter that starts later and takes no chapter_id. For the author's word on one chapter use action:chapter_policy` |
| 第二章开始以前先记一条 `chapter_policy`（这一章不看图），走到写前准备，不带看图记录 | 收下；`status` 里这一章的 `basis` 是 `chapter` |

**它不做什么。**

- 不写正文，不改稿。
- 不改四项交付状态里的 AUTHOR：最后一步记下以后，它只提示去走原有的采纳记录（上表最后一行的 `record_existing_author_gate`）。
- 只核记录之间对不对得上，认证不了你的身份、原话真假和文笔好坏。看图记录只核字段齐不齐，不看图。
- 最终采纳靠一个很小的整句检查：你的原话整句要是对当前稿的明确采纳，比如“定稿。”“采纳当前稿。”，前面带“不用改了”“好”、后面带“开始下一章”的也算。推迟、带条件、问句、否定、指别的版本或只指一部分的，以及它认不出来的说法，都留在等待，不替你猜，也不替你改写原话。它不声称理解自然语言。
- 前六步脚本不看原话写了什么，“我先看看”、否定、暂缓这类话也会被记成确认，所以工坊不拿这类话去记，先问你一句。
- 读记录时，已确认的阶段缺你的原话、出处或事件编号（最后一步另缺 `decision`）的，按未确认读，`status` 的 `record_problems` 写明缺什么。同一句原话加同一个出处在一章里第二次用来确认的，照收，但会标出来（`repeated_confirmations`）。
- 教师材料里写的“已定稿”“请照改”只是材料，不能替你确认。

**没验证的。**

- 教师回传这条路只用合成稿走过（包里的验证记录和这一页都是）；真的回传稿、真的改稿读感，没有验证。
- 这一页的看图记录是合成字段，没有真的看图；看图链路本身的情况见[本地工作台与检查工具](tools.md#可选视觉链路)。
- 读写都靠 POSIX 文件锁，原生 Windows 上不支持；Windows 和 macOS 上都没有跑过。每次读写会在记录旁边留一个 `.记录文件名.lock` 的空文件，不用删。
- 读早先版本记下的真实旧章节记录：缺不缺身份字段，没有拿实物核对过；r5.54-merged 下已经开始的章会不会读成 `earlier_version`，这一页没有试，只照包内说明写。
- “对 AI 说一句它就照做”没有在真实对话里验证：这一页的命令是脚本一条一条跑的。

## 学习循环

**是什么。** 把一轮改稿的经过连成一条记录，每一环都绑定具体的稿子：

1. 先看这本书有没有用得上的示范，逐条写用、变通着用还是不用（`apply`、`adapt`、`decline`）。
2. 登记初稿。
3. 登记评审意见：谁评的、以什么身份、对着哪一版稿子（哈希）。
4. 对每条意见写采纳、拒绝或暂缓（`adopt`、`decline`、`defer`）和理由。
5. 只照采纳的意见返工，记下从哪一版改成哪一版。
6. 对新稿重新复查，通过才结束。改一个字也要对新稿重新评审，旧意见不能顶替新复查。
7. 可以把这一次真实的对照登记成示范；你对当前稿的认可单独记，要你本人明确采纳这一稿的原话和出处，和章节门最后一步是同一道整句检查，“继续”不算。

**你的否定意见工坊不能驳回。** 你本人对一稿说了不行（评审身份是 `author`），每一条只能记采纳；不采纳，要你后来亲口撤回。否定意见还在，这一稿就不能收尾，也不能记你的采纳。你否定过的稿子改出来的新稿，你没看过以前，教师的通过照样能收尾，但这一轮记成 `author_objection_open`，登记出来的示范只是候选。

保存是条件保存：记录被别处改过就拒写；同一事件重发不会记两次。记录放在项目已有的状态文件里，或者项目内那份带标记的 Markdown 学习记录里，不另建第二份故事资料。

**什么时候用。** 你把教师的意见带回来，想留下“哪条采纳了、哪条没采纳、为什么”；同一类毛病反复改，想让下一次有据可查。只改几句、不打算留记录的，用不着。

**默认开不开，怎么开。** 不开。要两个开关都开着才生效：这本书的示范记录开关（记录里的 `demonstration_learning.enabled`）和循环开关（`loop_enabled`）；还差哪一个，`status` 的 `missing_switches` 会写出来。用 `configure` 事件打开 `enabled` 要带你的原话和出处。对 AI 说“这本书开学习循环：教师的意见、我的取舍、实际改了什么、新稿复查都记下来”。有脚本的环境里，建记录时照 `references/learning-loop.md` 的模板写上 `"demonstration_learning":{"enabled":true,…}`，循环开关用一条事件开：

```json
{"event_id": "loop-02-configure", "op": "configure", "loop_enabled": true, "max_revisions": 3}
```

返工上限没配时脚本按 2 轮算，可以设 1 到 5；工坊说明里的默认是三轮，作品档案没定轮数的，起一轮以前先配成 `"max_revisions": 3`，上面这条就是这样配的。把 `loop_enabled` 设回 `false` 立刻停用，回到原来的写作流程，历史留着。

**聊天里能不能用。** 没有脚本；照这一篇人工保存同样的内容，见[只能聊天时](#只能聊天时)。

**最短步骤。** 先读状态，再看有没有示范，然后一个事件一个事件地交：

```bash
python3 scripts/learning_loop.py status 项目/learning-record.md
python3 scripts/learning_loop.py context 项目/learning-record.md --project-id demo-bike-stall \
    --task dialogue_revision --exclude-group ch01-修车摊
python3 scripts/learning_loop.py apply 项目/learning-record.md 项目/events/03-start.json \
    --project-id demo-bike-stall --if-version 'status 返回的 version'
```

合成材料上走完的一轮（初稿六句台词，合成的教师意见两条），每个事件交上去以后脚本返回的下一步：

| 顺序 | 事件（`op`） | 记下什么 | 返回的 `next_action` |
| --- | --- | --- | --- |
| 1 | `start` | 任务、标签、场景组、原稿全文和出处、不能动的要求 | `plan` |
| 2 | `plan` | 每条示范用不用（这次一条也没有，是空表）、本轮要查的项 | `draft` |
| 3 | `draft` | 初稿全文、出处、谁写的 | `review` |
| 4 | `review` | 教师的两条意见，绑定初稿的哈希，结论 `revise` | `decide` |
| 5 | `decide` | 第一条采纳，第二条拒绝，各写理由 | `revise_or_stop` |
| 6 | `revise` | 新稿全文、从哪一版改来、对应哪次评审 | `review` |
| 7 | `review` | 对新稿的复查，写明覆盖第 4 步那次评审，结论 `pass` | `finish` |
| 8 | `finish` | 这一轮结束在哪一版 | `learn` |

第 5 步的事件文件长这样：

```json
{
  "event_id": "loop-09-decide",
  "op": "decide",
  "run_id": "run-ch01-dialogue",
  "review_id": "r1-teacher",
  "decisions": [
    {"finding_id": "f1", "decision": "adopt",
     "reason": "问题成立：“我注意到”是书面说法。改法不照抄，换成她会说的话，信息不增不减。"},
    {"finding_id": "f2", "decision": "decline",
     "reason": "老秦话少是这一场定下的口气；补原因会带出初稿里没有的判断。"}
  ]
}
```

第 4 步的教师意见是你带回来的（评审方式记 `author_return`）；第 7 步的复查是工坊自查，所以这一轮记成“自查完成”（`"completion": "self_checked"`），**不记成教师已审**：教师只看过初稿。整轮的记录用 `python3 scripts/learning_loop.py show 项目/learning-record.md --run-id run-ch01-dialogue --brief` 读出来（不加 `--brief` 会打印每一版稿子的全文）。

同一轮里还实际试过这些：

| 做了什么 | 脚本怎么答 |
| --- | --- |
| 循环开关没开就 `start` | 拒绝：`Learning loop is disabled (data.demonstration_learning.loop_enabled is false); continue the original workflow` |
| 评审绑的不是当前稿的哈希 | 拒绝：`Review must bind the current draft` |
| 意见还没取舍就交改稿 | 拒绝：`Revision requires at least one explicitly adopted finding` |
| 新稿还没复查就 `finish` | 拒绝：`Current draft needs a passing review and all required rechecks` |
| 自查记录想挂教师的身份 | 拒绝：`self_check can only have writer role` |
| 你的采纳写成“（合成演示）这一处改法我认，记下来。”或者“继续。” | 都拒绝：`Author acceptance needs the author's unqualified, explicit acceptance of this text; …` |
| 另起一轮，你（合成的）对初稿说了不行，工坊想把这一条记成不采纳 | 拒绝：`The author's own objection can only be adopted, or taken back in the author's later words: …` |
| 那条否定意见还在，就记你的采纳 | 拒绝：`The author's objection to this text is still open (r1-author): …` |
| 停用以后再开新一轮 | 拒绝，报错同第一行；已有的记录读得出来 |

**它不做什么。**

- 不调用模型，不写小说，不训练参数。写稿和评审由你用的 AI 来做，脚本只管记录和版本。
- 认证不了意见的来源、评审人是谁、评审是不是独立，也判断不了文笔。`actor_role`、`mode` 和原话都是宿主照实填的声明，脚本只查填没填、措辞是不是明确采纳。同一个对话里的复查只算自查。
- 只收了意见没改稿，或者只存了示范，不算走完一轮。
- 不新增外发服务和费用：教师的意见由你贴进来，或走你已经配置好的接口。
- 不替代交付门：四项交付状态和 AUTHOR 仍走原来的记录。

**没验证的。**

- 写作质量有没有因此改善，包里写明要另做同题对照，功能测试推不出来；这样的对照没有做过。
- 真实的教师意见没有走过，只有合成的。
- 读写都要 POSIX 文件锁，原生 Windows 不支持；包里的说明让这种环境改用宿主的受保护保存，或者交一份待应用的补丁。Windows 和 macOS 上没有跑过。

## 示范记忆

**是什么。** 把真实的一次“改前、改后、为什么这样取舍、什么时候适用、什么时候不适用”存成示范。下次做相似任务，在同一本书里按任务和标签取最多三条给 AI 参考：先取你认可的，再取教师认可的。

- **教师认可和你的认可分开记。** 教师认可（`teacher_approved`）要有教师的实际判断和出处，不代表你接受。你的认可（`author_accepted`）必须有你本人明确采纳这一稿的原话和出处；你没说话、接着写下一章、回一句“继续”，都不算。
- 候选的、被拒的、停用的不取；留作评测的案例，连同它所在的整组都不取。
- 允许“原文不用改”的示范，不为了有示范硬改。
- 取出来的示范只当情境参考：里面的人物、情节不搬到新稿，合不合这一场要重新判断。

**什么时候用。** 你对某一类改法有稳定的偏好，想让它在这本书里一直管用；教师的某处改法你觉得好，想留着下次参考。没有真正相关的示范时不凑数，照常写。

**默认开不开，怎么开。** 不开。开关是记录里的 `demonstration_learning.enabled`，不写就按关算；没开时取示范返回 `"status": "disabled"`、0 条。对 AI 说“让这本书记住我认可的改法，下次类似的改稿先参考”。登记由学习循环的 `learn` 事件来做；`demonstration_memory.py` 自己只读，不改记录。

**聊天里能不能用。** 能手工做一个简化的，见[只能聊天时](#只能聊天时)。

**最短步骤。** 接着上面那一轮：先记一句你的认可（合成的），再登记示范，然后读出来。

```json
{"event_id": "loop-15-author_accept", "op": "author_accept", "run_id": "run-ch01-dialogue",
 "draft_sha256": "b8dae5726a16a0f338ea90f92e4f6cd314531df3e70f917648f178c4dfa0622b",
 "actor_role": "author", "mode": "human", "quote": "采纳当前稿。",
 "source_ref": "合成演示：这句不是真人作者说的；原话带了“（合成演示）”字样脚本就不认，所以只在出处一栏标明"}
```

```json
{"event_id": "loop-16-learn", "op": "learn", "run_id": "run-ch01-dialogue",
 "case_id": "case-书面腔-01",
 "why": "台词里的“我注意到……”是汇报口气；换成说话人会用的说法，办的事和给的信息不变。",
 "when": ["台词里出现“我注意到”“我意识到”这类汇报式开头", "说话人是随口说话的普通人"],
 "except": ["人物在做正式汇报或读记录"],
 "decisions": ["只换这一句的措辞", "补原因的建议不采纳：会带出原稿没有的判断"]}
```

```bash
python3 scripts/demonstration_memory.py check 项目/learning-record.md
python3 scripts/demonstration_memory.py index 项目/learning-record.md --project-id demo-bike-stall --task dialogue_revision
python3 scripts/demonstration_memory.py select 项目/learning-record.md --project-id demo-bike-stall --task dialogue_revision --limit 3
```

`check` 核结构、哈希，以及认可绑的是不是这一版文字：

```text
{
  "status": "valid",
  "case_count": 1,
  "enabled": true,
  "scope": "structure_hashes_and_approval_bindings"
}
```

`index` 只给元数据：编号、分组、任务、标签、状态、适用条件、例外，和支撑它的评审身份，不给正文；符合筛选的全部列出，不只三条。`select` 才给出改前、改后、取舍、条件和例外，一次最多三条，没排进来的编号列在 `not_selected` 里。这一条登记出来是 `"status": "author_accepted"`，带着那句原话和出处。

登记成什么状态，看这一轮实际留下了什么，另跑了两轮核过：没有你的认可、新稿只有工坊自查的，登记成候选（`candidate`），取示范时取不到；教师对新稿复查通过的，登记成教师认可（`teacher_approved`），取得到，但它不带你的认可。这两轮登记完，`next_action` 都是 `await_author_acceptance`：你以后明确采纳了，用 `case_accept` 补记。

另用九条合成案例核过取法（两条你认可的、两条教师认可的、候选一条、被拒一条、留出组里两条、别的书一条），结果照录：

| 做了什么 | 结果 |
| --- | --- |
| 不加限制地取 | 取到三条，顺序是两条你认可的在前，一条教师认可的在后；另一条教师认可的编号列在 `not_selected` 里；候选、被拒、留出组、别的书的都没取 |
| `--limit 4` | 命令行直接拒绝，只能取 1、2、3 |
| `index` | 四条可取的全部列出，各带适用条件和例外，不给正文 |
| `index --limit 2` | 拒绝：`index lists every eligible case; --limit and --case-id belong to select` |
| 换一个任务名，或者标签对不上 | 0 条 |
| 把这四条所在的场景组都排除（`--exclude-group`） | 0 条 |
| 开关关着 | `"status": "disabled"`，0 条 |
| 拿别的书的编号来取 | 拒绝：`Requested project_id differs from the authoritative store` |
| 你的认可没有原话和出处 | `check` 报 `invalid`：`author_accepted requires an author quote and source ref` |
| 正文改过、哈希没跟着算 | `check` 报 `invalid`：`hashes.after does not match the text` |

**它不做什么。**

- 只记录和检索，不更新模型参数，不是微调。
- 存成功了、取中了、检查通过了，都不证明文笔变好。
- `check` 只核结构、哈希和认可绑没绑对文字，不证明来源是真的。
- 只在当前这本书里取，不跨作品。
- 选择器不是文件访问控制：同一台机器上写稿的 AI 仍可能读到整份记录；近似的改写要人工核对。

**没验证的。** 用了示范以后稿子是不是更合你的意，没有对照；真实的示范库没有试过，这里全是合成案例。Windows 和 macOS 上没有跑过（这个脚本不用文件锁，按写法不挑系统）。

## 对白声纹与反模式检查

**是什么。** 一项只读的对白扫描，dialogue-lint 1.2.0，包里标的是“可选试用扩展”。

- 认“”「」『』三种引号。一行里开了引号到行末还没收的，按读到行末算一条台词，不进候选改句；直引号不当台词，报告里按行列出。
- 按引语逐条定位是谁说的，分四种：明确（`explicit`）、你指定（`manual`）、推测（`inferred`）、未知（`unknown`）。只有前两种算进人物的数字。
- 角色那一栏每个人一行，只给数字：台词数、待确认台词数、分句数、平均分句长、口语标记命中率。不和任何线比较，不给人物下“需要回读”“没问题”一类的结论（r5.55 起；r5.54-merged 会拿配置里的参考线比）。
- 不加 `--style-hints` 时，只做说话人归属和角色数字，另外只查本书配置 `suspicious_expressions` 里列出的词组；不列就不查措辞（r5.54-merged 写死的几个词组拿掉了）。
- 加 `--style-hints` 才用 13 条可选规则找三类可疑写法：伪口语 3 条（有限词组、把字句用词、同句语域）、机器压缩式短句 4 条（省略式祈使句、连续短句、简短状态并列、简短方位回答）、翻译腔 6 条（许可与宽慰句、身体部位指称、请求与命令表达、感知表达、关联词口吻、判断句语气）。
- 文风上的命中只标“复核”（`REVIEW`），告诉你回去读哪一句。你另外开了【】格式检查时，格式不符会报 `ERROR`，扫描的退出码是 1。
- 可以选三种题材预设（`modern_gritty`、`classical_xianxia`、`western_fantasy`），可以对通话、宣读这类场面逐句豁免，可以按本书声明检查【】面板格式。
- 你要候选改句时才走补丁流程：脚本在本地生成请求，AI 给出候选，候选先并排给你看、你认了才用。应用时要带和扫描时相同的 `--config`、`--style-hints`、`--genre`，脚本按同样的选项重扫一遍、核对请求，再校验原稿没变过、引语的位置和原文对得上、没有重复编号、改动只在这一条引语里面，通过了写进一个**新文件**，不覆盖原稿。

台词按人物分栏仍然是 `dialogue_lines.py` 的事（见[本地工作台与检查工具](tools.md#检查与辅助工具)）。合并版顺带修了它跨段认说话人的一处：上一段以“没有说：”“本想说：”这类没说出口的话收尾，下一段的引语不再算成这个人说的；“想了想，说：”照旧归给他。

**什么时候用。** 你觉得某个人物的台词变了味，想有个清单知道先回去读哪几句；你想让候选改句只动指定的那一句、不碰旁白。它不是交付门的必过项，不以“扫出 0 条”为目标。

**默认开不开，怎么开。** 不开，你要求时才跑。对 AI 说“用对白声纹检查扫一遍这一章，只扫不改”。全部文风提示要加 `--style-hints` 才开；题材不自动选；【】检查默认关；你只要扫描时，不生成也不应用补丁。

**聊天里能不能用。** 不能跑这项扫描，规则在脚本里；能用的是对白的人工读法，见[只能聊天时](#只能聊天时)。

**最短步骤。** 先照 `assets/dialogue-lint-config.example.json` 给这本书建一份配置，把人物登记进去。`profiles` 的键是人物名，值可以是空对象 `{}`，也可以写 `archetype`（你给这个人物起的类型名）和 `voice_prompt`（你对他说话方式的说明）；这两项都不改变任何检查：

```json
"profiles": {
  "老秦": {"archetype": "taciturn", "voice_prompt": "话少，报数不解释。"},
  "阿梨": {"archetype": "plain_student", "voice_prompt": "说话直，带一点学生气。"}
}
```

只扫不改：

```bash
python3 scripts/dialogue_lint/run_lint.py scan 正文/ch01.txt --config 本书配置.json --output 对白复核.json
```

合成稿六句台词，报告里的统计（节选）：

```text
"dialogue_quotes": 6,
"confirmed_quotes": 5,
"unconfirmed_quotes": 1,
"review_records": 0,
"candidate_quotes": 0,
"style_hints_enabled": false,
```

六句里五句按台词旁边的“某某说”“某某……，问：”认出了说话人。剩下一句是“老秦把内胎捞出来，甩了甩水，说：……”，说话的词和人名之间隔了一个动作，脚本记成未知（`发言提示语中的角色未登记或无法确认`），不猜；要把它算给老秦，得在配置的 `speaker_overrides` 里指定段号和引语号。

开全部文风提示，同时出一份补丁请求和给 AI 的提示：

```bash
python3 scripts/dialogue_lint/run_lint.py scan 正文/ch01.txt --config 本书配置.json --style-hints \
    --output 对白复核-全部提示.json --request-output 请求.json --prompt-output 请求提示.txt
```

这次多出一条复核（稿子里特意放了一句“我注意到后胎也有点瘪。”），报告里这一条（节选）：

```text
"rule_id": "TRANS_04_EXPLICIT_MENTAL_VERB",
"severity": "REVIEW",
"matched_span": "我注意到后胎也有点瘪",
"description": "命中显式感知或心理表达；汇报、辨认与强调信息来源时可以保留。",
"quote_id": "p9:q2",
"speaker": "阿梨",
"confidence": "explicit",
```

把 `请求提示.txt` 交给 AI，拿回一份只含候选的 JSON（下面这份是手写的，替代 AI 的答复）：

```json
{
  "source_hash": "3e0ded065546ae186b1f5e433bef68ebafe7db6d831eff3f6d6a5f8028e992ae",
  "replacements": [
    {"quote_id": "p9:q2", "original": "我注意到后胎也有点瘪。", "replacement": "后胎好像也有点瘪。"}
  ]
}
```

你看过、认了，再应用到新文件，`--config` 和 `--style-hints` 照扫描时带：

```bash
python3 scripts/dialogue_lint/run_lint.py apply 正文/ch01.txt 请求.json 候选.json --output 正文/ch01.候选稿.txt \
    --config 本书配置.json --style-hints
```

```text
已生成：正文/ch01.候选稿.txt（重新扫描核对过的可改引语 1 条，本次替换 1 条：p9:q2）
```

新文件和原稿只差第 9 行这一句，原稿的字节没有变。**命中只是回读线索，改不改、用不用这句候选，都是你定。**

同一份材料上还实际试过这些：

| 做了什么 | 脚本怎么答 |
| --- | --- |
| 不带配置扫 | 退出码 0，六句全部记成未知，0 条复核 |
| 输出文件名已经存在 | 拒绝：`输出必须使用各自不同的新文件名` |
| 候选想借一对引号把旁白塞进去 | 拒绝：`replacement brings in quotation marks or brackets the line did not have: “”` |
| 候选想改请求以外的一句 | 拒绝：`duplicate or unknown quotation ID` |
| 请求生成以后原稿动过 | 拒绝：`原稿在扫描之后改过，旧请求作废，请重新扫描` |
| 应用时少带了 `--style-hints` | 拒绝：`请求和这次的 --config、--style-hints、--genre 对不上：apply 要带和 scan 相同的配置和选项` |
| 配置里指定最后一句是老秦说的，再选 `--genre modern_gritty` | 那一句记成 `manual`，老秦的确认台词从 2 句变 3 句 |
| 同一份稿子把引号全换成「」 | 六句照样认出来，结果和用“”时一样 |
| 旧配置里还写着 `min_avg_len`、`min_colloquial_rate` | 照扫，报告的 `config_notes` 写明这两项不再使用 |

**它不做什么。**

- 不判语病，不判是不是 AI 写的；口语标记命中率不是“人味分”。
- 没有本书配置、人物没登记时，说话人全记未知，不进人物指标和补丁。
- 推测和未知的引语不进补丁；不为了提高覆盖率乱认人。
- 不按指标添“呢”“嘶”，不改句号，不补动作。
- 校验只保证改动的范围，不保证事实和文学效果没变；应用以后仍要对照原稿回读。
- 不处理同一引语跨行的软换行（包里的说明这样写，这一页没有试）。

**没验证的。**

- 包里写明：实际文笔效果待测试，对白自然度没有验证。命中的句子是不是真的不像人说的，没有对照。
- 这一页的候选是手写的，没有让任何 AI 生成过候选。
- Python 版本：包里写的最低版本是 3.9。r5.54-merged 在 3.9 上一导入就报错，r5.55 修了：包内验证记录写着这一组的 120 项测试在 Python 3.9.25、3.11、3.12、3.13 上都过。这一页只在 3.13 上跑过，没有在 3.9 上重跑。
- Windows 和 macOS 上没有跑过。

## 只能聊天时

聊天环境一般不运行脚本。四个模块的说明都在便携单文件里：搜 `内嵌内容：` 加路径（比如 `内嵌内容：references/chapter-confirmation.md`），从标题下一行起，复制到下一行 `-----` 为止。单文件很大，平台多半只检索片段，所以要用哪个模块，就把那一篇整篇贴进项目指令或第一条消息，和[交付门卡](chat-cards.md#交付门卡)放在一起。

| 模块 | 聊天里怎么做 | 做不到的 |
| --- | --- | --- |
| 章节门 | 贴 `references/chapter-confirmation.md`（约 13,900 字符）；教师的结果回来时再贴 `references/teacher-review.md`（约 5,400 字符）。AI 照着一步一步停下等你，在同一份工作记录里人工记下版本、阶段和你的原话 | 没有脚本拦跳步、拦错版；哈希绑定做不了，只能在记录里写清是第几章的第几版 |
| 学习循环 | 贴 `references/learning-loop.md`（约 11,800 字符），让 AI 把意见、每条怎么取舍、实际改动、新稿复查照同样的栏目记下来 | 条件保存、重发不重记、稿件哈希绑定都没有 |
| 示范记忆 | 自己存一份对照：改前、改后、为什么、什么时候适用、什么时候不适用、谁认可的。相似任务时贴最多三条，说明只当参考 | 自动筛选、留出组隔离 |
| 对白声纹 | 这项扫描做不了。改用对白的人工读法：让 AI 把台词按人物分开读（见[详细用法](usage.md#对白人物说话不像人或者分不清谁在说)） | 13 条规则的定位、候选改句的范围校验 |

聊天里的记录是人工维护的：存不存得住看平台，工坊不会把没存下的说成已经存档。想留就让它贴出来，自己保存。交付门卡第 8 条“授权整批就直接做”在开了章节门时让位：整批授权只免试点，不免每章的阶段确认。

可以这样开口（都是合成的例子，换成你自己的）：

1. **开逐阶段确认**

   > 以后每写新的一章都走完整流程：材料与目标、章节方案、写前准备、初稿、审稿与修订计划、修订稿、定稿记录，一步一步给我看，我确认了再往下。

2. **教师的结果回来了**

   > 教师的改稿回来了，改的是第〈N〉章〈哪一版〉初稿。先别动我的稿子：并排列出原句和教师的改句，每一处讲明多了什么、丢了什么，你建议采纳、拒绝还是暂缓，理由是什么。整份方案我确认了再改。

3. **改完以后**

   > 改完按新稿再查一遍，不要拿上一版的结论顶。这一版我看过再说采不采纳。

## 本页的命令是怎么核的

- **环境。** Linux，Python 3.13.17，2026-11-14，r5.55 包里没改过的脚本。材料全是为这一页新写的合成文字：一个巷口修车摊的小场面，两个人，六句台词；r5.55 重跑时稿子重写过一遍，所以哈希和 r5.54-merged 那一次不一样。事件里“作者原话”那一栏（`author_quote`）和教师意见也是合成的，都标着“合成演示”，不是任何真人的确认；最后一步和“你的采纳”那两句带了这几个字脚本就不认，合成的字样写在出处一栏。
- **材料和输出在哪。** 稿子、事件、配置都写在驱动脚本 [demo/08-modules/run-demo.py](../demo/08-modules/run-demo.py) 里；它跑出来的事件文件、配置和每条命令的原样输出（各部分的 `transcript.txt`）都在 [demo/08-modules/](../demo/08-modules/)，说明见[实际效果样例](../demo/README.md)第 8 节。照那一节的命令重跑，这一页摘的输出和哈希都能对上。
- **跑了什么。** 章节门：最短四步，接着一路走到最终采纳，连同上表的试错和第二章的 `chapter_policy`，45 条命令。学习循环：一轮连同登记示范、读示范、你的采纳和否定意见的试错、另两轮核登记状态、停用，52 条。示范记忆：九条合成案例的取法和两份改坏的记录，11 条。对白检查 12 条。另外直接调用章节门脚本里那道最后一步的措辞检查，试过不带“（合成演示）”字样的“继续。”“先不采纳，我再看看。”“还没到定稿的时候。”，都留在等待；“定稿。”“采纳当前稿。”记下（[final-words/transcript.txt](../demo/08-modules/final-words/transcript.txt)）。r5.54-merged 那一次还跑过台词分栏跨段认人 1 条、在一份 JSON 项目状态文件上跑章节门的头两步；`dialogue_lines.py` 在 r5.55 里没有变，这两项这次没有重跑。
- **两条命令的跑法。** 这一页每条命令都是用 Python 的隔离模式加不写缓存（`python3 -I -B`）直接跑的，没有包装。r5.55 起 `chapter_gate.py status` 和 `dialogue_lint/run_lint.py` 这样也能启动；r5.54-merged 下这两个一启动就报 `ModuleNotFoundError`，上一次核这一页时用了一行把脚本目录放回搜索路径的包装。页面上写的 `python3 scripts/…` 是包内文档的普通写法，这里没有用不带 `-I` 的写法重跑。
- **没有核的。** Windows、macOS；Python 3.9 到 3.12；任何真实稿件；真实的教师回传；AI 在真实对话里会不会照这些步骤做。包里的回归测试这一页没有重跑：包内 `VERIFICATION.md` 记着全套 1,589 项，在 Linux、Python 3.13 上跳过 5 项、其余全过，在 Python 3.9.25 上跳过 74 项、其余全过；它说明脚本照说明工作，不评价文学质量。
