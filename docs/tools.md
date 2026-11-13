# 本地工作台与检查工具

[← 返回首页](../README.md) · 适用版本 `2026-11-14-r5.54-merged-candidate`

这些都是可选的。只在聊天里写作用不到它们；除维护用的 `darwin_eval.py`（在 `skills/darwin-novel-workshop/scripts/`）外，都在完整包的 `skills/novel-workshop/` 里；便携单文件里没有可运行的脚本。完整命令见包内 `USAGE.md` 第五节和 `skills/novel-workshop/references/local-workbench.md`。

这一页讲的是工作台和脚本做什么：脚本只核对程序能核对的东西，不评价文笔。工坊整体是让 AI 照着做的方法，不是效果保证。工坊只和不用工坊的 AI 比过一次（r5.46，规模小，执行和评审都是同一类模型）：改 AI 腔重的稿子，排第一的都是不用工坊的；从头起草，工坊多数在前。之后没有再比过。对白是不是更像人、更有感情，没有验证；好不好由你读了定。

- [本地工作台](#本地工作台)
- [检查与辅助工具](#检查与辅助工具)
- [可选视觉链路](#可选视觉链路)
- [运行条件与平台限制](#运行条件与平台限制)

## 本地工作台

需要 Node.js 18 或更新版本，只用内置模块，不装依赖。用来在本机浏览、搜索、预览和（可选）编辑作品文件。工作台读写文稿不联网、不调用模型，也不是云端服务；安装技能不会自动启动它。

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

### 可选：请 Gemini 改选中的一段（r5.46）

“改稿建议”侧栏，不配置不影响任何读写。

- 自备 Gemini API Key，保存在本机用户配置目录，或用环境变量 `GEMINI_API_KEY`；密钥只在你自己的电脑上填，不要发到聊天里。
- 只发选中的文字和你的要求（一次最多 6000 字），不发文稿的其他部分、文件名和路径。
- 回来的是候选稿，侧栏标出删去和加入的地方；整段采纳、删改后采纳或放弃由你定。Gemini 不直接写任何文件。
- “已配置”只说明填了密钥，不等于能用；向 Google 的请求真的拿回候选稿，才显示“已真实接通”。
- 第一次先用合成示例试：写作台里的“用合成示例试一次”，或双击 `check-gemini.cmd`（Windows）、`check-gemini.command`（macOS），或运行 `node scripts/oh-story/gemini-check.mjs`。

### 可选：Google AI 侧栏（r5.49，只用模拟程序测过）

“Google AI”侧栏用你自己的 Google AI 订阅登录，请 Gemini 改选中的一段，回复只是候选。

- 要先自己装好 Google 的官方程序（Antigravity CLI 的 `agy`，或 ACP Registry 发行的 antigravity-acp），工坊不替你下载、安装或修改它；不需要 API Key。
- 它和上面的 Gemini API 是两条独立的路，额度不够时不会自动换到 API。
- 不开写作台也能检查：`node scripts/oh-story/acp-check.mjs --runtime "官方程序的路径"` 只查程序和握手，加 `--login --try` 才登录并发一段工坊自带的合成文字；Windows 上也可以双击 `scripts/oh-story/check-acp.cmd`。
- **目前只用工坊自己写的模拟程序测过**：和官方程序握手、真实的 Google 登录、真实调用、Windows 实机都还没有验证；订阅能不能用来写小说也没有确认。

安装、核对程序校验值、连接和登录的详细步骤，见包内 `skills/novel-workshop/references/local-workbench.md`。

## 检查与辅助工具

需要 Python 3.9 或更新版本，在 `skills/novel-workshop` 目录运行。`scripts/` 顶层有 19 个脚本（合并候选版多了 `chapter_gate.py`、`learning_loop.py`、`demonstration_memory.py` 三个），另有 `scripts/dialogue_lint/` 目录（入口 `run_lint.py`，也是合并候选版多的）和 `scripts/oh-story/` 下的几个拆文工具。脚本只给要回去读的位置，不打分，也不判断文字是不是 AI 写的；命中不等于必须改，没命中也不说明写得好。

| 脚本 | 作用 |
| --- | --- |
| `punctuation_lint.py` | 标点与断句，给出行列、规则编号和等级，只读；可带作品的标点规则文件；`--baseline` 对照原稿，只列修改后新出现的问题 |
| `prose_lint.py` | 语感扫描和分场检测（重复词、段尾否定、等长短句连排、三连排比等）；`--hint deai` 加去 AI 味的复核提示（r5.48），`--hint deai-extra` 再加四项（r5.49）；合并候选版多一个 `--hint xian`：叙述里“先”字的复核，只定位和计数，默认不开，不随 `deai` 开 |
| `dialogue_lines.py` | 台词按说话人分栏，标出书面词、叙述专用的词；`--exchanges` 按来回再列一遍（r5.53）；加 `--long-lines` 才列一口气很长的句子（r5.54）；合并候选版修了跨段认说话人的一处：上一段以“没有说：”“本想说：”这类没说出口的话收尾，下一段的引语不再算成这个人说的 |
| `detail_check.py` | `compare`：原稿里有、修订稿里没了的说法和动态补语；`changes`：逐句列出删了、加了、改了哪几句，`--keep` 核对指定要留的句子（r5.49）；`anchors`：维护时用的写作对照例 |
| `fact_guard.py` | 跨章事实主张比对、列出要回查的章节；按故事时间核人物知情（r5.51）；只核对已登记的主张 |
| `rule_register.py` | 几份规则文件互相打架时，核对冲突登记表、列出待定项、查新叫法在各章的已有用法 |
| `workflow_guard.py` | 交付门：冻结输入、审稿绑定具体版本、输出四项状态、记录你的采纳（也能照实记录跳过审稿）；核对交出去的文件是不是检查过的那一版 |
| `delivery_manifest.py` | 多章交付：核对约定章数、实际文件、漏章、空稿和旧审稿 |
| `state_precheck.py` | 项目状态保存以前，列出候选要删、要改、要加的字段，只读（r5.49） |
| `project_state.py` | 多人、多代理共用的项目状态文件，条件保存 |
| `style_cards.py` | 风格卡：列索引（`index`）、字面线索（`match`）、加载选中的卡（`load`）、查有没有照搬卡里原话（`copied`）、核对卡库和本书配置（`check`） |
| `inspiration_library.py` | 本书灵感库：核对记录、按章或按人物地方列出、出素材卡的素材块 |
| `inspiration_write.py` | 写灵感库的唯一入口：迁移旧版、记下选择、回退、看历史，写前核修订号 |
| `visual_materials_cli.py` | 可选的联网选图链路，见下文 |
| `export_portable.py` | 导出核心文件夹、单文件或安装包（`--mode personal\|sale`、`--format portable\|install`），不自动发布 |
| `workflow_demo.py` | 虚构三章演练，审稿与采纳都是模拟的，只用来熟悉流程 |
| `chapter_gate.py` | 章节门读进度（只有 `status` 一个子命令，只读）：这一章停在七个阶段的哪一步，等你确认还是等教师回传；写入走 `learning_loop.py apply`。默认不开，见[四个可选模块](modules.md#章节门) |
| `learning_loop.py` | 学习循环和章节门的记录入口：`status`、`context`、`show` 只读，`apply` 一次交一个事件（带版本的条件保存，同一事件重发不重记）；不调用模型，不写小说。见[四个可选模块](modules.md#学习循环) |
| `demonstration_memory.py` | 示范记忆的只读选择器：`check` 核结构和哈希，`index` 列编号和状态，`select` 取最多三条认可过的示范。见[四个可选模块](modules.md#示范记忆) |
| `dialogue_lint/run_lint.py` | 对白声纹与反模式检查（可选试用）：`scan` 只读扫描出报告，命中只标“复核”；`apply` 校验候选改句以后写到新文件，不覆盖原稿。见[四个可选模块](modules.md#对白声纹与反模式检查) |
| `oh-story/build_chapter_index.py` | 章节位置索引：章节范围、原文行号、字符数与内容哈希，不做文学分析 |
| `oh-story/render_relation_chart.py` | 从已有的人物关系表生成 Mermaid 关系图，可选 PNG；不自行推断人物关系 |
| `oh-story/inspect_existing_assets.py` | 只读检查已有拆文资料的覆盖情况 |
| `darwin_eval.py`（维护技能里） | 维护用：保存与汇总方法对照记录，不调用模型、不生成正文、不评分 |

Node 一侧另有两个接通检查：`gemini-check.mjs` 和 `acp-check.mjs`，见上文。

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

整包测试在交付包目录运行 `python tests/run_tests.py`。合并候选版一共 1,429 项，1,424 项通过，5 项按既有条件跳过；其中 141 项在合并新带来的 12 个测试文件里：四个模块 124 项（章节门 23、学习循环 27、示范记忆 9、对白声纹 65），台词分栏跨段认说话人的修复 5 项，`prose_lint.py --hint xian` 12 项（这 12 项放在对白声纹的测试目录里，所以那个目录一共 77 项）。包内 `MERGE-VERIFICATION.md` 记的是 Linux、Python 3.12、Node.js 24 上的结果；在 Linux、Python 3.13 上重跑过一次，数目相同。测试检查脚本行为，比如标点定位、事实比对、审稿版本绑定、回传绑错版拒收，不评价文学质量。

## 可选视觉链路

给一章找参考图：SearXNG 和 Openverse 两路搜索，Crawl4AI 读来源页，ImageHash 把近似图归组，OpenCLIP 按这一场的文字和你的参考图排序；看过图以后由你挑整张或局部，挑中的部分写进本书的灵感库。写作、审稿和灵感库的核对、列出不需要它；你自己提供图片，也可以直接按素材方法写作。

- **要装的**：Pillow（解码图片）；ImageHash；Crawl4AI（需要 Python 3.10 以上）；OpenCLIP（会带上 torch，权重另下）；SearXNG 自己跑一个实例。Openverse 不用装。工坊只带调用它们的适配器，没有它们的代码、权重和密钥。
- **配置**：照 `assets/visual-materials-config.example.json` 复制一份，填 SearXNG 地址、权重路径和哈希；密钥只放环境变量。
- **核验**：`visual_materials_cli.py doctor --probe` 逐项真调一次；跑完一次完整运行，用 `verify-run` 看这一次实际跑通了什么。五项都在同一台机器上核得上，才算接通（`ALL_FIVE_LIVE`）；差哪项就照实写哪项。
- **实际情况**：做这条链路时，制作环境里只有 ImageHash 真跑通；SearXNG 没有实例，Openverse 的请求被网络拒绝，Crawl4AI 和 OpenCLIP 没装上。在你的电脑上通不通，要自己跑一次 `doctor --probe` 和一次完整运行才知道。
- 搜索只发几个短词，不发正文；运行文件夹是这一次搜索的缓存，属于你的私人材料，删掉不影响写作。

## 运行条件与平台限制

- 检查脚本和安装脚本要 Python 3.9 或更新版本；工作台和两个接通检查要 Node.js 18 或更新版本；Crawl4AI 要 Python 3.10 以上。
- Windows 上命令写 `python` 或 `py`。交付门、标点、文字检查、台词分栏、灵感库、视觉素材、事实比对、批量清单、冲突登记表、风格卡这几个脚本按设计可以在 Windows 上运行，输出都是 UTF-8。
- `project_state.py` 使用 POSIX 文件锁，只支持 Linux、macOS 等系统，原生 Windows 不支持；依赖它的三章演练在 Windows 上会说明原因后退出。
- 四个新模块的脚本只用 Python 标准库。`learning_loop.py`（读和写）和 `chapter_gate.py status` 用的是和 `project_state.py` 同一种文件锁，原生 Windows 同样不支持；每次读写会在记录旁边留一个 `.记录文件名.lock` 的空文件。`demonstration_memory.py` 和 `dialogue_lint/run_lint.py` 不用文件锁，按写法不挑系统。四个模块都没有在 Windows 上跑过。
- `chapter_gate.py status` 和 `dialogue_lint/run_lint.py` 要按普通写法 `python3 scripts/…` 运行；加了 Python 隔离模式（`python -I`）会报 `ModuleNotFoundError`。
- `dialogue_lint/` 这一组：其中 `dialogue_core.py` 有一处类型写法要 Python 3.10 才支持，按代码推断在 3.9 上一导入就报错，没有在 3.9 上实测。用这一组脚本，稳妥起见用 Python 3.10 或更新。
- 一组 Windows 上的测试问题在 r5.25 修过，只在 Linux 上模拟 Windows 的换行和缺少 fcntl 重跑过，还没有在 Windows 上重跑。遇到问题，保留命令和完整输出，方便排查。目前没有公开的反馈渠道；包内说明里请你“发给维护者”的地方，眼下没有对外的联系方式。
- 工作台的 Google AI 侧栏在 Windows 上的启动、结束进程、中文和空格路径等都还没有实测。
