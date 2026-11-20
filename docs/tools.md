# 本地工作台与检查工具

[← 返回首页](../README.md) · 适用版本 `2026-11-19-r5.59`

这些都是可选的。只在聊天里写作用不到它们；除维护用的 `darwin_eval.py`（在 `skills/darwin-novel-workshop/scripts/`）外，都在完整包的 `skills/novel-workshop/` 里；便携单文件里没有可运行的脚本。完整命令见包内 `USAGE.md` 第五节和 `skills/novel-workshop/references/local-workbench.md`。

这一页讲的是工作台和脚本做什么：脚本只核对程序能核对的东西，不评价文笔。工坊整体是让 AI 照着做的方法，不是效果保证。用工坊写、改的稿子，只和不用工坊的 AI 写、改的稿子比过一次（r5.46，规模小，执行和评审都是同一类模型）：改 AI 腔重的稿子，排第一的都是不用工坊的；从头起草，工坊多数在前。之后没有再比过。对白是不是更像人、更有感情，没有验证；好不好由你读了定。

- [本地工作台](#本地工作台)
- [检查与辅助工具](#检查与辅助工具)
- [可选视觉链路](#可选视觉链路)
- [运行条件与平台限制](#运行条件与平台限制)

## 本地工作台

需要 Node.js 18 或更新版本，只用内置模块，不装依赖。用来在本机浏览、搜索、预览和（可选）编辑作品文件。工作台读写文稿不联网、不调用模型，也不是云端服务；安装技能不会自动启动它。r5.59 起它没有 AI 侧栏，见下面[r5.59 起没有 AI 侧栏](#r559-起没有-ai-侧栏)。

### 打开

不用记命令：在技能目录的 `scripts/oh-story/` 里双击启动器。

- Windows：`open-workbench.cmd`（只读）或 `open-workbench-edit.cmd`（可改稿）。
- macOS：同名的 `.command`。从 ZIP 解出来的 `.command` 没有执行权限，双击会提示没有权限；可以在终端进入 `scripts/oh-story/` 运行 `sh open-workbench.command`（可改稿用 `sh open-workbench-edit.command`），或者先运行一次 `chmod +x *.command` 再双击。
- Linux：在终端里运行 `sh open-workbench.command`。
- 想先试一试：双击 `open-workbench-demo`。它在系统临时目录里放一份标明“合成示例”的小作品，以可改稿方式打开，随便改不碰你的作品。

第一次会问作品放在哪个文件夹（把文件夹拖进窗口再回车），以后记住；默认先找“文档/小说写作工坊”。启动后自动用浏览器打开，关掉启动窗口就停止。启动器只在本机用户配置目录的 `workbench.json` 里记作品目录的路径，不记文稿内容。

也可以直接运行服务程序，把路径换成自己的作品目录：

```text
node scripts/oh-story/dashboard-server.mjs --root "D:/小说/我的作品" --open
```

默认只读；加 `--allow-edit` 才允许改稿。只允许本机访问，必须明确指定作品根目录，不自动扫描个人主目录。默认端口 43110，被占用时往后找可用端口。关掉启动窗口或按 Ctrl+C 结束。

### 能做什么

拆文库与写作项目分栏、按文件名搜索、目录分页、文本查看、Markdown 预览、行号、明暗模式和恢复上次视图。认得“正文”“大纲”“设定”“追踪”等常见目录；没有这些目录时照样展示指定的根目录，原有作品不用重排。

限制：

- 搜索按文件名，不是全文搜索。
- 单个文件上限 2 MiB，更大的用本地编辑器。
- 能编辑的文件类型是 `.md`、`.txt`、`.json`、`.yaml`、`.yml`、`.toml`。
- Markdown 预览只做基础排版，表格和链接显示得简单；原始 PDF 用本地 PDF 阅读器打开，工作台可以读对应的提取文本。

### 编辑：两层开关

1. 用 `open-workbench-edit`（或 `--allow-edit`）启动，才允许改稿；只读启动时页面上的“开始编辑”是灰的。
2. 可改稿启动以后，每份文稿打开时仍是只读，点“开始编辑”才能改。

只照命令加了 `--allow-edit`、却发现还不能改的，多半是还没点“开始编辑”。

- 页面底部一直显示这份文稿的状态：只读、编辑中、未保存、保存中、已保存、保存失败。Ctrl+S（macOS 为 ⌘S）保存。
- 未保存的修改记成草稿，存在这台浏览器里：换文件、刷新、关闭页面都不会丢。再打开这份文稿时可以恢复、对比或丢弃草稿。
- “对比”按段列出打开时（或上次保存后）的版本和页面里现在的文字有哪些不同。
- 每次保存前，在作品根目录的 `.novel-workshop-backups/` 里备份原始字节和记录；备份失败就不保存。工作台不自动清理备份，不提供删除文件的功能。
- 保存前核对打开时的文件版本；磁盘上被别处改过的，拒绝覆盖，你可以保留当前编辑、对比磁盘版本或载入磁盘版本再决定。
- 不要用工作台直接编辑由 `project_state.py` 管理的状态文件。

### r5.59 起没有 AI 侧栏

r5.46 到 r5.58 的写作台有两个可选的侧栏：“改稿建议”（自备 Gemini API Key，r5.46 起）和“Google AI”（用 Google 的官方程序登录，r5.49 起，只用模拟程序测过）。r5.59 把两个都删了，连同它们的接通检查脚本（`gemini-check.mjs`、`acp-check.mjs`）和双击检查的启动器（`check-gemini`、`check-acp`），一共 11 个文件；服务里对应的接口也不在了。

- 读稿、改稿、草稿、对比、保存前备份这些本地功能照旧；拆文索引、人物关系图、演示启动器也照旧。
- 要请模型改一段，在对话里交给当前会话，或者你自己交给你选的教师。章节门里初稿交教师的默认设置（gemini-4-argon，思考等级选“高”，可以改，见[四个可选模块](modules.md#章节门)）没有变：那是你自己交给教师，不经过写作台。
- 以前用过这两个侧栏的，电脑上留着的密钥和本机记录，工坊不碰；不再用的，可以自己删。它们都在本机用户配置目录里（Windows：`%APPDATA%\novel-workshop\`；macOS：`~/Library/Application Support/novel-workshop/`；Linux：`~/.config/novel-workshop/`）：“改稿建议”的是 `gemini.json`、`gemini-status.json`、`gemini-check-report.txt`；“Google AI”的是 `acp.json`、`acp-status.json`、`acp-events.jsonl` 这几样 `acp` 开头的文件。删了 `gemini.json`，Key 本身在 Google 那边照样有效；自己装的官方程序和它记着的登录不是工坊的，工坊不动。完整的清单见包内 `skills/novel-workshop/references/local-workbench.md`“r5.59 起没有 AI 侧栏”。
- 同一个文件夹里的 `workbench.json` 是启动器记的作品目录，还在用。
- 从 r5.58 升级时，删掉的 11 个文件随旧版进 `.novel-workshop-backups/<时间>/`；退回 r5.58，两个侧栏就回来。
- 首页和[实际效果样例](../demo/README.md)里的工作台截图是 r5.59 的（2026-11-20 重拍）：工具栏上只有开始编辑、对比、行号、原文、预览；r5.58 及以前的工具栏上另有“改稿建议”“Google AI”两个按钮。

## 检查与辅助工具

需要 Python 3.9 或更新版本，在 `skills/novel-workshop` 目录运行。`scripts/` 顶层有 19 个脚本（r5.54-merged 多了 `chapter_gate.py`、`learning_loop.py`、`demonstration_memory.py` 三个），另有 `scripts/dialogue_lint/` 目录（入口 `run_lint.py`，也是 r5.54-merged 多的）和 `scripts/oh-story/` 下的几个拆文工具。脚本只给要回去读的位置，不打分，也不判断文字是不是 AI 写的；命中不等于必须改，没命中也不说明写得好。

| 脚本 | 作用 |
| --- | --- |
| `punctuation_lint.py` | 标点与断句，给出行列、规则编号和等级，只读；可带作品的标点规则文件；`--baseline` 对照原稿，只列修改后新出现的问题 |
| `prose_lint.py` | 语感扫描和分场检测（重复词、段尾否定、等长短句连排、三连排比等）；`--hint deai` 加去 AI 味的复核提示（r5.48），`--hint deai-extra` 再加四项（r5.49）；r5.54-merged 多一个 `--hint xian`：叙述里“先”字的复核，只定位和计数，默认不开，不随 `deai` 开 |
| `dialogue_lines.py` | 台词按说话人分栏，标出书面词、叙述专用的词；`--exchanges` 按来回再列一遍（r5.53）；加 `--long-lines` 才列一口气很长的句子（r5.54）；r5.54-merged 修了跨段认说话人的一处：上一段以“没有说：”“本想说：”这类没说出口的话收尾，下一段的引语不再算成这个人说的 |
| `detail_check.py` | `compare`：原稿里有、修订稿里没了的说法和动态补语；`changes`：逐句列出删了、加了、改了哪几句，`--keep` 核对指定要留的句子（r5.49）；`anchors`：维护时用的写作对照例，r5.59 起对照例可以带 `no_new_dialogue`，带了的核对时找出新加的台词，有就不通过（同一句拆成两句不算新加），没带的结果不变；只换格式、不动字句时怎样用 `changes` 加 `--keep` 对照、它核不到什么，见表下那一段（r5.57） |
| `fact_guard.py` | 跨章事实主张比对、列出要回查的章节；按故事时间核人物知情（r5.51）；只核对已登记的主张 |
| `rule_register.py` | 几份规则文件互相打架时，核对冲突登记表、列出待定项、查新叫法在各章的已有用法；新规则入册以后，已采纳的章不自动改，`collide` 能列出旧叫法在哪一章哪一行，工坊照这个列给你定（r5.58 写明，脚本没有改） |
| `workflow_guard.py` | 交付门：冻结输入、审稿绑定具体版本、输出四项状态、记录你的采纳（也能照实记录跳过审稿）；核对交出去的文件是不是检查过的那一版（`status --deliverable`），跳过审稿采纳的那一版这样核对不上，“说定本”是 BLOCK；还没有收回采纳的命令：你收回采纳以后，同一版仍显示 `AUTHOR=ACCEPTED`，不能照它说已定稿（r5.57 照实写明，脚本没有改，见[详细用法](usage.md#交付状态)） |
| `delivery_manifest.py` | 多章交付：核对约定章数、实际文件、漏章、空稿和旧审稿 |
| `state_precheck.py` | 项目状态保存以前，列出候选要删、要改、要加的字段，只读（r5.49） |
| `project_state.py` | 多人、多代理共用的项目状态文件，条件保存 |
| `style_cards.py` | 风格卡：列索引（`index`）、字面线索（`match`）、加载选中的卡（`load`）、查有没有照搬卡里原话（`copied`）、核对卡库和本书配置（`check`） |
| `inspiration_library.py` | 本书灵感库：核对记录、按章或按人物地方列出、出素材卡的素材块 |
| `inspiration_write.py` | 写灵感库的唯一入口：迁移旧版、记下选择、回退、看历史，写前核修订号 |
| `visual_materials_cli.py` | 可选的联网选图链路，见下文；r5.59 起读来源页和取图都守 robots.txt，同一站点的请求有间隔，另带一个只用标准库的自带读页（`visual_materials/static_reader.py`） |
| `export_portable.py` | 导出核心文件夹、单文件或安装包（`--mode personal\|sale`、`--format portable\|install`），不自动发布；个人导出默认不带 `assets/project-packs/`，命令行说有几份没带，加 `--include-projects` 才带上整个文件夹，连同作者改法累计 `_author/`，只有 `_author/` 的也能用（r5.56）；`--mode sale` 一律不带，便携单文件不展开它；出错时打印 “Export stopped: …”、退出码 1；r5.59 起视觉链路那一组的导出清单加了自带读页 `static_reader.py`，商业版的清单去掉了写作台两个侧栏的 11 个文件 |
| `workflow_demo.py` | 虚构三章演练，审稿与采纳都是模拟的，只用来熟悉流程 |
| `chapter_gate.py` | 章节门读进度（只有 `status` 一个子命令，只读）：这一章停在七个阶段的哪一步，等你确认还是等教师回传，按什么策略走（`workflow_policy`），记录里缺了什么（`record_problems`）；写入走 `learning_loop.py apply`。默认不开，见[四个可选模块](modules.md#章节门) |
| `learning_loop.py` | 学习循环和章节门的记录入口：`status`、`context`、`show` 只读，`apply` 一次交一个事件（带版本的条件保存，同一事件重发不重记）；不调用模型，不写小说。r5.59 加了几个可选的写法：登记示范时可以重写标签（`tags`），一章几场的适用判断可以按场写（`scopes`），这一稿是谁写的可以记下来（`role`）；收尾凭的是你本人的通过时记 `author_reviewed`（r5.58 记 `self_checked`）；不带新写法的旧事件照旧能用，结果和以前一样。见[四个可选模块](modules.md#学习循环) |
| `demonstration_memory.py` | 示范记忆的只读选择器：`check` 核结构、哈希和认可绑的文字，`index` 列出全部符合筛选的案例（只给编号、状态、适用条件和例外这类元数据），`select` 取最多三条认可过的示范。r5.59 起认可选的来源字段 `after_by`（改后的文字是谁写的），案例带了它的，`index` 连同它一起列出；来源字段写成列表、对象这类非字符串时，`check` 不再抛错停下，照未知值报出来。见[四个可选模块](modules.md#示范记忆) |
| `dialogue_lint/run_lint.py` | 对白声纹与反模式检查（可选试用，r5.55 起为 1.2.0）：`scan` 只读扫描出报告，认“”「」『』，角色一栏只给数字，命中只标“复核”；`apply` 要带和 `scan` 相同的选项，重扫核对、校验候选改句以后写到新文件，不覆盖原稿。见[四个可选模块](modules.md#对白声纹与反模式检查) |
| `oh-story/build_chapter_index.py` | 章节位置索引：章节范围、原文行号、字符数与内容哈希，不做文学分析 |
| `oh-story/render_relation_chart.py` | 从已有的人物关系表生成 Mermaid 关系图，可选 PNG；不自行推断人物关系 |
| `oh-story/inspect_existing_assets.py` | 只读检查已有拆文资料的覆盖情况 |
| `darwin_eval.py`（维护技能里） | 维护用：保存与汇总方法对照记录，不调用模型、不生成正文、不评分；r5.58 起，`blind` 打包以前先查两份产出里的版本线索（产出的路径、两份文件名不同时的文件名、两版技能目录的路径，加上用 `--identity-marker` 登记的），查到就以退出码 2 停下，什么文件都不写；中途出错时删掉这一次新建的文件，不留半截。查不到的线索（没登记的版本号、改写过的措辞、附件和图片）照旧要人工看一遍。r5.59 起，`freeze` 逐节核登记表里上锁的六节（`protected_sections`），改了又没有批准记录的，`summarize` 判 `BLOCKED_CONSTITUTION_CHANGE`；同一道题跑几次的可以用 `group` 合并再算；`blind` 的结果多 `packets`（两份匿名材料的 SHA-256），`verdict` 要求裁决带 `packets`，缺了、写坏了、和这个评估目录封存的 A／B 对不上的，以退出码 2 拒收 |

**只换格式、不动字句时怎样对照（保真转换，r5.57）。** 用 `detail_check.py changes 原稿 转换稿` 逐句对照，再加 `--keep`（把原稿每个非空行照原样写成一行锁句）核一遍，每一行都要是“原样在”。包里用合成短文实际跑过，核不到的照 `references/editing.md`“先定范围”里的“保真转换”写：`changes` 对硬换行接起来的几句多半只报“几句并成了一句”、不逐字比，汉字之间多出来的空格不报，两段并成一段只在段数上看得出，两章换了先后只列一章；`--keep` 对接头处多出来的字、汉字之间的空格、两段并成一段、章节换了先后，照样报“原样在”，很短的一行在别处出现过也算原样在。再跑 `punctuation_lint.py 转换稿 --baseline 原稿`，它列出转换带进来的半角标点和多出来的空格，删掉一个标点、换成另一个全角标点它不报；`workflow_guard.py status --deliverable` 只认同一版、只差末尾换行、只差换行符或 BOM。这几样都只读 UTF-8 文本，Word、PDF 先取出文字再比。没有一样能单独证明逐字相同：`changes` 里除了标题行和硬换行接起来的那几处，没有删、加、改的句子；`--keep` 每一行都是“原样在”；“对不上”里列的和硬换行接起来的那几处逐字读过；段数和章节顺序核过；`punctuation_lint.py --baseline` 没有新出现的空格和半角标点。这几样都做到了，才写“去掉格式以后正文逐字相同”。交付门里没有专门核这一项的检查，MECHANICAL 是 GREEN 不说明保真核过。怎样交付见[详细用法](usage.md#只换格式不动字句保真转换)。

Node 一侧原来另有两个接通检查 `gemini-check.mjs` 和 `acp-check.mjs`，r5.59 随两个侧栏一起删了。

安装脚本 `install.py` 在完整包的根目录，不在 `scripts/` 里（r5.56 改过）：`--upgrade` 先把装着的 `novel-workshop/assets/project-packs/`（作者改法累计 `_author/` 和你放进去的作品资料）复制进新版，每个文件核一次 SHA-256，再换上新版；`--dry-run` 的报告里，`carried` 列出要带过去的文件，`conflicts` 列出对不上的。新包在那里也带了同名而内容不同的文件的，它在写任何东西以前停下，退出码 1，要你加 `--keep installed`（留装着的）或 `--keep package`（用新包的，装着的那一份只留在备份里）再运行，一次对所有对不上的文件选同一边。符号链接和目录联接（junction）都拒绝。r5.55 和更早的安装器不带这个文件夹，用它们退回时记录留在备份里。用法见[详细用法](usage.md#升级与回退)。

几条常用命令（路径换成自己的）：

```text
python3 scripts/punctuation_lint.py 正文/第05章.md --format text
python3 scripts/prose_lint.py 正文/第05章-修订.md --hint deai --format text
python3 scripts/dialogue_lines.py 正文/第05章.md --names 甲,乙
python3 scripts/detail_check.py compare 正文/第05章.md 正文/第05章-修订.md
python3 scripts/style_cards.py index
python3 scripts/chapter_gate.py status 项目/学习记录.md --chapter-id 第05章
python3 scripts/learning_loop.py status 项目/学习记录.md
python3 scripts/demonstration_memory.py select 项目/学习记录.md --project-id 本书 --task dialogue_revision --limit 3
python3 scripts/dialogue_lint/run_lint.py scan 正文/第05章.txt --config 本书配置.json --output 对白复核.json
```

后四条属于默认不开的四个模块；事件文件怎么写、实际跑出来是什么样，见[四个可选模块](modules.md)。

整包测试在交付包目录运行 `python tests/run_tests.py`。r5.59 一共 2,005 项，照包内 `VERIFICATION.md` 本版一节：在 Linux、Python 3.13 上跳过 5 项，其余 2,000 项全部通过；在 Linux、Python 3.9.25 上跳过 81 项（多跳的是没装 Pillow 的 63 项、没装 PyYAML 的 2 项和 Crawl4AI 要 3.10 以上的 11 项），其余 1,924 项全部通过。其中章节门的测试 45 项，学习循环 69 项，对白声纹的测试目录 120 项，这几组和 r5.55 到 r5.58 相同；示范记忆 19 项，r5.59 加了 3 项（`after_by` 和非字符串的来源字段）。r5.59 新加九个测试文件，一共 255 项：技法库 25 项（`tests/test_r559_technique_library.py`），自我纠错 42 项（`tests/test_r559_self_correction.py`），学习循环的新写法 19 项（`tests/test_r559_learning_loop.py`），维护 48 项（`tests/test_r559_maintenance.py`），裁决带 `packets` 11 项（`tests/test_r559_verdict_packets.py`），引句只有标点 11 项（`tests/test_r559_closing_notes.py`），取图的规矩 61 项（`tests/test_r559_collect_hygiene.py`），自带读页 25 项（`tests/test_r559_static_reader.py`），版本号和本版说明 13 项（`tests/test_r559_package.py`）。网络一律用本机的临时服务或注入的替身，Crawl4AI 一律用替身。只测两个侧栏的三个测试文件（`tests/test_r547_gemini.py`、`tests/test_r549_acp.py`、`tests/test_r550_acp.py`）和它们的两个辅助文件删了；写作台的 Node 检查（`node tests/workbench_check.mjs skills/novel-workshop`）从 32 项变成 12 项，全过。此前各版新加的测试文件照旧在：r5.56 三个（安装器和导出器 40 项、页面说法 21 项、版本号和本版说明 7 项），r5.57 两个（页面说法和脚本行为 27 项、版本号和本版说明 10 项），r5.58 五个（点名改一处 10 项、新规则入册 11 项、转来别人的话怎么记 17 项、匿名对照材料检查 17 项、版本号和本版说明 14 项）；其中几份钉着旧说法的跟着 r5.59 改过，测试里写了为什么改。这一页没有重跑全套。测试检查脚本行为，比如标点定位、事实比对、审稿版本绑定、回传绑错版拒收、升级带上记录、对不上时停下、取图前先问 robots.txt，不评价文学质量。

## 可选视觉链路

给一章找参考图：SearXNG 和 Openverse 两路搜索，读来源页（Crawl4AI，或者工坊自带的读页），ImageHash 把近似图归组，OpenCLIP 按这一场的文字和你的参考图排序；看过图以后由你挑整张或局部，挑中的部分写进本书的灵感库。写作、审稿和灵感库的核对、列出不需要它；你自己提供图片，也可以直接按素材方法写作。完整说明见包内 `skills/novel-workshop/references/visual-materials.md`。

- **要装的**：Pillow（解码图片）；ImageHash；OpenCLIP（会带上 torch，权重另下）；SearXNG 自己跑一个实例。Openverse 不用装。Crawl4AI（需要 Python 3.10 以上，还要装它的浏览器）r5.59 起不是非装不可：没装、Python 低于 3.10、或者它的浏览器起不来时，collect 用工坊自带的读页去读来源页。工坊只带调用这些项目的适配器，没有它们的代码、权重和密钥。
- **自带读页（r5.59）**：只用 Python 标准库，用工坊的普通请求取网页的 HTML，不开浏览器，不执行网页里的脚本。靠脚本才显示的图它读不到，这时照实记下有几段脚本没跑，不说读过整页；要看这些图，自己在浏览器里打开来源页，或者装好 Crawl4AI 再读。谁来读由配置的 `page_reader.use` 定：`auto`（默认）是 Crawl4AI 能用就用它，用不了就用自带读页；`crawl4ai` 是只用 Crawl4AI，用不了就不读来源页；`builtin` 是只用自带读页。自带读页读的页不算 Crawl4AI 接通。
- **取图的规矩（r5.59）**：读来源页和取图都守 robots.txt，这一条不能关；robots.txt 不许，或者这一次取不到的，不打开、不取。同一站点两次请求至少隔 1 秒，只许调慢；站点拒绝（401、403、451）或出验证页的、限流（429）的，这一次运行不再向这个站点发请求，不重试，不换请求头或工具再试。工坊不绕过网站的防护：不过验证页，不解验证码，不用代理换地址，请求头写明是工坊，不冒充浏览器；配置里没有这类开关，写了的脚本拒收。你知道某个站不许自动访问的，把它写进 `network.blocked_hosts`。robots.txt 取几种读法里最严的，所以装的是 Python 3.9 还是 3.13 结果一样，代价是偏严，候选会少。这些管的是工坊自己发的请求（问 robots.txt、自带读页读页面、取图），是 collect 读页和取图的规矩；搜索这一步不按站点间隔。用 Crawl4AI 读页时是它的浏览器在请求：工坊只在把页面交给它以前查一次地址、问一次 robots.txt、等一次间隔，把自己的身份交给它（参数名没在装了 Crawl4AI 的机器上核对）；浏览器实际报什么身份、带不带站点种下的 cookie、它自己跟的跳转、页面里加载的图和脚本，工坊管不到，没验证。
- **缩略图（r5.59）**：原图取不到才退到搜索给的缩略图。原图因为 robots.txt 不许或这一次取不到、站点拒绝、站点在你的 `blocked_hosts` 里、这一次运行的请求数到了上限而取不到的，缩略图也不取（r5.58 会退到缩略图）；超时、文件太大这类原因照旧退缩略图。
- **图归原作者**：取来的图只用来给你看、给工坊比对；页面上写的署名、图注和授权链接另记一栏，标明工坊没有核对，不当作授权。参考是借几样写进文字，不是用图本身；网上找来的图不放进正文、封面、插图或要分发的文件，要那样用，得另外取得权利人的授权。
- **配置**：照 `assets/visual-materials-config.example.json` 复制一份，填 SearXNG 地址、权重路径和哈希；密钥只放环境变量。r5.59 起每一节只收样例里有的键，写错的、不认识的直接拒收（以前悄悄丢掉）；`network.user_agent` 必须以 `novel-workshop-visual-materials/` 开头，可以在括号里加你的邮箱或网址，不能写成浏览器的样子；`network.min_interval_seconds` 不能少于 1。r5.58 能用的配置在 r5.59 可能读不进来，照报错改。
- **核验**：`visual_materials_cli.py doctor` 逐项报代码在不在、这台机器配齐没有，也报 collect 会用谁读来源页、为什么；加 `--probe` 逐项真调一次。跑完一次完整运行，用 `verify-run` 看这一次实际跑通了什么。五项都在同一台机器上核得上，才算接通（`ALL_FIVE_LIVE`）；差哪项就照实写哪项；自带读页读的运行单列一行，不算进五项。
- **实际情况**：做这条链路时（r5.35），制作环境里只有 ImageHash 真跑通；SearXNG 没有实例，Openverse 的请求被网络拒绝，Crawl4AI 和 OpenCLIP 没装上。r5.59 的改动也是这样验的：制作环境里没装 Crawl4AI，它一侧全是替身；自带读页、验证页的认法、robots.txt 的判定都只用本机的临时服务和替身网络测过，没在真实网站上跑。在你的电脑上通不通，要自己跑一次 `doctor --probe` 和一次完整运行才知道。
- 搜索只发几个短词，不发正文；运行文件夹是这一次搜索的缓存，属于你的私人材料，删掉不影响写作。

## 运行条件与平台限制

- 检查脚本和安装脚本要 Python 3.9 或更新版本；工作台要 Node.js 18 或更新版本；Crawl4AI 要 Python 3.10 以上，找图链路的自带读页不受这个限制（r5.59）。
- Windows 上命令写 `python` 或 `py`。交付门、标点、文字检查、台词分栏、灵感库、视觉素材、事实比对、批量清单、冲突登记表、风格卡这几个脚本按设计可以在 Windows 上运行，输出都是 UTF-8。
- `project_state.py` 使用 POSIX 文件锁，只支持 Linux、macOS 等系统，原生 Windows 不支持；依赖它的三章演练在 Windows 上会说明原因后退出。
- 四个模块的脚本只用 Python 标准库。`learning_loop.py`（读和写）和 `chapter_gate.py status` 用的是和 `project_state.py` 同一种文件锁，原生 Windows 同样不支持；每次读写会在记录旁边留一个 `.记录文件名.lock` 的空文件。`demonstration_memory.py` 和 `dialogue_lint/run_lint.py` 不用文件锁，按写法不挑系统。四个模块都没有在 Windows 上跑过。
- r5.55 起，`chapter_gate.py status` 和 `dialogue_lint/run_lint.py` 加 Python 隔离模式（`python3 -I`）也能启动（r5.54-merged 下会报 `ModuleNotFoundError`）；按普通写法 `python3 scripts/…` 运行也行。包里写明 `chapter_gate.py`、`learning_loop.py` 照普通写法跑也不在技能目录里留 `__pycache__`；`run_lint.py` 的代码里也设了不写缓存。
- `dialogue_lint/` 这一组：r5.54-merged 在 Python 3.9 上一导入就报错，r5.55 修了；包内验证记录写着这一组的测试在 Python 3.9.25 上也过。这一页没有在 3.9 上重跑。
- 一组 Windows 上的测试问题在 r5.25 修过，只在 Linux 上模拟 Windows 的换行和缺少 fcntl 重跑过，还没有在 Windows 上重跑。遇到问题，保留命令和完整输出，到仓库的 [Issues](https://github.com/rumpelpalmour757-lgtm/novel-workshop/issues) 提；包内说明里请你“发给维护者”的地方，也发到那里。
- 工作台：r5.59 删掉两个侧栏以后，页面上的按钮只在 Linux 上的无头 Chromium 里点过（包内验证记录），Windows、macOS 实机没有测。
- `install.py` 拒绝 Windows 的目录联接，删文件遇到只读文件时清掉只读位再试一次：这两样只在 Linux 上模拟过，没有在原生 Windows 上跑；macOS 和不分大小写的文件系统也没有跑过（r5.56）。
