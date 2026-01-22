# Changelog

All notable changes to the Fairmind Integration Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-22

### Changed
- **Major refactor**: Reorganized from 12 function-specific agents to 6 role-based agents
  - Atlas (Tech Lead/Software Architect)
  - Echo (Software Engineer) - dynamically specializes based on task
  - Tess (QA Engineer)
  - Code Reviewer
  - Debug Detective
  - Shield (Cybersecurity Expert)

### Added

#### Skills (6 new technology-specific)
- `frontend-react-nextjs` - React, NextJS, TypeScript, Tailwind, Shadcn UI
- `backend-nextjs` - NextJS API routes, MongoDB, server-side logic
- `backend-python` - FastAPI, Pydantic, async patterns
- `backend-langchain` - LangChain, LangGraph, RAG systems
- `qa-playwright` - Playwright E2E testing, visual testing, MCP tools
- `ai-ml-systems` - LLM optimization, multi-agent systems, AI evaluation

#### Features
- `readiness-report` skill for repository assessment
- `plugin.json` for Claude Code plugin system compatibility
- All agents updated to use Claude Sonnet 4.5

### Fixed
- Skill directory structure corrected for Claude Code plugin format
- Skills moved to root directory for proper plugin loading

---

## [1.0.0] - 2025-10-28

### Added

#### Agents (12 total)
**Development Agents:**
- `ai-engineer.md` - AI/ML development with Fairmind task integration
- `backend-engineer.md` - Backend development with implementation plan support
- `frontend-engineer.md` - Frontend development with user story alignment

**Validation Agents:**
- `qa-engineer.md` - Testing aligned with Fairmind test expectations
- `code-reviewer.md` - Three-layer plan→journal→code verification
- `cybersec-engineer.md` - Security review against Fairmind requirements

**Utility Agents:**
- `debug-detective.md` - Cross-service debugging with Fairmind context
- `backend-issue-fixer.md` - Targeted backend fixes with user story context
- `frontend-issue-fixer.md` - Targeted frontend fixes with user story context
- `playwright-issue-analyzer.md` - Playwright test analysis
- `pr-diff-documenter.md` - Pull request documentation

**Orchestration Agent:**
- `tech-lead-software-architect.md` (Atlas) - Plan adaptation and agent coordination

#### Skills (3 total)
- `fairmind-context.md` - Intelligent context gathering from Fairmind projects, sessions, and work items
- `fairmind-tdd.md` - Test-driven development aligned with acceptance criteria and implementation plans
- `fairmind-code-review.md` - Systematic code review with plan→journal→code traceability

#### Features
- Complete team collaboration workflow with plan adaptation
- Cross-repository integration support via Fairmind Code tools
- Journal-based progress tracking for traceability
- Full integration with 40 Fairmind MCP tools (General, Studio, Code)
- Work package system for agent coordination
- Three-layer code review verification

#### Documentation
- Comprehensive README with installation and usage examples
- CONTRIBUTING guide for plugin development
- Plugin metadata (plugin.json) with component registry
- Team workflow examples
- Troubleshooting guide

### Infrastructure
- Plugin structure compliant with Claude Code plugin system
- MCP server requirement documentation
- Team installation support via settings.json
- Marketplace distribution ready

---

## [Unreleased]

### Planned Features
- Additional skills: `fairmind-debugging`, `fairmind-planning`, `fairmind-deployment`
- Integration with CI/CD pipelines
- Automated journal generation
- Multi-agent parallel execution support
- Skills for project managers and product owners
- Cross-project dependency tracking

---

## Version History

### Version Numbering

- **1.0.0** - Initial plugin release with complete Fairmind integration
- **1.x.x** - Minor updates, new agents/skills, bug fixes
- **2.0.0** - Major breaking changes (if needed)

### Release Notes Format

Each release documents:
- **Added:** New features, agents, skills, commands
- **Changed:** Updates to existing functionality
- **Deprecated:** Features marked for removal
- **Removed:** Deleted features
- **Fixed:** Bug fixes
- **Security:** Security vulnerability fixes

---

## Migration Guides

### From Standalone Agents to Plugin (1.0.0)

If you were using individual agent files before the plugin:

1. **Remove old agent files** from `.claude/agents/`
2. **Install plugin** via marketplace or source
3. **Update settings.json** to include Fairmind MCP server configuration
4. **Verify agents load** with `claude agents list` (if command available)

### Fairmind MCP Tools Migration

**Version 1.0.0 uses current Fairmind MCP API:**
- 13 General tools
- 21 Studio tools
- 6 Code tools

If Fairmind MCP API changes, agents will be updated to match.

---

## Support

For issues, questions, or feature requests:
- **Issues:** https://github.com/YOUR_ORG/fairmind-claude-agents/issues
- **Discussions:** https://github.com/YOUR_ORG/fairmind-claude-agents/discussions
- **Fairmind Support:** support@fairmind.com
