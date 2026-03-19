# Fairmind Integration — Automated Setup Guide

This file contains step-by-step instructions that any AI coding agent can follow to install the Fairmind Integration framework into a workspace. Each platform section is self-contained.

---

## Detect Your Platform

Before proceeding, identify which platform you are running on:

| Signal | Platform |
|--------|----------|
| You are Claude Code / Anthropic CLI | **Claude Code** |
| You are OpenAI Codex CLI / `codex` command | **OpenAI Codex CLI** |
| You are GitHub Copilot (VS Code, JetBrains, or github.com) | **GitHub Copilot** |
| You are Google Antigravity / Gemini-based IDE | **Google Antigravity** |

Follow ONLY the section for your platform.

---

## Claude Code Setup

### Step 1: Install the plugin

```bash
claude plugin marketplace add FairMind-Gen-AI-Studio/fairmind-integration
claude plugin install fairmind-integration
```

If the marketplace is not available, install from source:

```bash
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git /tmp/fairmind-integration
ln -s /tmp/fairmind-integration ~/.claude/plugins/fairmind-integration
```

### Step 2: Configure MCP Server

```bash
claude mcp add --transport http Fairmind https://project-context.fairmind.ai/mcp/mcp/ --header "Authorization: Bearer ${FAIRMIND_TOKEN}"
```

If `FAIRMIND_TOKEN` is not set, ask the user for their token.

### Step 3: Verify

Confirm the following exist:
- `~/.claude/plugins/fairmind-integration/skills/` — 9 skill directories
- `~/.claude/plugins/fairmind-integration/agents/` — 6 agent files
- MCP server "Fairmind" is configured

### Done

Report to the user:
- 6 agents installed (Atlas, Echo SWE, Echo CR, Tess, Debug Detective, Shield)
- 9 skills installed (fairmind-context, fairmind-tdd, fairmind-code-review, frontend-react-nextjs, backend-nextjs, backend-python, backend-langchain, qa-playwright, ai-ml-systems)
- Fairmind MCP server configured

---

## OpenAI Codex CLI Setup

### Step 1: Clone the framework

```bash
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin
```

### Step 2: Link Codex directories

```bash
# Link .codex directory (contains agents/ and skills -> ../skills symlink)
ln -sfn .fairmind-plugin/.codex .codex
```

### Step 3: Verify structure

Confirm these paths exist:
- `.codex/agents/atlas-tech-lead.toml` — and 5 other TOML files
- `.codex/skills/` — symlink resolving to 9 skill directories

### Step 4: Configure MCP (if applicable)

If the project uses `.codex/config.toml` or equivalent, add:

```toml
[mcp_servers.Fairmind]
type = "http"
url = "https://project-context.fairmind.ai/mcp/mcp/"
```

### Done

Report to the user:
- 6 subagents available: atlas_tech_lead, echo_software_engineer, echo_code_reviewer, tess_qa_engineer, debug_detective, shield_cybersec_engineer
- 9 skills linked via `.codex/skills/`
- Usage: reference agents by name in prompts, e.g. "Have atlas_tech_lead retrieve the plan"

---

## GitHub Copilot Setup

### Step 1: Clone the framework

```bash
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin
```

### Step 2: Link Copilot directories

```bash
# Create .github if it doesn't exist
mkdir -p .github

# Link agents and skills
ln -sfn ../.fairmind-plugin/.github/agents .github/agents
ln -sfn ../.fairmind-plugin/.github/skills .github/skills
```

### Step 3: Verify structure

Confirm these paths exist:
- `.github/agents/atlas-tech-lead.agent.md` — and 5 other `.agent.md` files
- `.github/skills/` — symlink resolving to 9 skill directories

### Step 4: Commit to default branch

For Copilot to discover the agents, they must be on the repository's default branch:

```bash
git add .github/agents/ .github/skills .fairmind-plugin
git commit -m "feat: add Fairmind AI agent framework for Copilot"
```

### Done

Report to the user:
- 6 custom agents available in Copilot: Atlas Tech Lead, Echo Software Engineer, Echo Code Reviewer, Tess QA Engineer, Debug Detective, Shield Cybersec Engineer
- 9 skills available as context
- Agents appear in VS Code Chat panel (agent dropdown), JetBrains, and GitHub.com
- For org-wide setup, move `.github/agents/` to the org's `.github` or `.github-private` repository

---

## Google Antigravity Setup

### Step 1: Clone the framework

```bash
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin
```

### Step 2: Link Antigravity directories

```bash
# Create .agent directory if it doesn't exist
mkdir -p .agent

# Link skills and workflows
ln -sfn ../.fairmind-plugin/.agent/skills .agent/skills
ln -sfn ../.fairmind-plugin/.agent/workflows .agent/workflows
```

### Step 3: Verify structure

Confirm these paths exist:
- `.agent/skills/` — symlink resolving to 9 skill directories, each with a `SKILL.md`
- `.agent/workflows/subagent-atlas-tech-lead.md` — and 5 other workflow files

### Step 4: Global install (optional)

To make skills available across all projects:

```bash
mkdir -p ~/.gemini/antigravity/skills
for skill in .fairmind-plugin/skills/*/; do
  ln -sfn "$(cd "$skill" && pwd)" "$HOME/.gemini/antigravity/skills/$(basename $skill)"
done
```

### Done

Report to the user:
- 9 skills available in `.agent/skills/` — Antigravity will auto-discover them based on task keywords
- 6 subagent workflows available in `.agent/workflows/` for orchestrated delegation
- Skills: fairmind-context, fairmind-tdd, fairmind-code-review, frontend-react-nextjs, backend-nextjs, backend-python, backend-langchain, qa-playwright, ai-ml-systems
- Workflows: Atlas (orchestrator), Echo (engineer), Echo (reviewer), Tess (QA), Debug Detective, Shield (security)

---

## Post-Setup: MCP Server Token

All platforms need access to the Fairmind MCP server. If the user hasn't provided a token yet, ask:

> "To connect to the Fairmind platform, I need your authentication token. You can find it in your Fairmind AI Studio account settings. Please provide your FAIRMIND_TOKEN."

Then configure it for the active platform using the instructions above.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skills not discovered | Verify symlinks resolve correctly: `ls -la .agent/skills/` (or platform equivalent) |
| Agents not appearing | Ensure files are on the default branch (Copilot) or in the correct directory |
| MCP server errors | Check token validity and network access to `project-context.fairmind.ai` |
| Symlink issues on Windows | Use `mklink /D` instead of `ln -s`, or copy files directly |
