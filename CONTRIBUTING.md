# Contributing to Fairmind Integration Plugin

Thank you for your interest in contributing to the Fairmind Integration Plugin! This document provides guidelines for contributing agents, skills, commands, and improvements.

## Development Setup

### Prerequisites

1. **Claude Code** installed and configured
2. **Fairmind MCP Server** installed and running
3. **Node.js** (for MCP server)
4. **Git** for version control

### Local Development

```bash
# Clone the repository
git clone https://github.com/FairMind-Gen-AI-Studio/fairmind-integration.git
cd fairmind-integration

# Create symlink for testing
ln -s $(pwd) ~/.claude/plugins/fairmind-integration-dev

# Or copy to project for testing
cp -r . /path/to/test-project/.claude/plugins/fairmind-integration-dev
```

## Contribution Types

### 1. Adding New Agents

**When to add a new agent:**
- Specialized role not covered by existing 12 agents
- Distinct workflow that doesn't fit existing agents
- New development paradigm (e.g., mobile, embedded systems)

**Steps:**

1. Create agent file in `agents/`
```bash
touch agents/your-agent-name.md
```

2. Follow the agent template structure:
```markdown
You are [Agent Name], a [description of role and expertise].

## Core Responsibilities
- Primary task 1
- Primary task 2

## Fairmind Integration
- Which Fairmind MCP tools you use
- How you interact with Fairmind platform
- Journal/work package patterns

## Workflow
1. Step-by-step process
2. How to handle different scenarios

## Best Practices
- Key guidelines
- Common pitfalls to avoid
```

3. Update `.claude-plugin/plugin.json`:
```json
{
  "components": {
    "agents": [
      "existing-agent",
      "your-agent-name"
    ]
  }
}
```

4. Update README.md with agent description
5. Test thoroughly with Fairmind MCP server
6. Submit PR with examples of agent usage

### 2. Creating New Skills

**When to create a new skill:**
- Reusable workflow across multiple agents
- Fairmind-specific process not covered by existing skills
- Cross-cutting concern (debugging, deployment, etc.)

**Steps:**

1. Create skill file in `skills/`
```bash
touch skills/fairmind-your-skill.md
```

2. Follow the skill template:
```markdown
---
name: fairmind-your-skill
description: Brief description of what this skill does
---

# Purpose
What problem does this skill solve?

# When to Use
- Scenario 1
- Scenario 2

# Prerequisites
- Required context
- Dependencies on other skills

# Workflow
1. Step 1
2. Step 2

# Inputs
- parameter1: description
- parameter2: description

# Outputs
What this skill produces

# Example Usage
Concrete example of using the skill
```

3. Consider skill dependencies:
   - Should it invoke `fairmind-context` first?
   - Does it build on other skills?

4. Update `.claude-plugin/plugin.json`
5. Update README.md
6. Test skill with multiple agents
7. Document skill interactions in README

### 3. Adding Commands

**When to add a command:**
- Workflow automation for common tasks
- Fairmind-specific shortcuts
- Multi-step processes that benefit from parameterization

**Steps:**

1. Create command file in `commands/`
```bash
touch commands/your-command.md
```

2. Follow command format:
```markdown
You are helping with [task description].

## Context
[Provide context about when to use this command]

## Steps
1. First action
2. Second action

## Parameters
- param1: description
- param2: description

## Example
/your-command [parameters]
```

3. Test command invocation
4. Update documentation

### 4. Improving Documentation

**Documentation areas:**
- Agent usage examples
- Skill interaction patterns
- Troubleshooting guides
- Configuration templates
- Team workflow examples

**Process:**
1. Identify documentation gap
2. Create/update relevant section
3. Add code examples if applicable
4. Test instructions on fresh setup
5. Submit PR

## Code Standards

### Agent Files

**Do:**
- Use clear, descriptive role names
- Document Fairmind MCP tool usage
- Provide concrete workflow examples
- Include error handling guidance
- Reference journal/work package patterns

**Don't:**
- Duplicate functionality of existing agents
- Create agents without Fairmind integration (unless utility agents)
- Skip workflow documentation

### Skill Files

**Do:**
- Use `fairmind-` prefix for Fairmind-specific skills
- Document inputs and outputs clearly
- Provide usage examples
- Explain when NOT to use the skill
- Test skill composition (using multiple skills together)

