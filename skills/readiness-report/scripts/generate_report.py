#!/usr/bin/env python3
"""
Report Generator for Agent Readiness

Generates formatted reports from analysis JSON.
Supports Markdown (with Mermaid diagrams) and self-contained HTML.

Usage:
    python generate_report.py --analysis-file /tmp/readiness_analysis.json
    python generate_report.py --analysis-file /tmp/readiness_analysis.json --format markdown
    python generate_report.py --analysis-file /tmp/readiness_analysis.json --format html
"""

import argparse
import json
from pathlib import Path

from diagrams import generate_visual_summary_mermaid
from html_report import generate_html_report


def format_level_bar(level_scores: dict, achieved: int) -> str:
    """Generate a visual level progress bar."""
    bars = []
    for level in range(1, 6):
        score = level_scores.get(str(level), level_scores.get(level, 0))
        if level <= achieved:
            indicator = "█" * 4
            status = f"L{level} {score:.0f}%"
        else:
            indicator = "░" * 4
            status = f"L{level} {score:.0f}%"
        bars.append(f"{indicator} {status}")
    return " | ".join(bars)


def format_criterion_row(criterion: dict) -> str:
    """Format a single criterion as a table row."""
    status = criterion["status"]
    crit_id = criterion["id"]
    score = criterion["score"]
    reason = criterion["reason"]

    if status == "pass":
        icon = "✓"
    elif status == "fail":
        icon = "✗"
    else:  # skip
        icon = "—"

    return f"{icon} `{crit_id}` | {score} | {reason}"


def get_top_strengths(data: dict, n: int = 3) -> list[tuple[str, int, list[str]]]:
    """Get top performing pillars with example passing criteria."""
    pillar_scores = []
    for pillar_name, pillar in data["pillars"].items():
        if pillar["total"] > 0:
            pct = pillar["percentage"]
            passing = [c["id"] for c in pillar["criteria"] if c["status"] == "pass"][:3]
            pillar_scores.append((pillar_name, pct, passing))

    # Sort by percentage descending
    pillar_scores.sort(key=lambda x: x[1], reverse=True)
    return pillar_scores[:n]


def get_top_opportunities(data: dict, n: int = 5) -> list[tuple[str, str, str]]:
    """Get highest priority improvement opportunities."""
    opportunities = []

    # Prioritize by level (lower levels first), then by pillar importance
    for pillar_name, pillar in data["pillars"].items():
        for criterion in pillar["criteria"]:
            if criterion["status"] == "fail":
                opportunities.append((
                    criterion["id"],
                    criterion["level"],
                    criterion["reason"],
                    pillar_name
                ))

    # Sort by level (ascending) to prioritize foundational issues
    opportunities.sort(key=lambda x: x[1])
    return [(o[0], o[2], o[3]) for o in opportunities[:n]]


