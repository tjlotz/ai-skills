---
name: weekly-recap
description: Drafts Tyler's weekly recap (Done / Doing / Blockers / Notes / Questions) for the Monday check-in by gathering the past week's evidence from Daily Notes, local git commits, Claude Code sessions, Google Calendar, Gmail (GitHub PR and Google Chat notifications), and Jira, then writes a short markdown file into the Weekly Recaps folder in the same style as past recaps. Use when asked to write, draft, or prep the weekly recap/review/update.
license: MIT
compatibility: claude
---

## What I do

- Finds the previous recap and uses its date as the start of the reporting window
- Gathers evidence for the window from every available source (local git, Claude sessions, Calendar, Gmail, Jira)
- Compresses dozens of commits, PRs, and tickets into a few short, project-grouped bullets
- Carries unfinished `Doing` items and open `Blockers` forward from last week
- Writes `<meeting-date>.md` into the Weekly Recaps folder using `template.md`
- If this week's recap already exists, updates it in place by adding and moving bullets, and never deletes Tyler's edits

## When to use me

- "Write my weekly recap", "prep my Monday update", "draft this week's review"
- `/weekly-recap` drafts for the next Monday (or today, if today is Monday)
- `/weekly-recap 2026-11-16` drafts for a specific meeting date

## Paths and mappings

