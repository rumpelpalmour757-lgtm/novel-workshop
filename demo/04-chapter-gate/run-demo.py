#!/usr/bin/env python3
"""Demo driver (written for the homepage demo, not part of the workshop package).

It only does what a person would do by hand: write one event file, run the package's own
learning_loop.py / chapter_gate.py as a separate process, and save what the process printed, byte for byte.
Nothing printed by the package scripts is edited here.

usage: run-demo.py SCRIPTS_DIR WORK_DIR DRAFT_FILE TEACHER_FILE
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

SCRIPTS, WORK, DRAFT, TEACHER = (Path(p).resolve() for p in sys.argv[1:5])
PY = [sys.executable, "-I", "-B"]
# Under -I the script's own folder is not on the import path, and chapter_gate.py's status command imports its
# sibling learning_loop. This one-liner puts the folder back and runs the unchanged script.
STATUS_SHIM = ('import sys,runpy; d=sys.argv[1]; sys.path.insert(0,d); '
               'sys.argv=[d+"/chapter_gate.py"]+sys.argv[2:]; runpy.run_path(sys.argv[0],run_name="__main__")')
SYNTHETIC = "合成演示：这句不是真人作者说的，只用来让脚本走到下一步"
STORE_TEMPLATE = """# 学习与章节确认记录（合成演示项目）

这份记录只属于演示用的合成小项目“渡口售票窗”。里面的“作者原话”都是为演示写的，不是任何真人作者的确认。

