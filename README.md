# ai-skills

A collection of reusable AI agent skills for use with OpenCode and Claude.

## Structure

```
skills/
  github/            — skills that depend on the `gh` CLI and GitHub issues/PRs
    scope-it/SKILL.md
    build-it/SKILL.md
    review-it/SKILL.md
    test-it/SKILL.md
    ship-it/SKILL.md
  standalone/        — skills with no external dependencies; work anywhere
    big-brain/SKILL.md
    cook-bruv/SKILL.md
    this-sus/SKILL.md
    roast-it/SKILL.md
    yeet-it/SKILL.md
```

Each skill is a directory containing a single `SKILL.md` file with YAML frontmatter (`name`, `description`) followed by markdown instructions. Skills are organized into groups but linked flatly to their destinations.

## Setup

Run the install script from the repo root:

```bash
bash link-skills.sh
```

The script auto-detects your OS and symlinks each skill directory into the expected locations:

| Tool | macOS / Linux | Windows |
| --- | --- | --- |
| OpenCode | `~/.config/opencode/skills/<name>` | `%APPDATA%\opencode\skills\<name>` |
| Claude | `~/.claude/skills/<name>` | `%USERPROFILE%\.claude\skills\<name>` |

Re-run `link-skills.sh` whenever you add a new skill.

### Windows

Run the script in **Git Bash** (or MSYS2/Cygwin). Symlinks on Windows require one of:

- [Developer Mode](https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development) enabled, or
- Running Git Bash as Administrator

## Adding a skill

Follow these steps:

1. Create `skills/<group>/<skill-name>/SKILL.md` (use `github/` for skills requiring the `gh` CLI, `standalone/` otherwise)
2. Add a `SKILL.md` with valid frontmatter (`name` must match the directory name)
3. Skill names must be unique across all groups
4. Run `bash link-skills.sh`

## AI agent context

See [AGENTS.md](AGENTS.md) for conventions, rules, and project context used by AI coding agents (Codex, Gemini, etc.). Claude Code reads [CLAUDE.md](CLAUDE.md), which points there as well.
