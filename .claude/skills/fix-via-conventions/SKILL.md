---
name: fix-via-conventions
description: Fix convention violations found by /review-via-conventions
argument-hint: "<path>"
---

Fix convention violations in a file using the report produced by `/review-via-conventions`.

## Steps

1. Parse `$ARGUMENTS` to get the file path. Accept paths under `lab/tasks/` (e.g., `lab/tasks/setup.md`, `lab/tasks/required/task-2.md`) or `wiki/` (e.g., `wiki/web-development.md`). If the path is missing or does not point to a file under one of these directories, ask the user.
2. Derive the report path: `tmp/review-via-conventions/<repo-root-path>`, where `<repo-root-path>` is the target file's path from the repository root (e.g., `tmp/review-via-conventions/lab/tasks/required/task-1.md` for `lab/tasks/required/task-1.md`, `tmp/review-via-conventions/wiki/web-development.md` for `wiki/web-development.md`). If the report file does not exist, tell the user to run `/review-via-conventions <path>` first and stop.
3. Read the report file.
4. Read the target file.
5. Read the convention files referenced in the report header so every fix is grounded in the actual convention text:
   - **For `lab/tasks/` files:**
     - `instructors/context/conventions/common.md`
     - `instructors/context/conventions/tasks.md`
   - **For `wiki/` files:**
     - `instructors/context/conventions/common.md`
     - `instructors/context/conventions/wiki.md`
6. Work through the report **Findings** one group at a time. For each violation, apply the minimal edit that resolves it. Use line numbers from the report as a starting guide, but always verify against the current file content (earlier fixes may shift lines).
7. Work through the report **Empty sections**. For each empty section that has no `<!-- TODO ... -->` marker, add `<!-- TODO fill in this section -->` directly below the heading. Empty sections that already contain a `<!-- TODO ... -->` cannot be auto-fixed — skip them and note them in the summary.
8. **TODOs** cannot be auto-fixed — they require content that only the author can supply. List them all as skipped in the summary.

## Rules

- The report is the single source of truth for *what* to fix. Do not look for additional violations beyond those listed in the report.
- Each fix must satisfy the convention cited in the report. When in doubt, re-read the convention text.
- Make the smallest change that resolves each violation. Do not rewrite surrounding text, reorder sections, or make stylistic changes unrelated to a reported violation.
- Preserve the author's voice and intent. Rephrase only when required by a convention.
- If a reported violation is ambiguous or cannot be fixed without changing the meaning of the content, skip it and note it in the summary.

## Output

After all fixes are applied, print a short summary listing:
- Number of convention violations fixed.
- Number of empty sections fixed (TODO marker added).
- Number of items skipped (empty sections already marked, TODOs), with reasons.
