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

2. **Edit the file** and replace `YOUR_FAIRMIND_PROJECT_ID` with your actual FairMind project ID.
   To find it, open Claude Code with the FairMind MCP server configured and ask:

   ```
   What's my FairMind project ID?
   ```

   Claude will call `General_list_projects` and return your project ID.

3. **Add secrets** to your repo (Settings > Secrets and variables > Actions):

   | Secret | Description |
   |--------|-------------|
   | `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth token. Generate with `claude setup-token` in your terminal. |
   | `FAIRMIND_API_KEY` | Your FairMind API key for MCP access. |

4. **Open a PR** — the review will trigger automatically.

### What it does

1. **Code review** with implementation coherence verification against FairMind requirements
2. **Journal check** — looks for `.fairmind/journals/TASK-{ID}_*_journal.md` in the PR diff
3. **FairMind task lookup** — fetches acceptance criteria and implementation plans
4. **Coherence assessment** — compares journal/code against requirements
5. **Security spot-check** — crypto, input validation, concurrency, auth, cookies
6. **Structured report** — posted as a PR comment with summary, checklists, and findings
