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

First, locate the plugin scripts directory:

```bash
PLUGIN_DIR=$(find ~/.claude/plugins/cache/fairmind-marketplace/fairmind-integration -maxdepth 1 \( -type d -o -type l \) 2>/dev/null | tail -1)
SCRIPTS_DIR="$PLUGIN_DIR/skills/readiness-report/scripts"
```

Then execute the analysis:

```bash
python "$SCRIPTS_DIR/analyze_repo.py" --repo-path .
```

Or if running from the fairmind-integration repo directly:
```bash
python skills/readiness-report/scripts/analyze_repo.py --repo-path /path/to/target/repo
```

This script checks for:
- Configuration files (.eslintrc, pyproject.toml, etc.)
- CI/CD workflows (.github/workflows/, .gitlab-ci.yml)
- Documentation (README, AGENTS.md, CONTRIBUTING.md)
- Test infrastructure (test directories, coverage configs)
- Security configurations (CODEOWNERS, .gitignore, secrets management)

### Step 2: Generate Executive Summary (HTML reports only)

For HTML reports, read the analysis JSON and generate a 2-3 sentence executive summary:

**Summary should include:**
- Current maturity level achieved
- Key strength area (top pillar)
- Priority action for improvement

**Example summary format:**
> This repository achieves L2 (Documented) maturity with strong Documentation coverage at 85%. To reach L3, prioritize adding integration tests and test coverage thresholds.

### Step 3: Generate Report

Generate the formatted report:

```bash
python "$SCRIPTS_DIR/generate_report.py" --analysis-file /tmp/readiness_analysis.json
```

**For FairMind integration**, save to validation results:
```bash
python "$SCRIPTS_DIR/generate_report.py" \
  --analysis-file /tmp/readiness_analysis.json \
  --output fairmind/validation_results/readiness_report.md
```

#### Report Format Options

| Format | Flag | Output | Best For |
|--------|------|--------|----------|
| Markdown | `--format markdown` (default) | Mermaid diagrams inline | GitHub, GitLab, VS Code |
| HTML | `--format html` | Self-contained HTML with FairMind branding | Browser viewing, sharing |

Generate HTML report with executive summary:
```bash
python "$SCRIPTS_DIR/generate_report.py" \
  --analysis-file /tmp/readiness_analysis.json \
  --format html \
  --summary "This repository achieves L2 maturity with strong documentation. Priority: add integration tests to reach L3." \
  --output report.html
```

#### Disable Diagrams

For markdown reports without Mermaid diagrams:
```bash
python "$SCRIPTS_DIR/generate_report.py" \
  --analysis-file /tmp/readiness_analysis.json \
  --no-diagrams
```

### Step 4: Present Results

The report includes:
1. **Overall Score**: Pass rate percentage and maturity level achieved
2. **Level Progress**: Visual bars showing L1-L5 completion percentages
3. **Visual Summary** (Markdown format):
   - Pillar scores bar chart (Mermaid)
   - Level progress chart with 80% threshold line
   - Criteria distribution pie chart
   - Improvement roadmap flowchart
4. **Strengths**: Top-performing pillars with passing criteria
5. **Opportunities**: Prioritized list of improvements to implement
6. **Detailed Criteria**: Collapsible sections (HTML) or tables (Markdown) showing each criterion status

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
| L1 | Manual | Basic version control | Manual assistance only |
| L2 | Scaffolded | Basic CI/CD and testing | Simple, well-defined tasks |
| L3 | Collaborative | Production-ready for agents | Routine maintenance |
| L4 | Automated | Comprehensive automation | Complex features |
| L5 | Autonomous | Full autonomous capability | End-to-end development |

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
