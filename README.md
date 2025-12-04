# Fairmind Integration Plugin for Claude Code

A comprehensive Claude Code plugin providing team collaboration with role-based agents and technology-specific skills. Features deep Fairmind platform integration with full traceability from implementation plans to code review.

## Overview

This plugin extends Claude Code with **6 role-based agents** and **9 technology-specific skills**, creating a complete team collaboration workflow with the Fairmind AI Studio platform. Agents focus on roles (what they do), while skills provide technology expertise (how they do it).

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
      "url": "https://project-context.mindstream.fairmind.ai/mcp/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**Option 2: Using Claude CLI**

```bash
claude mcp add --transport http Fairmind https://project-context.mindstream.fairmind.ai/mcp/mcp/ --header "Authorization: Bearer YOUR_TOKEN_HERE"
```

Replace `YOUR_TOKEN_HERE` with your Fairmind authentication token.

## Installation

### Option 1: Install from Marketplace (Recommended)

```bash
# Install globally for all projects
claude plugin install fairmind-integration

# Or install for specific project
cd your-project
claude plugin install fairmind-integration --project
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git

# Create symbolic link to Claude Code plugins directory
ln -s $(pwd)/fairmind-integration ~/.claude/plugins/fairmind-integration

# Or copy to project-specific location
cp -r fairmind-integration /path/to/your/project/.claude/plugins/fairmind-integration
```

### Option 3: Team Installation

For automatic installation across your team, add to your repository's `.claude/settings.json`:

```json
{
  "plugins": {
    "marketplaces": ["default"],
    "install": ["fairmind-integration"]
  }
}
```

## Plugin Structure

```
fairmind-integration/
├── .claude-plugin/
│   └── marketplace.json          # Plugin marketplace metadata
├── agents/                       # 6 role-based agents
│   ├── tech-lead.md              # Atlas - orchestration
│   ├── software-engineer.md      # Echo - all implementation
│   ├── qa-engineer.md            # Tess - testing
│   ├── code-reviewer.md          # Echo - code review
│   ├── debug-detective.md        # Debugging specialist
│   ├── cybersec-engineer.md      # Shield - security
│   └── archived/                 # Legacy agents (kept for reference)
├── fairmind-context/             # Fairmind context skill
│   └── SKILL.md
├── fairmind-tdd/                 # TDD workflow skill
│   └── SKILL.md
├── fairmind-code-review/         # Code review skill
│   └── SKILL.md
├── frontend-react-nextjs/        # Frontend technology skill
│   ├── SKILL.md
│   └── references/
│       ├── react-patterns.md
│       ├── nextjs-conventions.md
│       ├── typescript-guidelines.md
│       ├── tailwind-shadcn.md
│       └── zustand-state.md
├── backend-nextjs/               # NextJS backend skill
│   ├── SKILL.md
│   └── references/
│       ├── api-routes.md
│       ├── mongodb-patterns.md
│       ├── authentication.md
│       └── error-handling.md
├── backend-python/               # Python backend skill
│   ├── SKILL.md
│   └── references/
│       ├── fastapi-patterns.md
│       ├── pydantic-models.md
│       ├── async-patterns.md
│       └── testing-patterns.md
├── backend-langchain/            # LangChain/AI skill
│   ├── SKILL.md
│   └── references/
│       ├── chain-patterns.md
│       ├── agent-patterns.md
│       ├── rag-patterns.md
│       ├── prompt-engineering.md
│       └── memory-patterns.md
├── qa-playwright/                # Playwright testing skill
│   ├── SKILL.md
│   └── references/
│       ├── test-patterns.md
│       ├── selectors.md
│       ├── visual-testing.md
│       ├── mcp-tools.md
│       └── ci-integration.md
├── ai-ml-systems/                # AI/ML systems skill
│   ├── SKILL.md
│   └── references/
│       ├── llm-optimization.md
│       ├── agent-architecture.md
│       ├── evaluation-patterns.md
│       └── cost-optimization.md
├── commands/                     # Slash commands
│   ├── fix-issue.md
│   └── ...
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
   └─ Write to fairmind/work_packages/frontend/TASK-123_workpackage.md

2. Echo (Software Engineer)
   └─ Read work_packages/frontend/TASK-123_workpackage.md
   └─ Load `frontend-react-nextjs` skill
   └─ Use fairmind-tdd skill → Implement with TDD
   └─ Update fairmind/journals/TASK-123_echo_journal.md
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

```
your-project/
├── fairmind/
│   ├── work_packages/        # Atlas-adapted plans for agents
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── ai/
│   │   ├── qa/
│   │   └── fixes/
│   ├── journals/             # Agent progress tracking
│   └── validation_results/   # Test and review reports
└── [your code]
```

## Configuration

### Project-Specific Settings

Create `.claude/settings.json` in your project:

```json
{
  "fairmind": {
    "defaultProject": "your-project-id",
    "journalPath": "fairmind/journals",
    "workPackagePath": "fairmind/work_packages"
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
5. **Use skill references** - each skill has detailed reference files

## Version History

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
Integrates with [Fairmind AI Studio](https://fairmind.ai) platform.

## Support

- **Issues:** https://github.com/FairMind-Gen-AI-Studio/fairmind-integration/issues
- **Fairmind Support:** support@fairmind.ai
