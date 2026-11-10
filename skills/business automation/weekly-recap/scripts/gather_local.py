#!/usr/bin/env python3
"""Gather local evidence for a weekly recap: git commits + Claude Code sessions.

Usage:
    python gather_local.py --since 2026-11-02 [--until 2026-11-09]
        [--projects-dir C:/Projects] [--author Tyler]
        [--claude-dir ~/.claude/projects]

Prints a markdown digest to stdout. Read-only; never modifies repos.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

NOISE_PREFIXES = (
    "<command-", "<local-command", "<system-reminder", "Caveat:",
    "[Request interrupted", "<task-notification", "<bash-",
)
NOISE_COMMITS = (
    "bumped", "decremented", "addressed", "address pr", "self-review",
    "index on", "wip on", "fixed failing", "merge ", "fixup", "squash",
)
PR_RE = re.compile(r"\(#\d+\)\s*$")


def git_commits(projects_dir: Path, since: str, until: str, author: str):
    out = {}
    for repo in sorted(p for p in projects_dir.iterdir() if (p / ".git").exists()):
        try:
            res = subprocess.run(
                ["git", "-C", str(repo), "log", "--all", "--no-merges",
                 f"--since={since}", f"--until={until}", f"--author={author}",
                 "--date=short", "--pretty=%ad|%D|%s"],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=30,
            )
        except Exception as e:  # noqa: BLE001
            print(f"warn: git failed in {repo.name}: {e}", file=sys.stderr)
            continue
        lines = [l for l in res.stdout.splitlines() if l.strip()]
        if lines:
            out[repo.name] = lines
        # Branches with recent activity by anyone help spot open PR branches.
    return out


def repo_name(cwd: str) -> str:
    """Roll a session's cwd up to its enclosing git repo name."""
    p = Path(cwd)
    for cand in (p, *p.parents):
        if (cand / ".git").exists():
            return cand.name
    return p.name


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content
                         if isinstance(c, dict) and c.get("type") == "text")
    return ""


def claude_sessions(claude_dir: Path, since_dt: datetime, until_dt: datetime):
    """Return {project: [(start, n_prompts, [prompts...])]}"""
    result = defaultdict(list)
    if not claude_dir.exists():
        return result
    for f in claude_dir.glob("*/*.jsonl"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime < since_dt:
            continue
        prompts, start, cwd = [], None, None
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if rec.get("type") != "user" or rec.get("isSidechain") or rec.get("isMeta"):
                        continue
                    ts = rec.get("timestamp")
                    if not ts:
                        continue
                    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if t < since_dt or t > until_dt:
                        continue
                    msg = rec.get("message", {})
                    txt = text_of(msg.get("content", "")).strip()
                    if not txt or txt.startswith(NOISE_PREFIXES):
                        continue
                    start = start or t
                    cwd = cwd or rec.get("cwd")
                    prompts.append(" ".join(txt.split())[:300])
        except OSError:
            continue
        if prompts:
            project = repo_name(cwd) if cwd else f.parent.name
            result[project].append((start, prompts))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="YYYY-MM-DD inclusive")
    ap.add_argument("--until", default=None, help="YYYY-MM-DD exclusive (default: now)")
    ap.add_argument("--projects-dir", default="C:/Projects")
    ap.add_argument("--author", default="Tyler")
    ap.add_argument("--claude-dir", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--max-prompts", type=int, default=6)
    a = ap.parse_args()

    since_dt = datetime.fromisoformat(a.since).replace(tzinfo=timezone.utc)
    until_dt = (datetime.fromisoformat(a.until).replace(tzinfo=timezone.utc)
                if a.until else datetime.now(timezone.utc) + timedelta(days=1))
    until_str = until_dt.strftime("%Y-%m-%d")

    print(f"# Local evidence {a.since} -> {until_str}\n")
    print("## Git commits (author ~ %s)\n" % a.author)
    commits = git_commits(Path(a.projects_dir), a.since, until_str, a.author)
    if not commits:
        print("_none_\n")
    for repo, lines in commits.items():
        merged, wip, branches, seen = [], [], set(), set()
        for l in lines:
            date, refs, subj = (l.split("|", 2) + ["", ""])[:3]
            for r in refs.split(","):
                r = r.strip().replace("HEAD -> ", "").replace("origin/", "")
                if r and not r.startswith(("tag:", "refs/stash")) and r not in ("HEAD", "main", "master", "develop"):
                    branches.add(r)
            if subj in seen or subj.lower().startswith(NOISE_COMMITS):
                continue
            seen.add(subj)
            (merged if PR_RE.search(subj) else wip).append(f"{date} {subj}")
        print(f"### {repo}")
        print("**Merged PRs (squash titles):**")
        print("\n".join(f"- {m}" for m in merged) or "- _none_")
        print("**Other commits (deduped, noise dropped):**")
        print("\n".join(f"- {w}" for w in wip[:25]) or "- _none_")
        if branches:
            print("**Branches touched:** " + ", ".join(sorted(branches)))
        print()

    print("## Claude Code sessions\n")
    sessions = claude_sessions(Path(a.claude_dir).expanduser(), since_dt, until_dt)
    if not sessions:
        print("_none_\n")
    for project, items in sorted(sessions.items()):
        print(f"### {project}")
        for start, prompts in sorted(items):
            print(f"- {start:%Y-%m-%d} ({len(prompts)} prompts)")
            for p in prompts[: a.max_prompts]:
                print(f"    - {p}")
        print()


if __name__ == "__main__":
    main()
