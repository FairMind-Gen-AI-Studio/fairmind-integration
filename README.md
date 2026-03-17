# Fairmind Integration — Multi-Platform AI Agent Framework

A cross-platform agent framework providing team collaboration with role-based agents and technology-specific skills. Works natively with **Claude Code**, **OpenAI Codex CLI**, **GitHub Copilot**, and **Google Antigravity**. Features deep Fairmind platform integration with full traceability from implementation plans to code review.

## Overview

This plugin provides **6 role-based agents** and **9 technology-specific skills**, creating a complete team collaboration workflow with the Fairmind AI Studio platform. Agents focus on roles (what they do), while skills provide technology expertise (how they do it).

All agents and skills are defined once and mapped to each platform's native format via symlinks and platform-specific profile files.

## Key Features

**6 Role-Based Agents**
- **Atlas (Tech Lead)** - Orchestration, plan adaptation, coordination
- **Echo (Software Engineer)** - All implementation work (frontend, backend, AI)
- **Tess (QA Engineer)** - Test execution and validation
- **Echo (Code Reviewer)** - Code quality and standards review
- **Debug Detective** - Complex debugging scenarios
- **Shield (Cybersecurity)** - Security analysis and validation

**9 Technology Skills**
- `fairmind-context` - Intelligent context gathering from Fairmind platform
- `fairmind-tdd` - Test-driven development workflow
- `fairmind-code-review` - Three-layer verification (plan-journal-code)
- `frontend-react-nextjs` - React, NextJS, TypeScript, Tailwind, Shadcn
- `backend-nextjs` - NextJS API routes, MongoDB, authentication
- `backend-python` - FastAPI, Pydantic, async patterns
- `backend-langchain` - LangChain, LangGraph, RAG patterns
- `qa-playwright` - Playwright test patterns, selectors, CI integration
- `ai-ml-systems` - LLM optimization, agent architecture, evaluation

**Complete Workflow**
- Atlas adapts Fairmind plans for the Software Engineer
- Echo implements using appropriate skills and TDD with journal tracking
- Tess validates with Playwright tests
- Code Reviewer verifies against plans and requirements
- Shield performs security review

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTS (Roles)                            │
├─────────────────────────────────────────────────────────────────┤
│  Atlas        Echo (SWE)     Tess (QA)    Code Reviewer  Shield │
│  (Tech Lead)  (implements)   (tests)      (reviews)      (sec)  │
└──────┬────────────┬────────────┬────────────┬──────────────┬────┘
       │            │            │            │              │
       ▼            ▼            ▼            ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SKILLS (Capabilities)                      │
