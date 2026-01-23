#!/usr/bin/env python3
"""
Mermaid diagram generators for Agent Readiness Reports.

Generates inline Mermaid diagrams for markdown reports.

Usage:
    from diagrams import (
        pillar_bar_chart_mermaid,
        level_progress_mermaid,
        distribution_pie_mermaid,
        roadmap_flowchart_mermaid,
        generate_visual_summary_mermaid,
    )
"""

# Pillar short names for charts (keep labels concise)
PILLAR_SHORT_NAMES = {
    "Style & Validation": "Style",
    "Build System": "Build",
    "Testing": "Test",
    "Documentation": "Docs",
    "Dev Environment": "DevEnv",
    "Debugging & Observability": "Debug",
    "Security": "Security",
    "Task Discovery": "Tasks",
    "Product & Analytics": "Product",
}


def _get_short_name(pillar_name: str) -> str:
    """Get shortened pillar name for chart labels."""
    return PILLAR_SHORT_NAMES.get(pillar_name, pillar_name[:8])


def pillar_bar_chart_mermaid(pillars: dict) -> str:
    """
    Generate Mermaid xychart for pillar scores comparison.

    Args:
        pillars: Dict of pillar data from analysis JSON

    Returns:
        Mermaid xychart-beta code block
    """
    names = []
    scores = []

    for pillar_name, pillar_data in pillars.items():
        names.append(f'"{_get_short_name(pillar_name)}"')
        scores.append(str(int(pillar_data["percentage"])))

    x_axis = ", ".join(names)
    y_values = ", ".join(scores)

    return f"""```mermaid
xychart-beta
    title "Pillar Scores (%)"
    x-axis [{x_axis}]
    y-axis "Score" 0 --> 100
    bar [{y_values}]
```"""


def level_progress_mermaid(level_scores: dict, achieved_level: int = 0) -> str:
    """
    Generate Mermaid xychart for level progression (L1-L5).

    Args:
        level_scores: Dict of level -> score percentage
        achieved_level: Currently achieved level

    Returns:
        Mermaid xychart-beta code block
    """
    levels = []
    scores = []

    for level in range(1, 6):
        score = level_scores.get(str(level), level_scores.get(level, 0))
        marker = " *" if level <= achieved_level else ""
        levels.append(f'"L{level}{marker}"')
        scores.append(str(int(score)))

    x_axis = ", ".join(levels)
    y_values = ", ".join(scores)

    return f"""```mermaid
xychart-beta
    title "Maturity Level Progress"
    x-axis [{x_axis}]
    y-axis "Completion %" 0 --> 100
    bar [{y_values}]
    line [80, 80, 80, 80, 80]
```"""


def distribution_pie_mermaid(passed: int, failed: int, skipped: int) -> str:
    """
    Generate Mermaid pie chart for pass/fail/skip distribution.

    Args:
        passed: Number of passing criteria
        failed: Number of failing criteria
        skipped: Number of skipped criteria

    Returns:
        Mermaid pie chart code block
    """
    return f"""```mermaid
pie showData
    title Criteria Distribution
    "Pass ({passed})" : {passed}
    "Fail ({failed})" : {failed}
    "Skip ({skipped})" : {skipped}
```"""


def roadmap_flowchart_mermaid(
    current_level: int,
    target_level: int,
    opportunities: list[tuple[str, str, str]],
) -> str:
    """
    Generate Mermaid flowchart for improvement roadmap.

    Args:
        current_level: Currently achieved level (0-5)
        target_level: Target level to achieve
        opportunities: List of (criterion_id, reason, pillar) tuples

    Returns:
        Mermaid flowchart code block
    """
    current_str = f"L{current_level}" if current_level > 0 else "Pre-L1"
    target_str = f"L{target_level}"

    # Build improvement steps (max 4 to keep diagram readable)
    steps = []
    for i, (crit_id, reason, _) in enumerate(opportunities[:4]):
        # Truncate reason for readability
        short_reason = reason[:30] + "..." if len(reason) > 30 else reason
        steps.append((chr(ord("B") + i), crit_id, short_reason))

    # Build flowchart
    lines = ["```mermaid", "flowchart LR"]
    lines.append(f'    A["{current_str}"]')

    prev = "A"
    for node_id, crit_id, reason in steps:
        lines.append(f'    {node_id}["{crit_id}"]')
        lines.append(f"    {prev} --> {node_id}")
        prev = node_id

    final_node = chr(ord("B") + len(steps))
    lines.append(f'    {final_node}(["{target_str}"])')
    lines.append(f"    {prev} --> {final_node}")

    # Add styling
    lines.append(f"    style A fill:#f9f,stroke:#333")
    lines.append(f"    style {final_node} fill:#9f9,stroke:#333")
    lines.append("```")

    return "\n".join(lines)


def generate_visual_summary_mermaid(analysis: dict) -> str:
    """
    Generate complete visual summary section with all Mermaid charts.

    Args:
        analysis: Full analysis JSON data

    Returns:
        Markdown section with all Mermaid diagrams
    """
    pillars = analysis["pillars"]
    level_scores = analysis["level_scores"]
    achieved_level = analysis["achieved_level"]

    # Count criteria
    passed = sum(
        1 for p in pillars.values() for c in p["criteria"] if c["status"] == "pass"
    )
    failed = sum(
        1 for p in pillars.values() for c in p["criteria"] if c["status"] == "fail"
    )
    skipped = sum(
        1 for p in pillars.values() for c in p["criteria"] if c["status"] == "skip"
    )

    # Get opportunities for roadmap
    opportunities = []
    for pillar_name, pillar in pillars.items():
        for criterion in pillar["criteria"]:
            if criterion["status"] == "fail":
                opportunities.append(
                    (criterion["id"], criterion["reason"], pillar_name)
                )
    # Sort by level
    opportunities.sort(
        key=lambda x: next(
            (
                c["level"]
                for p in pillars.values()
                for c in p["criteria"]
                if c["id"] == x[0]
            ),
            99,
        )
    )

    target_level = min(achieved_level + 1, 5) if achieved_level < 5 else 5

    sections = [
        "## Visual Summary",
        "",
        "### Pillar Scores",
        "",
        pillar_bar_chart_mermaid(pillars),
        "",
        "### Level Progress",
        "",
        level_progress_mermaid(level_scores, achieved_level),
        "",
        "### Criteria Distribution",
        "",
        distribution_pie_mermaid(passed, failed, skipped),
        "",
    ]

    # Only add roadmap if there are opportunities
    if opportunities:
        sections.extend(
            [
                "### Improvement Roadmap",
                "",
                roadmap_flowchart_mermaid(achieved_level, target_level, opportunities),
                "",
            ]
        )

    return "\n".join(sections)
