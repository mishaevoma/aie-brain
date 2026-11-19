#!/usr/bin/env python3
"""Run the project review on the eval fixtures with a headless coding agent.

Each fixture is copied to a fresh folder outside this repository and committed there, so the
agent sees an ordinary project with no wiki above it. The agent gets the same line a person
would paste. The run folder keeps what came back: the review, a trace of what the agent did
with arrival times, and whether the fixture's tree was left as it was found.

Usage:
  python3 evals/run.py --label baseline
  python3 evals/run.py --label after-fix --fixtures 03 07 --via skill
  python3 evals/run.py --label smoke --agent claude --model sonnet --fixtures 07

  --via url        paste line with the published review URL (default)
  --via skill      paste line with the path of this checkout's SKILL.md (tests unpublished edits)
  --via installed  the skill copied into the fixture, as `npx skills add` leaves it

Standard library only. The agents are the logged-in command-line tools on this machine.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "evals" / "fixtures"
SKILL = ROOT / ".agents" / "skills" / "brain-consult"
REVIEW_URL = "https://mishaevoma.github.io/aie-brain/review.md"
CODEX_APP = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
GIT_ID = ["-c", "user.name=evals", "-c", "user.email=evals@example.invalid"]


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *GIT_ID, *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def tree_state(cwd: Path) -> str:
    """Every tracked change, untracked file and ignored file. Empty means untouched."""
    return git(cwd, "status", "--porcelain", "--untracked-files=all", "--ignored")


def fixture_revision(name: str) -> str:
    """The git tree of the fixture as committed, marked when the working copy differs."""
    try:
        tree = git(ROOT, "rev-parse", "--short", f"HEAD:evals/fixtures/{name}")
    except subprocess.CalledProcessError:
        return "uncommitted"
    dirty = git(ROOT, "status", "--porcelain", "--", f"evals/fixtures/{name}")
    return tree + ("+local" if dirty else "")


def wiki_clone(work: Path) -> Path:
    """The committed wiki without evals/, so a local run cannot read the answer key."""
    clone = work / "wiki"
    if not clone.exists():
        if git(ROOT, "status", "--porcelain", "--", ".", ":!evals/runs"):
            print("note: uncommitted changes are not in the wiki copy the agent reads; commit first to test them")
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{ROOT}", str(clone)], check=True)
        shutil.rmtree(clone / "evals", ignore_errors=True)
    return clone


def prompt_for(via: str, review_url: str, wiki: Path | None) -> str:
    if via == "url":
        return f"Review this project using\n{review_url}"
    if via == "skill":
        return f"Review this project using\n{wiki / '.agents/skills/brain-consult/SKILL.md'}"
    return "Use brain-consult to review this project."


def prepare(name: str, work: Path, via: str, wiki: Path | None) -> Path:
    target = work / name
    shutil.copytree(FIXTURES / name, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if via == "installed":
        for home in (".claude/skills", ".agents/skills"):
            shutil.copytree(wiki / ".agents/skills/brain-consult", target / home / "brain-consult")
    git(target, "init", "-q")
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "fixture")
    return target


def codex_command(args: argparse.Namespace, prompt: str) -> list[str]:
    binary = shutil.which("codex") or CODEX_APP
    command = [binary, "exec", "--json", "--ephemeral", "--ignore-user-config"]
    if args.model:
        command += ["-m", args.model]
    command += ["-c", f'model_reasoning_effort="{args.effort}"']
    if args.network:
        # A person who approves the agent's network commands. The fixture stays writable on
        # purpose: staying read-only has to come from the review, and is checked afterwards.
        command += ["-s", "workspace-write", "-c", "sandbox_workspace_write.network_access=true"]
    else:
        command += ["-s", "read-only"]
    if args.wiki:
        command += ["--add-dir", str(args.wiki)]
    return command + [prompt]


def claude_command(args: argparse.Namespace, prompt: str) -> list[str]:
    command = [
        "claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--include-partial-messages",
        "--strict-mcp-config", "--permission-mode", "dontAsk",
        "--allowedTools", "Read,Glob,Grep,WebFetch,WebSearch,Bash,Skill,Task,TodoWrite",
    ]
    if args.model:
        command += ["--model", args.model]
    if args.wiki:
        command += ["--add-dir", str(args.wiki)]
    return command


def read_codex(events: list[tuple[float, dict]]) -> dict:
    messages = [(t, e["item"]["text"]) for t, e in events
                if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
    steps = []
    for t, e in events:
        item = e.get("item", {})
        if e.get("type") != "item.completed" or item.get("type") == "agent_message":
            continue
        if item.get("type") == "command_execution":
            steps.append((t, f"shell exit={item.get('exit_code')}: {item.get('command', '')}"))
        elif item.get("type") == "web_search":
            titles = "; ".join(str(r.get("title") or r.get("domain") or "") for r in item.get("results", [])[:2])
            steps.append((t, f"web {json.dumps(item.get('action'))} -> {titles[:80]}"))
        else:
            steps.append((t, f"{item.get('type')}: {json.dumps(item)[:400]}"))
    usage = next((e.get("usage") for _, e in reversed(events) if e.get("type") == "turn.completed"), None)
    review = max(messages, key=lambda m: len(m[1]), default=(None, ""))
    return {"review": review[1], "review_at": review[0], "steps": steps, "messages": messages, "usage": usage, "model": None}


def read_claude(events: list[tuple[float, dict]]) -> dict:
    model = next((e.get("model") for _, e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
    steps, messages = [], []
    first_delta: dict[int, float] = {}  # message number -> arrival of its first text
    number = 0
    for t, e in events:
        if e.get("type") == "stream_event":
            event = e.get("event", {})
            if event.get("type") == "message_start":
                number += 1
            elif event.get("type") == "content_block_delta" and event.get("delta", {}).get("type") == "text_delta":
                first_delta.setdefault(number, t)
        elif e.get("type") == "assistant":
            for block in e.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    steps.append((t, f"{block.get('name')}: {json.dumps(block.get('input'))}"))
                elif block.get("type") == "text" and block.get("text", "").strip():
                    messages.append((first_delta.get(number, t), block["text"]))
    result = next((e for _, e in reversed(events) if e.get("type") == "result"), {})
    review = max(messages, key=lambda m: len(m[1]), default=(None, result.get("result", "")))
    usage = {k: result.get(k) for k in ("total_cost_usd", "num_turns", "duration_ms") if k in result}
    return {"review": review[1] or result.get("result", ""), "review_at": review[0], "steps": steps,
            "messages": messages, "usage": usage, "model": model}


def run_one(name: str, args: argparse.Namespace, work: Path, out: Path) -> dict:
    target = prepare(name, work, args.via, args.wiki)
    prompt = prompt_for(args.via, args.review_url, args.wiki)
    command = codex_command(args, prompt) if args.agent == "codex" else claude_command(args, prompt)
    env = dict(os.environ)
    if args.via == "installed":
        env["AIE_BRAIN"] = str(args.wiki)
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=target, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    events: list[tuple[float, dict]] = []
    try:
        for line in process.stdout:
            try:
                events.append((round(time.monotonic() - started, 1), json.loads(line)))
            except json.JSONDecodeError:
                continue
            if time.monotonic() - started > args.timeout:
                process.kill()
                break
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        process.kill()
    seconds = round(time.monotonic() - started, 1)
    parsed = read_codex(events) if args.agent == "codex" else read_claude(events)
    left_behind = tree_state(target)

    def public(text: str) -> str:
        """Local paths say nothing about the review and name the machine it ran on."""
        for path, label in [(work, "<work>"), (work.resolve(), "<work>"), (ROOT, "<wiki>"), (Path.home(), "~")]:
            text = text.replace(str(path), label)
        return text

    folder = out / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "review.md").write_text(public(parsed["review"].rstrip()) + "\n", encoding="utf-8")
    trace = [f"prompt: {prompt!r}", ""]
    timeline = sorted([(t, "step", s) for t, s in parsed["steps"]] + [(t, "says", m) for t, m in parsed["messages"]])
    for t, kind, text in timeline:
        text = public(text)
        shown = text[:300] if kind == "step" else text.strip().splitlines()[0][:200] + f" … ({len(text)} chars)"
        trace.append(f"{t:7.1f}s  {kind}  {shown}")
    (folder / "trace.txt").write_text(public("\n".join(trace)) + "\n", encoding="utf-8")
    meta = {
        "fixture": name,
        "fixture_revision": fixture_revision(name),
        "agent": args.agent,
        "agent_version": subprocess.run([command[0], "--version"], capture_output=True, text=True).stdout.strip(),
        "model": parsed["model"] or args.model or "agent default",
        "effort": args.effort if args.agent == "codex" else None,
        "via": args.via,
        "network_approved": args.network if args.agent == "codex" else None,
        "prompt": public(prompt),
        "wiki_revision": git(ROOT, "log", "-1", "--format=%h %cs"),
        "date": dt.date.today().isoformat(),
        "seconds_total": seconds,
        "seconds_to_review": parsed["review_at"],
        "steps": len(parsed["steps"]),
        "usage": parsed["usage"],
        "read_only": left_behind == "",
        "left_behind": left_behind.splitlines(),
        "exit_code": process.returncode,
    }
    (folder / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", required=True, help="names the run folder: evals/runs/<date>-<label>")
    parser.add_argument("--agent", choices=["codex", "claude"], default="codex")
    parser.add_argument("--model", help="model for the agent; its own default when omitted")
    parser.add_argument("--effort", default="medium", help="Codex reasoning effort (default medium)")
    parser.add_argument("--via", choices=["url", "skill", "installed"], default="url")
    parser.add_argument("--review-url", default=REVIEW_URL)
    parser.add_argument("--fixtures", nargs="*", help="fixture names or their number prefixes; all when omitted")
    parser.add_argument("--no-network", dest="network", action="store_false",
                        help="Codex only: keep the sandbox offline, as when nobody approves a network command")
    parser.add_argument("--parallel", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=900, help="seconds per review")
    parser.add_argument("--work", help="where fixture copies go; a new temporary folder when omitted")
    args = parser.parse_args()

    names = sorted(p.name for p in FIXTURES.iterdir() if p.is_dir())
    if args.fixtures:
        names = [n for n in names if any(n == f or n.startswith(f) for f in args.fixtures)]
    if not names:
        print("no fixture matches")
        return 2
    out = ROOT / "evals" / "runs" / f"{dt.date.today().isoformat()}-{args.label}"
    out.mkdir(parents=True, exist_ok=True)
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="aie-brain-evals-"))
    work = work / f"{args.label}-{int(time.time())}"
    work.mkdir(parents=True)
    args.wiki = None if args.via == "url" else wiki_clone(work)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {pool.submit(run_one, name, args, work, out): name for name in names}
        for future in concurrent.futures.as_completed(futures):
            meta = future.result()
            to_review = meta["seconds_to_review"]
            print(f"{meta['fixture']:<18} {meta['seconds_total']:>6}s total, review at "
                  f"{to_review if to_review is not None else '-'}s, {meta['steps']} steps, "
                  f"{'read-only' if meta['read_only'] else 'LEFT FILES: ' + '; '.join(meta['left_behind'])}")
    print(f"reviews in {out.relative_to(ROOT)}; fixture copies in {work}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