<!-- NOVEL_WORKSHOP_LEARNING_START -->
```json
{"schema_version":1,"project_id":"%s","revision":0,"data":{}}
```
<!-- NOVEL_WORKSHOP_LEARNING_END -->
"""


class Walk:
    def __init__(self, folder, project):
        self.dir = WORK / folder
        (self.dir / "events").mkdir(parents=True, exist_ok=True)
        (self.dir / "outputs").mkdir(exist_ok=True)
        self.project = project
        self.store = self.dir / "learning-record.md"
        self.store.write_text(STORE_TEMPLATE % project, encoding="utf-8")
        (self.dir / "learning-record.initial.md").write_text(STORE_TEMPLATE % project, encoding="utf-8")
        self.transcript = []
        self.step = 0
        self.version = None

    def run(self, name, shown, argv):
        done = subprocess.run(argv, cwd=self.dir, capture_output=True)
        out = done.stdout.decode("utf-8") + done.stderr.decode("utf-8")
        (self.dir / "outputs" / ("%02d-%s.txt" % (self.step, name))).write_bytes(done.stdout + done.stderr)
        self.transcript.append("$ %s\n%s[退出码 %d]\n" % (shown, out if out.endswith("\n") or not out else out + "\n",
                                                        done.returncode))
        self.step += 1
        try:
            return done.returncode, json.loads(done.stdout.decode("utf-8") or done.stderr.decode("utf-8"))
        except ValueError:
            return done.returncode, {}

    def loop_status(self):
        code, result = self.run("status", 'python3 -I -B "$NW_SCRIPTS/learning_loop.py" status learning-record.md',
                                PY + [str(SCRIPTS / "learning_loop.py"), "status", "learning-record.md"])
        self.version = result["version"]
        return result

    def gate_status(self, chapter, label="gate-status"):
        return self.run(label, "python3 -I -B -c '%s' \"$NW_SCRIPTS\" status learning-record.md --chapter-id %s"
                        % (STATUS_SHIM, chapter),
                        PY + ["-c", STATUS_SHIM, str(SCRIPTS), "status", "learning-record.md", "--chapter-id", chapter])[1]

    def apply(self, name, event):
        path = "events/%02d-%s.json" % (self.step, name)
        (self.dir / path).write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        code, result = self.run(name, 'python3 -I -B "$NW_SCRIPTS/learning_loop.py" apply learning-record.md %s '
                                "--project-id %s --if-version '%s'" % (path, self.project, self.version),
                                PY + [str(SCRIPTS / "learning_loop.py"), "apply", "learning-record.md", path,
                                      "--project-id", self.project, "--if-version", self.version])
        if code == 0:
            self.version = result["version"]
        return code, result

    def gate(self, name, action, chapter=None, stage=None, **fields):
        event = {"event_id": "demo-%02d-%s" % (self.step, name), "op": "chapter_gate", "action": action}
        if chapter:
            event["chapter_id"] = chapter
        if stage:
            event["stage"] = stage
        event.update(fields)
        return self.apply(name, event) + (event["event_id"],)

    def confirm(self, name, chapter, stage, presented, quote):
        return self.gate(name, "confirm", chapter, stage, presentation_id=presented["presentation_id"],
                         presentation_version=presented["presentation_version"], actor_role="author", mode="human",
                         author_quote="（合成演示）" + quote, source_ref=SYNTHETIC)

    def save(self):
        (self.dir / "transcript.txt").write_text("\n".join(self.transcript), encoding="utf-8")


SCOPE = ("【合成演示】本章范围：一场，渡口售票窗，末班船开前十分钟。人物：老郝（售票员）、丁穗（新来第三天的售票员）、"
         "冯姐（常坐船的乘客）。篇幅：三百字以内。不改的事实：价目表上活禽按行李算，一只一块。前章：无（演示项目只有这一章）。"
         "材料缺口：没有口吻表，没有作者样本，没有设定档。")
OUTLINE = ("【合成演示】一场四拍。一，老郝教丁穗撕票；二，冯姐带一只活鸡买票，老郝报两块；三，丁穗翻价目表，说表上是一块；"
           "四，老郝不接话，冯姐付一块，票推出去。谁在乎什么：丁穗在乎头几天别出错，老郝在乎在新人面前的面子。"
           "事后一拍：无。章尾：停在票推出去、鸡扑腾一下。")
PREPARATION = ("【合成演示】节拍卡：上面四拍。声音：老郝惜字，丁穗照章说话，冯姐嘴快。风格卡：不加载。"
               "本轮必查：谁在说（台词分栏）、标点。不适用：口吻表（没有）。")


def main_walk():
    walk = Walk("chapter-gate", "demo-ferry-booth")
    draft_bytes, teacher_bytes = DRAFT.read_bytes(), TEACHER.read_bytes()
    draft_sha, teacher_sha = hashlib.sha256(draft_bytes).hexdigest(), hashlib.sha256(teacher_bytes).hexdigest()
    walk.loop_status()
    walk.gate("configure", "configure", visual_required=False, teacher_handoff="user_return", actor_role="author",
              mode="human", author_quote="（合成演示）新章一关一关给我看，我点头了再往下；初稿我自己交给教师，结果由我带回来。",
              source_ref=SYNTHETIC)
    walk.gate_status("ch01", "gate-status-not-started")
    _, scope, _ = walk.gate("present-scope", "present", "ch01", "scope", content=SCOPE,
                            source_ref="demo/04-chapter-gate（合成的本章范围）")
    walk.gate("skip-to-draft-rejected", "present", "ch01", "draft", content=draft_bytes.decode("utf-8"),
              source_ref="demo/05-teacher-review/draft.md（合成稿）", artifact_sha256=draft_sha)
    walk.confirm("confirm-scope", "ch01", "scope", scope, "范围可以。")
    _, outline, _ = walk.gate("present-outline", "present", "ch01", "outline", content=OUTLINE,
                              source_ref="demo/04-chapter-gate（合成的章纲）")
    walk.confirm("confirm-outline", "ch01", "outline", outline, "章纲可以，照这个准备。")
    _, preparation, _ = walk.gate("present-preparation", "present", "ch01", "preparation", content=PREPARATION,
                                  source_ref="demo/04-chapter-gate（合成的写前准备）")
    walk.confirm("confirm-preparation", "ch01", "preparation", preparation, "准备可以，写初稿。")
    _, draft, _ = walk.gate("present-draft", "present", "ch01", "draft", content=draft_bytes.decode("utf-8"),
                            source_ref="demo/05-teacher-review/draft.md（合成稿）", artifact_sha256=draft_sha)
    walk.gate_status("ch01", "gate-status-at-draft")
    # ---- past the draft stage: the handoff to the teacher and the return ----
    walk.confirm("confirm-draft", "ch01", "draft", draft, "初稿我拿去给教师看。")
    binding = {"draft_presentation_id": draft["presentation_id"],
               "draft_presentation_version": draft["presentation_version"],
               "returned_text": teacher_bytes.decode("utf-8"),
               "source_ref": "demo/05-teacher-review/teacher-revision.md（合成的教师改稿）",
               "teacher_name": "合成教师（演示用，不是真人或真实模型的回传）"}
    walk.gate("teacher-return-wrong-hash-rejected", "teacher_return", "ch01", draft_sha256=teacher_sha, **binding)
    walk.gate("teacher-return", "teacher_return", "ch01", draft_sha256=draft_sha, **binding)
    walk.gate_status("ch01", "gate-status-after-teacher-return")
    walk.save()


def visual_walk():
    walk = Walk("chapter-gate-visual", "demo-visual-required")
    walk.loop_status()
    walk.gate("configure", "configure", visual_required=True, teacher_handoff="user_return", actor_role="author",
              mode="human", author_quote="（合成演示）每章写前都要有视觉材料；初稿我自己交给教师。", source_ref=SYNTHETIC)
    _, scope, _ = walk.gate("present-scope", "present", "ch01", "scope", content=SCOPE,
                            source_ref="demo/04-chapter-gate（合成的本章范围）")
    walk.confirm("confirm-scope", "ch01", "scope", scope, "范围可以。")
    _, outline, _ = walk.gate("present-outline", "present", "ch01", "outline", content=OUTLINE,
                              source_ref="demo/04-chapter-gate（合成的章纲）")
    walk.confirm("confirm-outline", "ch01", "outline", outline, "章纲可以，照这个准备。")
    walk.gate("present-preparation-without-visual-rejected", "present", "ch01", "preparation", content=PREPARATION,
              source_ref="demo/04-chapter-gate（合成的写前准备，没有视觉材料）")
    walk.gate_status("ch01", "gate-status-still-at-preparation")
    walk.save()


if __name__ == "__main__":
    main_walk()
    visual_walk()
