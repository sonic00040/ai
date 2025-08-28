# Implementation Process Guide for AI Agent

This document outlines the process for the AI agent to log development progress and implementation details.

## Workflow for Implementing Features:1

1.  **Reference the Development Plan:**
    *   Always refer to `docs/development_plan.md` to identify the next feature or step to implement.

2.  **Implement the Feature:**
    *   Execute the necessary commands, write code, or perform other actions to implement the chosen feature.

3.  **Record Progress in `docs/development_progress.md`:**
    *   Once a feature or significant step from `docs/development_plan.md` is successfully implemented, add a concise entry to `docs/development_progress.md`.
    *   The entry should clearly state what was implemented, referencing the plan (e.g., "Completed: Plan 1, Step 1 - Project Setup & Environment").
    *   Include the date of completion.

4.  **Detailed Implementation Notes (Internal to Agent):**
    *   While `docs/implementation_log.md` itself is a guide, the AI agent should maintain its own internal, detailed log of specific tool calls, code snippets, and command outputs that were used to achieve the implementation. This internal log is for the agent's own reference and for debugging/review if needed, but it is not directly written to this file. The user can ask for specific details if required.

## Example Entry for `docs/development_progress.md`:

```markdown
### [Date - e.g., 2025-08-20]

*   **Completed:** Plan 1, Step 1 - Project Setup & Environment
    *   Created project directories.
    *   Initialized Python virtual environment.
    *   Created `.env.example` and `.gitignore`.
```