**Don't:**
- Create skills that are just wrappers around single MCP tools
- Skip error handling scenarios
- Forget to update skill dependencies

### Commands

**Do:**
- Use kebab-case naming
- Provide clear parameter descriptions
- Include usage examples
- Document expected outcomes

**Don't:**
- Create commands that duplicate skill functionality
- Skip parameter validation

## Testing Guidelines

### Testing Agents

1. **Context gathering:** Verify agent retrieves correct Fairmind context
2. **Workflow execution:** Test complete workflow end-to-end
3. **Journal updates:** Confirm journal entries are created/updated correctly
4. **Cross-repo integration:** If applicable, test Code tools usage
5. **Error handling:** Test behavior with missing/invalid context

### Testing Skills

1. **Standalone usage:** Test skill in isolation
2. **Skill composition:** Test with other skills (especially fairmind-context)
3. **Multiple agents:** Verify skill works with different agents
4. **Edge cases:** Test with missing parameters, invalid IDs, etc.
5. **Output validation:** Confirm outputs match documentation

### Testing Commands

1. **Parameter handling:** Test with various parameter combinations
2. **Error scenarios:** Test with missing/invalid parameters
3. **Integration:** Test command with relevant agents
4. **Documentation:** Verify usage examples work as documented

## Pull Request Process

### Before Submitting

- [ ] Code follows existing patterns
- [ ] All tests pass locally
- [ ] Documentation updated (README, CONTRIBUTING)
- [ ] plugin.json updated if new components added
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive data in commits (API keys, etc.)

### PR Template

```markdown
## Description
[Describe what this PR does]

## Type of Change
- [ ] New agent
- [ ] New skill
- [ ] New command
- [ ] Bug fix
- [ ] Documentation update
- [ ] Other (specify)

## Changes Made
- Change 1
- Change 2

## Testing
[Describe how you tested this]

## Screenshots/Examples
[If applicable, show the new functionality]

## Checklist
- [ ] Tested with Fairmind MCP server
- [ ] Documentation updated
- [ ] plugin.json updated
- [ ] Follows existing patterns
```

### Review Process

1. Maintainer reviews code and tests
2. Feedback provided if changes needed
3. Once approved, PR merged to main
4. Version bumped if significant changes
5. Plugin published to marketplace (if applicable)

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes to agent/skill interfaces
- **MINOR** (0.x.0): New agents, skills, or commands (backwards compatible)
- **PATCH** (0.0.x): Bug fixes, documentation updates

## Release Process

1. Update version in `.claude-plugin/plugin.json`
2. Update CHANGELOG.md with changes
3. Create git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. Create GitHub release
6. Publish to Claude Code marketplace (if applicable)

## Community Guidelines

### Communication

- Be respectful and constructive
- Provide clear context in issues/PRs
- Share examples of usage
- Help other contributors

### Issue Reporting

**Bug Reports:**
- Describe expected vs actual behavior
- Provide steps to reproduce
- Include Claude Code version
- Include Fairmind MCP server version
- Attach relevant logs/screenshots

**Feature Requests:**
- Describe the use case
- Explain why existing agents/skills don't cover it
- Provide examples of desired behavior

## Development Workflow Example

```bash
# 1. Create feature branch
git checkout -b feature/new-mobile-agent

# 2. Create agent file
cat > agents/mobile-engineer.md << 'EOF'
You are Mobile Engineer, specializing in iOS and Android development...
EOF

# 3. Update plugin.json
# Edit .claude-plugin/plugin.json

# 4. Test locally
ln -s $(pwd) ~/.claude/plugins/fairmind-integration-dev
# Open Claude Code and test agent

# 5. Update documentation
# Edit README.md

# 6. Commit and push
git add agents/mobile-engineer.md .claude-plugin/plugin.json README.md
git commit -m "feat(agents): add Mobile Engineer agent for iOS/Android development"
git push origin feature/new-mobile-agent

# 7. Create PR on GitHub
```

## Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Create an issue with bug report template
- **Features:** Create an issue with feature request template
- **Chat:** Join our Discord/Slack (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- README.md Contributors section
- Release notes
- Plugin marketplace listing (if applicable)

Thank you for making the Fairmind Integration Plugin better!
