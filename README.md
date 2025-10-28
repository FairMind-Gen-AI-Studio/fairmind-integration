# Fairmind Integration Plugin for Claude Code

A comprehensive Claude Code plugin providing team collaboration agents and skills with deep Fairmind platform integration. Enables full traceability from implementation plans to code review with specialized AI agents for every stage of development.

## Overview

This plugin extends Claude Code with 12 specialized agents and 3 Fairmind-aware skills, creating a complete team collaboration workflow with the Fairmind AI Studio platform. It provides plan adaptation, test-driven development, and systematic code review with full plan→journal→code traceability.

## Key Features

**🤖 12 Specialized Agents**
- Development agents with Fairmind context integration
- Validation agents with requirements verification
- Orchestration agent (Atlas) for plan adaptation
- Cross-repository integration support

**🎯 3 Fairmind-Aware Skills**
- `fairmind-context`: Intelligent context gathering from projects, sessions, and work items
- `fairmind-tdd`: Test-driven development aligned with acceptance criteria
- `fairmind-code-review`: Three-layer verification (plan→journal→code)

**🔄 Complete Workflow**
- Atlas (Tech Lead) adapts Fairmind plans for specialized agents
- Dev agents implement using TDD with journal tracking
- Code Reviewer verifies against original plans and requirements

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

Once published to a Claude Code marketplace:

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
│   └── plugin.json          # Plugin metadata
├── agents/                   # 12 specialized agents
│   ├── ai-engineer.md
│   ├── backend-engineer.md
│   ├── frontend-engineer.md
│   ├── qa-engineer.md
│   ├── code-reviewer.md
│   ├── cybersec-engineer.md
│   ├── debug-detective.md
│   ├── backend-issue-fixer.md
│   ├── frontend-issue-fixer.md
│   ├── playwright-issue-analyzer.md
│   ├── pr-diff-documenter.md
│   └── tech-lead-software-architect.md
├── skills/                   # 3 Fairmind skills
│   ├── fairmind-context.md
│   ├── fairmind-tdd.md
│   └── fairmind-code-review.md
├── commands/                 # Optional slash commands
└── README.md
```

## Agents

### Development Agents (Batch 1)

**AI Engineer** - ML/AI development with Fairmind context
**Backend Engineer** - Backend development with implementation plans
**Frontend Engineer** - Frontend development with user story alignment

All development agents:
- Retrieve implementation plans from Fairmind tasks
- Follow TDD workflow aligned with acceptance criteria
- Document progress in `fairmind/journals/{role}/`
- Use cross-repository Code tools for integrations

### Validation Agents (Batch 2)

**QA Engineer (Tess)** - Testing aligned with Fairmind test expectations
**Code Reviewer (Echo)** - Three-layer plan→journal→code verification
**Cybersecurity (Shield)** - Security review against Fairmind requirements

### Utility Agents (Batch 3)

**Debug Detective** - Cross-service debugging with Fairmind context
**Backend/Frontend Issue Fixers** - Targeted fixes with user story context
**Playwright Issue Analyzer** - Test analysis (no Fairmind integration)
**PR Diff Documenter** - PR documentation (no Fairmind integration)

### Orchestration Agent (Batch 4)

**Tech Lead (Atlas)** - The critical orchestrator

**Primary Role:** Plan adaptation and agent coordination
- Retrieves generic Fairmind implementation plans
- Analyzes agent capabilities vs plan requirements
- Adapts plans into agent-specific work packages
- Writes to `fairmind/work_packages/{role}/`
- Monitors execution and coordinates handoffs

**Key Principle:** Atlas translates between Fairmind's project plans and agent-specific capabilities. Never implements code, always adapts plans.

## Skills

### fairmind-context

**Purpose:** Reusable context gathering for any Fairmind work

**Inputs:**
- `project_id` (optional - can auto-detect)
- `user_story_id` (optional)
- `task_id` (optional)
- `target_project_id` (optional - for cross-project integrations)

**Outputs:** Complete context including project, session, user story, task with implementation plan, requirements, tests, and documentation

**Invoked by:** All other Fairmind skills as foundation

### fairmind-tdd

**Purpose:** Test-driven development aligned with Fairmind plans

**Workflow:**
1. **Setup:** Invoke `fairmind-context`, get implementation plan and test expectations
2. **Red:** Write failing test aligned with acceptance criteria
3. **Green:** Implement minimal code following the plan
4. **Refactor:** Clean up while maintaining tests
5. **Documentation:** Update journal with traceability

**Key Difference:** Tests aligned with Fairmind acceptance criteria, implementation follows plan from `get_task`, journal provides traceability chain.

### fairmind-code-review

**Purpose:** Systematic code review with full traceability

**Three-Layer Verification:**
1. **Plan Verification:** Compare implementation plan vs journal entries (detect scope creep, missing items)
2. **Requirements Verification:** Check code against acceptance criteria, functional/technical requirements, test coverage
3. **Integration Verification:** Verify API contracts in other repositories (if applicable)

**Output:** Structured report with plan compliance, requirements compliance, integration checks, and recommendations

## Team Workflow Example

```
1. Tech Lead (Atlas)
   └─ get_task("TASK-123") → Retrieve Fairmind implementation plan
   └─ Analyze: "This needs React frontend + Node.js API"
   └─ Adapt plan for Frontend Engineer and Backend Engineer
   └─ Write to fairmind/work_packages/frontend/ and fairmind/work_packages/backend/

