# Fairmind Claude Agents

A unified collection of Claude Code agents and commands for software development workflows, with specialized tools for the Fairmind AI Studio platform.

## Overview

This repository contains a comprehensive set of AI agents and commands designed to work with [Claude Code](https://claude.com/claude-code). It combines general-purpose development tools with Fairmind-specific workflows.

## Structure

```
fairmind-claude-agents/
├── agents/          # 12 specialized AI agents
├── commands/        # 23 custom commands
├── directive/       # Environment configuration templates
├── scripts/         # Helper scripts (e.g., SonarQube analyzer)
└── settings.local.json  # MCP Playwright permissions config
```

## Agents (12)

### General Development Agents
- **ai-engineer.md** - AI and machine learning development
- **backend-engineer.md** - Backend development and API design
- **frontend-engineer.md** - Frontend development and UI/UX
- **code-reviewer.md** - Code review and quality assurance
- **debug-detective.md** - Debugging and troubleshooting
- **qa-engineer.md** - Quality assurance and testing
- **cybersec-engineer.md** - Security auditing and best practices
- **tech-lead-software-architect.md** - Architecture and technical leadership
- **pr-diff-documenter.md** - Pull request documentation

### Fairmind-Specific Agents
- **backend-issue-fixer.md** - Backend issue resolution for Fairmind platform
- **frontend-issue-fixer.md** - Frontend issue resolution for Fairmind platform
- **playwright-issue-analyzer.md** - Playwright test analysis and debugging

## Commands (23)

### Documentation
- `add-changelog` - Generate changelog entries
- `create-architecture-documentation` - Create architecture docs
- `create-onboarding-guide` - Create onboarding documentation
- `docs` - General documentation generation
- `generate-api-documentation` - Generate API docs
- `pr-review` - Pull request review

### Code Quality & Security
- `code-review` - Comprehensive code review
- `security-audit` - Security vulnerability assessment
- `performance-audit` - Performance analysis
- `sonarqube-fix` - SonarQube issue resolution

### Development Workflows
- `explore-plan-code-test` - Full development cycle workflow
- `implement-caching-strategy` - Add caching to applications
- `add-performance-monitoring` - Add performance monitoring

### Fairmind Platform
- `fairmind` - Fairmind platform development helper
- `fix-issue` - General issue resolution workflow
- `fix-frontend-issue` - Frontend-specific issue resolution
- `migrate-to-k8s` - Kubernetes migration guide

### Content & Utilities
- `book-review` - Book review generation
- `linkedin-post` - LinkedIn content creation
- `ghost-writer` - General writing assistance
- `report` - Report generation
- `ultra-think` - Deep analysis mode
- `index` - Index generation

## Installation

### Option 1: Clone Repository
```bash
git clone https://github.com/YOUR_ORG/fairmind-claude-agents.git
cd fairmind-claude-agents
```

### Option 2: Add as Claude Code Configuration
Copy the desired agents and commands to your Claude Code configuration directory:

```bash
# For project-specific setup
cp -r agents/ commands/ /path/to/your/project/.claude/

# For global setup (all projects)
cp -r agents/ commands/ ~/.claude/
```

## Usage

### Using Agents
Agents are automatically available in Claude Code. Reference them in your conversations:

```
@ai-engineer help me design a neural network architecture
@backend-issue-fixer investigate this API error
```

### Using Commands
Commands can be invoked with the `/` prefix:

```
/code-review
/security-audit
/migrate-to-k8s
```

## Configuration

### MCP Playwright Permissions
The `settings.local.json` file contains permissions for the MCP Playwright integration, allowing Claude Code to:
- Navigate web pages
- Take screenshots
- Interact with browser elements
- Analyze web applications

### Environment Configuration
Use the `directive/fairmind-local-directive.md.example` as a template for setting up your local environment configuration.

## Scripts

### SonarQube Analyzer
The `scripts/analyze_sonarqube.py` script integrates with SonarCloud to:
- Fetch code quality issues
- Categorize issues by type
- Generate JSON reports
- Support PR-aware analysis

Usage:
```bash
python scripts/analyze_sonarqube.py
```

## Contributing

When adding new agents or commands:
1. Follow the existing naming conventions
2. Include clear descriptions and usage examples
3. Test with Claude Code before committing
4. Update this README with new entries

## License

[Specify your license here]

## Acknowledgments

Built for use with [Claude Code](https://claude.com/claude-code) by Anthropic.