├─────────────────────────────────────────────────────────────────┤
│  Fairmind Skills:                                                │
│  • fairmind-context    • fairmind-tdd    • fairmind-code-review │
│                                                                  │
│  Technology Skills:                                              │
│  • frontend-react-nextjs   • backend-nextjs   • backend-python  │
│  • backend-langchain       • qa-playwright    • ai-ml-systems   │
└─────────────────────────────────────────────────────────────────┘
```

## Requirements

### Fairmind MCP Server

This plugin **requires** the Fairmind MCP server to be installed and configured. The server provides 40 tools across three categories:

**General Tools (13):** Project/session management, document access, RAG retrieval
**Studio Tools (21):** Needs, user stories, tasks, requirements, test management
**Code Tools (6):** Cross-repository search, analysis, and integration verification

### MCP Server Configuration

**Option 1: Using settings.json**

Add to your `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
  "mcpServers": {
    "Fairmind": {
      "type": "http",
      "url": "https://project-context.fairmind.ai/mcp/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**Option 2: Using Claude CLI**

```bash
claude mcp add --transport http Fairmind https://project-context.fairmind.ai/mcp/mcp/ --header "Authorization: Bearer YOUR_TOKEN_HERE"
```

Replace `YOUR_TOKEN_HERE` with your Fairmind authentication token.

## Installation

### Prerequisites

All platforms require the **Fairmind MCP Server** (see [MCP Server Configuration](#mcp-server-configuration) below).

---

### Claude Code

**Option A: From Marketplace (Recommended)**

```bash
# Add the marketplace and install
claude plugin marketplace add FairMind-Gen-AI-Studio/fairmind-integration
claude plugin install fairmind-integration

# Or install for a specific project only
cd your-project
claude plugin install fairmind-integration --scope project
```

**Option B: From Source**

```bash
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git

# Global install (all projects)
ln -s $(pwd)/fairmind-integration ~/.claude/plugins/fairmind-integration

# Or project-local install
cp -r fairmind-integration /path/to/your/project/.claude/plugins/fairmind-integration
```

**Option C: Team Auto-Install**

Add to your repository's `.claude/settings.json`:

```json
{
  "plugins": {
    "marketplaces": ["default"],
    "install": ["fairmind-integration"]
  }
}
```

Skills are loaded from `skills/` and agents from `agents/` automatically.

---

### OpenAI Codex CLI

Codex discovers subagents from `~/.codex/agents/` (global) or `.codex/agents/` (project). Skills are loaded from `.codex/skills/`.

**Option A: Clone into your project (Recommended)**

```bash
cd your-project

# Clone as a subdirectory or submodule
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin

# Symlink .codex into project root
ln -s .fairmind-plugin/.codex .codex
```

The `.codex/skills` symlink already points to `skills/`, and `.codex/agents/` contains all 6 TOML subagent definitions.

**Option B: Global install**

```bash
# Copy agents to global Codex config
cp .codex/agents/*.toml ~/.codex/agents/

# Copy skills to global Codex skills (create if needed)
mkdir -p ~/.codex/skills
cp -r skills/* ~/.codex/skills/
```

**Referencing subagents in prompts:**

```
"Have atlas_tech_lead retrieve the plan, then echo_software_engineer implement it."
```

See the [Codex subagents documentation](https://simonwillison.net/2026/Mar/16/codex-subagents/) and [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) for more details.

---

### GitHub Copilot

Copilot discovers custom agents from `.github/agents/` in your repository. Skills in `.github/skills/` are available as context. No installation step needed — just commit the files.

**Option A: Clone into your project (Recommended)**

```bash
cd your-project

git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin

# Symlink Copilot directories into project root
ln -s .fairmind-plugin/.github/agents .github/agents
ln -s .fairmind-plugin/.github/skills .github/skills
```

**Option B: Copy directly**

```bash
# Copy agent profiles
mkdir -p .github/agents
cp .github/agents/*.agent.md your-project/.github/agents/

# Symlink skills
ln -s /path/to/fairmind-integration/skills your-project/.github/skills
```

**Option C: Organization-wide**

Place agent profiles in your org's `.github` or `.github-private` repository under `agents/` to make them available across all repositories:

```
your-org/.github/
└── agents/
    ├── atlas-tech-lead.agent.md
    ├── echo-software-engineer.agent.md
    └── ...
```

Once committed to the default branch, agents appear automatically in VS Code (Chat panel → agent dropdown), JetBrains, and GitHub.com Copilot.

See the [GitHub Copilot custom agents documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents) for more details.

---

### Google Antigravity

Antigravity discovers skills from `.agent/skills/` (workspace) or `~/.gemini/antigravity/skills/` (global). Workflows in `.agent/workflows/` provide subagent orchestration patterns.

**Option A: Clone into your project (Recommended)**

```bash
cd your-project

git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git .fairmind-plugin

# Symlink Antigravity directories into project root
ln -s .fairmind-plugin/.agent/skills .agent/skills
ln -s .fairmind-plugin/.agent/workflows .agent/workflows
```

**Option B: Global install**

```bash
# Copy skills to global Antigravity directory
mkdir -p ~/.gemini/antigravity/skills
cp -r skills/* ~/.gemini/antigravity/skills/

# Copy workflows
mkdir -p ~/.gemini/antigravity/global_workflows
cp .agent/workflows/*.md ~/.gemini/antigravity/global_workflows/
```

**Option C: Direct workspace install**

```bash
mkdir -p .agent/skills .agent/workflows

# Symlink each skill (or copy)
for skill in skills/*/; do
  ln -s "../../$skill" ".agent/skills/$(basename $skill)"
done

# Copy workflow definitions
cp .agent/workflows/*.md your-project/.agent/workflows/
```

Skills are automatically discovered by Antigravity when placed in `.agent/skills/`. The agent matches keywords from each `SKILL.md` description to determine which skill to load for the current task.

See the [Antigravity skills tutorial](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) and the [skills placement guide](https://medium.com/google-cloud/confused-about-where-to-put-your-agent-skills-ea778f3c64f3) for more details.

## CI/CD: Automated Code Review

AI-powered code review pipeline with FairMind requirements verification. Copy the workflow into your repo and every PR gets reviewed automatically.

See **[ci/](./ci/)** for the workflow file and setup instructions.

## Cross-Platform Architecture

Skills are defined once in `skills/` and shared across all platforms via symlinks. Agents are translated into each platform's native format.

```
Platform          Skills Discovery Path      Agents/Subagents Path            Format
────────────────  ─────────────────────────  ───────────────────────────────  ──────────────
Claude Code       skills/ (direct)           agents/*.md                      Markdown
OpenAI Codex      .codex/skills/ → skills/   .codex/agents/*.toml             TOML
GitHub Copilot    .github/skills/ → skills/  .github/agents/*.agent.md        Markdown+YAML
Antigravity       .agent/skills/ → skills/   .agent/workflows/subagent-*.md   Workflow MD
```

### Repository Structure

```
fairmind-integration/
│
├── skills/                          # Canonical skill definitions (single source of truth)
│   ├── fairmind-context/SKILL.md
│   ├── fairmind-tdd/SKILL.md
│   ├── fairmind-code-review/SKILL.md
│   ├── frontend-react-nextjs/SKILL.md + references/
│   ├── backend-nextjs/SKILL.md + references/
│   ├── backend-python/SKILL.md + references/
│   ├── backend-langchain/SKILL.md + references/
│   ├── qa-playwright/SKILL.md + references/
│   └── ai-ml-systems/SKILL.md + references/
│
├── agents/                          # Claude Code agents (canonical definitions)
│   ├── tech-lead.md                 # Atlas - orchestration
│   ├── software-engineer.md         # Echo - all implementation
│   ├── qa-engineer.md               # Tess - testing
│   ├── code-reviewer.md             # Echo - code review
│   ├── debug-detective.md           # Debugging specialist
│   └── cybersec-engineer.md         # Shield - security
│
├── .codex/                          # OpenAI Codex CLI
│   ├── skills -> ../skills          # Symlink to shared skills
│   └── agents/                      # TOML subagent definitions
│       ├── atlas-tech-lead.toml
│       ├── echo-software-engineer.toml
│       ├── echo-code-reviewer.toml
│       ├── tess-qa-engineer.toml
│       ├── debug-detective.toml
│       └── shield-cybersec-engineer.toml
│
├── .github/                         # GitHub Copilot
│   ├── skills -> ../skills          # Symlink to shared skills
│   └── agents/                      # Markdown+YAML agent profiles
│       ├── atlas-tech-lead.agent.md
│       ├── echo-software-engineer.agent.md
│       ├── echo-code-reviewer.agent.md
│       ├── tess-qa-engineer.agent.md
│       ├── debug-detective.agent.md
│       └── shield-cybersec-engineer.agent.md
│
├── .agent/                          # Google Antigravity
│   ├── skills -> ../skills          # Symlink to shared skills
│   └── workflows/                   # Workflow-based subagent definitions
│       ├── subagent-atlas-tech-lead.md
│       ├── subagent-echo-software-engineer.md
│       ├── subagent-echo-code-reviewer.md
│       ├── subagent-tess-qa-engineer.md
│       ├── subagent-debug-detective.md
│       └── subagent-shield-cybersec-engineer.md
│
├── .claude-plugin/
│   └── marketplace.json             # Claude Code marketplace metadata
├── commands/                        # Slash commands
│   └── fix-issue.md
├── ci/                              # CI/CD automated code review
└── README.md
```

## Agents

### Atlas (Tech Lead)

**Role:** Orchestration and coordination - NEVER implements code

**Responsibilities:**
- Retrieves implementation plans from Fairmind
- Adapts plans for Echo (Software Engineer)
- Specifies which skill(s) to load for each task
- Monitors progress through journals
- Coordinates validation with Tess and Code Reviewer

### Echo (Software Engineer)

**Role:** All implementation work

**Specializes dynamically** by loading appropriate skills:
- Frontend work: `frontend-react-nextjs`
- Backend (NextJS): `backend-nextjs`
- Backend (Python): `backend-python`
- AI/LLM work: `backend-langchain` + `ai-ml-systems`

**Workflow:**
1. Read work package from Atlas
2. Load required skill(s)
3. Implement following skill patterns
4. Document in journal
5. Mark completion

### Tess (QA Engineer)

**Role:** Test execution and validation

**Responsibilities:**
- Execute test plans from work packages
- Use `qa-playwright` skill for Playwright patterns
- Validate against acceptance criteria
- Generate validation reports

### Echo (Code Reviewer)

**Role:** Code quality verification

**Three-Layer Verification:**
1. Plan compliance (plan vs journal)
2. Requirements compliance (code vs acceptance criteria)
3. Integration verification (cross-repo contracts)

**Uses skills for context:** Can load technology skills to understand expected patterns.

### Debug Detective

**Role:** Complex debugging scenarios

**Capabilities:**
- Root cause analysis
- Cross-service debugging
- Performance investigation

### Shield (Cybersecurity Expert)

**Role:** Security analysis and validation

**Responsibilities:**
- Security code review
- Vulnerability assessment
- Security architecture review
- Compliance verification

## Skills

### Fairmind Integration Skills

**fairmind-context**
- Intelligent context gathering from Fairmind platform
- Used by all other skills as foundation

**fairmind-tdd**
- Test-driven development aligned with acceptance criteria
- Red-Green-Refactor with journal tracking

**fairmind-code-review**
- Three-layer verification system
- Plan → Journal → Code traceability

### Technology Skills

Each technology skill includes:
- `SKILL.md` - Workflow and when to use
- `references/` - Detailed patterns, examples, best practices

**frontend-react-nextjs**
- Component patterns, hooks, state management
- NextJS App Router, server components
- TypeScript, Tailwind CSS, Shadcn UI

**backend-nextjs**
- API route design and middleware
- MongoDB patterns and optimization
- Authentication with NextAuth

**backend-python**
- FastAPI patterns and best practices
- Pydantic models and validation
- Async patterns and testing

**backend-langchain**
- LangChain chains and LCEL
- LangGraph agents and workflows
- RAG patterns and prompt engineering

**qa-playwright**
- Test organization and fixtures
- Selector strategies
- Visual testing and CI integration

**ai-ml-systems**
- LLM optimization and model selection
- Multi-agent architecture patterns
- Evaluation and cost optimization

## Team Workflow Example

```
1. Atlas (Tech Lead)
   └─ get_task("TASK-123") → Retrieve Fairmind implementation plan
   └─ Analyze: "This needs React frontend + Node.js API"
   └─ Create work package specifying skills to load
   └─ Write to .fairmind/<project>/<session>/work_packages/frontend/TASK-123_workpackage.md

2. Echo (Software Engineer)
   └─ Read work_packages/frontend/TASK-123_workpackage.md
   └─ Load `frontend-react-nextjs` skill
   └─ Use fairmind-tdd skill → Implement with TDD
   └─ Update .fairmind/<project>/<session>/journals/TASK-123_echo_journal.md
   └─ Create completion flag

3. Tess (QA Engineer)
   └─ Load `qa-playwright` skill
   └─ Execute test scenarios
   └─ Create validation report

4. Echo (Code Reviewer)
   └─ Use fairmind-code-review skill
   └─ Load relevant technology skill for context
   └─ Verify: Plan → Journal → Code traceability
   └─ Provide structured feedback
```

## Usage Examples

### Starting New Development Work

```bash
# Atlas retrieves and adapts the plan
@tech-lead retrieve task TASK-456 and create work packages

# Echo implements with appropriate skill
@software-engineer implement the work package for TASK-456

# Tess validates
@qa-engineer run tests for TASK-456

# Review the implementation
@code-reviewer review TASK-456 implementation
```

### Using the Fix Issue Command

```bash
# Automatically classify and fix an issue
/fix-issue login-bug

# Specify issue type explicitly
/fix-issue login-bug --type fe-be
```

## Directory Structure Created by Workflow

Atlas resolves the active project and session from FairMind, slugifies both, and scopes all artifacts under `.fairmind/<project-slug>/<session-slug>/`:

```
your-project/
├── .fairmind/
│   ├── active-context.json          # Pointer to current session
│   └── <project-slug>/
│       └── <session-slug>/
│           ├── context.json         # Full project/session metadata
│           ├── execution_plans/
│           ├── requirements/
│           │   ├── needs/
│           │   ├── user_stories/
│           │   └── technical_tasks/
│           │       └── tests/
│           ├── attachments/
│           ├── blueprints/
│           ├── journals/            # Agent progress tracking
│           ├── work_packages/       # Atlas-adapted plans for agents
│           │   ├── frontend/
│           │   ├── backend/
│           │   ├── ai/
│           │   ├── qa/
│           │   └── fixes/
│           ├── validation_results/  # Test and review reports
│           └── coordination_logs/
└── [your code]
```

## Configuration

### Project-Specific Settings

Create `.claude/settings.json` in your project:

```json
{
  "fairmind": {
    "defaultProject": "your-project-id",
    "journalPath": ".fairmind/<project-slug>/<session-slug>/journals",
    "workPackagePath": ".fairmind/<project-slug>/<session-slug>/work_packages"
  }
}
```

### Team Settings

For consistent team setup, commit `.claude/settings.json` with:

```json
{
  "plugins": {
    "install": ["fairmind-integration"]
  },
  "mcpServers": {
    "Fairmind": {
      "type": "http",
      "url": "https://project-context.fairmind.ai/mcp/mcp/",
      "headers": {
        "Authorization": "Bearer ${env:FAIRMIND_TOKEN}"
      }
    }
  }
}
```

## Best Practices

1. **Always start with Atlas** for new Fairmind tasks - let it adapt the plan and specify skills
2. **Load skills before implementation** - skills provide patterns and examples
3. **Follow fairmind-tdd** for implementation - maintains traceability
4. **Update journals regularly** - enables meaningful code review
5. **Use skill references** - each skill has detailed reference files

## Version History

**3.0.0** (2026-03-17)
- Cross-platform support: Claude Code, OpenAI Codex CLI, GitHub Copilot, Google Antigravity
- Skills unified under `skills/` with symlinks for each platform
- Added 6 Codex TOML subagents in `.codex/agents/`
- Added 6 Copilot agent profiles in `.github/agents/` (Markdown + YAML frontmatter)
- Added 6 Antigravity workflow subagents in `.agent/workflows/`
- CI/CD automated code review pipeline

**2.0.0** (2024-12-04)
- Reorganized from 12 function-specific agents to 6 role-based agents
- Added 6 new technology-specific skills with reference files
- Consolidated frontend, backend, AI engineers into single Software Engineer
- Skills now provide technology expertise, agents focus on roles
- Updated fix-issue command to use new structure

**1.0.0** (2025-10-28)
- Initial release with 12 specialized agents
- 3 Fairmind-aware skills
- Complete plan→journal→code workflow

## License

MIT

## Contributing

Contributions welcome! Please:
1. Follow existing agent/skill patterns
2. Test thoroughly with Fairmind MCP server
3. Update documentation
4. Submit PR with clear description

## Acknowledgments

Built for [Claude Code](https://claude.com/claude-code) by Anthropic.
Cross-platform support for [OpenAI Codex CLI](https://github.com/openai/codex), [GitHub Copilot](https://github.com/features/copilot), and [Google Antigravity](https://antigravity.google).
Integrates with [Fairmind AI Studio](https://fairmind.ai) platform.

## Support

- **Issues:** https://github.com/FairMind-Gen-AI-Studio/fairmind-integration/issues
- **Fairmind Support:** support@fairmind.ai
