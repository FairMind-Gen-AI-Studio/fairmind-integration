# Fairmind Integration Extension for Gemini CLI

A comprehensive Gemini CLI extension providing team collaboration with role-based agents and technology-specific skills. Features deep Fairmind platform integration with full traceability from implementation plans to code review.

## Overview

This extension extends Gemini CLI with **6 role-based agents** and **9 technology-specific skills**, creating a complete team collaboration workflow with the Fairmind AI Studio platform. Agents focus on roles (what they do), while skills provide technology expertise (how they do it).

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

**20 Custom Commands** (TOML format)
- `/fix-issue` - Enhanced issue fix orchestrator
- `/gh-commit` - Smart conventional commits
- `/gh-review-pr` - PR review workflow
- `/security-audit` - Security assessment
- `/migrate-to-k8s` - Kubernetes migration
- `/ultra-think` - Deep analysis mode
- And 14 more...

**Complete Workflow**
- Atlas adapts Fairmind plans for the Software Engineer
- Echo implements using appropriate skills and TDD with journal tracking
- Tess validates with Playwright tests
- Code Reviewer verifies against plans and requirements
- Shield performs security review

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        AGENTS (Roles)                            │
├──────────────────────────────────────────────────────────────────┤
│  Atlas        Echo (SWE)     Tess (QA)    Code Reviewer   Shield │
│  (Tech Lead)  (implements)   (tests)      (reviews)       (sec)  │
└──────┬────────────┬────────────┬────────────┬───────────────┬────┘
       │            │            │            │               │
       ▼            ▼            ▼            ▼               ▼