def generate_markdown_report(data: dict, include_diagrams: bool = True) -> str:
    """Generate a full markdown report from analysis data."""
    repo_name = data["repo_name"]
    pass_rate = data["pass_rate"]
    achieved = data["achieved_level"]
    total_passed = data["total_passed"]
    total = data["total_criteria"]
    languages = data.get("languages", ["Unknown"])
    repo_type = data.get("repo_type", "application")
    level_scores = data["level_scores"]

    lines = []

    # Header
    lines.append(f"# Agent Readiness Report: {repo_name}")
    lines.append("")
    lines.append(f"**Languages**: {', '.join(languages)}  ")
    lines.append(f"**Repository Type**: {repo_type}  ")
    lines.append(f"**Pass Rate**: {pass_rate}% ({total_passed}/{total} criteria)  ")
    if achieved > 0:
        lines.append(f"**Achieved Level**: **L{achieved}**")
    else:
        lines.append(f"**Achieved Level**: **Not yet L1** (need 80% at L1)")
    lines.append("")

    # Monorepo app detection info
    detected_apps = data.get("detected_apps", [])
    undetected_folders = data.get("undetected_app_folders", [])
    if repo_type == "monorepo" and detected_apps:
        lines.append("### Detected Applications")
        lines.append("")
        for app in detected_apps:
            app_langs = ", ".join(app.get("languages", ["Unknown"]))
            lines.append(f"- **{app['name']}**: {app_langs}")
        lines.append("")
        if undetected_folders:
            lines.append(f"> **Warning**: Folders without manifest files: {', '.join(undetected_folders)}")
            lines.append("")

    # Level Progress (gated progression - must pass 80% of previous level to unlock)
    lines.append("## Level Progress")
    lines.append("")
    lines.append("| Level | Score | Status |")
    lines.append("|-------|-------|--------|")
    for level in range(1, 6):
        score = level_scores.get(str(level), level_scores.get(level, 0))
        prev_score = level_scores.get(str(level - 1), level_scores.get(level - 1, 100)) if level > 1 else 100
        is_unlocked = level == 1 or prev_score >= 80

        if not is_unlocked:
            lines.append(f"| L{level} | 🔒 | Locked (need 80% at L{level-1}) |")
        elif achieved > 0 and level <= achieved:
            lines.append(f"| L{level} | {score:.0f}% | ✓ Achieved |")
        elif score >= 80:
            lines.append(f"| L{level} | {score:.0f}% | Passed |")
        else:
            lines.append(f"| L{level} | {score:.0f}% | {80-score:.0f}% to go |")
    lines.append("")

    # Visual Summary (Mermaid diagrams)
    if include_diagrams:
        lines.append(generate_visual_summary_mermaid(data))
        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")

    # Strengths
    strengths = get_top_strengths(data)
    if strengths:
        lines.append("### Strengths")
        lines.append("")
        for pillar_name, pct, passing in strengths:
            if passing:
                passing_str = ", ".join(f"`{p}`" for p in passing)
                lines.append(f"- **{pillar_name}** ({pct}%): {passing_str}")
            else:
                lines.append(f"- **{pillar_name}** ({pct}%)")
        lines.append("")

    # Opportunities
    opportunities = get_top_opportunities(data)
    if opportunities:
        lines.append("### Priority Improvements")
        lines.append("")
        lines.append("| Criterion | Issue | Pillar |")
        lines.append("|-----------|-------|--------|")
        for crit_id, reason, pillar in opportunities:
            lines.append(f"| `{crit_id}` | {reason} | {pillar} |")
        lines.append("")

    # Detailed Results
    lines.append("## Detailed Results")
    lines.append("")

    for pillar_name, pillar in data["pillars"].items():
        pct = pillar["percentage"]
        passed = pillar["passed"]
        total = pillar["total"]

        lines.append(f"### {pillar_name}")
        lines.append(f"**Score**: {passed}/{total} ({pct}%)")
        lines.append("")
        lines.append("| Status | Criterion | Score | Details |")
        lines.append("|--------|-----------|-------|---------|")

        for criterion in pillar["criteria"]:
            status = criterion["status"]
            if status == "pass":
                icon = "✓"
            elif status == "fail":
                icon = "✗"
            else:
                icon = "—"

            crit_id = criterion["id"]
            score = criterion["score"]
            reason = criterion["reason"]
            scope = criterion.get("scope", "repo")
            app_results = criterion.get("app_results", {})

            # Add scope indicator and app breakdown for app-scoped criteria
            if scope == "app" and app_results:
                failing_apps = [name for name, passed in app_results.items() if not passed]
                # Clean reason (remove existing failing list if present)
                clean_reason = reason.split(" (failing:")[0]
                if failing_apps:
                    app_detail = f" *(failing: {', '.join(failing_apps)})*"
                else:
                    app_detail = " *(all apps pass)*"
                lines.append(f"| {icon} | `{crit_id}` | {score} | {clean_reason}{app_detail} |")
            else:
                lines.append(f"| {icon} | `{crit_id}` | {score} | {reason} |")

        lines.append("")

    # Recommendations
    lines.append("## Recommended Next Steps")
    lines.append("")

    if achieved < 2:
        lines.append("**Focus on L1/L2 Foundations:**")
        lines.append("1. Add missing linter and formatter configurations")
        lines.append("2. Document build and test commands in README")
        lines.append("3. Set up pre-commit hooks for fast feedback")
        lines.append("4. Create AGENTS.md with project context for AI agents")
    elif achieved < 3:
        lines.append("**Progress to L3 (Production Ready):**")
        lines.append("1. Add integration/E2E tests")
        lines.append("2. Set up test coverage thresholds")
        lines.append("3. Configure devcontainer for reproducible environments")
        lines.append("4. Add automated PR review tooling")
    else:
        lines.append("**Optimize for L4+:**")
        lines.append("1. Implement complexity analysis and dead code detection")
        lines.append("2. Set up flaky test detection and quarantine")
        lines.append("3. Add security scanning (CodeQL, Snyk)")
        lines.append("4. Configure deployment observability")

    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated from repository analysis*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Agent Readiness report from analysis"
    )
    parser.add_argument(
        "--analysis-file", "-a",
        default="/tmp/readiness_analysis.json",
        help="Path to analysis JSON file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format (markdown with Mermaid diagrams, or self-contained HTML)"
    )
    parser.add_argument(
        "--no-diagrams",
        action="store_true",
        help="Disable inline Mermaid diagrams in markdown report"
    )
    parser.add_argument(
        "--summary", "-s",
        help="Executive summary text to include in HTML report (typically generated by agent)"
    )

    args = parser.parse_args()

    # Load analysis
    analysis_path = Path(args.analysis_file)
    if not analysis_path.exists():
        print(f"Analysis file not found: {args.analysis_file}")
        print("Run analyze_repo.py first to generate the analysis.")
        return 1

    data = json.loads(analysis_path.read_text())

    # Generate report
    if args.format == "markdown":
        report = generate_markdown_report(data, include_diagrams=not args.no_diagrams)
    else:  # html
        report = generate_html_report(data, summary=args.summary)

    # Output
    if args.output:
        Path(args.output).write_text(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    exit(main())
