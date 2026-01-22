---
name: readiness-report
description: Evaluates repository readiness for AI-assisted development. Run to assess codebase maturity (L1-L5) across 81 criteria in 9 pillars. Useful before starting new projects or diagnosing agent workflow issues.
---

# Agent Readiness Report

## Overview

Evaluate how well a repository supports autonomous AI development by analyzing it across nine technical pillars and five maturity levels.

**Announce at start:** "I'm using the readiness-report skill to evaluate this repository's agent readiness."

## When to Use

Use this skill when:
- Starting work on a new/unfamiliar repository
- Diagnosing why agent workflows are failing
- Assessing infrastructure gaps before development
- Planning repository improvements for better AI collaboration

## Quick Start

Run `/readiness-report` to evaluate the current repository.

## Workflow

### Step 1: Run Repository Analysis

Execute the analysis script from the skill's scripts directory:

```bash
python ~/.claude/skills/readiness-report/scripts/analyze_repo.py --repo-path .
```

Or if running from this repo:
```bash
python skills/readiness-report/scripts/analyze_repo.py --repo-path /path/to/target/repo
```

This script checks for:
- Configuration files (.eslintrc, pyproject.toml, etc.)
- CI/CD workflows (.github/workflows/, .gitlab-ci.yml)
- Documentation (README, AGENTS.md, CONTRIBUTING.md)
- Test infrastructure (test directories, coverage configs)
- Security configurations (CODEOWNERS, .gitignore, secrets management)

### Step 2: Generate Report

After analysis, generate the formatted report:

```bash
python skills/readiness-report/scripts/generate_report.py --analysis-file /tmp/readiness_analysis.json
```

**For FairMind integration**, save to validation results:
```bash
python skills/readiness-report/scripts/generate_report.py \
  --analysis-file /tmp/readiness_analysis.json \
  --output fairmind/validation_results/readiness_report.md
```

### Step 3: Present Results

The report includes:
1. **Overall Score**: Pass rate percentage and maturity level achieved
2. **Level Progress**: Bar showing L1-L5 completion percentages
3. **Strengths**: Top-performing pillars with passing criteria
4. **Opportunities**: Prioritized list of improvements to implement
5. **Detailed Criteria**: Full breakdown by pillar showing each criterion status

## Nine Technical Pillars

| Pillar | Purpose | Key Signals |
|--------|---------|-------------|
| **Style & Validation** | Catch bugs instantly | Linters, formatters, type checkers |
| **Build System** | Fast, reliable builds | Build docs, CI speed, automation |
| **Testing** | Verify correctness | Unit/integration tests, coverage |
| **Documentation** | Guide the agent | AGENTS.md, README, architecture docs |
| **Dev Environment** | Reproducible setup | Devcontainer, env templates |
| **Debugging & Observability** | Diagnose issues | Logging, tracing, metrics |
| **Security** | Protect the codebase | CODEOWNERS, secrets management |
| **Task Discovery** | Find work to do | Issue templates, PR templates |
| **Product & Analytics** | Error-to-insight loop | Error tracking, product analytics |

See `references/criteria.md` for the complete list of 81 criteria.

## Five Maturity Levels

| Level | Name | Description | Agent Capability |
|-------|------|-------------|------------------|
| L1 | Initial | Basic version control | Manual assistance only |
| L2 | Managed | Basic CI/CD and testing | Simple, well-defined tasks |
| L3 | Standardized | Production-ready for agents | Routine maintenance |
| L4 | Measured | Comprehensive automation | Complex features |
| L5 | Optimized | Full autonomous capability | End-to-end development |

**Level Progression**: To unlock a level, pass >=80% of criteria at that level AND all previous levels.

See `references/maturity-levels.md` for detailed level requirements.

## Interpreting Results

### Pass vs Fail vs Skip

- **Pass**: Criterion met (contributes to score)
- **Fail**: Criterion not met (opportunity for improvement)
- **Skip**: Not applicable to this repository type (excluded from score)

### Priority Order

Fix gaps in this order:
1. **L1-L2 failures**: Foundation issues blocking basic agent operation
2. **L3 failures**: Production readiness gaps
3. **High-impact L4+ failures**: Optimization opportunities

### Common Quick Wins

1. **Add AGENTS.md**: Document commands, architecture, and workflows for AI agents
2. **Configure pre-commit hooks**: Catch style issues before CI
3. **Add PR/issue templates**: Structure task discovery
4. **Document single-command setup**: Enable fast environment provisioning

## Integration with FairMind

After running the readiness report:

1. **Store results** in `fairmind/validation_results/readiness_report.md`
2. **Inform work package complexity**:
   - L1-L2 repos: Need more detailed work packages, manual verification steps
   - L3+ repos: Standard automation workflows apply
3. **Identify setup tasks**: Missing infrastructure becomes prerequisite work for Atlas to delegate

## Reference Files

| File | Content | When to Use |
|------|---------|-------------|
| `references/criteria.md` | All 81 criteria by pillar | Understanding what's measured |
| `references/maturity-levels.md` | Level definitions | Understanding progression |

## Next Steps

After reviewing the report:
- **For low scores (L1-L2)**: Create setup work packages for infrastructure gaps
- **For medium scores (L3)**: Proceed with standard development workflows
- **For high scores (L4+)**: Leverage advanced automation capabilities

## Automated Remediation

After reviewing the report, common fixes can be automated:
- Generate AGENTS.md from repository structure
- Add missing issue/PR templates
- Configure standard linters and formatters
- Set up pre-commit hooks

Ask to "fix readiness gaps" to begin automated remediation of failing criteria.