2. Frontend Engineer
   └─ Read work_packages/frontend/TASK-123.md
   └─ Use fairmind-context skill → Get user story, acceptance criteria
   └─ Use fairmind-tdd skill → Implement with TDD
   └─ Update fairmind/journals/frontend/2025-10-28-TASK-123.md

3. Backend Engineer
   └─ Read work_packages/backend/TASK-123.md
   └─ Use fairmind-context skill → Get API requirements
   └─ Use fairmind-tdd skill → Implement endpoints
   └─ Update fairmind/journals/backend/2025-10-28-TASK-123.md

4. Code Reviewer (Echo)
   └─ Use fairmind-code-review skill
   └─ Verify: Plan → Journals → Code traceability
   └─ Check acceptance criteria met
   └─ Validate cross-repo API contract (if integration)
   └─ Provide structured feedback
```

## Usage Examples

### Starting New Development Work

```bash
# Atlas retrieves and adapts the plan
@tech-lead-software-architect retrieve task TASK-456 and create work packages

# Dev agent implements with TDD
@frontend-engineer implement the work package for TASK-456

# Review the implementation
@code-reviewer review TASK-456 implementation
```

### Cross-Repository Integration

```bash
# Investigate API contract in another service
@backend-engineer check the payment-service API for checkout endpoint

# Debug cross-service issue
@debug-detective investigate why auth-service calls are failing
```

### Security Review

```bash
# Review against Fairmind security requirements
@cybersec-engineer review authentication implementation for security requirements
```

## Directory Structure Created by Workflow

```
your-project/
├── fairmind/
│   ├── work_packages/        # Atlas-adapted plans for agents
│   │   ├── frontend/
│   │   ├── backend/
│   │   └── ai/
│   └── journals/             # Agent progress tracking
│       ├── frontend/
│       ├── backend/
│       └── ai/
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

**Note:** Use environment variable `FAIRMIND_TOKEN` to avoid committing tokens to version control. Team members should set their own token:

```bash
export FAIRMIND_TOKEN="your-token-here"
```

## Best Practices

1. **Always start with Atlas** for new Fairmind tasks - let it adapt the plan
2. **Use fairmind-context** in all development work - ensures full context
3. **Follow fairmind-tdd** for implementation - maintains traceability
4. **Update journals regularly** - enables meaningful code review
5. **Use Code tools only for cross-repo** - use local file tools for current repository

## Troubleshooting

### Plugin Not Loading

```bash
# Verify plugin installation
claude plugin list

# Check plugin structure
ls -la ~/.claude/plugins/fairmind-integration/.claude-plugin/
```

### Fairmind MCP Server Issues

```bash
# Test MCP server connection
claude mcp test Fairmind

# Check server logs
tail -f ~/.claude/logs/mcp-Fairmind.log
```

### Missing Context

If skills can't find Fairmind context:
1. Verify Fairmind MCP server is configured
2. Check you're in a project with Fairmind integration
3. Ensure `project_id` or `task_id` is available

## Development

### Adding Custom Agents

1. Create new agent file in `agents/`
2. Follow existing agent format
3. Update `.claude-plugin/plugin.json` components list
4. Test with Claude Code

### Creating Additional Skills

1. Create skill file in `skills/`
2. Follow Fairmind skill naming convention
3. Use `fairmind-context` as foundation
4. Update plugin.json and README

## Version History

**1.0.0** (2025-10-28)
- Initial release
- 12 specialized agents with Fairmind integration
- 3 Fairmind-aware skills
- Complete plan→journal→code workflow
- Cross-repository integration support

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
Integrates with [Fairmind AI Studio](https://fairmind.com) platform.

## Support

- **Issues:** https://github.com/FairMind-Gen-AI-Studio/fairmind-integration/issues
- **Documentation:** https://docs.fairmind.com/claude-integration
- **Fairmind Support:** support@fairmind.com
