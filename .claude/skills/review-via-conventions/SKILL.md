---
name: review-via-conventions
description: Review a task file for convention violations
argument-hint: "<path>"
---

Review a single file for violations of the lab authoring conventions. The file must be under `lab/tasks/` or `wiki/`.

## Steps

1. Parse `$ARGUMENTS` to get the file path. Accept paths under `lab/tasks/` (e.g., `lab/tasks/setup.md`, `lab/tasks/required/task-2.md`) or `wiki/` (e.g., `wiki/web-development.md`). If the path is missing or does not point to a file under one of these directories, ask the user.
2. Read the target file.
3. Read the convention files that apply to the target file:
   - **For `lab/tasks/` files:**
     - `instructors/context/conventions/common.md` — writing conventions (4.1–4.23)
     - `instructors/context/conventions/tasks.md` — task structure (Section 3) and design principles (Section 12)
   - **For `wiki/` files:**
     - `instructors/context/conventions/common.md` — writing conventions (4.1–4.23)
     - `instructors/context/conventions/wiki.md` — wiki file structure and section patterns
4. Go through the target file **line by line**. Check it against **every** convention in both files. Flag each violation with its line number.
5. Scan for `<!-- TODO ... -->` comments. Report each one with its line number and the comment text.
6. Scan for empty sections: a heading immediately followed by another heading, a `<!-- TODO ... -->` comment, or end of file, with no real content lines in between. Report each empty section with its line number and heading text.

## Rules

- The convention files are the single source of truth. Check every rule they contain — do not skip any.
- Do not invent rules beyond what the convention files state.
- Be strict: flag every violation, no matter how small.
- Do not fix anything — only report.
- If a convention does not apply to the file (e.g., the file has no Docker commands), skip that category and note "Not applicable."
- For `lab/tasks/setup.md`: skip task-only conventions (Section 3 template, acceptance criteria format). Apply all `common.md` conventions.

## Output format

Write the report to `tmp/review-via-conventions/<repo-root-path>`, where `<repo-root-path>` is the file's path from the repository root (e.g., `tmp/review-via-conventions/lab/tasks/setup.md` for `lab/tasks/setup.md`, `tmp/review-via-conventions/wiki/web-development.md` for `wiki/web-development.md`). Create intermediate directories if they do not exist.

The report must be self-contained so another session or agent can act on it without extra context. Structure:

1. **Header** — file path reviewed, date, convention files used.
2. **Findings** — grouped by convention number (e.g., "4.2. Terminal commands", "Section 3. Task document structure"). Under each group, list findings as numbered items with line numbers. If a group has no findings, write "No issues found."
3. **TODOs** — list every `<!-- TODO ... -->` comment with its line number and text. If none, write "No TODOs found."
4. **Empty sections** — list every heading that has no content (only a TODO comment, another heading, or EOF follows). Include line number and heading text. If none, write "No empty sections found."
5. **Summary** — total violation count (conventions + TODOs + empty sections) and a short overall assessment.

After writing the file, print its path in the conversation so the user can find it.
