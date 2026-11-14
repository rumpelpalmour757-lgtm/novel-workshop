#!/usr/bin/env python3
"""Demo driver for docs/modules.md (written for the homepage, not part of the workshop package).

It only does what a person would do by hand: write one event file or config, run the package's own
learning_loop.py, chapter_gate.py, demonstration_memory.py or dialogue_lint/run_lint.py as a separate
process, and save what the process printed, byte for byte. Nothing printed by the package scripts is
edited here. The last part is the one exception: it calls the final-stage wording check inside
chapter_gate.py directly, to show which sentences it records and which it leaves pending.

Every text in here is synthetic and was written for the demo: a bike-repair stall at the mouth of a
lane, two people (老秦, 阿梨). The "author's words" are not any real author's.

usage: run-demo.py SCRIPTS_DIR WORK_DIR
SCRIPTS_DIR is skills/novel-workshop/scripts of the unpacked package; WORK_DIR should be empty.
Writes every command and its exact output to WORK_DIR/<part>/transcript.txt and outputs/.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

SCRIPTS, WORK = (Path(p).resolve() for p in sys.argv[1:3])
PY = [sys.executable, "-I", "-B"]
SYN = "合成演示：这句不是真人作者说的，只用来让脚本走到下一步"
START = "<!-- NOVEL_WORKSHOP_LEARNING_START -->"
END = "<!-- NOVEL_WORKSHOP_LEARNING_END -->"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Part:
    def __init__(self, name):
        self.dir = WORK / name
        (self.dir / "events").mkdir(parents=True, exist_ok=True)
        (self.dir / "outputs").mkdir(exist_ok=True)
        self.log = []
        self.n = 0

    def run(self, label, argv, shown):
        done = subprocess.run(argv, cwd=self.dir, capture_output=True)
        out = (done.stdout + done.stderr).decode("utf-8")
        self.n += 1
        (self.dir / "outputs" / ("%02d-%s.txt" % (self.n, label))).write_text(out, encoding="utf-8")
        self.log.append("### %02d %s\n$ %s\n%s[exit %d]\n" % (self.n, label, shown, out, done.returncode))
        try:
            return done.returncode, json.loads(done.stdout.decode("utf-8") or "{}")
        except ValueError:
            return done.returncode, {}

    def save(self):
        (self.dir / "transcript.txt").write_text("\n".join(self.log), encoding="utf-8")


class Store(Part):
    def __init__(self, name, record, project, data):
        super().__init__(name)
        self.record = record
        self.project = project
        path = self.dir / record
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": 1, "project_id": project, "revision": 0, "data": data}
        path.write_text(START + "\n```json\n" + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
                        + "\n```\n" + END + "\n", encoding="utf-8")
        self.version = None

    def status(self):
        code, res = self.run("loop-status", PY + [str(SCRIPTS / "learning_loop.py"), "status", self.record],
                             "learning_loop.py status " + self.record)
        self.version = res.get("version")
        return res

    def gate_status(self, chapter):
        return self.run("gate-status", PY + [str(SCRIPTS / "chapter_gate.py"), "status", self.record,
                                             "--chapter-id", chapter],
                        "chapter_gate.py status %s --chapter-id %s" % (self.record, chapter))[1]

    def apply(self, label, event, version=None):
        rel = "events/%02d-%s.json" % (self.n + 1, label)
        (self.dir / rel).write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        use = version or self.version
        code, res = self.run(label, PY + [str(SCRIPTS / "learning_loop.py"), "apply", self.record, rel,
                                          "--project-id", self.project, "--if-version", use],
                             "learning_loop.py apply %s %s --project-id %s --if-version %s"
                             % (self.record, rel, self.project, use))
        if code == 0 and res.get("version"):
            self.version = res["version"]
        return code, res


# ---------------------------------------------------------------- chapter gate
def gate():
    s = Store("gate", "项目/learning-record.md", "demo-bike-stall", {})
    s.status()
    scope_event = {
        "event_id": "ch01-01-present-scope", "op": "chapter_gate", "action": "present",
        "chapter_id": "ch01", "stage": "scope",
        "content": "【合成演示】本章范围：一场，巷口修车摊，傍晚收摊前。人物：老秦（修车的，话少）、阿梨（来补胎的学生）。"
                   "篇幅：两百字以内。不改的事实：补两处三块。材料缺口：没有前章，没有口吻表。",
        "source_ref": "合成演示：为这一页新写的本章范围"}
    _, scope = s.apply("present-scope", scope_event)
    s.gate_status("ch01")
    before_confirm = s.version
    confirm = {"event_id": "ch01-02-confirm-scope", "op": "chapter_gate", "action": "confirm",
               "chapter_id": "ch01", "stage": "scope", "presentation_id": scope["presentation_id"],
               "presentation_version": scope["presentation_version"], "actor_role": "author", "mode": "human",
               "author_quote": "（合成演示）继续。", "source_ref": SYN}
    s.apply("confirm-scope", confirm)
    # trials
    s.apply("trial-skip-to-draft", {"event_id": "ch01-t1-draft", "op": "chapter_gate", "action": "present",
                                    "chapter_id": "ch01", "stage": "draft", "content": "跳过的初稿",
                                    "source_ref": "合成演示", "artifact_sha256": sha("跳过的初稿")})
    s.apply("trial-stale-version", {"event_id": "ch01-t2-outline", "op": "chapter_gate", "action": "present",
                                    "chapter_id": "ch01", "stage": "outline", "content": "旧版本上的章纲",
                                    "source_ref": "合成演示"}, version=before_confirm)
    s.apply("trial-resend-confirm", confirm)
    _, outline = s.apply("present-outline", {
        "event_id": "ch01-03-present-outline", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "outline", "content": "【合成演示】一场三拍：阿梨推车来补胎；老秦报两处三块；阿梨说后胎也瘪，老秦说打气就行。",
        "source_ref": "合成演示：章节方案"})
    s.apply("confirm-outline", {"event_id": "ch01-04-confirm-outline", "op": "chapter_gate", "action": "confirm",
                                "chapter_id": "ch01", "stage": "outline", "presentation_id": outline["presentation_id"],
                                "presentation_version": outline["presentation_version"], "actor_role": "author",
                                "mode": "human", "author_quote": "（合成演示）方案可以。", "source_ref": SYN})
    prep = "【合成演示】节拍卡三拍；声音：老秦话少，报数不解释；阿梨说话直。"
    s.apply("trial-preparation-without-visual", {
        "event_id": "ch01-t4-prep", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "preparation", "content": prep, "source_ref": "合成演示：写前准备"})
    _, preparation = s.apply("present-preparation", {
        "event_id": "ch01-05-present-preparation", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "preparation", "content": prep, "source_ref": "合成演示：写前准备",
        "visual_evidence": {"mode": "author_images", "source_refs": ["合成演示：没有真的图，只是字段"],
                            "observation_ref": "合成演示：看图记录（没有真的看图）",
                            "selection_ref": "合成演示：作者的选择（合成）"}})
    s.apply("confirm-preparation", {
        "event_id": "ch01-06-confirm-preparation", "op": "chapter_gate", "action": "confirm", "chapter_id": "ch01",
        "stage": "preparation", "presentation_id": preparation["presentation_id"],
        "presentation_version": preparation["presentation_version"], "actor_role": "author", "mode": "human",
        "author_quote": "（合成演示）准备可以，写吧。", "source_ref": SYN})
    d1 = "（合成初稿第一版）阿梨推车来补胎。老秦说：“两处，三块。”\n"
    _, draft = s.apply("present-draft", {
        "event_id": "ch01-07-present-draft", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "draft", "content": d1, "source_ref": "合成演示：初稿第一版", "artifact_sha256": sha(d1)})
    s.apply("confirm-draft", {
        "event_id": "ch01-08-confirm-draft", "op": "chapter_gate", "action": "confirm", "chapter_id": "ch01",
        "stage": "draft", "presentation_id": draft["presentation_id"],
        "presentation_version": draft["presentation_version"], "actor_role": "author", "mode": "human",
        "author_quote": "（合成演示）初稿我拿去给教师。", "source_ref": SYN})
    s.gate_status("ch01")
    s.apply("trial-review-without-return", {
        "event_id": "ch01-t5-review", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "review", "content": "没有回传的审稿方案", "source_ref": "合成演示"})
    teacher = "（合成教师改稿）阿梨推车来补胎。老秦说：“两处破了，三块钱。”\n"
    bind = {"draft_presentation_id": draft["presentation_id"],
            "draft_presentation_version": draft["presentation_version"], "returned_text": teacher,
            "source_ref": "合成演示：教师改稿（不是真人回传）", "teacher_name": "合成教师（演示用）"}
    s.apply("trial-return-wrong-hash", {"event_id": "ch01-t6-return", "op": "chapter_gate",
                                        "action": "teacher_return", "chapter_id": "ch01",
                                        "draft_sha256": sha(teacher), **bind})
    _, ret1 = s.apply("teacher-return", {"event_id": "ch01-09-teacher-return", "op": "chapter_gate",
                                         "action": "teacher_return", "chapter_id": "ch01",
                                         "draft_sha256": sha(d1), **bind})
    s.apply("reopen-draft", {"event_id": "ch01-10-reopen-draft", "op": "chapter_gate", "action": "reopen",
                             "chapter_id": "ch01", "stage": "draft", "reason": "合成演示：作者要换一版初稿",
                             "author_quote": "（合成演示）初稿我自己改了一句，换这一版。", "source_ref": SYN})
    d2 = "（合成初稿第二版）阿梨推车来补胎。老秦看了一眼，说：“两处，三块。”\n"
    _, draft2 = s.apply("present-draft-v2", {
        "event_id": "ch01-11-present-draft-v2", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "draft", "content": d2, "source_ref": "合成演示：初稿第二版", "artifact_sha256": sha(d2)})
    s.apply("confirm-draft-v2", {
        "event_id": "ch01-12-confirm-draft-v2", "op": "chapter_gate", "action": "confirm", "chapter_id": "ch01",
        "stage": "draft", "presentation_id": draft2["presentation_id"],
        "presentation_version": draft2["presentation_version"], "actor_role": "author", "mode": "human",
        "author_quote": "（合成演示）这一版拿去给教师。", "source_ref": SYN})
    s.apply("trial-review-with-old-return", {
        "event_id": "ch01-t7-review", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "review", "content": "拿旧回传做的方案", "source_ref": "合成演示",
        "teacher_return_id": ret1.get("teacher_return_id", "ch01-09-teacher-return")})
    bind2 = dict(bind, draft_presentation_id=draft2["presentation_id"],
                 draft_presentation_version=draft2["presentation_version"],
                 returned_text="（合成教师改稿，对第二版）阿梨推车来补胎。老秦看了一眼，说：“两处破了，三块钱。”\n")
    _, ret2 = s.apply("teacher-return-v2", {"event_id": "ch01-13-teacher-return-v2", "op": "chapter_gate",
                                            "action": "teacher_return", "chapter_id": "ch01",
                                            "draft_sha256": sha(d2), **bind2})
    _, review = s.apply("present-review", {
        "event_id": "ch01-14-present-review", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "review", "content": "【合成演示】审稿方案：教师把“三块”改成“三块钱”，拟拒绝，老秦惜字。",
        "source_ref": "合成演示：审稿方案", "teacher_return_id": ret2.get("teacher_return_id")})
    s.apply("confirm-review", {
        "event_id": "ch01-15-confirm-review", "op": "chapter_gate", "action": "confirm", "chapter_id": "ch01",
        "stage": "review", "presentation_id": review["presentation_id"],
        "presentation_version": review["presentation_version"], "actor_role": "author", "mode": "human",
        "author_quote": "（合成演示）方案照这个改。", "source_ref": SYN})
    rv = "（合成修订稿）阿梨推车来补胎。老秦看了一眼，说：“两处，三块。”阿梨把钱放在工具箱上。\n"
    _, revision = s.apply("present-revision", {
        "event_id": "ch01-16-present-revision", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "revision", "content": rv, "source_ref": "合成演示：修订稿", "artifact_sha256": sha(rv)})
    s.apply("confirm-revision", {
        "event_id": "ch01-17-confirm-revision", "op": "chapter_gate", "action": "confirm", "chapter_id": "ch01",
        "stage": "revision", "presentation_id": revision["presentation_id"],
        "presentation_version": revision["presentation_version"], "actor_role": "author", "mode": "human",
        "author_quote": "（合成演示）修订稿可以，交定稿。", "source_ref": SYN})
    s.apply("trial-final-wrong-artifact", {
        "event_id": "ch01-t8-final", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "final", "content": d2, "source_ref": "合成演示", "artifact_sha256": sha(d2)})
    _, final = s.apply("present-final", {
        "event_id": "ch01-18-present-final", "op": "chapter_gate", "action": "present", "chapter_id": "ch01",
        "stage": "final", "content": "【合成演示】定稿记录：当前候选稿是修订稿。", "source_ref": "合成演示：定稿记录",
        "artifact_sha256": sha(rv)})
    fbase = {"op": "chapter_gate", "action": "confirm", "chapter_id": "ch01", "stage": "final",
             "presentation_id": final["presentation_id"], "presentation_version": final["presentation_version"],
             "actor_role": "author", "mode": "human", "source_ref": SYN}
    trials = [("final-continue", "（合成演示）继续。", True), ("final-not-yet", "（合成演示）先不采纳，我再看看。", True),
              ("final-labelled-accept", "（合成演示）采纳这一版。", True), ("final-jiu-zhe-ban", "就这版吧。", True),
              ("final-later", "下午再定稿。", True), ("final-no-decision", "采纳这一版。", False)]
    for i, (label, quote, with_decision) in enumerate(trials):
        event = dict(fbase, event_id="ch01-t9-%d" % i, author_quote=quote)
        if with_decision:
            event["decision"] = "accept_final_version"
        s.apply("trial-" + label, event)
    s.apply("confirm-final", dict(fbase, event_id="ch01-19-confirm-final", author_quote="采纳这一版。",
                                  decision="accept_final_version",
                                  source_ref="合成演示：这句不是真人作者说的；最后一关的原话带了“（合成演示）”字样脚本就不认，所以只在出处一栏标明"))
    s.gate_status("ch01")
    s.apply("trial-configure-with-chapter", {"event_id": "cfg-t-chapter", "op": "chapter_gate", "action": "configure",
                                             "chapter_id": "ch02", "visual_required": False,
                                             "teacher_handoff": "user_return", "actor_role": "author",
                                             "mode": "human", "author_quote": "（合成演示）这一章不看图。",
                                             "source_ref": SYN})
    s.apply("chapter-policy-ch02", {"event_id": "ch02-01-policy", "op": "chapter_gate", "action": "chapter_policy",
                                    "chapter_id": "ch02", "visual_required": False, "actor_role": "author",
                                    "mode": "human", "author_quote": "（合成演示）第二章不用看图。",
                                    "source_ref": SYN})
    _, sc2 = s.apply("ch02-present-scope", {"event_id": "ch02-02-present-scope", "op": "chapter_gate",
                                            "action": "present", "chapter_id": "ch02", "stage": "scope",
                                            "content": "【合成演示】第二章范围。", "source_ref": "合成演示"})
    s.apply("ch02-confirm-scope", {"event_id": "ch02-03-confirm-scope", "op": "chapter_gate", "action": "confirm",
                                   "chapter_id": "ch02", "stage": "scope", "presentation_id": sc2["presentation_id"],
                                   "presentation_version": sc2["presentation_version"], "actor_role": "author",
                                   "mode": "human", "author_quote": "（合成演示）第二章范围可以。", "source_ref": SYN})
    _, ol2 = s.apply("ch02-present-outline", {"event_id": "ch02-04-present-outline", "op": "chapter_gate",
                                              "action": "present", "chapter_id": "ch02", "stage": "outline",
                                              "content": "【合成演示】第二章方案。", "source_ref": "合成演示"})
    s.apply("ch02-confirm-outline", {"event_id": "ch02-05-confirm-outline", "op": "chapter_gate",
                                     "action": "confirm", "chapter_id": "ch02", "stage": "outline",
                                     "presentation_id": ol2["presentation_id"],
                                     "presentation_version": ol2["presentation_version"], "actor_role": "author",
                                     "mode": "human", "author_quote": "（合成演示）第二章方案可以。", "source_ref": SYN})
    s.apply("ch02-preparation-without-visual", {"event_id": "ch02-06-present-preparation", "op": "chapter_gate",
                                                "action": "present", "chapter_id": "ch02", "stage": "preparation",
                                                "content": "【合成演示】第二章写前准备，不看图。",
                                                "source_ref": "合成演示"})
    s.gate_status("ch02")
    s.save()


# ---------------------------------------------------------------- learning loop
DRAFT = """巷口的修车摊快收了，老秦把打气筒靠到墙根。