┌──────────────────────────────────────────────────────────────────┐
│                       SKILLS (Capabilities)                      │
├──────────────────────────────────────────────────────────────────┤
│  Fairmind Skills:                                                │
│  • fairmind-context    • fairmind-tdd    • fairmind-code-review  │
│                                                                  │
│  Technology Skills:                                              │
│  • frontend-react-nextjs   • backend-nextjs   • backend-python   │
│  • backend-langchain       • qa-playwright    • ai-ml-systems    │
└──────────────────────────────────────────────────────────────────┘
```

## Requirements

### Fairmind MCP Server

This extension **requires** the Fairmind MCP server to be configured. The server provides 40 tools across three categories:

- **General Tools (13):** Project/session management, document access, RAG retrieval
- **Studio Tools (21):** Needs, user stories, tasks, requirements, test management
- **Code Tools (6):** Cross-repository search, analysis, and integration verification

### MCP Server Configuration

Add to your `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "Fairmind": {
      "type": "http",
      "url": "https://project-context.mindstream.fairmind.ai/mcp/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_HERE` with your Fairmind authentication token.

## Installation

### Option 1: Install from GitHub (Recommended)

```bash
gemini extensions install https://github.com/FairMind-Gen-AI-Studio/fairmind-integration
```

To update after changes are pushed:

```bash
gemini extensions update fairmind-integration
```

### Option 2: Install from Local Path

```bash
# Clone the repository
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git

# Install from local path (creates a copy in ~/.gemini/extensions/)
gemini extensions install --path ./fairmind-integration
```

### Option 3: Symlink for Development

For active development with live changes (no need to reinstall after edits):

```bash
ln -s /path/to/fairmind-integration ~/.gemini/extensions/fairmind-integration
```

### Verify Installation

```bash
gemini extensions list
```

### Uninstall

```bash
gemini extensions uninstall fairmind-integration
```

## Extension Structure

```
fairmind-integration/
├── gemini-extension.json            # Extension manifest
├── GEMINI.md                        # Extension context file
├── agents/                          # 6 role-based subagents
│   ├── tech-lead.md                 # Atlas - orchestration
│   ├── software-engineer.md         # Echo - all implementation
│   ├── qa-engineer.md               # Tess - testing
│   ├── code-reviewer.md             # Echo - code review
│   ├── debug-detective.md           # Debugging specialist
│   └── cybersec-engineer.md         # Shield - security
├── commands/                        # 20 custom commands (TOML)
│   ├── fix-issue.toml
│   ├── gh-commit.toml
│   ├── gh-review-pr.toml
│   ├── security-audit.toml
│   ├── ultra-think.toml
│   └── ...
├── skills/                          # 9 technology skills
│   ├── fairmind-context/
│   │   └── SKILL.md
│   ├── fairmind-tdd/
│   │   └── SKILL.md
│   ├── fairmind-code-review/
│   │   └── SKILL.md
│   ├── frontend-react-nextjs/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── react-patterns.md
│   │       ├── nextjs-conventions.md
│   │       ├── typescript-guidelines.md
│   │       ├── tailwind-shadcn.md
│   │       └── zustand-state.md
│   ├── backend-nextjs/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── api-routes.md
│   │       ├── mongodb-patterns.md
│   │       ├── authentication.md
│   │       └── error-handling.md
│   ├── backend-python/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── fastapi-patterns.md
│   │       ├── pydantic-models.md
│   │       ├── async-patterns.md
│   │       └── testing-patterns.md
│   ├── backend-langchain/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── chain-patterns.md
│   │       ├── agent-patterns.md
│   │       ├── rag-patterns.md
│   │       ├── prompt-engineering.md
│   │       └── memory-patterns.md
│   ├── qa-playwright/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── test-patterns.md
│   │       ├── selectors.md
│   │       ├── visual-testing.md
│   │       ├── mcp-tools.md
│   │       └── ci-integration.md
│   └── ai-ml-systems/
│       ├── SKILL.md
│       └── references/
│           ├── llm-optimization.md
│           ├── agent-architecture.md
│           ├── evaluation-patterns.md
│           └── cost-optimization.md
├── workflow-templates/              # CI/CD workflow templates
│   ├── gemini-cli-review.yml
│   └── gemini-cli-review.properties.json
├── directive/                       # Local directive examples
│   └── fairmind-local-directive.md.example
├── scripts/                         # Utility scripts
│   └── analyze_sonarqube.py
└── docs/
    └── architecture-evolution.md
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

Uses technology skills for context when reviewing domain-specific code.

### Debug Detective

**Role:** Complex debugging scenarios

**Capabilities:**
- Methodical root cause analysis
- Cross-service debugging via Fairmind Code tools
- Performance investigation
- Race condition and memory leak detection

### Shield (Cybersecurity Expert)

**Role:** Security analysis and final validation gate

**Responsibilities:**
- Security code review (OWASP Top 10)
- Vulnerability assessment (CVSS scoring)
- Threat modeling (STRIDE methodology)
- Compliance verification

## Skills

### Fairmind Integration Skills

| Skill | Purpose |
|-------|---------|
| `fairmind-context` | Intelligent context gathering from Fairmind platform. Used by all other skills as foundation. |
| `fairmind-tdd` | Test-driven development aligned with acceptance criteria. Red-Green-Refactor with journal tracking. |
| `fairmind-code-review` | Three-layer verification system: Plan -> Journal -> Code traceability. |

### Technology Skills

Each technology skill includes a `SKILL.md` with workflow guidance and a `references/` directory with detailed patterns, examples, and best practices.

| Skill | Coverage |
|-------|----------|
| `frontend-react-nextjs` | React components, hooks, NextJS App Router, TypeScript, Tailwind CSS, Shadcn UI, Zustand |
| `backend-nextjs` | API route design, MongoDB patterns, NextAuth authentication, error handling |
| `backend-python` | FastAPI patterns, Pydantic models, async patterns, pytest testing |
| `backend-langchain` | LangChain chains/LCEL, LangGraph agents, RAG patterns, prompt engineering |
| `qa-playwright` | Test organization, selector strategies, visual testing, CI integration |
| `ai-ml-systems` | LLM optimization, multi-agent architecture, evaluation, cost optimization |

## Usage

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

### Using Custom Commands

```bash
# Automatically classify and fix an issue
/fix-issue login-bug

# Specify issue type explicitly
/fix-issue login-bug --type fe-be

# Smart conventional commits
/gh-commit

# Security audit
/security-audit

# Deep analysis mode
/ultra-think Should we migrate to microservices?
```

### Team Workflow Example

```
1. Atlas (Tech Lead)
   └─ get_task("TASK-123") -> Retrieve Fairmind implementation plan
   └─ Analyze: "This needs React frontend + Node.js API"
   └─ Create work package specifying skills to load
   └─ Write to .fairmind/work_packages/frontend/TASK-123_workpackage.md

2. Echo (Software Engineer)
   └─ Read work_packages/frontend/TASK-123_workpackage.md
   └─ Load `frontend-react-nextjs` skill
   └─ Use fairmind-tdd skill -> Implement with TDD
   └─ Update .fairmind/journals/TASK-123_echo_journal.md
   └─ Create completion flag

3. Tess (QA Engineer)
   └─ Load `qa-playwright` skill
   └─ Execute test scenarios
   └─ Create validation report

4. Echo (Code Reviewer)
   └─ Use fairmind-code-review skill
   └─ Load relevant technology skill for context
   └─ Verify: Plan -> Journal -> Code traceability
   └─ Provide structured feedback
```

## Directory Structure Created by Workflow

```
your-project/
├── .fairmind/
│   ├── execution_plans/         # Original Fairmind plans
│   ├── requirements/            # Needs, stories, tasks, tests
│   ├── journals/                # Agent progress tracking (mandatory)
│   │   ├── TASK-123_echo_journal.md
│   │   ├── TASK-123_tess_journal.md
│   │   ├── TASK-123_echo-codereviewer_journal.md
│   │   └── TASK-123_shield_journal.md
│   ├── work_packages/           # Atlas-adapted plans for agents
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── ai/
│   │   ├── qa/
│   │   └── fixes/
│   ├── validation_results/      # Test, review, security reports
│   └── coordination_logs/       # Atlas coordination notes
└── [your code]
```

## CI/CD: Automated Code Review

A reusable GitHub Actions workflow template is included for automated PR code review with FairMind requirements verification.

> **Note:** The workflow currently uses a placeholder for the Gemini CLI GitHub Action integration, as no official `gemini-cli-action` exists yet. See `.github/workflows/gemini-cli-review.yml` for the full review logic and adapt as needed.

The workflow performs:
- Journal verification (`.fairmind/journals/TASK-{ID}_*_journal.md`)
- FairMind requirements coherence check
- Security spot-checks (crypto, input validation, concurrency, auth, cookies)
- Structured reporting with acceptance criteria checklist

## Configuration

### Project-Specific Settings

Create `.gemini/settings.json` in your project:

```json
{
  "mcpServers": {
    "Fairmind": {
      "type": "http",
      "url": "https://project-context.mindstream.fairmind.ai/mcp/mcp/",
      "headers": {
        "Authorization": "Bearer ${env:FAIRMIND_TOKEN}"
      }
    }
  }
}
```

### Team Settings

For consistent team setup, commit `.gemini/settings.json`:

```json
{
  "extensions": {
    "install": ["fairmind-integration"]
  },
  "mcpServers": {
    "Fairmind": {
      "type": "http",
      "url": "https://project-context.mindstream.fairmind.ai/mcp/mcp/",
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
5. **Use skill references** - each skill has detailed reference files in `references/`

## License

MIT

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgments

Built for [Gemini CLI](https://github.com/google-gemini/gemini-cli).
Integrates with [Fairmind AI Studio](https://fairmind.ai).

## Support

- **Issues:** https://github.com/FairMind-Gen-AI-Studio/fairmind-integration/issues
- **Fairmind Support:** support@fairmind.ai
