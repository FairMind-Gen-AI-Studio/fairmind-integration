# CI/CD Pipelines

Ready-to-use workflow files for integrating FairMind with your CI/CD pipeline.

## FairMind Code Review

**[fairmind-code-review.yml](./fairmind-code-review.yml)** — AI-powered code review with FairMind requirements verification.

Every PR gets reviewed by Claude, which also verifies that the implementation is coherent with your FairMind user stories, tasks, and acceptance criteria.

### Setup

1. **Copy the file** into your repo:

   ```bash
   mkdir -p .github/workflows
   curl -o .github/workflows/fairmind-code-review.yml \
     https://raw.githubusercontent.com/FairMind-Gen-AI-Studio/fairmind-integration/main/ci/fairmind-code-review.yml
   ```

2. **Set your project ID** — open the file and change the `FAIRMIND_PROJECT_ID` env var at the top:

   ```yaml
   env:
     FAIRMIND_PROJECT_ID: "your-actual-project-id"
   ```

   Don't know your project ID? Open Claude Code with the FairMind MCP server configured and ask *"What's my FairMind project ID?"*

3. **Add secrets** to your repo (Settings > Secrets and variables > Actions):

   | Secret | Description |
   |--------|-------------|
   | `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth token. Generate with `claude setup-token` in your terminal. |
   | `FAIRMIND_API_KEY` | Your FairMind API key for MCP access. |

4. **Open a PR** — the review will trigger automatically.

### Prerequisites

This pipeline works best when the **FairMind coding agents** are used from the start to implement tasks from your Project Context. The agents produce journals (`.fairmind/journals/`) and follow the implementation plans defined in FairMind, giving the reviewer full traceability between requirements and code. Without that workflow, the review falls back to analyzing the raw diff — still useful, but less precise.

### What it does

1. **Code review** with implementation coherence verification against FairMind requirements
2. **Journal check** — looks for `.fairmind/journals/TASK-{ID}_*_journal.md` in the PR diff
3. **FairMind task lookup** — fetches acceptance criteria and implementation plans
4. **Coherence assessment** — compares journal/code against requirements
5. **Security spot-check** — crypto, input validation, concurrency, auth, cookies
6. **Structured report** — posted as a PR comment with summary, checklists, and findings
