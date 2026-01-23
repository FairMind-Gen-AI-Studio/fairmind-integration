---
description: "Evaluate repository readiness for AI-assisted development. Assesses codebase maturity (L1-L5) across 81 criteria in 9 pillars."
---

# Readiness Report

Evaluate the current repository's readiness for AI-assisted development across 81 criteria in 9 pillars.

## Instructions

1. **Run repository analysis**:
   ```bash
   # Find the plugin directory with diagram support (has diagrams.py)
   PLUGIN_DIR=$(for d in ~/.claude/plugins/cache/fairmind-marketplace/fairmind-integration/*/; do
     [ -f "${d}skills/readiness-report/scripts/diagrams.py" ] && echo "$d" && break
   done)
   python "${PLUGIN_DIR}skills/readiness-report/scripts/analyze_repo.py" --repo-path .
   ```

2. **Ask user for preferred report format**:
   - **Markdown + Diagrams** (`--format markdown`): Best for GitHub, GitLab, VS Code
   - **ASCII Charts** (`--format brief`): Best for terminal viewing
   - **JSON** (`--format json`): For programmatic access
   - **SVG Export** (`--export-charts DIR`): For presentations/PDF (requires matplotlib)

3. **Generate report** with user's chosen format:
   ```bash
   python "${PLUGIN_DIR}skills/readiness-report/scripts/generate_report.py" \
     --analysis-file /tmp/readiness_analysis.json \
     --output fairmind/validation_results/readiness_report.md \
     --format markdown
   ```

   For SVG export, add: `--export-charts ./charts`

4. **Present results** and recommend next steps based on achieved level:
   - L1-L2: Focus on foundational improvements
   - L3: Ready for standard automation workflows
   - L4+: Can leverage advanced AI patterns