阿梨推着车过来，问：“还能补吗？”

老秦看了一眼车胎，说：“能。”

他把内胎按进水盆，冒出两串气泡。老秦说：“两处，三块。”

阿梨说：“行。”她捏了捏后轮。阿梨说：“我注意到后胎也有点瘪。”

老秦把内胎捞出来，甩了甩水，说：“打点气就行。”
"""
REVISED = DRAFT.replace("我注意到后胎也有点瘪。", "后胎好像也有点瘪。")


def loop():
    data = {"demonstration_learning": {"enabled": True, "loop_enabled": False, "max_revisions": 2},
            "demonstrations": {}, "learning_runs": {}, "learning_events": {}}
    s = Store("loop", "项目/learning-record.md", "demo-bike-stall", data)
    (s.dir / "项目/ch01-初稿.txt").write_text(DRAFT, encoding="utf-8")
    s.status()
    run = "run-ch01-dialogue"
    start = {"event_id": "loop-03-start", "op": "start", "run_id": run, "task": "dialogue_revision",
             "tags": ["对白", "书面腔"], "group_id": "ch01-修车摊", "input_text": DRAFT,
             "source_ref": "合成演示：为这一页新写的修车摊初稿", "constraints": ["不改补胎的价钱", "老秦话少"]}
    s.apply("trial-start-while-disabled", dict(start, event_id="loop-01-start"))
    # No work profile sets a number of rounds here, so the workshop's default of three is configured
    # before the run starts (references/learning-loop.md, "返工次数"); unconfigured, the script allows two.
    s.apply("configure", {"event_id": "loop-02-configure", "op": "configure", "loop_enabled": True,
                          "max_revisions": 3})
    s.run("context", PY + [str(SCRIPTS / "learning_loop.py"), "context", s.record, "--project-id", "demo-bike-stall",
                           "--task", "dialogue_revision", "--exclude-group", "ch01-修车摊"],
          "learning_loop.py context %s --project-id demo-bike-stall --task dialogue_revision --exclude-group ch01-修车摊"
          % s.record)
    s.apply("start", start)
    s.apply("plan", {"event_id": "loop-04-plan", "op": "plan", "run_id": run, "applications": [],
                     "checks": ["台词像不像这个人", "价钱不变"]})
    s.apply("draft", {"event_id": "loop-05-draft", "op": "draft", "run_id": run, "text": DRAFT,
                      "source_ref": "合成演示：初稿原样登记", "actor": {"name": "合成写作者", "context_id": "writer-1"}})
    findings = [{"id": "f1", "issue": "“我注意到”是书面说法，不像学生随口说的", "evidence": "我注意到后胎也有点瘪。",
                 "scope": "第 9 行"},
                {"id": "f2", "issue": "老秦该说一句为什么打气就行", "evidence": "打点气就行。", "scope": "第 11 行"}]
    review = {"event_id": "loop-07-review", "op": "review", "run_id": run, "review_id": "r1-teacher",
              "draft_sha256": sha(DRAFT),
              "reviewer": {"name": "合成教师", "role": "teacher", "mode": "author_return", "context_id": "teacher-1"},
              "verdict": "revise", "findings": findings, "source_ref": "合成演示：教师意见（不是真人回传）"}
    s.apply("trial-review-wrong-hash", dict(review, event_id="loop-06-review", draft_sha256=sha(REVISED)))
    s.apply("review", review)
    revise = {"event_id": "loop-10-revise", "op": "revise", "run_id": run, "parent_sha256": sha(DRAFT),
              "text": REVISED, "source_ref": "合成演示：第二版", "review_id": "r1-teacher",
              "actor": {"name": "合成写作者", "context_id": "writer-1"}}
    s.apply("trial-revise-before-decide", dict(revise, event_id="loop-08-revise"))
    s.apply("decide", {"event_id": "loop-09-decide", "op": "decide", "run_id": run, "review_id": "r1-teacher",
                       "decisions": [
                           {"finding_id": "f1", "decision": "adopt",
                            "reason": "问题成立：“我注意到”是书面说法。改法不照抄，换成她会说的话，信息不增不减。"},
                           {"finding_id": "f2", "decision": "decline",
                            "reason": "老秦话少是这一场定下的口气；补原因会带出初稿里没有的判断。"}]})
    s.apply("revise", revise)
    s.apply("trial-finish-before-recheck", {"event_id": "loop-11-finish", "op": "finish", "run_id": run,
                                            "draft_sha256": sha(REVISED)})
    recheck = {"event_id": "loop-13-review", "op": "review", "run_id": run, "review_id": "r2-self",
               "draft_sha256": sha(REVISED),
               "reviewer": {"name": "合成写作者", "role": "writer", "mode": "self_check", "context_id": "writer-1"},
               "verdict": "pass", "findings": [], "source_ref": "合成演示：工坊自查", "rechecks": ["r1-teacher"]}
    s.apply("trial-selfcheck-as-teacher", dict(recheck, event_id="loop-12-review",
                                               reviewer=dict(recheck["reviewer"], role="teacher")))
    s.apply("recheck", recheck)
    s.apply("finish", {"event_id": "loop-14-finish", "op": "finish", "run_id": run, "draft_sha256": sha(REVISED)})
    acc = {"op": "author_accept", "run_id": run, "draft_sha256": sha(REVISED), "actor_role": "author",
           "mode": "human", "source_ref": SYN}
    s.apply("trial-accept-labelled", dict(acc, event_id="loop-15a-author_accept",
                                          quote="（合成演示）这一处改法我认，记下来。"))
    s.apply("trial-accept-continue", dict(acc, event_id="loop-15b-author_accept", quote="继续。"))
    s.apply("author-accept", dict(acc, event_id="loop-15-author_accept", quote="采纳当前稿。",
                                  source_ref="合成演示：这句不是真人作者说的；原话带了“（合成演示）”字样脚本就不认，所以只在出处一栏标明"))
    s.apply("learn", {"event_id": "loop-16-learn", "op": "learn", "run_id": run, "case_id": "case-书面腔-01",
                      "why": "台词里的“我注意到……”是汇报口气；换成说话人会用的说法，办的事和给的信息不变。",
                      "when": ["台词里出现“我注意到”“我意识到”这类汇报式开头", "说话人是随口说话的普通人"],
                      "except": ["人物在做正式汇报或读记录"],
                      "decisions": ["只换这一句的措辞", "补原因的建议不采纳：会带出原稿没有的判断"]})
    mem0 = [str(SCRIPTS / "demonstration_memory.py")]
    s.run("mem-check-first", PY + mem0 + ["check", s.record], "demonstration_memory.py check " + s.record)
    s.run("mem-index-first", PY + mem0 + ["index", s.record, "--project-id", "demo-bike-stall", "--task",
                                          "dialogue_revision"],
          "demonstration_memory.py index %s --project-id demo-bike-stall --task dialogue_revision" % s.record)
    s.run("mem-select-first", PY + mem0 + ["select", s.record, "--project-id", "demo-bike-stall", "--task",
                                           "dialogue_revision", "--limit", "3"],
          "demonstration_memory.py select %s --project-id demo-bike-stall --task dialogue_revision --limit 3" % s.record)
    s.run("show-brief", PY + [str(SCRIPTS / "learning_loop.py"), "show", s.record, "--run-id", run, "--brief"],
          "learning_loop.py show %s --run-id %s --brief" % (s.record, run))
    # two more rounds: self-check only -> candidate; teacher pass on new text -> teacher_approved
    for run3, mode, lead in (("run-self-only", "self", "收得早"), ("run-teacher-pass", "teacher", "还没收")):
        text = DRAFT.replace("快收了", lead)
        newer = text.replace("我注意到后胎也有点瘪。", "后胎好像也有点瘪。")
        s.apply(run3 + "-start", dict(start, event_id=run3 + "-01", run_id=run3, group_id="grp-" + run3,
                                      tags=["对白"], case_ids=[], input_text=text))
        s.apply(run3 + "-plan", {"event_id": run3 + "-02", "op": "plan", "run_id": run3, "applications": [],
                                 "checks": ["口气"]})
        s.apply(run3 + "-draft", {"event_id": run3 + "-03", "op": "draft", "run_id": run3, "text": text,
                                  "source_ref": "合成演示", "actor": {"name": "合成写作者", "context_id": "writer-1"}})
        if mode == "self":
            s.apply(run3 + "-review", {"event_id": run3 + "-04", "op": "review", "run_id": run3, "review_id": "s1",
                                       "draft_sha256": sha(text),
                                       "reviewer": {"name": "合成写作者", "role": "writer", "mode": "self_check",
                                                    "context_id": "writer-1"},
                                       "verdict": "pass", "findings": [], "source_ref": "合成演示"})
            final_text = text
        else:
            s.apply(run3 + "-review", {"event_id": run3 + "-04", "op": "review", "run_id": run3, "review_id": "t1",
                                       "draft_sha256": sha(text),
                                       "reviewer": {"name": "合成教师", "role": "teacher", "mode": "independent_agent",
                                                    "context_id": "teacher-2"},
                                       "verdict": "revise", "findings": findings[:1], "source_ref": "合成演示"})
            s.apply(run3 + "-decide", {"event_id": run3 + "-05", "op": "decide", "run_id": run3, "review_id": "t1",
                                       "decisions": [{"finding_id": "f1", "decision": "adopt", "reason": "成立"}]})
            s.apply(run3 + "-revise", {"event_id": run3 + "-06", "op": "revise", "run_id": run3,
                                       "parent_sha256": sha(text), "text": newer, "source_ref": "合成演示",
                                       "review_id": "t1", "actor": {"name": "合成写作者", "context_id": "writer-1"}})
            s.apply(run3 + "-recheck", {"event_id": run3 + "-07", "op": "review", "run_id": run3, "review_id": "t2",
                                        "draft_sha256": sha(newer),
                                        "reviewer": {"name": "合成教师", "role": "teacher", "mode": "independent_agent",
                                                     "context_id": "teacher-2"},
                                        "verdict": "pass", "findings": [], "source_ref": "合成演示",
                                        "rechecks": ["t1"]})
            final_text = newer
        s.apply(run3 + "-finish", {"event_id": run3 + "-08", "op": "finish", "run_id": run3,
                                   "draft_sha256": sha(final_text)})
        s.apply(run3 + "-learn", {"event_id": run3 + "-09", "op": "learn", "run_id": run3, "case_id": "case-" + run3,
                                  "why": "合成演示", "when": ["合成演示"], "except": [], "decisions": ["合成演示"]})
    # the author's objection cannot be declined by the workshop
    run2 = "run-author-no"
    an = DRAFT.replace("快收了", "要收了")
    s.apply("a-start", dict(start, event_id="no-01-start", run_id=run2, group_id="ch01-修车摊-另一稿", case_ids=[],
                            input_text=an))
    s.apply("a-plan", {"event_id": "no-02-plan", "op": "plan", "run_id": run2, "applications": [], "checks": ["口气"]})
    s.apply("a-draft", {"event_id": "no-03-draft", "op": "draft", "run_id": run2, "text": an,
                        "source_ref": "合成演示", "actor": {"name": "合成写作者", "context_id": "writer-1"}})
    s.apply("a-author-review", {"event_id": "no-04-review", "op": "review", "run_id": run2, "review_id": "r1-author",
                                "draft_sha256": sha(an),
                                "reviewer": {"name": "作者（合成）", "role": "author", "mode": "human",
                                             "context_id": "author-1"},
                                "verdict": "revise",
                                "findings": [{"id": "f1", "issue": "（合成演示）阿梨这句不像她", "evidence": "我注意到后胎也有点瘪。",
                                              "scope": "第 9 行"}],
                                "source_ref": SYN})
    s.apply("trial-decline-author", {"event_id": "no-05-decide", "op": "decide", "run_id": run2,
                                     "review_id": "r1-author",
                                     "decisions": [{"finding_id": "f1", "decision": "decline",
                                                    "reason": "工坊觉得这句可以留"}]})
    s.apply("trial-accept-over-objection", {"event_id": "no-06-accept", "op": "author_accept", "run_id": run2,
                                            "draft_sha256": sha(an), "quote": "采纳当前稿。", "actor_role": "author",
                                            "mode": "human", "source_ref": SYN})
    s.apply("a-stop", {"event_id": "no-07-stop", "op": "stop", "run_id": run2, "reason": "合成演示：只为试作者否定意见"})
    mem = [str(SCRIPTS / "demonstration_memory.py")]
    s.run("mem-check", PY + mem + ["check", s.record], "demonstration_memory.py check " + s.record)
    s.run("mem-index", PY + mem + ["index", s.record, "--project-id", "demo-bike-stall", "--task", "dialogue_revision"],
          "demonstration_memory.py index ... --task dialogue_revision")
    s.run("mem-select", PY + mem + ["select", s.record, "--project-id", "demo-bike-stall", "--task",
                                    "dialogue_revision", "--limit", "3"],
          "demonstration_memory.py select ... --task dialogue_revision --limit 3")
    s.apply("configure-off", {"event_id": "loop-90-configure", "op": "configure", "loop_enabled": False})
    s.apply("trial-start-after-off", dict(start, event_id="loop-91-start", run_id="run-after-off"))
    s.status()
    s.save()


# ---------------------------------------------------------------- nine cases
def memory():
    template = json.loads((SCRIPTS.parent / "assets/demonstration-case-template.json").read_text(encoding="utf-8"))

    def case(cid, status, group=None, split="development", project="demo-bike-stall", task="dialogue_revision",
             tags=("对白",)):
        item = json.loads(json.dumps(template))
        item.update(id=cid, project_id=project, group_id=group or ("grp-" + cid), status=status, split=split,
                    task=task, tags=list(tags), before="合成原稿：" + cid, after="合成改稿：" + cid,
                    why="合成演示", when=["双方正在对话"], decisions=["合成演示"], **{"except": ["正式汇报"]})
        item["source"] = {"ref": "合成演示：" + cid, "version": "1", "reviewer": "合成", "evidence": "合成演示"}
        if status == "author_accepted":
            item["author_acceptance"] = {"quote": "采纳当前稿。", "ref": "合成演示：" + cid}
        item["hashes"] = {k: sha(item[k]) for k in ("before", "after")}
        return item

    cases = [case("a1", "author_accepted"), case("a2", "author_accepted"), case("t1", "teacher_approved"),
             case("t2", "teacher_approved"), case("c1", "candidate"), case("r1", "rejected"),
             case("h1", "teacher_approved", group="held", split="evaluation"),
             case("h2", "author_accepted", group="held"),
             case("o1", "author_accepted", project="another-book")]

    def store(name, items, enabled=True):
        s = Store(name, "记录.md", "demo-bike-stall",
                  {"demonstration_learning": {"enabled": enabled, "loop_enabled": False},
                   "demonstrations": {c["id"]: c for c in items}, "learning_runs": {}, "learning_events": {}})
        return s

    mem = [str(SCRIPTS / "demonstration_memory.py")]
    s = store("memory", cases)
    base = ["--project-id", "demo-bike-stall", "--task", "dialogue_revision"]
    for label, args in (("select", ["select", s.record] + base),
                        ("select-limit4", ["select", s.record] + base + ["--limit", "4"]),
                        ("index", ["index", s.record] + base),
                        ("index-limit", ["index", s.record] + base + ["--limit", "2"]),
                        ("select-other-task", ["select", s.record, "--project-id", "demo-bike-stall", "--task",
                                               "scene_revision"]),
                        ("select-tag-mismatch", ["select", s.record] + base + ["--tag", "动作"]),
                        ("select-exclude-group", ["select", s.record] + base + ["--exclude-group", "grp-a1",
                                                                                  "--exclude-group", "grp-a2",
                                                                                  "--exclude-group", "grp-t1",
                                                                                  "--exclude-group", "grp-t2"]),
                        ("select-other-project", ["select", s.record, "--project-id", "another-book", "--task",
                                                  "dialogue_revision"])):
        s.run(label, PY + mem + args, "demonstration_memory.py " + " ".join(args))
    s.save()
    off = store("memory-off", cases, enabled=False)
    off.run("select-disabled", PY + mem + ["select", off.record] + base, "demonstration_memory.py select (disabled)")
    off.save()
    bad1 = [dict(c) for c in cases]
    bad1[0] = dict(bad1[0], author_acceptance=None)
    b = store("memory-noquote", bad1)
    b.run("check-noquote", PY + mem + ["check", b.record], "demonstration_memory.py check (no quote)")
    b.save()
    bad2 = [dict(c) for c in cases]
    bad2[2] = dict(bad2[2], after="合成改稿：t1（改过一个字）")
    b2 = store("memory-texthash", bad2)
    b2.run("check-texthash", PY + mem + ["check", b2.record], "demonstration_memory.py check (text changed)")
    b2.save()


# ---------------------------------------------------------------- dialogue lint
def lint():
    p = Part("lint")
    (p.dir / "正文").mkdir(exist_ok=True)
    (p.dir / "正文/ch01.txt").write_text(DRAFT, encoding="utf-8")
    config = {"profiles": {"老秦": {"archetype": "taciturn", "voice_prompt": "话少，报数不解释。"},
                           "阿梨": {"archetype": "plain_student", "voice_prompt": "说话直，带一点学生气。"}},
              "cold_protagonist_names": [], "aliases": {}, "speaker_overrides": [], "stress_speakers": [],
              "suspicious_expressions": [], "min_profile_quotes": 3, "genre_id": None, "genre_overrides": {},
              "scene_overrides": [], "system_brackets": {"enabled": False}}
    (p.dir / "本书配置.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    old = dict(config, profiles={"老秦": {"archetype": "taciturn", "min_avg_len": 3.0, "min_colloquial_rate": 0.0,
                                         "voice_prompt": "话少，报数不解释。"},
                                "阿梨": {"archetype": "plain_student", "min_avg_len": 4.0, "min_colloquial_rate": 0.2,
                                         "voice_prompt": "说话直，带一点学生气。"}})
    (p.dir / "旧配置.json").write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")
    lint_py = [str(SCRIPTS / "dialogue_lint/run_lint.py")]
    p.run("scan", PY + lint_py + ["scan", "正文/ch01.txt", "--config", "本书配置.json", "--output", "对白复核.json"],
          "run_lint.py scan 正文/ch01.txt --config 本书配置.json --output 对白复核.json")
    p.run("scan-old-config", PY + lint_py + ["scan", "正文/ch01.txt", "--config", "旧配置.json", "--output",
                                             "对白复核-旧配置.json"], "run_lint.py scan (old config with min_avg_len)")
    p.run("scan-hints", PY + lint_py + ["scan", "正文/ch01.txt", "--config", "本书配置.json", "--style-hints",
                                        "--output", "对白复核-全部提示.json", "--request-output", "请求.json",
                                        "--prompt-output", "请求提示.txt"],
          "run_lint.py scan 正文/ch01.txt --config 本书配置.json --style-hints --output 对白复核-全部提示.json "
          "--request-output 请求.json --prompt-output 请求提示.txt")
    request = json.loads((p.dir / "请求.json").read_text(encoding="utf-8"))
    (p.dir / "request-copy.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    items = request.get("items") or request.get("quotes") or []
    qid = None
    for item in items:
        if "我注意到" in json.dumps(item, ensure_ascii=False):
            qid = item.get("quote_id")
    source_hash = request.get("source_hash")
    cand = {"source_hash": source_hash,
            "replacements": [{"quote_id": qid, "original": "我注意到后胎也有点瘪。", "replacement": "后胎好像也有点瘪。"}]}
    (p.dir / "候选.json").write_text(json.dumps(cand, ensure_ascii=False, indent=2), encoding="utf-8")
    p.run("apply-without-same-options", PY + lint_py + ["apply", "正文/ch01.txt", "请求.json", "候选.json", "--output",
                                                        "正文/ch01.候选稿-试.txt", "--config", "本书配置.json"],
          "run_lint.py apply ... --config 本书配置.json (no --style-hints)")
    p.run("apply", PY + lint_py + ["apply", "正文/ch01.txt", "请求.json", "候选.json", "--output",
                                   "正文/ch01.候选稿.txt", "--config", "本书配置.json", "--style-hints"],
          "run_lint.py apply 正文/ch01.txt 请求.json 候选.json --output 正文/ch01.候选稿.txt --config 本书配置.json --style-hints")
    p.run("scan-no-config", PY + lint_py + ["scan", "正文/ch01.txt", "--output", "无配置.json"],
          "run_lint.py scan 正文/ch01.txt --output 无配置.json")
    p.run("scan-output-exists", PY + lint_py + ["scan", "正文/ch01.txt", "--config", "本书配置.json", "--output",
                                                "对白复核.json"], "run_lint.py scan ... --output 对白复核.json (exists)")
    bad = dict(cand, replacements=[dict(cand["replacements"][0], replacement="后胎好像也有点瘪。”她说，“")])
    (p.dir / "候选-越界.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    p.run("apply-outside-quote", PY + lint_py + ["apply", "正文/ch01.txt", "请求.json", "候选-越界.json", "--output",
                                                 "正文/越界.txt", "--config", "本书配置.json", "--style-hints"],
          "run_lint.py apply (replacement adds quotes)")
    bad2 = dict(cand, replacements=[dict(cand["replacements"][0], quote_id="p3:q1", original="还能补吗？")])
    (p.dir / "候选-别的句.json").write_text(json.dumps(bad2, ensure_ascii=False), encoding="utf-8")
    p.run("apply-unknown-quote", PY + lint_py + ["apply", "正文/ch01.txt", "请求.json", "候选-别的句.json", "--output",
                                                 "正文/别的句.txt", "--config", "本书配置.json", "--style-hints"],
          "run_lint.py apply (quote not in request)")
    (p.dir / "正文/ch01-改过.txt").write_text(DRAFT.replace("快收了", "快收摊了"), encoding="utf-8")
    p.run("apply-source-changed", PY + lint_py + ["apply", "正文/ch01-改过.txt", "请求.json", "候选.json", "--output",
                                                  "正文/改过.txt", "--config", "本书配置.json", "--style-hints"],
          "run_lint.py apply (source changed)")
    over = dict(config, speaker_overrides=[{"para_index": 11, "quote_index": 1, "speaker": "老秦"}])
    (p.dir / "本书配置-指定.json").write_text(json.dumps(over, ensure_ascii=False, indent=2), encoding="utf-8")
    p.run("scan-override-genre", PY + lint_py + ["scan", "正文/ch01.txt", "--config", "本书配置-指定.json", "--genre",
                                                 "modern_gritty", "--output", "对白复核-指定.json"],
          "run_lint.py scan ... --config 本书配置-指定.json --genre modern_gritty")
    (p.dir / "正文/ch01-直角引号.txt").write_text(DRAFT.replace("“", "「").replace("”", "」"), encoding="utf-8")
    p.run("scan-corner-quotes", PY + lint_py + ["scan", "正文/ch01-直角引号.txt", "--config", "本书配置.json",
                                                "--output", "对白复核-直角引号.json"],
          "run_lint.py scan (「」 quotes)")
    p.save()


# ---------------------------------------------------------------- final-stage wording check
# The chapter walkthrough above has to mark its synthetic final words in source_ref, because words that
# start with "（合成演示）" are not a plain acceptance. Here the same small check inside chapter_gate.py is
# called directly with unmarked sentences, each with decision:accept_final_version.
FINAL_WORDS = ["继续。", "先不采纳，我再看看。", "还没到定稿的时候。", "定稿。", "采纳当前稿。"]
FINAL_CHECK = """import json, sys
sys.path.insert(0, sys.argv[1])
import chapter_gate
for quote in json.loads(sys.argv[2]):
    try:
        chapter_gate._final_decision({"author_quote": quote, "decision": "accept_final_version"})
        print("recorded", quote)
    except Exception as error:
        print("pending ", quote, "|", type(error).__name__, error)
"""


def final_words():
    p = Part("final-words")
    p.run("final-words", PY + ["-c", FINAL_CHECK, str(SCRIPTS), json.dumps(FINAL_WORDS, ensure_ascii=False)],
          "python3 -I -B -c <call chapter_gate._final_decision on each sentence> SCRIPTS_DIR '%s'"
          % json.dumps(FINAL_WORDS, ensure_ascii=False))
    p.save()


if __name__ == "__main__":
    gate()
    loop()
    memory()
    lint()
    final_words()