- **Recaps folder:** `C:\Users\NPD_User\Nocturnal Dropbox\Tyler Lotz\Nocturnal\Weekly Recaps` (an Obsidian vault)
- **Template:** `template.md` in that folder
- **Local repos:** `C:\Projects\*` (git author `Tyler`)
- **Gatherer script:** `scripts/gather_local.py` (in this skill's directory)

| Source repo / Jira / chat term | Recap heading | Short name |
|---|---|---|
| `ceryx_implant_bg26`, "Ceryx", "CM" | `#### Ceryx` | CM |
| `neuraworx_stimulator_bg26`, "NeuraWorx", "NW" | `#### NeuraWorx` | NW |
| `npd_platform`, `npd_common` | `#### Platform` | platform |
| Office, IT, admin, testing support | `#### Office` | — |

If work maps to a project not in the table, use the repo or Jira project's plain name as the heading.

## Instructions

### 1. Set the dates

1. Meeting date = the argument if given, otherwise the next Monday on or after today. The file name is `YYYY-MM-DD.md` for that date.
2. If that file already exists and is non-empty, switch to **update mode** (see step 6). Never replace it wholesale.
3. Window start = the date in the file name of the most recent dated recap *before* the meeting date (ignore `template.md`, `Untitled.md`, and names with a suffix like `(Software Meeting)`). Window end = now. Expect to run several times during the week: an early run makes a thin draft, and later runs fill it in.

### 2. Read the context

1. Read `template.md`. Its section headings and the `----` / `---` dividers are the skeleton; keep them exactly.
2. Read the three most recent recaps. They set the voice, and the latest one supplies:
   - `Doing` items to check off or carry forward
   - `Blockers` to confirm as still open or resolved
   - `Questions` whose answers may have shown up this week

### 3. Gather evidence

Run all sources. When a connector is missing or not authenticated, skip it, keep going, and list it in the final report. Don't stop to ask.

**Local (always available):**

```
python -I "<skill-dir>/scripts/gather_local.py" --since <window-start>
```

This prints merged PRs (squash titles ending in `(#N)`), other deduped commits, branches touched, and the opening prompts of each Claude Code session, grouped by repo. Merged PRs are the strongest Done signal. Claude prompts show what was really being worked on, including bench work, debugging, and reviews that never became commits.

**Google Calendar:** list events in the window and in the coming week (`list_events` with `startTime`/`endTime`, `orderBy: startTime`). Look for visits, deliveries, releases, testing sessions, OOO, and deadlines. Skip recurring standups and other routine meetings.

**Gmail, GitHub notifications:** search `from:notifications@github.com after:<window-start> -subject:"run failed"` with the `THREAD_VIEW_SUMMARY` view and `pageSize` 50. Subjects look like `[Org/repo] Title (PR #N)`, and snippets say "Merged #N", "approved", or "requested your review". Split the results into:
- PRs Tyler authored (`author@noreply` in cc): merged ones go to Done, open ones to Doing
- PRs Tyler reviewed (`review_requested@noreply` in cc): leave these out of the file, since past recaps don't list reviews. Mention them in the chat reply only.
- Review requests still unanswered after 2+ days: mention in chat as possible follow-ups

This covers repos that aren't cloned locally or are stale there. `gh` is not logged in on this machine.

**Daily Notes (high value):** `C:\Users\NPD_User\Nocturnal Dropbox\Tyler Lotz\Nocturnal\Daily Notes\YYYY-MM-DD.md`. Read every note dated within the window, plus the latest note before it. This is where Tyler actually tracks his tasks; Jira often lags behind. What to look for:
- `- [x]` items are Done and `- [ ]` items are Doing. A struck-through line (`~~...~~`) was dropped, so ignore it.
- Headings such as `### Up Next` and `### Back Port` list planned work for Doing or Up Next.
- Notes from meetings with Matt Poss ("Meeting with Poss") can contain priorities and decisions. Use them only as factual Notes bullets, and never copy personal or HR-type remarks into the recap.
- Long technical design notes (e.g. a synthetic data spec) show what was being worked on. Summarize them to one bullet; never copy them in.

**Google Chat (best effort):** task requests come in as DMs from Matt Poss (`mattp@nocturnalpd.com`). As of 2026-11, Chat doesn't email these and no Chat connector exists. Run one quick check, `from:chat-noreply@google.com after:<window-start>`. If it finds nothing, report "Google Chat: no source" in the chat reply and move on.

**Todoist:** no connector, so skip it.

**Jira (Atlassian MCP):** cloudId `b65f0dfd-6d1d-44a6-8e46-beaab88b905a` (`nocturnalpd.atlassian.net`). Run two JQL queries:
1. `assignee = currentUser() AND updated >= "<window-start>"`: Done tickets go to Done, In Progress tickets to Doing, Blocked or flagged tickets to Blockers.
2. `reporter = currentUser() AND created >= "<window-start>"`: follow-ups Tyler filed this week. These are candidates for `### Up Next`.

Tickets that haven't moved in weeks are backlog, so ignore them. Put ticket keys inline in backticks, e.g. `CM-185`.

**Calendar notes:** the recap meeting is the recurring Monday "Software Group Touchpoint". Skip it and other recurring meetings (e.g. "NeuraWorx Internal Weekly"). One-off meetings such as testing syncs, visits, and reviews can become a Notes bullet.

### 4. Classify

**No double counting:** skip anything already listed in the previous recap's Done. This applies even when its Jira ticket was closed or its PR merged inside the window, because tickets are often closed in bulk the morning of the meeting.

- **Done:** merged PRs, Jira tickets moved to Done, deliveries or releases, and last week's `Doing` items that the evidence shows finished.
- **Doing:** open PRs, active branches with no merge yet, In Progress tickets, and last week's `Doing` items with no sign of completion. Put work that hasn't started but is clearly queued under `### Up Next`.
- **Blockers:** only things waiting on someone or something else, such as hardware, testing, a review, or a decision. Name the person or thing being waited on. Leave the section empty if there are none; don't invent blockers.
- **Notes:** only notable facts from the week, like visits, releases, deadlines, decisions in chat, and hardware or board status. Keep it to a few bullets, and leave it empty if nothing qualifies.
- **Questions:** leave empty. Tyler writes these during or just before the meeting. Suggest at most three candidate questions in the chat reply instead.

### 5. Write in Tyler's style

Past recaps are short, about 300–1500 characters. Match them:

- Use project subheadings (`#### Ceryx`, `#### NeuraWorx`) only when there's more than one project in a section. With a single project, use plain bullets.
- Each bullet is a terse fragment of 3–10 words with no full sentences and no trailing periods.
- **Compress hard.** Aim for 2–4 bullets per project in Done and 1–4 in Doing. Group related PRs into themes: eight merged PRs might become "Impedance bring up for Ceryx" and "Port NW to CM". Never list commits. Before writing, check every merged PR is in Done and not left in Doing.
- Wrap module and identifier names in backticks: `impedanceMgr`, `adcMgr`, `backupRtcMgr`.
- Add status as a suffix only when it matters: `(merged)`, `- in review`, `(open PR)`, `- in test`.
- Use one nesting level (a tab plus `-`) only to add a single clarifying detail.
- Keep the dividers exactly as the template has them (`----` after Done, `---` elsewhere).
- No emoji, no bold section summaries, and no source citations in the file.

### 6. Write and report

**New file:** start from `template.md` and write the file to the recaps folder.

**Update mode (the file already exists):** Tyler may have edited it since the last run, so treat every existing line as his.
1. Never delete or reword an existing line. Never touch the `Notes` or `Questions` sections except to append.
2. Add new evidence as new bullets in the right section and project group. Skip anything an existing bullet already covers, even if worded differently.
3. If a `Doing` bullet is now finished (merged PR, `[x]` in Daily Notes, Jira Done), *move* it, with its sub-bullets, to `Done` unchanged. You may append a status suffix like `(merged)`.
4. If an item looks stale or wrong, don't remove it. Flag it in the chat reply.
5. Use Edit for targeted insertions rather than rewriting the whole file.

Then reply in chat with:
   - the path written, and in update mode a short list of what was added or moved
   - which sources were used, and which were skipped and why
   - anything ambiguous that Tyler should check (e.g. "Not sure `feature/synthetic-impedance` is Done vs Doing")
   - up to three suggested Questions
3. Don't commit, send, or share the recap anywhere else.
