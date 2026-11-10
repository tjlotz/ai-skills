---
name: big-brain
description: Scopes a feature before you start building — works through a plan conversationally and updates the plan with an agreed task checklist so you're ready to code. Pairs with cook-bruv, this-sus, and yeet-it.
license: MIT
compatibility: opencode, claude
---

## What I do

- Accepts a standard description of a feature or bugfix
- Asks focused questions one at a time to understand the feature, constraints, and context
- Proposes a concrete task breakdown and iterates until the user confirms the plan
- Signals clearly when the scope is agreed and the issue is ready — so you can start building with confidence

## When to use me

Use me at the start of any non-trivial piece of work, before writing a single line of code. Common scenarios:

- You have an bug that needs fleshing out before you start
- You have an idea in your head but no plan yet — I'll help you shape and capture it
- You've been talking through an idea mid-conversation and want to formalize it into an official plan — just invoke me and I'll pick up where the conversation left off
- A `this-sus` session surfaced issues you want to track and plan — scope them into a new plan
- You want a clear task checklist to work from so nothing falls through the cracks

Invoke me with: `/big-brain [optional context]`

Examples:
- `/big-brain` — scope and refine an existing idea from the conversation
- `/big-brain [feature proposal]` — start from scratch, create a new task list

## Instructions

### Step 1: Detect input

There are two modes of invocation — detect which applies:

**Mode A — No context given, prior conversation exists:**

If the user has already been discussing an idea or feature in the current conversation, do not ask them to re-explain it. You already have the context. Briefly summarize what you understand them to want (1-2 sentences) and ask if that's the right starting point before moving to step 2.

**Mode C — No context given, no prior context in the coversation:**

Start the conversation cold from step 2.

---

### Step 2: Understand the feature (conversational)

Ask questions **one at a time** — do not present a list of questions all at once. Wait for the user's answer before asking the next question. The goal is to build a shared understanding of the work before proposing a plan.

Key things to uncover (not a script — adapt based on what you already know from the issue, prior conversation, or prior answers):

- What problem does this solve, or what is the user trying to build?
- Who is affected or benefits from this?
- Are there any known constraints, dependencies on other work, or things that are explicitly out of scope?
- Are there existing patterns, components, or conventions in the codebase this should follow?
- Are there any open questions or risks that should be noted?

Skip any question already clearly answered by the issue or prior conversation. Only ask about genuine gaps.

Keep the conversation tight — 2 to 4 questions is usually enough. Stop asking when you have enough to write a solid plan.

---

### Step 3: Propose a task breakdown

Once you have enough context, propose a concrete task list. Format it clearly:

```
Here's how I'd break this down:

1. <task one>
2. <task two>
3. <task three>
...

Does this cover everything, or is there anything missing, wrong, or that should be reordered?
```

Be specific — tasks should be actionable, not vague. "Add validation to the form submit handler" is better than "handle validation".

---

### Step 4: Iterate until agreed

Refine the plan based on the user's feedback. Add, remove, reorder, or reword tasks as needed. Keep iterating until the user explicitly confirms the plan is good to go.

Do not proceed to step 5 until you have clear confirmation.

---

### Step 5: Write the task list

Format the issue body as follows:

```markdown
## Background
<1-2 sentences summarizing the problem or goal>

## Tasks
- [ ] task one
- [ ] task two
- [ ] task three
```

Keep the background concise and factual. The task list should exactly reflect the agreed plan from step 4 — do not add or remove tasks at this stage.

---

### Step 6: Signal ready

Confirm that the plan has been created or updated and tell the user they're scoped and ready to build.

Example closing message:
```
Your big-brain idea is dope. Let's cook, fam.
```

**STOP HERE.**

Do not enter plan mode, start coding, create files, run commands, or take any implementation action. Your job is complete. The user will explicitly tell you when to proceed with the work.
